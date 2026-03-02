import sys, shutil, os, random, time

kernel_running: bool = False

class Kernel:
    def __init__(self) -> None:
        self._version_info: str = "PY-DOS 1.6.1 prerelease 4"
        self._path: list = ["/", "c"]
        self._debug_mode: bool = False

    def update_state(self, name: str, bugcheck_text: str = "") -> int:
        # Updates ONLY debug_mode and ended
        if name == "debug":
            self._debug_mode = not self._debug_mode
            return 0
        elif name == "bugcheck":
            print(f"The system ran into an error it could not have recovered from. Error code: {bugcheck_text}")
            time.sleep(10)
            sys.exit(0)
        else:
            return 1

    def update_path(self, new_path: str) -> int:
        # Will update the path to the given new path
        # Returns 0 if successful, 1 if _path is already at root, 2 if new_path is invalid

        if new_path == "..":
            if self._path[0] == "/":
                return 1

            split_path = self._path[0].split("/")
            split_path.pop()
            self._path[0] = "/".join(split_path)

            return 0

        elif new_path == "/":
            self._path[0] = "/"
            return 0
        elif "/" in new_path:
            pass
        elif "/" not in new_path:
            if self._path[0] == "/":
                self._path[0] += new_path
                return 0

            self._path[0] += "/" + new_path
            return 0
        else:
            return 2

    def get_info(self, name) -> str | int | list | bool:
        if name == "ver":
            return self._version_info
        elif name == "path":
            return self._path
        elif name == "debug":
            return self._debug_mode
        else:
            return -1

def start_kernel():
    global kernel_running, kernel
    kernel_running = True
    kernel = Kernel()


class Shell:
    def __init__(self) -> None:
        self._dos_prompt: str = "C:\\> "
        self._echo_state: bool = True

    def _build_prompt(self) -> None:
        current_path = kernel.get_info("path")
        split_path = current_path[0].split("/")
        if len(split_path) > 0:
            self.dos_prompt = "C:" + "\\".join(split_path) + "> "
        else:
            self.dos_prompt = "C:\\> "

    def echo(self, text: list) -> None:
        if text:
            if text[0] == "on":
                self._echo_state = True
            elif text[0] == "off":
                self._echo_state = False
            else:
                text = " ".join(text)
                print(text)
        else:
            if self._echo_state:
                print("Echo is ON")
            else:
                print("Echo is OFF")

    def clear_screen(self, args):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        else:
            for i in range(0, 50):
                print("\n")

    def version(self, args) -> None:
        print(kernel.get_info("ver"))

    def help_command(self, args):
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

    def stop(self, args):
        # Eventually here goes any logic that saves the current state of the program
        return 9

