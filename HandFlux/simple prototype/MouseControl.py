import cv2
import mediapipe as mp
import win32api
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

def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

is_left_click_held = False

# Process video frames
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
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
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Scale coordinates to the screen
                cursor_x = int(index_tip.x * screen_width)
                cursor_y = int(index_tip.y * screen_height)
                win32api.SetCursorPos((cursor_x, cursor_y))

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
