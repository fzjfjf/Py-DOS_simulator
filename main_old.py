import msvcrt
import shutil
import os

# file structure stored in a variable
ROOT = sorted(["DOS <DIR>", "IO.SYS", "MSDOS.SYS", "MS-DOS_6", "COMMAND.COM", "WINA20.386", "CONFIG.SYS", "AUTOEXEC.BAT"])
DOS = sorted(["AAAA <DIR>", "ATTRIB.EXE", "CHKDSK.EXE", "COUNTRY.SYS", "COUNTRY.TXT", "DEBUG.EXE", "DOSSETUP.INI", "DRVSPACE.BIN", "EDIT.COM", "EXPAND.EXE", "FDISK.EXE", "FORMAT.COM", "KEYB.COM", "KEYBOARD.SYS", "MEM.EXE", "NLSFUNC.EXE", "README.TXT", "NETWORKS.TXT", "QBASIC.EXE", "REPLACE.EXE", "RESTORE.EXE", "SCANDISK.EXE", "SCANDISK.INI", "SETUP.EXE", "SYS.COM", "XCOPY.EXE", "DEFRAG.EXE", "DEFRAG.HLP", "EGA.CPI", "EGA2.CPI", "EGA3.CPI", "EMM386.EXE", "ISO.CPI", "KEYBRD2.SYS", "MSCDEX.EXE", "ANSI.SYS", "APPEND.EXE", "CHKSTATE.SYS", "CHOICE.COM", "DBLWIN.HLP", "DELTREE.EXE", "DISKCOMP.COM", "DISKCOPY.COM", "DISPLAY.SYS", "DOSHELP.HLP", "DOSKEY.COM", "DRVSPACE.EXE", "DRVSPACE.HLP", "DRVSPACE.INF", "DRVSPACE.SYS", "DRVSPACE.TXT", "MSD.EXE", "VFINTD.386", "DRIVER.SYS", "EDIT.HLP", "FASTHELP.EXE", "FASTOPEN.EXE", "FC.EXE", "FIND.EXE", "GRAPHICS.COM", "GRAPHICS.PRO", "HELP.COM", "HELP.HLP", "HIMEM.SYS", "INTERLNK.EXE", "INTERSVR.EXE", "LABEL.EXE", "LOADFIX.COM", "MEMMAKER.EXE", "MEMMAKER.HLP", "MEMMAKER.INF", "MODE.COM", "MONOUMB.386", "MORE.COM", "MOVE.EXE", "MSBACKUP.EXE", "MSBCONFG.HLP", "MSBCONFG.OVL", "MSTOOLS.DLL", "MWBACKR.DLL",  "POWER.EXE", "PRINT.EXE", "QBASIC.HLP", "RAMDRIVE.SYS", "SETVER.EXE", "SHARE.EXE", "SIZER.EXE", "SMARTDRV.EXE", "SMARTMON.EXE", "SMARTMON.HLP", "SORT.EXE", "SUBST.EXE", "TREE.COM", "UNFORMAT.COM", "MSBACKUP.HLP", "MSBACKUP.OVL", "MSAV.EXE", "MSAV.HLP", "MSAVHELP.OVL", "MSAVIRUS.LST", "MSBACKDB.OVL", "MSBACKDR.OVL", "MSBACKFB.OVL", "MSBACKFR.OVL", "MWAV.EXE", "MWAV.HLP", "MWAVABSI.DLL", "MWAVDLG.DLL", "MWAVDOSL.DLL", "MWAVDRVL.DLL", "MWAVMGR.DLL", "MWAVSCAN.DLL", "MWAVSOS.DLL", "MWAVTSR.EXE", "MWBACKF.DLL", "MWBACKUP.EXE", "MWBACKUP.HLP", "MWGRAFIC.DLL", "MWUNDEL.EXE", "MWUNDEL.HLP", "UNDELETE.EXE", "VSAFE.COM", "WNTOOLS.GRP", "COMMAND.COM"])
AAAA = sorted(["SECRET.TXT", "AAAB <DIR>",])
AAAB = sorted(["HELLO.TXT", "HI.TXT"])

existingDicts: dict = {
    "dos": DOS,
    "aaaa": AAAA,
    "/": ROOT,
    "aaab": AAAB,
}

