import shutil
from random import randint
from time import sleep
from sys import exit, stdin
from os import name, system, path
from hashlib import sha256
from json import load, dump

# ========= Classes ========
# ====== Exception classes =====
class InvalidFileSystemStructure(Exception):
    def __init__(self, message="Invalid file system structure"):
        super().__init__(message)




# ===== Core classes =====
class FileSystem:
    def __init__(self):
        self._folder_structure: dict = {}
        self._drive_label: str = ""
        self._drive_letter: str = ""

    def package_state(self) -> dict:
        state = {
            "letter": self._drive_letter,
            "fs": self._folder_structure,
            "label": self._drive_label
        }

        return state

    def initialize_file_system(self, fs):
        # Make a drive label
        drive_label_list: list[str] = []
        for i in range(0, 9):   # Generate a random drive label
            drive_label_list.append(str(randint(0, 9)))
        drive_label_list[4] = "-"
        for i in range(0, 9):   # Turn the numbers into strings
            drive_label_list[i] = str(drive_label_list[i])
        self._drive_label: str = "".join(drive_label_list)

        # Check fs for correct structure and assign fs to folder_structure
        def _validate_folder(folder):
            """
            Recursively checks a folder dictionary.
            Every folder must have:
                - "files": list
                - "folders": dict
            """
            if not isinstance(folder, dict):
                    raise InvalidFileSystemStructure("101")

            elif "files" not in folder or "folders" not in folder:
                raise InvalidFileSystemStructure("102")

            elif not isinstance(folder["files"], list):
                raise InvalidFileSystemStructure("103")

            elif not isinstance(folder["folders"], dict):
                raise InvalidFileSystemStructure("104")

            # Recurse into subfolders
            for subfolder_name, subfolder in folder["folders"].items():
                _validate_folder(subfolder)

        _validate_folder(fs)

        self._folder_structure: dict = fs
    def get_current_folder(self, path_to_use: str):
        # Will return a dict of the current folder
        if path_to_use == "/":
            return self._folder_structure

        split_path = path_to_use.split("/")
        current_folder = self._folder_structure

        for part in split_path:
            if part:
                current_folder = current_folder["folders"][part]

        return current_folder

    def change_directory(self, args: list[str], current_path: str) -> dict:
        try:
            new_path: str = args[0]
        except IndexError:
            return {"command": "cd", "exitcode": "invalidsyntax", "newpath": current_path}

        if new_path == "/":
            return {"command": "cd", "exitcode": "succesful", "newpath": "/"}
        elif new_path == ".." and current_path != "/":
            split_path: list[str] = current_path.split("/")
            split_path.pop()
            return {"command": "cd","exitcode": "succesful",
                   "newpath": ("/".join(split_path)) if len(split_path) > 1 else ("/" + "/".join(split_path))}
        elif new_path == ".":
            return {"command": "cd", "exitcode": "succesful", "newpath": current_path}
        else:
            current_folder = self.get_current_folder(current_path)
            if new_path in current_folder["folders"]:
                return {"command": "cd", "exitcode": "succesful", "newpath": (current_path + "/" + new_path)
                if current_path != "/" else (current_path + new_path)}
            else:
                return {"command": "cd", "exitcode": "invalidsyntax", "newpath": current_path}

    def dir_command(self, current_path: str) -> dict:
        # Will return a list of all items in the current folder

        current_folder = self.get_current_folder(current_path)

        folders = list(current_folder["folders"].keys())
        files = current_folder["files"]

        return_value = {
            "command": "dir",
            "files": files,
            "folders": folders,
            "label": self._drive_label,
            "exitcode": "succesful"
        }
        return return_value

    def make_directory(self, args: list[str], current_path):

        try:
            folder_name_or_path: str = args[0]
        except IndexError:
            return {"command": "mkdir", "exitcode": "invalidsyntax"}

        if folder_name_or_path.startswith("c:\\"):
            # Absolute path
            return {"command": "mkdir", "exitcode": "invalidsyntax"} # For now
        else:
            # Relative path
            current_folder: dict = self.get_current_folder(current_path)
            if folder_name_or_path not in current_folder["folders"]:
                # Folder doesnt exist
                current_folder["folders"][folder_name_or_path] = {
                    "folders": {},
                    "files": [],
                }
                return {"command": "mkdir", "exitcode": "succesful"}
            else:
                # Folder exists
                return {"command": "mkdir", "exitcode": "folderalreadyexists"}

    def remove_directory_or_file(self, args: list[str], current_path):
        try:
            file_or_folder_to_delete: str = args[0]
        except IndexError:
            return {"command": "rm", "exitcode": "invalidsyntax"}

        if file_or_folder_to_delete.startswith("C:\\"):
            # Absolute path
            return {"command": "rm", "exitcode": "invalidsyntax"} # For now
        else:
            # Relative path
            current_folder: dict = self.get_current_folder(current_path)

            if file_or_folder_to_delete in current_folder["folders"]:
                current_folder["folders"].pop(file_or_folder_to_delete)
            elif file_or_folder_to_delete in current_folder["files"]:
                for i in range(0, len(current_folder["files"])):
                    # Get the index of the item so it can be popped
                    if current_folder["files"][i] == file_or_folder_to_delete:
                        current_folder["files"].pop(i)
                        break
            else:
                return {"command": "rm", "exitcode": "filefolderdoesntexist"}
            return {"command": "rm", "exitcode": "succesful"}



