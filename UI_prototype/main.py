# Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import PhotoImage, StringVar, messagebox, ttk

# Additonal imports
import pyautogui

class generalUI:
    def button_hover(tkb, b_Hover, b_Release ):
    # Changes the colour of the button whether if it hovers or not
        tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
        tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))

class gameMenu:
    # For Game Tab Functions
    def run_gameMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Game Tab - Shows available games
            def showF(uiCurrent):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiCurrent.pack(fill="both")

            if menuAct != "Game":
                showF(uiDynamTabs["Game"])
                menuAct = "Game"
            else: 
                # Sets Game Menu tab as the default tab first
                showF(uiDynamTabs["Game"])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")
    
    # To filter the games
    def filterGame():
        filter = gameSearchBar.get()
        if filter !="":
            print(filter)
        else:
            print("Filter has nothing in it")

class profileMenu:
    # For Profile Tab Functions
    def run_profileMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Profile Tab - Shows the profiles the user set
            def showF(uiCurrent):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiCurrent.pack(fill="both")

            if menuAct != "Profile":
                showF(uiDynamTabs["Profiles"])
                menuAct = "Profile"
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")

class gestureMenu:
    # For Gesture Tab Functions
    def run_gestureMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Gestures Tab - Shows the gestures the user set
            def showF(uiCurrent):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiCurrent.pack(fill="both")
        
            if menuAct != "Gesture":
                showF(uiDynamTabs["Gestures"])
                menuAct = "Gesture"
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")

class quit:
    # Class for closing the window
    def exit_program():
        global quitCan, quitAct, onceMade
        try:
            def zeroAll():
                quit.release_control()  # Ensure any running process is terminated before exiting
                root.destroy()
        
            def stayIn():
                global quitAct
                quitCan.place_forget()
                quitAct = False

            

            if not quitAct:
                if not onceMade:
                    quitCan.place(relheight=1, relwidth=1)
        
                    quitLabel = tk.Label(quitCan, text="Do you want to quit?", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 25, "bold"))
                    yesButton = tk.Button(quitCan, text="YES", command=zeroAll ,width=15, height=3, bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20))
                    noButton = tk.Button(quitCan, text="NO", command=stayIn ,width=15, height=3, bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20))

                    quitLabel.pack(padx=25, pady=25, anchor="center")
                    yesButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(yesButton, exitRed, greyThree)

                    noButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(noButton, exitRed, greyThree)
                    quitAct = True
                    onceMade = True
                else:
                    quitCan.place(relheight=1, relwidth=1)
            else:
                messagebox.showerror("Info", "Something went wrong here") 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up quit confirmation: {e}") 

    def exit_viaKey(key):
        global quitAct
        if not quitAct:
            if key.keysym == "Escape" and quitCan.winfo_ismapped:
                quit.exit_program()
    
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

