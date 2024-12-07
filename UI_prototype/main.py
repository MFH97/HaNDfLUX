# Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import PhotoImage, StringVar, messagebox, ttk

# Additonal imports
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
    global tutAct
    global tut_count

    tutFrame.pack(side="left", fill="x")
    tutlabel1.pack(anchor="nw")
    tutlabel2.pack(anchor="nw")
    tutlabel3.pack(anchor="nw")
    tutlabel4.pack(anchor="nw")
    tutlabel5.pack(anchor="nw")
    # Tutorial Process - Video / Tkinter animation on how to use the software
    try:
        def tutClose():
            global tutAct
            tutFrame.pack_forget()
            tutAct = False
        
        def animate():
            global tut_count
            if tut_count < MaxRes[1]:
                tut_count += 5
                tutlabel5.config(height=tut_count)
                tutlabel5.after(15,animate)

        if not tutAct:
            animate()
            tutAct = True
        else:
            tutClose()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to startup Tutorial process: {e}")

def run_faq():
    global faqAct
    try:
        # Closes the FAQ
        def faqClose():
            global faqAct
            faqCanvas.place_forget()
            faqAct = False

        # Function to Load a TXT File in the folder to faqtxt Text Element
        def txtLoader():
            with open('faq_text.txt', 'r') as txtfile:
                faq_text = txtfile.read()
                faqtxt.insert(tk.END, faq_text)

        # Checks if FAQ UI is opened
        if not faqAct:
            faqCanvas = tk.Canvas(root, width=400, height=300, bg="#444444", highlightthickness=0)
            faqCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)

            # FAQ Frame & Scrollbar to navigate
            faqTF = tk.Frame(faqCanvas, padx=5, pady=5, bg="#222222")
            faqFrame = tk.Frame(faqCanvas, padx=5, pady=5, bg="#444444")
            faqScroll = tk.Scrollbar(faqCanvas)

            # Text Element to input FAQ Items
            faqtxt = tk.Text(faqFrame, yscrollcommand = faqScroll.set, bg="#444444", width=1100, font=("Archivo Black", 14), fg="#EEEEEE", border=0, wrap="word")
        
            # Label and button to close the FAQ Window
            FAQlabel = tk.Label(faqTF, text="Frequently Asked Questions", bg="#222222", fg="#FE5312", font=("Archivo Black", 20, "bold"))
            close_faq = tk.Button(faqTF, text="Return", command=faqClose, width=10, height=0, bg="#B83301", fg="#FFFFFF", border=0, font=("Archivo Black", 15, "bold"))

            # GUI Layout
            faqTF.pack(side="top", anchor="nw", fill="x")
            FAQlabel.pack(pady=5, side="left", anchor="nw")
            close_faq.pack(padx=30, pady=15, side="right", anchor="ne")
            button_hover(close_faq,"#B83301", "#333333")

            faqFrame.pack(side="left", anchor="nw")
            faqtxt.pack(padx=10, pady=10, side="left", fill="both")
            faqScroll.pack(side="right", fill="y")

            # Loads the TXT into the faqtxt Element
            txtLoader()
        else:
            faqClose()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to start FAQ Process: {e}")

