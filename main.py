import sys
import shutil
import os

# file structure stored in a variable
ROOT = sorted([
        "SCRIPTS <DIR>",
        "DOS <DIR>",
        "IO.SYS",
        "MSDOS.SYS",
        "MS-DOS_6",
        "COMMAND.COM",
        "WINA20.386",
        "CONFIG.SYS",
        "AUTOEXEC.BAT"])
DOS = sorted(["AAAA <DIR>", "ATTRIB.EXE", "CHKDSK.EXE", "COUNTRY.SYS", "COUNTRY.TXT", "DEBUG.EXE", "DOSSETUP.INI", "DRVSPACE.BIN", "EDIT.COM", "EXPAND.EXE",
              "FDISK.EXE", "FORMAT.COM", "KEYB.COM", "KEYBOARD.SYS", "MEM.EXE", "NLSFUNC.EXE", "README.TXT", "NETWORKS.TXT", "QBASIC.EXE", "REPLACE.EXE",
              "RESTORE.EXE", "SCANDISK.EXE", "SCANDISK.INI", "SETUP.EXE", "SYS.COM", "XCOPY.EXE", "DEFRAG.EXE", "DEFRAG.HLP", "EGA.CPI", "EGA2.CPI",
              "EGA3.CPI", "EMM386.EXE", "ISO.CPI", "KEYBRD2.SYS", "MSCDEX.EXE", "ANSI.SYS", "APPEND.EXE", "CHKSTATE.SYS", "CHOICE.COM", "DBLWIN.HLP",
              "DELTREE.EXE", "DISKCOMP.COM", "DISKCOPY.COM", "DISPLAY.SYS", "DOSHELP.HLP", "DOSKEY.COM", "DRVSPACE.EXE", "DRVSPACE.HLP", "DRVSPACE.INF",
              "DRVSPACE.SYS", "DRVSPACE.TXT", "MSD.EXE", "VFINTD.386", "DRIVER.SYS", "EDIT.HLP", "FASTHELP.EXE", "FASTOPEN.EXE", "FC.EXE", "FIND.EXE",
              "GRAPHICS.COM", "GRAPHICS.PRO", "HELP.COM", "HELP.HLP", "HIMEM.SYS", "INTERLNK.EXE", "INTERSVR.EXE", "LABEL.EXE", "LOADFIX.COM", "MEMMAKER.EXE",
              "MEMMAKER.HLP", "MEMMAKER.INF", "MODE.COM", "MONOUMB.386", "MORE.COM", "MOVE.EXE", "MSBACKUP.EXE", "MSBCONFG.HLP", "MSBCONFG.OVL",
              "MSTOOLS.DLL", "MWBACKR.DLL", "POWER.EXE", "PRINT.EXE", "QBASIC.HLP", "RAMDRIVE.SYS", "SETVER.EXE","SHARE.EXE", "SIZER.EXE", "SMARTDRV.EXE",
              "SMARTMON.EXE", "SMARTMON.HLP", "SORT.EXE", "SUBST.EXE", "TREE.COM", "UNFORMAT.COM", "MSBACKUP.HLP", "MSBACKUP.OVL", "MSAV.EXE", "MSAV.HLP",
              "MSAVHELP.OVL", "MSAVIRUS.LST", "MSBACKDB.OVL", "MSBACKDR.OVL", "MSBACKFB.OVL", "MSBACKFR.OVL", "MWAV.EXE", "MWAV.HLP", "MWAVABSI.DLL", 
              "MWAVDLG.DLL", "MWAVDOSL.DLL", "MWAVDRVL.DLL", "MWAVMGR.DLL", "MWAVSCAN.DLL", "MWAVSOS.DLL", "MWAVTSR.EXE", "MWBACKF.DLL", "MWBACKUP.EXE",
              "MWBACKUP.HLP", "MWGRAFIC.DLL", "MWUNDEL.EXE", "MWUNDEL.HLP", "UNDELETE.EXE", "VSAFE.COM", "WNTOOLS.GRP","COMMAND.COM"])
AAAA = sorted(["SECRET.TXT", "AAAB <DIR>"])
AAAB = sorted(["HELLO.TXT", "HI.TXT"])

existingDicts = {
    "dos": DOS,
    "aaaa": AAAA,
    "/": ROOT,
    "aaab": AAAB,
    "scripts": ["example.pds"], 
}

