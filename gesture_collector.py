import cv2
import mediapipe as mp
import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Directory to save datasets
DATASET_DIR = "gesture_data"
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

# Define gestures
GESTURES = ["left", "right"]  # You can expand this list
SAMPLES_PER_GESTURE = 250

# Collect Data
def collect_gesture_data(gesture_label):
    cap = cv2.VideoCapture(0)
    count = 0
    print(f"Collecting data for {gesture_label}... Press 'q' to quit.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append(lm.x)
                    landmarks.append(lm.y)
                    landmarks.append(lm.z)
                
                # Save landmarks with the label
                if count < SAMPLES_PER_GESTURE:
                    data = [gesture_label] + landmarks
                    save_to_csv(data, gesture_label)
                    count += 1

        # Display progress
        cv2.putText(frame, f"Collecting {gesture_label}: {count}/{SAMPLES_PER_GESTURE}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Data Collection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= SAMPLES_PER_GESTURE:
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Save to CSV
def save_to_csv(data, gesture_label):
    file_path = os.path.join(DATASET_DIR, f"{gesture_label}.csv")
    with open(file_path, 'a') as f:
        f.write(",".join(map(str, data)) + "\n")

# Train the Model
def train_model():
    all_data = []
    all_labels = []
    
    for gesture_label in GESTURES:
        file_path = os.path.join(DATASET_DIR, f"{gesture_label}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, header=None)
            data = df.iloc[:, 1:].values  # Landmarks
            labels = df.iloc[:, 0].values  # Labels
            all_data.extend(data)
            all_labels.extend(labels)
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(all_data, all_labels, test_size=0.2, random_state=42)
    
    # Train a RandomForest Classifier
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")
    joblib.dump(clf, "gesture_model.pkl")

# Recognize Gestures
def recognize_gestures():
    clf = joblib.load("gesture_model.pkl")
    cap = cv2.VideoCapture(0)
    
    print("Recognizing gestures... Press 'q' to quit.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Extract landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append(lm.x)
                    landmarks.append(lm.y)
                    landmarks.append(lm.z)
                
                # Predict gesture
                landmarks = np.array(landmarks).reshape(1, -1)
                prediction = clf.predict(landmarks)
                gesture = prediction[0]
                
                # Display prediction
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Gesture Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Main Menu
def main():
    while True:
        print("1. Collect Data")
        print("2. Train Model")
        print("3. Recognize Gestures")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            for gesture in GESTURES:
                collect_gesture_data(gesture)
        elif choice == '2':
            train_model()
        elif choice == '3':
            recognize_gestures()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
