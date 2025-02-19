# Test using 'mgm_v2.h5' final testing
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model
import win32api, win32con
import pydirectinput, pyautogui  # Ensure pyautogui is imported
import math, time

# this 2 libraries for the on-screen keyboard and more encoding support across various devices
import os, sys
#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
base_path = os.getcwd()

modelPath = f"{base_path}\\resources\\mgm_v2.h5"
model = load_model(modelPath)
posRef = 0

with open(f"{base_path}\\resources\\config.ini", "r") as config:
    for items in config:
        if ("posDisplace" in items):
            setGet = items.split("Ã· ")
            posRef = setGet[1].replace("\n","")
    config.close()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Path to the mapping file
mapping_file_path = 'resources/gesture_key_mapping.txt'

# Variables to track gestures and debounce for each hand
last_gesture = {'Left': None, 'Right': None}
last_gesture_time = {'Left': 0, 'Right': 0}
debounce_time_ms = 30  # Adjust the debounce time in milliseconds

screen_width, screen_height = pydirectinput.size()
cursor_speed = 5
position_displacement = float(posRef)
previous_base_coord = [0, 0]
is_left_click_held = False

# Record selected controller
controller_state = "Mouse"
controller_states = ["Mouse", "Keyboard", "Default", "Steering", "Swiping"]
changed_controller = False
c_timer_started = False
c_start_time = 0

# Keyboard emulator variables
selected_key_input = "a"
selected_key_pressed = False
keyboard_selection = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", 
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", 
                     "u", "v", "w", "x", "y", "z",
                     "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