#to store all error messages in one place, easier to manage later
errorMessages = {
    0: "The system couldn't find the file specified.",
    1: "The directory already exists",
    2: "The syntax of the command is incorrect.",
    3: "Access denied",
    4: "The directory doesn't exist",
    5: "The system cannot find the path specified",
    6: "File does not exist",
}

#variables we need
versionInfo = "PY-DOS Version 1.5.1"
counter = 0
folder = "/"
dos_prompt = r"C:\> "
listInUse = ROOT
debugMode = False
echoState = True

#syncs dosPrompt and listInUse to align with folder
def syncStates():
    global dos_prompt, listInUse
    print("ENTERED SYNCSTATES") if debugMode else None #for debugging purposes
    if folder == "/":
        #easiest to hardcore root bc it has to be here
        dos_prompt = r"C:\> "
        listInUse = existingDicts["/"]
    else:
        print("ELSE") if debugMode else None #debugging purposes
        splitFolder = folder.split("/")
        listInUse = existingDicts[splitFolder[len(splitFolder) - 2]] #we needed to split Folder earlier so we can assign a list here
                                                                     #subtracted by two to get of the empty string at the end and last folder
        print(listInUse) if debugMode else None #debugging purposes
        i = 0
        while i <= len(splitFolder):  # a while loop to remove the empty elements
            if splitFolder[i] == "":
                splitFolder.pop(i)
            i += 1
        i = 0
        dos_prompt = "C:"  #set up dosPrompt for reconstructing
        while i < len(splitFolder):   #another while loop to reconstruct dosPrompt
            dos_prompt = dos_prompt + "\\" + splitFolder[i].upper()
            print(dos_prompt) if debugMode else None #debugging purposes
            i+=1
        dos_prompt = dos_prompt + "\\> " #add the end part of dos prompt
        print(dos_prompt) if debugMode else None #yet again, debugging purposes

#deletes a file
def  delCommand():
    try: #to catch user not putting in a file name
        i = 0
        while i < len(listInUse): #to iterate through the list to get index for pop()
            if listInUse[i].lower() == ui[1]: #check to see if file is in the list
                listInUse.pop(i)
                return #end the loop NOW so the print doesnt get triggered
            i+=1 #dont forget to increment
        print(errorMessages[0])
    except IndexError:
        print(errorMessages[0])

#makes a new directory
def mkdir():
    global listInUse, existingDicts
    try:
        if ui[1] in existingDicts and ui[1].upper() in listInUse: #check to see if directory exists
            print(errorMessages[1])
            return
        else:
            listInUse.append((ui[1].upper() + " <DIR>")) #make a new element in the current list
            existingDicts[ui[1]] = [] #make a new dict element (key is ui[1] and the other is an empty list)
    except IndexError:
        print(errorMessages[2])

#removes a directory
def rmdir():
    print(ui) if debugMode else None #debugging purposes
    global existingDicts
    try:
        var1 = (ui[1] + " <dir>") #prepare the user input for checking
        print(var1) if debugMode else None #debugging purposes
        if ui[1] == "dos":                  #first check for dos folder and root, those have to always exist
            print(errorMessages[3])
        elif ui[1] == "/" or ui[1] == "\\":
            print(errorMessages[3])
        elif ui[1] in existingDicts and var1.upper() in listInUse: #we need to make sure the directory exists
            print("EXISTS") if debugMode else None #debugging purposes
            existingDicts.pop(ui[1]) #delete the key in the dict so user cant access list, we aren't actually deleting the list
            i = 0
            while i < len(listInUse): #while loop to find and remove the directory from the current list
                if var1.upper() == listInUse[i]:
                    listInUse.pop(i)
                i+=1
            print(existingDicts) if debugMode else None #you know the drill, debugging purposes
        else:
            print(errorMessages[4])
    except IndexError:
        print(errorMessages[2])

