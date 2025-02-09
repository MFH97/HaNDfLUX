import os
import warnings
import cv2
import mediapipe as mp
import numpy as np
import pydirectinput
import time, os
from tensorflow.keras.models import load_model


# Suppress logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')

print(f"Started Swipe Motion Gesture Control with PID: {os.getpid()}")

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Load the saved Keras model for gesture recognition
model = load_model('twoHands_model.h5')  # Ensure the model file exists

class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# global variable pause state
is_paused = False
pause_start_time = None

# Default sensitivity values
DEFAULT_BASE_THRESHOLD = 0.01
DEFAULT_MIN_THRESHOLD = 0.01

# Constants
BASE_THRESHOLD = DEFAULT_BASE_THRESHOLD # Increasing the threshold make it not sensitive. Where decreasing it make it more sensitive
MIN_THRESHOLD = DEFAULT_MIN_THRESHOLD # Increasing the threshold make it not sensitive. Where decreasing it make it more sensitive
ADAPTIVE_WINDOW = 20
THRESHOLD_RESTORE_RATE = 0.0005
IDLE_TIMEOUT = 1.0
LOG_FILE = "gesture_log.txt"
SETTINGS_FILE = "sensitivity_settings.txt"
KEYS = {"Swipe Left": "d", "Swipe Right": "j"}
TREND_WINDOW = 50  # Number of gestures to analyze trends
SWIPE_COOLDOWN = 0  # Minimum time between swipes
SPAM_WINDOW = 2  # Allow spamming gestures within this time window

# Tracking variables
prev_landmarks = {"Left": None, "Right": None}
gesture_state = {"Left": None, "Right": None}
swipe_velocities = {"Left": [], "Right": []}
adaptive_threshold = BASE_THRESHOLD
last_motion_time = {"Left": time.time(), "Right": time.time()}
gesture_trends = {"Left": [], "Right": []}
last_swipe_time = {"Left": 0, "Right": 0}
spam_start_time = {"Left": 0, "Right": 0}
spam_count = {"Left": 0, "Right": 0}

# Initialize log file
with open(LOG_FILE, "w") as log_file:
    log_file.write("Gesture Sensitivity Log\n")
    log_file.write("========================\n")


