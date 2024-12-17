# MediaPipe x Gesture Recognition for Two Hands
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model #type: ignore
import os
import pydirectinput
import traceback
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
    global cap
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    release_current_key()
    print("Resources released, program exiting.")

# Register cleanup for exit events
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup)

#default_path = os.getcwd()
#model_path = default_path + r"\twoHands_model.h5"

# Load the saved Keras model for gesture recognition
model = load_model('twoHands_model.h5')  # Ensure the model file exists

# Gesture-to-key mapping
gesture_to_key = {
    'one': 'w',  # Accelerate
    'stop': 's',  # Decelerate/reverse
    'peace': 'a',  # Steer left
    'peace_inverted': 'd',  # Steer right
    'like': 'e',  # Shift up
    'dislike': 'q',  # Shift down
    'fist': 'space',  # E-brake
    'call': 'shift',  # Clutch
    'rock': 'c'  # ANNA Activation
}

class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Increase max hands to 2
mp_drawing = mp.solutions.drawing_utils

# Track the currently pressed key
current_key = None
last_pressed_time = time.time()
min_press_interval = 1  # Minimum interval between key presses in seconds

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

def release_current_key():
    global current_key
    if current_key is not None:
        print(f"Releasing key: {current_key}")
        pydirectinput.keyUp(current_key)
        current_key = None

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

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                landmarks = preprocess_landmarks(hand_landmarks.landmark)
                input_data = np.expand_dims(landmarks, axis=0)
                prediction = model.predict(input_data)
                predicted_class = np.argmax(prediction[0])
                predicted_gesture = class_names[predicted_class]
                confidence = np.max(prediction[0])

                if confidence > confidence_threshold:
                    if predicted_gesture == consistent_gesture[idx]:
                        consistent_frames[idx] += 1
                    else:
                        consistent_gesture[idx] = predicted_gesture
                        consistent_frames[idx] = 1

                    if consistent_frames[idx] >= required_consistent_frames:
                        label = f"Hand {idx+1}: {predicted_gesture} ({confidence:.2f})"

                        if predicted_gesture in gesture_to_key and time.time() - last_pressed_time > min_press_interval:
                            new_key = gesture_to_key[predicted_gesture]

                            if current_key != new_key:
                                release_current_key()
                                print(f"Pressing key: {new_key}")
                                pydirectinput.keyDown(new_key)
                                current_key = new_key
                                last_pressed_time = time.time()
                else:
                    label = f"Hand {idx+1}: No valid gesture"
                    release_current_key()

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, label, (10, 40 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            release_current_key()

        cv2.imshow('Hand Gesture Recognition', frame)
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit the loop
            break

    except Exception as e:
        print(f"Error during processing at frame {frame_count}: {e}")
        traceback.print_exc()

cleanup()
