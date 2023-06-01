import Unique
import json, time, subprocess, threading, os, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

#------------------------- Variables and Constants  ------------------------------ 

NUM_TESTS = 1
KEY_DELAY = 0.7
CAPTURE_LENGTH = "210"
INTERFACE = Unique.INTERFACE
PROFILE_PATH = Unique.PROFILE_PATH
CAPTURE_PATH = Unique.CAPTURE_PATH
PLAYER_TYPE = Unique.PLAYER_TYPE
FIELDS = ["Time", "Stream FPS", "Ping", "Frame Loss", "Packet Loss",  "Available Bandwith", "Used Bandwidth", "Resolution"]
metrics = []

#-------------------------------- Methods ---------------------------------------- 

# Send a raw command via the devtools protocol
def dispatchKeyEvent(driver, name, options = {}):
  options["type"] = name
  body = json.dumps({'cmd': 'Input.dispatchKeyEvent', 'params': options})
  resource = "/session/%s/chromium/send_command" % driver.session_id
  url = driver.command_executor._url + resource
  driver.command_executor._request('POST', url, body)

# Holds down a key for the given duration
def holdKey(key, driver, duration):
  endtime = time.time() + duration
  options = { \
    "code": "Key" + key.upper(),
    "key": key,
    "text": key,
    "unmodifiedText": key,
    "nativeVirtualKeyCode": ord(key.upper()),
    "windowsVirtualKeyCode": ord(key.upper())
  }

  while True:
    dispatchKeyEvent(driver, "rawKeyDown", options)
    dispatchKeyEvent(driver, "char", options)

    if time.time() > endtime:
      dispatchKeyEvent(driver, "keyUp", options)
      break

# Launches GFN in chrome and starts a Rocket League game session
def launchGame(driver: WebDriver) -> WebElement:
  # Starts a Rocket league game session on GFN
  driver.get("https://play.geforcenow.com/mall/#/streamer?launchSource=GeForceNOW&cmsId=100871611&shortName=rocket_league_egs&appLaunchMode=Default&bgImageUrl=https:%2F%2Fimg.nvidiagrid.net%2Fapps%2F100871511%2FZZ%2FHERO_IMAGE_01_ba30a70f-6050-47ca-8303-bfaad8439a6b.jpg")

  # Waits until the "start playing" prompt comes up and clicks on it (timesout after 1 hour)
  WebDriverWait(driver, 3600).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-focus-indicator.font-button2.text-button-icon.mat-raised-button.mat-button-base.mat-accent"))).click()

  # Waits until the game loads on the remote systen (usually takes around 30 seconds)
  time.sleep(45)

  # Locates the video stream
  element = driver.find_element(By.TAG_NAME, "video")

  # Presses the enter key to start the game 
  element.send_keys(Keys.ENTER)

  return element

# Starts a private match in Rocket League
def launchMatch(element: WebElement):
  # Navigates to the play button
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ARROW_DOWN)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ARROW_UP)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ENTER)

  # Navigates to custom game button
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ARROW_LEFT)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ARROW_RIGHT)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ENTER)

  # Navigates to private match button
  for i in range(2):
      time.sleep(KEY_DELAY)
      element.send_keys(Keys.ARROW_RIGHT)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ENTER)

  if PLAYER_TYPE == "host":
    # Navigates to create private match button
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ARROW_RIGHT)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ARROW_LEFT)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ENTER)

    # Navigates to create match button
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ARROW_UP)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ARROW_DOWN)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ENTER)


  elif PLAYER_TYPE == "guest":
    # Navigates to join private match button
    time.sleep(3)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ARROW_RIGHT)
    time.sleep(KEY_DELAY)
    element.send_keys(Keys.ENTER)


  # Navigates to create join button
  for i in range(2):
      time.sleep(KEY_DELAY)
      element.send_keys(Keys.ARROW_DOWN)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ENTER)
  
  # Navigates to auto button
  time.sleep(8)
  element.send_keys(Keys.ARROW_UP)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ARROW_DOWN)
  time.sleep(KEY_DELAY)
  element.send_keys(Keys.ENTER)

# Starts capturing network traffic on the ethernet port
def captureTraffic(iteration: int):
  # Creates a new folder for each set of tests
  # Checks to see if the folder exists only for the first test in a set
  if i == 1:    
    global setNum 
    setNum = 1
    succesfullyCreated = False

    # Keeps trying to create a folder until it doesn't exist
    while not succesfullyCreated:
      try:
        os.mkdir(Unique.CAPTURE_PATH + str(setNum))
        succesfullyCreated = True
        path = Unique.CAPTURE_PATH + str(setNum) + "\\"
      except FileExistsError:
        setNum += 1
  else:
     path = Unique.CAPTURE_PATH + str(setNum) + "\\"


  # Calls tshark in the command prompt
  subprocess.run("tshark -i " + INTERFACE + " -w " + path + "Capture" + str(iteration) + ".pcap" + " -a duration:" + CAPTURE_LENGTH)


