# 2 hands prediction 

import os 
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to extract hand landmarks from images
def extract_landmarks_from_images(data_dir):
    categories = os.listdir(data_dir)  # Get gesture categories
    data = []
    labels = []

    for category in categories:
        folder_path = os.path.join(data_dir, category)
        label = categories.index(category)  # Assign numeric label to each category

        for img_name in os.listdir(folder_path):
            try:
                # Load the image
                img_path = os.path.join(folder_path, img_name)
                img = cv2.imread(img_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Process the image with MediaPipe and handle up to two hands
                results = hands.process(img_rgb)

                # Check if hand landmarks were detected
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Extract 21 landmarks (each having x, y, z)
                        landmark_list = []
                        for landmark in hand_landmarks.landmark:
                            landmark_list.extend([landmark.x, landmark.y, landmark.z])
                        
                        # Append the landmarks and the corresponding label
                        data.append(landmark_list)
                        labels.append(label)
            except Exception as e:
                print(f"Error processing image {img_name}: {e}")

    return np.array(data), np.array(labels)

# Directory containing gesture images
data_dir = "C:/FYP"

# Extract landmarks and labels
landmarks, labels = extract_landmarks_from_images(data_dir)

# Split the data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.2, random_state=42)

# Define a new model for MediaPipe landmarks
model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),  # 63 inputs (21 landmarks * 3 coordinates)
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(len(np.unique(labels)), activation='softmax')  # Output layer for classification
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

# Early stopping to avoid overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32, callbacks=[early_stopping])

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

# Save the trained model
model.save('twoHands_model.h5')

# Plot training & validation accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
