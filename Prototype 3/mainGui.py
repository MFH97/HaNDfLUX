#With GUI
import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def run_program1():
    try:
        subprocess.run(["python", os.path.join(base_path, "MouseControl.py")], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Mouse Control: {e}")

def run_program2():
    try:
        subprocess.run(["python", os.path.join(base_path, "control_2hands.py")], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")

def exit_program():
    root.destroy()

# Set the base path to your scripts
base_path = r"C:\Users\mdfah\OneDrive\Desktop\FYP\Prototype 3"  # Replace with your directory

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

# Exit button
exit_button = tk.Button(frame, text="Exit", command=exit_program, width=20, height=2, fg="white", bg="red")
exit_button.pack(pady=10)

# Run the tkinter event loop
root.mainloop()
