# Clipboard Storage
This application stores your copy clipboard items in memory which
can be brought up using the command ctrl+alt+v.
## Setup
- To start the clipboard-copy application you must first install the 
library dependencies in the requirements.txt file. You can do this by
running ```pip3 install -r requirments.txt```, once these have been 
installed you will be good to run the application! 
## Configuration
- Logging file is stored in Logs/main.log, this stores all copies
recorded.
- The default keyboard wait characters are ctrl+alt+v but this can
be change depending on what input is passed to the controller's 
constructor method.
## Technical details
- The clipboard stores this data using the library Pyperclip, the 
clipboard is polled every second looking for updates.
- To run on linux you need to run with Sudo otherwise the keyboard 
library will not be able to listen to keyboard input ```sudo python3
 main.py```.
## Assets
icon.png - Icons made by [Freepik](https://www.freepik.com") from www.flaticon.com
