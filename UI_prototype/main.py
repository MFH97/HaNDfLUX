# Main program for GUI interface
import subprocess, os, psutil, tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog

# Additonal imports
import pyautogui, re
import time, threading
from pynput.mouse import Controller
from PIL import Image, ImageTk
from pygrabber.dshow_graph import FilterGraph

# Class for General UI Functions
class generalUI:
    # Changes the colour of the mapped button when the mouse hovers over it
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
    
    # Gets the styling for the UI
    def getStyling():
        global ui_AC1, ui_AC2, ui_AC3, ui_AC4, ui_AE, ui_AH1, ui_AH2, ui_AH3, ui_AC1, ui_Bold, ui_Font, ui_AC1, ui_Txt, configRef
        try:
            # Clears the previous items in the list
            colourPalette = []
            
            # Adds new items to the list
            if os.path.isfile(configRef):
                with open(configRef, "r") as cScheme:
                    for colours in cScheme:
                        if "ui_" in colours:
                            Arm = colours.split("Ã· ")
                            colourPalette.append(Arm[1].replace("\n",""))
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False

            # Assigns the values to their respective elements
            ui_AC1 = colourPalette[0]
            ui_AC2 = colourPalette[1]
            ui_AC3 = colourPalette[2]
            ui_AC4 = colourPalette[3]

            ui_AE = colourPalette[4]

            ui_AH1 = colourPalette[5]
            ui_AH2 = colourPalette[6]
            ui_AH3 = colourPalette[7]

            ui_Bold = colourPalette[8]
            ui_Font = colourPalette[9]
            ui_Txt = colourPalette[10]
            cScheme.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to map the styling to the respective UI Elements: {e}")
        
    # Gets the config for the automatiic tutorial startup
    def startTutorial():
        global tutStartUp, configRef
        try:
            if os.path.isfile(configRef):
                with open(configRef, "r") as config:
                    for items in config:
                        if "startupTut Ã·" in items:
                            tutConfig = items.split("Ã· ")
                            tutStartUp = tutConfig[1].replace("\n","")
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False

            if tutStartUp == "Enabled":
                run.tutorial()
            else:
                pass

            config.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the tutorial UI: {e}")

    # Gets the available cameras for using again2
    def getCameras(camList):
        global cam
        try:
            # Clear the old list
            graph = FilterGraph()
            cams = graph.get_input_devices()
            
            if cams:
                for cam, device in enumerate(cams):
                    camList[cam] = device
            else:
                messagebox.showerror("Error", "No cameras detected! Hanflux REQUIRES a camera to function!")
        
            return camList

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get the available cameras: {e}")

    # Gets the gesture profiles
    def loadProfiles(profileControls):
        global configRef
        try:
            # Clears the old list
            profileControls.clear()

            # Adds in the new list
            if os.path.isfile(configRef):
                with open(configRef, "r") as config:
                    for items in config:
                        if "profileMap Ã·" in items:
                            profileItems = items.split("Ã· ")
                            profileItems = profileItems[1].split(" â”¼ ")
                            profileItems[-1] = profileItems[-1].replace("\n","")
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False
            
            for item in range(len(profileItems)):
                profileControls[profileItems[item].capitalize()] = profileItems[item]
            
            config.close()
            return profileControls

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the gesture profiles: {e}")

    # Adds a gesture profile for the created game
    def addProfile(profileControl):
        global pControls, configRef
        try:
            pControls.update({profileControl.capitalize(): profileControl})

            addition = " â”¼ ".join(f"{profileItems}" for profileKey, profileItems in pControls.items())

            backupRef = f"{base_path}\\resources\\gkm_backup.txt"
            profileRef = f"{base_path}\\resources\\profiles\\{profileControl}.txt"

            if os.path.isfile(configRef):
                with open(configRef, "r") as config:
                    addRef = config.readlines()

                with open(configRef, 'w') as add:
                    for items in addRef:
                        if "profileMap Ã·" in items:
                            add.write(f"profileMap Ã· {addition}\n")
                        else:
                            add.write(items)
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False
            
            if os.path.isfile(backupRef):
                with open(backupRef, 'r') as addReference:
                    newKeys = addReference.readlines()
            else:
                messagebox.showerror("Error", "The backup mapping cannot be found!")
                return False

            with open(profileRef, 'w') as appendKeys:
                appendKeys.writelines(newKeys)
        
            config.close(), add.close(), addReference.close(), appendKeys.close()
            bindsTabFunc.refreshList(pControls)
            return pControls

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add the profile: {e}")

    # Edits the gesture profile name after editing the game's name
    def editProfile(profileControl, newProfile):
        global pControls, configRef
        try:
            # Changes the profile's name
            pControls.update({profileControl.capitalize():newProfile})
            #pControls[profileControl.capitalize()] = newProfile
            append = " â”¼ ".join(f"{profileItems}" for profileKey, profileItems in pControls.items())
            
            # Consolidates that change in config.ini
            oldRef = f"{base_path}\\resources\\profiles\\{profileControl}.txt"
            newRef = f"{base_path}\\resources\\profiles\\{newProfile}.txt"

            if os.path.isfile(configRef):
                with open(configRef, "r") as config:
                    editRef = config.readlines()

                with open(configRef, 'w') as add:
                    for items in editRef:
                        if "profileMap Ã·" in items:
                            add.write(f"profileMap Ã· {append}\n")
                        else:
                            add.write(items)
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False

            # Renames the text file for that gesture profile
            if os.path.isfile(oldRef):
                os.rename(oldRef, newRef)
            else:
                messagebox.showerror("Error", "The original profile control cannot be found!")
                return False
            
            config.close(), add.close()
            bindsTabFunc.refreshList(pControls)
            return pControls

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add the profile: {e}")
     
    # Removes the selected gesture profile
    def deleteProfile(profileControl):
        global pControls, configRef
        try:
            
            # Removes that particular item
            del pControls[profileControl.capitalize()]

            remainder = " â”¼ ".join(f"{profileItems}" for profileKey, profileItems in pControls.items())
            
            with open(configRef, "r") as config:
                configGet = config.readlines()

            with open(configRef, 'w') as delete:
                for items in configGet:
                    if "profileMap Ã·" in items:
                        delete.write(f"profileMap Ã· {remainder}\n")
                    else:
                        delete.write(items)

            os.remove(f"{base_path}\\resources\\profiles\\{profileControl}.txt")
            bindsTabFunc.refreshList(pControls)
            return pControls

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete the profile: {e}")

    # Loads the game gesture profile
    def loadGameProfile(profileControl):
        global tutStartUp
        try:
            fileRef = f"{base_path}\\resources\\profiles\\{profileControl}.txt"
            defaultRef = f"{base_path}\\resources\\profiles\\default.txt"
            gkmRef = f"{base_path}\\resources\\gesture_key_mapping.txt"
            
            # Checks if the game gesture profile exists, and uses the default if it does not exist.
            if os.path.exists(fileRef):
                with open(fileRef, 'r') as openRef:
                    controls = openRef.readlines()
            elif os.path.isfile(defaultRef):
                with open(defaultRef, "r") as openRef:
                    controls = openRef.readlines()
            else:
                messagebox.showerror("Error", "Profile Controls and Default Controls cannot be found!")
                return False
            
            if os.path.isfile(gkmRef):
                with open(gkmRef, 'w') as openControls:
                    openControls.writelines(controls)
            else:
                messagebox.showerror("Error", "gesture_key_mapping.txt cannot be found!")
                return False
        
            openRef.close()
            openControls.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the game profile: {e}")