def run_settings():
    global gearAct
    global gearCanvas
    try:
        # Closes the settings
        def setClose():
            global gearAct
            gearCanvas.place_forget()
            gearAct = False

        if not gearAct:
            # Settings process - Tkinter overlay to change settings
            gearCanvas = tk.Canvas(root, bg="#444444", highlightthickness=0)
            gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
            
            gearTF = tk.Frame(gearCanvas, padx=5, pady=5, bg="#222222")
            gearFrame = tk.Frame(gearCanvas, padx=5, pady=5, bg="#333333")

            gearScroll = tk.Scrollbar(gearFrame)
            
            gearTitle = tk.Label(gearTF, text="Settings", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))
            closeGear = tk.Button(gearTF, text="Return", command=setClose, width=10, height=0, bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 15, "bold"))

            debugLabel = tk.Label(gearFrame, text="Debug", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            debugDescLabel = tk.Label(gearFrame, text="For devs to configure the controls", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 12))

            button1 = tk.Button(gearFrame, text="Mouse", command=run_program1, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
            button2 = tk.Button(gearFrame, text="Two-handed Gesture", command=run_program2, width=20, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
            button3 = tk.Button(gearFrame, text="Swipe Motion Gesture", command=run_program3, width=20, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))

            
            gearScroll.pack(side="right", fill="y")
            gearTF.pack(side="top", anchor="nw", fill="x")
            gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
            gearFrame.pack(anchor="w", fill="x")
            
            closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
            button_hover(closeGear,"#B83301", "#333333")

            debugLabel.pack(padx=10, pady=5, anchor="nw")
            debugDescLabel.pack(padx=10, pady=2, anchor="nw")

            button1.pack(padx=5, pady=5, side="left", anchor="w")
            button_hover(button1,"#B83301", "#333333")

            button2.pack(padx=5, pady=5, side="left", anchor="w")
            button_hover(button2,"#B83301", "#333333")

            button3.pack(padx=5, pady=5, side="left", anchor="w")
            button_hover(button3,"#B83301", "#333333")

            """
            # Scrollbar Tester
            label = tk.Label(gearFrame, text="Scrollbar Test", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            label.pack(padx=10, pady=2)
            label = tk.Label(gearFrame, text="Scrollbar Test", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            label.pack(padx=10, pady=2)
            label = tk.Label(gearFrame, text="Scrollbar Test", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            label.pack(padx=10, pady=2)
            label = tk.Label(gearFrame, text="Scrollbar Test", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            label.pack(padx=10, pady=2)
            label = tk.Label(gearFrame, text="Scrollbar Test", bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 20, "bold"))
            label.pack(padx=10, pady=2)
            """

            gearAct = True
        else:
            setClose()
  
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
        #messagebox.showinfo("Info", "No program is currently running.") - Commented to streamline UI modifiactions -Jun Hong

def exit_program():
    release_control()  # Ensure any running process is terminated before exiting
    root.destroy()

# Set the base path to your scripts
base_path = ""  # Replace with your directory

# Track running subprocess
process = None

# For UI Animation
tut_count = 0

# Tracks if widget UI is open
gearAct = False
tutAct = False
faqAct = False

# Gets the resolution for the default monitor
MaxRes = pyautogui.size()

# Initialize the tkinter root window
root = tk.Tk()
root.title("Handflux-GUI Prototype 1.4")
root.geometry('800x600')
root.maxsize(MaxRes[0],MaxRes[1])
root.minsize(800,600)
root.configure(background="#333333")

# Configure the GUI layout
UIframe1 = tk.Frame(root, padx=5, pady=5, bg="#333333")
UIframe2 = tk.Frame(root, padx=5, pady=5, bg="#333333")

# GUI Labels
TKlabel = tk.Label(UIframe1, text="Handflux Prototype", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))

# Button to display a tutorial window/widget
tutorial_button = tk.Button(UIframe2, text="Help", command=run_tutorial, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
button_hover(tutorial_button,"#B80120", "#333333")

tutFrame = tk.Frame(root, padx=5, pady=5, bg="#333333")
tutlabel1 = tk.Label(tutFrame, text="These buttons function as such:", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 12))
tutlabel2 = tk.Label(tutFrame, text="Settings - Opens up the settings for the app", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel3 = tk.Label(tutFrame, text="FAQ - Shows the frequently asked questions about the app", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel4 = tk.Label(tutFrame, text="Release Control - Closes the control and its webcam window", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))
tutlabel5 = tk.Label(tutFrame, text="Exit - Closes the app", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 10))

# Miscellaneous UI Buttons
settings_img = PhotoImage(file = "settings.png")
scaled_settingsImg = settings_img.subsample(2, 2)
settings_button = tk.Button(UIframe1, image=scaled_settingsImg, command=run_settings, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0)
faq_button = tk.Button(UIframe2, text="FAQs", command=run_faq, width=10, height=2, bg="#333333", fg="#FFFFFF", activebackground='#B83301', border=0, font=("Archivo Black", 10))
searchBar = tk.Entry(UIframe1, bg="#EEEEEE", bd=0, font=("Archivo Black",10))

# Release control button
release_button = tk.Button(UIframe2, text="Release Controls", command=release_control, width=15, height=2, bg="#333333", fg="#FFFFFF", activebackground='#660000', border=0, font=("Archivo Black", 10))

# Exit button - better implemented as image
exit_button = tk.Button(UIframe2, text="Exit", command=exit_program ,width=10, height=2, bg="#333333", fg="#FFFFFF", border=0, font=("Archivo Black", 10))

# GUI Layout and Labels
UIframe1.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")

# Search Bar
#searchBar.pack(side="left", anchor="nw")

settings_button.pack(padx=50, pady=5, side="right", anchor="ne")
button_hover(settings_button,"#B80120", "#333333")

# Transfer to settings maybe, figure out a way to make UI pop in and out
UIframe2.pack(side="top", fill="x")
tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")

faq_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(faq_button,"#B80120", "#333333")

release_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(release_button,"#660000", "#333333")

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
button_hover(exit_button,"#CC3300", "#333333")

# Run the tkinter event loop
root.mainloop()
