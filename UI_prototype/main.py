# Main program for GUI interface
import subprocess
import os
import tkinter as tk
import psutil
from tkinter import PhotoImage, messagebox, filedialog

# Additonal imports
import pyautogui

class generalUI:
    def button_hover(tkb, b_Hover, b_Release ):
    # Changes the colour of the button whether if it hovers or not
        tkb.bind("<Enter>", func=lambda e: tkb.config(background=b_Hover))
        tkb.bind("<Leave>", func=lambda e: tkb.config(background=b_Release))

class gameTabFunc:
    # For Game Tab Functions
    # Maps the gamesDisplay frame for usage
    def __init__(self, gFrame):
        self.gFrame = gFrame
        gamesList = open('gamesList.txt', 'r')
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
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
        
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
            
                # Var checks
                """
                for gameItem in range(game_Count):
                    print(gameDisplayArray[gameItem])
                    print(descDisplayArray[gameItem])
                    print(thumbDisplayArray[gameItem])
                    print("\n \n")
                    pass 
                """
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

                #Var checks
                """
                for gameItem in range(game_Count):
                    print(gameDisplayArray[gameItem])
                    print(descDisplayArray[gameItem])
                    print(thumbDisplayArray[gameItem])
                    print("\n \n")
                    pass
                """

            # Closes the filestream for gamesList.txt
            gamesList.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")

    # Filters the output of gameDisplay
    def filterGame():
        global gamesList, gamesDisplay
        try:
            filter = gameSearchBar.get()
            if filter !="":
                gamesList = open('gamesList.txt', 'r')
                gameTabFunc.gameDisplay(gamesList, filter)
                gameTabFunc.id_Game(gamesDisplay)
                gameSearchBar.delete(0, 'end')
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
    
    # Resets the filters in filterGame
    def resetFilter():
        global gamesList, gamesDisplay
        try:
            filter = ""
            gamesList = open('gamesList.txt', 'r')
            gameTabFunc.gameDisplay(gamesList, filter)
            gameTabFunc.id_Game(gamesDisplay)
            gameSearchBar.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")

    # Displays that specific game
    def game_Describe(gameItem):
        
        global gamesDisplay, gameMasterFrame, gameDetails, gameDisplay
        # Goes back to the Games Tab
        def goBack():
            gameDisplay.pack_forget()
            gameTabFunc(gamesDisplay)
            gameMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
            gamesDisplay.pack(padx=10, pady=1, side="top", fill="x")
        
        # Goes to the respective profile's description in Profile Tab
        def goToProfile(profileItem):
            gameDisplay.pack_forget()
            profileTabFunc.run_profileMenu()
            profileTabFunc.profile_Describe(profileItem)

        # Experimental function to write to gamesList.txt
        def writeToFile():
            filepath_New = filedialog.askopenfilename(initialdir = "/", title = "Select a File",filetypes = (("Exe files","*.exe*"),("Text files","*.txt*")))

            # Formats the filepath to fit the gamesList format
            filepath_Change = f"ExeÃ· {gItemExt[0]}Ã· {filepath_New}"

            with open('gamesList.txt', "r") as txt:
                gameWrite = txt.readlines()

            filepath_Update = False
            with open('gamesList.txt', 'w') as txt:
                for line in gameWrite:
                    if not filepath_Update and gameDetails[3] in line:
                        txt.write(filepath_Change + "\n")
                        filepath_Update = True
                    else:
                        txt.write(line)

            # Changes the filepath in the game description
            gameItemFile.configure(text = filepath_New)

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
        
            # Displays the new items
            gameGet = open('gamesList.txt', 'r')
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

            # Prints out the game details
            """
            for i in range(len(gameDetails)):
                print(gameDetails[i] + "\n")
            """

            # Displays the selected game
            game_DisplayFrame = tk.Frame(gameDisplay, bg=ui_AC2)
            game_DisplayPicFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            game_InfoFrame = tk.Frame(game_DisplayFrame, bg=ui_AC2)
            gameItemLabel = tk.Label(gameDisplay, text=gameDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            backButton = tk.Button(gameDisplay, text="Go back", command=goBack, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
            gameLink = tk.Button(gameDisplay, text="Go to Profiles", command=lambda: goToProfile(gameDetails[0]), bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
     
            gameItemImg = PhotoImage(file = gameDetails[2]).subsample(1,1)
            gameImg = tk.Label(game_DisplayPicFrame, image=gameItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
            gameImg.image = gameItemImg

            s = tk.Scrollbar(root, orient='horizontal')

            gameItemTxt = tk.Text(game_DisplayFrame, width=65, height=5, xscrollcommand=s.set, wrap="word", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            gameItemTxt.insert(tk.END, gameDetails[1])
            gameItemTxt.configure(exportselection=0, state="disabled")  

            #gameItemTxt = tk.Label(game_DisplayFrame, text=gameDetails[1], wraplength=1250, height=5, justify="left", bg=ui_AC4, fg=ui_Txt, border=0, font=(ui_Font, 12))
            gameItemFileP = tk.Button(game_InfoFrame, text="Configure Filepath", command=writeToFile, bg=ui_AC1, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 12))
            gameItemFile = tk.Label(game_InfoFrame, text=gameDetails[3], wraplength=5000, height=1, justify="left", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 12))

            game_InfoFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayFrame.pack(padx=5, pady=5, side="bottom", fill="x")
            game_DisplayPicFrame.pack(padx=5, pady=5, side="left", fill="x")
            gameItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")

            backButton.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(backButton, ui_AH1, ui_AC1)

            gameLink.pack(padx=4, pady=4, side="left", anchor="w")
            generalUI.button_hover(gameLink, ui_AH1, ui_AC1)

            gameImg.pack(padx=4, pady=4, side="left", anchor="nw")
            gameItemTxt.pack(padx=4, pady=4, side="left", anchor="nw")

            gameItemFileP.pack(padx=4, pady=4, side="left", anchor="nw")
            generalUI.button_hover(gameItemFileP, ui_AH1, ui_AC1)
            gameItemFile.pack(padx=4, pady=4, side="left", anchor="nw")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display individual game: {e}")
      
class profileTabFunc:
    # For Profile Tab Functions
    # Maps the profilesDisplay frame for usage
    def __init__(self, pFrame):
        self.pFrame = pFrame
        profilesList = open('gamesList.txt', 'r')
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
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")
    
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
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
        
    # Gets the available games from gamesList.txt using filters from filterGame
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

            # Closes the filestream for gamesList.txt
            gamesList.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the profiles: {e}")

    # Filters the output of profilesDisplay
    def filterProfile():
        global gamesList, profilesDisplay
        try:
            filter = profileSearchBar.get()
            if filter !="":
                gamesList = open('gamesList.txt', 'r')
                profileTabFunc.profileDisplay(gamesList, filter)
                profileTabFunc.id_Profile(profilesDisplay)
                profileSearchBar.delete(0, 'end')
            else:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")
    
    # Resets the filters in filterProfiles
    def resetFilter():
        global gamesList, profilesDisplay
        try:
            filter = ""
            gamesList = open('gamesList.txt', 'r')
            profileTabFunc.profileDisplay(gamesList, filter)
            profileTabFunc.id_Profile(profilesDisplay)
            profileSearchBar.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter the games: {e}")

    # Displays that specific game
    def profile_Describe(profileItem):
        global profilesDisplay, profileMasterFrame, gameDetails, profileDisplay
        # Goes back to the Games Tab
        def goBack():
            profileDisplay.pack_forget()
            profileTabFunc(profilesDisplay)
            profileMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
            profilesDisplay.pack(padx=10, pady=1, side="top", fill="x")
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
            pItemExt = profileItem.split()
            #print(pItemExt[0])
        
            # Displays the new items
            itemGet = open('gamesList.txt', 'r')
            for line in itemGet:
                if f"GameÃ· {pItemExt[0]}" in line:
                    gameName = line.split("Ã· ")
                    profileDetails.append(gameName[2].replace("\n","'S PROFILE"))
            
                elif f"ThumbImgÃ· {pItemExt[0]}" in line:
                    gameThumb = line.split("Ã· ")
                    file = base_path + gameThumb[2].replace("\n","")
                    profileDetails.append(file)
                
                elif f"ExeÃ· {pItemExt[0]}" in line:
                    gameExe = line.split("Ã· ")
                    file = gameExe[2].replace("\n","")
                    profileDetails.append(file)
        
            profileIF = tk.Frame(profileDisplay, bg=ui_AC2)
            profileDF = tk.Frame(profileDisplay, bg=ui_AC2)
            profileItemLabel = tk.Label(profileDisplay, text=profileDetails[0], bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))

            profileItemImg = PhotoImage(file = profileDetails[1]).subsample(1,1)
            profileImg = tk.Label(profileDF, image=profileItemImg, bg=ui_AC1, fg=ui_Txt, border=0)
            profileImg.image = profileItemImg

            backButton = tk.Button(profileDisplay, text="Go back", command=goBack, bg=ui_AC2, fg=ui_Txt, border=0, activebackground=ui_AH1, font=(ui_Font, 15, ui_Bold))
        
            profileIF.pack(padx=5, pady=15, side="left", fill="x")
            profileDF.pack(padx=5, pady=15, side="bottom", fill="x")

            profileItemLabel.pack(padx=5, pady=5, side="top", anchor="nw")
            backButton.pack(padx=5, pady=5, side="top", anchor="nw")

            profileImg.pack(padx=5, pady=5, side="left")

            generalUI.button_hover(backButton, ui_AH1, ui_AC1)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"{e}")

class gestureTabFunc:
    # For Gesture Tab Functions
    # Maps the gesturesDisplay frame for usage
    def __init__(self, geFrame):
        self.geFrame = geFrame
        #profilesList = open('gesturesList.txt', 'r')
        #profileTabFunc.gestureDisplay(gesturesList, filter)
        #profileTabFunc.id_Gesture(gesturesDisplay)
        for uiBorder in uiMasterFrame.winfo_children():
            uiBorder.config(bg=ui_AC1)
            menuGestureTabBorder.config(bg=ui_AH1)

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
                gestureTabFunc(profilesDisplay)

                gestureMasterFrame.pack(padx=5, pady=15, side="top", fill="x")
                gestureLabel.pack(padx=10, pady=5, side="left")
                gesture_SearchBorder.pack(padx=5, pady=15, side="right", anchor="ne")
                gesture_ResetBorder.pack(padx=5, pady=15, side="right", anchor="ne")

                gestureResetSearch.pack(padx=2, pady=2, side="right")
                gestureSearchButton.pack(padx=2,pady=2, anchor="center")
                gestureSearchBar.pack(ipady=9.75, padx=1, pady=15, side="right", anchor="ne")   
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change active tab to Game Tab: {e}")
    
    def filterGesture():
        pass

    def resetFilter():
        pass 

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
                        tk.Label(tutFrame, text="GETTING STARTED", anchor="ne", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 25, ui_Bold)),
                        tk.Label(tutFrame, text="Games - Shows the available games for mapping ", anchor="e", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Profiles - Shows the profiles you made, contains the gestures you mapped for a game", anchor="e", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Gestures - Shows the gestures you made for mapping", anchor="e", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="Settings - Opens up the settings for you to fine tune", anchor="e", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                        tk.Label(tutFrame, text="FAQs - Opens up the FAQ", anchor="e", bg=ui_AC2, fg=ui_AH2, font=(ui_Font, 12, ui_Bold)),
                    ]
                   
                    tutFrame.pack(fill="x")
                   
                    for e in range(len(tutContent)):
                        tutItem = tutContent[e]
                        tutItem.pack(padx=5, pady=5, anchor="nw")
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
                with open('faq_text.txt', 'r') as txtfile:
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
            
            def canvasResize(e):
                if not isinstance(e, int):
                    gearCanvas.itemconfig(gearSettings, width=e.width)        
                else:
                    gearCanvas.itemconfig(gearSettings, width=e)
            
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
            
                    gearMaster = tk.Frame(gearCanvas, padx=5, pady=5, bg=ui_AC1)
               
                    gearScroll = tk.Scrollbar(gearMaster, command=gearCanvas.yview)
                    gearCanvas.configure(yscrollcommand=gearScroll.set)

                    gearSettings = gearCanvas.create_window((0, 0), window=gearMaster)

                    gearMaster.bind("<Configure>", canvasConfig)
                    gearCanvas.bind("<Configure>", canvasResize)
                    gearCanvas.bind_all("<MouseWheel>", mouseScroll)

                    gearTF = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC1)
                    debugFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC2)
                    testFrame = tk.Frame(gearMaster, padx=5, pady=5, bg=ui_AC4)
            
                    gearTitle = tk.Label(gearTF, text="SETTINGS", bg=ui_AC1, fg=ui_AH2, font=(ui_Font, 25, ui_Bold))
                    closeGear = tk.Button(gearTF, text="RETURN", command=setClose, width=10, height=0, bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 15, ui_Bold))

                    debugLabel = tk.Label(debugFrame, text="DEBUG", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    debugDescLabel = tk.Label(debugFrame, text="For devs to configure the controls", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 12))

                    button1 = tk.Button(debugFrame, text="Mouse", command=run.program1, width=10, height=2, bg=ui_AC2, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button2 = tk.Button(debugFrame, text="Two-handed Gesture", command=run.program2, width=20, height=2, bg=ui_AC2, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button3 = tk.Button(debugFrame, text="Swipe Motion Gesture", command=run.program3, width=20, height=2, bg=ui_AC2, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    button4 = tk.Button(debugFrame, text="Hybrid Gestures", command=run.program4, width=20, height=2, bg=ui_AC2, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))
                    
                    # Release control button
                    release_button = tk.Button(debugFrame, text="Reset Controls", command=quit.release_control, width=15, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH3, border=0, font=(ui_Font, 10))

                    #gearScroll.pack(side="right", fill="y")
                    gearTF.pack(side="top", anchor="nw", fill="x")
                    gearTitle.pack(padx=10, pady=10, side="left", anchor="nw")
                    debugFrame.pack(anchor="w", fill="x")
                    testFrame.pack(anchor="w", fill="both")
            
                    closeGear.pack(padx=30, pady=10, side="right", anchor="ne")
                    generalUI.button_hover(closeGear,ui_AH1, ui_AC1)

                    debugLabel.pack(padx=10, pady=5, anchor="nw")
                    debugDescLabel.pack(padx=10, pady=2, anchor="nw")

                    button1.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button1,ui_AH1, ui_AC1)

                    button2.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button2,ui_AH1, ui_AC1)

                    button3.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button3,ui_AH1, ui_AC1)

                    button4.pack(padx=5, pady=5, side="left", anchor="w")
                    generalUI.button_hover(button4,ui_AH1, ui_AC1)

                    release_button.pack(padx=5, pady=5, side="left", anchor="nw")
                    generalUI.button_hover(release_button, ui_AH3, ui_AC1)
                
                    """
                    # Scrollbar Tester
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    label = tk.Label(testFrame, text="Scrollbar Test", bg=ui_AC2, fg=ui_Txt, border=0, font=(ui_Font, 20, ui_Bold))
                    label.pack(padx=10, pady=2)
                    """
                    
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
#base_path = f"Filepath/Folder"
base_path = os.getcwd()

