# Main program for GUI interface
import subprocess, os, psutil, tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog


# Additonal imports
import pyautogui, re
import time, threading
from pynput import *
from PIL import Image, ImageTk
# from pynput.keyboard import Controller, Key

class generalUI:
    # Changes the colour of the button whether if it hovers or not
    def button_hover(tkb, b_Hover, b_Release ):
        try:
            tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
            tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change the button's colour: {e}")

    # Centers the window upon changing the window settings or opening up the app
    def centerWindow(win):
        try:
            win.update_idletasks()

            winWidth = win.winfo_width()
            winHeight = win.winfo_height()

            screenWidth = win.winfo_screenwidth()
            screenHeight = win.winfo_screenheight()

            winX = int((screenWidth // 2) - (winWidth // 2))
            winY = int((screenHeight // 2) - (winHeight // 2))

            win.geometry(f"{winWidth}x{winHeight}+{winX}+{winY}")
            win.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to center the window: {e}")

class gameTabFunc:
    # For Game Tab Functions

    # Maps the gamesDisplay frame for usage, and changes the highlighted border to Games
    def __init__(self, gFrame):
        try:  
            self.gFrame = gFrame
            gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
            gameTabFunc.gameDisplay(gamesList, filter)
            gameTabFunc.id_Game(gFrame)
            for uiBorder in uiMasterFrame.winfo_children():
                uiBorder.config(bg=ui_AC1)
                menuGameTabBorder.config(bg=ui_AH1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display games: {e}")
    
    # Scroll Functions for Games Tab
    def gamesDConfig(e):
        gamesDisplay.configure(scrollregion=gamesDisplay.bbox("all"))

    def gamesDScroll(e):
        gamesDisplay.xview_scroll(-1 * (e.delta // 120), "units")

    # Swaps the current Tab to the Games Tab
    def run_gameMenu():
        global menuAct, uiDynamTabs, gameDisplay, gamesDFrame
        try:  
            def showF(uiGame):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiGame.pack(fill="both")

            if menuAct != "Game":
                showF(uiDynamTabs["Game"])
                menuAct = "Game"
                gameDisplay.pack_forget()
                
                gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                gamesDisplay.create_window((0, 0), window=gamesDFrame)

                gamesDisplay.bind("<Configure>", gameTabFunc.gamesDConfig)
                gamesDisplay.bind_all("<MouseWheel>", gameTabFunc.gamesDScroll)
                gameTabFunc(gamesDFrame)
            else: 
                # Sets Game Menu tab as the default tab first
                showF(uiDynamTabs["Game"])      
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")

    # Displays the games list
    def id_Game(self):
        try:
            # Clears the old list
            for gItem in self.winfo_children():
                gItem.destroy()

            # Filepath definitions - Placeholder for Improper filepaths, and Add Game for addGameButton
            placeThumb = base_path + "\\img\\gameimg\\placeholder.png"
            addThumb = base_path + "\\img\\plus.png"

            # Fills the new list
            for gItem in range(game_Count):
                gameFrame = tk.Frame(self, bg=ui_AC4)
                gameItem = tk.Text(gameFrame, bg=ui_AC4, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(ui_Font, 10))
                gameItem.insert(tk.END, gameDisplayArray[gItem])
                gameItem.configure(exportselection=0, state="disabled")

                if os.path.isfile(thumbDisplayArray[gItem]):
                    giIMG = Image.open(thumbDisplayArray[gItem])  
                    giForm = giIMG.resize((220, 300))
                    gameImg = ImageTk.PhotoImage(giForm)
                    thumbDisplayArray[gItem] = gameImg
                    gameButton = tk.Button(gameFrame, image=gameImg, command=lambda gIter=gItem: gameTabFunc.game_Describe(gameDisplayArray[gIter]), bg=ui_AC1, fg=ui_Txt, border=0)
                else:
                    giIMG = Image.open(placeThumb)  
                    giForm = giIMG.resize((220, 300))
                    gameImg = ImageTk.PhotoImage(giForm)
                    thumbDisplayArray[gItem] = gameImg
                    gameButton = tk.Button(gameFrame, image=gameImg, command=lambda gIter=gItem: gameTabFunc.game_Describe(gameDisplayArray[gIter]), bg=ui_AC1, fg=ui_Txt, border=0)

                gameFrame.pack(padx=25, pady=25, side="left", anchor="w")
                gameButton.pack(padx=2, pady=2)
                generalUI.button_hover(gameButton, ui_AH1, ui_AC1)
                gameItem.pack()
            
            addGameF = tk.Frame(self, bg=ui_AC4)

            agiIMG = Image.open(addThumb)  
            agiForm = agiIMG.resize((220, 300))
            addGameIMG = ImageTk.PhotoImage(agiForm)
            addGameButton = tk.Button(addGameF, image=addGameIMG, command= gameTabFunc.addGame, bg=ui_AC1, fg=ui_Txt, border=0)
            addGameButton.image = addGameIMG
            generalUI.button_hover(addGameButton, ui_AH1, ui_AC1)

            addGameF.pack(padx=25, pady=25,side="left", anchor="w")
            addGameButton.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fill the game tab: {e}")
        
    # Gets the available games from gamesList.txt using filters from filterGame
    def gameDisplay(txt, filter):
        global game_Count, gamesList, gameDisplayArray, descDisplayArray, gamesList
        try:
            # Resets the list
            game_Count = 0
            gameDisplayArray.clear()
            descDisplayArray.clear()
            thumbDisplayArray.clear()
            exeDisplayArray.clear()
            # Redundant Filter check
            if filter:
                filterForm = filter.upper()
                # Fills the list with the filter results
                for line in txt:
                    if f"GameÃ· {filterForm}" in line:
                        gameName = line.split("Ã· ")
                        game_Count += 1
                        gameDisplayArray.append(gameName[2].replace("\n",""))
            
                    elif f"DescÃ· {filterForm}" in line:
                        gameDesc = line.split("Ã· ")
                        descDisplayArray.append(gameDesc[2].replace("\n",""))
            
                    elif f"ThumbImgÃ· {filterForm}" in line:
                        gameThumb = line.split("Ã· ")
                        file = base_path + gameThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif f"ExeÃ· {filterForm}" in line:
                        gameExe = line.split("Ã· ")
                        file = gameExe[2].replace("\n","")
                        exeDisplayArray.append(file)
            else:
                # Default list filling
                for line in txt:
                    if "GameÃ· " in line:
                        gameName = line.split("Ã· ")
                        game_Count += 1
                        gameDisplayArray.append(gameName[2].replace("\n",""))
            
                    elif "DescÃ· " in line:
                        gameDesc = line.split("Ã· ")
                        descDisplayArray.append(gameDesc[2].replace("\n",""))
            
                    elif "ThumbImgÃ· " in line:
                        gameThumb = line.split("Ã· ")
                        baseCheck = gameThumb[2].startswith("BASE")
                        if baseCheck:
                            txt = gameThumb[2].replace("\n","")
                            txt2 = txt.replace("BASE","")
                            file = base_path + txt2
                        else:
                            file = gameThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif "ExeÃ· " in line:
                        gameExe = line.split("Ã· ")
                        file = gameExe[2].replace("\n","")
                        exeDisplayArray.append(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the games: {e}")

    # Filters the output of gameDisplay
    def filterGame():
        global gamesList, gamesDisplay, gamesDFrame
        try:
            filter = gameSearchBar.get()
            if filter !="":
                gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
                gameTabFunc.gameDisplay(gamesList, filter)
                gameTabFunc.id_Game(gamesDFrame)
                gameSearchBar.delete(0, "end")
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
    
    # Resets the filters in filterGame
    def resetFilter():
        global gamesList, gamesDisplay, gamesDFrame
        try:
            filter = ""
            gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
            gameTabFunc.gameDisplay(gamesList, filter)
            gameTabFunc.id_Game(gamesDFrame)
            gameSearchBar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset the filters: {e}")

    # UI for adding a game to gamesList
    def addGame():
        global gamesDisplay, gameMasterFrame, gameDisplay, gamesDFrame

        # Goes back to the Games Tab and clears the data in add game tab
        def goBack():
            global imgPath, exePath
            try:
                imgPath = ""
                exePath = ""
                gameDisplay.pack_forget()
                gameTabFunc(gamesDFrame)
                gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                gamesDisplay.create_window((0, 0), window=gamesDFrame)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to go back to the Games Tab: {e}")
        
        # Writes the EXE filepath to gameItemFile
        def writeEXE():
            global exePath
            try:
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",filetypes = [('Executables', '*.exe')])
                if filepath_New:
                    exePath = filepath_New
                    # Changes the filepath in the game description
                    addGameFPDesc.configure(text = filepath_New)
                else:
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Failed to modify EXE filepath: {e}")
        
        # Writes the image's filepath to gameItemImg
        def writeIMG():
            global imgPath
            try:
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",filetypes=[('Image files', '*.png *.jpg *.jpeg')])
                if filepath_New:
                    imgPath = filepath_New
                    newImg = Image.open(filepath_New)  
                    newImgS = newImg.resize((220, 300))
                    newImgSS = ImageTk.PhotoImage(newImgS)
                    addGameImg.configure(image = newImgSS)
                    addGameImg.image = newImgSS
                else:
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply new picture to thing: {e}")

        # Adds the game to games list
        def addToGL():
            global imgPath, exePath
            try:
                # Retrieves the data entered
                gameN = addGameLabel.get("1.0","end-1c")
                gameD = addGameTXT.get("1.0","end-1c")

                # Checks the fields from the entered data
                if imgPath == "":
                    imgPath = base_path + f"\\img\\gameimg\\Placeholder.png"
                else:
                    pass
                if exePath == "":
                    messagebox.showinfo("Warning","One or more fields are not filled")
                    return
                if gameN == "Add game name here":
                    gameName = "SAMPLE GAME"
                else:
                    gameName = gameN.upper()
                if gameD == "Add game description here":
                    gameDesc = "Sample Desc"
                else:
                    gameDesc = gameD

                addGList = open(f"{base_path}\\resources\\gamesList.txt", "a")
                addGList.write(f"\n \nGameÃ· {gameName}Ã· {gameName} \n")
                addGList.write(f"DescÃ· {gameName}Ã· {gameDesc} \n")
                addGList.write(f"ThumbImgÃ· {gameName}Ã· {imgPath} \n")
                addGList.write(f"ExeÃ· {gameName}Ã· {exePath}")
                addGList.close()
                messagebox.showinfo("You have added a Game to the list!","Feel free to go back to the main menu")
                goBack()
                gameTabFunc(gamesDFrame)
            except NameError:
                messagebox.showinfo("Warning","One or more fields are not filled")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add games to games list: {e}")

        try:
            # Hides the game selection tab
            gameMasterFrame.pack_forget()
            gamesDisplay.pack_forget()
            gameDisplay.pack(padx=10, pady=1, side="top", fill="x")

            # Clears the old items
            for gItem in gameDisplay.winfo_children():
                gItem.destroy()
                gameDetails.clear()

            # Displays the Add Game UI
            game_DisplayFrame = tk.Frame(gameDisplay, bg=ui_AC2)
            game_DisplayPicFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_TutFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_InfoFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_AddFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)

            addGameLabel = tk.Text(gameDisplay, width=75, height=2, wrap="word", bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))
            addGameLabel.insert(tk.END, "Add game name here")

            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))

            agiIMG = Image.open(base_path + f"\\img\\gameimg\\Placeholder.png")  
            agiForm = agiIMG.resize((220, 300))
            addGameItemImg = ImageTk.PhotoImage(agiForm)
            addGameImg = tk.Button(game_DisplayPicFrame, image=addGameItemImg, command=writeIMG, bg=ui_AC1, fg=ui_Txt, border=0)
            addGameImg.image = addGameItemImg
            agiLabel = tk.Label(game_TutFrame, text="Click on the white area to add your own image", height=1, bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 12))

            addGameTXT = tk.Text(game_DisplayFrame, width=65, height=5, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            addGameTXT.insert(tk.END, "Add game description here")

            addGameFP = tk.Button(game_InfoFrame, text="Configure Filepath (REQUIRED)", command=writeEXE, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            addGameFPDesc = tk.Label(game_InfoFrame, text="Filepath", wraplength=MaxRes[0], height=1, justify="left", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 12))

            addGameButton = tk.Button(game_AddFrame, text="Add Game to Games List", command=addToGL, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))

            game_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            
            game_AddFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_TutFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            
            addGameLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)
            
            addGameImg.pack(padx=4, pady=4, side="left", anchor="nw")
            addGameTXT .pack(padx=4, pady=4, side="left", anchor="nw")
            
            addGameFP.pack(padx=4, pady=4, side="left", anchor="w")
            addGameFPDesc.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(addGameFP, ui_AH1, ui_AC1)

            agiLabel.pack(padx=4, pady=4, side="top", anchor="nw")

            addGameButton.pack(padx=4, pady=4, side="bottom", anchor="nw")
            generalUI.button_hover(addGameButton, ui_AH1, ui_AC1)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display Game Adder UI: {e}")

    # Displays that specific game 
    def game_Describe(gameItem):
        global gamesDisplay, gameMasterFrame, gameDetails, gameDisplay, gameProcess, gamesList, process, gControls, gamesDFrame

        # Goes back to the Games Tab
        def goBack():
            try:
                gameDisplay.pack_forget()
                gameTabFunc(gamesDFrame)
                gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                gamesDisplay.create_window((0, 0), window=gamesDFrame)
                gItemExt.clear()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to go back to the Games Tab: {e}")

        # Runs the exe described in the filepath
        def runGame():
            def gameCheck(proc):
                while True:
                    procs = [proc.name() for proc in psutil.process_iter()]
                    if proc not in procs:
                        #quit.release_control()
                        break
                    time.sleep(1)

            def gameStart(proc):
                thread = threading.Thread(target=gameCheck, args=(proc,))
                thread.daemon = True
                thread.start()

            def runControl():
                controlIndex = controlsList.get()
                controllerProgram = gControls[controlIndex]
                controllerProgram()   

            try:
                gameEXE = gameDetails[3]
                gameEXE = gameEXE.split("/")

                if len(gameDetails[3]) == 0 or gameDetails[3] == "Filepath":
                    messagebox.showerror("Error", "Game's EXE filepath is NOT configured")
                else:
                    # Starts up the respective game's control and game
                    os.startfile(gameDetails[3])
                    gameStart(gameEXE[-1])
                    runControl()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run the game: {e}")

        # Experimental function to write the filepath for an EXE to the gamesList
        def writeEXE():
            try:
                # Formats the filepath to fit the gamesList format
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",filetypes = [('Execitables', '*.exe')])
                if filepath_New:
                    filepath_Change = f"ExeÃ· {gameItem}Ã· {filepath_New}"
                    with open(f"{base_path}\\resources\\gamesList.txt", "r") as txt:
                        gameWrite = txt.readlines()

                    filepath_Update = False
                    with open(f"{base_path}\\resources\\gamesList.txt", "w") as txt:
                        for line in gameWrite:
                            if not filepath_Update and f"ExeÃ· {gameItem}Ã· " in line:
                                txt.write(filepath_Change + "\n")
                                gameDetails[3] = filepath_New
                                filepath_Update = True
                            else:
                                txt.write(line)
                    # Changes the filepath in the game description
                    gameItemFile.configure(text = filepath_New)
                else:
                    messagebox.showinfo("Warning: ", "Select an executable application to change the filepath")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to modify Exe's Filepath: {e}")
        try:
            # Hides the game selection tab
            gameMasterFrame.pack_forget()
            gamesDisplay.pack_forget()
            gameDisplay.pack(padx=10, pady=1, side="top", fill="x")

            # Clears the old items
            for gItem in gameDisplay.winfo_children():
                gItem.destroy()
                gameDetails.clear()
            
            gItemExt = gameItem.split()

            # Gets the new items
            with open(f"{base_path}\\resources\\gamesList.txt", "r") as gameGet:
                for line in gameGet:
                    if f"GameÃ· {gItemExt[0]}" in line:
                        gameName = line.split("Ã· ")
                        gameDetails.append(gameName[2].replace("\n",""))
                
                    elif f"DescÃ· {gItemExt[0]}" in line:
                        gameDesc = line.split("Ã· ")
                        gameDetails.append(gameDesc[2].replace("\n",""))
                
                    elif f"ThumbImgÃ· {gItemExt[0]}" in line:
                        gameThumb = line.split("Ã· ")
                        baseCheck = gameThumb[2].startswith("BASE")
                        if baseCheck:
                            txt = gameThumb[2].replace("\n","")
                            txt2 = txt.replace("BASE","")
                            file = base_path + txt2
                        else:
                            file = gameThumb[2].replace("\n","")
                        gameDetails.append(file)
                    
                    elif f"ExeÃ· {gItemExt[0]}" in line:
                        gameExe = line.split("Ã· ")
                        file = gameExe[2].replace("\n","")
                        gameDetails.append(file)

            # Displays the selected game
            game_DisplayFrame = tk.Frame(gameDisplay, bg=ui_AC2)
            game_DisplayPicFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_InfoFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_RunFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            gameItemLabel = tk.Label(gameDisplay, text=gameDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            
            if os.path.isfile(gameDetails[2]):
                giIMG = Image.open(gameDetails[2])  
                giFormat = giIMG.resize((220, 300))
                gameItemImg = ImageTk.PhotoImage(giFormat)
                gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
                gameImg.image = gameItemImg
            else:
                giIMG = Image.open(base_path + f"\\img\\gameimg\\Placeholder.png")  
                giFormat = giIMG.resize((220, 300))
                gameItemImg = ImageTk.PhotoImage(giFormat)
                gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
                gameImg.image = gameItemImg

            gameItemTxt = tk.Text(game_DisplayFrame, width=65, height=5, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            gameItemTxt.insert(tk.END, gameDetails[1])
            gameItemTxt.configure(exportselection=0, state="disabled")  

            gameItemFileP = tk.Button(game_InfoFrame, text="Configure Filepath", command=writeEXE, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gameItemFile = tk.Label(game_InfoFrame, text=gameDetails[3], wraplength=MaxRes[0], height=1, justify="left", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 12))
            
            gameItemExe = tk.Button(game_RunFrame, text=f"Start Game with selected controller", command=runGame, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gameRelease = tk.Button(game_RunFrame, text=f"Release Gesture Control", command=quit.release_control, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))

            game_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            game_RunFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            gameItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            controlsList = tk.StringVar(root)
            controlsList.set(next(iter(gControls)))
            gameControls = tk.OptionMenu(game_RunFrame, controlsList, *gControls.keys())
            gameControls.configure(bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, highlightbackground=ui_AC1, font=(ui_Font, 12))

            gameControls.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)

            gameImg.pack(padx=4, pady=4, side="left", anchor="nw")
            gameItemTxt.pack(padx=4, pady=4, side="left", anchor="nw")

            gameItemFileP.pack(padx=4, pady=4, side="left", anchor="nw")
            generalUI.button_hover(gameItemFileP, ui_AH1, ui_AC1)
            gameItemFile.pack(padx=4, pady=4, side="left", anchor="nw")
            
            gameRelease.pack(padx=8, pady=8, side="bottom", anchor="nw")
            generalUI.button_hover(gameRelease, ui_AH1, ui_AC1)
            
            gameItemExe.pack(padx=8, pady=8, side="bottom", anchor="nw")
            generalUI.button_hover(gameItemExe, ui_AH1, ui_AC1)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the individual game: {e}")
      
class bindsTabFunc:
    # For Keybinds Tab Functions

    # Changes the highlighted border to Keybinds
    def __init__(self, gFrame):
        try:  
            self.gFrame = gFrame
            for uiBorder in uiMasterFrame.winfo_children():
                uiBorder.config(bg=ui_AC1)
                menuBindsTabBorder.config(bg=ui_AH1)
                bindsTabFunc.loadKeys()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display keybinds: {e}")

    # Swaps the current tab to the Keybinds Tab
    def run_bindsMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Profile Tab - Shows the profiles the user set
            def showF(uiBinds):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiBinds.pack(fill="both")

            if menuAct != "Keybind":
                showF(uiDynamTabs["Binds"])
                menuAct = "Keybind"
                bindsCanvas.pack_forget()
                bindsTabFunc(bindsCanvas)
                bindsMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                bindsCanvas.pack(padx=10, pady=1, side="left", fill="both")
                bindsMasterFrame.pack(padx=5, pady=15, side="top")
                bindsLabel.pack(padx=10, pady=10, side="left", anchor="nw")
                saveBinds.pack(padx=10, pady=10, side="left", anchor="nw")
                resetBinds.pack(padx=10, pady=10, side="left", anchor="nw")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Keybinds Tab: {e}")
        
    # Updates the assigned key to the pressed key
    def updateKeys(gesture):
        #global bindChange
        try:

            def keyPress(newKeybind):
                
                newKey = newKeybind.keysym
                initBinds[gesture] = newKey
                bindLabel[gesture].config(text=f"Key*: {newKey}")
                root.unbind("<KeyPress>")
                messagebox.showinfo("Keybind Updated", f"{gesture} is now bound to {newKey}")
            
            root.bind("<KeyPress>", keyPress)
            #bindChange[gNumber].config(text="Listening...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update the keybind: {e}")

    def saveKeys():
        global handOption
        try:
            # Reset the changes
            changeArray = []

            # Consolidates the changes
            for gesture, key in initBinds.items():
                newBind = f"{gesture}={key}\n"
                changeArray.append(newBind)

            with open(f"{base_path}\\resources\\gesture_key_mapping.txt", 'r') as baseLine:
                changeLines = baseLine.readlines()
            
            if handOption.get() == "Left":
                for change in range(len(changeLines[0:12])):
                    changeLines[change] = changeArray[change]
            else:
                for change in range(len(changeLines[13:])):
                    changeLines[change] = changeArray[change]
            
            with open(f"{base_path}\\resources\\gesture_key_mapping.txt", 'w') as newBinds:
                newBinds.writelines(changeLines)

            messagebox.showinfo("Keybinds Saved", "Keybinds are saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save keybinds: {e}")

    def loadKeys():
        global bindChange, handOption
        try:
            def canvasConfig(e):
                bindsCanvas.configure(scrollregion=bindsCanvas.bbox("all"))

            def mouseScroll(e):
                bindsCanvas.yview_scroll(-1 * (e.delta // 120), "units")

            def switchHands(*args):
                activeHand = handOption.get()
                activeHV = hControls[activeHand]
                generateKey(activeHV)
            
            def generateKey(e):
                try:
                    # Clears the old selections
                    gNumber = 0
                    for bindings in bindFrame.values():
                        bindings.pack_forget()

                    with open(f"{base_path}\\resources\\gesture_key_mapping.txt", "r") as line:
                        for binds in line:
                            # Splits gestures and keybinds
                            gesture, key = binds.strip().split("=")

                            # Filters out the respective hand gestures
                            if e in binds:
                                initBinds[gesture] = key
                                bindFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)
                                keyFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)
                                imgFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)

                                gestureFormat = gesture.split(":")
                                bindAction = tk.Label(bindFrame[gNumber], text=f"{gestureFormat[0].capitalize()} Hand: {gestureFormat[1].capitalize()}", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

                                # Checks if the image file exists
                                imgS = base_path + f"\\img\\gestureimg\\{gestureFormat[1]}.png"
                                if os.path.isfile(imgS):
                                    gtIMG = Image.open(imgS)  
                                    gtForm = gtIMG.resize((150, 150))
                                    gestThumb = ImageTk.PhotoImage(gtForm)
                                    gestImg = tk.Label(keyFrame[gNumber], image=gestThumb, bg=ui_AC1, fg=ui_Txt, border=0)
                                    gestImg.image = gestThumb
                                else:
                                    gtIMG = Image.open(base_path + f"\\img\\gestureimg\\placeholder.png")  
                                    gtForm = gtIMG.resize((150, 150))
                                    gestThumb = ImageTk.PhotoImage(gtForm)
                                    gestImg = tk.Label(keyFrame[gNumber], image=gestThumb, bg=ui_AC1, fg=ui_Txt, border=0)
                                    gestImg.image = gestThumb

                                bindLabel[gesture] = tk.Label(keyFrame[gNumber], text=f"Key: {key}",bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))
                                bindChange[gNumber] = tk.Button(keyFrame[gNumber], text="Change", command=lambda a=gesture: bindsTabFunc.updateKeys(a), bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 15, ui_Bold))
                                bindFrame[gNumber].pack(padx=10, pady=5, anchor="nw")
                                keyFrame[gNumber].pack(padx=10, pady=5, anchor="nw")
                                imgFrame[gNumber].pack(padx=10, pady=5, anchor="nw")
                                
                                bindAction.pack(padx=5, side="left")
                                gestImg.pack(padx=5, pady=5, side="left", anchor="nw")
                                bindLabel[gesture].pack(padx=5, side="left")

                                bindChange[gNumber].pack(padx=5, side="right", anchor="e")
                                generalUI.button_hover(bindChange[gNumber], ui_AH1, ui_AC1)
                                gNumber += 1
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate the keybinds: {e}")

            # Shows the keybinds menu
            bindMaster = tk.Frame(bindsCanvas, padx=5, pady=5, bg=ui_AC2)
            bindsCanvas.create_window((0, 0), window=bindMaster)

            handOption = tk.StringVar(root)
            handOption.set(next(iter(hControls)))
            handOption.trace_add("write", switchHands)
            
            dropFrame = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)
            drop = tk.OptionMenu(dropFrame, handOption, *hControls)
            drop.configure(bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, highlightbackground=ui_AC1, font=(ui_Font, 12))

            bindMaster.bind("<Configure>", canvasConfig)
            bindsCanvas.bind_all("<MouseWheel>", mouseScroll)

            dropFrame.pack(padx=20, pady=5, anchor="nw")
            drop.pack(side="left")
            generateKey(hControls["Left"])
                    
        except FileNotFoundError:
            print("No keybinds found")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the keybind menu: {e}")

