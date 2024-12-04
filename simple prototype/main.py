#Main program for GUI interface
import subprocess
import os
import psutil
import tkinter as tk
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
        messagebox.showinfo("Info", "No program is currently running.")


def exit_program():
    release_control()  # Ensure any running process is terminated before exiting
    root.destroy()

# Set the base path to your scripts
base_path = ""  # Replace with your directory

# Initialize the tkinter root window
root = tk.Tk()
root.title("Program Selector")

# Configure the GUI layout
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=20)

label = tk.Label(frame, text="Select a program to run:", font=("Arial", 14))
label.pack(pady=10)

# Buttons for each program
button1 = tk.Button(frame, text="Run Mouse Control", command=run_program1, width=20, height=2)
button1.pack(pady=5)

button2 = tk.Button(frame, text="Run Two Hands Gesture Control", command=run_program2, width=20, height=2)
button2.pack(pady=5)

button2 = tk.Button(frame, text="Run Swipe Motion Gesture Control", command=run_program3, width=20, height=2)
button2.pack(pady=5)

# Release control button
release_button = tk.Button(frame, text="Release Control", command=release_control, width=20, height=2, fg="white", bg="blue")
release_button.pack(pady=5)

# Exit button
exit_button = tk.Button(frame, text="Exit", command=exit_program, width=20, height=2, fg="white", bg="red")
exit_button.pack(pady=10)

# Run the tkinter event loop
root.mainloop()
