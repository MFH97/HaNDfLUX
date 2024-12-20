# Main program for GUI interface
import subprocess, os, psutil, tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog

# Additonal imports
import pyautogui, re
import time, threading

class generalUI:
    def button_hover(tkb, b_Hover, b_Release ):
        # Changes the colour of the button whether if it hovers or not
        try:
            tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
            tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change the button's colour: {e}")

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
    # Maps the gamesDisplay frame for usage
    def __init__(self, gFrame):
        self.gFrame = gFrame
        gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
        gameTabFunc.gameDisplay(gamesList, filter)
        gameTabFunc.id_Game(gamesDisplay)
        for uiBorder in uiMasterFrame.winfo_children():
            uiBorder.config(bg=ui_AC1)
            menuGameTabBorder.config(bg=ui_AH1)
        
    # Swaps the current Tab to the Games Tab
    def run_gameMenu():
        global menuAct, uiDynamTabs, gameDisplay
        try:  
            def showF(uiGame):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiGame.pack(fill="both")

            if menuAct != "Game":
                showF(uiDynamTabs["Game"])
                menuAct = "Game"
                gameDisplay.pack_forget()
                gameTabFunc(gamesDisplay)
                gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
            
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

            # Fills the new list
            for gItem in range(game_Count):
                gameFrame = tk.Frame(self, bg=ui_AC4)
                gameItem = tk.Text(gameFrame, bg=ui_AC4, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(ui_Font, 10))
                gameItem.insert(tk.END, gameDisplayArray[gItem])
                gameItem.configure(exportselection=0, state="disabled")

                gameImg = PhotoImage(file = thumbDisplayArray[gItem]).subsample(1,1)
                thumbDisplayArray[gItem] = gameImg
                gameButton = tk.Button(gameFrame, image=gameImg, command=lambda gIter=gItem: gameTabFunc.game_Describe(gameDisplayArray[gIter]), bg=ui_AC1, fg=ui_Txt, border=0)

                gameFrame.pack(padx=25, pady=2, side="left")
                gameButton.pack()
                gameItem.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fill the game tab: {e}")
        
    # Gets the available games from gamesList.txt using filters from filterGame
    def gameDisplay(txt, filter):
        global game_Count, gamesList, gameDisplayArray, descDisplayArray, gamesList, gamesDisplay
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
                #print(filterForm)
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
                        file = base_path + gameThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif "ExeÃ· " in line:
                        gameExe = line.split("Ã· ")
                        file = gameExe[2].replace("\n","")
                        exeDisplayArray.append(file)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the games: {e}")

    # Filters the output of gameDisplay
    def filterGame():
        global gamesList, gamesDisplay
        try:
            filter = gameSearchBar.get()
            if filter !="":
                gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
                gameTabFunc.gameDisplay(gamesList, filter)
                gameTabFunc.id_Game(gamesDisplay)
                gameSearchBar.delete(0, "end")
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
    
    # Resets the filters in filterGame
    def resetFilter():
        global gamesList, gamesDisplay
        try:
            filter = ""
            gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
            gameTabFunc.gameDisplay(gamesList, filter)
            gameTabFunc.id_Game(gamesDisplay)
            gameSearchBar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset the filters: {e}")

    # Displays that specific game
    def game_Describe(gameItem):
        global gamesDisplay, gameMasterFrame, gameDetails, gameDisplay, gameProcess, gamesList, process

        # Goes back to the Games Tab
        def goBack():
            gameDisplay.pack_forget()
            gameTabFunc(gamesDisplay)
            gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
            gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
            gItemExt.clear()
        
        # Goes to the respective profile's description in Profile Tab
        def goToProfile(profileItem):
            gameDisplay.pack_forget()
            profileTabFunc.run_profileMenu()
            profileTabFunc.profile_Describe(profileItem)

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

            try:
                gameEXE = gameDetails[3]
                gameEXE = gameEXE.split("/")

                if len(gameDetails[3]) == 0 or gameDetails[3] == "Filepath":
                    messagebox.showerror("Error", "Game's EXE filepath is NOT configured")
                else:
                    # Starts up the respective game's control and game
                    if gameDetails[4] == "Mouse":
                       run.program1()
                    elif gameDetails[4] == "Two-Hands":
                       run.program2()
                    elif gameDetails[4] == "Swipe":
                        run.program3()
                    elif gameDetails[4] == "Hybrid":
                        run.program4()
                    elif gameDetails[4] == "HB2":
                        run.program5()
                    else: 
                        pass
                    os.startfile(gameDetails[3])
                    gameStart(gameEXE[-1])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to run the game: {e}")

        # Experimental function to write the filepath for an EXE to the gamesList
        def writeEXE():
            try:
                # Formats the filepath to fit the gamesList format
                filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",filetypes = (("Exe files","*.exe*"),("Text files","*.txt*")))
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
                        file = base_path + gameThumb[2].replace("\n","")
                        gameDetails.append(file)
                    
                    elif f"ExeÃ· {gItemExt[0]}" in line:
                        gameExe = line.split("Ã· ")
                        file = gameExe[2].replace("\n","")
                        gameDetails.append(file)
                    
                    elif f"ControlsÃ· {gItemExt[0]}" in line:
                        gameControls = line.split("Ã· ")
                        file = gameControls[2].replace("\n","")
                        gameDetails.append(file)

                    elif f"GestureMapÃ· {gItemExt[0]}" in line:
                        gestureControl = line.split("Ã· ")
                        file = gestureControl[2].replace("\n","")
                        gameDetails.append(file)

            # Displays the selected game
            game_DisplayFrame = tk.Frame(gameDisplay, bg=ui_AC2)
            game_DisplayPicFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_InfoFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_RunFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            gameItemLabel = tk.Label(gameDisplay, text=gameDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            profileLink = tk.Button(gameDisplay, text="Map Profiles", command=lambda: goToProfile(gameDetails[0]), bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
     
            gameItemImg = PhotoImage(file = gameDetails[2]).subsample(1,1)
            gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
            gameImg.image = gameItemImg

            gameItemTxt = tk.Text(game_DisplayFrame, width=65, height=5, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            gameItemTxt.insert(tk.END, gameDetails[1])
            gameItemTxt.configure(exportselection=0, state="disabled")  

            gameItemFileP = tk.Button(game_InfoFrame, text="Configure Filepath", command=writeEXE, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gameItemFile = tk.Label(game_InfoFrame, text=gameDetails[3], wraplength=MaxRes[0], height=1, justify="left", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 12))
            
            gameItemExe = tk.Button(game_RunFrame, text=f"Start Game with {gameDetails[4]} Controls", command=runGame, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gameRelease = tk.Button(game_RunFrame, text=f"Release Gesture Control", command=quit.release_control, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))

            game_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            game_RunFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            gameItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)

            profileLink.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(profileLink, ui_AH1, ui_AC1)

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
      
class profileTabFunc:
    # For Profile Tab Functions
    # Maps the profilesDisplay frame for usage
    def __init__(self, pFrame):
        self.pFrame = pFrame
        profilesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
        profileTabFunc.profileDisplay(profilesList, filter)
        profileTabFunc.id_Profile(profilesDisplay)
        for uiBorder in uiMasterFrame.winfo_children():
            uiBorder.config(bg=ui_AC1)
            menuProfileTabBorder.config(bg=ui_AH1)

    # Swaps the current tab to the Profiles Tab
    def run_profileMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Profile Tab - Shows the profiles the user set
            def showF(uiProfile):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiProfile.pack(fill="both")

            if menuAct != "Profile":
                showF(uiDynamTabs["Profiles"])
                menuAct = "Profile"
                profileDisplay.pack_forget()
                profileMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                profilesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                profileTabFunc(profilesDisplay)

                profileMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                profileLabel.pack(padx=10, pady=5, side="left")
                profile_SearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
                profile_ResetBorder.pack(padx=5, pady=15, side="right", anchor="ne")

                profileResetSearch.pack(padx=2, pady=2, side="right")
                profileSearchButton.pack(padx=2,pady=2, anchor="center")
                profileSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Profile Tab: {e}")
    
    def id_Profile(self):
        try:
            # Clears the old list
            for pItem in self.winfo_children():
                pItem.destroy()

            # Fills the new list
            for pItem in range(game_Count):
                profileFrame = tk.Frame(self, bg=ui_AC4)
                profileItem = tk.Text(profileFrame, bg=ui_AC4, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(ui_Font, 10))
                profileItem.insert(tk.END, gameDisplayArray[pItem])
                profileItem.configure(exportselection=0, state="disabled")

                profileImg = PhotoImage(file = thumbDisplayArray[pItem]).subsample(1,1)
                thumbDisplayArray[pItem] = profileImg
                profileButton = tk.Button(profileFrame, image=profileImg, command=lambda pIter=pItem: profileTabFunc.profile_Describe(gameDisplayArray[pIter]), bg=ui_AC1, fg=ui_Txt, border=0)

                profileFrame.pack(padx=25, pady=2, side="left")
                profileButton.pack()
                profileItem.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fill the profile tab: {e}")
        
    # Gets the available games from gamesList.txt using filters
    def profileDisplay(txt, filter):
        global game_Count, gamesList, gameDisplayArray, profileDisplayArray, descDisplayArray, gamesList, gamesDisplay
        try:
            # Resets the list
            game_Count = 0
            gameDisplayArray.clear()
            descDisplayArray.clear()
            thumbDisplayArray.clear()
            exeDisplayArray.clear()
            profileDisplayArray.clear()

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
                        file = base_path + gameExe[2].replace("\n","")
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
                        file = base_path + gameThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif "ExeÃ· " in line:
                        gameExe = line.split("Ã· ")
                        file = base_path + gameExe[2].replace("\n","")
                        exeDisplayArray.append(file)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the game profiles: {e}")

    # Filters the output of profilesDisplay
    def filterProfile():
        global gamesList, profilesDisplay
        try:
            filter = profileSearchBar.get()
            if filter !="":
                gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
                profileTabFunc.profileDisplay(gamesList, filter)
                profileTabFunc.id_Profile(profilesDisplay)
                profileSearchBar.delete(0, "end")
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the game profiles: {e}")
    
    # Resets the filters in filterProfiles
    def resetFilter():
        global gamesList, profilesDisplay
        try:
            filter = ""
            gamesList = open(f"{base_path}\\resources\\gamesList.txt", "r")
            profileTabFunc.profileDisplay(gamesList, filter)
            profileTabFunc.id_Profile(profilesDisplay)
            profileSearchBar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset the filters: {e}")

    # Displays that specific game's profile
    def profile_Describe(profileItem):
        global profilesDisplay, profileMasterFrame, gameDetails, profileDisplay

        # Goes back to the Games Tab
        def goBack():
            profileDisplay.pack_forget()
            profileTabFunc(profilesDisplay)
            profileMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
            profilesDisplay.pack(padx=10, pady=1, side="top", fill="x")
        
        # Goes to the respective game's description in Game Tab
        def goToGame(profileItem):
            profileDisplay.pack_forget()
            gameTabFunc.run_gameMenu()
            gameTabFunc.game_Describe(profileItem)

        # Goes to the mapped gesture
        def goToGesture(gestureItem):
            profileDisplay.pack_forget()
            gestureTabFunc.run_gestureMenu()
            gestureTabFunc.gesture_Describe(gestureItem)

        try:
            # Hides the game selection tab
            profileMasterFrame.pack_forget()
            profilesDisplay.pack_forget()

            # Creates an individual profile tab for the UI to use
            profileDisplay.pack(padx=10, pady=1, side="top", fill="x")

            # Clears the old items
            for gItem in profileDisplay.winfo_children():
                gItem.destroy()

            
            profileDetails.clear()
            unMapped.clear()
            unMappedDesc.clear()
            pItemExt = profileItem.split()
            gestureMap = []
            extractor = []
            mappedGes = []
            unMapGes = []
            unMapDesc = []
        
            # Displays the new items
            with open(f"{base_path}\\resources\\gamesList.txt", "r") as gameGet:
                for line in gameGet:
                    if f"GameÃ· {pItemExt[0]}" in line:
                        gameName = line.split("Ã· ")
                        profileDetails.append(gameName[2].replace("\n","'S PROFILE"))
            
                    elif f"ThumbImgÃ· {pItemExt[0]}" in line:
                        gameThumb = line.split("Ã· ")
                        extract = base_path + gameThumb[2].replace("\n","")
                        profileDetails.append(extract)
                
                    elif f"ExeÃ· {pItemExt[0]}" in line:
                        gameExe = line.split("Ã· ")
                        extract = gameExe[2].replace("\n","")
                        profileDetails.append(extract)
            
                    elif f"GestureMapÃ· {pItemExt[0]}" in line:
                        gameGesture = line.split("Ã· ")
                        gestureMap = gameGesture[2:]
                        for gesture in range(len(gestureMap)):
                            extractor.append(gestureMap[gesture].replace("\n",""))
                        profileDetails.append(extractor)
                    
                    elif f"ControlsÃ· {pItemExt[0]}" in line:
                        gameControl = line.split("Ã· ")
                        controlCheck = gameControl[2].replace("\n","")

            # Lists mapped gestures
            with open(f"{base_path}\\resources\\gesturesList.txt", "r") as gesturesGet:
                for line in gesturesGet:
                    if "ThumbImgÃ· " in line:
                        for things in profileDetails[3]:
                            testing = rf"\b{things}Ã·"
                            if re.search(testing, line):
                                gestureImg = line.split("Ã· ")
                                gestureImgForm = base_path + gestureImg[2].replace("\n","")
                                mappedGes.append(gestureImgForm)

                mapGesForm = ", ".join(profileDetails[3])
                profileDetails.append(mappedGes)
                profileDetails.append(f"MAPPED GESTURE(S): {mapGesForm}")
                
            # Lists unmapped gestures
            if controlCheck != "Swipe":
                with open(f"{base_path}\\resources\\gesturesList.txt", "r") as gesturesGet:
                    for line in gesturesGet:
                        if "ThumbImgÃ· " in line:
                            avT = line.split("Ã· ")
                            if avT[1].replace("\n","") not in profileDetails[3]:
                                unMapImg = line.split("Ã· ")
                                unMapImgForm = base_path + unMapImg[2].replace("\n","")
                                unMapImgDesc = unMapImg[1].replace("\n","")
                                unMapGes.append(unMapImgForm)
                                unMapDesc.append(unMapImgDesc)

                unMapDescForm = ", ".join(unMapDesc)
                unMapped.append(unMapGes)
                unMappedDesc.append(unMapDescForm)

            # Var checks
            #print(profileDetails[3])
            #print(unMapped)
            #print(unMappedDesc)

            # Displays the selected profile
            profile_DisplayFrame = tk.Frame(profileDisplay, bg=ui_AC2)
            profile_DisplayPicFrame = tk.Frame(profile_DisplayFrame, bg=ui_AC2)
            profile_InfoFrame = tk.Frame(profile_DisplayFrame, bg=ui_AC2)
            profile_GestureMap = tk.Frame(profile_DisplayFrame, bg=ui_AC2)
            profile_GesturePic = tk.Frame(profile_DisplayFrame, bg=ui_AC2)
            profile_Unmapped = tk.Frame(profile_DisplayFrame, bg=ui_AC2)
            profileItemLabel = tk.Label(profileDisplay, text=profileDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            profileScroll = tk.Scrollbar(profileDisplay, command=profileDisplay.yview)
            profileDisplay.configure(yscrollcommand=profileScroll.set)

            backButton = tk.Button(profileDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            gameLink = tk.Button(profileDisplay, text="Configure Game", command=lambda: goToGame(profileDetails[0]), bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))

            profileItemImg = PhotoImage(file = profileDetails[1]).subsample(1,1)
            profileImg = tk.Label(profile_DisplayPicFrame, image=profileItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
            profileImg.image = profileItemImg

            if profileDetails[3][0] == "NONE":
                #gestureLink = tk.Button(profileDisplay, text="No gesture", state="disabled", bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                gestureImgLabel = tk.Label(profile_GestureMap, text="NO MAPPED GESTURES", bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))
                profileGestureImg = tk.Label(profile_GesturePic, text="", bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))
                profileImg.pack(padx=4, pady=4, side="left", anchor="nw")
                profileGestureImg.pack(padx=4, pady=4, side="left", anchor="nw")
            else:
                for things in range(len(profileDetails[4])):
                    #gestureLink = tk.Button(profileDisplay, text="To Gesture", command=lambda: goToGesture(profileDetails[3]), bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                    gestureImg = PhotoImage(file = profileDetails[4][things]).subsample(3,3)
                    gestureImgLabel = tk.Label(profile_GestureMap, text=profileDetails[5], bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))
                    profileGestureImg = tk.Label(profile_GesturePic, image=gestureImg, bg=ui_AC1, fg=ui_Txt, border=0)
                    gestureImg.image = gestureImg
                    profileImg.pack(padx=4, pady=4, side="left", anchor="nw")
                    profileGestureImg.pack(padx=4, pady=4, side="left", anchor="nw")
                    #generalUI.button_hover(gestureLink, ui_AH1, ui_AC1)
            
            assignGesture = "AVAILABLE GESTURES: "
            if not unMappedDesc:
                assignGesture = "NO AVAIALBE GESTURES"
            else:
                for Iter in range(len(unMappedDesc)):
                    assignGesture += f" {unMappedDesc[Iter]} "

            unMapLabel = tk.Label(profile_Unmapped, text=assignGesture, bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))
            
            profile_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            profile_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            profile_GestureMap.pack(padx=5, pady=5, side="top", fill="x")
            profile_GesturePic.pack(padx=5, pady=5, side="top", fill="x")
            profile_Unmapped.pack(padx=5, pady=5, side="top", fill="x")
            
            gestureImgLabel.pack(padx=4, pady=4, side="top", anchor="nw")
            profile_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            profileItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            unMapLabel.pack(padx=5, pady=5, side="top", anchor="nw")
            backButton.pack(padx=4, pady=4, side="left", anchor="nw")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)

            gameLink.pack(padx=4, pady=4, side="left", anchor="nw")
            generalUI.button_hover(gameLink, ui_AH1, ui_AC1)
            
            for Iter in range(len(unMapGes)):
                availImg = PhotoImage(file = unMapGes[Iter]).subsample(3,3)
                ImgLabel = tk.Label(profile_Unmapped, image=availImg, bg=ui_AC1, fg=ui_Txt, border=0)
                availImg.image = availImg
                ImgLabel.pack(padx=4, pady=4, side="left", anchor="nw")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the individual profile: {e}")