errorMessages = {
    "FileNotFound": "The system couldn't find the file specified.",
    "DirectoryExists": "The directory already exists",
    "IncorrectSyntax": "The syntax of the command is incorrect.",
    "AccessDenied": "Access denied",
    "DirectoryNotFound": "The directory doesn't exist",
    "PathNotFound": "The system cannot find the path specified",
    "FileDoesntExist": "File does not exist",
}

versionInfo = "PY-DOS Version 1.5.1"
counter = 0
folder = "/"
dos_prompt = r"C:\> "
listInUse = ROOT
debugMode = False
echoState = True
var1 = False

try:
    import msvcrt
    getchar = msvcrt.getch
except ImportError:
    import tty
    import termios

    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def script_parser(script_name):
    global ui
    for i in range(0, len(listInUse)):
        if script_name[0] not in listInUse[i]:
            print(f"{ui} is not recognized as the name of an internal, external command or a name of a file or a program")
            return
    try:
        with open(script_name[0], "r", newline=None) as script:
            script_contents = script.readlines()
    except FileNotFoundError:
        print(f"{ui} is not recognized as the name of an internal, external command or a name of a file or a program")
        return
    for line in script_contents:
        print(line) if debugMode else None  # <--- debug statement restored
        if line.startswith("#"):
            pass
        else:
            ui = line.lower().strip().split()
            execute_commands(ui)


def execute_commands(ui):
    global var1, debugMode
    var1 = False
    try:
        if ui[0] == "exit":
            var1 = True
        elif ui[0] == "mkdir":
            mkdir()
        elif ui[0] == "dir":
            dirCommand()
        elif ui[0] == "cls":
            os.system("cls") if os.name == "nt" else os.system("clear")
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
        elif ui[0] == "rmdir":
            rmdir()
        elif ui[0] == "developermodedebug":
            debugMode = not debugMode
            print("DEBUG ON") if debugMode else print("DEBUG OFF")
        elif ui[0] == "echo":
            echoCommand()
        else:
            script_parser(ui)
    except IndexError as e:
        pass
        print(e) if debugMode else None


def syncStates():
    global dos_prompt, listInUse
    print("ENTERED SYNCSTATES") if debugMode else None  # <--- debug statement restored
    if folder == "/":
        dos_prompt = r"C:\> "
        listInUse = existingDicts["/"]
    else:
        print("ELSE") if debugMode else None  # <--- debug statement restored
        splitFolder = folder.split("/")
        listInUse = existingDicts[splitFolder[len(splitFolder) - 2]]
        print(listInUse) if debugMode else None  # <--- debug statement restored
        i = 0
        while i <= len(splitFolder):
            if splitFolder[i] == "":
                splitFolder.pop(i)
            i += 1
        i = 0
        dos_prompt = "C:"
        while i < len(splitFolder):
            dos_prompt = dos_prompt + "\\" + splitFolder[i].upper()
            print(dos_prompt) if debugMode else None  # <--- debug statement restored
            i += 1
        dos_prompt = dos_prompt + "\\> "
        print(dos_prompt) if debugMode else None  # <--- debug statement restored


def delCommand():
    try:
        i = 0
        while i < len(listInUse):
            if listInUse[i].lower() == ui[1]:
                listInUse.pop(i)
                return
            i += 1
        print(errorMessages["FileNotFound"])
    except IndexError:
        print(errorMessages["FileNotFound"])


def mkdir():
    global listInUse, existingDicts
    try:
        if ui[1] in existingDicts and ui[1].upper() in listInUse:
            print(errorMessages["DirectoryExists"])
            return
        else:
            listInUse.append(ui[1].upper() + " <DIR>")
            existingDicts[ui[1]] = []
    except IndexError:
        print(errorMessages["IncorrectSyntax"])


def rmdir():
    global existingDicts
    print(ui) if debugMode else None  # <--- debug statement restored
    try:
        var1 = ui[1] + " <dir>"
        print(var1) if debugMode else None  # <--- debug statement restored
        if ui[1] == "dos":
            print(errorMessages["AccessDenied"])
        elif ui[1] == "/" or ui[1] == "\\":
            print(errorMessages["AccessDenied"])
        elif ui[1] in existingDicts and var1.upper() in listInUse:
            print("EXISTS") if debugMode else None  # <--- debug statement restored
            existingDicts.pop(ui[1])
            i = 0
            while i < len(listInUse):
                if var1.upper() == listInUse[i]:
                    listInUse.pop(i)
                i += 1
            print(existingDicts) if debugMode else None  # <--- debug statement restored
        else:
            print(errorMessages["DirectoryNotFound"])
    except IndexError:
        print(errorMessages["IncorrectSyntax"])


