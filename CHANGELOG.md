## Changelog

## v1.5.1 aplha
- Improved load_state_from_json

## v1.5.0 alpha
- Added saving and loading state of the simulator thru commands:
  - ```state save``` to save the state and  
  - ```state load``` to load the state  
  Note: If a state.json file exists, it will automatically be loaded
- Added ```shutdown```
- Simplied if...elif chain in Shell.parser_and_dispatcher method

## v1.4.3 alpha
- Added rmdir command. Only relative paths supported (Folder or file is always deleted in the working directory)
- Added changepassword command.
- Update help command to have detailed descriptions of the new commands added
  
## v1.4.2 alpha
- Added mkdir command. Only relative paths supported (Folder is always made in the working directory)

## v1.4.1 alpha
- Added detailed descriptions of some commands to help
- Fixed a bug where after logging off and logging back in you couldnt get to the dos prompt
  
## v1.4.0 alpha
- Added ```cd``` command. ```..```, ```.```, ```/``` and relative paths are supported.
- Added ```help``` command
- Changed ```shutdown``` to ```logoff```
- Added type hints to most if not all variables that didnt have them
