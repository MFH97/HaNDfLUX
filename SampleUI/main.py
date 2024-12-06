# Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import PhotoImage, messagebox
from tkinter.ttk import *

import pyautogui

def button_hover(tkb, b_Hover, b_Release ):
    # Changes the colour of the button whether if it hovers or not
    tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
    tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))

def run_program1():
    global process
    try:
        if process is not None:
            messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
            return
        # Start MouseControl program
        process = subprocess.Popen(
            ["python", os.path.join(base_path, "MouseControl.py")],
            shell=True
        )
        print(f"Started Mouse Control with PID: {process.pid}")  # Debugging info
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Mouse Control: {e}")

def run_program2():
    global process
    try:
        if process is not None:
            messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
            return
        # Placeholder for Two Hands Gesture Control program
        process = subprocess.Popen(
            ["python", os.path.join(base_path, "control_2hands.py")],
            shell=True
        )
        print(f"Started Two Hands Gesture Control with PID: {process.pid}")  # Debugging info
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")

def run_program3():
    global process
    try:
        if process is not None:
            messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
            return
        # Placeholder for Two Hands Gesture Control program
        process = subprocess.Popen(
            ["python", os.path.join(base_path, "swipeControl.py")],
            shell=True
        )
        print(f"Started Swipe Motion Gesture Control with PID: {process.pid}")  # Debugging info
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")

def run_tutorial():
    global MaxRes
    global tut_count
    global tut_toggle
    tutlabel1.pack(anchor="nw")
    tutlabel2.pack(anchor="nw")
    tutlabel3.pack(anchor="nw")
    tutlabel4.pack(anchor="nw")
    tutlabel5.pack(anchor="nw")
    tutlabel6.pack(anchor="nw")
    # Tutorial Process - Video / Tkinter animation on how to use the software
    try:
        if tut_toggle == False:
            if tut_count < MaxRes[1]:
                tutlabel6.config(height=tut_count)
                tut_count += 1
                tutlabel6.after(15,run_tutorial)
                if tut_count == MaxRes[1]:
                    tut_toggle = True

    except Exception as e:
        messagebox.showerror("Error", f"Failed to startup Tutorial process: {e}")

def run_faq():
    try:
        # Function to Load a TXT File in the folder to faqtxt Text Element
        def txtLoader():
            with open('faq_text.txt', 'r') as txtfile:
                faq_text = txtfile.read()
                faqtxt.insert(tk.END, faq_text)

        # FAQ Process - Tkinter Window for troubleshooting issues via FAQ
        faq_window = tk.Toplevel()
        faq_window.title("FAQ")
        faq_window.geometry('1200x600')
        faq_window.maxsize(1600,900)
        faq_window.minsize(1200,600)
        faq_window.configure(background="#333333")

        # FAQ Frame & Scrollbar to navigate
        faqframe = tk.Frame(faq_window, padx=5, pady=5, bg="#333333")
        faqtitleframe = tk.Frame(faq_window, padx=5, pady=5, bg="#222222")
        faqScroll = tk.Scrollbar(faq_window)

        # Text Element to input FAQ Items
        faqtxt = tk.Text(faq_window, yscrollcommand = faqScroll.set, bg="#333333", width=1100, font=("Archivo Black", 14), fg="#EEEEEE")
        
        # Label and button to close the FAQ Window
        FAQlabel = tk.Label(faqtitleframe, text="Handflux FAQ", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))
        close_faq = tk.Button(faqtitleframe, text="Return", command=faq_window.destroy, width=10, height=0, bg="#B83301", fg="#FFFFFF", border=0, font=("Archivo Black", 15, "bold"))

        # GUI Layout
        faqtitleframe.pack(side="top", anchor="nw", fill="x")
        FAQlabel.pack(pady=5, side="left", anchor="nw")
        close_faq.pack(padx=25, pady=5, side="right", anchor="ne")
        button_hover(close_faq,"#B83301", "#333333")

        faqframe.pack(side="left", anchor="nw")
        faqtxt.pack(side="left", fill="both")
        faqScroll.pack(side="right", fill="y")

        # Loads the TXT into the faqtxt Element
        txtLoader()

        #faqlist.bind("<Button-1>", no_select)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start FAQ Process: {e}")

def run_settings():
    try:
        # Settings process - Tkinter overlay to change settings
        gearCanvas = tk.Canvas(root, width=400, height=300, bg="#444444", highlightthickness=0)
        gearCanvas.place(x=0, y=0, relwidth=1, relheight=1)

        gearTF = tk.Frame(gearCanvas, padx=5, pady=5, bg="#222222")
        gearFrame = tk.Frame(gearCanvas, padx=5, pady=5, bg="#222222")

        gearTitle = tk.Label(gearTF, text="Settings", bg="#222222", fg="#FE5312", font=("Archivo Black", 20, "bold"))
        closeGear = tk.Button(gearTF, text="Return", command=gearCanvas.destroy, width=10, height=0, bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 15, "bold"))

        gearTF.pack(side="top", anchor="nw", fill="x")
        gearFrame.pack(side="top", anchor="nw", fill="x")
        gearTitle.pack(pady=5, side="left", anchor="nw")
        
        closeGear.pack(padx=5, pady=5, side="right", anchor="ne")
        button_hover(closeGear,"#B83301", "#333333")
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open up Settings: {e}")

