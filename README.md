# Starlink Rocket League Cloud Gaming Script

## Setting Up the Data Collection Script
1. Place the GFNAutomationLinux.py file in the directory where you wish to store your data.
2. Under the Varibles and Constants section of the script, adjust the following based on your system:
   - INTERFACE: The network interace you wish to collect your data over
   - PROFILE_PATH: Your chrome profile path which can be found in chrome://version/ under the Profile Path field (use the parent folder)
   - CAPTURE_PATH: The directory for saving the data: script_directory/Results/temp/ (The results and temp folders will be created automatically)
   - EXHAUST_POS_X and EXHAUST_POS_Y: The center position for the car's exhaust depending on the screen resolution.

3. Before running the script, make sure that
   - Your chrome is logged into a single profile and pop-up for choosing a profile is disabled.
   - You have already logged into Geforce Now.
   - You have already manually tried to set up or join a private match on rocket league.
     (the game remembers the last selected gameplay mode and private match joining details, so not doing this can affect the navigation)
   - You have properly ended the previous Geforce Now session (otherwise it will load mid-session and breaks the script).
  
## Running the Data Collection Script
1. 
  
