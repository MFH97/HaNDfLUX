import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
import pydirectinput
import time, os

# Load the trained model
model = load_model('mgm_v2.h5')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
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

# Gesture-to-key mapping for left and right hands
gesture_to_key_left = {
    'call': 'shift',
    'dislike': 'q',
    'fist': 'space',
    'like': 'e',
    'ok': 'k',
    'one': 'w',
    'peace': 'a',
    'peace_inverted': 'd',
    'rock': 'c',
    'stop': 's',
    'stop_inverted': 'g',
    'three': '3'
}

gesture_to_key_right = {
    'call': 'r',
    'dislike': 'x',
    'fist': 'n',
    'like': 'v',
    'ok': 'm',
    'one': 'u',
    'peace': 'o',
    'peace_inverted': 'p',
    'rock': 'j',
    'stop': 'k',
    'stop_inverted': 'l',
    'three': ';'
}

# Variables to track gestures and debounce for each hand
last_gesture = {'Left': None, 'Right': None}
last_gesture_time = {'Left': 0, 'Right': 0}
debounce_time_ms = 100  # Adjust the debounce time in milliseconds

# Open webcam
base_path = os.getcwd()
with open(f"{base_path}\\resources\\config.ini", "r") as config:
    for items in config:
        if "configCam" in items:
            camUse = items.split("Ã· ")
            activeCam = camUse[1].replace("\n","")
    config.close()
cap = cv2.VideoCapture(int(activeCam))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Determine handedness
            handedness = results.multi_handedness[i].classification[0].label  # 'Left' or 'Right'
            if handedness == 'Right':
                handedness = 'Left'
            elif handedness == 'Left':
                handedness = 'Right'

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

            # Check if the gesture is stable for the debounce duration
            current_time = time.time() * 1000  # Current time in milliseconds
            if gesture_name == last_gesture[handedness]:
                if current_time - last_gesture_time[handedness] > debounce_time_ms:
                    # Trigger key press based on handedness
                    if handedness == 'Left' and gesture_name in gesture_to_key_left:
                        key = gesture_to_key_left[gesture_name]
                        pydirectinput.press(key)  # Simulate key press for left hand
                        print(f"Left Hand - Pressed key: {key}")
                    elif handedness == 'Right' and gesture_name in gesture_to_key_right:
                        key = gesture_to_key_right[gesture_name]
                        pydirectinput.press(key)  # Simulate key press for right hand
                        print(f"Right Hand - Pressed key: {key}")
                    last_gesture_time[handedness] = current_time  # Reset the timer
            else:
                # Update the gesture and reset the timer for the hand
                last_gesture[handedness] = gesture_name
                last_gesture_time[handedness] = current_time

            # Display the gesture name and handedness on the frame
            cv2.putText(frame, f'{handedness} Hand: {gesture_name}', (10, 30 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