class run:
    # Class for running things in the UI
    def program1():
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

    def program2():
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

    def program3():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for Two Hands Gesture Control program
            process = subprocess.Popen(
                ["python", os.path.join(base_path, "swipeControl.py")],
                hell=True
            )
            print(f"Started Swipe Motion Gesture Control with PID: {process.pid}")  # Debugging info
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")

    def tutorial():
        global tutAct, MaxRes, tut_count, tutCanvas 
        # Tutorial Process - Video / Tkinter animation on how to use the software
        try:
            # Checks if Escape key is pressed
            def tutKey(key):
                if key.keysym == "Escape":
                    tutClose()

            # Closes the tutorial
            def tutClose():
                global tutAct
                tutCanvas.place_forget()
                tutAct = False
        
            if not tutAct:
                tutCanvas = tk.Canvas(root, width=400, height=300, bg=greyThree, highlightthickness=0)
                tutCanvas.place(relx=0.15, rely=0.25, bordermode="inside")
                root.bind("<Key>", tutKey)

                tutFrame = tk.Frame(tutCanvas, padx=5, pady=5, bg=greyThree)
                tutlabel1 = tk.Label(tutFrame, text="These buttons function as such:", anchor="ne", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 12))
                tutlabel2 = tk.Label(tutFrame, text="Settings - Opens up the settings for the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 10))
                tutlabel3 = tk.Label(tutFrame, text="FAQ - Shows the frequently asked questions about the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 10))
                tutlabel4 = tk.Label(tutFrame, text="Release Control - Closes the control and its webcam window", anchor="ne", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 10))
                tutlabel5 = tk.Label(tutFrame, text="Exit - Closes the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=("Archivo Black", 10))
            
                tutFrame.pack(fill="x")
                tutlabel1.pack()
                tutlabel2.pack()
                tutlabel3.pack()
                tutlabel4.pack()
                tutlabel5.pack()
                tutAct = True
            else:
                tutClose()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to startup Tutorial process: {e}")

    def faq():
        global faqAct
        try:
            # Checks if Escape key is pressed
            def faqKey(key):
                if key.keysym == "Escape":
                    faqClose()

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
                faqCanvas = tk.Canvas(root, width=400, height=300, bg=greyFour, highlightthickness=0)
                faqCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                root.bind("<Key>", faqKey)

                # FAQ Frame & Scrollbar to navigate
                faqTF = tk.Frame(faqCanvas, padx=5, pady=5, bg=greyTwo)
                faqFrame = tk.Frame(faqCanvas, padx=5, pady=5, bg=greyFour)
                faqScroll = tk.Scrollbar(faqCanvas)

                # Text Element to input FAQ Items
                faqtxt = tk.Text(faqFrame, yscrollcommand = faqScroll.set, bg=greyFour, width=1100, font=("Archivo Black", 14), fg=ui_Txt, border=0, wrap="word")
        
                # Label and button to close the FAQ Window
                FAQlabel = tk.Label(faqTF, text="Frequently Asked Questions", bg=greyTwo, fg=brightMahogany, font=("Archivo Black", 20, "bold"))
                close_faq = tk.Button(faqTF, text="Return", command=faqClose, width=10, height=0, bg=mahoGany, fg=ui_Txt, border=0, font=("Archivo Black", 15, "bold"))

                # GUI Layout
                faqTF.pack(side="top", anchor="nw", fill="x")
                FAQlabel.pack(pady=5, side="left", anchor="nw")
                close_faq.pack(padx=30, pady=15, side="right", anchor="ne")
                generalUI.button_hover(close_faq,mahoGany, greyTwo)

                faqFrame.pack(side="left", anchor="nw")
                faqtxt.pack(padx=10, pady=10, side="left", fill="both")
                faqScroll.pack(side="right", fill="y")

                faqAct = True

                # Loads the TXT into the faqtxt Element
                txtLoader()
            else:
                faqClose()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start FAQ Process: {e}")

    def settings():
        global gearAct, gearCanvas
        try:
            # Checks if Escape key is pressed
            def settingKey(key):
                if key.keysym == "Escape":
                    setClose()

            # Closes the settings
            def setClose():
                global gearAct
                gearCanvas.place_forget()
                gearAct = False

            if not gearAct:
                # Settings process - Tkinter overlay to change settings
                gearCanvas = tk.Canvas(root, bg=greyFour, highlightthickness=0)
                gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                root.bind("<Key>", settingKey)
            
                gearTF = tk.Frame(gearCanvas, padx=5, pady=5, bg=greyTwo)
                gearFrame = tk.Frame(gearCanvas, padx=5, pady=5, bg=greyThree)

                gearScroll = tk.Scrollbar(gearFrame)
            
                gearTitle = tk.Label(gearTF, text="SETTINGS", bg=greyTwo, fg=brightMahogany, font=("Archivo Black", 25, "bold"))
                closeGear = tk.Button(gearTF, text="RETURN", command=setClose, width=10, height=0, bg=greyTwo, fg=ui_Txt, border=0, font=("Archivo Black", 15, "bold"))

                debugLabel = tk.Label(gearFrame, text="DEBUG", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                debugDescLabel = tk.Label(gearFrame, text="For devs to configure the controls", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 12))

                button1 = tk.Button(gearFrame, text="Mouse", command=run.program1, width=10, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))
                button2 = tk.Button(gearFrame, text="Two-handed Gesture", command=run.program2, width=20, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))
                button3 = tk.Button(gearFrame, text="Swipe Motion Gesture", command=run.program3, width=20, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))

                gearScroll.pack(side="right", fill="y")
                gearTF.pack(side="top", anchor="nw", fill="x")
                gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
                gearFrame.pack(anchor="w", fill="x")
            
                closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
                generalUI.button_hover(closeGear,mahoGany, greyTwo)

                debugLabel.pack(padx=10, pady=5, anchor="nw")
                debugDescLabel.pack(padx=10, pady=2, anchor="nw")

                button1.pack(padx=5, pady=5, side="left", anchor="w")
                generalUI.button_hover(button1,mahoGany, greyTwo)

                button2.pack(padx=5, pady=5, side="left", anchor="w")
                generalUI.button_hover(button2,mahoGany, greyTwo)

                button3.pack(padx=5, pady=5, side="left", anchor="w")
                generalUI.button_hover(button3,mahoGany, greyTwo)

                """
                # Scrollbar Tester
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                label = tk.Label(gearFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=("Archivo Black", 20, "bold"))
                label.pack(padx=10, pady=2)
                """

                gearAct = True
            else:
                setClose()
  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up Settings: {e}")