class settingsFunc:
    # For Settings tab functions
    # Display the settings
    def display_Settings():
        global gearAct, gearCanvas, onceMade_Settings, gearSettings
        try:
            # Checks if Escape key is pressed
            def settingKey(key):
                if key.keysym == "Escape":
                    setClose()
            
            def canvasConfig(e):
                gearCanvas.configure(scrollregion=gearCanvas.bbox("all"))

            def mouseScroll(e):
                gearCanvas.yview_scroll(-1 * (e.delta // 120), "units")
            
            def canvasResize(e):
                if not isinstance(e, int):
                    gearCanvas.itemconfig(gearSettings, width=e.width)        
                else:
                    gearCanvas.itemconfig(gearSettings, width=e)

            # Closes the settings
            def setClose():
                global gearAct
                gearCanvas.place_forget()
                gearAct = False

            # Toggles the display mode
            def toggleWindowState(state):
                # Resets the state of the display first
                root.attributes('-fullscreen',False)
                root.overrideredirect(False)

                # Checks what button has been pressed
                if state == "fullscreen":
                    root.attributes('-fullscreen',True)
                    generalUI.centerWindow(root)
                elif state == "borderless":
                    root.overrideredirect(True)
                    generalUI.centerWindow(root)
                elif state == "windowed":
                    root.attributes('-fullscreen',False)
                    root.overrideredirect(False)
                    generalUI.centerWindow(root)
                else:
                    print("Invalid window state")
                    pass

            if not gearAct:
                if not onceMade_Settings:
                    # Settings process - Tkinter overlay to change settings
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                
                    root.bind("<Key>", settingKey)
            
                    gearMaster = tk.Frame(gearCanvas, padx=5, pady=5, bg=ui_AC1)
                    gearSettings = gearCanvas.create_window((0, 0), window=gearMaster)

                    gearMaster.bind("<Configure>", canvasConfig)
                    gearCanvas.bind("<Configure>", canvasResize)
                    gearCanvas.bind_all("<MouseWheel>", mouseScroll)

                    gearTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC1)
                    gearTitle = tk.Label(gearTF, text="SETTINGS", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))
                    closeGear = tk.Button(gearTF, text="RETURN", command=setClose, width=10, height=0, bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))

                    """
                    # Debug Controls
                    debugFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    debugLabel = tk.Label(debugFrame, text="DEBUG", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    debugDescLabel = tk.Label(debugFrame, text="For devs to configure the controls", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))

                    button1 = tk.Button(debugFrame, text="Mouse", command=run.program1, width=8, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button2 = tk.Button(debugFrame, text="Two-handed Gesture", command=run.program2, width=17, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button3 = tk.Button(debugFrame, text="Swipe Motion Gesture", command=run.program3, width=18, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button4 = tk.Button(debugFrame, text="Hybrid Gestures", command=run.program4, width=14, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button5 = tk.Button(debugFrame, text="HB2", command=run.program5, width=8, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button7 = tk.Button(debugFrame, text="Steering 2", command=run.program7, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    release_button = tk.Button(debugFrame, text="Reset Controls", command=quit.release_control, width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    """

                    # Toggles window state
                    winStateTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    winStateFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    winStateLabel = tk.Label(winStateTF, text="DISPLAY", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    winStateDescLabel = tk.Label(winStateTF, text="Modify the display mode of the App", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))
                    
                    fullscreen_button = tk.Button(winStateFrame, text="Fullscreen", command=lambda:toggleWindowState("fullscreen"), width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    borderless_button = tk.Button(winStateFrame, text="Borderless Windowed", command=lambda:toggleWindowState("borderless"), width=20, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    windowed_button = tk.Button(winStateFrame, text="Windowed", command=lambda:toggleWindowState("windowed"), width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))

                    helperTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    helperFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    helperLabel = tk.Label(helperTF, text="HELP", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    helperDescLabel = tk.Label(helperTF, text="Contains info on how to use the App", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))

                    tutorial_button = tk.Button(helperFrame, text="HELP", command=run.tutorial, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    faq_button = tk.Button(helperFrame, text="FAQs", command=run.faq, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

                    gearTF.pack(side="top", anchor="nw", fill="x")
                    gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
                    #debugFrame.pack(anchor="w", fill="x")

                    winStateTF.pack(side="top", anchor="nw", fill="x")
                    winStateFrame.pack(anchor="w", fill="x")

                    helperTF.pack(side="top", anchor="nw", fill="x")
                    helperFrame.pack(anchor="w", fill="x")
            
                    closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
                    generalUI.button_hover(closeGear,ui_AH1, ui_AC1)

                    #debugLabel.pack(padx=10, pady=5, anchor="nw")
                    #debugDescLabel.pack(padx=10, pady=2, anchor="nw")
                    
                    winStateLabel.pack(padx=10, pady=5, anchor="nw")
                    winStateDescLabel.pack(padx=10, pady=2, anchor="nw")

                    helperLabel.pack(padx=10, pady=5, anchor="nw")
                    helperDescLabel.pack(padx=10, pady=2, anchor="nw")

                    """
                    button1.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button1,ui_AH1, ui_AC1)

                    button2.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button2,ui_AH1, ui_AC1)

                    button3.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button3,ui_AH1, ui_AC1)

                    button4.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button4,ui_AH1, ui_AC1)

                    button5.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button5,ui_AH1, ui_AC1)

                    button7.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button7,ui_AH1, ui_AC1)

                    release_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(release_button, ui_AH1, ui_AC1)
                    """

                    fullscreen_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(fullscreen_button, ui_AH1, ui_AC1)

                    borderless_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(borderless_button, ui_AH1, ui_AC1)

                    windowed_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(windowed_button, ui_AH1, ui_AC1)

                    tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")
                    generalUI.button_hover(tutorial_button, ui_AH1, ui_AC1)

                    faq_button.pack(padx=5, pady=5, side="left", anchor="nw")
                    generalUI.button_hover(faq_button, ui_AH1, ui_AC1)

                    gearAct = True
                    onceMade_Settings = True
                else:
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    canvasResize(root.winfo_width())
                    gearAct = True
            else:
                setClose()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up Settings: {e}")

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
                ["py", os.path.join(base_path, "MouseControl.py")],
                shell=True
            )

            # Debugging info 
            print(f"Started Mouse Control with PID: {process.pid}")

            # For runGame to process
            return process
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
                ["py", os.path.join(base_path, "control_2hands.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Two Hands Gesture Control with PID: {process.pid}")

            # For runGame to process
            return process
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
                ["py", os.path.join(base_path, "swipeControl.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Swipe Motion Gesture Control with PID: {process.pid}")
            
            # For runGame to process
            return process
        
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
                ["py", os.path.join(base_path, "hybrid.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Hybrid Gesture Control with PID: {process.pid}")
            
            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Hybrid Gesture Control: {e}")
    
    def program5():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for HB2 Gesture Control Program
            process = subprocess.Popen(
                ["py", os.path.join(base_path, "hb2.py")],
                shell=True
            )
            # Debugging info
            print(f"Started HB2 Gesture Control with PID: {process.pid}")

            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run HB2 Gesture Control: {e}")
    
    def program6():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for HB2 Gesture Control Program
            process = subprocess.Popen(
                ["py", os.path.join(base_path, "steering.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Steering 1 Gesture Control with PID: {process.pid}")

            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Steering 1 Gesture Control: {e}")

    def program7():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for HB2 Gesture Control Program
            process = subprocess.Popen(
                ["py", os.path.join(base_path, "steering2.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Steering 2 Gesture Control with PID: {process.pid}")

            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Steering 2 Gesture Control: {e}")

    def program8():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            # Placeholder for HB2 Gesture Control Program
            process = subprocess.Popen(
                ["py", os.path.join(base_path, "again2.py")],
                shell=True
            )
            # Debugging info
            print(f"Started Again 2 Gesture Control with PID: {process.pid}")

            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Again Gesture Control: {e}")

    def tutorial():
        global tutAct, MaxRes, tut_count, tutCanvas, onceMade_Tut
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
            
            root.bind("<Key>", tutKey)
            # Displays the tutorial canvas
            if not tutAct:
                if not onceMade_Tut:
                    tutCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    tk.Misc.lift(tutCanvas)

                    tutFrame = tk.Frame(tutCanvas, padx=5, pady=5, bg=ui_AC2)

                    tutContent = [
                        tk.Label(tutFrame, text="GETTING STARTED", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 25, ui_Bold)),
                        tk.Label(tutFrame, text="To close, click the button labelled 'Close', or press the Escape Key", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 18, ui_Bold)),
                        tk.Label(tutFrame, text="Games – Shows the supported games",  bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Keybinds – Shows the gestures and the keys they are mapped to",  bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Settings – Opens up the settings for you to fine tune", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold))
                    ]
                    closeTut = tk.Button(tutFrame, text="Close", command=tutClose, border=0, bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))

                    tutFrame.pack(anchor="nw")
                    for e in range(len(tutContent)):
                        tutItem = tutContent[e]
                        tutItem.pack(padx=5, pady=5, anchor="nw")
                    closeTut.pack(padx=5, pady=5, anchor="nw")
                    generalUI.button_hover(closeTut, ui_AH1, ui_AC2)
                    tutAct = True
                    onceMade_Tut = True
                else:
                    tutCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    tk.Misc.lift(tutCanvas)
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
                with open(f"{base_path}\\resources\\faq_text.txt", "r") as txtfile:
                    faq_text = txtfile.read()
                    faqtxt.insert(tk.END, faq_text)
            
            root.bind("<Key>", faqKey)
            # Checks if FAQ UI is opened
            if not faqAct:
                # Opens FAQ UI and brings it to the front
                faqCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                tk.Misc.lift(faqCanvas)

                # FAQ Frame & Scrollbar to navigate
                faqTF = tk.Frame(faqCanvas, padx=5, pady=5, bg=ui_AC1)
                faqFrame = tk.Frame(faqCanvas, padx=5, pady=5, bg=ui_AC3)
                faqScroll = tk.Scrollbar(faqCanvas)

                # Text Element to input FAQ Items
                faqtxt = tk.Text(faqFrame, yscrollcommand = faqScroll.set, bg=ui_AC3, height=MaxRes[0], width=MaxRes[1], font=(ui_Font, 14), fg=ui_Txt, border=0, wrap="word")

                # Label and button to close the FAQ Window
                FAQlabel = tk.Label(faqTF, text="Frequently Asked Questions", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 20, ui_Bold))
                close_faq = tk.Button(faqTF, text="Return", command=faqClose, width=10, height=0, bg=ui_AH1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))

                # GUI Layout
                faqTF.pack(side="top", anchor="nw", fill="x")
                FAQlabel.pack(pady=5, side="left", anchor="nw")
                close_faq.pack(padx=30, pady=15, side="right", anchor="ne")
                generalUI.button_hover(close_faq,ui_AH1, ui_AC1)
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

class quit:
    # Class for closing the window
    def exit_program():
        global quitCan, quitAct, onceMade_Quit, gamesList
        try:
            # Closes everything and ensures any running process is terminated before exiting
            def zeroAll():
                gamesList.close()
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
        
                    quitLabel = tk.Label(quitCan, text="Do you want to quit?", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))
                    yesButton = tk.Button(quitCan, text="YES", command=zeroAll ,width=15, height=3, bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20))
                    noButton = tk.Button(quitCan, text="NO", command=stayIn ,width=15, height=3, bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20))

                    quitLabel.pack(padx=25, pady=25, anchor="center")
                    yesButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(yesButton, ui_AE, ui_AC2)

                    noButton.pack(padx=25, pady=25, anchor="center")
                    generalUI.button_hover(noButton, ui_AE, ui_AC2)
                    quitAct = True
                    onceMade_Quit = True
                else:
                    quitCan.place(relheight=1, relwidth=1)
                    quitAct = True
            else:
                messagebox.showerror("Info", "Something went wrong here") 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up quit confirmation: {e}") 

    def exit_viaKey(key):
        global quitAct
        if not quitAct:
            if key.keysym == "Escape" and quitCan.winfo_ismapped and tutCanvas.winfo_ismapped != True and faqCanvas.winfo_ismapped !=True:
                quit.exit_program()
                #quitAct = True
            else:
                #print("One or more UIs are active")
                pass
    
    def release_control():
        global process
        if process is not None:
            try:
                # Terminate process and all its children
                parent = psutil.Process(process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                process.wait()  # Ensure the process is fully terminated
                print("Process and its children terminated successfully.")  # Debugging info
                process = None
                messagebox.showinfo("Info", "Running program has been terminated.")
            except psutil.NoSuchProcess:
                process = None
            except Exception as e:
                messagebox.showerror("Error", f"Failed to terminate the program: {e}")
        else:
            print("No process to terminate.")  # Debugging info
            #messagebox.showinfo("Info", "No program is currently running.") - Commented to streamline UI modifiactions -Jun Hong

# Sets the base path to the scripts. Currently os.getcwd() since it returns the current directory the code is in without the hardcoding issue
base_path = os.getcwd()

# Version Number 
versionNum = "1.5"

# For tracking UI activity and subprocesses
#gNumber = 0
tut_count = 0
faqAct = False
gearAct = False
quitAct = False
tutAct = False
onceMade_Quit = False
onceMade_Settings = False
onceMade_Tut = False
filter = ""

imgPath = ""
exePath = ""

process = None
gameProcess = None

gameDisplayArray = []
descDisplayArray = []
thumbDisplayArray = []
exeDisplayArray = []
profileDisplayArray = []
gameDetails = []
profileDetails = []
gestureDetails = []
unMapped = []
unMappedDesc = []
gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
gameTabFunc.gameDisplay(gamesList, filter)

# Temporary colour scheme variables to prevent hardcoding problems, and maybe implement a way to mod the UI layout
ui_AC1= "#222222"
ui_AC2 = "#333333"
ui_AC3 = "#444444"
ui_AC4 = "#555555"
ui_Txt = "#CDCDCD"
ui_AH1 = "#B83301"
ui_AH3 = "#660000"
ui_AH2 = "#FE5312"
ui_AE = "#CC3300"
ui_Font = "Archivo Black"
ui_Bold = "bold"

testingTurquoise = "#00FFD5"

# Tracks which menu section is active
menuAct = "Game"

# Resolution definitions
MaxRes = pyautogui.size()
Defined_Res = {
    "1280x720": [1280, 720],
    "1366x768": [1366,768],
    "1440x810": [1440,810],
    "1920x1080": [1920,1080],
}

# Gesture Controls definitions
gControls = {
    "Mouse" : run.program1,
    "Two Handed" : run.program2,
    "Swipe" : run.program3,
    "Hybrid 1" : run.program4,
    "Hybrid 2" : run.program5,
    "Steering 1" : run.program6,
    "Steering 2" : run.program7,
    "Again 2" : run.program8,
}

# Hand Controls definitions
hControls = {
    "Left": "left:",
    "Right": "right:"
}

# Initial list for listing keybinds, will be filled with loadKeys
initBinds = {}

# Initialises the tkinter root window with 1280 x 720 as the default
root = tk.Tk()
root.title(f"Handflux - GUI Prototype {versionNum}")
root.geometry(f"{Defined_Res['1280x720'][0]}x{Defined_Res['1280x720'][1]}")
root.maxsize(MaxRes[0],MaxRes[1])
root.minsize(1280,720)
root.configure(background=ui_AC1)
generalUI.centerWindow(root)
root.bind("<Key>", quit.exit_viaKey)

# Configure the GUI layout
uiMasterFrame = tk.Frame(root, padx=5, pady=5, bg=ui_AC1)
uiDynamFrame = tk.Frame(root, padx=5, pady=5, bg=ui_AC1)

# Tabs for the UI Frame, opens up game menu as the default
uiDynamTabs = {
    "Game": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=ui_AC1),
    "Binds": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=ui_AC1)
}
gameTabFunc.run_gameMenu()