# A class to be able to have more than one drive mounted
class FileSystem:
    def __init__(self):
        self.file_system: dict = {}
        # Make a serial number for volume
        self.serial_no_list: list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 9):
            self.serial_no_list[i] = random.randint(0, 9)
        self.serial_no_list[4] = "-"
        for i in range(0, 9):
            self.serial_no_list[i] = str(self.serial_no_list[i])
        self.serial_no = "" + "".join(self.serial_no_list)

    def initializer(self, fs: dict) -> None:
        # A function to load custom file systems
        self.file_system = fs

    def get_current_folder(self, path_to_use: str) -> dict:
        split_path = path_to_use.split("/")
        current_folder = self.file_system

        for part in split_path:
            if part:
                current_folder = current_folder["folders"][part]

        return current_folder

    def check_folder_existence(self, dest_path: list | str, absolute_path: bool):
        if absolute_path:
            current_folder = self.get_current_folder("/")
            for part in dest_path:
                if part in current_folder["folders"]:
                    current_folder = current_folder["folders"][part]
                else:
                    return False
            return True
        current_folder = self.get_current_folder(kernel.get_info("path")[0])
        if dest_path in current_folder["folders"]:
            return True
        else:
            return False

    def dir_command(self, args: list) -> None:
        # Lists all files in a folder
        print(f"""Volume in drive C is DOS 
Volume Serial Number is {self.serial_no}
Directory of {dos_prompt.strip("> ")} 
    
. <DIR>
.. <DIR>""")
        try:
            switch = args[0]
        except IndexError:
            print("NO SWITCH") if debug_mode else None
            switch = ""

        current_folder: dict = self.get_current_folder(kernel.get_info("path")[0])
        folder_count: int = 0
        file_count: int = 0

        if switch == "/p":
            line_count = shutil.get_terminal_size((80, 20)).lines - 3
            i = 6 # 6 because the header takes 6 lines
            for folder in current_folder["folders"]:
                print(folder + " <DIR>")
                folder_count+=1
                i+=1
                if i == line_count:
                    print("Press any key to continue...")
                    getchar()
                    i = 0
            for file in current_folder["files"]:
                print(file)
                file_count+=1
                i+=1
                if i == line_count:
                    print("Press any key to continue...")
                    getchar()
                    i = 0
        else:
            for folder in current_folder["folders"]:
                print(folder.upper() + " <DIR>")
                folder_count+=1
            for file in current_folder["files"]:
                print(file.upper())
                file_count+=1
        print(f"""    {file_count} File(s)
    {folder_count} Folder(s)""")


    def make_directory(self, args):
        pass


    def change_directory(self, args):
        dest = args[0]

        if dest == "/" or dest == "\\":
            kernel.update_path("/")
            #dos_prompt = f"{path[1].upper()}:\\> "
        elif dest == "..":
            if kernel.get_info("path")[0] == "/":
                return
            kernel.update_path("..")
                #dos_prompt = f"{path[1].upper()}:\\" + "\\".join(split_path) + "> "

        elif dest == ".":
            return
        else:
            current_folder = self.get_current_folder(kernel.get_info("path")[0])
            if dest.startswith("c:\\"):
                split_dest = dest.split("\\")
                split_dest.pop(0)
                if not self.check_folder_existence(split_dest, True):
                    print(f"Invalid directory - {dest}")
                    return
                
                kernel.update_path("/" + "/".join(split_dest))
                #dos_prompt = ("C:\\" + "\\".join(split_dest) + "> ").upper()
                return
            
            if self.check_folder_existence(dest, False):
                #print(kernel.get_info("path")) if debug_mode else None
                kernel.update_path(dest)
                #print(kernel.get_info("path")) if debug_mode else None
                #dos_prompt = (dos_prompt.strip("\\> ") + "\\" + dest + "> ").upper()
                return

            print(f"Invalid directory - {dest}")

            
    def rmdir(self, args):
        # Only for folders
        try:
            folder_to_remove = args[0]
        except IndexError:
            print("Invalid syntax")
            return
        try:
            switch = args[1]
        except IndexError:
            switch = ""
        
        if folder_to_remove.startswith(f"{kernel.get_info("path")[1]}:\\"):
            # If folder_to_remove is an absolute path
            folder_to_remove_split = folder_to_remove.split("\\")
            folder_to_remove_split.pop(0)
            path_of_folder = ("/" + "/".join(folder_to_remove_split))

            if self.check_folder_existence(folder_to_remove_split, True):
                current_folder = self.get_current_folder(path_of_folder)
                
                # Check if folder is empty
                if not current_folder["folders"][folder_to_remove_split[-1]] and switch != "/s":
                    print("Folder is not empty - use /s to force delete")
                    return
                current_folder["folders"].pop(folder_to_remove_split[-1], None)
                return
            
            print("Folder doesn't exist")
            return

        # Else folder_to_remove is a relative path
        current_folder = self.get_current_folder(kernel.get_info("path")[0])
        if folder_to_remove in current_folder["folders"]:
            current_folder["folders"].pop(folder_to_remove, None)
            return
        
        # Else the folder doesn't exist, so throw an error
        print(f"Folder doesn't exist")
        return
        

    def del_command(self, args):
        # Only for files
        file_to_remove = args[0]
    

cdrive = FileSystem()
cdrive.initializer({
    "folders": {
        "dos": {
            "folders": {
                "aaaa": {
                    "folders": {},
                    "files": [],
                }
            },
            "files": sorted([
                "ATTRIB.EXE", "CHKDSK.EXE", "COUNTRY.SYS", "COUNTRY.TXT", "DEBUG.EXE", "DOSSETUP.INI", "DRVSPACE.BIN",
                "EDIT.COM", "EXPAND.EXE", "FDISK.EXE", "FORMAT.COM", "KEYB.COM", "KEYBOARD.SYS", "MEM.EXE",
                "NLSFUNC.EXE", "README.TXT", "NETWORKS.TXT", "QBASIC.EXE", "REPLACE.EXE", "RESTORE.EXE", "SCANDISK.EXE",
                "SCANDISK.INI", "SETUP.EXE", "SYS.COM", "XCOPY.EXE", "DEFRAG.EXE", "DEFRAG.HLP", "EGA.CPI", "EGA2.CPI",
                "EGA3.CPI", "EMM386.EXE", "ISO.CPI", "KEYBRD2.SYS", "MSCDEX.EXE", "ANSI.SYS", "APPEND.EXE",
                "CHKSTATE.SYS", "CHOICE.COM", "DBLWIN.HLP", "DELTREE.EXE", "DISKCOMP.COM", "DISKCOPY.COM", "DISPLAY.SYS",
                "DOSHELP.HLP", "DOSKEY.COM", "DRVSPACE.EXE", "DRVSPACE.HLP", "DRVSPACE.INF", "DRVSPACE.SYS",
                "DRVSPACE.TXT", "MSD.EXE", "VFINTD.386", "DRIVER.SYS", "EDIT.HLP", "FASTHELP.EXE", "FASTOPEN.EXE",
                "FC.EXE", "FIND.EXE", "GRAPHICS.COM", "GRAPHICS.PRO", "HELP.COM", "HELP.HLP", "HIMEM.SYS", "INTERLNK.EXE",
                "INTERSVR.EXE", "LABEL.EXE", "LOADFIX.COM", "MEMMAKER.EXE", "MEMMAKER.HLP", "MEMMAKER.INF", "MODE.COM",
                "MONOUMB.386", "MORE.COM", "MOVE.EXE", "MSBACKUP.EXE", "MSBCONFG.HLP", "MSBCONFG.OVL", "MSTOOLS.DLL",
                "MWBACKR.DLL", "POWER.EXE", "PRINT.EXE", "QBASIC.HLP", "RAMDRIVE.SYS", "SETVER.EXE","SHARE.EXE",
                "SIZER.EXE", "SMARTDRV.EXE", "SMARTMON.EXE", "SMARTMON.HLP", "SORT.EXE", "SUBST.EXE", "TREE.COM",
                "UNFORMAT.COM", "MSBACKUP.HLP", "MSBACKUP.OVL", "MSAV.EXE", "MSAV.HLP", "MSAVHELP.OVL", "MSAVIRUS.LST",
                "MSBACKDB.OVL", "MSBACKDR.OVL", "MSBACKFB.OVL", "MSBACKFR.OVL", "MWAV.EXE", "MWAV.HLP", "MWAVABSI.DLL",
                "MWAVDLG.DLL", "MWAVDOSL.DLL", "MWAVDRVL.DLL", "MWAVMGR.DLL", "MWAVSCAN.DLL", "MWAVSOS.DLL",
                "MWAVTSR.EXE", "MWBACKF.DLL", "MWBACKUP.EXE", "MWBACKUP.HLP", "MWGRAFIC.DLL", "MWUNDEL.EXE",
                "MWUNDEL.HLP", "UNDELETE.EXE", "VSAFE.COM", "WNTOOLS.GRP", "COMMAND.COM"
            ]),
        },
        "scripts": {
            "folders": {},
            "files": sorted([
                "example.pds",
            ]),
        }
    },
    "files": sorted([
        "IO.SYS", "MSDOS.SYS", "MS-DOS_6", "COMMAND.COM", "WINA20.386", "CONFIG.SYS", "AUTOEXEC.BAT",
    ])
})