# Collects in-game network metrics from GFN overlay 
def captureMetrics(driver, metrics):
  timeout = int(CAPTURE_LENGTH) # duration of gameplay
  timeout_start = time.time() # Keeps track of the starting time

  while time.time() < timeout_start + timeout:
      metric = [] # stores all the metrics for each interval

      sec = time.time() - timeout_start # seconds passed since the start of collection
      
      # Locates all the web elements where the metric are displayed
      streamFPS = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[2]/span')
      ping = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[3]/span')
      frameLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[1]')
      frameLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[2]')
      packetLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[1]')
      packetLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[2]')
      resolution = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[5]/div/span')
      bandwidthAvailable = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[3]/div/span[1]')
      bandwidthUsed = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[4]/div/span[1]')

      # Adds them to the list
      metric.append(sec)
      metric.append(streamFPS.text)
      metric.append(ping.text)
      metric.append(frameLoss.text)
      metric.append(packetLoss.text)
      metric.append(bandwidthAvailable.text)
      metric.append(bandwidthUsed.text)
      metric.append(resolution.text)

      # Adds the metrics of each interval to the list of all the intervals
      metrics.append(metric)
      time.sleep(0.6)

# Holds forwards and left at the same time to steer left
def steerLeft():
  driveForward =  threading.Thread(target= holdKey, args=('w', driver, 1.40))
  turnLeft = threading.Thread(target= holdKey, args=('a', driver, 1.40))
  driveForward.start()
  turnLeft.start()
  driveForward.join()
  turnLeft.join()

# Holds forwards and right at the same time to steer right
def steerRight():
  driveForward =  threading.Thread(target= holdKey, args=('w', driver, 1.40))
  turnRight = threading.Thread(target= holdKey, args=('d', driver, 1.40))
  driveForward.start()
  turnRight.start()
  driveForward.join()
  turnRight.join()

# Holds forwards and boost at the same time to boost forward
def boostForward():
  driveForward =  threading.Thread(target= holdKey, args=('w', driver, 0.30))
  boost = threading.Thread(target= holdKey, args=('x', driver, 0.30))
  driveForward.start()
  boost.start()
  driveForward.join()
  boost.join()

# Drives the car around in the match
def driveCar():
  # Moves the car closer to the middle
  holdKey('w', driver, 1.8)

  # Drives in a loop in both directions (4 times each)
  for i in range (24):
    time.sleep(0.1)
    steerLeft()
    time.sleep(0.1)
    boostForward()
    time.sleep(0.1)
    steerLeft()
    time.sleep(0.1)
    boostForward()

    time.sleep(0.1)
    steerRight()
    time.sleep(0.1)
    boostForward()
    time.sleep(0.1)
    steerRight()
    time.sleep(0.1)
    boostForward()

  # Stops the car
  holdKey('s', driver, 0.5)

  # Makes sure the car has stopped
  time.sleep(2)
  
  # Double Jumps
  holdKey('z', driver, 0.5)
  time.sleep(0.1)
  holdKey('z', driver, 0.5)


def closeGame(element: WebElement):
   # Leaves the match
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ESCAPE)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ARROW_UP)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ENTER)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ARROW_LEFT)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ENTER)
   
   # Waits for the main menu to load
   time.sleep(3)

   # Leaves the game
   for i in range(6):
      time.sleep(KEY_DELAY)
      element.send_keys(Keys.ARROW_DOWN)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ENTER)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ARROW_LEFT)
   time.sleep(KEY_DELAY)
   element.send_keys(Keys.ENTER)

  # Wait until the game properly closes
   time.sleep(15)

#-------------------------------- Execution ---------------------------------------- 

for i in range(1, NUM_TESTS + 1):
  # Resets the metrics array
  metrics = []
  
  # Loads my chrome profile, so that GFN doesn't require login
  options = webdriver.ChromeOptions() 
  options.add_argument("user-data-dir=" + PROFILE_PATH) 
  driver = webdriver.Chrome(options=options)

  # Launches the game and match
  element = launchGame(driver=driver)

  time.sleep(KEY_DELAY)
  element.send_keys("n")

  launchMatch(element=element)

  if PLAYER_TYPE == 'host':
    # Waits for the match to load
    time.sleep(12)
  elif PLAYER_TYPE == 'guest':
    # Waits for the match to load
    time.sleep(7)

  # Creates seperate threads for driving the car and capturing network traffic 
  gamePlay = threading.Thread(target=driveCar)
  dataCollection = threading.Thread(target=captureTraffic, args=[i])
  metricCollection = threading.Thread(target=captureMetrics, args=(driver, metrics))

  # Runs both threads concurrently
  gamePlay.start()
  dataCollection.start()
  metricCollection.start()

  # Wait for the execution of the threads to complete before the rest of the program executes
  gamePlay.join()
  dataCollection.join()
  metricCollection.join()

  # Writes the metrics to a CSV file
  with open(Unique.CAPTURE_PATH + str(setNum) + "\\" + "Metrics" + str(i) + ".csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(FIELDS)
    write.writerows(metrics)

  time.sleep(5)

  # Closes the game
  closeGame(element=element)

  # Closes the automation session
  driver.close()







