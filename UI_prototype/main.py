# Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import Image, PhotoImage, StringVar, messagebox, ttk

# Additonal imports
import pyautogui
from PIL import Image, ImageTk

class generalUI:
    def button_hover(tkb, b_Hover, b_Release ):
    # Changes the colour of the button whether if it hovers or not
        tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
        tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))

class tabFunc:
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

    # To be integrated with filterGame
    def gameDisplay(txt, filter):
        global game_Count, gamesList, gamesDisplay, gameDisplayArray, descDisplayArray

        # Resets the list
        game_Count = 0
        gameDisplayArray.clear()
        descDisplayArray.clear()
        imgDisplayArray.clear()

        # Fills the list
        for line in txt:
            if "GameÃ· " in line:
                gameName = line.split("Ã· ")
                game_Count += 1
                gameDisplayArray.append(gameName[1].replace("\n",""))
            
            elif "DescÃ· " in line:
                gameDesc = line.split("Ã· ")
                descDisplayArray.append(gameDesc[1].replace("\n",""))
            
            elif "ImgÃ· " in line:
                gameImg = line.split("Ã· ")
                file = base_path + gameImg[1].replace("\n","")
                imgDisplayArray.append(file)

        # Var checks
        #print(game_Count)
        for gameItem in range(game_Count):
            pass
            #print(gameDisplayArray[gameItem])
            #print(descDisplayArray[gameItem])
            #print(imgDisplayArray[gameItem])
        
        return game_Count, gameDisplayArray, descDisplayArray, imgDisplayArray

    # To filter the games
    def filterGame():
        global game_Count, gamesList, gameDisplayArray
        filter = gameSearchBar.get()
        if filter !="":
            gamesList = open('gamesList.txt', 'r')
            tabFunc.gameDisplay(gamesList, filter)
            
        else:
            print("Null")

    def closeTXT():
        global gamesList
        gamesList.close()

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

    def game_Describe(gameItem):
        print(gameItem)

