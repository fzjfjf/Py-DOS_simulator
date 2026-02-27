import shutil, json
from random import randint
from time import sleep
from sys import exit, stdin
from os import name, system

# ========= Classes ========
# ====== Exception classes =====
class InvalidFileSystemStructure(Exception):
    def __init__(self, message="Invalid file system structure"):
        super().__init__(message)




# ===== Core classes =====
class FileSystem:
    def __init__(self):
        self._folder_structure = {}
        self._drive_label = ""

    def initialize_file_system(self, fs):
        # Make a drive label
        drive_label_list = []
        for i in range(0, 9):   # Generate a random drive label
            drive_label_list.append(randint(0, 9))
        drive_label_list[4] = "-"
        for i in range(0, 9):   # Turn the numbers into strings
            drive_label_list[i] = str(drive_label_list)
        self._drive_label = "".join(drive_label_list)

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

            if "files" not in folder or "folders" not in folder:
                raise InvalidFileSystemStructure("102")

            if not isinstance(folder["files"], list):
                raise InvalidFileSystemStructure("103")

            if not isinstance(folder["folders"], dict):
                raise InvalidFileSystemStructure("104")

            # Recurse into subfolders
            for subfolder_name, subfolder in folder["folders"].items():
                _validate_folder(subfolder)

        _validate_folder(fs)

    def change_directory(self):
        pass

    def dir_command(self):
        pass

    def make_directory(self):
        pass

    def remove_directory_or_file(self):
        pass




class Kernel:
    def __init__(self):
        self._path: str = "/"
        self._working_drive: str = "c"
        self._mounted_drives: dict = {
            "c": FileSystem(),
        }
        self._kernel_commands: dict = {
            "mount": self.mount_drive,
        }


    def command_resolver(self, split_user_input):
        # Will resolve non-shell commands like CD, DIR, ...
        pass

    def mount_drive(self, drive_letter, fs):
        # Will mount the drive
        self._mounted_drives[drive_letter] = FileSystem()
        try:
            self._mounted_drives[drive_letter].initialize_file_system(fs)
        except InvalidFileSystemStructure as e:
            e = e.args[0]
            if e == "101":
                self.bug_check(101, "INVALID_FS-DICT")
            elif e == "102":
                self.bug_check(102, "INVALID_FS-KEYS")
            elif e == "103":
                self.bug_check(103, "INVALID_FI_TYPE")
            elif e == "104":
                self.bug_check(104, "INVALID_FO_TYPE")
            else:
                self.bug_check(100, "INVALID_FILE_SYSTEM_STRUCTURE")

    def update_path(self):
        pass

    def bug_check(self, exit_code, exit_code_for_print):
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
    def __init__(self):
        self._dos_prompt: str = "C:\\> "
        self._version_info: str = "PY-DOS 1.1.0 alpha"
        self._shell_commands: dict = {}
        self._is_running: bool = True
        self.echo_state: bool = True

    def parser_and_dispatcher(self, user_input):
        # Parses user input and calls functions accordingly
        split_input = user_input.lower().split()
        if len(split_input) > 0:        # Ignore empty input
            if split_input[0] == "trigger_bug_check":   # Debug case
                kernel.bug_check(20, "BUG_CHECK_ON_COMMAND")
            elif split_input[0] in self._shell_commands:
                self._shell_commands[split_input[0]](split_input[1:])
            else:
                kernel.command_resolver(split_input)

    def command_loop(self):
        while self._is_running:
            user_input = input(self._dos_prompt)
            self.parser_and_dispatcher(user_input)

    def update_dos_prompt(self):
        pass

    def getchar(self):
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
    def shutdown(self, args):
        # Here goes any code that saves the current state of the simulator (currently none)

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

    def echo(self, args):
        # Repeats the string provided by user, prints echo state if no string provided
        if len(args) == 0:      # If no arguments are provided
            print("Echo is ON") if self.echo_state else print("Echo is OFF")
        elif args[0] == "on":
            self.echo_state = True
        elif args[0] == "off":
            self.echo_state = False
        else:
            print(" ".join(args))

    def help(self, args):
        # Prints all available commands with short explanations
        pass

    def version(self, args):
        # Prints the version
        print(f"\n{self._version_info}\n")

    def on_start(self, args):
        # Prints starting message
        print(f"""{self._version_info}

Copyright (C) 2026      All rights reserved
""")

    # Add all Shell commands to the dict
    def initialize_shell_commands(self):
        self._shell_commands = {
        "ver": self.version,
        "help": self.help,
        "echo": self.echo,
        "cls": self.clear_screen,
        "shutdown": self.shutdown,
        }




def on_start():
    global kernel
    # Replace the placeholder kernel object
    kernel = Kernel()
    kernel.mount_drive("c", {"folders": {}, "files": []})

    shell = Shell()
    shell.initialize_shell_commands()
    return shell

def main():
    shell = on_start()
    shell.on_start([])
    shell.command_loop()

if __name__ == "__main__":
    main()