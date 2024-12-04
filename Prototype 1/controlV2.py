import cv2
import numpy as np
from tensorflow.keras.models import load_model
import pydirectinput

# Load the saved Keras model
model = load_model('gesture_recognition_model.h5')

# Gesture-to-key mapping (for Forza Horizon 4)
gesture_to_key = {
    #'one': 'w',  # Accelerate
    #'stop': 's',  # Decelerate/reverse
   # 'peace': 'a',  # Steer left
    #'peace_inverted': 'd',  # Steer right
    'like': 'w',  # Shift up
    'dislike': 'a', #'q',  # Shift down
    'fist': 'space',  # E-brake
    'call': 's',  # Clutch
    #'rock': 'c'  # ANNA Activation
}

# Gesture class names (corresponding to your model's output)
class_names = ['call', 'dislike', 'fist', 'like', 'one', 'peace', 'peace_inverted', 'rock', 'stop']

# Track the currently pressed key
current_key = None

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to preprocess the frame for the model
def preprocess_frame(frame):
    img = cv2.resize(frame, (224, 224))  # Resize to match the input size of the model
    img = img.astype('float32') / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension (1, 224, 224, 3)
    return img

# Function to release the current key
def release_current_key():
    global current_key
    if current_key is not None:
        pydirectinput.keyUp(current_key)  # Release the key that was being held down
        current_key = None

# Loop to continuously get frames from the webcam
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    frame = cv2.flip(frame, 1)  # Optional: Flip the frame for mirror-like view
    input_data = preprocess_frame(frame)

    # Run inference using the Keras model
    prediction = model.predict(input_data)
    predicted_class = np.argmax(prediction[0])
    predicted_gesture = class_names[predicted_class]

    # Display the prediction on the frame
    label = f"Prediction: {predicted_gesture}"
    cv2.putText(frame, label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Gesture Recognition', frame)

    # Simulate the corresponding key press based on the predicted gesture
    if predicted_gesture in gesture_to_key:
        new_key = gesture_to_key[predicted_gesture]

        # Only press and hold the new key if it's different from the current one
        if current_key != new_key:
            release_current_key()  # Release the previous key if there was one
            pydirectinput.keyDown(new_key)  # Hold down the new key
            current_key = new_key

    # If no gesture matches, release the current key
    else:
        release_current_key()

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
