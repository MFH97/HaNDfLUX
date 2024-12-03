#Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import messagebox

# Track running subprocess
process = None

def run_program1():
    global process
    try:
        if process is not None:
            messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
            return
        # Start MouseControl program
        process = subprocess.Popen(
            ["py", os.path.join(base_path, "MouseControl.py")],
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
            ["py", os.path.join(base_path, "control_2hands.py")],
            shell=True
        )
        print(f"Started Two Hands Gesture Control with PID: {process.pid}")  # Debugging info
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")



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
        #messagebox.showinfo("Info", "No programs are currently running.")


def exit_program():
    release_control()  # Ensure any running process is terminated before exiting
    root.destroy()

# Set the base path to your scripts
base_path = r"C:\Users\User\OneDrive\UniStuff\FYP\HF2\simple prototype"  # Replace with your directory

# Initialize the tkinter root window
root = tk.Tk()
root.title("Handflux-GUI Prototype 1.1")
root.geometry('800x500')
root.maxsize(1920,1080)
root.minsize(640,480)

root.configure(background="#333333")

# GUI Layout Configuration
Titleframe = tk.Frame(root, padx=10, pady=5, bg="#333333")
Titleframe.pack(anchor="nw")

#Spareframe = tk.Frame(root, padx=25, pady=5)
#Spareframe.pack(anchor="e",side="left")

# GUI Labels
TKlabel = tk.Label(Titleframe, text="Handflux Prototype", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))
TKlabel.pack(pady=5, anchor="nw")

PRlabel = tk.Label(Titleframe, text="Select a program to run:", font=("Archivo Black", 14), bg="#333333", fg="#FE5312")
PRlabel.pack(pady=5, anchor="nw")

# Buttons for each program
button1 = tk.Button(Titleframe, text="Mouse Controls", command=run_program1, width=25, height=2, bg="#B83301", fg="#FFFFFF")

button2 = tk.Button(Titleframe, text="Two-handed Gesture Controls", command=run_program2, width=25, height=2, bg="#B83301", fg="#FFFFFF")

# Release control button
release_button = tk.Button(Titleframe, text="Release Control", command=release_control, width=20, height=2, bg="#660000", fg="#FFFFFF")

# Exit button
exit_button = tk.Button(Titleframe, text="Exit", command=exit_program ,width=20, height=2, bg="#ff3300", fg="white")


# Orients the buttons based on this layout: Button 1, Button 2, Release, Exit
button1.pack(padx=5, pady=5, side="left", anchor="nw")
button2.pack(padx=5, pady=5, side="left", anchor="nw")
release_button.pack(padx=5, pady=5, side="left", anchor="w")
exit_button.pack(padx=5, pady=5, side="left", anchor="w")


# Run the tkinter event loop
root.mainloop()
