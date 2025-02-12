#Test using 'mgm_v2.h5' final testing
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import win32api
import win32con
import pydirectinput
import math
import time

# this 2 libraries for the on screen keyboard and more encoding support accross various devices
import os
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
base_path = os.getcwd()

modelPath = f"{base_path}\\resources\\mgm_v2.h5"
model = load_model(modelPath)

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

# Function to load gesture-to-key mapping from a .txt file
def load_gesture_to_key_mapping(file_path):
    mappings = {'left': {}, 'right': {}}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip empty lines or comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse the line in the format: hand:gesture=key
                if ':' in line and '=' in line:
                    hand, rest = line.split(':', 1)
                    gesture, key = rest.split('=', 1)
                    hand = hand.strip().lower()  # Normalize hand to lowercase
                    gesture = gesture.strip()
                    key = key.strip()
                    
                    # Add the mapping to the correct hand
                    if hand in mappings:
                        mappings[hand][gesture] = key
    except FileNotFoundError:
        print(f"Mapping file {file_path} not found. Using default mappings.")
    except Exception as e:
        print(f"Error reading mapping file: {e}")
    return mappings

# Path to the mapping file
mapping_file_path = 'resources/gesture_key_mapping.txt'

# Load gesture-to-key mapping
gesture_to_key = load_gesture_to_key_mapping(mapping_file_path)

# Access left and right mappings
gesture_to_key_left = gesture_to_key.get('left', {})
gesture_to_key_right = gesture_to_key.get('right', {})

# Variables to track gestures and debounce for each hand
last_gesture = {'Left': None, 'Right': None}
last_gesture_time = {'Left': 0, 'Right': 0}
debounce_time_ms = 30  # Adjust the debounce time in milliseconds

# Function to bring up the on-screen keyboard
def open_onscreen_keyboard():
    try:
        os.startfile('osk.exe')  # Launch on-screen keyboard without elevation
    except Exception as e:
        print(f"Failed to open on-screen keyboard: {e}")

screen_width, screen_height = pydirectinput.size()
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
    current_cursor_x, current_cursor_y = pydirectinput.position()
    
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

# Selecting thing the webcam function
def select_camera():
    """Allow the user to choose the webcam to use."""
    print("Searching for available cameras...")
    index = 0
    available_cameras = []
    activeCam = ""
    
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        available_cameras.append(index)
        print(f"Camera {index}: Available")
        cap.release()
        index += 1
    
    if not available_cameras:
        print("No cameras found!")
        sys.exit(1)
        cv2.destroyAllWindows()
    
    print("\nAvailable Cameras:")
    for cam in available_cameras:
        print(f"Camera {cam}")
    
    while True:
        try:
            with open(f"{base_path}\\resources\\config.ini", "r") as config:
                for items in config:
                    if ("configCam" in items):
                        camUse = items.split("Ã· ")
                        activeCam = camUse[1].replace("\n","")
                        print(activeCam)
                config.close()
            
            #selected_cam = int(input("\nEnter the camera index you want to use: "))
            selected_cam = int(activeCam)
            if selected_cam in available_cameras:
                print(f"Using Camera {selected_cam}")
                return selected_cam
            else:
                print("Invalid selection. Please choose a valid camera index.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Select the camera
camera_index = select_camera()
cap = cv2.VideoCapture(camera_index)
key = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Determine handedness directly from MediaPipe results
            handedness = results.multi_handedness[i].classification[0].label  # 'Left' or 'Right'
            
            # Extract landmarks and process them
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

            # Process gesture and trigger actions
            current_time = time.time() * 1000  # Current time in milliseconds

            # Check gesture against previous gesture and debounce if necessary
            if gesture_name == last_gesture[handedness]:
                if current_time - last_gesture_time[handedness] > debounce_time_ms:
                    # Trigger action for the gesture
                    if handedness == 'Left' and gesture_name in gesture_to_key_left:
                        key = gesture_to_key_left[gesture_name]
                        if key == 'open_keyboard':
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            open_onscreen_keyboard()  # Open the on-screen keyboard
                        elif key == 'mouse_movement':
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            # Get fingertip coordinates and move the mouse
                            index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                            index_x = int(index_base.x * screen_width)
                            index_y = int(index_base.y * screen_height)
                            dpadCursor(index_x, index_y)  # Run the D8 movement function
                            previous_base_coord = [index_base.x, index_base.y]
                        elif key == 'left_click':
                            if not is_left_click_held:
                                pydirectinput.mouseDown()
                                is_left_click_held = True
                        else:
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            pydirectinput.keyDown(key)  # Simulate key press
                        
                        print(f"Left Hand - Pressed key: {key}")
                    elif handedness == 'Right' and gesture_name in gesture_to_key_right:
                        key = gesture_to_key_right[gesture_name]
                        if key == 'open_keyboard':
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            open_onscreen_keyboard()  # Open the on-screen keyboard
                        elif key == 'mouse_movement':
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            # Get fingertip coordinates and move the mouse
                            index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                            index_x = int(index_base.x * screen_width)
                            index_y = int(index_base.y * screen_height)
                            dpadCursor(index_x, index_y)  # Run the D8 movement function
                            previous_base_coord = [index_base.x, index_base.y]
                        elif key == 'left_click':
                            if not is_left_click_held:
                                pydirectinput.mouseDown()
                                is_left_click_held = True
                        else:
                            if is_left_click_held:
                                pydirectinput.mouseUp()
                                is_left_click_held = False
                            pydirectinput.keyDown(key)  # Simulate key press

                        print(f"Right Hand - Pressed key: {key}")
                    last_gesture_time[handedness] = current_time  # Reset the timer
            else:
                # Update the gesture and reset the timer for the hand
                pydirectinput.keyUp(key)
                last_gesture[handedness] = gesture_name
                last_gesture_time[handedness] = current_time

            # Display the gesture name on the frame
            cv2.putText(frame, f'Gesture: {gesture_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Draw landmarks on the hand
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        pydirectinput.keyUp(key)
        
    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