def release_control():
    global process
    if process is not None:
        try:
            print(f"Terminating process with PID: {process.pid}")  # Debugging info
            # Terminate process and all its children
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()

            process.wait()  # Ensure the process is fully terminated
            print("Process and its children terminated successfully.")  # Debugging info
            process = None
            messagebox.showinfo("Info", "Running program has been terminated.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to terminate the program: {e}")
    else:
        print("No process to terminate.")  # Debugging info
        #messagebox.showinfo("Info", "No program is currently running.")

def exit_program():
    release_control()  # Ensure any running process is terminated before exiting
    root.destroy()

# Set the base path to your scripts
base_path = ""  # Replace with your directory

# Track running subprocess
process = None

# For UI Animation
tut_count = 0
tut_toggle = False

# Gets the resolution for the default monitor
MaxRes = pyautogui.size()

# Initialize the tkinter root window
root = tk.Tk()
root.title("Handflux-GUI Prototype 1.3")
root.geometry('800x600')
root.maxsize(MaxRes[0],MaxRes[1])
root.minsize(800,600)
root.configure(background="#333333")

# For UI Management, Pack cannot be mixed with Grid and Vice Versa
#Thing.pack(side="top/left/right/down", fill="none/x/y/both", expand="true/false", padx=123, pady=123)
#Thing.grid(row=123, column=123, rowspan=123, columnspan=123, padx=123, pady=123, sticky=nsew)

# Configure the GUI layout
UIframe1 = tk.Frame(root, padx=5, pady=5, bg="#333333")
UIframe2 = tk.Frame(root, padx=5, pady=5, bg="#333333")

# GUI Labels
TKlabel = tk.Label(UIframe1, text="Handflux Prototype", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))

# Buttons for each program
button1 = tk.Button(UIframe1, text="Mouse", command=run_program1, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
button2 = tk.Button(UIframe1, text="Two-handed Gesture", command=run_program2, width=20, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
button3 = tk.Button(UIframe1, text="Swipe Motion Gesture", command=run_program3, width=20, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))

# Button to display a tutorial window/widget
tutorial_button = tk.Button(UIframe2, text="Help", command=run_tutorial, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
button_hover(tutorial_button,"#B80120", "#333333")
tutFrame = tk.Frame(root, padx=5, pady=5, bg="#333333")
tutlabel1 = tk.Label(tutFrame, text="Click a Control button above to open up the webcam with that control", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 12))
tutlabel2 = tk.Label(tutFrame, text="Mouse - Your hands act as the PC's Mouse", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel3 = tk.Label(tutFrame, text="Two-handed Gesture - Hand Gestures are linked to set keybinds", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel4 = tk.Label(tutFrame, text="Swipe Motion Gesture - Swipe Gestures are linked to set keybinds", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel5 = tk.Label(tutFrame, text="Release Control - Closes the control and its webcam window", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel6 = tk.Label(tutFrame, text="Exit - Closes the app", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))

# Miscellaneous UI Buttons
settings_img = PhotoImage(file = "settings.png")
scaled_settingsImg = settings_img.subsample(2, 2)
settings_button = tk.Button(UIframe1, image=scaled_settingsImg, command=run_settings, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0)


faq_button = tk.Button(UIframe2, text="FAQs", command=run_faq, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))

# Release control button
release_button = tk.Button(UIframe2, text="Release Controls", command=release_control, width=15, height=2, bg="#333333", fg="#FFFFFF", activebackground='#660000', border=0, font=("Archivo Black", 10))

# Exit button - better implemented as image
exit_button = tk.Button(UIframe2, text="Exit", command=exit_program ,width=10, height=2, bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 10))

# GUI Layout and Labels
UIframe1.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")

# Button Layout
button1.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(button1,"#B83301", "#333333")

button2.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(button2,"#B83301", "#333333")

button3.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(button3,"#B83301", "#333333")

settings_button.pack(padx=50, pady=5, side="right", anchor="ne")
button_hover(settings_button,"#B80120", "#333333")

# For the second row
UIframe2.pack(side="top", fill="x")
tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")

faq_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(faq_button,"#B80120", "#333333")

release_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(release_button,"#660000", "#333333")

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(exit_button,"#CC3300", "#333333")

# Temp tutorial Section
tutFrame.pack(side="left", fill="x")

# Run the tkinter event loop
root.mainloop()
