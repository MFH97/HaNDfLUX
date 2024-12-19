import cv2
import mediapipe as mp
import win32api
import win32con
import pyautogui
import math
import signal
import sys
import atexit

# Global termination flag
terminate_flag = False

# Signal handler for termination
def signal_handler(sig, frame):
    global terminate_flag
    terminate_flag = True
    print("Termination signal received, shutting down...")

# Cleanup function
def cleanup():
    if video.isOpened():
        video.release()
    cv2.destroyAllWindows()
    print("Resources released, program exiting.")

# Register cleanup for exit
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
atexit.register(cleanup)

# Initialize Mediapipe and webcam
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Error: Could not access the webcam.")
    sys.exit(1)

screen_width, screen_height = pyautogui.size()
cursor_speed = 5
position_displacement = 1.5
previous_base_coord = [0, 0]

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
        
#Cursor Postion Movement function  
def positionCursor(index_x, index_y, index_base, previous_base_coord):
    deadzone_dist = calculate_distance(index_base.x, index_base.y, previous_base_coord[0], previous_base_coord[1])
    #print(str(deadzone_dist))
    
    center_pos = [screen_width / 2, screen_height / 2]
    offset_x = int((index_x - center_pos[0]) * position_displacement)
    offset_y = int((index_y - center_pos[1]) * position_displacement)
    
    if deadzone_dist > 0.006:
        #Move cursor
        win32api.SetCursorPos(((index_x + offset_x), (index_y + offset_y)))

def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

is_left_click_held = False

# Process video frames
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
    while video.isOpened() and not terminate_flag:
        ret, frame = video.read()
        if not ret:
            print("Error: Failed to capture video frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        image_height, image_width, _ = frame.shape

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get fingertip coordinates and move the mouse
                index_base = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                # Scale coordinates to the screen
                index_x = int(index_base.x * screen_width)
                index_y = int(index_base.y * screen_height)
                
                #Functions to move the cursor (Do not run both functions at once!)
                dpadCursor(index_x, index_y) #Run D8 movement function
                #positionCursor(index_x, index_y, index_base, previous_base_coord) #Run hand position cursor
                
                previous_base_coord = [index_base.x, index_base.y]

                # Calculate distance between index and thumb
                distance = calculate_distance(index_tip.x, index_tip.y, thumb_tip.x, thumb_tip.y)

                # Click mouse if fingers are close enough
                if distance < 0.05:
                    if not is_left_click_held:
                        pyautogui.mouseDown()
                        is_left_click_held = True
                else:
                    if is_left_click_held:
                        pyautogui.mouseUp()
                        is_left_click_held = False

        cv2.imshow("Mouse Control", frame)

        # Break loop on manual exit
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cleanup()
