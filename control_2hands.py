import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model #type: ignore
import pydirectinput
import time

# Load the saved Keras model for gesture recognition
model = load_model('twoHands_model.h5')  # This model is trained on landmarks

# Gesture-to-key mapping
gesture_to_key = {
    'one': 'w', 'stop': 's', 'peace': 'a', 'peace_inverted': 'd',
    'like': 'e', 'dislike': 'q', 'fist': 'space', 'call': 'shift', 'rock': 'c'
}

# Swipe-to-key mapping
swipe_to_key = {
    'left_swipe': 'f',  # Inner drum
    'right_swipe': 'k'  # Outer drum
}

# Gesture class names (corresponding to your model's output)
class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2, static_image_mode=False, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Track currently pressed keys for both hands
current_keys = [None, None]  # [key_for_hand_1, key_for_hand_2]

# Swipe detection parameters
swipe_velocity_threshold = 0.15  # Adjust based on your swiping speed
previous_wrist_positions = [None, None]  # For both hands

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to preprocess landmarks for gesture classification
def preprocess_landmarks(landmarks):
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    return flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)

# Function to release the key for a specific hand
def release_key_for_hand(hand_idx):
    global current_keys
    if current_keys[hand_idx] is not None:
        print(f"Releasing key for Hand {hand_idx + 1}: {current_keys[hand_idx]}")
        pydirectinput.keyUp(current_keys[hand_idx])
        current_keys[hand_idx] = None

# Swipe detection function (updated for individual hands)
def detect_swipe(hand_idx, wrist_position):
    global current_keys

    if previous_wrist_positions[hand_idx] is not None:
        # Calculate wrist movement
        delta_position = wrist_position - previous_wrist_positions[hand_idx]
        horizontal_movement = delta_position[0]  # Focus on x-axis for left/right swipe

        if horizontal_movement < -swipe_velocity_threshold:  # Right swipe
            print(f"Hand {hand_idx + 1}: Detected right swipe")
            swipe_key = swipe_to_key['right_swipe']
            if current_keys[hand_idx] != swipe_key:
                release_key_for_hand(hand_idx)
                print(f"Pressing key for Hand {hand_idx + 1}: {swipe_key}")
                pydirectinput.keyDown(swipe_key)
                current_keys[hand_idx] = swipe_key
        elif horizontal_movement > swipe_velocity_threshold:  # Left swipe
            print(f"Hand {hand_idx + 1}: Detected left swipe")
            swipe_key = swipe_to_key['left_swipe']
            if current_keys[hand_idx] != swipe_key:
                release_key_for_hand(hand_idx)
                print(f"Pressing key for Hand {hand_idx + 1}: {swipe_key}")
                pydirectinput.keyDown(swipe_key)
                current_keys[hand_idx] = swipe_key

    # Update wrist position for the next frame
    previous_wrist_positions[hand_idx] = wrist_position

# Frame rate display and response time calculation
def display_fps_and_response(frame, response_time, fps):
    cv2.putText(
        frame, f"Response Time: {response_time:.1f} ms | FPS: {fps:.1f}",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2
    )

# Main loop (updated to handle gestures independently for each hand)
previous_time = time.time()
frame_count = 0
fps_interval = 10
fps_timer = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    start_time = time.time()  # Start time for response calculation

    # Flip and process frame
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        input_data = []
        hand_indices = []
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Preprocess landmarks for inference
            landmarks = preprocess_landmarks(hand_landmarks.landmark)
            input_data.append(landmarks)
            hand_indices.append(idx)

            # Swipe detection
            wrist = hand_landmarks.landmark[0]  # Wrist landmark
            wrist_position = np.array([wrist.x, wrist.y])
            detect_swipe(idx, wrist_position)

            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Batch gesture recognition
        if input_data:
            input_data = np.array(input_data)
            predictions = model.predict(input_data)

            for i, idx in enumerate(hand_indices):
                predicted_class = np.argmax(predictions[i])
                predicted_gesture = class_names[predicted_class]
                confidence = np.max(predictions[i])

                if confidence > 0.8:
                    label = f"Hand {idx + 1}: {predicted_gesture} ({confidence:.2f})"
                    cv2.putText(frame, label, (10, 70 + idx * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    if predicted_gesture in gesture_to_key:
                        new_key = gesture_to_key[predicted_gesture]
                        if current_keys[idx] != new_key:
                            release_key_for_hand(idx)
                            print(f"Pressing key for Hand {idx + 1}: {new_key}")
                            pydirectinput.keyDown(new_key)
                            current_keys[idx] = new_key
                else:
                    release_key_for_hand(idx)
    else:
        # Release keys if no hands are detected
        for idx in range(len(current_keys)):
            release_key_for_hand(idx)

    # Calculate response time and FPS
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # in milliseconds
    frame_count += 1
    if frame_count % fps_interval == 0:
        current_time = time.time()
        fps = fps_interval / (current_time - fps_timer)
        fps_timer = current_time
    else:
        fps = frame_count / (time.time() - previous_time)

    display_fps_and_response(frame, response_time, fps)

    cv2.imshow('Hand Gesture Recognition', cv2.resize(frame, (640, 480)))  # Resize to reduce display lag
    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
