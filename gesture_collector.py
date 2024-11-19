import cv2
import mediapipe as mp
import numpy as np
import os
from tqdm import tqdm  # For progress bar

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Constants
GESTURES = ["Left", "Right"]  # Ensure these match Mediapipe's hand labels
DATA_PATH = "gesture_data"
SAMPLES_PER_GESTURE = 250

# Initialize variables
current_hand = 0  # 0 for Left, 1 for Right
collected_samples = 0
collecting = False

# Create folders for gestures automatically
def setup_data_folders():
    os.makedirs(DATA_PATH, exist_ok=True)
    for gesture in GESTURES:
        os.makedirs(os.path.join(DATA_PATH, gesture), exist_ok=True)
    print(f"Folders created for gestures: {GESTURES}")

# Save hand landmarks to file
def save_landmarks(hand_landmarks, hand_name):
    global collected_samples
    landmarks = []
    for landmark in hand_landmarks.landmark:
        landmarks.extend([landmark.x, landmark.y, landmark.z])
    landmarks = np.array(landmarks)

    # Save to file
    filename = os.path.join(DATA_PATH, hand_name, f"{collected_samples}.npy")
    np.save(filename, landmarks)
    collected_samples += 1

# Main function for collecting gestures
def gesture_collector():
    global current_hand, collected_samples, collecting

    # Ensure folders are set up
    setup_data_folders()

    cap = cv2.VideoCapture(0)
    print(f"Starting Gesture Collector. Press 's' to start/pause, and 'q' to quit.")

    progress_bar = None  # Placeholder for progress bar

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        # Check for hand landmarks
        if result.multi_hand_landmarks:
            print("Hands detected!")
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                hand_label = handedness.classification[0].label  # 'Left' or 'Right'
                print(f"Detected hand: {hand_label}")

                if collecting and hand_label == GESTURES[current_hand]:
                    save_landmarks(hand_landmarks, GESTURES[current_hand])

                    if progress_bar is None:
                        # Initialize the progress bar
                        progress_bar = tqdm(total=SAMPLES_PER_GESTURE, desc=f"Collecting {GESTURES[current_hand]}", unit="samples")
                    progress_bar.update(1)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        else:
            print("No hands detected.")

        # Overlay collection status
        cv2.putText(frame, f"Collecting: {collecting}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Hand: {GESTURES[current_hand]}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Gesture Collector", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Start/Pause collection
            collecting = not collecting
            if collecting:
                print(f"Started collecting for {GESTURES[current_hand]}")
                if progress_bar is None:
                    progress_bar = tqdm(total=SAMPLES_PER_GESTURE, desc=f"Collecting {GESTURES[current_hand]}", unit="samples")
            else:
                print(f"Paused collection.")
                if progress_bar:
                    progress_bar.close()
                    progress_bar = None
        elif key == ord('q'):  # Quit
            break

        # Check if collection is complete
        if collected_samples >= SAMPLES_PER_GESTURE:
            print(f"Collected {SAMPLES_PER_GESTURE} samples for {GESTURES[current_hand]}")
            collecting = False
            collected_samples = 0
            current_hand += 1
            if progress_bar:
                progress_bar.close()
                progress_bar = None

            if current_hand >= len(GESTURES):
                print("Gesture collection complete.")
                break
            print(f"Switching to {GESTURES[current_hand]}")

    cap.release()
    cv2.destroyAllWindows()

# Run the gesture collector
gesture_collector()
