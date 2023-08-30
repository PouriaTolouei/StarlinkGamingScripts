# Starlink Rocket League Cloud Gaming Script

## Setting Up the Data Collection Script
1. Copy GFNAutomationLinux.py onto the two remote systems that you want to run the game on. 
2. Install and set up selenium on each using this tutorial: https://pypi.org/project/selenium/
3. Install wireshark using pip.
   - Allow non-root user to run network capture.
   - Run "sudo chmod +x /usr/bin/dumpcap" after the installation.
4. Place the GFNAutomationLinux.py file in the directory where you wish to store your data.
   - Make sure the directory and your username is consistent across the two systems.
5. Have two seperate Geforce Now accounts ready.

<br> On each of the systems, follow these steps: <br> <br>

5. Under the Varibles and Constants section of the script, adjust the following based on your system:
   - INTERFACE: The network interace you wish to collect your data over.
   - PROFILE_PATH: Your chrome profile path which can be found in chrome://version/ under the "Profile Path" field (use the parent folder).
   - CAPTURE_PATH: The directory for saving the data: script_directory/Results/temp/ (The results and temp folders will be created automatically).
   - EXHAUST_POS_X and EXHAUST_POS_Y: The center position for the car's exhaust depending on the screen resolution.
6. Log into Geforce Now on your chrome browser and in the settings, adjust the following options based on your needs:
   - Server Location
   - Stream Quality
7. Launch Rocket League, login as necessary, and try setting up or joining a private match.
   - The game remembers the last selected gameplay mode and private match joining details, so not doing this  affects the navigation.
8. While the game is running, use Ctrl + G to launch GeforceNow overlay and go into settings:
   - Under "Shortcut controls", set "Change format" shortcut to "N".
   - Under "Heads up display", set statistics "Position" to "Upper right".
9. While the game is running, go into the game settings:
   - Under "Controls" > "View/Change bindings", set "Boost" to "X".
   - Under "Camera", set "Stiffness" to 1.00.
10. Make sure the car body chosen under "Garage" in Rocket League has an exhaust that's easy to track.
    - The Merc body (one of the defaults) is recommded.   
11. Before running the script, make sure that
    - All the libraries at the top of the script are installed.
       - selenium
       - matplotlib
       - pyvirtualdisplay
       - mss   
    - Your chrome is logged into a single profile and pop-up for choosing a profile is disabled.
    - You have already logged into Geforce Now.
    - You have already manually tried to set up or join a private match on rocket league.
    - You have properly set the Geforce Now and Rocket League settings and key bindings.
    - You have properly ended the previous Geforce Now session (otherwise it will load mid-session and breaks the script).
  
## Running the Data Collection Script
1. Copy RunTests.py onto a system that is different from the system that is running the game.
2. Install the paramiko library.
3. Under the Varibles and Constants of the script, update the CAPTURE_PATH to match the directory where the data collection script is stored on your remote systems (no need to include "results/temp").
   - This script assumes that the two remote systems have the exact same directory for storing the data collection scripts.
4. Use the following command to start a testing session:
   - "python3 Directory/RunTests.py system1_IP system1_username system1_password system1_type system2_IP system2_username system2_password system2_type number_of_5_round_sets".
   - The system_type can be either "host" or "guest" depending on if the system is creating a private match or joining one.
   - A completed example where two systems each create their own private match is: "python3 RunTests.py 111.22.333.44 pouria 123456 host 555.66.777.88 pouria 123456 host".

You can also set this command as a cronjob to automatically run tests without supervision.

## Analyzing the Collected Data
1. Download all of your "Results" folders across the different systems.
2. For each scenario involving two system, create a folder. Within that folder, include a copy of  AnalyzeMetricsCombined.py script and create a folder for each systems.
   - The script creates combined graphs and stores them in the "Analysis" folder which will be automatically generated inside the scenario folder.
3. Within each system folder, include the "Results" folder that system and include a copy of AnalyzeMetricsIndividual.py script.
   - The scripts creates graphs and stores them in the "Analysis" folder which will be automatically generated inside the "Results" folder.
  
To find the analysis scripts and see an example of this structure, please take a look at the "DataAnalysis" folder.
  
   

