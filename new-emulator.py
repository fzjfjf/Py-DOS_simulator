import shutil, json
from random import randint
from time import sleep
from sys import exit, stdin
from os import name, system
from hashlib import sha256

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
            "label": self._drive_label
        }
        return return_value

    def make_directory(self, args: list[str]):
        pass

    def remove_directory_or_file(self):
        pass


class UserAccount:
    def __init__(self):
        self._user_name: str = ""
        self._role: str = "normal"
        self._password: str = ""

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

        self.login_screen()

    def login_screen(self):
        # Is shown at the start, or after typing 'logout' into the shell. Basically its own small shell
        while True:
            user: str = input("Enter user name: ")
            password: str = input("Enter password: ")

            try:
                if self._users[user].check_password(password):
                    self._current_user = user
                    self.shell.on_start()
                    self.shell.command_loop()
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
            else:
                return {"command": "invalid"}
        except IndexError:
            return {"command": "createuser", "exitcode": "invalidsyntax"}

    def mount_drive(self, drive_letter: str, fs: dict):
        # Will mount the drive
        self._mounted_drives[drive_letter] = FileSystem()
        try:
            self._mounted_drives[drive_letter].initialize_file_system(fs)
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

    def update_path(self, new_path: str):
        self._path = new_path

    def bug_check(self, exit_code: int, exit_code_for_print: str):
        # Kind of like a BSOD or kernel panic
        # Here goes any code that saves the state (currently none)

        print(f"The system ran into an error it could not recover from\nEXIT CODE: {exit_code_for_print}")
        sleep(10)
        exit(exit_code)

    def save_state_to_json(self):
        pass

    def load_state_from_json(self):
        pass

class Shell:
    def __init__(self, kernel):
        self.kernel = kernel
        self._dos_prompt: str = "C:\\> "
        self._version_info: str = "PY-DOS 1.4.0 alpha"
        self._shell_commands: dict= {
            "ver": self.version,
            "help": self.help,
            "echo": self.echo,
            "cls": self.clear_screen,
            "logoff": self.logoff,
        }
        self._is_running: bool = True
        self.echo_state: bool = True

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
                            print(folder, " <DIR>")
                            counter[0] += 1
                        for file in result["files"]:      # Go through all files, print them and increase the counter
                            print(file)
                            counter[1] += 1
                        print(f"Files: {counter[1]}\nFolders: {counter[0]}")    # Print the count
                    elif result["command"] == "createuser":
                        print("Invalid syntax") if result["exitcode"] == "invalidsyntax" else None
                        print("Only root can create new admin users") if result["exitcode"] == "notenoughprivileges" else None
                        print("User already exists") if result["exitcode"] == "userexists" else None

                    elif result["command"] == "cd":
                        print("Invalid syntax") if result["exitcode"] == "invalidsyntax" else None
                        self.update_dos_prompt(result["newpath"])

    def command_loop(self):
        while self._is_running:
            user_input = input(self._dos_prompt if self.echo_state else "")
            self.parser_and_dispatcher(user_input)

    def update_dos_prompt(self, new_path: str):
        self._dos_prompt = "C:" + "\\".join(new_path.split("/")) + "> "

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

    # Shell commands, not dependent on Kernel and FileSystem
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
help - Shows this message
ver - Shows the version
echo - Prints the text after the command
logoff - Logs out of the current session
createuser - Creates a new user account
dir - Lists folders and files inside the working directory
""")
        else:
            pass

    def version(self, args):
        # Prints the version
        print(f"\n{self._version_info}\n")

    def on_start(self):
        # Prints starting message
        print(f"""{self._version_info}

Copyright (C) 2026      All rights reserved
""")




def main():
    kernel = Kernel()
    kernel.on_boot()

if __name__ == "__main__":
    main()