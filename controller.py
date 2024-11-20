import warnings
import cv2
import mediapipe as mp
import numpy as np
import pydirectinput
import time
import joblib

# Suppress specific UserWarnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module=r"google\.protobuf\.symbol_database"
)

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Load trained gesture model
MODEL_PATH = "gesture_model.pkl"
gesture_model = joblib.load(MODEL_PATH)

# Constants
THRESHOLD = 0.010  # Velocity threshold for motion detection
KEYS = {
    "Swipe Left": "d",
    "Swipe Right": "j",
    "Gesture_A": "w",
    "Gesture_B": "s"
}

# Tracking variables
prev_landmarks = {"Left": None, "Right": None}
gesture_state = {"Left": None, "Right": None}
current_gesture = "None"  # Variable to store the current gesture
last_executed_time = 0  # To debounce gesture execution
GESTURE_COOLDOWN = 0.1  # Cooldown in seconds

# Motion detection for swipe gestures
def detect_motion(current_landmarks, hand_label):
    global prev_landmarks, gesture_state

    if prev_landmarks[hand_label] is None:
        prev_landmarks[hand_label] = current_landmarks
        return "Idle"

    # Calculate velocity along the x-axis
    prev_x = np.mean([lm[0] for lm in prev_landmarks[hand_label]])
    current_x = np.mean([lm[0] for lm in current_landmarks])
    velocity = current_x - prev_x

    # Update previous landmarks
    prev_landmarks[hand_label] = current_landmarks

    # Determine gesture based on velocity
    if hand_label == "Left" and velocity > THRESHOLD and gesture_state[hand_label] != "Swipe Right":
        gesture_state[hand_label] = "Swipe Right"
        return "Swipe Right"
    elif hand_label == "Right" and velocity < -THRESHOLD and gesture_state[hand_label] != "Swipe Left":
        gesture_state[hand_label] = "Swipe Left"
        return "Swipe Left"
    elif abs(velocity) < THRESHOLD:
        gesture_state[hand_label] = None

    return "Idle"

# Gesture prediction using trained model
def detect_trained_gesture(landmarks):
    global current_gesture

    flat_landmarks = np.array(landmarks).flatten().reshape(1, -1)
    try:
        probabilities = gesture_model.predict_proba(flat_landmarks)
        max_prob = np.max(probabilities)
        predicted_gesture = gesture_model.classes_[np.argmax(probabilities)]

        # Define a confidence threshold (adjust as necessary)
        CONFIDENCE_THRESHOLD = 0.8
        if max_prob >= CONFIDENCE_THRESHOLD:
            current_gesture = predicted_gesture
            return predicted_gesture
        else:
            current_gesture = "None"
            return None
    except Exception as e:
        print(f"[ERROR] Gesture prediction failed: {e}")
        current_gesture = "None"
        return None

# Key execution based on gesture
def execute_gesture(gesture):
    global last_executed_time

    # Check cooldown
    current_time = time.time()
    if current_time - last_executed_time < GESTURE_COOLDOWN:
        return  # Skip execution if in cooldown

    if gesture == "Swipe Left":
        pydirectinput.press(KEYS["Swipe Left"])
    elif gesture == "Swipe Right":
        pydirectinput.press(KEYS["Swipe Right"])
    elif gesture == "right":
        pydirectinput.press(KEYS["Gesture_B"])
    elif gesture == "left":
        pydirectinput.press(KEYS["Gesture_A"])

    # Update last execution time
    last_executed_time = current_time

# Main function
def main():
    global current_gesture

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Starting Controller. Press 'q' to quit.")

    while cap.isOpened():
        start_time = time.time()  # Start timer for response time calculation
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)  # Flip for mirroring
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                hand_label = "Left" if handedness.classification[0].label == "Right" else "Right"
                raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                # Detect swipe motion
                motion = detect_motion(raw_landmarks, hand_label)

                # Detect trained gestures if no swipe motion
                if motion == "Idle":
                    trained_gesture = detect_trained_gesture(raw_landmarks)
                    if trained_gesture:
                        execute_gesture(trained_gesture)
                else:
                    execute_gesture(motion)
                    current_gesture = motion

                # Draw landmarks for visualization
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Calculate response time
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Overlay response time and current gesture on the frame
        cv2.putText(frame, f"Response Time: {response_time:.2f} ms", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Gesture: {current_gesture}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Controller", frame)

        # Quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