class gestureTabFunc:
    # For Gesture Tab Functions
    # Maps the gesturesDisplay frame for usage
    def __init__(self, gFrame):
        self.gFrame = gFrame
        gesturesList = open(f"{base_path}\\resources\\gesturesList.txt", "r")
        gestureTabFunc.gestureDisplay(gesturesList, filter)
        gestureTabFunc.id_Gesture(gesturesDisplay)

        for uiBorder in uiMasterFrame.winfo_children():
            uiBorder.config(bg=ui_AC1)
            menuGestureTabBorder.config(bg=ui_AH1)

    # Swaps the current tab to the Gestures Tab
    def run_gestureMenu():
        global menuAct, uiDynamTabs
        try:
            # Swaps the current Tab for the Gestures Tab - Shows the gestures the user set
            def showF(uiGesture):
                for uiTabs in uiDynamTabs.values():
                    uiTabs.pack_forget()
                    uiGesture.pack(fill="both")
        
            if menuAct != "Gesture":
                showF(uiDynamTabs["Gestures"])
                menuAct = "Gesture"
                gestureDisplay.pack_forget()
                gestureMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gesturesDisplay.pack(padx=10, pady=1, side="top", fill="x")
                gestureTabFunc(gesturesDisplay)

                gestureMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gestureLabel.pack(padx=10, pady=5, side="left")
                gesture_SearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
                gesture_ResetBorder.pack(padx=5, pady=15, side="right", anchor="ne")

                gestureResetSearch.pack(padx=2, pady=2, side="right")
                gestureSearchButton.pack(padx=2,pady=2, anchor="center")
                gestureSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")   
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Gestures Tab: {e}")
    
    def id_Gesture(self):
        try:
            # Clears the old list
            for gItem in self.winfo_children():
                gItem.destroy()

            # Fills the new list
            for gItem in range(gesture_Count):
                gestureFrame = tk.Frame(self, bg=ui_AC4)
                gestureItem = tk.Text(gestureFrame, bg=ui_AC4, fg=ui_Txt, height=3, width=20, border=0, wrap="word", font=(ui_Font, 10))
                gestureItem.insert(tk.END, gameDisplayArray[gItem])
                gestureItem.configure(exportselection=0, state="disabled")

                gestureImg = PhotoImage(file = thumbDisplayArray[gItem]).subsample(2,2)
                thumbDisplayArray[gItem] = gestureImg
                profileButton = tk.Button(gestureFrame, image=gestureImg, command=lambda gIter=gItem: gestureTabFunc.gesture_Describe(gameDisplayArray[gIter]), bg=ui_AC1, fg=ui_Txt, border=0)

                gestureFrame.pack(padx=25, pady=2, side="left")
                profileButton.pack()
                gestureItem.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fill the gestures tab: {e}")
        
    # Gets the available games from gesturesList.txt using filters from filterGesture
    def gestureDisplay(txt, filter):
        global gesture_Count, gesturesList, descDisplayArray, gamesList, gesturesDisplay
        try:
            # Resets the list
            gesture_Count = 0
            gameDisplayArray.clear()
            descDisplayArray.clear()
            thumbDisplayArray.clear()
            exeDisplayArray.clear()
            gameDisplayArray.clear()

            # Redundant Filter check
            if filter:
                filterForm = filter.upper()
                # Fills the list with the filter results
                for line in txt:
                    if f"GestureÃ· {filterForm}" in line:
                        gestureName = line.split("Ã· ")
                        gameDisplayArray.append(gestureName[2].replace("\n",""))
                        gesture_Count += 1
            
                    elif f"DescÃ· {filterForm}" in line:
                        gestureDesc = line.split("Ã· ")
                        descDisplayArray.append(gestureDesc[2].replace("\n",""))
            
                    elif f"ThumbImgÃ· {filterForm}" in line:
                        gestureThumb = line.split("Ã· ")
                        file = base_path + gestureThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif f"GameMapÃ· {filterForm}" in line:
                        gestureMap = line.split("Ã· ")
                        file = base_path + gestureMap[2].replace("\n","")
                        exeDisplayArray.append(file)
            else:
                # Default list filling
                for line in txt:
                    if "GestureÃ·" in line:
                        gestureName = line.split("Ã· ")
                        gameDisplayArray.append(gestureName[2].replace("\n",""))
                        gesture_Count += 1
            
                    elif "DescÃ·" in line:
                        gestureDesc = line.split("Ã· ")
                        descDisplayArray.append(gestureDesc[2].replace("\n",""))
            
                    elif "ThumbImgÃ·" in line:
                        gestureThumb = line.split("Ã· ")
                        file = base_path + gestureThumb[2].replace("\n","")
                        thumbDisplayArray.append(file)
                
                    elif "GameMapÃ·" in line:
                        gestureMap = line.split("Ã· ")
                        file = base_path + gestureMap[2].replace("\n","")
                        exeDisplayArray.append(file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the gestures: {e}")

    # Filters the output of gesturesDisplay
    def filterGesture():
        global gesturesList, gesturesDisplay
        try:
            filter = gestureSearchBar.get()
            if filter !="":
                gesturesList = open(f"{base_path}\\resources\\gesturesList.txt", "r")
                gestureTabFunc.gestureDisplay(gesturesList, filter)
                gestureTabFunc.id_Gesture(gesturesDisplay)
                gestureSearchBar.delete(0, "end")
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the gestures: {e}")
    
    # Resets the filters in filterGestures
    def resetFilter():
        global gesturesList, gesturesDisplay
        try:
            filter = ""
            gesturesList = open(f"{base_path}\\resources\\gesturesList.txt", "r")
            gestureTabFunc.gestureDisplay(gesturesList, filter)
            gestureTabFunc.id_Gesture(gesturesDisplay)
            gestureSearchBar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset the filters: {e}")

    # Displays that specific gesture
    def gesture_Describe(gestureItem):
        global gesturesDisplay, gestureMasterFrame, gestureDetails, gestureDisplay

        # Goes back to the Gestures Tab
        def goBack():
            gestureDisplay.pack_forget()
            gestureTabFunc(gesturesDisplay)
            gestureMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
            gesturesDisplay.pack(padx=10, pady=1, side="top", fill="x")
        
        # To search for games that has this gesture, temporarily goes to the hardcoded profile instead
        def goToProfile(profileItem):
            gestureDisplay.pack_forget()
            profileTabFunc.run_profileMenu()
            profileTabFunc.profile_Describe(profileItem)
            #profileList = open(f"{base_path}\\resources\\gamesList.txt", "r")
            #profileTabFunc.profileDisplay(profileList, profileItem)
            #print(profileItem)

        try:
            # Hides the gesture selection tab
            gestureMasterFrame.pack_forget()
            gesturesDisplay.pack_forget()

            # Creates an individual gesture tab for the UI to use
            gestureDisplay.pack(padx=10, pady=1, side="top", fill="x")

            # Clears the old items
            for gItem in gestureDisplay.winfo_children():
                gItem.destroy()
        
            gestureDetails.clear()
            gItemExt = gestureItem.split()
            testFilter = rf"\b{re.escape(gItemExt[0])}\b"
        
            # Displays the new items
            with open(f"{base_path}\\resources\\gesturesList.txt", "r") as gestureGet:
                for line in gestureGet:
                    if f"GestureÃ· {gItemExt[0]}" in line:
                        gestureName = line.split("Ã· ")
                        gestureDetails.append(f"SELECTED GESTURE: {gestureName[2].replace("\n"," ")}")
                
                    elif f"DescÃ· {gItemExt[0]}" in line:
                        gestureDesc= line.split("Ã· ")
                        extract = gestureDesc[2].replace("\n","")
                        gestureDetails.append(extract)
                    
                    elif f"ThumbImgÃ· {gItemExt[0]}" in line:
                        gestureImg = line.split("Ã· ")
                        extract = base_path + gestureImg[2].replace("\n","")
                        gestureDetails.append(extract)

            with open(f"{base_path}\\resources\\gamesList.txt", "r") as gameGet:
                for line in gameGet:
                    if re.search(testFilter, line):
                        gameName = line.split("Ã· ")
                        extract = gameName[1].replace("\n","")
                        gestureDetails.append(extract)
                        
            gesture_DisplayFrame = tk.Frame(gestureDisplay, bg=ui_AC2)
            gesture_DisplayPicFrame = tk.Frame(gesture_DisplayFrame, bg=ui_AC2)
            gesture_InfoFrame = tk.Frame(gesture_DisplayFrame, bg=ui_AC2)
            gestureItemLabel = tk.Label(gestureDisplay, text=gestureDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            backButton = tk.Button(gestureDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            
            gestureItemImg = PhotoImage(file = gestureDetails[2]).subsample(1,1)
            gestureImg = tk.Label(gesture_DisplayPicFrame, image=gestureItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
            gestureImg.image = gestureItemImg

            gestureDescTitle = tk.Label(gesture_InfoFrame, text="Gesture Information: ", bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            gestureDesc = tk.Label(gesture_InfoFrame, text=gestureDetails[1], bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gesturePadding = tk.Label(gesture_InfoFrame, bg=ui_AC1, fg=ui_Txt, border=0)
            
            gameMapTitle = tk.Label(gesture_InfoFrame, text="Currently Mapped to: ", bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))

            # Checks if the gesture is mapped to a game profile
            if len(gestureDetails) < 4:
                profileLink = tk.Button(gestureDisplay, text="No profiles known", state="disabled", bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                gameMap = tk.Label(gesture_InfoFrame, text="No game", bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            else:
                profileLink = tk.Button(gestureDisplay, text="Configure Profile", command=lambda: goToProfile(gestureDetails[3]), bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
                gameMap = tk.Label(gesture_InfoFrame, text=gestureDetails[3], bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
                generalUI.button_hover(profileLink, ui_AH1, ui_AC1)
            #gameMap = tk.Label(gesture_InfoFrame, text=gestureDetails[3], bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            
            gesture_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            gesture_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            gestureItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            gesture_InfoFrame.pack(padx=5, pady=10, side="top", fill="x")
            gestureDescTitle.pack(padx=5, pady=5, side="top", anchor="nw")
            gestureDesc.pack(padx=5, pady=5, side="top", anchor="nw")
            gesturePadding.pack(padx=5, pady=10, side="top", anchor="nw")
            gameMapTitle.pack(padx=5, pady=5, side="top", anchor="nw")
            gameMap.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="nw")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)

            profileLink.pack(padx=4, pady=4, side="left", anchor="nw")

            gestureImg.pack(padx=4, pady=4, side="left", anchor="nw")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display the individual gesture: {e}")

class quit:
    # Class for closing the window
    def exit_program():
        global quitCan, quitAct, onceMade_Quit, gamesList
        try:
            # Closes everything and ensures any running process is terminated before exiting
            def zeroAll():
                gamesList.close()
                gesturesList.close()
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
            if key.keysym == "Escape" and quitCan.winfo_ismapped and tutCanvas.winfo_ismapped != True and gearCanvas.winfo_ismapped !=True and faqCanvas.winfo_ismapped !=True:
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

                    tutFrame = tk.Frame(tutCanvas, padx=5, pady=5, bg=ui_AC2)

                    tutContent = [
                        tk.Label(tutFrame, text="GETTING STARTED", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 25, ui_Bold)),
                        tk.Label(tutFrame, text="To close, click the button labelled 'Close', or press the Escape Key", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 18, ui_Bold)),
                        tk.Label(tutFrame, text="Games - Shows the available games for mapping ",  bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Profiles - Shows the profiles you made, contains the gestures you mapped for a game",  bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Gestures - Shows the gestures you made for mapping", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Settings - Opens up the settings for you to fine tune", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="FAQs - Opens up the FAQ", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
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
                faqCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
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

    def settings():
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
               
                    gearScroll = tk.Scrollbar(gearMaster, command=gearCanvas.yview)
                    gearCanvas.configure(yscrollcommand=gearScroll.set)

                    gearSettings = gearCanvas.create_window((0, 0), window=gearMaster)

                    gearMaster.bind("<Configure>", canvasConfig)
                    gearCanvas.bind("<Configure>", canvasResize)
                    gearCanvas.bind_all("<MouseWheel>", mouseScroll)

                    gearTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC1)
                    gearTitle = tk.Label(gearTF, text="SETTINGS", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))
                    closeGear = tk.Button(gearTF, text="RETURN", command=setClose, width=10, height=0, bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))

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

                    winStateTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    winStateFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)

                    winStateLabel = tk.Label(winStateTF, text="DISPLAY", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    winStateDescLabel = tk.Label(winStateTF, text="Modify the display mode of the App", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))

                    # Toggle borderless / fullscreen
                    fullscreen_button = tk.Button(winStateFrame, text="Fullscreen", command=lambda:toggleWindowState("fullscreen"), width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    borderless_button = tk.Button(winStateFrame, text="Borderless Windowed", command=lambda:toggleWindowState("borderless"), width=20, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))
                    windowed_button = tk.Button(winStateFrame, text="Windowed", command=lambda:toggleWindowState("windowed"), width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))

                    #gearScroll.pack(side="right", fill="y")
                    gearTF.pack(side="top", anchor="nw", fill="x")
                    gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
                    debugFrame.pack(anchor="w", fill="x")

                    winStateTF.pack(side="top", anchor="nw", fill="x")
                    winStateFrame.pack(anchor="w", fill="x")
            
                    closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
                    generalUI.button_hover(closeGear,ui_AH1, ui_AC1)

                    debugLabel.pack(padx=10, pady=5, anchor="nw")
                    debugDescLabel.pack(padx=10, pady=2, anchor="nw")
                    
                    winStateLabel.pack(padx=10, pady=5, anchor="nw")
                    winStateDescLabel.pack(padx=10, pady=2, anchor="nw")

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

                    fullscreen_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(fullscreen_button, ui_AH1, ui_AC1)

                    borderless_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(borderless_button, ui_AH1, ui_AC1)

                    windowed_button.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(windowed_button, ui_AH1, ui_AC1)

                    gearAct = True
                    onceMade_Settings = True
                else:
                    gearCanvas.place(relx=0.02, rely=0.02, relheight=0.95, relwidth=0.95)
                    gearAct = True
                    canvasResize(root.winfo_width())
            else:
                setClose()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open up Settings: {e}")

# Sets the base path to the scripts. Currently os.getcwd() since it returns the current directory the code is in without the hardcoding issue
base_path = os.getcwd()

# Version Number 
versionNum = "1.48"

# For tracking UI activity and subprocesses
tut_count = 0
gearAct = False
tutAct = False
faqAct = False
quitAct = False
onceMade_Quit = False
onceMade_Settings = False
onceMade_Tut = False
filter = ""

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
gesturesList = open(f"{base_path}\\resources\\gesturesList.txt", "r")
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
uiMiscFrame = tk.Frame(root, padx=5, pady=5, bg=ui_AC1)
uiDynamFrame = tk.Frame(root, padx=5, pady=5, bg=ui_AC1)

# Tabs for the UI Frame, opens up game menu as the default
uiDynamTabs = {
    "Game": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=ui_AC1),
    "Profiles": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=ui_AC1),
    "Gestures": tk.Frame(uiDynamFrame, padx=5, pady=5, bg=ui_AC1)
}
gameTabFunc.run_gameMenu()

