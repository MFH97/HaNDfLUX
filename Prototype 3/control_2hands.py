# MediaPipe x Gesture Recognition for Two Hands
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import pydirectinput
import traceback
import time

# Load the saved Keras model for gesture recognition
model = load_model('twoHands_model.h5')  # This model is trained on landmarks

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

# Gesture class names (corresponding to your model's output)
class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Increase max hands to 2 for detecting both hands
mp_drawing = mp.solutions.drawing_utils

# Track the currently pressed key
current_key = None
last_pressed_time = time.time()
min_press_interval = 1  # Minimum interval between key presses in seconds

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to preprocess landmarks for gesture classification
def preprocess_landmarks(landmarks):
    # Convert the landmarks into a flattened array
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()

    # Normalize the landmarks by subtracting the wrist (landmark 0) coordinates
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    flattened_landmarks = flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)

    return flattened_landmarks

# Function to release the current key
def release_current_key():
    global current_key
    if current_key is not None:
        print(f"Releasing key: {current_key}")
        pydirectinput.keyUp(current_key)  # Release the key that was being held down
        current_key = None

# Main loop for hand gesture detection and processing
frame_count = 0  # Track frame count to see how long the program runs
last_frame_time = time.time()
consistent_gesture = [None, None]  # Track consistent gestures for both hands
consistent_frames = [0, 0]  # Track how many consecutive frames detected the same gesture per hand
required_consistent_frames = 5  # Require at least 5 consecutive frames to trigger the same gesture
confidence_threshold = 0.8  # Set a confidence threshold for gesture prediction

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Failed to grab frame at frame count {frame_count}. Webcam might have disconnected.")
            break  # Terminate only if frame grabbing repeatedly fails

        frame = cv2.flip(frame, 1)  # Flip the frame for a mirror-like view
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB for MediaPipe
        results = hands.process(frame_rgb)  # Process the frame for hand detection

        frame_count += 1  # Increment frame count
        current_time = time.time()
        elapsed_time = current_time - last_frame_time

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Preprocess the landmarks for gesture recognition
                landmarks = preprocess_landmarks(hand_landmarks.landmark)

                # Reshape for model input (1, 63)
                input_data = np.expand_dims(landmarks, axis=0)

                # Run inference using the gesture recognition model
                prediction = model.predict(input_data)
                predicted_class = np.argmax(prediction[0])
                predicted_gesture = class_names[predicted_class]
                confidence = np.max(prediction[0])

                # Check confidence and require consistency across multiple frames
                if confidence > confidence_threshold:  # Only accept predictions above the threshold
                    # Check if the gesture is consistent over multiple frames
                    if predicted_gesture == consistent_gesture[idx]:
                        consistent_frames[idx] += 1
                    else:
                        consistent_gesture[idx] = predicted_gesture
                        consistent_frames[idx] = 1

                    if consistent_frames[idx] >= required_consistent_frames:
                        label = f"Hand {idx+1}: {predicted_gesture} ({confidence:.2f})"

                        # Only press a new key if enough time has passed
                        if predicted_gesture in gesture_to_key and current_time - last_pressed_time > min_press_interval:
                            new_key = gesture_to_key[predicted_gesture]

                            # Only press and hold the new key if it's different from the current one
                            if current_key != new_key:
                                release_current_key()  # Release the previous key if there was one
                                print(f"Pressing key: {new_key}")
                                pydirectinput.keyDown(new_key)  # Hold down the new key
                                current_key = new_key
                                last_pressed_time = current_time  # Update the time of the last press
                else:
                    label = f"Hand {idx+1}: No valid gesture"
                    release_current_key()

                # Draw hand landmarks and label
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.putText(
                    frame,
                    label,
                    (10, 40 + idx * 30),  # Offset text position for multiple hands
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )
        else:
            # No hand detected, release the current key
            release_current_key()

        # Display the frame
        cv2.imshow('Hand Gesture Recognition', frame)

        # Ensure the OpenCV window is updated and handles key events
        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit the loop
            break

        # Reset time for the next frame
        last_frame_time = current_time

    except Exception as e:
        print(f"Error during processing at frame {frame_count}: {e}")
        traceback.print_exc()

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
