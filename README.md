# PyDOS

Disclaimer: The project is under construction, so the README may not reflect the actual changes in each revision

PyDOS is a simple DOS simulator, that replicates some DOS functionalities, and adds other ones. 

## Supported commands

PyDOS currently supports these comamnds:
- ```ver``` Shows the version of PyDOS
- ```cls``` CLears the screen
- ```logoff``` Logs out of the current user account
- ```echo ON/OFF/text``` Prints any text after the command, or toggles the dos prompt on and off
- ```createuser username password type``` Will create a new user, type can be ```admin``` or ```normal```   
  Note: Only an admin user can create another admin user
- ```dir``` Shows all files and folders in the current directory
- ```help``` Lists all commands with a brief explanation
- ```cd``` Change the working directory

## Commands that are in progress

PyDOS will eventually support these commands:
- ```help``` with the ability to get a more detailed description of any command
- ```shutdown``` Poweroff the system
- ```mkdir``` or ```md``` Make a new directory
- ```rmdir``` or ```rm``` Remove a directory
- ```del``` Delete a file
- ```changepassword``` Changes the password of an existing account

## Other features that are in progress


PyDOS will eventually support:
- editing a .txt or a .pds file tha exists within the directory PyDOS is in 
- scripts, with a .pds extension (short for PyDosScript), that are written on your host PC, or through the edit feature in PyDOS
- saving the state on ```shutdown```, ```logoff``` and when a bugcheck is raised