#changes current directory
def cdCommand():
    global folder, dos_prompt, listInUse
    try: #try...except to catch IndexError, we don't need the program to crash, don't we?
        if ui[1] == "..":
            if folder != "/": #check to see if we are in the root, if we are it doesn't make sense to go back, right?
                splitFolder = folder.split("/") #split the folder so we can work on it easier
                print(splitFolder) if debugMode else None #debugging purposes
                i = 0
                while i <= len(splitFolder):    # a while loop to remove the empty elements
                    if splitFolder[i] == "":
                        splitFolder.pop(i)
                    i+=1
                splitFolder.pop()               #to remove the last element(folder we are currently going down from)
                print(splitFolder) if debugMode else None #debugging purposes
                i = 0
                folder = "" #prepare folder for rebuilding
                while i < len(splitFolder): #while loop to rebuild folder
                    folder = folder + "/" + splitFolder[i]
                    i+=1
                folder = folder + "/" #folder path always has a slash at the end
                syncStates() #run syncStates() to sync dosPrompt and listInUse
        elif ui[1] == "/?": #help, pretty self-explanatory
            print("""Help for cd command:
cd .. - goes to previous folder
cd folder_name - goes to the folder specified if the folder exists""")
        elif ui[1] == ".": #doesnt do anything
            pass
        elif ui[1] == "\\": #cd \ goes immideately to root, so we put all variables to starting states
            folder = "/"
            dos_prompt = "C:\\> "
            listInUse = ROOT
            return
        else: #if we passed every elif above, it means user provided a name of the directory to change to
            for name in listInUse: #iterate through all the elements
                try:
                    var = name.lower().split() #prepare for checking
                    if var[1] == "<dir>" and ui[1] == var[0]: #we need to check if the name user provided is a directory
                                                              #(all directories have <dir> next to them) and the name itself
                        folder = folder + ui[1] + "/" #adjust folder, dosPrompt and listInUse
                        dos_prompt = dos_prompt[:-2] + ui[1].upper() + r"\> "
                        listInUse = existingDicts[var[0]]
                        return
                except IndexError: #to catch if user didn't provide a directory name
                    pass
            print(errorMessages[5])
    except IndexError as e:
        print(errorMessages[5])
        print(e) if debugMode else None

#copies files from one place to another
def copy(xcopy):
    global listInUse, folder, existingDicts
    try: #to catch Index errors
        source = ui[1]
        dest = ui[2]
    except IndexError:
        print(errorMessages[2])
        return
    splitSource = source.strip().split("\\")
    splitDest = dest.strip().split("\\")
    if splitDest[len(splitDest) - 1] == "":
        splitDest.pop(len(splitDest) - 1)
    print(existingDicts[splitDest[len(splitDest) - 1].lower() if (splitDest[len(splitDest) - 1]) != "c:" else "/"]) if debugMode else None
    print(f"splitSource = {splitSource}, splitDest = {splitDest}") if debugMode else None
    try:
        if splitSource[len(splitSource) - 1].upper() in existingDicts[splitSource[len(splitSource) - 2] if (splitSource[len(splitSource) - 2]) != "c:" else "/"]:
        #we need to check if the file exists, it is the same as for checking to see if the file already exists in destination folder
        #we basically get the file name in uppercase first, then get the folder that the file is supposed to be in, also we need to make sure
        #that if the file is on the root (/) we assign it manually bc split() will give c:
        #in here: len(splitSource) - 1  (-1) is to get the index of file name, as it is last item
        #in here: len(splitSource) - 2  (-2) is to get the index of folder name, as it is second to last
            pass
        else:
            print(errorMessages[6])
            return #we have to return bc we want to end the function NOW, not after all code executed
    except KeyError:
        print(errorMessages[0])
        return
    try:
        if splitSource[len(splitSource) - 1].upper() in existingDicts[splitDest[len(splitDest) - 1] if (splitDest[len(splitDest) - 1]) != "c:" else "/"]:
        #im sorry for anyone trying to debug this crap, it basically checks if the file trying to be copied already exists
        #i could have put it in more lines, but i dont want to, also there is an explanation above that is similar
            ui1 = input("A file with this name already exists. Do you want to overwrite it? (y/n) ").lower()
            if ui1 == "n":
                print("Cancelled.")
                return
            elif ui1 == "y":
            #usually we would need to delete the file then copy over the other one but since we arent
            #dealing with actual files we dont even need to do anything
                localList = existingDicts[splitDest[len(splitDest) - 1] if (splitDest[len(splitDest) - 1]) != "c:" else "/"]
                print(localList) if debugMode else None
                print("Copy successful!")
        else:
            localList = existingDicts[splitDest[len(splitDest) - 1] if (splitDest[len(splitDest) - 1]) != "c:" else "/"]
            localList.append(splitSource[len(splitSource) - 1].upper())
            print(localList) if debugMode else None
            print("Copy successful!")
    except KeyError:
        print(errorMessages[2])
    if xcopy:
        try:
            localList = existingDicts[
            splitSource[len(splitSource) - 2].lower() if (splitSource[len(splitSource) - 2]) != "c:" else "/"]
        except KeyError:
            print(errorMessages[5])
        i = 0
        while i < len(localList):
            if splitSource[len(splitSource) - 1].upper() == localList[i].upper():
                localList.pop(i)
                break
            i += 1