def log_data(data):
    """Log data to the .txt file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(data + "\n")

def preprocess_landmarks(landmarks):
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    flattened_landmarks = flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)
    return flattened_landmarks

def check_pause_gesture(gestures):
    """Check if both hands are performing the 'one' gesture and toggle pause."""
    global is_paused, pause_start_time
    if gestures["Left"] == "one" and gestures["Right"] == "one":
        if pause_start_time is None:
            pause_start_time = time.time()
            print("Pause gesture detected, starting timer...")
        elif time.time() - pause_start_time >= 2.5:  # Time required to hold the gesture
            is_paused = not is_paused
            print("System Paused" if is_paused else "System Resumed")
            pause_start_time = None  # Reset the timer
    else:
        # Reset timer if gesture is interrupted
        if pause_start_time is not None:
            print("Pause gesture interrupted.")
        pause_start_time = None

# this is for determine the user is tired or still on normal state
def analyze_behavior(hand_label):
    """Analyze gesture behavior trends."""
    if len(gesture_trends[hand_label]) < TREND_WINDOW:
        return "Analyzing..."

    velocities = [entry['velocity'] for entry in gesture_trends[hand_label][-TREND_WINDOW:]]
    avg_velocity = np.mean(velocities)
    idle_times = [entry['idle_time'] for entry in gesture_trends[hand_label][-TREND_WINDOW:]]
    avg_idle = np.mean(idle_times)

    if avg_velocity < BASE_THRESHOLD * 0.5 and avg_idle > IDLE_TIMEOUT * 1.5:
        return "Tired"
    elif avg_velocity > BASE_THRESHOLD * 0.7 and avg_idle < IDLE_TIMEOUT:
        return "Deliberate"
    return "Neutral"


def detect_motion(current_landmarks, hand_label):
    """Detect motion and manage adaptive sensitivity."""
    global prev_landmarks, gesture_state, swipe_velocities, adaptive_threshold, last_motion_time, gesture_trends

    if prev_landmarks[hand_label] is None:
        prev_landmarks[hand_label] = current_landmarks
        return "Idle"

    prev_x = np.mean([lm[0] for lm in prev_landmarks[hand_label]])
    current_x = np.mean([lm[0] for lm in current_landmarks])
    velocity = current_x - prev_x

    prev_landmarks[hand_label] = current_landmarks
    swipe_velocities[hand_label].append(abs(velocity))
    if len(swipe_velocities[hand_label]) > ADAPTIVE_WINDOW:
        swipe_velocities[hand_label].pop(0)

    if abs(velocity) < adaptive_threshold / 2:
        if time.time() - last_motion_time[hand_label] > IDLE_TIMEOUT:
            gesture_state[hand_label] = None
            return "Idle"
    else:
        last_motion_time[hand_label] = time.time()

    # This is the adaptive sensitivity behaviour detection logic
    avg_velocity = np.mean(swipe_velocities[hand_label])
    if avg_velocity < adaptive_threshold:
        adaptive_threshold = max(avg_velocity, MIN_THRESHOLD)
        log_data(f"Adjusted threshold down to {adaptive_threshold:.4f} for {hand_label} hand.")
    elif avg_velocity > adaptive_threshold and adaptive_threshold < BASE_THRESHOLD:
        adaptive_threshold = min(adaptive_threshold + THRESHOLD_RESTORE_RATE, BASE_THRESHOLD)
        log_data(f"Adjusted threshold up to {adaptive_threshold:.4f} for {hand_label} hand.")

    # Detect gestures based on refined velocity logic
    if velocity > adaptive_threshold and hand_label == "Left" and gesture_state[hand_label] != "Swipe Right":
        return "Swipe Right"
    elif velocity < -adaptive_threshold and hand_label == "Right" and gesture_state[hand_label] != "Swipe Left":
        return "Swipe Left"

    gesture_state[hand_label] = None

    # Log trends for analysis
    idle_time = time.time() - last_motion_time[hand_label]
    gesture_trends[hand_label].append({"velocity": abs(velocity), "idle_time": idle_time})
    if len(gesture_trends[hand_label]) > TREND_WINDOW:
        gesture_trends[hand_label].pop(0)

    return "Idle"

# this is for executing the swipe gesture
def execute_gesture(gesture, hand_label):
    """Execute gesture actions with spam detection."""
    global last_swipe_time, spam_start_time, spam_count

    current_time = time.time()

    # Prevent excessive spamming
    if current_time - last_swipe_time[hand_label] < SWIPE_COOLDOWN:
        return

    if current_time - spam_start_time[hand_label] > SPAM_WINDOW:
        spam_start_time[hand_label] = current_time
        spam_count[hand_label] = 0

    spam_count[hand_label] += 1
    last_swipe_time[hand_label] = current_time

    # Trigger key press
    if gesture in KEYS:
        print(f"Gesture Detected: {gesture} -> Pressing '{KEYS[gesture]}' (Spam Count: {spam_count[hand_label]})")
        pydirectinput.press(KEYS[gesture])

def save_sensitivity_settings():
    """Save sensitivity settings to a file."""
    with open(SETTINGS_FILE, "w") as settings_file:
        settings_file.write(f"BASE_THRESHOLD={BASE_THRESHOLD}\n")
        settings_file.write(f"MIN_THRESHOLD={MIN_THRESHOLD}\n")
    print("Sensitivity settings saved.")


def load_sensitivity_settings():
    """Load sensitivity settings from a file."""
    global BASE_THRESHOLD, MIN_THRESHOLD
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as settings_file:
            for line in settings_file:
                key, value = line.strip().split("=")
                if key == "BASE_THRESHOLD":
                    BASE_THRESHOLD = float(value)
                elif key == "MIN_THRESHOLD":
                    MIN_THRESHOLD = float(value)
        print("Sensitivity settings loaded.")
    else:
        print("No sensitivity settings file found. Using default values.")


# Load settings at the start
load_sensitivity_settings()

def main():
    """Main function."""
    global adaptive_threshold, is_paused

    adaptive_threshold = BASE_THRESHOLD

    base_path = os.getcwd()
    with open(f"{base_path}\\resources\\config.ini", "r") as config:
        for items in config:
            if "configCam" in items:
                camUse = items.split("Ã· ")
                activeCam = camUse[1].replace("\n","")
        config.close()
    cap = cv2.VideoCapture(int(activeCam))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 60)  # Set FPS to 60

    print("Gesture Controller started. Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gestures = {"Left": "Idle", "Right": "Idle"}

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                hand_label = "Left" if handedness.classification[0].label == "Right" else "Right"
                raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                motion = detect_motion(raw_landmarks, hand_label)
                
                if motion in KEYS and not is_paused:
                    execute_gesture(motion, hand_label)

                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Always check for pause gesture
        check_pause_gesture(gestures)

        # Display status
        status_text = "PAUSED" if is_paused else "ACTIVE"
        cv2.putText(frame, f"System Status: {status_text}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Left Hand: {gestures['Left']}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Hand: {gestures['Right']}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Adaptive Sensitivity: {adaptive_threshold:.4f}", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Gesture Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    save_sensitivity_settings()

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("Log file cleared.")


if __name__ == "__main__":
    main()
