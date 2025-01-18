#Test using 'mgm_v2.h5' final testing
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import win32api
import win32con
import pyautogui
import math

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

# Function to load gesture-to-key mapping from a .txt file
def load_gesture_to_key_mapping(file_path):
    mapping = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:  # Ensure the line contains a valid mapping
                    gesture, key = line.strip().split('=', 1)
                    mapping[gesture] = key
    except FileNotFoundError:
        print(f"Mapping file {file_path} not found. Using default mappings.")
    except Exception as e:
        print(f"Error reading mapping file: {e}")
    return mapping

# Path to the mapping file
mapping_file_path = 'gesture_key_mapping.txt'

# Load gesture-to-key mapping
gesture_to_key = load_gesture_to_key_mapping(mapping_file_path)

# Function to bring up the on-screen keyboard
def open_onscreen_keyboard():
    try:
        os.startfile('osk.exe')  # Launch on-screen keyboard without elevation
    except Exception as e:
        print(f"Failed to open on-screen keyboard: {e}")

# Gesture-to-key mapping
"""gesture_to_key = {
    'call': 'c',            # Clutch
    'dislike': 'q',             # Shift down
    'fist': 'space',            # E-brake
    'like': 'e',                # Shift up
    'ok': 'k',                  # Custom key
    'one': 'w',                 # Acceleratee
    'peace': 'a',               # Steer left
    'peace_inverted': 'd',      # Steer right
    'rock': 'r',                # ANNA Activation
    'stop': 's',                # Decelerate/reverse
    'stop_inverted': 'g',       # Custom key
    'three': '3'                # Custom key
}"""

screen_width, screen_height = pyautogui.size()
cursor_speed = 5
position_displacement = 1.5
previous_base_coord = [0, 0]
is_left_click_held = False

# Cursor D8 Movement function
def dpadCursor(index_x, index_y):
    # Create deadzone
    screen_center_vector = [screen_width / 2, screen_height / 2]
    
    deadzone_width = screen_width / 6
    deadzone_height = screen_height / 6
    deadzone_min_vector = [screen_center_vector[0] - (deadzone_width / 2), screen_center_vector[1] - (deadzone_height / 2)]
    deadzone_max_vector = [screen_center_vector[0] + (deadzone_width / 2), screen_center_vector[1] + (deadzone_height / 2)]
    
    dist_from_center = calculate_distance(screen_center_vector[0], screen_center_vector[1], index_x, index_y)
    current_speed = int(cursor_speed * (dist_from_center/100))
    #print(str(dist_from_center))
    current_cursor_x, current_cursor_y = pyautogui.position()
    
    if not (deadzone_min_vector[0] < index_x < deadzone_max_vector[0] and deadzone_min_vector[1] < index_y < deadzone_max_vector[1]):
        #control the movement of the cursor, similar to a d-pad
        if index_x < deadzone_min_vector[0] and index_y < deadzone_min_vector[1]:                             #top left position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -current_speed, -current_speed, 0, 0)
        if deadzone_min_vector[0] < index_x < deadzone_max_vector[0] and index_y < deadzone_min_vector[1]:    #top middle position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -current_speed, 0, 0)
        if deadzone_max_vector[0] < index_x  and index_y < deadzone_min_vector[1]:                            #top right position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, current_speed, -current_speed, 0, 0)
        if index_x < deadzone_min_vector[0]  and deadzone_min_vector[1] < index_y < deadzone_max_vector[1]:   #middle left position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -current_speed, 0, 0, 0)
        if deadzone_max_vector[0] < index_x  and deadzone_min_vector[1] < index_y < deadzone_max_vector[1]:   #middle right position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, current_speed, 0, 0, 0)
        if index_x < deadzone_min_vector[0] and deadzone_max_vector[1] < index_y:                             #bottom left position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -current_speed, current_speed, 0, 0)
        if deadzone_min_vector[0] < index_x < deadzone_max_vector[0] and deadzone_max_vector[1] < index_y:    #bottom middle position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, current_speed, 0, 0)
        if deadzone_max_vector[0] < index_x  and deadzone_max_vector[1] < index_y:                            #bottom right position
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, current_speed, current_speed, 0, 0)
            
def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
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
                    if is_left_click_held:
                        pyautogui.mouseUp()
                        is_left_click_held = False
                    open_onscreen_keyboard()  # Call the function to open the on-screen keyboard
                elif action == 'mouse_movement':
                    if is_left_click_held:
                        pyautogui.mouseUp()
                        is_left_click_held = False
                    # Get fingertip coordinates and move the mouse
                    index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    
                    # Scale coordinates to the screen
                    index_x = int(index_base.x * screen_width)
                    index_y = int(index_base.y * screen_height)
                    
                    #Functions to move the cursor (Do not run both functions at once!)
                    dpadCursor(index_x, index_y) #Run D8 movement function
                    #positionCursor(index_x, index_y, index_base, previous_base_coord) #Run hand position cursor
                    
                    previous_base_coord = [index_base.x, index_base.y]
                elif action == 'left_click':
                    if not is_left_click_held:
                        pyautogui.mouseDown()
                        is_left_click_held = True
                else:
                    if is_left_click_held:
                        pyautogui.mouseUp()
                        is_left_click_held = False
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