#shows all files and folders in a list
def dirCommand():
    global counter, listInUse
    localList = sorted(listInUse) #listInUse may not be sorted so we sort it here
    print("")
    counter = 0 #keeps track of what line we are on, needed for /p
    try:
        if ui[1] == "/p": #a switch to show only a screenful each time
            maxHeight = shutil.get_terminal_size((80, 20)).lines - 3 #calculate maxheight by getting terminal size
            for file in localList: #we need to iterate over every item to print it outside of brackets and quotes
                print(file)
                counter += 1
                if counter == maxHeight:
                    print("Press any key to continue...")
                    msvcrt.getch() #waits for a keystroke before continuing
                    counter = 0 #set counter back to 0 so we can stop again
            return
    except IndexError:
        pass
    for file in localList:
        print(file)
    print("")

#echo command from dos
def echoCommand():
    global echoState
    try:
        if ui[1] == "on":
            echoState = True
        elif ui[1] == "off":
            echoState = False
        else:
            i = 0
            ui.pop(0)
            while i < len(ui):
                print(ui[i], end=" ")
                i+=1 #DONT FORGET
            print("")
    except IndexError:
        print("ECHO is " + str(echoState))

#print the version and other text that is always at the start in DOS
print(f"""
{versionInfo}
Copyright (C) 2025      All rights reserved

Initializing HIMEM.sys...
Invalid HIMEM.sys file

No CD-ROM support
No .exe support
No .bat support
No file handling support
No support
It's an emulator what do you expect?!
 """)

#command loop
while True:
    #for debugging purposes
    print(f"folder = {folder}") if debugMode else None
    print(f"listInUse = {listInUse}") if debugMode else None

    #basic input from user
    ui = input(dos_prompt if echoState == True else "").lower().strip().split()
    #a try...except to catch IndexError, e.g. user pressing enter without typing anything
    try:
        #an if statement that just calls functions defined before or does what the command would usually do
        #if it doesn't take much space
        if ui[0] == "exit":
            print("Why you want to exit? Well, it isn't my job to care so goodbye!")
            break
        elif ui[0] == "mkdir":
            mkdir()
        elif ui[0] == "dir":
            dirCommand()
        elif ui[0] == "cls":
            os.system("cls")
        elif ui[0] == "cd":
            cdCommand()
        elif ui[0] == "cd..":
            ui.append("..")
            cdCommand()
        elif ui[0] == "cd.":
            ui.append(".")
            cdCommand()
        elif ui[0] == "copy":
            copy(False)
        elif ui[0] == "del":
            delCommand()
        elif ui[0] == "xcopy" or ui[0] == "move":
            copy(True)
        elif ui[0] == "ver":
            print(f"""
{versionInfo}
        """)
        elif ui[0] == "help":
            print("""
EXIT - Shutdowns DOS
DIR - Displays all items in a directory
CD - Changes directory
VER - Shows version
HELP - Displays this message
CLS - Clears the screen
MKDIR - Makes a new directory with the name provided
RMDIR - Removes the directory if it exists
COPY - Copies one file from another, a full path from and to needed
DEL - Deletes a file specified in the same directory
ECHO - Outputs any text written after, or turns on and of echoing
XCOPY - Same as COPY, but deletes the source file
MOVE - Same as XCOPY
""")
#i know i said that this if is to call functions and only do commands that are short but i
# was lazy so i just put the entire help here
        elif ui[0] == "rmdir":
            rmdir()
        elif ui[0] == "developermodedebug":
            #for debugging purposes
            debugMode = not debugMode
            print("DEBUG ON") if debugMode else print("DEBUG OFF")
        elif ui[0] == "echo":
            echoCommand()
        else:
            print(f"{ui} is not recognized as the name of an internal, external command or a name of a file or a program")
    except IndexError as e:
        #the except IndexError statement i mentioned earlier
        pass    #dos just prints another dos prompt if enter is pressed
        print(e) if debugMode else None