import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

# Constants
DATA_PATH = "gesture_data"
GESTURES = ["Left", "Right"]
SAMPLES_PER_GESTURE = 250
INPUT_SHAPE = 63  # Each hand has 21 landmarks with x, y, z (21 * 3)

# Load Data
def load_data():
    data = []
    labels = []

    for gesture_idx, gesture in enumerate(GESTURES):
        gesture_path = os.path.join(DATA_PATH, gesture)
        for file_name in os.listdir(gesture_path):
            if file_name.endswith(".npy"):
                file_path = os.path.join(gesture_path, file_name)
                landmarks = np.load(file_path)

                # Add data and labels
                data.append(landmarks)
                labels.append(gesture_idx)

    return np.array(data), np.array(labels)

# Preprocess Data
def preprocess_data(data, labels):
    data = data.reshape(data.shape[0], -1)  # Flatten data if not already
    labels = to_categorical(labels, num_classes=len(GESTURES))  # One-hot encode labels
    return train_test_split(data, labels, test_size=0.2, random_state=42)

# Build Model
def build_model(input_shape, num_classes):
    model = Sequential([
        Input(shape=(input_shape,)),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')  # Output layer
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Train the Model
def train_model(model, X_train, X_val, y_train, y_val):
    # Use `.keras` for modern format or specify `.h5` explicitly
    checkpoint = ModelCheckpoint("gesture_model.keras", save_best_only=True, monitor='val_loss', mode='min')
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=32,
        callbacks=[checkpoint]
    )
    return history


# Main function
def main():
    print("Loading data...")
    data, labels = load_data()
    print(f"Data shape: {data.shape}, Labels shape: {labels.shape}")

    print("Preprocessing data...")
    X_train, X_val, y_train, y_val = preprocess_data(data, labels)

    print("Building model...")
    model = build_model(INPUT_SHAPE, len(GESTURES))

    print("Training model...")
    train_model(model, X_train, X_val, y_train, y_val)

    print("Model training complete. Saved as 'gesture_model.h5'")

if __name__ == "__main__":
    main()
