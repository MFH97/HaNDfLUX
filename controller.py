import cv2
import mediapipe as mp
import numpy as np
import pydirectinput
from tensorflow.keras.models import load_model

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Load trained gesture model
MODEL_PATH = "gesture_model.keras"
model = load_model(MODEL_PATH)

# Constants
GESTURES = ["Idle", "Swipe Left", "Swipe Right"]  # Modify based on gestures in the model
THRESHOLD = 0.15  # Sensitivity for detecting motion
KEYS = {"Swipe Left": "d", "Swipe Right": "j"}  # Key mappings for gestures

# Tracking variables
prev_landmarks = {"Left": None, "Right": None}  # Store previous landmarks to calculate movement

def detect_motion(current_landmarks, hand_label):
    """
    Detect swipe motion based on the difference in x-coordinates between current and previous landmarks.
    """
    global prev_landmarks

    if prev_landmarks[hand_label] is None:
        prev_landmarks[hand_label] = current_landmarks
        return "Idle"

    # Calculate movement along the x-axis
    prev_x = np.mean([lm[0] for lm in prev_landmarks[hand_label]])
    current_x = np.mean([lm[0] for lm in current_landmarks])
    delta_x = current_x - prev_x

    # Update previous landmarks
    prev_landmarks[hand_label] = current_landmarks

    # Determine gesture based on movement
    if hand_label == "Left" and delta_x > THRESHOLD:  # Swipe Right (mapped to left hand due to mirroring)
        return "Swipe Right"
    elif hand_label == "Right" and delta_x < -THRESHOLD:  # Swipe Left (mapped to right hand due to mirroring)
        return "Swipe Left"
    return "Idle"

def main():
    cap = cv2.VideoCapture(0)
    print("Starting Controller. Press 'q' to quit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)  # Flip for mirroring effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gestures = {"Left": "Idle", "Right": "Idle"}  # Default to idle

        # Process hand landmarks
        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                # Adjust handedness to match real-world perspective
                hand_label = "Left" if handedness.classification[0].label == "Right" else "Right"
                landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect motion
                motion = detect_motion(landmarks, hand_label)
                gestures[hand_label] = motion

        # Execute gestures
        for hand_label, gesture in gestures.items():
            if gesture in KEYS:
                print(f"{gesture}: Pressing '{KEYS[gesture]}'")
                pydirectinput.press(KEYS[gesture])

        # Display the frame
        cv2.putText(frame, f"Left: {gestures['Left']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right: {gestures['Right']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Controller", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()