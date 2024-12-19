# File: hand_control.py
import cv2
import numpy as np
import mediapipe as mp
import pydirectinput
import pyautogui
from tensorflow.keras.models import load_model
import time

# Load the gesture recognition model
model = load_model('twoHands_model.h5')

# Gesture-to-key mapping (Left Hand)
gesture_to_key = {
    'stop': 's',       # Key for "stop" gesture
    'fist': 'space',   # Key for "fist" gesture
}

# Supported gestures
class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Process both hands
mp_drawing = mp.solutions.drawing_utils

# Track state for both hands
current_left_key = None
current_right_key = None
last_left_press_time = None
last_right_press_time = None

def release_left_key():
    """Release the currently pressed key for the left hand."""
    global current_left_key
    if current_left_key is not None:
        pydirectinput.keyUp(current_left_key)
        print(f"Released left key: {current_left_key}")
        current_left_key = None

def release_right_key():
    """Release the currently pressed key for the right hand."""
    global current_right_key
    if current_right_key is not None:
        pyautogui.keyUp(current_right_key)
        print(f"Released right key: {current_right_key}")
        current_right_key = None

def preprocess_landmarks(landmarks):
    """Preprocess hand landmarks for the gesture model."""
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    return flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)

def determine_knuckle_tilt(index_knuckle, pinky_knuckle):
    """Determine the movement direction based on the knuckle positions of the middle finger and pinky."""
    dx = pinky_knuckle[0] - index_knuckle[0]  # Compare X-coordinates
    dy = pinky_knuckle[1] - index_knuckle[1]  # Compare Y-coordinates

    if abs(dy) <= 0.05:  # Horizontal alignment
        return "w"
    elif dy > 0.05:  # Line tilts to the right
        return "d"
    elif dy < -0.05:  # Line tilts to the left
        return "a"
    return None  # No valid direction detected

# Webcam setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_time = time.time()

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_label = handedness.classification[0].label  # 'Left' or 'Right'

            if hand_label == "Right":
                # Knuckle-based WASD control for the right hand
                middle_knuckle = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
                pinky_knuckle = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

                middle_coords = (middle_knuckle.x, middle_knuckle.y)
                pinky_coords = (pinky_knuckle.x, pinky_knuckle.y)

                key = determine_knuckle_tilt(middle_coords, pinky_coords)

                # Right hand can only trigger 'w', 'a', or 'd'
                if key in ["w", "a", "d"]:
                    if current_right_key != key:
                        release_right_key()
                        pyautogui.keyDown(key)
                        current_right_key = key
                        print(f"Right hand pressed key: {key}")
                    elif current_time - (last_right_press_time or 0) > 0.1:
                        pyautogui.keyDown(key)
                        last_right_press_time = current_time
                else:
                    release_right_key()

            elif hand_label == "Left":
                # Gesture-based control for the left hand
                landmarks = preprocess_landmarks(hand_landmarks.landmark)
                input_data = np.expand_dims(landmarks, axis=0)
                prediction = model.predict(input_data)
                predicted_class = np.argmax(prediction[0])
                predicted_gesture = class_names[predicted_class]
                confidence = np.max(prediction[0])

                if confidence > 0.8 and predicted_gesture in gesture_to_key:
                    key = gesture_to_key[predicted_gesture]

                    # Press and hold the new gesture key
                    if current_left_key != key:
                        release_left_key()
                        pydirectinput.keyDown(key)
                        current_left_key = key
                        print(f"Left hand pressed key: {key}")
                    elif current_time - (last_left_press_time or 0) > 0.1:
                        pydirectinput.keyDown(key)
                        last_left_press_time = current_time

                else:
                    release_left_key()

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        # Release keys if no hands are detected
        release_left_key()
        release_right_key()

    # Display the frame
    cv2.imshow('Gesture Recognition', frame)

    # Exit loop on 'Esc' key press
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
release_left_key()
release_right_key()
cap.release()
cv2.destroyAllWindows()