# Game Tab - Opens up a specific game & displays its desc. Has a button that transfers to profile
menuGameTabBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC2)
menuGameTab = tk.Button(menuGameTabBorder, text="GAMES", command=gameTabFunc.run_gameMenu, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
gameMasterFrame = tk.Frame(uiDynamTabs["Game"], background=ui_AC1)
gamesDisplay = tk.Canvas(uiDynamTabs["Game"], background=ui_AC1, highlightthickness=0)
gameDisplay = tk.Canvas(uiDynamTabs["Game"], background=ui_AC1, highlightthickness=0)

# Initialises the game tab
gameTabFunc(gamesDisplay)

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
gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")

generalUI.button_hover(gameSearchButton,ui_AH1, ui_AC2)
generalUI.button_hover(gameResetSearch,ui_AH1, ui_AC2)

# Profile Tab - Displays the gestures mapped to a game. Has buttons that transfers to that gesture
menuProfileTabBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC2)
menuProfileTab = tk.Button(menuProfileTabBorder, text="PROFILES", command=profileTabFunc.run_profileMenu, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

profileMasterFrame = tk.Frame(uiDynamTabs["Profiles"], background=ui_AC1)
profilesDisplay = tk.Canvas(uiDynamTabs["Profiles"], background=ui_AC1, highlightthickness=0)
profileDisplay = tk.Canvas(uiDynamTabs["Profiles"], background=ui_AC1, highlightthickness=0)

profile_SearchBorder = tk.Frame(profileMasterFrame, background=ui_AH1)
profile_ResetBorder = tk.Frame(profileMasterFrame, background=ui_AH1)
profileLabel = tk.Label(profileMasterFrame, text="PROFILES", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
profileSearchBar = tk.Entry(profileMasterFrame, bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 10))
profileSearchButton= tk.Button(profile_SearchBorder, text="Search", command=profileTabFunc.filterProfile, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))
profileResetSearch= tk.Button(profile_ResetBorder, text="Reset Search", command=profileTabFunc.resetFilter, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))

