# Test using 'mgm_v2.h5' final testing
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import win32api
import win32con
import pydirectinput
import pyautogui  # Ensure pyautogui is imported
import math
import time

# this 2 libraries for the on-screen keyboard and more encoding support across various devices
import os
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
base_path = os.getcwd()

#modelPath = f"{base_path}\\resources\\mgm_v2.h5"
modelPath = "mgm_v2.h5"
model = load_model(modelPath)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Path to the mapping file
mapping_file_path = 'resources/gesture_key_mapping.txt'

# Variables to track gestures and debounce for each hand
last_gesture = {'Left': None, 'Right': None}
last_gesture_time = {'Left': 0, 'Right': 0}
debounce_time_ms = 30  # Adjust the debounce time in milliseconds

screen_width, screen_height = pydirectinput.size()
cursor_speed = 5
position_displacement = 1.5
previous_base_coord = [0, 0]
is_left_click_held = False

# Record selected controller
controller_state = "Mouse"
controller_states = ["Mouse", "Default", "Steering", "Swiping"]
changed_controller = False

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

# Load gesture-to-key mapping
gesture_to_key = load_gesture_to_key_mapping(mapping_file_path)

# Access left and right mappings
gesture_to_key_left = gesture_to_key.get('left', {})
gesture_to_key_right = gesture_to_key.get('right', {})

# Function to bring up the on-screen keyboard
def open_onscreen_keyboard():
    try:
        os.startfile('osk.exe')  # Launch on-screen keyboard without elevation
    except Exception as e:
        print(f"Failed to open on-screen keyboard: {e}")

# Cursor Position Movement function  
def positionCursor(index_x, index_y, index_base, previous_base_coord):
    deadzone_dist = calculate_distance(index_base.x, index_base.y, previous_base_coord[0], previous_base_coord[1])
    
    center_pos = [screen_width / 2, screen_height / 2]
    offset_x = int((index_x - center_pos[0]) * position_displacement)
    offset_y = int((index_y - center_pos[1]) * position_displacement)
    
    if deadzone_dist > 0.006:
        # Move cursor
        win32api.SetCursorPos(((index_x + offset_x), (index_y + offset_y)))
            
def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Selecting the webcam function
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
            with open(f"config.ini", "r") as config:
                for items in config:
                    if ("configCam" in items):
                        camUse = items.split("Ã· ")
                        activeCam = camUse[1].replace("\n","")
                        print(activeCam)
                config.close()
            
            # selected_cam = int(input("\nEnter the camera index you want to use: "))
            selected_cam = int(activeCam)
            if selected_cam in available_cameras:
                print(f"Using Camera {selected_cam}")
                return selected_cam
            else:
                print("Invalid selection. Please choose a valid camera index.")
        except ValueError:
            print("Invalid input. Please enter a number.")

current_right_key = None  # Initialize right hand key state
current_left_key = None   # Initialize left hand key state

def determine_thumb_direction(thumb_tip, thumb_ip):
    """Determine the movement direction based on the thumb's tip and intermediate phalanx (IP)."""
    dx = thumb_tip[0] - thumb_ip[0]  # Compare X-coordinates
    dy = thumb_tip[1] - thumb_ip[1]  # Compare Y-coordinates

    sensitivity = 0.05  # Adjust this value for sensitivity

    if abs(dx) > abs(dy) and abs(dy) <= sensitivity:  # Horizontal alignment
        return "w"  # Move forward (upward)
    elif dy > sensitivity:  # Thumb pointing down
        return "a"  # Turn left
    elif dy < -sensitivity:  # Thumb pointing up
        return "d"  # Turn right
    return None  # No valid direction detected

def release_right_key():
    """Release the currently pressed key for the right hand."""
    global current_right_key
    if current_right_key is not None:
        pyautogui.keyUp(current_right_key)
        print(f"Released right key: {current_right_key}")
        current_right_key = None

def release_left_key():
    """Release the currently pressed key for the left hand."""
    global current_left_key
    if current_left_key is not None:
        pyautogui.keyUp(current_left_key)
        print(f"Released left key: {current_left_key}")
        current_left_key = None

# this for calculating the velocity for the swipe gesture to trigger
def calculate_velocity(prev_coords, curr_coords, delta_time):
    velocities = [
        ((c[0] - p[0]) / delta_time) if delta_time > 0 else 0
        for c, p in zip(curr_coords, prev_coords)
    ]
    print(f"Individual Velocities: {velocities}")  # Debugging
    return np.median(velocities) if velocities else 0

# Select the camera
camera_index = select_camera()
cap = cv2.VideoCapture(camera_index)
key = ""