# Version Number 
versionNum = "1.45"

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

gameDisplayArray = []
descDisplayArray = []
thumbDisplayArray = []
exeDisplayArray = []
profileDisplayArray = []
gameDetails = []
profileDetails = []
gamesList = open('gamesList.txt', 'r')
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

# Gets the resolution for the default monitor
MaxRes = pyautogui.size()

# Initialize the tkinter root window
root = tk.Tk()
root.title(f"Handflux - GUI Prototype {versionNum}")
root.geometry('1280x720')
root.maxsize(MaxRes[0],MaxRes[1])
root.minsize(1280,720)
root.configure(background=ui_AC1)
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
gamesDisplay = tk.Frame(uiDynamTabs["Game"], background=ui_AC1)
gameDisplay = tk.Frame(uiDynamTabs["Game"], background=ui_AC1)

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
profilesDisplay = tk.Frame(uiDynamTabs["Profiles"], background=ui_AC1)
profileDisplay = tk.Frame(uiDynamTabs["Profiles"], background=ui_AC1)

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
gesturesDisplay = tk.Frame(uiDynamTabs["Gestures"], background=ui_AC1)
gestureDisplay = tk.Frame(uiDynamTabs["Gestures"], background=ui_AC1)

gesture_SearchBorder = tk.Frame(gestureMasterFrame, background=ui_AH1)
gesture_ResetBorder = tk.Frame(gestureMasterFrame, background=ui_AH1)
gestureLabel = tk.Label(gestureMasterFrame, text="GESTURES", bg=ui_AC1, fg=ui_Txt, font=(ui_Font, 15, ui_Bold))
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
settings_img = PhotoImage(file = base_path + "\\img\\settings.png")
scaled_settingsImg = settings_img.subsample(2, 2)
settings_button = tk.Button(uiMasterFrame, image=scaled_settingsImg, command=run.settings, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0)
faq_button = tk.Button(uiMasterFrame, text="FAQs", command=run.faq, width=10, height=2, bg=ui_AC1, fg=ui_Txt, activebackground=ui_AH1, border=0, font=(ui_Font, 10))

# Exit button - better implemented as image
exit_button = tk.Button(uiMasterFrame, text="EXIT", command=quit.exit_program ,width=10, height=2, bg=ui_AC1, fg=ui_Txt, border=0, font=(ui_Font, 10))

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