class quit:
    # Class for closing the window
    def exit_program():
        global quitCan, quitAct, onceMade_Quit
        try:
            # Closes everything and ensures any running process is terminated before exiting
            def zeroAll():
                tabFunc.closeTXT()
                quit.release_control() 
                root.destroy()

            # Returns to the main menu
            def stayIn():
                global quitAct
                quitCan.place_forget()
                quitAct = False

            if not quitAct:
                if not onceMade_Quit:
                    quitCan.place(relheight=1, relwidth=1)
        
                    quitLabel = tk.Label(quitCan, text="Do you want to quit?", bg=greyThree, fg=brightMahogany, font=(standardFont, 25, boldForm))
                    yesButton = tk.Button(quitCan, text="YES", command=zeroAll ,width=15, height=3, bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20))
                    noButton = tk.Button(quitCan, text="NO", command=stayIn ,width=15, height=3, bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20))

                    quitLabel.pack(padx=25, pady=25, anchor="center")
                    yesButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(yesButton, exitRed, greyThree)

                    noButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(noButton, exitRed, greyThree)
                    quitAct = True
                    onceMade_Quit = True
                else:
                    quitCan.place(relheight=1, relwidth=1)
            else:
                messagebox.showerror("Info", "Something went wrong here") 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up quit confirmation: {e}") 

    def exit_viaKey(key):
        #global quitAct
        #if not quitAct:
        if key.keysym == "Escape" and quitCan.winfo_ismapped and tutCanvas.winfo_ismapped != True and gearCanvas.winfo_ismapped !=True and faqCanvas.winfo_ismapped !=True:
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
                shell=True
            )
            print(f"Started Swipe Motion Gesture Control with PID: {process.pid}")  # Debugging info
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Two Hands Gesture Control: {e}")

    def program4():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for Hybrid Gesture Control Program
            process = subprocess.Popen(
                ["python", os.path.join(base_path, "hybrid.py")],
                shell=True
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
                tutCanvas.place(relx=0.15, rely=0.25, bordermode="inside")
                root.bind("<Key>", tutKey)

                tutFrame = tk.Frame(tutCanvas, padx=5, pady=5, bg=greyThree)
                tutlabel1 = tk.Label(tutFrame, text="These buttons function as such:", anchor="ne", bg=greyThree, fg=brightMahogany, font=(standardFont, 12))
                tutlabel2 = tk.Label(tutFrame, text="Settings - Opens up the settings for the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=(standardFont, 10))
                tutlabel3 = tk.Label(tutFrame, text="FAQ - Shows the frequently asked questions about the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=(standardFont, 10))
                tutlabel4 = tk.Label(tutFrame, text="Release Control - Closes the control and its webcam window", anchor="ne", bg=greyThree, fg=brightMahogany, font=(standardFont, 10))
                tutlabel5 = tk.Label(tutFrame, text="Exit - Closes the app", anchor="ne", bg=greyThree, fg=brightMahogany, font=(standardFont, 10))
            
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
                
                faqCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                root.bind("<Key>", faqKey)

                # FAQ Frame & Scrollbar to navigate
                faqTF = tk.Frame(faqCanvas, padx=5, pady=5, bg=greyTwo)
                faqFrame = tk.Frame(faqCanvas, padx=5, pady=5, bg=greyFour)
                faqScroll = tk.Scrollbar(faqCanvas)

                # Text Element to input FAQ Items
                faqtxt = tk.Text(faqFrame, yscrollcommand = faqScroll.set, bg=greyFour, width=1100, font=(standardFont, 14), fg=ui_Txt, border=0, wrap="word")
        
                # Label and button to close the FAQ Window
                FAQlabel = tk.Label(faqTF, text="Frequently Asked Questions", bg=greyTwo, fg=brightMahogany, font=(standardFont, 20, boldForm))
                close_faq = tk.Button(faqTF, text="Return", command=faqClose, width=10, height=0, bg=mahoGany, fg=ui_Txt, border=0, font=(standardFont, 15, boldForm))

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
        global gearAct, gearCanvas, onceMade_Settings
        try:
            # Checks if Escape key is pressed
            def settingKey(key):
                if key.keysym == "Escape":
                    setClose()
            
            def canvasConfig(e):
                gearCanvas.configure(scrollregion=gearCanvas.bbox("all"))
            
            def canvasResize(e):
                gearCanvas.itemconfig(gearSettings, width=e.width)
            
            def mouseScroll(e):
                gearCanvas.yview_scroll(-1 * (e.delta // 120), "units")

            # Closes the settings
            def setClose():
                global gearAct
                gearCanvas.place_forget()
                gearAct = False

            if not gearAct:
                if not onceMade_Settings:
                    # Settings process - Tkinter overlay to change settings
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                
                    root.bind("<Key>", settingKey)
            
                    gearMaster = tk.Frame(gearCanvas, padx=5, pady=5, bg=greyTwo)
               
                    gearScroll = tk.Scrollbar(gearMaster, command=gearCanvas.yview)
                    gearCanvas.configure(yscrollcommand=gearScroll.set)

                    gearSettings = gearCanvas.create_window((0, 0), window=gearMaster)

                    gearMaster.bind("<Configure>", canvasConfig)
                    gearCanvas.bind("<Configure>", canvasResize)
                    gearCanvas.bind_all("<MouseWheel>", mouseScroll)

                    gearTF = tk.Frame(gearMaster, padx=5, pady=5, bg=greyTwo)
                    debugFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=greyThree)
                    testFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=greyFive)
            
                    gearTitle = tk.Label(gearTF, text="SETTINGS", bg=greyTwo, fg=brightMahogany, font=(standardFont, 25, boldForm))
                    closeGear = tk.Button(gearTF, text="RETURN", command=setClose, width=10, height=0, bg=greyTwo, fg=ui_Txt, border=0, font=(standardFont, 15, boldForm))

                    debugLabel = tk.Label(debugFrame, text="DEBUG", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    debugDescLabel = tk.Label(debugFrame, text="For devs to configure the controls", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 12))

                    button1 = tk.Button(debugFrame, text="Mouse", command=run.program1, width=10, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
                    button2 = tk.Button(debugFrame, text="Two-handed Gesture", command=run.program2, width=20, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
                    button3 = tk.Button(debugFrame, text="Swipe Motion Gesture", command=run.program3, width=20, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
                    button4 = tk.Button(debugFrame, text="Hybrid Gestures", command=run.program4, width=20, height=2, bg=greyThree, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
                    
                    # Release control button
                    release_button = tk.Button(debugFrame, text="Reset Controls", command=quit.release_control, width=15, height=2, bg=greyTwo, fg=ui_Txt, activebackground=crimSon, border=0, font=(standardFont, 10))

                    gearScroll.pack(side="right", fill="y")
                    gearTF.pack(side="top", anchor="nw", fill="x")
                    gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
                    debugFrame.pack(anchor="w", fill="x")
                    testFrame.pack(anchor="w", fill="both")
            
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

                    button4.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button4,mahoGany, greyTwo)

                    release_button.pack(padx=5, pady=5, side="left", anchor="nw")
                    generalUI.button_hover(release_button, crimSon, greyTwo)
                
                    """
                    # Scrollbar Tester
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=greyThree, fg=ui_Txt, border=0, font=(standardFont, 20, boldForm))
                    label.pack(padx=10, pady=2)
                    """
                    
                    gearAct = True
                    onceMade_Settings = True
                else:
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    gearCanvas.bind("<Configure>", canvasResize)

            else:
                setClose()
  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up Settings: {e}")

# Sets the base path to the scripts. Currently os.getcwd() since it returns the current directory the code is in without the hardcoding issue
#base_path = f"Filepath/Folder"
base_path = os.getcwd()

# Version Number 
versionNum = "1.43"

# For tracking UI activity and subprocesses
tut_count = 0
gearAct = False
tutAct = False
faqAct = False
quitAct = False
onceMade_Quit = False
onceMade_Settings = False
filter = ""

process = None

gameDisplayArray = []
descDisplayArray = []
imgDisplayArray = []
gamesList = open('gamesList.txt', 'r')
tabFunc.gameDisplay(gamesList, filter)

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
standardFont = "Archivo Black"
boldForm = "bold"

testingTurquoise = "#00FFD5"

# Tracks which menu section is active
menuAct = "Game"

# Gets the resolution for the default monitor
MaxRes = pyautogui.size()

# Initialize the tkinter root window
root = tk.Tk()
root.title(f"Handflux - GUI Prototype {versionNum}")
root.geometry('1360x780')
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
    "GameInfo": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "Profiles": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "ProfileSet": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "Gestures": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo),
    "GestureSet": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=greyTwo)
}
tabFunc.run_gameMenu()

# Game Tab - Opens up a specific game & displays its desc. Has a button that transfers to profile
menuGameTab = tk.Button(uiMasterFrame, text="GAMES", command=tabFunc.run_gameMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))

gameMasterFrame = tk.Frame(uiDynamTabs["Game"], background=greyTwo)
gamesDisplay = tk.Frame(uiDynamTabs["Game"], background=greyTwo)

gameSearchBorder = tk.Frame(gameMasterFrame, background=mahoGany)
gameLabel = tk.Label(gameMasterFrame, text="GAMES & APPS", bg=greyTwo, fg=ui_Txt, font=(standardFont, 15, boldForm))
gameSearchBar = tk.Entry(gameMasterFrame, bg=greyFive, fg=ui_Txt, border=0, font=(standardFont, 10))
gameSearchButton= tk.Button(gameSearchBorder, text="Search", command=tabFunc.filterGame, bg=greyThree, fg=ui_Txt, border=0, activebackground=mahoGany, font=(standardFont, 11, boldForm))

gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
gameLabel.pack(padx=5, pady=15, side="left")
gameSearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
gameSearchButton.pack(padx=2,pady=2, anchor="center")
gameSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")
generalUI.button_hover(gameSearchButton,mahoGany, greyThree)

gamesDisplay.pack(padx=10, pady=5, side="top", fill="x")

for gItem in range(game_Count):
    gameFrame = tk.Frame(gamesDisplay, bg=greyFive)
    gameItem = tk.Text(gameFrame, bg=greyFive, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(standardFont, 10))
    gameItem.insert(tk.END, gameDisplayArray[gItem])
    gameItem.configure(exportselection=0, state="disabled")

    gameImg = PhotoImage(file = imgDisplayArray[gItem]).subsample(1,1)
    imgDisplayArray[gItem] = gameImg
    gameButton = tk.Button(gameFrame, image=gameImg, command=lambda gIter=gItem: tabFunc.game_Describe(gameDisplayArray[gIter]), bg=greyTwo, fg=ui_Txt, border=0)

    gameFrame.pack(padx=35, pady=20, side="left")
    gameButton.pack()
    gameItem.pack()
    
# Profile Tab - Displays the gestures mapped to a game. Has buttons that transfers to that gesture
menuProfileTab = tk.Button(uiMasterFrame, text="PROFILES", command=tabFunc.run_profileMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
profileLabel = tk.Label(uiDynamTabs["Profiles"], text="PROFILES", bg=greyTwo, fg=ui_Txt, font=(standardFont, 15, boldForm))

profileLabel.pack(padx=10, pady=5, side="left")

# Gestures Tab - Displays the gestures that are mapped. Has buttons that transfers or re-do that gesture
menuGestureTab = tk.Button(uiMasterFrame, text="GESTURES", command=tabFunc.run_gestureMenu, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
gestureLabel = tk.Label(uiDynamTabs["Gestures"], text="GESTURES", bg=greyTwo, fg=ui_Txt, font=(standardFont, 15, boldForm))

gestureLabel.pack(padx=10, pady=5, side="left")

# GUI Labels
TKlabel = tk.Label(uiMasterFrame, text=f"PROTOTYPE {versionNum}", anchor="ne", bg=greyTwo, fg=brightMahogany, font=(standardFont, 25, boldForm))

# Button to display a tutorial window/widget
tutorial_button = tk.Button(uiMiscFrame, text="HELP", command=run.tutorial, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))
generalUI.button_hover(tutorial_button, mahoGany, greyTwo)

# Miscellaneous UI Buttons
settings_img = PhotoImage(file = "settings.png")
scaled_settingsImg = settings_img.subsample(2, 2)
settings_button = tk.Button(uiMasterFrame, image=scaled_settingsImg, command=run.settings, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0)
faq_button = tk.Button(uiMiscFrame, text="FAQs", command=run.faq, width=10, height=2, bg=greyTwo, fg=ui_Txt, activebackground=mahoGany, border=0, font=(standardFont, 10))

# Exit button - better implemented as image
exit_button = tk.Button(uiMiscFrame, text="EXIT", command=quit.exit_program ,width=10, height=2, bg=greyTwo, fg=ui_Txt, border=0, font=(standardFont, 10))

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

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(exit_button, exitRed, greyTwo)

uiDynamFrame.pack(side="top", fill="x")

# Global Canvases
quitCan = tk.Canvas(root, width=400, height=300, bg=greyThree, highlightthickness=0)
tutCanvas = tk.Canvas(root, width=400, height=300, bg=greyThree, highlightthickness=0)
faqCanvas = tk.Canvas(root, width=400, height=300, bg=greyFour, highlightthickness=0)
gearCanvas = tk.Canvas(root, bg=greyFour, highlightthickness=0)

# Run the tkinter event loop
root.mainloop()