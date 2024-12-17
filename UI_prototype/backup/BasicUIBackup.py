# MediaPipe x Gesture Recognition for Two Hands
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model # type: ignore
import pydirectinput
import traceback
import time

# TKinter import
from tkinter import *
from PIL import Image, ImageTk 


# Global Cam functions
def camopen():
    global cap
    global check
    tkwebcam.pack()

    if check == False:
        cap = cv2.VideoCapture(0)
        check = True
    
    while True:
        try:
            _, frame = cap.read() 
            imgGet = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            camVid = ImageTk.PhotoImage(Image.fromarray(imgGet))
            tkwebcam.image = camVid
            tkwebcam.configure(image=camVid)
            tkwebcam.update()

            # Checks if the frame is acquired
            if not _:
                break

        except:
            break

def camclose():
    global check
    if check == True:
        cap.release()
        cv2.destroyAllWindows()
        check = False
    tkwebcam.pack_forget()

# Function to preprocess landmarks for gesture classification
def preprocess_landmarks(landmarks):
    # Convert the landmarks into a flattened array
    flattened_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()

    # Normalize the landmarks by subtracting the wrist (landmark 0) coordinates
    wrist_x, wrist_y, wrist_z = flattened_landmarks[0], flattened_landmarks[1], flattened_landmarks[2]
    flattened_landmarks = flattened_landmarks - np.array([wrist_x, wrist_y, wrist_z] * 21)

    return flattened_landmarks

# Function to release the current key
def release_current_key():
    global current_key
    if current_key is not None:
        print(f"Releasing key: {current_key}")
        pydirectinput.keyUp(current_key)  # Release the key that was being held down
        current_key = None
    
""" 
#TKinter Sample Code

from tkinter import *

root = Tk()
root.title('TKinter_Handflux')
root.geometry('1366x768')
a = Label(root)
a.pack()
root.mainloop()


#Kivy Sample Code

from kivy.app import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class Kivy_Handflux(App):
    pass

if __name__ == '__main__':
    Kivy_Handflux().run() 

"""

# TKinter Window specs - GUI
tkwin = Tk()
tkwin.title('TKinter_Handflux')
tkwin.geometry('1280x768')
tkwin.maxsize(1920,1080)
tkwin.minsize(640,480)

# Escape window to close the TKinter GUI
tkwin.bind('<Escape>', lambda e: tkwin.quit())
check = False

# Open the webcam and checks if it's open
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()
    
# Widget for the webcam to load in
tkwebcam = Label(tkwin)

# command=lambda : camopen("Open")) 
# Button for opening up the camera
openbutton = Button(tkwin, text="Open the Camera", command=camopen) 
openbutton.pack()

# Button for closing down the camera
closebutton = Button(tkwin, text="Close the Camera", command=camclose)
closebutton.pack()

# Creates the TKinter Window
tkwin.mainloop()