# Set the base path to your scripts
base_path = r"C:\Users\User\OneDrive\UniStuff\FYP\Handflux\UI_Prototype"  # Replace with your directory

# Version Number
versionNum = "1.42"

# For tracking UI activity and subprocesses
tut_count = 0
gearAct = False
tutAct = False
faqAct = False
quitAct = False
onceMade = False

process = None

# Temporary colour scheme variables to prevent hardcoding problems, and maybe implement a way to mod the UI layout
greyTwo= "#222222"
greyThree = "#333333"
greyFour = "#444444"
greyFive = "#555555"
ui_Txt = "#CDCDCD"
mahoGany = "#B83301"
crimSon = "#660000"
brightMahogany = "#FE5312"
exitRed = "#CC3300"

testingTurquoise = "#00FFD5"

# Tracks which menu section is active
menuAct = "Game"

# Gets the resolution for the default monitor
MaxRes = pyautogui.size()

# Initialize the tkinter root window
root = tk.Tk()
root.title(f"Handflux - GUI Prototype {versionNum}")
root.geometry('800x600')
root.maxsize(MaxRes[0],MaxRes[1])
root.minsize(800,600)
root.configure(background=greyTwo)
root.bind("<Key>", quit.exit_viaKey)

# Configure the GUI layout
uiMasterFrame = tk.Frame(root, padx=5, pady=5, bg=greyTwo)
uiMiscFrame = tk.Frame(root, padx=5, pady=5, bg=greyTwo)
uiDynamFrame = tk.Frame(root, padx=5, pady=5, bg=greyTwo)

# Tabs for the UI Frame, opens up game menu as the default
uiDynamTabs = {
    "Game": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "Profiles": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "Gestures": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
}
gameMenu.run_gameMenu()

# Game Tab
menuGameTab = tk.Button(uiMasterFrame, text="GAMES", command=gameMenu.run_gameMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))

gameMasterFrame = tk.Frame(uiDynamTabs["Game"], background=greyTwo)
gamesDisplay = tk.Frame(uiDynamTabs["Game"], background=testingTurquoise)

gameSearchBorder = tk.Frame(gameMasterFrame, background=mahoGany)
gameLabel = tk.Label(gameMasterFrame, text="GAMES & APPS", bg=greyTwo, fg=ui_Txt, font=("Archivo Black", 15, "bold"))
gameSearchBar = tk.Entry(gameMasterFrame, bg=greyFive, fg=ui_Txt, border=0, font=("Archivo Black", 10))
gameSearchButton= tk.Button(gameSearchBorder, text="Search", command=gameMenu.filterGame, bg=greyThree, fg=ui_Txt, border=0, activebackground=mahoGany, font=("Archivo Black", 11, "bold"))

gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
gameLabel.pack(padx=5, pady=15, side="left")
gameSearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
gameSearchButton.pack(padx=2,pady=2, anchor="center")
gameSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")
generalUI.button_hover(gameSearchButton,mahoGany, greyThree)

gamesDisplay.pack(padx=10, pady=5, side="top", fill="x")

# Profile Tab
menuProfileTab = tk.Button(uiMasterFrame, text="PROFILES", command=profileMenu.run_profileMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))
profileLabel = tk.Label(uiDynamTabs["Profiles"], text="PROFILES", bg=greyThree, fg=ui_Txt, font=("Archivo Black", 15, "bold"))

profileLabel.pack(padx=5, pady=15, side="left")

# Gestures Tab
menuGestureTab = tk.Button(uiMasterFrame, text="GESTURES", command=gestureMenu.run_gestureMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))
gestureLabel = tk.Label(uiDynamTabs["Gestures"], text="GESTURES", bg=greyThree, fg=ui_Txt, font=("Archivo Black", 15, "bold"))

gestureLabel.pack(padx=5, pady=15, side="left")

# GUI Labels
TKlabel = tk.Label(uiMasterFrame, text=f"PROTOTYPE {versionNum}", anchor="ne", bg=greyTwo, fg=brightMahogany, font=("Archivo Black", 25, "bold"))

# Button to display a tutorial window/widget
tutorial_button = tk.Button(uiMiscFrame, text="HELP", command=run.tutorial, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))
generalUI.button_hover(tutorial_button, mahoGany, greyTwo)

# Miscellaneous UI Buttons
settings_img = PhotoImage(file = "settings.png")
scaled_settingsImg = settings_img.subsample(2, 2)
settings_button = tk.Button(uiMasterFrame, image=scaled_settingsImg, command=run.settings, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0)
faq_button = tk.Button(uiMiscFrame, text="FAQs", command=run.faq, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=("Archivo Black", 10))

# Release control button
release_button = tk.Button(uiMiscFrame, text="RESET CONTROLS", command=quit.release_control, width=15, height=2, bg=greyTwo, fg=ui_Txt, activebackground=crimSon, border=0, font=("Archivo Black", 10))

# Exit button - better implemented as image
exit_button = tk.Button(uiMiscFrame, text="EXIT", command=quit.exit_program ,width=10, height=2, bg=greyTwo, fg=ui_Txt, border=0, font=("Archivo Black", 10))

# GUI Layout and Labels
uiMasterFrame.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")

# Menu Tabs Layout
menuGameTab.pack(padx=5, pady=5, side="left", anchor="w")
generalUI.button_hover(menuGameTab, mahoGany, greyTwo)

menuProfileTab.pack(padx=5, pady=5, side="left", anchor="w")
generalUI.button_hover(menuProfileTab, mahoGany, greyTwo)

menuGestureTab.pack(padx=5, pady=5, side="left", anchor="w")
generalUI.button_hover(menuGestureTab, mahoGany, greyTwo)

settings_button.pack(padx=50, pady=5, side="right", anchor="ne")
generalUI.button_hover(settings_button, mahoGany, greyTwo)

# Transfer to settings maybe, figure out a way to make UI pop in and out
uiMiscFrame.pack(side="top", fill="x")
tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")

faq_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(faq_button, mahoGany, greyTwo)

release_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(release_button, crimSon, greyTwo)

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(exit_button, exitRed, greyTwo)

uiDynamFrame.pack(side="top", fill="x")
quitCan = tk.Canvas(root, width=400, height=300, bg=greyThree, highlightthickness=0)

# Run the tkinter event loop
root.mainloop()
