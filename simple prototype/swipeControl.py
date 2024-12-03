import cv2
import mediapipe as mp
import numpy as np
import pydirectinput
import time

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Constants
THRESHOLD = 0.010  # Reduced threshold for quicker detection
KEYS = {"Swipe Left": "d", "Swipe Right": "j"}  # Key mappings for gestures

# Tracking variables
prev_landmarks = {"Left": None, "Right": None}
gesture_state = {"Left": None, "Right": None}  # Ensure one trigger per swipe

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
    elif abs(velocity) < THRESHOLD:  # Reset state when hand stops moving significantly
        gesture_state[hand_label] = None

    return "Idle"

def execute_gesture(gesture):
    """
    Execute the gesture if it is mapped to a key.
    """
    if gesture in KEYS:
        print(f"Gesture Detected: {gesture} -> Pressing '{KEYS[gesture]}'")
        pydirectinput.press(KEYS[gesture])  # Press key instantly without separate keyDown/keyUp

def main():
    global current_gesture

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution for faster processing
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Starting Controller. Press 'q' to quit.")

    while cap.isOpened():
        start_time = time.time()  # Start timer for response time calculation
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        start_time = time.time()  # Start timing

        frame = cv2.flip(frame, 1)  # Flip for mirroring effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        gestures = {"Left": "Idle", "Right": "Idle"}  # Default gestures

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                # Adjust handedness to match real-world perspective
                hand_label = "Left" if handedness.classification[0].label == "Right" else "Right"
                raw_landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]

                # Detect motion
                motion = detect_motion(raw_landmarks, hand_label)
                gestures[hand_label] = motion

                # Execute gesture immediately
                if motion != "Idle":
                    execute_gesture(motion)
                    current_gesture = motion

                # (Optional) Draw landmarks on the frame for debugging
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Calculate frame processing time
        elapsed_time_ms = int((time.time() - start_time) * 1000)

        # Display overlay information
        cv2.putText(frame, f"Left Hand: {gestures['Left']}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Right Hand: {gestures['Right']}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Processing Time: {elapsed_time_ms} ms", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Controller", frame)

        # Check for quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
