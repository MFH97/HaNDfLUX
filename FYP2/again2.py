#Test using 'mgm_v2.h5' final testing
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui

# this 2 libraries for the on screen keyboard and more encoding support accross various devices
import os
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# Load the trained model
model = load_model('mgm_v2.h5')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Gesture class-to-name mapping
gesture_names = {
    0: 'call',
    1: 'dislike',
    2: 'fist',
    3: 'like',
    4: 'ok',
    5: 'one',
    6: 'peace',
    7: 'peace_inverted',
    8: 'rock',
    9: 'stop',
    10: 'stop_inverted',
    11: 'three'
}

# Gesture-to-key mapping
gesture_to_key = {
    'call': 'open_keyboard',    # To open the on-screen keyboard
    'dislike': 'q',             # Shift down
    'fist': 'space',            # E-brake
    'like': 'e',                # Shift up
    'ok': 'k',                  # Custom key
    'one': 'w',                 # Accelerate
    'peace': 'a',               # Steer left
    'peace_inverted': 'd',      # Steer right
    'rock': 'r',                # ANNA Activation
    'stop': 's',                # Decelerate/reverse
    'stop_inverted': 'g',       # Custom key
    'three': '3'                # Custom key
}

# Function to bring up the on-screen keyboard
def open_onscreen_keyboard():
    try:
        os.startfile('osk.exe')  # Launch on-screen keyboard without elevation
    except Exception as e:
        print(f"Failed to open on-screen keyboard: {e}")


# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])  # Flatten x, y, z into a single list

            # Convert landmarks to input array
            input_data = np.expand_dims(landmarks, axis=0)  # Shape (1, 63)

            # Predict gesture
            prediction = model.predict(input_data)
            predicted_class = np.argmax(prediction)

            # Get the gesture name
            gesture_name = gesture_names.get(predicted_class, 'Unknown')

            # Perform key action if gesture is mapped to a key
            if gesture_name in gesture_to_key:
                action = gesture_to_key[gesture_name]
                if action == 'open_keyboard':
                    open_onscreen_keyboard()  # Call the function to open the on-screen keyboard
                else:
                    pyautogui.press(action)  # Simulate key press

            # Display the gesture name on the frame
            cv2.putText(frame, f'Gesture: {gesture_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