def cdCommand():
    global folder, dos_prompt, listInUse
    try:
        if ui[1] == "..":
            if folder != "/":
                splitFolder = folder.split("/")
                print(splitFolder) if debugMode else None  # <--- debug statement restored
                i = 0
                while i <= len(splitFolder):
                    if splitFolder[i] == "":
                        splitFolder.pop(i)
                    i += 1
                splitFolder.pop()
                print(splitFolder) if debugMode else None  # <--- debug statement restored
                i = 0
                folder = ""
                while i < len(splitFolder):
                    folder = folder + "/" + splitFolder[i]
                    i += 1
                folder = folder + "/"
                syncStates()
        elif ui[1] == "/?":
            print("""Help for cd command:
cd .. - goes to previous folder
cd folder_name - goes to the folder specified if the folder exists""")
        elif ui[1] == ".":
            pass
        elif ui[1] == "\\":
            folder = "/"
            dos_prompt = "C:\\> "
            listInUse = ROOT
            return
        else:
            for name in listInUse:
                try:
                    var = name.lower().split()
                    if var[1] == "<dir>" and ui[1] == var[0]:
                        folder = folder + ui[1] + "/"
                        dos_prompt = dos_prompt[:-2] + ui[1].upper() + r"\> "
                        listInUse = existingDicts[var[0]]
                        return
                except IndexError:
                    pass
            print(errorMessages["PathNotFound"])
    except IndexError as e:
        print(errorMessages["PathNotFound"])
        print(e) if debugMode else None


def copy(xcopy):
    global listInUse, folder, existingDicts
    try:
        source = ui[1]
        dest = ui[2]
    except IndexError:
        print(errorMessages["IncorrectSyntax"])
        return

    splitSource = source.strip().split("\\")
    splitDest = dest.strip().split("\\")
    print(f"splitSource = {splitSource}, splitDest = {splitDest}") if debugMode else None  # <--- debug restored

    if splitDest[-1] == "":
        splitDest.pop(-1)

    try:
        if (splitSource[-1].upper() not in existingDicts[(
            splitSource[-2] if splitSource[-2] != "c:" else "/")]
        ):
            print(errorMessages["FileDoesntExist"])
            return
    except KeyError:
        print(errorMessages["FileNotFound"])
        return

    try:
        localList = existingDicts[(splitDest[-1] if splitDest[-1] != "c:" else "/")]
        print(localList) if debugMode else None  # <--- debug restored

        if splitSource[-1].upper() in localList:
            ui1 = input(
                "A file with this name already exists. Do you want to overwrite it? (y/n) "
            ).lower()
            if ui1 == "n":
                print("Cancelled.")
                return
        else:
            localList.append(splitSource[-1].upper())
        print("Copy successful!")
    except KeyError:
        print(errorMessages["IncorrectSyntax"])

    if xcopy:
        try:
            localList = existingDicts[(splitSource[-2].lower() if splitSource[-2] != "c:" else "/")]
            for i in range(len(localList)):
                if splitSource[-1].upper() == localList[i].upper():
                    localList.pop(i)
                    break
        except KeyError:
            print(errorMessages["PathNotFound"])


def dirCommand():
    global counter, listInUse
    localList = sorted(listInUse)
    print("")
    counter = 0
    try:
        if ui[1] == "/p":
            maxHeight = shutil.get_terminal_size((80, 20)).lines - 3
            for file in localList:
                print(file)
                counter += 1
                if counter == maxHeight:
                    print("Press any key to continue...")
                    getchar()
                    counter = 0
            return
    except IndexError:
        pass

    for file in localList:
        print(file)
    print("")


def echoCommand():
    global echoState
    try:
        if ui[1] == "on":
            echoState = True
        elif ui[1] == "off":
            echoState = False
        else:
            ui.pop(0)
            length_of_input = len(ui)
            for i in range(length_of_input):
                print(ui[i], end=" ")
            print("")
    except IndexError as e:
        print(e) if debugMode else None
        print("ECHO is OFF") if not echoState else print("ECHO is ON")


print(f"""
{versionInfo}
Copyright (C) 2025        All rights reserved

Initializing HIMEM.sys...
Invalid HIMEM.sys file

No CD-ROM support
""")

while True:
    print(f"folder = {folder}") if debugMode else None  # <--- debug restored
    print(f"listInUse = {listInUse}") if debugMode else None  # <--- debug restored
    ui = input(dos_prompt if echoState else "").lower().strip().split()
    execute_commands(ui)
    if var1:
        break

