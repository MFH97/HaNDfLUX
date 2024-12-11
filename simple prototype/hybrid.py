import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import pydirectinput
import pyautogui
import time
import signal
import sys
import atexit

# Termination flag
terminate_flag = False

# Signal handler for termination
def signal_handler(sig, frame):
    global terminate_flag
    terminate_flag = True
    print("Termination signal received, shutting down...")

# Cleanup function to release resources
def cleanup():
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    release_current_key()
    print("Resources released, program exiting.")

# Register cleanup for exit events
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup)

# Load the saved Keras model for gesture recognition
model = load_model('twoHands_model.h5')  # Ensure the model file exists

# Gesture-to-key mapping for the left hand
gesture_to_key = {
    #'one': 'w',  # Accelerate
    'stop': 's',  # Decelerate/reverse
    #'peace': 'a',  # Steer left
    #'peace_inverted': 'd',  # Steer right
    #'like': 'e',  # Shift up
    #'dislike': 'q',  # Shift down
    'fist': 'space',  # E-brake
    #'call': 'shift',  # Clutch
    #'rock': 'c'  # ANNA Activation
}

class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Increase max hands to 2
mp_drawing = mp.solutions.drawing_utils

# Track the currently pressed key for the left hand
current_left_key = None

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit(1)

def preprocess_landmarks(landmarks):
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    flattened_landmarks = flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)
    return flattened_landmarks

def release_left_key():
    global current_left_key
    if current_left_key is not None:
        print(f"Releasing left hand key: {current_left_key}")
        pydirectinput.keyUp(current_left_key)
        current_left_key = None

def determine_direction(wrist, index_tip):
    dx = index_tip[0] - wrist[0]
    dy = index_tip[1] - wrist[1]

    if abs(dy) > abs(dx):  # Vertical movement is dominant
        if dy < 0:
            return "w"  # Move Forward
        else:
            return "s"  # Move Downward
    else:  # Horizontal movement is dominant
        if dx > 0:
            return "d"  # Move Right
        else:
            return "a"  # Move Left

# Main loop
frame_count = 0
consistent_gesture = [None, None]
consistent_frames = [0, 0]
required_consistent_frames = 5
confidence_threshold = 0.8

while not terminate_flag:
    try:
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to grab frame at frame count {frame_count}.")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        frame_count += 1

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, (hand_landmarks, handedness) in enumerate(zip(results.multi_hand_landmarks, results.multi_handedness)):
                hand_label = handedness.classification[0].label  # 'Left' or 'Right'

                if hand_label == "Right":
                    # WASD control using the right hand
                    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    wrist_coords = (int(wrist.x * frame.shape[1]), int(wrist.y * frame.shape[0]))
                    index_coords = (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0]))

                    key = determine_direction(wrist_coords, index_coords)
                    pyautogui.keyDown(key)
                    time.sleep(0.05)
                    pyautogui.keyUp(key)

                    # Display direction label
                    direction_label = f"Right Hand: {key.upper()}"
                    cv2.putText(frame, direction_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                elif hand_label == "Left":
                    # Gesture recognition using the left hand
                    landmarks = preprocess_landmarks(hand_landmarks.landmark)
                    input_data = np.expand_dims(landmarks, axis=0)
                    prediction = model.predict(input_data)
                    predicted_class = np.argmax(prediction[0])
                    predicted_gesture = class_names[predicted_class]
                    confidence = np.max(prediction[0])

                    if confidence > confidence_threshold:
                        if predicted_gesture in gesture_to_key:
                            new_left_key = gesture_to_key[predicted_gesture]

                            if current_left_key != new_left_key:
                                release_left_key()
                                print(f"Pressing left hand key: {new_left_key}")
                                pydirectinput.keyDown(new_left_key)
                                current_left_key = new_left_key

                        # Display gesture label
                        gesture_label = f"Left Hand: {predicted_gesture} ({confidence:.2f})"
                        cv2.putText(frame, gesture_label, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        release_left_key()

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Gesture Recognition', frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit the loop
            break

    except Exception as e:
        print(f"Error during processing at frame {frame_count}: {e}")
        traceback.print_exc()

cleanup()
