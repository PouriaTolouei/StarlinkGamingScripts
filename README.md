# Starlink Rocket League Cloud Gaming Script

## Setting Up the Data Collection Script
1. Copy GFNAutomationLinux.py onto the system that you want to run the game on. 
2. Install and set up selenium using this tutorial: https://pypi.org/project/selenium/
3. Place the GFNAutomationLinux.py file in the directory where you wish to store your data.
4. Under the Varibles and Constants section of the script, adjust the following based on your system:
   - INTERFACE: The network interace you wish to collect your data over
   - PROFILE_PATH: Your chrome profile path which can be found in chrome://version/ under the "Profile Path" field (use the parent folder)
   - CAPTURE_PATH: The directory for saving the data: script_directory/Results/temp/ (The results and temp folders will be created automatically)
   - EXHAUST_POS_X and EXHAUST_POS_Y: The center position for the car's exhaust depending on the screen resolution.
5. Log into Geforce Now on your chrome browser and in the settings, adjust the following options based on your needs:
   - Server Location
   - Stream Quality
6. Launch Rocket League, login as necessary, and try setting up or joining a private match.
   - The game remembers the last selected gameplay mode and private match joining details, so not doing this  affects the navigation.
7. While the game is running, use Ctrl + G to launch GeforceNow overlay and go into settings:
   - Under "Shortcut controls", set "Change format" shortcut to "N",
   - Under "Heads up display", set statistics "Position" to "Upper right".
8. While the game is running, go into the game settings:
   - Under "Controls" > "View/Change bindings", set "Boost" to "X".
   - Under "Camera", set "Stiffness" to 1.00.
9. Make sure the car body chosen under "Garage" in Rocket League has an exhaust that's easy to track.
   - The Merc body (one of the defaults) is recommded.
10. Before running the script, make sure that
   - All the libraries at the top of the script are installed.
   - Your chrome is logged into a single profile and pop-up for choosing a profile is disabled.
   - You have already logged into Geforce Now.
   - You have already manually tried to set up or join a private match on rocket league.
   - You have properly set the Geforce Now and Rocket League settings and key bindings.
   - You have properly ended the previous Geforce Now session (otherwise it will load mid-session and breaks the script).
  
## Running the Data Collection Script
1. 
2. 
  