# Initialize swiping variable
is_d_pressed = False
is_k_pressed = False
previous_fingertip_coords = None  # Store previous fingertip positions
previous_time = None
velocity_threshold = 1050 # Adjust this for sensitivity tuning the more you bump it up the faster your hand needs to go
min_distance_threshold = 10  # Ignore tiny jitters
velocity_history = []  # Store last few velocity values for smoothing


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    cv2.putText(frame, f'Current Control: {controller_state}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

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

            # Change controller
            if gesture_name == "three" and changed_controller == False:
                del controller_states[0]
                controller_states.append(controller_state)
                controller_state = controller_states[0]
                changed_controller = True
            
            if controller_state == "Mouse" and gesture_name != "three":
                # Get fingertip coordinates and move the mouse
                index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                # Scale coordinates to the screen
                index_x = int(index_base.x * screen_width)
                index_y = int(index_base.y * screen_height)
                
                # Functions to move the cursor (Do not run both functions at once!)
                positionCursor(index_x, index_y, index_base, previous_base_coord)  # Run hand position cursor
                
                previous_base_coord = [index_base.x, index_base.y]
                
                # Calculate distance between index and thumb
                distance = calculate_distance(index_tip.x, index_tip.y, thumb_tip.x, thumb_tip.y)

                # Click mouse if fingers are close enough
                if distance < 0.05:
                    if not is_left_click_held:
                        pydirectinput.mouseDown()
                        is_left_click_held = True
                else:
                    if is_left_click_held:
                        pydirectinput.mouseUp()
                        is_left_click_held = False
                        
            if controller_state == "Steering" and gesture_name != "three":
                # Add steering logic here (from your previous code)
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    hand_label = handedness.classification[0].label  # 'Left' or 'Right'

                    if hand_label == "Right":
                        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

                        thumb_tip_coords = (thumb_tip.x, thumb_tip.y)
                        thumb_ip_coords = (thumb_ip.x, thumb_ip.y)
                        distance = np.sqrt((thumb_tip_coords[0] - thumb_ip_coords[0]) ** 2 +
                                           (thumb_tip_coords[1] - thumb_ip_coords[1]) ** 2)

                        if distance < 0.05:  # Adjust proximity threshold
                            continue  # Skip further processing for this hand

                        key = determine_thumb_direction(thumb_tip_coords, thumb_ip_coords)
                        if key in ["w", "a", "d"]:
                            if current_right_key != key:
                                release_right_key()
                                pyautogui.keyDown(key)
                                current_right_key = key
                                last_press_time = time.time()
                                print(f"Right hand pressed steering key: {key}")
                            elif time.time() - (last_press_time or 0) > 0.1:
                                pyautogui.keyDown(key)
                                last_press_time = time.time()
                                print(f"Continuously pressing steering key: {key}")
                        else:
                            release_right_key()

            if controller_state == "Default" and gesture_name != "three":
                # Process gesture and trigger actions
                current_time = time.time() * 1000  # Current time in milliseconds

                if gesture_name == last_gesture[handedness]:
                    if current_time - last_gesture_time[handedness] > debounce_time_ms:
                        if handedness == 'Left' and gesture_name in gesture_to_key_left:
                            key = gesture_to_key_left[gesture_name]
                            if key == 'open_keyboard':
                                open_onscreen_keyboard()
                            else:
                                pydirectinput.keyDown(key)
                            
                            print(f"Left Hand - Pressed key: {key}")
                        elif handedness == 'Right' and gesture_name in gesture_to_key_right:
                            key = gesture_to_key_right[gesture_name]
                            if key == 'open_keyboard':
                                open_onscreen_keyboard()
                            else:
                                pydirectinput.keyDown(key)

                            print(f"Right Hand - Pressed key: {key}")
                        last_gesture_time[handedness] = current_time
                else:
                    pydirectinput.keyUp(key)
                    last_gesture[handedness] = gesture_name
                    last_gesture_time[handedness] = current_time

                # Display the gesture name on the frame
                cv2.putText(frame, f'Gesture: {gesture_name}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Draw landmarks on the hand
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # The Swiping logic here
            if controller_state == "Swiping" and gesture_name != "three":
                for hand_landmarks in results.multi_hand_landmarks:
                    wrist_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * screen_width)

                    # Use index fingertip for more accuracy
                    index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    fingertip_coords = [(int(index_fingertip.x * screen_width) - wrist_x, 
                                        int(index_fingertip.y * screen_height))]

                    current_time = time.time()

                    if previous_fingertip_coords is not None and previous_time is not None:
                        delta_time = max(current_time - previous_time, 0.001)  # Prevent division by zero

                        # Calculate velocity (change in x over time)
                        velocities = [
                            ((c[0] - p[0]) / delta_time) if delta_time > 0 else 0
                            for c, p in zip(fingertip_coords, previous_fingertip_coords)
                        ]
                        velocity_x = np.mean(velocities) if velocities else 0  # Moving average for stability

                        # ** Fast Direction Locking Without Delay **
                        if velocity_x < -velocity_threshold:
                            if not is_d_pressed:  # Only press if it's not already pressed
                                pydirectinput.press('d')  
                                print("Swiped Left: Pressing 'D'")
                            is_d_pressed = True
                            is_k_pressed = False

                        elif velocity_x > velocity_threshold:
                            if not is_k_pressed:  # Only press if it's not already pressed
                                pydirectinput.press('j')
                                print("Swiped Right: Pressing 'J'")
                            is_k_pressed = True
                            is_d_pressed = False

                        else:
                            is_d_pressed = False
                            is_k_pressed = False

                    # Update previous positions and time
                    previous_fingertip_coords = fingertip_coords
                    previous_time = current_time

                    # Add minimal sleep to prevent freezing
                    time.sleep(0.0001)

    else:
        if changed_controller == True:
            changed_controller = False
        
        if controller_state == "Default":
            pydirectinput.keyUp(key)
        
    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
