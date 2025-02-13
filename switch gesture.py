import os
import time
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import pydirectinput

# Load the trained model
model = load_model("mgm_v2.h5")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Gesture class mapping
gesture_names = {
    0: 'call',
    1: 'dislike',
    2: 'fist',
    3: 'like',
    4: 'ok',
    5: 'one',
    6: 'peace',
    7: 'peace_inverted',
    8: 'rock',  # Assigned to cycle controllers
    9: 'stop',
    10: 'stop_inverted',
    11: 'three'
}

# Define available controllers
controllers = ["game", "mouse", "steering"]
current_controller_index = 0  # Start with game controller
controller_hold_start = None
gesture_to_switch = "rock"  # Gesture used to cycle controllers
hold_time_threshold = 3  # Seconds to switch controller

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            input_data = np.expand_dims(landmarks, axis=0)
            prediction = model.predict(input_data)
            predicted_class = np.argmax(prediction)
            gesture_name = gesture_names.get(predicted_class, "Unknown")

            # Check if the cycling gesture is being held
            if gesture_name == gesture_to_switch:
                if controller_hold_start is None:
                    controller_hold_start = current_time  # Start tracking time

                elif current_time - controller_hold_start >= hold_time_threshold:
                    # Cycle to the next controller
                    current_controller_index = (current_controller_index + 1) % len(controllers)
                    selected_controller = controllers[current_controller_index]
                    print(f"Switching to {selected_controller} control...")

                    # Restart with the new controller script
                    if selected_controller == "mouse":
                        os.system("python MouseControl.py")
                    elif selected_controller == "steering":
                        os.system("python steering2.py")
                    elif selected_controller == "game":
                        os.system("python again2.py")

                    exit()  # Exit current script
            else:
                controller_hold_start = None  # Reset hold timer if gesture is lost

            # Display current controller mode
            cv2.putText(frame, f'Controller: {controllers[current_controller_index]}', 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture-Based Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
