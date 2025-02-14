# File: hand_control.py
import cv2
import numpy as np
import mediapipe as mp
import pydirectinput
import pyautogui
from tensorflow.keras.models import load_model
import time, os

# Load the gesture recognition model
base_path = os.getcwd()
modelPath = f"{base_path}\\resources\\twoHands_model.h5"
model = load_model(modelPath)

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
last_press_time = None

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

def determine_thumb_direction(thumb_tip, thumb_ip):
    """Determine the movement direction based on the thumb's tip and intermediate phalanx (IP)."""
    dx = thumb_tip[0] - thumb_ip[0]  # Compare X-coordinates
    dy = thumb_tip[1] - thumb_ip[1]  # Compare Y-coordinates

    sensitivity = 0.05  # Adjust this value for sensitivity

    if abs(dx) > abs(dy) and abs(dy) <= sensitivity:  # Horizontal alignment
        return "w"
    elif dy > sensitivity:  # Thumb pointing down
        return "a"
    elif dy < -sensitivity:  # Thumb pointing up
        return "d"
    return None  # No valid direction detected

# Webcam setup
with open(f"{base_path}\\resources\\config.ini", "r") as config:
    for items in config:
        if "configCam" in items:
            camUse = items.split("Ã· ")
            activeCam = camUse[1].replace("\n","")
    config.close()
cap = cv2.VideoCapture(int(activeCam))
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

def preprocess_landmarks(landmarks):
    """Preprocess hand landmarks for the gesture model."""
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    return flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)

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
                # Thumb-based WASD control for the right hand
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

                # Calculate distance between thumb tip and thumb IP
                thumb_tip_coords = (thumb_tip.x, thumb_tip.y)
                thumb_ip_coords = (thumb_ip.x, thumb_ip.y)
                distance = np.sqrt((thumb_tip_coords[0] - thumb_ip_coords[0]) ** 2 +
                                   (thumb_tip_coords[1] - thumb_ip_coords[1]) ** 2)

                # Release keys if thumb tip is close to thumb IP
                if distance < 0.05:  # Adjust proximity threshold
                    release_right_key()
                    print("Right hand keys released due to thumb proximity.")
                    continue  # Skip further processing for this hand

                # Thumb-based control
                key = determine_thumb_direction(thumb_tip_coords, thumb_ip_coords)

                # Right hand can only trigger 'w', 'a', or 'd'
                press_interval = 0.1  # Time in seconds between presses (adjust for frequency)
                if key in ["w", "a", "d"]:
                    if current_right_key != key:
                        release_right_key()
                        pyautogui.keyDown(key)
                        current_right_key = key
                        last_press_time = current_time
                        print(f"Right hand pressed key: {key}")
                    elif current_time - (last_press_time or 0) > press_interval:
                        pyautogui.keyDown(key)
                        last_press_time = current_time
                        print(f"Continuously pressing: {key}")
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
                    else:
                        pydirectinput.keyDown(key)  # Ensure continuous press
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