# Class for Game Tab Functions
class gameTabFunc:
    # Maps the gamesDisplay frame for usage, and changes the highlighted border to Games
    def __init__(self, gFrame):
        global gameListRef
        try:  
            self.gFrame = gFrame
            if os.path.isfile(gameListRef):
                gamesList = open(gameListRef, "r")
            else:
                messagebox.showerror("Error", "The games list cannot be found!")
                return False
            
            gameTabFunc.gameDisplay(gamesList, filter)
            gameTabFunc.id_Game(gFrame)

            for uiBorder in uiMasterFrame.winfo_children():
                uiBorder.config(bg=ui_AC1)
                menuGameTabBorder.config(bg=ui_AH1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display games: {e}")
    
    # Scroll Functions for the Games Tab
    def gamesDConfig(e):
        global onceSet_Game
        gamesDisplay.configure(scrollregion=gamesDisplay.bbox("all"))

        if not onceSet_Game:
            gamesDisplay.xview_moveto(0)
            onceSet_Game = True

    def gamesDScroll(e):
        gamesDisplay.xview_scroll(-1 * (e.delta // 100), "units")

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
                gameBorder = tk.Frame(gameFrame, bg=ui_AC4)
                gameItem = tk.Text(gameFrame, bg=ui_AC4, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(ui_Font, 10))
                gameItem.insert(tk.END, gameDisplayArray[gItem])
                gameItem.configure(exportselection=0, state="disabled")

                # Checks if the image file exists
                if os.path.isfile(thumbDisplayArray[gItem]):
                    giIMG = Image.open(thumbDisplayArray[gItem])  
                    giForm = giIMG.resize((220, 300))
                    gameImg = ImageTk.PhotoImage(giForm)
                    thumbDisplayArray[gItem] = gameImg
                    gameButton = tk.Button(gameBorder, image=gameImg, command=lambda gIter=gItem: gameTabFunc.game_Describe(gameDisplayArray[gIter]),
                                           bg=ui_AC1, fg=ui_Txt, border=0)
                else:
                    # Loads the placeholder image instead
                    giIMG = Image.open(placeThumb)  
                    giForm = giIMG.resize((220, 300))
                    gameImg = ImageTk.PhotoImage(giForm)
                    thumbDisplayArray[gItem] = gameImg
                    gameButton = tk.Button(gameBorder, image=gameImg, command=lambda gIter=gItem: gameTabFunc.game_Describe(gameDisplayArray[gIter]),
                                           bg=ui_AC1, fg=ui_Txt, border=0)

                gameFrame.pack(padx=25, pady=25, side="left", anchor="w")
                gameBorder.pack()
                gameButton.pack(padx=10,pady=10)
                gameItem.pack()

                generalUI.button_hover(gameBorder, ui_AH1, ui_AC4)
            
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
        global gamesList, gamesDisplay, gamesDFrame, gameListRef
        try:
            filter = gameSearchBar.get()
            if filter !="":
                if os.path.isfile(gameListRef):
                    gamesList = open(gameListRef, "r")
                else:
                    messagebox.showerror("Error", "The games list cannot be found!")
                    return False
                
                gameTabFunc.gameDisplay(gamesList, filter)
                gameTabFunc.id_Game(gamesDFrame)
                gameSearchBar.delete(0, "end")
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
    
    # Resets the filters in filterGame
    def resetFilter():
        global gamesList, gamesDisplay, gamesDFrame, gameListRef
        try:
            filter = ""
            if os.path.isfile(gameListRef):
                gamesList = open(gameListRef, "r")
            else:
                messagebox.showerror("Error", "The games listcannot be found!")
                return False
            
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
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",
                                                          filetypes = [('Executables', '*.exe')])

                if filepath_New:
                    # Changes the filepath in the game description
                    exePath = filepath_New
                    addGameFP.configure(text = filepath_New)
                else:
                    pass
            except Exception as e:
                messagebox.showerror("Error", f"Failed to modify EXE filepath: {e}")
        
        # Writes the image's filepath to gameItemImg
        def writeIMG():
            global imgPath
            try:
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",
                                                          filetypes=[('Image files', '*.png *.jpg *.jpeg')])
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
            global imgPath, exePath, gameListRef
            try:
                # Retrieves the data entered
                gameN = addGameLabel.get("1.0","end-1c")
                gameD = addGameTXT.get("1.0","end-1c")

                gameN = re.sub(r'[]\\\/:*?÷"<>|[]' , "" ,  gameN)

                # Checks the fields from the entered data
                if imgPath == "" or imgPath == f"{base_path}\\img\\gameimg\\PlaceHolder.png":
                    imgPath = f"BASE/img/gameimg/Placeholder.png"
                else:
                    pass
                if exePath == "":
                    messagebox.showinfo("Warning","One or more fields are not filled")
                    return False
                if gameN == "Add game name here" or gameN == "":
                    gameName = "SAMPLE GAME"
                else:
                    gameName = gameN.upper()
                if gameD == "Add game description here" or gameD == "":
                    gameDesc = "Sample Desc"
                else:
                    gameDesc = gameD

                # Additional check if the game profile already exists
                gameProfileRef = f"{base_path}\\resources\\profiles\\{gameN.lower()}.txt"
                if os.path.isfile(gameProfileRef):
                    messagebox.showerror("Error", "A game of that name already exists!")
                    return False
                else:
                    if os.path.isfile(gameListRef):
                        addGList = open(gameListRef, "a")
                        addGList.write(f"\n \nGameÃ· {gameName}Ã· {gameName}\n")
                        addGList.write(f"DescÃ· {gameName}Ã· {gameDesc}\n")
                        addGList.write(f"ThumbImgÃ· {gameName}Ã· {imgPath}\n")
                        addGList.write(f"ExeÃ· {gameName}Ã· {exePath}")
                        addGList.close()

                        generalUI.addProfile(gameName.lower())
                        messagebox.showinfo("You have added a Game to the list!","You can now assign controls to the game!")
                        goBack()
                        gameTabFunc(gamesDFrame)
                    else:
                        messagebox.showerror("Error", "The games list cannot be found!")
                        return False

            except NameError:
                messagebox.showwarning("Warning","One or more fields are not filled")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add games to games list: {e}")

        # Clears the text in game name
        def selectName(e):
            if addGameLabel.get("1.0","end-1c") == "Add game name here":
                addGameLabel.delete("1.0","end")

        # Clears the text in game description
        def selectDesc(e):
            if addGameTXT.get("1.0","end-1c") == "Add game description here":
                addGameTXT.delete("1.0","end")

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

            addGameLabel = tk.Text(gameDisplay, width=MaxRes[0], height=2, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0,font=(ui_Font, 15, ui_Bold))
            addGameLabel.insert(tk.END, "Add game name here")

            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1,
                                   font=(ui_Font, 15, ui_Bold))

            placeHolder = base_path + f"\\img\\gameimg\\Placeholder.png"

            if os.path.isfile(placeHolder):
                agiIMG = Image.open(placeHolder)
            else:
                messagebox.showerror("Error", "The placeholder image cannot be found!")
                return False
            
            agiForm = agiIMG.resize((220, 300))
            addGameItemImg = ImageTk.PhotoImage(agiForm)
            addGameImg = tk.Button(game_DisplayPicFrame, image=addGameItemImg, command=writeIMG, bg=ui_AC1, fg=ui_Txt, border=0)
            addGameImg.image = addGameItemImg
            agiLabel = tk.Label(game_TutFrame, text="Click on the white area to add your own image", height=1, bg=ui_AC1, fg=ui_Txt,
                                font=(ui_Font, 12))

            addGameTXT = tk.Text(game_DisplayFrame, width=MaxRes[0], height=5, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            addGameTXT.insert(tk.END, "Add game description here")

            addGameLabel.bind("<Button-1>", selectName)
            addGameTXT.bind("<Button-1>", selectDesc)

            addGameFP = tk.Button(game_InfoFrame, text="Configure Filepath (REQUIRED)", command=writeEXE, bg=ui_AC1, fg=ui_Txt, border=0,
                                  activebackground=ui_AH1, font=(ui_Font, 12))
            addGameButton = tk.Button(game_AddFrame, text="Add Game to Games List", command=addToGL, bg=ui_AC1, fg=ui_Txt, border=0,
                                      activebackground=ui_AH1, font=(ui_Font, 12))

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
            generalUI.button_hover(addGameFP, ui_AH1, ui_AC1)

            agiLabel.pack(padx=4, pady=4, side="top", anchor="nw")

            addGameButton.pack(padx=4, pady=4, side="bottom", anchor="nw")
            generalUI.button_hover(addGameButton, ui_AH1, ui_AC1)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display Game Adder UI: {e}")

    # Displays that specific game 
    def game_Describe(gameItem):
        global gamesDisplay, gameMasterFrame, gameDetails, gameDisplay, gameProcess, gamesList, process, gamesDFrame, gameListRef, textR

        # Goes back to the Games Tab
        def goBack():
            try:
                gameDisplay.pack_forget()
                gameTabFunc(gamesDFrame)
                gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                gamesDisplay.create_window((0, 0), window=gamesDFrame)
                gameGet.close()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to go back to the Games Tab: {e}")

        # Runs the exe described in the filepath
        def runGame():
            # Checks if the game is in the process list
            def gameCheck(proc):
                while True:
                    procs = [proc.name() for proc in psutil.process_iter()]
                    
                    if proc not in procs:
                        #quit.release_control()
                        break
                    time.sleep(1)

            # Opens up an asynchronous thread for the game and gesture control to concurrently run
            def gameStart(proc):
                thread = threading.Thread(target=gameCheck, args=(proc,))
                thread.daemon = True
                thread.start()

            try:
                gameEXE = gameDetails[2]
                gameEXE = gameEXE.split("/")

                if len(gameDetails[2]) == 0 or gameDetails[2] == "Filepath":
                    messagebox.showerror("Error", "Game's EXE filepath is NOT configured")
                else:
                    # Starts up the respective game's control, gesture profile and game
                    os.startfile(gameDetails[2])
                    run.program1()
                    generalUI.loadGameProfile(gameDetails[0].lower())
                    gameStart(gameEXE[-1])
                    

            except Exception as e:
                messagebox.showerror("Error", f"Failed to run the game: {e}")

        # Experimental function to write the filepath for an EXE to the gamesList
        def writeEXE():
            global gameListRef
            try:
                # Formats the filepath to fit the gamesList format
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",
                                                          filetypes = [('Execitables', '*.exe')])
                if filepath_New:

                    filepath_Change = f"ExeÃ· {gameItem}Ã· {filepath_New}"
                    if os.path.isfile(gameListRef):
                        with open(gameListRef, "r") as gameGets:
                            gameWrite = gameGets.readlines()

                        filepath_Update = False
                        with open(gameListRef, "w") as writeList:
                            for line in gameWrite:
                                if not filepath_Update and f"ExeÃ· {gameItem}Ã· " in line:
                                    writeList.write(filepath_Change + "\n")
                                    gameDetails[2] = filepath_New
                                    filepath_Update = True
                                else:
                                    writeList.write(line)
                    else:
                        messagebox.showerror("Error", "The games list cannot be found!")
                        return False

                    # Changes the filepath in the game description
                    gameItemFile.configure(text = filepath_New)
                    gameGets.close(), writeList.close()

                else:
                    messagebox.showinfo("Warning: ", "Select an executable application to change the filepath")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to modify Exe's Filepath: {e}")
        
        # Confirmation dialog to check if the user wants to delete the game
        def confirmDelete():
            try:
                # Clears the dialog and returns to the game
                def undoDelete():
                    dialogFrame.place_forget()

                dialogFrame = tk.Canvas(gameDisplay, background=ui_AC2, highlightthickness=0)
                
                confirmDialog = tk.Label(dialogFrame, text="Do you want to delete this game? This is irreversible!", bg=ui_AC1,
                                         fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                yesButton = tk.Button(dialogFrame, text="Yes", command=deleteGame, bg=ui_AH1, fg=ui_Txt, border=0, width=15, height=3,
                                      activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                noButton = tk.Button(dialogFrame, text="No", command=undoDelete, bg=ui_AC1, fg=ui_Txt, border=0, width=15, height=3,
                                     activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                dialogFrame.place(relx=0, rely=0, relheight=1, relwidth=1)
                confirmDialog.pack(padx=25, pady=25, side="top", fill="x")

                yesButton.pack(padx=10, pady=10)
                generalUI.button_hover(yesButton, ui_AH2, ui_AH1)

                noButton.pack(padx=10, pady=10)
                generalUI.button_hover(noButton, ui_AH1, ui_AC1)

            except Exception as e:
                 messagebox.showerror("Error", f"Failed to load the confirmation dialog {e}")
        
        # Deletes the game from gameslist after confirmation
        def deleteGame():
            global gameListRef
            try:
                delTextR = False
                gameWrite = []
                # Gets the reference for game deletion
                if os.path.isfile(gameListRef):
                    with open(gameListRef, "r") as delRefer:
                        for line in delRefer:
                            if f"GameÃ· {gameItem}Ã·" in line:
                                delTextR = True
                                continue
                            
                            if f"ExeÃ· {gameItem}Ã·" in line:
                                delTextR = False
                                continue
                            
                            if not delTextR:
                                gameWrite.append(line)

                    with open(gameListRef, "w") as deletion:
                        deletion.writelines(gameWrite)
                else:
                    messagebox.showerror("Error", "The games list cannot be found!")
                    return False
                
                delRefer.close(), deletion.close()
                
                # Removes the thumbnail image and goes back to the main menu IF it is not in the base directory
                if baseImg == "BASE":
                    pass
                else:
                    os.remove(gameDetails[1])
                    pass

                generalUI.deleteProfile(gameItem)
                goBack()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete the game in gameslist: {e}")
        
        # Edits the game's name in gameslist after the game's name is changed in gameDisplay
        def renameGame(game):
            global gameListRef
            try:
                # Gets the reference for game rename and formats it
                gui = gameItemLabel.get("1.0","end-1c")
                gui = re.sub(r'[]\\\/:*?÷"<>|[]' , "" , gui.upper())
                print(gui)

                if os.path.exists(f"{base_path}\\resources\\profiles\\{gui.lower()}.txt") or gui in game:
                    messagebox.showerror("Error", "The renamed game already exists!")
                    return False
                else:
                    if os.path.isfile(gameListRef):
                        with open(gameListRef, "r") as renameRef:
                            gameWrite = renameRef.read()

                        editToken = f"GameÃ· {gui}Ã· {gui}\nDescÃ· {gui}Ã· {gameDetails[3]}\nThumbImgÃ· {gui}Ã· {gameDetails[1]}\nExeÃ· {gui}Ã· {gameDetails[2]}"
                        gameEdit = re.sub(rf"(GameÃ·\ {game}Ã·\s*)(.*?)(\s*ExeÃ·\ {game}Ã·)", re.escape(editToken), gameWrite, flags=re.DOTALL)
                        gameEdit = gameEdit.replace("\\n","\n").replace("\\","")

                        with open(gameListRef, "w") as renameSet:
                            renameSet.write(gameEdit)
                    else:
                        messagebox.showerror("Error", "The games list cannot be found!")
                        return False
                    
                    gameItemLabel.delete('1.0', tk.END) 
                    gameItemLabel.insert(tk.END, gui)
                    gameDetails[0] = gui
                    generalUI.editProfile(game.lower(), gui.lower())

                    messagebox.showinfo("Success!", f"The game is now renamed to {gui}")
                    renameRef.close(), renameSet.close()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit the game's name: {e}")

        # Main game display
        try:
            print(gameItem)
            # Hides the game selection tab
            gameMasterFrame.pack_forget()
            gamesDisplay.pack_forget()
            gameDisplay.pack(padx=10, pady=1, side="top", fill="x")

            # Clears the old game details
            for gItem in gameDisplay.winfo_children():
                gItem.destroy()
                gameDetails.clear()
            baseImg = ""
            textR = False
            textDesc = []

            # Gets the new game details
            if os.path.isfile(gameListRef):
                with open(gameListRef, "r") as gameGet:
                    for line in gameGet:
                        if f"GameÃ· {gameItem}" in line:
                            gameName = line.split("Ã· ")
                            gameDetails.append(gameName[2].replace("\n",""))
                    
                        if f"ThumbImgÃ· {gameItem}" in line:
                            gameThumb = line.split("Ã· ")
                            baseCheck = gameThumb[2].startswith("BASE")
                            if baseCheck:
                                txt = gameThumb[2].replace("\n","")
                                txt2 = txt.replace("BASE","")
                                file = base_path.replace("\\","/") + txt2
                                baseImg = "BASE"
                            else:
                                file = gameThumb[2].replace("\n","")
                            gameDetails.append(file)
                        
                        if f"ExeÃ· {gameItem}" in line:
                            gameExe = line.split("Ã· ")
                            file = gameExe[2].replace("\n","")
                            gameDetails.append(file)
                
                with open(gameListRef, "r") as gameDescGet:
                    for line in gameDescGet:
                        if f"DescÃ· {gameItem}" in line:
                            textR = True
                            baseLine = line.split("Ã· ")
                            baseDesc = baseLine[2].replace(f"\n" , "")
                            textDesc.append(baseDesc)
                            continue

                        if f"ThumbImgÃ·" in line:
                            textR = False
                            continue

                        if textR:
                            textDesc.append(line.strip())
                
                textExt = "\n".join(textDesc)
                gameDetails.append(textExt.replace(f"DescÃ· {gameItem}Ã· " , ""))

                gameGet.close(), gameDescGet.close()

            else:
                messagebox.showerror("Error", "The games list cannot be found!")
                return False

            # Displays the selected game and its details
            game_DisplayFrame = tk.Frame(gameDisplay, bg=ui_AC2)
            game_DisplayPicFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_InfoFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_RunFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)

            gameItemLabel = tk.Text(gameDisplay, width=MaxRes[0], height=2, wrap="word", bg=ui_AC3, fg=ui_Txt, border=0,
                                    font=(ui_Font, 15, ui_Bold))
            gameItemLabel.insert(tk.END, gameDetails[0])

            gameRename = tk.Button(gameDisplay, text="Rename Game", command=lambda gameN=gameDetails[0]: renameGame(gameN), bg=ui_AC1,
                                   fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            gameDelete = tk.Button(gameDisplay, text=f"DELETE GAME", command= confirmDelete, bg=ui_AH1, fg=ui_Txt, border=0,
                                   activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1,
                                   font=(ui_Font, 15, ui_Bold))
            
            placeHolder = base_path + f"\\img\\gameimg\\Placeholder.png"
            if os.path.isfile(gameDetails[1]):
                giIMG = Image.open(gameDetails[1])  
                giFormat = giIMG.resize((220, 300))
                gameItemImg = ImageTk.PhotoImage(giFormat)
                gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
                gameImg.image = gameItemImg
            else:
                if os.path.isfile(placeHolder):
                    giIMG = Image.open(placeHolder)
                else:
                    messagebox.showerror("Error", "The placeholder image cannot be found!")
                    return False
                
                giFormat = giIMG.resize((220, 300))
                gameItemImg = ImageTk.PhotoImage(giFormat)
                gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
                gameImg.image = gameItemImg

            gameItemTxt = tk.Text(game_DisplayFrame, width=MaxRes[0], height=5, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0,
                                  font=(ui_Font, 12))
            gameItemTxt.insert(tk.END, gameDetails[3])
            gameItemTxt.configure(exportselection=0, state="disabled")  

            gameItemFileP = tk.Button(game_InfoFrame, text="Configure Filepath", command=writeEXE, bg=ui_AC1, fg=ui_Txt, border=0,
                                      activebackground=ui_AH1, font=(ui_Font, 12))
            gameItemFile = tk.Label(game_InfoFrame, text=gameDetails[2], wraplength=MaxRes[0], height=1, justify="left", bg=ui_AC1,
                                    fg=ui_Txt, font=(ui_Font, 12))
            
            gameItemExe = tk.Button(game_RunFrame, text=f"Start Game with Gesture Controls", command=runGame, bg=ui_AC1, fg=ui_Txt,
                                    border=0, height=3, activebackground=ui_AH1, font=(ui_Font, 12))
            gameRelease = tk.Button(game_RunFrame, text=f"Release Gesture Control", command=quit.release_control, bg=ui_AC1, fg=ui_Txt,
                                    border=0, activebackground=ui_AH1, font=(ui_Font, 12))

            game_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            game_RunFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            gameItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="w")
            
            gameDelete.pack(padx=4, pady=4, side="right")
            gameRename.pack(padx=4, pady=4, side="right")

            gameImg.pack(padx=4, pady=4, side="left", anchor="nw")
            gameItemTxt.pack(padx=4, pady=4, side="left", anchor="nw")

            gameItemFileP.pack(padx=4, pady=4, side="left", anchor="nw")
            gameItemFile.pack(padx=4, pady=4, side="left", anchor="nw")

            gameRelease.pack(padx=8, pady=8, side="bottom", anchor="nw")
            gameItemExe.pack(padx=8, pady=8, side="bottom", anchor="nw")

            generalUI.button_hover(backButton, ui_AH1, ui_AC1)
            generalUI.button_hover(gameDelete, ui_AH2, ui_AH1)
            generalUI.button_hover(gameRename, ui_AH1, ui_AC1)
            generalUI.button_hover(gameItemFileP, ui_AH1, ui_AC1)
            generalUI.button_hover(gameRelease, ui_AH1, ui_AC1)
            generalUI.button_hover(gameItemExe, ui_AH1, ui_AC1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the individual game: {e}")

# Class for Keybinds Tab Functions 
class bindsTabFunc:  
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

    # Scroll functions for the Keybinds Tab
    def bindCanvasConfig(e):
        bindsCanvas.configure(scrollregion=bindsCanvas.bbox("all"))

    def bindCanvasScroll(e):
        global onceSet_Binds
        bindsCanvas.yview_scroll(-1 * (e.delta // 100), "units")
        if not onceSet_Binds:
            bindsCanvas.yview_moveto(0)
            onceSet_Binds = True

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
                bindsMasterFrame.pack(padx=5, pady=15, side="top", fill="both")
                bindsCanvas.pack(padx=10, pady=1, side="left", fill="both")

                bindsLabel.pack(padx=10, pady=15, side="left", anchor="nw")
                saveBinds.pack(padx=10, pady=10, side="left", anchor="nw")
                resetBinds.pack(padx=10, pady=10, side="left", anchor="nw")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Keybinds Tab: {e}")
        
    # Updates the assigned key to the pressed key
    def updateKeys(gRef, gesture):
        try:
            # Checks what input has been pressed and maps it
            def keyPress(newKeybind):
                try:
                    # If a mouse click is the new bind, sets it as the new keybind
                    if newKeybind.num != "??":
                        newKey = newKeybind.num
                        if newKey == 1:
                            newClick = "left_click"
                        elif newKey == 2:
                            newClick = "middle_click"
                        elif newKey == 3:
                            newClick = "right_click"
                        else:
                            messagebox.showerror("Error","Unknown input!")
                        
                        initBinds[gesture] = newClick
                        bindLabel[gesture].config(text=f"Key*: {newClick}")
                        messagebox.showinfo("Keybind Updated", f"{gesture} is now bound to {newClick}")
                    # Or if a keypress is the new bind, sets that as the new keybind instead
                    elif newKeybind.keysym:
                        newKey = newKeybind.keysym.lower()
                        initBinds[gesture] = newKey
                        bindLabel[gesture].config(text=f"Key*: {newKey}")
                        messagebox.showinfo("Keybind Updated", f"{gesture} is now bound to {newKey}")               
                    else:
                        messagebox.showerror("Error", "Unknown input!")
                    
                    # Removes the input detection and input detection dialog
                    root.unbind("<KeyPress>")
                    root.unbind("<Button>")
                    dialogFrame.place_forget()

                except Exception as e:
                     messagebox.showerror("Error", f"Failed to detect the input: {e}")

            # Gets the dropdown list option for mapping the new input
            gMapper = controlType[gRef].get()

            # If option is Mouse Movement, sets keybind to mouse_movement
            if gMapper == controlsList[0]:
                initBinds[gesture] = "mouse_movement"
                bindLabel[gesture].config(text="Key*: mouse_movement")
                messagebox.showinfo("Keybind Updated", f"{gRef} is now bound to Mouse Movement")
            
            # If option is Detect Input, displays a dialog showing that inputs are being detected
            elif gMapper == controlsList[1]:
                dialogFrame = tk.Canvas(bindsCanvas, background=ui_AC2, highlightthickness=0)
                bindDialog = tk.Label(dialogFrame, text="Press a keyboard button or Click with your mouse", bg=ui_AC1, fg=ui_Txt,
                                      border=0, font=(ui_Font, 20, ui_Bold))

                dialogFrame.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                bindDialog.pack(padx=25, pady=25, fill="x")

                root.bind("<KeyPress>", keyPress)
                root.bind("<Button>", keyPress)
            else:
                messagebox.showerror("Error", f"Somehow this error was triggered")
 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update the keybind: {e}")

    # Saves the keybinds to the active gesture profile
    def saveKeys():
        global handOption
        try:
            # Checks which profile is to be changed
            activeProfile = profileOption.get()
            activePR = pControls[activeProfile]

            # Reset the changes
            changeArray = []
            rightStart = 12

            # Consolidates the changes
            for gesture, key in initBinds.items():
                newBind = f"{gesture}={key}\n"
                changeArray.append(newBind)

            profileRef = f"{base_path}\\resources\\profiles\\{activePR}.txt"
            if os.path.isfile(profileRef):
                with open(profileRef, 'r') as baseLine:
                    changeLines = baseLine.readlines()
                
                if handOption.get() == "Left":
                    for change in range(len(changeLines[0:11])):
                        changeLines[change] = changeArray[change]
                elif handOption.get() == "Right":
                    for change in range(len(changeLines[12:])):
                        changeLines[rightStart] = changeArray[rightStart]
                        rightStart += 1
                
                with open(profileRef, 'w') as newBinds:
                    newBinds.writelines(changeLines)

            else:
                messagebox.showerror("Error", "The gesture profile cannot be found!")
                return False
            
            messagebox.showinfo("Keybinds Saved", "Keybinds are saved!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save keybinds: {e}")

    # Loads the keybinds from the geasture profile dropdown list
    def loadKeys():
        global bindChange, handOption
        try:
            # Switches the hands
            def switchThing(*args):
                activeHand = handOption.get()
                activeProfile = profileOption.get()
                activeHV = hControls[activeHand]
                activePR = pControls[activeProfile]
                generateKey(activeHV, activePR)
            
            # Main function for generating the keybinds
            def generateKey(e, f):
                try:
                    # Clears the old selections
                    gNumber = 0
                    for bindings in bindMaster.winfo_children():
                        bindings.pack_forget()

                    # Add a dropdown list displaying 3 options - mouse_movement, open_keyboard and detect input
                    activeRef = f"{base_path}\\resources\\profiles\\{f}.txt"
                    if os.path.isfile(activeRef):
                        with open(activeRef, "r") as line:
                            for binds in line:
                                # Splits gestures and keybinds
                                gesture, key = binds.strip().split("=")

                                # Filters out the respective hand gestures and displays them
                                if e in binds:
                                    initBinds[gesture] = key
                                    bindFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)
                                    keyFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)
                                    imgFrame[gNumber] = tk.Frame(bindMaster, padx=5, pady=5, bg=ui_AC2)

                                    gestureFormat = gesture.split(":")
                                    bindAction = tk.Label(bindFrame[gNumber],text=f"{gestureFormat[0].capitalize()} Hand: {gestureFormat[1].capitalize()}",
                                                          bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

                                    # Checks if the image file exists
                                    imgS = base_path + f"\\img\\gestureimg\\{gestureFormat[1]}.png"
                                    placeHolder = base_path + f"\\img\\gestureimg\\placeholder.png"
                                    if os.path.isfile(imgS):
                                        gtIMG = Image.open(imgS)  
                                        gtForm = gtIMG.resize((150, 150))
                                        gestThumb = ImageTk.PhotoImage(gtForm)
                                        gestImg = tk.Label(keyFrame[gNumber], image=gestThumb, bg=ui_AC1, fg=ui_Txt, border=0)
                                        gestImg.image = gestThumb
                                    else:
                                        if os.path.isfile(placeHolder):
                                            gtIMG = Image.open(placeHolder)
                                        else:
                                            messagebox.showerror("Error", "The placeholder image cannot be found!")
                                            return False
                                        gtForm = gtIMG.resize((150, 150))
                                        gestThumb = ImageTk.PhotoImage(gtForm)
                                        gestImg = tk.Label(keyFrame[gNumber], image=gestThumb, bg=ui_AC1, fg=ui_Txt, border=0)
                                        gestImg.image = gestThumb

                                    bindLabel[gesture] = tk.Label(keyFrame[gNumber], text=f"Key: {key}",bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))

                                    controlType[gNumber] = tk.StringVar(root)
                                    controlType[gNumber].set(controlsList[1])
                                    bindCType[gNumber] = tk.OptionMenu(keyFrame[gNumber], controlType[gNumber], *controlsList)
                                    bindCType[gNumber].configure(bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, highlightbackground=ui_AC1,
                                                                 font=(ui_Font, 12))
                                    bindChange[gNumber] = tk.Button(keyFrame[gNumber], text="Change", command=lambda gRef=gNumber,
                                                                    gNum= gesture:bindsTabFunc.updateKeys(gRef, gNum), bg=ui_AC1, fg=ui_Txt,
                                                                    activebackground=ui_AH1, border=0, font=(ui_Font, 15, ui_Bold))

                                    bindFrame[gNumber].pack(padx=20, pady=5, anchor="nw", fill="x")
                                    keyFrame[gNumber].pack(padx=20, pady=5, anchor="nw", fill="x")
                                    imgFrame[gNumber].pack(padx=20, pady=5, anchor="nw", fill="x")
                                    
                                    bindAction.pack(padx=5, side="left")
                                    gestImg.pack(padx=5, pady=5, side="left", anchor="nw")
                                    bindLabel[gesture].pack(padx=5, side="left")

                                    bindChange[gNumber].pack(padx=5, side="right", anchor="e")
                                    bindCType[gNumber].pack(padx=5, side="right", anchor="e")

                                    generalUI.button_hover(bindChange[gNumber], ui_AH1, ui_AC1)
                                    gNumber += 1
                    else:
                        messagebox.showerror("Error", "The gesture profile cannot be found!")
                        return False

                    bindMaster.bind("<Configure>", bindsTabFunc.bindCanvasConfig)
                    bindsCanvas.bind_all("<MouseWheel>", bindsTabFunc.bindCanvasScroll)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate the keybinds: {e}")

            # Shows the keybinds menu
            bindsCanvas.create_window((0, 0), window=bindMaster)

            handOption.trace_add("write", switchThing)
            profileOption.trace_add("write", switchThing)
            
            switchThing(hControls["Left"], pControls["Default"])

        except FileNotFoundError:
            # If the keybinds text file cannot be found
            messagebox.showerror("Error", "No keybinds found")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the keybind menu: {e}")

    # Resets the keybinds to the default mappings for the active gesture profile
    def resetKeys():
        try:
            activeProfile = profileOption.get()
            activePR = pControls[activeProfile]
            gkmRef = f"{base_path}\\resources\\gkm_backup.txt"
            profileRef = f"{base_path}\\resources\\profiles\\{activePR}.txt"

            if os.path.isfile(gkmRef):
                with open(gkmRef, 'r') as referReset:
                    resetBase = referReset.readlines()
            else:
                messagebox.showerror("Error", "The backup gesture reference cannot be found!")
                return False

            if os.path.isfile(profileRef):
                with open(profileRef, 'w') as resetActual:
                    resetActual.writelines(resetBase)
            else:
                messagebox.showerror("Error", "The gesture profile cannot be found!")
                return False
            
            referReset.close(), resetActual.close()
            bindsTabFunc.loadKeys()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset the keys: {e}")

    # Refreshes the gesture profile dropdown list
    def refreshList(pControlList):
        global pControls, profileDrop
        try:
            profileOption.set(next(iter(pControls)))
            profileDrop["menu"].delete(0, "end")
            for items in pControls:
                profileDrop["menu"].add_command(label=items, command=tk._setit(profileOption, items))
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh the dropdown list: {e}")

# Class for settings page functions
class settingsFunc:
    # Checks if Escape key is pressed
    def settingKey(key):
        if key.keysym == "Escape":
            settingsFunc.setClose()
    
    # Closes the settings
    def setClose():
        global gearAct
        gearCanvas.place_forget()
        gearAct = False
        if menuAct == "Keybind":
            bindsCanvas.bind("<Configure>", bindsTabFunc.bindCanvasConfig)
            bindsCanvas.bind_all("<MouseWheel>", bindsTabFunc.bindCanvasScroll)
            root.bind("<Key>", quit.exit_viaKey)
        else:
            gamesDisplay.bind("<Configure>", gameTabFunc.gamesDConfig)
            gamesDisplay.bind_all("<MouseWheel>", gameTabFunc.gamesDScroll)
            root.bind("<Key>", quit.exit_viaKey)

    # Scroll functions for the settings
    def canvasConfig(e):
        gearCanvas.configure(scrollregion=gearCanvas.bbox("all"))

    def mouseScroll(e):
        global onceSet_Settings
        gearCanvas.yview_scroll(-1 * (e.delta // 100), "units")

        if not onceSet_Settings:
            gearCanvas.yview_moveto(0.01)
            onceSet_Settings = True
    
    # Toggles the option for tutorial to automatically start up
    def setTutAuto(tutState):
        global tutStartUp, autoTutOpen, configRef
        try:
            if os.path.isfile(configRef):
                with open(configRef, "r") as config:
                    for items in config:
                        if "startupTut" in items:
                            tutConfig = items.split("Ã· ")
                            startConfig = tutConfig[1].replace("\n","")

                # Toggles the state in config.ini
                if startConfig == "Disabled":
                    startConfig = "Enabled"
                else:
                    startConfig = "Disabled"
                
                with open(configRef, "r") as ref:
                    configWrite = ref.readlines()
            
                with open(configRef, "w") as mod:
                    for item in configWrite:
                        if f"startupTut Ã· " in item:
                            mod.write(f"startupTut Ã· {startConfig}\n")
                        else:
                            mod.write(item)
            else:
                messagebox.showerror("Error", "config.ini cannot be found!")
                return False
            
            ref.close(), mod.close(), config.close()
            tutState, tutStartUp = startConfig, startConfig
            return tutState

        except Exception as e:
            messagebox.showerror("Error", f"Failed to toggle the auto startup tutorial: {e}")
    
    # Display the settings
    def display_Settings():
        global gearAct, gearCanvas, onceMade_Settings, gearSettings, tutStartUp, autoTutOpen
        try:
            # Resizes the canvas when the window is resized
            def canvasResize(e):
                if not isinstance(e, int):
                    gearCanvas.itemconfig(gearSettings, width=e.width)        
                else:
                    gearCanvas.itemconfig(gearSettings, width=e)

            # Toggles the windows display mode
            def toggleWindowState(state):
                try:
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
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to toggle the window state: {e}")
            
            # Toggles the button status
            def setAutoButton():
                oldState = ""
                newState= settingsFunc.setTutAuto(oldState)
                autoTutOpen.config(text=f"{newState}")

            # Sets the camera for again2 to use
            def detectCamFunc():
                global camGet
                try:
                    # Sets the changes
                    def setCamFunc(cam, name):
                        global configRef
                        try:
                            # Consolidates the changes
                            if os.path.isfile(configRef):
                                with open(configRef, "r") as configGet:
                                    camWrite = configGet.readlines()

                                with open(configRef, "w") as configWrite:
                                    for line in camWrite:
                                        if f"configCam Ã· " in line:
                                            configWrite.write(f"configCam Ã· {cam}\n")
                                        else:
                                            configWrite.write(line)
                            else:
                                messagebox.showerror("Error", "config.ini cannot be found!")
                                return False
                            
                            configGet.close(), configWrite.close()
                            messagebox.showinfo("", f"Default Camera is now set to {name}")
                
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to modify config.ini: {e}")

                    # Clears the old list
                    for camItems in camDisplayFrame.winfo_children():
                        camItems.destroy()

                    # Gets the new list and displays it on the settings page
                    generalUI.getCameras(camGet)
                    for ind, name in camGet.items():
                        button = tk.Button(camDisplayFrame, text=name, command=lambda camNum = ind, camName = name: setCamFunc(camNum, camName),
                                           width=20, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                        button.pack(padx=5, pady=5, side="left")
                        generalUI.button_hover(button, ui_AH1, ui_AC1)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to display the new cameras: {e}")

            # Gets the sensitivity setting from config.ini
            def senseGet():
                global configRef
                try:
                    if os.path.isfile(configRef):
                        with open(configRef, "r") as configGet:
                            for line in configGet:
                                if f"posDisplace Ã·" in line:
                                    senseInt = line.split("Ã· ")
                                    senseRef = (senseInt[1].replace("\n",""))
                    else:
                        messagebox.showerror("Error", "config.ini cannot be found!")
                        return False
                    
                    sensSlider.set(senseRef)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to get the sensitivity valuesi: {e}")
            
            # Edits the sensitivity setting in config.ini
            def senseEdit():
                global configRef
                try:
                    newVal = sensSlider.get()
                    # Consolidates the changes
                    if os.path.isfile(configRef):
                        with open(configRef, "r") as configGet:
                            camWrite = configGet.readlines()

                        with open(configRef, "w") as configWrite:
                            for line in camWrite:
                                if f"posDisplace Ã· " in line:
                                    configWrite.write(f"posDisplace Ã· {newVal}\n")
                                else:
                                    configWrite.write(line)
                    else:
                        messagebox.showerror("Error", "config.ini cannot be found!")
                        return False
                    
                    messagebox.showinfo("Note", f"Sensitivity has now been set to {newVal}")
                    configGet.close(), configWrite.close()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to modify config.ini: {e}")

            # Checks if the settings are currently active
            if not gearAct:
                # Checks if it's already made
                if not onceMade_Settings:
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                
                    root.bind("<Key>", settingsFunc.settingKey)
                    gearSettings = gearCanvas.create_window((0, 0), window=gearMaster)

                    gearTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC1)
                    gearTitle = tk.Label(gearTF, text="SETTINGS", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))
                    closeGear = tk.Button(gearTF, text="RETURN", command=settingsFunc.setClose, width=10, height=0, bg=ui_AC1, fg=ui_Txt, border=0,
                                          font=(ui_Font, 15, ui_Bold))

                    # Toggles window state
                    winStateTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    winStateFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    winStateLabel = tk.Label(winStateTF, text="DISPLAY", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    winStateDescLabel = tk.Label(winStateTF, text="Modify the display mode of the App", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))
                    
                    fullscreen_button = tk.Button(winStateFrame, text="Fullscreen", command=lambda:toggleWindowState("fullscreen"), width=15, height=2,
                                                  bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    borderless_button = tk.Button(winStateFrame, text="Borderless Windowed", command=lambda:toggleWindowState("borderless"), width=20,
                                                  height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    windowed_button = tk.Button(winStateFrame, text="Windowed", command=lambda:toggleWindowState("windowed"), width=15, height=2,
                                                bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))

                    # For setting the auto-start tutorial feature
                    miscTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    miscFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    miscLabel = tk.Label(miscTF, text="TUTORIAL START-UP", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    miscDescLabel = tk.Label(miscTF, text="Sets whether if you want to have the tutorial shown when you start up the app", bg=ui_AC2,
                                             fg=ui_Txt, border=0, font=(ui_Font, 12))
                    autoTutOpen = tk.Button(miscFrame, text=f"{tutStartUp}", command=setAutoButton, width=12, height=2, bg=ui_AC1, fg=ui_Txt,
                                            activebackground=ui_AH1, border=0, font=(ui_Font, 10))

                    # For setting the camera for again2 to use
                    camTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    camFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    camDisplayFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    camLabel = tk.Label(camTF, text="DEFAULT CAMERA", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    camDescLabel = tk.Label(camTF, text="Set a default camera for the gesture controller to use", bg=ui_AC2, fg=ui_Txt,
                                            border=0, font=(ui_Font, 12))
                    camLister = tk.Button(camFrame, text="Detect Cameras", command=detectCamFunc, width=20, height=2, bg=ui_AC1, fg=ui_Txt,
                                          activebackground=ui_AH1, border=0, font=(ui_Font, 10))

                    # Modifies the sensitivity settings in config.ini
                    sensTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    sensFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    sensLabel = tk.Label(sensTF, text="SENSITIVITY", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    sensDescLabel = tk.Label(sensTF, text="Sets the sensitivity of the mouse movement for the gesture controls", bg=ui_AC2, fg=ui_Txt,
                                             border=0, font=(ui_Font, 12))

                    floatSet = tk.DoubleVar()
                    sensSlider = tk.Scale(sensFrame, bg=ui_AC2, fg=ui_Txt, highlightthickness=0, highlightcolor=ui_AH2, troughcolor=ui_Txt, length=800,
                                          width=30,orient="horizontal", from_=1, to=2, variable=floatSet, resolution=0.02, font=(ui_Font, 12))
                    sensEditor = tk.Button(sensFrame, text="Set Sensitivity", command=senseEdit, width=20, height=2, bg=ui_AC1, fg=ui_Txt,
                                           activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    senseGet()

                    # For getting help / viewing the FAQ
                    helperTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    helperFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    helperLabel = tk.Label(helperTF, text="HELP", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    helperDescLabel = tk.Label(helperTF, text="Contains info on how to use the App", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))

                    tutorial_button = tk.Button(helperFrame, text="HELP", command=run.tutorial, width=10, height=2, bg=ui_AC1, fg=ui_Txt,
                                                activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    faq_button = tk.Button(helperFrame, text="FAQs", command=run.faq, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1,
                                           border=0, font=(ui_Font, 10))

                    detectCamFunc()
                    gearTF.pack(side="top", anchor="nw", fill="x")
                    gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")

                    winStateTF.pack(side="top", anchor="nw", fill="x")
                    winStateFrame.pack(anchor="w", fill="x")

                    miscTF.pack(side="top", anchor="nw", fill="x")
                    miscFrame.pack(anchor="w", fill="x")

                    camTF.pack(side="top", anchor="nw", fill="x")
                    camFrame.pack(anchor="w", fill="x")
                    camDisplayFrame.pack(anchor="w", fill="x")

                    sensTF.pack(side="top", anchor="nw", fill="x")
                    sensFrame.pack(anchor="w", fill="x")

                    helperTF.pack(side="top", anchor="nw", fill="x")
                    helperFrame.pack(anchor="w", fill="x")
            
                    closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
                    
                    winStateLabel.pack(padx=10, pady=5, anchor="nw")
                    winStateDescLabel.pack(padx=10, pady=2, anchor="nw")

                    miscLabel.pack(padx=10, pady=5, anchor="nw")
                    miscDescLabel.pack(padx=10, pady=2, anchor="nw")

                    camLabel.pack(padx=10, pady=5, anchor="nw")
                    camDescLabel.pack(padx=10, pady=2, anchor="nw")
                    camLister.pack(padx=10, pady=2, anchor="nw")

                    sensLabel.pack(padx=10, pady=5, anchor="nw")
                    sensDescLabel.pack(padx=10, pady=2, anchor="nw")
                    sensSlider.pack(padx=10, pady=2)
                    sensEditor.pack(padx=10, pady=10)

                    helperLabel.pack(padx=10, pady=5, anchor="nw")
                    helperDescLabel.pack(padx=10, pady=2, anchor="nw")

                    fullscreen_button.pack(padx=5, pady=5, side="left", anchor="w")
                    borderless_button.pack(padx=5, pady=5, side="left", anchor="w")
                    windowed_button.pack(padx=5, pady=5, side="left", anchor="w")

                    autoTutOpen.pack(padx=5, pady=5, side="left", anchor="nw")

                    tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")
                    faq_button.pack(padx=5, pady=5, side="left", anchor="nw")

                    generalUI.button_hover(closeGear,ui_AH1, ui_AC1)
                    generalUI.button_hover(fullscreen_button, ui_AH1, ui_AC1)
                    generalUI.button_hover(borderless_button, ui_AH1, ui_AC1)
                    generalUI.button_hover(windowed_button, ui_AH1, ui_AC1)

                    generalUI.button_hover(autoTutOpen, ui_AH1, ui_AC1)

                    generalUI.button_hover(camLister, ui_AH1, ui_AC1)

                    generalUI.button_hover(sensEditor, ui_AH1, ui_AC1)

                    generalUI.button_hover(faq_button, ui_AH1, ui_AC1)
                    generalUI.button_hover(tutorial_button, ui_AH1, ui_AC1)

                    gearAct = True
                    onceMade_Settings = True
                else:
                    # Reopens the settings
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    gearCanvas.coords(gearSettings, 0, 0)
                    root.bind("<Key>", settingsFunc.settingKey)
                    gearAct = True

                gearMaster.bind("<Configure>", settingsFunc.canvasConfig)
                gearCanvas.bind("<Configure>", canvasResize)
                gearCanvas.bind_all("<MouseWheel>", settingsFunc.mouseScroll)
                mouse.scroll(1,0)

            else:
                # Closes the settings otherwise
                settingsFunc.setClose()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up Settings: {e}")
        
# Class for running programs in the UI
class run:
    # Default Controls - Hybrid
    def program1():
        global process
        try:
            if process is not None:
                messagebox.showwarning("Warning", "Another program is already running. Please stop it first.")
                return
            process = subprocess.Popen(["py", os.path.join(base_path, "CC3.py")], shell=True)

            # Debugging info 
            print(f"Started Mouse Control with PID: {process.pid}")

            # For runGame to process
            return process
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Mouse Control: {e}")

    # Shows a tutorial in the app - Video / Text
    def tutorial():
        global tutAct, MaxRes, tutCanvas, onceMade_Tut, gearMaster
        try:
            # Checks if Escape key is pressed
            def tutKey(key):
                if key.keysym == "Escape":
                    tutClose()

            # Closes the tutorial
            def tutClose():
                try:
                    global tutAct
                    tutCanvas.place_forget()
                    tutAct = False
                    
                    # Restores scroll functionality for settings or game tab
                    if gearAct:
                        gearMaster.bind("<Configure>", settingsFunc.canvasConfig)
                        gearCanvas.bind_all("<MouseWheel>", settingsFunc.mouseScroll)
                        root.bind("<Key>", settingsFunc.settingKey)
                    else:
                        gamesDisplay.bind("<Configure>", gameTabFunc.gamesDConfig)
                        gamesDisplay.bind_all("<MouseWheel>", gameTabFunc.gamesDScroll)
                        root.bind("<Key>", quit.exit_viaKey)
                
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to close the tutorial: {e}")

                        # Toggle for auto start tutorial
            
            # Closes the tutorial and sets the config.ini to disabled
            def tutDis():
                tutFuncState = ""
                tutClose()
                settingsFunc.setTutAuto(tutFuncState)

            # Scroll Functions for tutorial UI
            def tutConfig(e):
                tutCanvas.configure(scrollregion=tutCanvas.bbox("all"))

            def tutScroll(e):
                global onceSet_Tut
                tutCanvas.yview_scroll(-1 * (e.delta // 100), "units")
                if not onceSet_Tut:
                    tutCanvas.yview_moveto(0)
                    onceSet_Tut = True
            
            # Resizes the tutorial canvas when the window is resized
            def tutResize(e):
                if not isinstance(e, int):
                    tutCanvas.itemconfig(tutDisplay, width=e.width)        
                else:
                    tutCanvas.itemconfig(tutDisplay, width=e)

            tutMenu = tk.Frame(tutMaster, bg=ui_AC1)
            tutText = tk.Frame(tutMaster, bg=ui_AC3)

            # Displays the tutorial canvas
            if not tutAct:
                if not onceMade_Tut:
                    tutCanvas.place(relheight=1, relwidth=1)
                    root.bind("<Key>", tutKey)
                    tk.Misc.lift(tutCanvas)
                    tutDisplay = tutCanvas.create_window((0, 0), window=tutMaster)
                    
                    uiTabsPNG = f"{base_path}\\img\\tutimg\\uiTabs.png"
                    if os.path.isfile(uiTabsPNG):
                        tabIMG = Image.open(uiTabsPNG)  
                        tabsImg = ImageTk.PhotoImage(tabIMG)
                    else:
                        messagebox.showerror("Error", "The uiTabs image cannot be found!")
                        return False

                    gameTabPNG = f"{base_path}\\img\\tutimg\\gameTab.png"
                    if os.path.isfile(gameTabPNG):
                        gtabIMG = Image.open(gameTabPNG)  
                        gametabImg = ImageTk.PhotoImage(gtabIMG)
                    else:
                        messagebox.showerror("Error", "The gameTab image cannot be found!")
                        return False

                    addGamePNG = f"{base_path}\\img\\tutimg\\addGame.png"
                    if os.path.isfile(addGamePNG):
                        gaddImg = Image.open(addGamePNG)  
                        gameAddImg = ImageTk.PhotoImage(gaddImg)
                    else:
                        messagebox.showerror("Error", "The addGame image cannot be found!")
                        return False

                    tutTitle = tk.Label(tutText, text="GETTING STARTED WITH HANDFLUX", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 25, ui_Bold))
                    tutDesc1 = tk.Label(tutText, text="This UI can be closed by clicking on 'Close' or pressing the ESC key",
                                        bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 20))
                    tutDesc2 = tk.Label(tutText, text="Tip: You can tell the app to not show this by going to SETTINGS", bg=ui_AC2,
                                        fg=ui_Txt, font=(ui_Font, 20))
                    tutUIBase = tk.Label(tutText, text="Main Menu Tabs", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 18, ui_Bold))
                    tutUIImg = tk.Label(tutText, image=tabsImg, bg=ui_AC1, fg=ui_Txt, border=0)
                    tutUIImg.image = tabsImg

                    tutUIG = tk.Label(tutText, text="GAMES – Shows the games from the games list text file.", bg=ui_AC2, fg=ui_Txt,
                                      font=(ui_Font, 14))
                    tutUIK = tk.Label(tutText, text="KEYBINDS – Shows the gestures and the keys they are mapped to.",  bg=ui_AC2,
                                      fg=ui_Txt, font=(ui_Font, 14))
                    tutUIS = tk.Label(tutText, text="SETTINGS – Opens up the settings for you to fine tune.", bg=ui_AC2, fg=ui_Txt,
                                      font=(ui_Font, 14))
                    tutUIQ = tk.Label(tutText, text="QUIT - Closes the App", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))

                    tutGTBase = tk.Label(tutText, text="Game Tab", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 18, ui_Bold))
                    tutGTImg = tk.Label(tutText, image=gametabImg, bg=ui_AC1, fg=ui_Txt, border=0)
                    tutGTDesc = tk.Label(tutText, text="Displays the games and apps you can use. The default items are listed above.",
                                         bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14, ui_Bold))
                    tutGTGC1 = tk.Label(tutText, text="1. (Optional) Type the item's name in the searchbar and click on 'Search' to filter it.",
                                        bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))
                    tutGTGC2 = tk.Label(tutText, text="2. Click on that game/app to go to that game/app.", bg=ui_AC2, fg=ui_Txt,
                                        font=(ui_Font, 14))
                    tutGTImg.image = gametabImg
                    
                    tutAGDesc1 = tk.Label(tutText, text="To add a game or app to the list Click on the Add a Game Button.", bg=ui_AC2,
                                          fg=ui_Txt, font=(ui_Font, 18, ui_Bold))
                    tutAGImg = tk.Label(tutText, image=gameAddImg, bg=ui_AC1, fg=ui_Txt, border=0)
                    tutAGDesc2 = tk.Label(tutText, text="Then do these steps to add a new item to the Games List.", bg=ui_AC2, fg=ui_Txt,
                                          font=(ui_Font, 18, ui_Bold))
                    tutAGImg.image = gameAddImg

                    tutAGS1 = tk.Label(tutText, text="1. (REQUIRED) Click on Configure Filepath to set the EXE for the app to use.",
                                       bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 14))
                    tutAGS2 = tk.Label(tutText, text="2. Type in a name for the new item.", bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))
                    tutAGS3 = tk.Label(tutText, text="3. (Optional) Type in a description for the new item.", bg=ui_AC2, fg=ui_Txt,
                                       font=(ui_Font, 14))
                    tutAGS4 = tk.Label(tutText, text="4. (Optional) Click on the white area to add a thumbnail for the new item.",
                                       bg=ui_AC2, fg=ui_Txt, font=(ui_Font, 14))
                    tutAGS5 = tk.Label(tutText, text="5. Click on 'Add Game to Games List' to add it to the Games List.", bg=ui_AC2,
                                       fg=ui_Txt, font=(ui_Font, 14))

                    closeTut = tk.Button(tutMenu, text="Close", command=tutClose, border=0, bg=ui_AC1, fg=ui_Txt,
                                         font=(ui_Font, 25, ui_Bold))
                    hideTut = tk.Button(tutMenu, text="Do not show again", command=tutDis, border=0, bg=ui_AC1, fg=ui_Txt,
                                        font=(ui_Font, 25, ui_Bold))
                    
                    tutMenu.pack(pady=5, side="top", fill="x")
                    tutText.pack(pady=5, side="bottom", fill="x")

                    closeTut.pack(padx=10, pady=5, side="right")
                    hideTut.pack(padx=10, pady=5, side="right")

                    generalUI.button_hover(closeTut, ui_AH1, ui_AC1)
                    generalUI.button_hover(hideTut, ui_AH1, ui_AC1)
                    
                    tutTitle.pack(pady=5)
                    tutDesc1.pack(pady=5)
                    tutDesc2.pack(pady=5)

                    tutUIBase.pack(pady=40)
                    tutUIImg.pack(pady=5)

                    tutUIG.pack(pady=5)
                    tutUIK.pack(pady=5)
                    tutUIS.pack(pady=5)
                    tutUIQ.pack(pady=5)

                    tutGTBase.pack(pady=40)
                    tutGTImg.pack(pady=5)
                    tutGTDesc.pack(pady=5)
                    tutGTGC1.pack(pady=5)
                    tutGTGC2.pack(pady=5)

                    tutAGDesc1.pack(pady=40)
                    tutAGImg.pack()
                    tutAGDesc2.pack(pady=5)
                    tutAGS1.pack(pady=5)
                    tutAGS2.pack(pady=5)
                    tutAGS3.pack(pady=5)
                    tutAGS4.pack(pady=5)
                    tutAGS5.pack(pady=5)

                    tutAct = True
                    onceMade_Tut = True
                    mouse.scroll(1,0)
                    
                else:
                    tutCanvas.place(relheight=1, relwidth=1)
                    root.bind("<Key>", tutKey)
                    tk.Misc.lift(tutCanvas)
                    tutAct = True

                tutMaster.bind("<Configure>", tutConfig)
                tutCanvas.bind_all("<MouseWheel>", tutScroll)
                tutCanvas.bind("<Configure>", tutResize)

            else:
                #tutClose()
                pass

        except Exception as e:
            messagebox.showerror("Error", f"Failed to startup Tutorial process: {e}")

    # Shows the Frequently Asked Questions
    def faq():
        global faqAct
        try:
            # Checks if the escape key is pressed
            def faqKey(key):
                if key.keysym == "Escape":
                    faqClose()
            
            # Closes the FAQ
            def faqClose():
                global faqAct
                faqCanvas.place_forget()
                faqAct = False
                root.bind("<Key>", settingsFunc.settingKey)
            
            # Function to Load a TXT File in the folder to faqtxt Text Element
            def txtLoader():
                faqRef = f"{base_path}\\resources\\faq_text.txt"
                if os.path.isfile(faqRef):
                    with open(faqRef, "r") as txtfile:
                        faq_text = txtfile.read()
                        faqtxt.insert(tk.END, faq_text)
                        txtfile.close()
                else:
                    messagebox.showerror("Error", "The FAQ Text file cannot be found!")
                    return False
            
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
                faqtxt = tk.Text(faqFrame, yscrollcommand = faqScroll.set, bg=ui_AC3, height=MaxRes[0], width=MaxRes[1],
                                 font=(ui_Font, 14), fg=ui_Txt, border=0, wrap="word")

                # Label and button to close the FAQ Window
                FAQlabel = tk.Label(faqTF, text="Frequently Asked Questions", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 20, ui_Bold))
                close_faq = tk.Button(faqTF, text="Return", command=faqClose, width=10, height=0, bg=ui_AH1, fg=ui_Txt,
                                      border=0, font=(ui_Font, 15, ui_Bold))

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

# Class for closing the window
class quit:
    # Main exit function
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
                    yesButton = tk.Button(quitCan, text="YES", command=zeroAll ,width=15, height=3, bg=ui_AC2, fg=ui_Txt,
                                          border=0, font=(ui_Font, 20))
                    noButton = tk.Button(quitCan, text="NO", command=stayIn ,width=15, height=3, bg=ui_AC2, fg=ui_Txt,
                                         border=0, font=(ui_Font, 20))

                    quitLabel.pack(padx=25, pady=25, anchor="center")

                    yesButton.pack(padx=25, pady=25, anchor="center")
                    noButton.pack(padx=25, pady=25, anchor="center")

                    generalUI.button_hover(yesButton, ui_AE, ui_AC2)
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

    # Opens up exit confirmation dialog
    def exit_viaKey(key):
        global quitAct
        if not quitAct:
            if key.keysym == "Escape" and quitCan.winfo_ismapped and tutCanvas.winfo_ismapped != True and faqCanvas.winfo_ismapped !=True:
                quit.exit_program()
            else:
                pass
    
    # Closes the active control window
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
            #messagebox.showinfo("Info", "No program is currently running.")

# Sets the base path to the scripts.
base_path = os.getcwd()
configRef = f"{base_path}\\resources\\config.ini"
gameListRef = f"{base_path}\\resources\\gamesList.txt"

# Version Number 
versionNum = "1.56"

# For tracking UI activity and subprocesses
tutStartUp = ""
autoTutOpen = ""
faqAct = False
gearAct = False
quitAct = False
tutAct = False
onceMade_Quit = False
onceMade_Settings = False
onceMade_Tut = False
onceSet_Game = False
onceSet_Binds = False
onceSet_Settings = False
onceSet_Tut = False
textR = False
filter = ""
mouse = Controller()

imgPath = ""
exePath = ""
baseImg = ""

process = None
gameProcess = None

ui_AC1 = ""
ui_AC2 = ""
ui_AC3 = ""
ui_AC4 = ""
ui_AE = ""
ui_AH1 = ""
ui_AH2 = ""
ui_AH3 = ""
ui_Bold = ""
ui_Font = ""
ui_Txt = ""
testingTurquoise = "#00FFD5"
generalUI.getStyling()

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
camGet = {}
profileControls = {}

# Checks for gameslist file existence
if os.path.isfile(gameListRef):
    gamesList = open(gameListRef, "r")
else:
    messagebox.showerror("Error", "The games list cannot be found!")
    exit()

gameTabFunc.gameDisplay(gamesList, filter)
generalUI.getCameras(camGet)

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

# Hand Controls definitions
hControls = {
    "Left": "left:",
    "Right": "right:"
}

# Control Type definitions for Keybinds - mouse_movement, open_keyboard and detect input
controlsList = [
    "Mouse Movement",
    "Detect Input",
]

# Initial list for listing keybinds, will be filled with loadKeys
initBinds = {}

# Initial list for listing the profiles, will be filled with profiles
pControls = {}
generalUI.loadProfiles(pControls)

# Initialises the tkinter root window with 1280 x 720 as the default
root = tk.Tk()
root.title(f"Handflux {versionNum}")
root.geometry(f"{Defined_Res['1280x720'][0]}x{Defined_Res['1280x720'][1]}")
root.iconbitmap("handflux.ico")
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
bindCType = {}
bindChange = {}
controlType = {}

bindsMasterFrame = tk.Frame(uiDynamTabs["Binds"], background=ui_AC1)
bindsLabel = tk.Label(bindsMasterFrame, text="KEYBINDS", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
saveBinds = tk.Button(bindsMasterFrame, text="Save Keybinds", command=bindsTabFunc.saveKeys, width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
resetBinds = tk.Button(bindsMasterFrame, text="Reset Keybinds", command=bindsTabFunc.resetKeys, width=15, height=2, bg=ui_AH1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

dropFrame = tk.Frame(bindsMasterFrame, padx=5, pady=5, bg=ui_AC2)
handOption = tk.StringVar(root)
handOption.set(next(iter(hControls)))
handDrop = tk.OptionMenu(dropFrame, handOption, *hControls)
handDrop.configure(bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, highlightbackground=ui_AC1, font=(ui_Font, 12))

profileOption = tk.StringVar(root)
profileOption.set(next(iter(pControls)))
profileDrop = tk.OptionMenu(dropFrame, profileOption, *pControls)
profileDrop.configure(bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, highlightbackground=ui_AC1, font=(ui_Font, 12))

dropFrame.pack(padx=20, pady=5, anchor="nw")
handDrop.pack(padx=10, side="left")
profileDrop.pack(padx=10, side="left")

generalUI.button_hover(saveBinds,ui_AH1, ui_AC2)   
generalUI.button_hover(resetBinds,ui_AE, ui_AH1)

# GUI Labels
TKlabel = tk.Label(uiMasterFrame, text=f"HANDFLUX {versionNum}", anchor="ne", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))

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
menuBindsTabBorder.pack(side="left", anchor="w")
menuBindsTab.pack(padx=2, pady=2, side="left", anchor="w")
settingsBorder.pack(side="left", anchor="w")
settings_button.pack(padx=2, pady=2, side="left", anchor="nw")
exit_button.pack(padx=5, pady=5, side="left", anchor="nw")

generalUI.button_hover(menuGameTab, ui_AH1, ui_AC1)
generalUI.button_hover(menuBindsTab, ui_AH1, ui_AC1)
generalUI.button_hover(settings_button, ui_AH1, ui_AC1)
generalUI.button_hover(exit_button, ui_AE, ui_AC1)

uiDynamFrame.pack(side="top", fill="x")

# Global Canvases
quitCan = tk.Canvas(root, width=1200, height=600, bg=ui_AC2, highlightthickness=0)
tutCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC2, highlightthickness=0)
tutMaster = tk.Frame(tutCanvas, padx=5, pady=5, bg=ui_AC1)
faqCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC3, highlightthickness=0)
gearCanvas = tk.Canvas(root, width=1200, height=600, bg=ui_AC3, highlightthickness=0)
gearMaster = tk.Frame(gearCanvas, padx=5, pady=5, bg=ui_AC1)
bindsCanvas= tk.Canvas(uiDynamTabs["Binds"], width=MaxRes[0], height=MaxRes[1], background=ui_AC1, highlightthickness=0)
bindMaster = tk.Frame(bindsCanvas, padx=5, pady=5, bg=ui_AC2)

# Run the tkinter event loop
root.after(50, generalUI.startTutorial())
root.mainloop()