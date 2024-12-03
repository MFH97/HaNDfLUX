import cv2
import mediapipe as mp
import win32api
import pyautogui
import math

# Initialize Mediapipe drawing and hand solutions
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video = cv2.VideoCapture(0)

# Screen dimensions for scaling cursor position
screen_width, screen_height = pyautogui.size()

def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Track the state of the mouse (whether left click is held or not)
is_left_click_held = False

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        frame = cv2.flip(frame, 1)  # Flip the frame for a mirrored view
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image_height, image_width, _ = image.shape
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

                # Get index finger tip and thumb tip coordinates
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Convert normalized coordinates to pixel coordinates
                index_fingertip_x = int(index_finger_tip.x * image_width)
                index_fingertip_y = int(index_finger_tip.y * image_height)
                thumb_tip_x = int(thumb_tip.x * image_width)
                thumb_tip_y = int(thumb_tip.y * image_height)

                # Draw a circle at the index finger tip and thumb tip
                cv2.circle(image, (index_fingertip_x, index_fingertip_y), 15, (0, 255, 0), -1)
                cv2.circle(image, (thumb_tip_x, thumb_tip_y), 15, (255, 0, 0), -1)

                # Calculate the distance between the index finger tip and thumb tip
                distance = calculate_distance(index_finger_tip.x, index_finger_tip.y, thumb_tip.x, thumb_tip.y)

                # Scale the index finger coordinates to the screen size
                scaled_x = int(index_finger_tip.x * screen_width)
                scaled_y = int(index_finger_tip.y * screen_height)

                # Move the cursor to the index finger position
                win32api.SetCursorPos((scaled_x, scaled_y))

                # Hold left click if the distance is small
                if distance < 0.05:  # Adjust threshold based on your camera and hand size
                    if not is_left_click_held:
                        pyautogui.mouseDown()  # Start holding left click
                        is_left_click_held = True
                else:
                    if is_left_click_held:
                        pyautogui.mouseUp()  # Release left click
                        is_left_click_held = False

        cv2.imshow("game", image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
