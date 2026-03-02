import time, sys, os, shutil, random

# Globals
kernel_is_running: bool = False


# Classes
class FileSystem:
    def __init__(self):
        pass



class Kernel:
    def __init__(self):
        self.path: str = "/"
        self.working_drive: str = "c"

    def command_resolver(self):
        # Will resolve non-shell commands like VER, CD, ...
        pass

# Make a kernel object
if not kernel_is_running:
    kernel = Kernel()
    kernel_is_running = True
else:
    raise RuntimeError("The kernel is already running!")



class Shell:
    def __init__(self):
        self._dos_prompt: str = "C\\> "
        self._version_info: str = "PY-DOS 1.0.0 alpha"
        self._shell_commands: dict = {}
        self._is_running: bool = True
        self.echo_state: bool = True

    def parses_and_dispatcher(self):
        # Parses user input and calls functions accordingly
        pass

    def command_loop(self):
        while self._is_running:
            user_input = input(self._dos_prompt)
            self.parse_and_dispatch(user_input)


    # Shell commands, not dependent on Kernel and FileSystem
    def shutdown(self, args):
        # Here goes any code that saves the current state of the simulator
        self._is_running = False

    def clear_screen(self, args):
        # Clears the screen while paying attention to os.name
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        else:
            for i in range(0, 100):
                print("\n")

    def echo(self, args):
        # Repeats the string provided by user, prints echo state if no string provided
        if len(args) == 0:      # If no arguments are provided
            print("Echo is ON") if self.echo_state else print("Echo is OFF")
        elif args[0] == "ON":
            self.echo_state = True
        elif args[0] == "OFF":
            self.echo_state = False
        else:
            print("".join(args))

    def help(self, args):
        # Prints all available commands with short explanations
        pass

    def version(self, args):
        # Prints the version
        pass

    def on_start(self, args):
        # Prints starting message
        print(f"""{self._version_info}

Copyright (C) 2026      All rights reserved
""")


def main():
    pass

if __name__ == "__main__":
    main()