class UserAccount:
    def __init__(self):
        self._user_name: str = ""
        self._role: str = "normal"
        self._password: str = ""

    def package_state(self) -> dict:
        # No need for bugcheck because either way all of it is going to be saved
        state = {
            "user_name": self._user_name,
            "role": self._role,
            "password": self._password
        }

        return state

    def whoami(self):
        return self._user_name

    def initialize_user(self, args: list[str], role_of_current_user: str):
        try:
            name: str = args[0]
            password: str = args[1]
            role: str = args[2]
        except IndexError:
            return {"command": "create_user", "exitcode": "invalidsyntax"}

        if role not in ["admin", "normal"]:
            return {"command": "create_user", "exitcode": "unsupportedrole"}

        if role_of_current_user != "admin" and role == "admin":
            return {"command": "create_user", "exitcode": "notenoughprivileges"}

        self._user_name = name
        self._password = sha256(password.encode()).hexdigest()
        self._role = role

        return {"command": "create_user", "exitcode": "succesful"}

    def get_role(self):
        return self._role

    def check_password(self, password_to_check: str) -> bool:
        if not isinstance(password_to_check, str):
            return False

        hashed_password = sha256(password_to_check.encode()).hexdigest()
        if hashed_password == self._password:
            return True

        return False

    def change_password(self, new_password: str):
        if not isinstance(new_password, str):
            return {"command": "changepassword", "exitcode": "invalidsyntax"}

        self._password = sha256(new_password.encode()).hexdigest()
        return {"command": "changepassword", "exitcode": "succesful"}