keyboard_timer_started = False
keyboard_start_time = 0

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
    
    if deadzone_dist > 0.005:
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
            with open(f"{base_path}\\resources\\config.ini", "r") as config:
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


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    LEFT_ZONE = 0.42  # Left zone size
    RIGHT_ZONE = 0.58 # Right zone size

    previous_zone = "Idle"
    previous_palm_x = None  # Store the previous x-coordinate
    last_keypress_time = 0  # To prevent repeated key presses
    
    cv2.putText(frame, f'Current Control: {controller_state}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if controller_state == "Keyboard":
        cv2.putText(frame, f'Current key selected: {selected_key_input}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

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
                if c_timer_started == False:
                    c_start_time = time.time()
                    c_timer_started = True
                
                c_end_time = time.time()
                c_length = c_end_time - c_start_time
                
                if c_length >= 1:
                    if handedness == "Right":
                        del controller_states[0]
                        controller_states.append(controller_state)
                        controller_state = controller_states[0]
                        changed_controller = True
                        c_start_time = 0
                        c_timer_started = False
                    if handedness == "Left":
                        controller_state = controller_states[-1]
                        del controller_states[-1]
                        controller_states.insert(0, controller_state)
                        changed_controller = True
                        c_start_time = 0
                        c_timer_started = False
            else:
                c_start_time = 0
                c_timer_started = False
                
            if changed_controller == True and gesture_name != "three":
                c_start_time = 0
                c_timer_started = False
                changed_controller = False
            
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
                        
            if controller_state == "Keyboard" and gesture_name != "three":
                if gesture_name == "stop":
                    if keyboard_timer_started == False:
                        keyboard_start_time = time.time()
                        keyboard_timer_started = True
                    
                    keyboard_end_time = time.time()
                    keyboard_length = keyboard_end_time - keyboard_start_time
                    
                    if keyboard_length >= 0.5:
                        del keyboard_selection[0]
                        keyboard_selection.append(selected_key_input)
                        selected_key_input = keyboard_selection[0]
                        keyboard_start_time = 0
                        keyboard_timer_started = False
                elif gesture_name == "stop_inverted":
                    if keyboard_timer_started == False:
                        keyboard_start_time = time.time()
                        keyboard_timer_started = True
                    
                    keyboard_end_time = time.time()
                    keyboard_length = keyboard_end_time - keyboard_start_time
                    
                    if keyboard_length >= 0.5:
                        selected_key_input = keyboard_selection[-1]
                        del keyboard_selection[-1]
                        keyboard_selection.insert(0, selected_key_input)
                        keyboard_start_time = 0
                        keyboard_timer_started = False
                else:
                    keyboard_start_time = 0
                    keyboard_timer_started = False
                
                if selected_key_pressed == False:
                    if gesture_name == "like" and handedness == "Right":
                        pydirectinput.press(selected_key_input)
                        selected_key_pressed = True
                        
                    if gesture_name == "like" and handedness == "Left":
                        pydirectinput.keyDown("shift")
                        pydirectinput.press(selected_key_input)
                        pydirectinput.keyUp("shift")
                        selected_key_pressed = True
                        
                if selected_key_pressed == True and gesture_name != "like":
                    selected_key_pressed = False

            
             # Add steering logic here                 
            if controller_state == "Steering" and gesture_name != "three":
                # Check if left hand "stop" gesture is performed
                if handedness == "Left" and gesture_name == "stop":
                    pydirectinput.press('s')  # Simulate pressing the 's' key for stop
                    print("Left hand stop gesture detected. Pressing 's' to stop.")

                # Check if left hand "fist" gesture is performed
                if handedness == "Left" and gesture_name == "fist":
                    pydirectinput.press(' ')  # Simulate pressing the ' ' key for spacebar
                    print("Left hand fist gesture detected. Pressing ' ' to Boost.")
                #Right hand steering control
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
                                pydirectinput.keyDown(key)
                                current_right_key = key
                                last_press_time = time.time()
                                print(f"Right hand pressed steering key: {key}")
                            elif time.time() - (last_press_time or 0) > 0.1:
                                pydirectinput.keyDown(key)
                                last_press_time = time.time()
                                print(f"Continuously pressing steering key: {key}")
                        else:
                            release_right_key()# steering ends here

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
                height, width, _ = frame.shape
                left_line_x = int(width * LEFT_ZONE)
                right_line_x = int(width * RIGHT_ZONE)

                hand_landmarks = results.multi_hand_landmarks[0]
                palm_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)

                # Draw zones (unchanged)
                cv2.line(frame, (left_line_x, 0), (left_line_x, height), (255, 0, 0), 2)
                cv2.line(frame, (right_line_x, 0), (right_line_x, height), (0, 0, 255), 2)

                current_time = time.time()

                # Improved Swiping Logic: Check for crossing boundaries
                if previous_palm_x is not None:  # Need a previous value to compare
                    if palm_x < left_line_x and previous_palm_x >= left_line_x:  # Crossed Left
                        if previous_zone != "Left" and current_time - last_keypress_time > 0.1: # Debounce
                            pydirectinput.press('d')
                            print("Left Zone Entered: Pressing 'D'")
                            previous_zone = "Left"
                            last_keypress_time = current_time

                    elif palm_x > right_line_x and previous_palm_x <= right_line_x: # Crossed Right
                        if previous_zone != "Right" and current_time - last_keypress_time > 0.1: # Debounce
                            pydirectinput.press('j')
                            print("Right Zone Entered: Pressing 'J'")
                            previous_zone = "Right"
                            last_keypress_time = current_time

                elif palm_x < left_line_x:
                    if previous_zone != "Left" and current_time - last_keypress_time > 0.1: # Debounce
                        pydirectinput.press('d')
                        print("Left Zone Entered: Pressing 'D'")
                        previous_zone = "Left"
                        last_keypress_time = current_time

                elif palm_x > right_line_x:
                    if previous_zone != "Right" and current_time - last_keypress_time > 0.1: # Debounce
                        pydirectinput.press('j')
                        print("Right Zone Entered: Pressing 'J'")
                        previous_zone = "Right"
                        last_keypress_time = current_time


                else:
                    previous_zone = "Idle"

                previous_palm_x = palm_x  # Update previous position for the next frame

    else:
        c_start_time = 0
        c_timer_started = False
        
        if changed_controller == True:
            changed_controller = False
            
        if controller_state == "Keyboard":
            keyboard_start_time = 0
            keyboard_timer_started = False
            selected_key_pressed = False
        
        if controller_state == "Default":
            pydirectinput.keyUp(key)
        
    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