def clear(args):
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    else:
        print("Unsupported operating system")

def stop(args) -> None:
    global ended
    ended = True

def echo(message):
    global echo_state
    if message:
        if message[0] == "on":
            echo_state = True
        elif message[0] == "off":
            echo_state = False
        else:
            message = " ".join(message)
            print(message)
    else:
        if echo_state:
            print("Echo is ON")
        else:
            print("Echo is OFF")

def debug(args):
    global debug_mode
    debug_mode = not debug_mode

def ver(args):
    print(version_info)

def help_command(args):
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

ddrive = FileSystem()
ddrive.initializer({
    "folders": {},
    "files": [],
})

mounted_drives = {
    "c": cdrive,
    "d": ddrive
}

def cd_help(args):
    mounted_drives[path[1]].change_directory(args)

def dir_help(args):
    mounted_drives[path[1]].dir_command(args)

def mkdir_help(args):
    mounted_drives[path[1]].make_directory(args)

def del_help(args):
    mounted_drives[path[1]].del_command(args)

def rmdir_help(args):
    mounted_drives[path[1]].rmdir(args)


commands: dict = {
    "cd": cd_help,
    "dir": dir_help,
    "exit": stop,
    "cls": clear,
    "echo": echo,
    "mkdir": mkdir_help,
    "md": mkdir_help,
    "devmode": debug,
    "del": del_help,
    "rmdir": rmdir_help,
    "help": help_command,
    "ver": ver,
}

def command_parser_and_execute(user_input: str) -> None:
    global dos_prompt
    user_input_list = user_input.lower().strip().split()
    try:
        if user_input_list[0] in commands:
            print(f"CALLING: {user_input_list[0]}, ARGS: {user_input_list[1:]}") if debug_mode else None
            commands[user_input_list[0]](user_input_list[1:])
        elif user_input_list[0].strip(":") in mounted_drives:
            path[1] = user_input_list[0].strip(":")
            dos_prompt = f"{user_input_list[0].upper()}\\> "
        else:
            print(f'Bad command or filename - "{user_input_list[0]}"')
    except IndexError:
        return

def run_on_start() -> None:
    start_kernel()

    global current_drive
    current_drive = path[1]
    global getchar
    # Define the getchar function. If on Windows, just use msvcrt, if on Linux/macOS/Android, define my own
    try:
        import msvcrt
        getchar = msvcrt.getch # type: ignore[attr-defined]
    except ImportError:
        import tty
        import termios

        def getchar():
            ch = ""
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch



    # Startup message, the lines must not be indented because otherwise they won't be displayed properly
    print(f"""{version_info}
Copyright (C) 2025        All rights reserved

Initializing HIMEM.sys...
Invalid HIMEM.sys file

No CD-ROM support""")


def main() -> None:
    global current_drive
    while True:
        command_parser_and_execute(input(dos_prompt) if echo_state else input())
        if ended:
            break
        current_drive = path[1]



if __name__ == "__main__":
    run_on_start()
    main()