# Game Tab - Opens up a specific game & displays its desc. Has a button that transfers to profile
menuGameTabBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC1)
menuGameTab = tk.Button(menuGameTabBorder, text="GAMES", command=gameTabFunc.run_gameMenu, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
gameMasterFrame = tk.Frame(uiDynamTabs["Game"], background=ui_AC1)
gamesDisplay = tk.Canvas(uiDynamTabs["Game"], background=ui_AC1, highlightthickness=0, width=MaxRes[0], height=MaxRes[1])
gameDisplay = tk.Canvas(uiDynamTabs["Game"], background=ui_AC1, highlightthickness=0)

gamesDFrame = tk.Frame(gamesDisplay, padx=15, pady=15, bg=ui_AC2)

# Initialises the game tab
gameTabFunc(gamesDFrame)

game_SearchBorder = tk.Frame(gameMasterFrame, background=ui_AH1)
game_ResetBorder = tk.Frame(gameMasterFrame, background=ui_AH1)
gameLabel = tk.Label(gameMasterFrame, text="GAMES & APPS", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
gameSearchBar = tk.Entry(gameMasterFrame, bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 10))
gameSearchButton= tk.Button(game_SearchBorder, text="Search", command=gameTabFunc.filterGame, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))
gameResetSearch= tk.Button(game_ResetBorder, text="Reset Search", command=gameTabFunc.resetFilter, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))

gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
gameLabel.pack(padx=5, pady=15, side="left")
game_SearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
game_ResetBorder.pack(padx=5, pady=15, side="right", anchor="ne")

gameResetSearch.pack(padx=2, pady=2, side="right")
gameSearchButton.pack(padx=2,pady=2, anchor="center")
gameSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")
gamesDisplay.pack(padx=10, pady=1, side="left", fill="both")

gamesDisplay.create_window((0, 0), window=gamesDFrame)
gamesDisplay.bind("<Configure>", gameTabFunc.gamesDConfig)
gamesDisplay.bind_all("<MouseWheel>", gameTabFunc.gamesDScroll)

generalUI.button_hover(gameSearchButton,ui_AH1, ui_AC2)
generalUI.button_hover(gameResetSearch,ui_AH1, ui_AC2)

# Keybinds Tab - Displays the assigned keys for the 
menuBindsTabBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC1)
menuBindsTab = tk.Button(menuBindsTabBorder, text="KEYBINDS", command=bindsTabFunc.run_bindsMenu, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
bindFrame = {}
keyFrame = {}
imgFrame = {}
bindLabel = {}
bindAction = {}
bindChange = {}

bindsMasterFrame = tk.Frame(uiDynamTabs["Binds"], background=ui_AC1)
bindsLabel = tk.Label(bindsMasterFrame, text="KEYBINDS", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
saveBinds = tk.Button(bindsMasterFrame, text="Save Keybinds", command=bindsTabFunc.saveKeys, width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
resetBinds = tk.Button(bindsMasterFrame, text="Reset Previous", command=bindsTabFunc.loadKeys, width=15, height=2, bg=ui_AH1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

generalUI.button_hover(saveBinds,ui_AH1, ui_AC2)   
generalUI.button_hover(resetBinds,ui_AE, ui_AH1)

# GUI Labels
TKlabel = tk.Label(uiMasterFrame, text=f"PROTOTYPE {versionNum}", anchor="ne", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))

# Settings Tab - Displays the settings for the app.

settingsBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC1)
settings_button = tk.Button(settingsBorder, text="SETTINGS", command=settingsFunc.display_Settings, width=10, height=2, bg=ui_AC1, fg=ui_Txt,activebackground=ui_AH1, border=0, font=(ui_Font, 10))

# Exit button
exit_button = tk.Button(uiMasterFrame, text="QUIT", command=quit.exit_program, width=10, height=2, bg=ui_AC1, fg=ui_Txt,activebackground=ui_AH1, border=0, font=(ui_Font, 10))

# GUI Layout and Labels
uiMasterFrame.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")

# Menu Tabs Layout
menuGameTabBorder.pack(side="left", anchor="w")
menuGameTab.pack(padx=2, pady=2, side="left", anchor="w")
generalUI.button_hover(menuGameTab, ui_AH1, ui_AC1)

menuBindsTabBorder.pack(side="left", anchor="w")
menuBindsTab.pack(padx=2, pady=2, side="left", anchor="w")
generalUI.button_hover(menuBindsTab, ui_AH1, ui_AC1)

settingsBorder.pack(side="left", anchor="w")
settings_button.pack(padx=2, pady=2, side="left", anchor="nw")
generalUI.button_hover(settings_button, ui_AH1, ui_AC1)

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(exit_button, ui_AE, ui_AC1)

uiDynamFrame.pack(side="top", fill="x")

# Global Canvases
quitCan = tk.Canvas(root, width=1200, height=600, bg=ui_AC2, highlightthickness=0)
tutCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC2, highlightthickness=0)
faqCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC3, highlightthickness=0)
gearCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC3, highlightthickness=0)
bindsCanvas= tk.Canvas(uiDynamTabs["Binds"], width=MaxRes[0], height=MaxRes[1], background=ui_AC1, highlightthickness=0)

# Run the tkinter event loop
root.mainloop()