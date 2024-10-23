#V5)unfreeze 60 layers

import os
import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Sequential, load_model  # Import load_model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

# Path to the main folder containing subfolders of gestures
data_dir = "C:/FYP"
IMG_SIZE = 224  # Update image size to 224x224

# Function to load and preprocess images
def load_and_preprocess_images(data_dir):
    categories = os.listdir(data_dir)  # Get the names of the subfolders (gesture names)
    data = []
    labels = []

    for category in categories:
        folder_path = os.path.join(data_dir, category)
        label = categories.index(category)  # Assign a numeric label based on the folder name

        for img_name in os.listdir(folder_path):
            try:
                # Construct the full image path
                img_path = os.path.join(folder_path, img_name)

                # Load the image in RGB format using OpenCV
                img = cv2.imread(img_path, cv2.IMREAD_COLOR)

                # Resize the image to the specified IMG_SIZE
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

                # Normalize the image (pixel values between 0 and 1)
                img = img.astype('float32') / 255.0

                # Append the processed image and its label to the lists
                data.append(img)
                labels.append(label)

            except Exception as e:
                print(f"Error loading image {img_name}: {e}")

    # Convert the lists to NumPy arrays
    data = np.array(data)
    labels = np.array(labels)

    return data, labels

# Call the function and load the data
images, labels = load_and_preprocess_images(data_dir)

# Split the data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Define the ResNet50 base model with 224x224 input shape
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Unfreeze the last few layers of ResNet50 for fine-tuning
base_model.trainable = True
for layer in base_model.layers[:-60]:  # Unfreeze the last 60 layers
    layer.trainable = False

# Define the new model with ResNet50 as the base and custom layers on top
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),  # Global pooling layer to reduce dimensions
    Dense(512, activation='relu'),  # Custom dense layer
    Dropout(0.4),  # Dropout for regularization
    Dense(256, activation='relu'),
    Dropout(0.3),
    Dense(len(np.unique(labels)), activation='softmax')  # Output layer for classification
])

# Compile the model with a lower learning rate for fine-tuning
model.compile(optimizer=Adam(learning_rate=0.00005), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Early stopping to avoid overfitting
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model with data augmentation and early stopping
history = model.fit(datagen.flow(X_train, y_train, batch_size=32), 
                    validation_data=(X_test, y_test), 
                    epochs=70)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

# Save the model after training
model.save('gesture_recognition_model.h5')  # Save the model to an HDF5 file

# To load the saved model later
# loaded_model = load_model('gesture_recognition_model.h5')

import matplotlib.pyplot as plt

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
