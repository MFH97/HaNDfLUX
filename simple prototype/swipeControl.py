import os
import warnings
import cv2
import mediapipe as mp
import numpy as np
import pydirectinput
import time


# Suppress logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')

print(f"Started Swipe Motion Gesture Control with PID: {os.getpid()}")

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Constants
BASE_THRESHOLD = 0.01
MIN_THRESHOLD = 0.006
ADAPTIVE_WINDOW = 20
THRESHOLD_RESTORE_RATE = 0.0005
IDLE_TIMEOUT = 1.0
LOG_FILE = "gesture_log.txt"
KEYS = {"Swipe Left": "d", "Swipe Right": "j"}
TREND_WINDOW = 50  # Number of gestures to analyze trends
SWIPE_COOLDOWN = 0.3  # Minimum time between swipes
SPAM_WINDOW = 0.5  # Allow spamming gestures within this time window

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


def main():
    """Main function."""
    global adaptive_threshold

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
                gestures[hand_label] = motion
                if motion in KEYS:
                    execute_gesture(motion, hand_label)

                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.putText(frame, f"Left Hand: {gestures['Left']}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Hand: {gestures['Right']}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Adaptive Sensitivity: {adaptive_threshold:.4f}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Gesture Controller", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print("Log file cleared.")


if __name__ == "__main__":
    main()