class Kernel:
    def __init__(self):
        self._path: str = "/"
        self._working_drive: str = "c"
        self._mounted_drives: dict = {
            "c": FileSystem(),
        }
        self._current_user: str = "root"
        self._users: dict = {
            "admin": UserAccount(),
        }
        self._users["admin"].initialize_user(["admin", "root", "admin"], "admin")
        self.shell = Shell(self)
        self.on_login: bool = True

    def package_state(self, bugcheck: bool) -> dict:
        if bugcheck:
            state: dict = {
                "path": self._path,
                "working_drive": self._working_drive,
                "current_user": self._current_user,
            }
        else:
            state: dict = {
                "working_drive": self._working_drive,
            }

        return state

    def on_boot(self):
        self.mount_drive("c", {
            "folders": {
                "docs": {
                    "folders": {
                        "important": {
                            "folders": {

                            },
                            "files": []
                        }
            },
                "files": ["readme.txt", "test.txt"]}
            },
            "files": ["autoexec.bat", "config.sys"]
        })

        if path.exists("state.json"):
            self.load_state_from_json()
        self.login_screen()

    def login_screen(self):
        # Is shown at the start, or after typing 'logout' into the shell. Basically its own small shell
        while self.on_login == True:
            user: str = input("Enter user name: ")
            password: str = input("Enter password: ")

            try:
                if self._users[user].check_password(password):
                    #on_login = False
                    self._current_user = user
                    self.shell.on_start()
                    self.shell.command_loop()
                    self.save_state_to_json()

                else:
                    print("Invalid password")
            except KeyError:
                print("Invalid user")

    def create_user(self, args: list[str]):
        if args[0] not in self._users:
            self._users[args[0]] = UserAccount()
            current_role: str = self._users[self._current_user].get_role()
            return_value: dict = self._users[args[0]].initialize_user(args, current_role)
            if return_value["exitcode"] == "notenoughprivileges":
                self._users.pop(args[0])
            return return_value

        return {"command": "createuser", "exitcode": "userexists"}


    def command_resolver(self, split_user_input: list[str]):
        # Will resolve non-shell commands like CD, DIR, ...
        try:
            if split_user_input[0] == "dir":
                return self._mounted_drives[self._working_drive].dir_command(self._path)
            elif split_user_input[0] == "cd":
                result = self._mounted_drives[self._working_drive].change_directory(split_user_input[1:], self._path)

                self.update_path(result["newpath"])
                return result

            elif split_user_input[0] == "createuser":
                return self.create_user(split_user_input[1:])
            elif split_user_input[0] == "mkdir" or split_user_input[0] == "md":
                return self._mounted_drives[self._working_drive].make_directory(split_user_input[1:], self._path)
            elif split_user_input[0] == "rm" or split_user_input[0] == "del":
                return self._mounted_drives[self._working_drive].remove_directory_or_file(split_user_input[1:],
                                                                                          self._path)
            elif split_user_input[0] == "changepassword":
                return self._users[self._current_user].change_password(split_user_input[1])
            elif split_user_input[0] == "state":
                if len(split_user_input) == 2:
                    self.save_state_to_json() if split_user_input[1] == "save" else None
                    self.load_state_from_json() if split_user_input[1] == "load" else None
                else:
                    return {"command": "state", "exitcode": "invalidsyntax"}
            elif split_user_input[0] == "shutdown":
                self.shutdown()
            else:
                return {"command": "invalid"}
        except IndexError:
            return {"command": "createuser", "exitcode": "invalidsyntax"}

    def shutdown(self):
        self.save_state_to_json()
        self.on_login = False
        self.shell._is_running = False


    def mount_drive(self, drive_letter: str, fs: dict):
        # Will mount the drive
        self._mounted_drives[drive_letter] = FileSystem()
        try:
            self._mounted_drives[drive_letter].initialize_file_system(fs)
            self._mounted_drives[drive_letter]._drive_letter = drive_letter
        except InvalidFileSystemStructure as e:
            e = e.args[0]
            if e == "101":
                self.bug_check(101, "INVALID_FS-TYPE")
            elif e == "102":
                self.bug_check(102, "INVALID_FS-KEYS")
            elif e == "103":
                self.bug_check(103, "INVALID_FI_TYPE")
            elif e == "104":
                self.bug_check(104, "INVALID_FO_TYPE")
            else:
                self.bug_check(100, "INVALID_FILE_SYSTEM_STRUCTURE")

    def bug_check(self, exit_code: int, exit_code_for_print: str):
        # Kind of like a BSOD or kernel panic
        # Here goes any code that saves the state (currently none)
        self.save_state_to_json(True)
        print(f"The system ran into an error it could not recover from\nEXIT CODE: {exit_code_for_print}")
        sleep(10)
        exit(exit_code)

    def update_path(self, new_path: str):
        self._path = new_path

    def save_state_to_json(self, bugcheck=False):
        # Get all states
        shell = self.shell.package_state(bugcheck)
        accounts = []
        for account in self._users:
            accounts.append(self._users[account].package_state())
        drives = []
        for drive in self._mounted_drives:
            drives.append(self._mounted_drives[drive].package_state())
        kernel = self.package_state(bugcheck)

        # Put all states inside one dict
        full_state = {
            "bugcheck": bugcheck,
            "accounts": accounts,
            "drives": drives,
            "kernel": kernel,
        }

        with open("state.json", "w") as f:
            dump(full_state, f, indent=4)


    def load_state_from_json(self):
        with open("state.json", "r") as f:
            state = load(f)

        # Bring back the accounts
        self._users = {}
        for account in state["accounts"]:
            self._users[account["user_name"]] = UserAccount()
            self._users[account["user_name"]]._user_name = account["user_name"]
            self._users[account["user_name"]]._password = account["password"]
            self._users[account["user_name"]]._role = account["role"]

        # Bring back the drives
        self._mounted_drives = {}
        for drive in state["drives"]:
            self._mounted_drives[drive["letter"]] = FileSystem()
            self._mounted_drives[drive["letter"]].initialize_file_system(drive["fs"])
            self._mounted_drives[drive["letter"]]._drive_label = drive["label"]
            self._mounted_drives[drive["letter"]]._drive_letter = drive["letter"]

        self._working_drive = state["kernel"]["working_drive"]

        if state["bugcheck"]:
            self._path = state["kernel"]["path"]
            self._current_user = state["kernel"]["current_user"]