generalUI.button_hover(profileSearchButton,ui_AH1, ui_AC2)
generalUI.button_hover(profileResetSearch,ui_AH1, ui_AC2)

# Gestures Tab - Displays the gestures that are mapped. Has buttons that transfers or re-do that gesture
menuGestureTabBorder = tk.Frame(uiMasterFrame, pady=1, bg=ui_AC2)
menuGestureTab = tk.Button(menuGestureTabBorder, text="GESTURES", command=gestureTabFunc.run_gestureMenu, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

gestureMasterFrame = tk.Frame(uiDynamTabs["Gestures"], background=ui_AC1)
gesturesDisplay = tk.Canvas(uiDynamTabs["Gestures"], background=ui_AC1, highlightthickness=0)
gestureDisplay = tk.Frame(uiDynamTabs["Gestures"], background=ui_AC1)

gesture_SearchBorder = tk.Frame(gestureMasterFrame, background=ui_AH1)
gesture_ResetBorder = tk.Frame(gestureMasterFrame, background=ui_AH1)
gestureLabel = tk.Label(gestureMasterFrame, text="AVAILABLE GESTURES", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
gestureSearchBar = tk.Entry(gestureMasterFrame, bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 10))
gestureSearchButton= tk.Button(gesture_SearchBorder, text="Search", command=gestureTabFunc.filterGesture, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))
gestureResetSearch= tk.Button(gesture_ResetBorder, text="Reset Search", command=gestureTabFunc.resetFilter, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 11, ui_Bold))

