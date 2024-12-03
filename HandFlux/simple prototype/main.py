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
        #messagebox.showinfo("Info", "No program is currently running.") # I temporarily commented this code to streamline the UI benchmarking process -Jun Hong


def exit_program():
    release_control()  # Ensure any running process is terminated before exiting
    root.destroy()

# Set the base path to your scripts
base_path = r"Directory"  # Replace with your directory

# Initialize the tkinter root window
root = tk.Tk()
root.title("Handflux-GUI Prototype 1.1")
root.geometry('800x500')
root.maxsize(1920,1080)
root.minsize(640,480)
root.configure(background="#333333")

# For UI Management, Pack cannot be mixed with Grid and Vice Versa
#Thing.pack(side="top/left/right/down", fill="none/x/y/both", expand="true/false", padx=123, pady=123)
#Thing.grid(row=123, column=123, rowspan=123, columnspan=123, padx=123, pady=123, sticky=nsew)

# GUI Layout Configuration
UIframe1 = tk.Frame(root, padx=5, pady=5, bg="#333333")
UIframe2 = tk.Frame(root, padx=5, pady=5, bg="#333333")

# GUI Labels
TKlabel = tk.Label(UIframe1, text="Handflux Prototype", anchor="ne", bg="#333333", fg="#FE5312", font=("Archivo Black", 25, "bold"))
PRlabel = tk.Label(UIframe1, text="Select a program to run:", font=("Archivo Black", 14), bg="#333333", fg="#FE5312")

# Buttons for each program
button1 = tk.Button(UIframe1, text="Mouse Controls", command=run_program1, width=20, height=2, bg="#B83301", fg="#FFFFFF")
button2 = tk.Button(UIframe1, text="Two-handed Gesture Controls", command=run_program2, width=25, height=2, bg="#B83301", fg="#FFFFFF")
button3 = tk.Button(UIframe1, text="Swipe Motion Gesture Controls", command=run_program3, width=25, height=2, bg="#B83301", fg="#FFFFFF")

# Release control button
release_button = tk.Button(UIframe2, text="Release Controls", command=release_control, width=15, height=2, bg="#660000", fg="#FFFFFF")

# Exit button
exit_button = tk.Button(UIframe2, text="Exit", command=exit_program ,width=10, height=2, bg="#CC3300", fg="#FFFFFF")

# GUI Layout and Labels
UIframe1.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")
PRlabel.pack(pady=5, anchor="nw")

# Button Layout
button1.pack(padx=5, pady=5, side="left", anchor="nw")
button2.pack(padx=5, pady=5, side="left", anchor="nw")
button3.pack(padx=5, pady=5, side="left", anchor="nw")

# For the second row
UIframe2.pack(side="top", fill="x")
release_button.pack(padx=5, pady=5, side="left", anchor="nw")
exit_button.pack(padx=5, pady=5, side="left", anchor="nw")

# Runs the tkinter event loop
root.mainloop()