class Shell:
    def __init__(self, kernel):
        self.kernel = kernel
        self._dos_prompt: str = "C:\\> "
        self._version_info: str = "PY-DOS 1.4.1 alpha"
        self._shell_commands: dict= {
            "ver": self.version,
            "help": self.help,
            "echo": self.echo,
            "cls": self.clear_screen,
            "logoff": self.logoff,
        }
        self._is_running: bool = True
        self.echo_state: bool = True

    # ======= Functions =======
    # ===== Methods ===== (mostly dependent on kernel)
    def package_state(self, bugcheck: bool):
        if bugcheck is True:
            state: dict = {
            "dos_prompt": self._dos_prompt,
            "version_info": self._version_info,
            "is_running": self._is_running,
            "echo_state": self.echo_state,
        }
        else:
            state: dict = {
                "is_running": self._is_running,
                "echo_state": self.echo_state,
            }
        return state

    def parser_and_dispatcher(self, user_input: str):
        # Parses user input and calls functions accordingly
        split_input = user_input.lower().split()
        if len(split_input) > 0:        # Ignore empty input
            if split_input[0] == "trigger_bug_check":   # Debug case
                self.kernel.bug_check(20, "BUG_CHECK_ON_COMMAND")
            elif split_input[0] in self._shell_commands:    # Check if command is owned by Shell
                self._shell_commands[split_input[0]](split_input[1:])
            else:       # Pass the command to the kernel
                result = self.kernel.command_resolver(split_input)   # Pass the input to the kernel

                if result is not None and isinstance(result, dict):      # If kernel returned something
                    if result["command"] == "dir":      # If the command was dir
                        print(f"""Volume in drive C is DOS 
Volume Serial Number is {result["label"]}
Directory of {self._dos_prompt.strip("> ")} 
    
. <DIR>
.. <DIR>""")
                        counter = [2, 0]        # [0] for folders, [1] for files
                        for folder in result["folders"]:      # Go through all folders, print them with <DIR>, and
                                                                # increase the counter
                            print(folder.upper(), " <DIR>")
                            counter[0] += 1
                        for file in result["files"]:      # Go through all files, print them and increase the counter
                            print(file.upper())
                            counter[1] += 1
                        print(f"    Files: {counter[1]}\n    Folders: {counter[0]}")    # Print the count
                    elif result["command"] == "cd":
                        # Handle cd separately because it needs to update dos prompt
                        print("Invalid syntax") if result["exitcode"] == "invalidsyntax" else None
                        self.update_dos_prompt(result["newpath"])
                    elif result["exitcode"] == "invalidsyntax":
                        print("Invalid syntax")
                    elif result["exitcode"] == "notenoughprivileges":
                        print("Only admin users can create new admin users")
                    elif result["exitcode"] == "userexists":
                        print("User already exists")
                    elif result["exitcode"] == "folderalreadyexists":
                        print("Folder already exists")
                    elif result["exitcode"] == "filefolderdoesntexist":
                        print("File or folder doesnt exist")


    def command_loop(self):
        self._is_running = True
        while self._is_running:
            user_input = input(self._dos_prompt if self.echo_state else "")
            self.parser_and_dispatcher(user_input)

    def update_dos_prompt(self, new_path: str):
        self._dos_prompt = "C:" + "\\".join(new_path.upper().split("/")) + "> "

    def getchar(self):
        # Used for /p in dir - to be added
        if name == "nt":
            import msvcrt
            self.getchar = msvcrt.getch()
        elif name == "posix":
            import tty
            import termios
            ch = ""
            fd = stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

    # ===== Shell commands ===== (not dependent on kernel)
    def logoff(self, args):
        # Here goes any code that saves the current state of the simulator (currently none)

        self.clear_screen([])
        self._is_running = False

    def clear_screen(self, args):
        # Clears the screen while paying attention to os.name
        if name == "nt":
            system("cls")
        elif name == "posix":
            system("clear")
        else:
            for i in range(0, 100):
                print("\n")

    def echo(self, args: list):
        # Repeats the string provided by user, prints echo state if no string provided
        if len(args) == 0:      # If no arguments are provided
            print("Echo is ON") if self.echo_state else print("Echo is OFF")
        elif args[0] == "on":
            self.echo_state = True
        elif args[0] == "off":
            self.echo_state = False
        else:
            print(" ".join(args))

    def help(self, args: list):
        # Prints all available commands with short explanations
        if len(args) == 0:
            print("""
    (DDA) = Detailed Description Available
help - Shows this message
ver - Shows the version
echo - Prints the text after the command (DDA)
logoff - Logs out of the current session
createuser - Creates a new user account (DDA)
dir - Lists folders and files inside the working directory (DDA)
cd - Change the working directory (DDA)
mkdir - Makes a new folder in the working directory (DDA)
rm - Deletes a file or a folder in the working directory (DDA)
del - Same as rm
changepassword - Changes the password of the current user (DDA)
""")
        else:
            name = args[0]  # No need for a try:...except here because the upper branch will execute if there are no args
            if name == "createuser":
                print("""
createuser
Usage and meaning:
    createuser will create a new user account. 
    Every account can either be: admin or normal.
    Every account MUST HAVE a password.
    Only admin users can create new admin accounts.
    
    createuser newuser 1234 normal
Syntax:
    createuser username password type
""")
            elif name == "dir":
                print("""
dir
Usage and meaning:
    dir will list all files and folders in the current working directory
    
    dir
Syntax:
    dir
""")
            elif name == "cd":
                print("""
cd
Usage and meaning:
    cd will change the current working directory
    Supported arguments:
        '..' - goes to the parent directory
        '/' - goes to the root
        '.' - stays in the current directory
        PATH - name of a directory in the working directory
Syntax:
    cd ARGUMENT
    """)
            elif name == "echo":
                print("""
echo
Usage and meaning:
    echo will print any text after the command to the shell
    Supported arguments:
        on - turns echo on
        off - turns echo off
        MESSAGE - the text that is printed to the shell
Syntax:
    echo ARGUMENT
    """)
            elif name == "mkdir":
                print("""
mkdir
Usage and meaning:
    mkdir will create a new folder in the working directory 
    Supported arguments:
        NAME - name of the folder
        
Syntax:
    mkdir NAME""")
            elif name == "rm" or name == "del":
                print("""
rmdir
Usage and meaning:
    rmdir will delete a file or folder in the working directory 
    Supported arguments:
        NAME - name of the folder
Syntax:
    rmdir NAME""")
            elif name == "changepassword":
                print("""
changepassword
Usage and meaning:
    changepassword changes the password of the current user
    Supported arguments:
        NEW_PASSWORD - the new password
Syntax:
    changepassword NEW_PASSWORD""")

    def version(self, args):
        # Prints the version
        print(f"\n{self._version_info}\n")

    def on_start(self):
        # Prints starting message
        self.clear_screen([])
        print(f"""{self._version_info}

Copyright (C) 2026      All rights reserved
""")


def main():
    kernel = Kernel()
    kernel.on_boot()

if __name__ == "__main__":
    main()