generalUI.button_hover(gestureSearchButton,ui_AH1, ui_AC2)
generalUI.button_hover(gestureResetSearch,ui_AH1, ui_AC2)

# GUI Labels
TKlabel = tk.Label(uiMasterFrame, text=f"PROTOTYPE {versionNum}", anchor="ne", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))

# Button to display a tutorial window/widget
tutorial_button = tk.Button(uiMasterFrame, text="HELP", command=run.tutorial, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
generalUI.button_hover(tutorial_button, ui_AH1, ui_AC1)

# Miscellaneous UI Buttons
settings_Img = PhotoImage(file = base_path + "\\img\\settings.png")
scaled_SettingsImg = settings_Img.subsample(2, 2)
settings_button = tk.Button(uiMasterFrame, image=scaled_SettingsImg, command=run.settings, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0)
faq_button = tk.Button(uiMasterFrame, text="FAQs", command=run.faq, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

# Exit button
exit_button = tk.Button(uiMasterFrame, text="QUIT", command=quit.exit_program , width=10, height=2, bg=ui_AC1, fg=ui_Txt,activebackground=ui_AH1, border=0, font=(ui_Font, 10))

# GUI Layout and Labels
uiMasterFrame.pack(side="top", fill="x")
TKlabel.pack(pady=5, anchor="nw")

# Menu Tabs Layout
menuGameTabBorder.pack(side="left", anchor="w")
menuGameTab.pack(padx= 2, pady=2, side="left", anchor="w")
generalUI.button_hover(menuGameTab, ui_AH1, ui_AC1)

menuProfileTabBorder.pack(side="left", anchor="w")
menuProfileTab.pack(padx= 2, pady=2, side="left", anchor="w")
generalUI.button_hover(menuProfileTab, ui_AH1, ui_AC1)

menuGestureTabBorder.pack(side="left", anchor="w")
menuGestureTab.pack(padx= 2, pady=2, side="left", anchor="w")
generalUI.button_hover(menuGestureTab, ui_AH1, ui_AC1)

settings_button.pack(padx=50, pady=5, side="right", anchor="ne")
generalUI.button_hover(settings_button, ui_AH1, ui_AC1)

# Transfer to settings maybe, figure out a way to make UI pop in and out
uiMiscFrame.pack(side="top", fill="x")
tutorial_button.pack(padx=5, pady=5, side="left", anchor="nw")

faq_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(faq_button, ui_AH1, ui_AC1)

exit_button.pack(padx=5, pady=5, side="left", anchor="nw")
generalUI.button_hover(exit_button, ui_AE, ui_AC1)

uiDynamFrame.pack(side="top", fill="x")

# Global Canvases
quitCan = tk.Canvas(root, width=400, height=300, bg=ui_AC2, highlightthickness=0)
tutCanvas = tk.Canvas(root, width=400, height=300, bg=ui_AC2, highlightthickness=0)
faqCanvas = tk.Canvas(root, width=400, height=300, bg=ui_AC3, highlightthickness=0)
gearCanvas = tk.Canvas(root, bg=ui_AC3, highlightthickness=0)

# Run the tkinter event loop
root.mainloop()