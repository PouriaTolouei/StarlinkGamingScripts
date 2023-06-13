import Unique
import json, time, subprocess, threading, os, csv, pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import matplotlib.pyplot as plt
from matplotlib.category import UnitData

#------------------------- Variables and Constants  ------------------------------ 

NUM_TESTS = 1
KEY_DELAY = 0.7
CAPTURE_LENGTH = "120"
INTERFACE = Unique.INTERFACE
PROFILE_PATH = Unique.PROFILE_PATH
CAPTURE_PATH = Unique.CAPTURE_PATH
PLAYER_TYPE = Unique.PLAYER_TYPE
FIELDS = ["Time", "Stream FPS", "Ping", "Packet Loss", "Used Bandwidth", "Resolution"]
FIELDS2 = ["Time",  "Ping", "Packet Loss", "Input Latency"]
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

# Starts capturing network traffic and creates the test folder
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
  startTime = time.time() # Keeps track of the starting time

  while time.time() < startTime + timeout:
      metric = [] # stores all the metrics for each interval

      sec = time.time() - startTime # seconds passed since the start of collection
      
      # Locates all the web elements where the metric are displayed
      streamFPS = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[2]/span')
      ping = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[3]/span')
      # frameLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[1]')
      # frameLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[2]')
      packetLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[1]')
      # packetLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[2]')
      resolution = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[5]/div/span')
      # bandwidthAvailable = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[3]/div/span[1]')
      bandwidthUsed = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[4]/div/span[1]')

      # Adds them to the list
      metric.append(sec)
      metric.append(int(streamFPS.text))
      metric.append(int(ping.text))
      metric.append(int(packetLoss.text))
      metric.append(int(bandwidthUsed.text))
      metric.append(resolution.text)

      # Adds the metrics of each interval to the list of all the intervals
      metrics.append(metric)
      time.sleep(0.7)

# Captures the boost action by observing pixel color change towards red in the exhaust 
def captureAction(measurements):
    start_time = time.time() # staring time of capture

    # Keeps looking for pixel color change
    while True:
        pixel = pyautogui.pixel(Unique.EXHAUST_POS_X, Unique.EXHAUST_POS_Y) # Pixel in the exhaust

        # Checks to see if the pixel has become more red to confirm boost action 
        # or times out after 0.5 second
        if (pixel[0] > 200) or (time.time() - start_time) >= 1:
            # Captures the time
            action_time = time.time()
            measurements.append(action_time)
            break

# Boosts the car and captures the time the key was pressed
def boost(driver, measurements):
   holdKey('x', driver, 0.07) # Presses the boost key for the average key press time
   
   # Captures the time
   key_time = time.time() 
   measurements.append(key_time)

   # Collects the ping corresponding to the key press
   ping = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[3]/span')
   packetLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[1]')
   measurements.append(int(ping.text))
   measurements.append(int(packetLoss.text))
   


# Drives the car around in the match
def driveCar(driver, inputLatency):
  timeout = int(CAPTURE_LENGTH) # duration of gameplay
  startTime = time.time() # Keeps track of the starting time

  while time.time() < startTime + timeout:
      measurements = [] # Keeps track of the input latency measurements
      
      # Boosts the car and measures and records key press and action timestamps
      # move =  threading.Thread(target= boost, args=[driver, measurements])
      # capture = threading.Thread(target= captureAction, args=[measurements])

      sec = time.time() - startTime # seconds passed since the start of input latency collection
      measurements.append(sec)
     
      boost(driver, measurements)
      captureAction(measurements)

     
      # Calculates input latency (action time - key press time)
      measurements.append((measurements[4] - measurements[1]) * 1000)

      # Removes the timestamps as they are not relevant for analysis
      measurements.pop(4)
      measurements.pop(1)

      inputLatency.append(measurements)

      # Waits for the boost effect to fade away
      time.sleep(1.5)


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
  inputLatency = []

  # Loads my chrome profile, so that GFN doesn't require login
  options = webdriver.ChromeOptions() 
  options.add_argument("user-data-dir=" + PROFILE_PATH)
  options.add_experimental_option("useAutomationExtension", False)
  options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
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
  gamePlay = threading.Thread(target=driveCar, args=[driver, inputLatency])
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

  testFolder = Unique.CAPTURE_PATH + str(setNum) + "\\"

  # Writes the metrics to a CSV file
  with open(testFolder + "Metrics" + str(i) + ".csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(FIELDS)
    write.writerows(metrics)

  # Writes the input latency data to a CSV file
  with open(testFolder + "Latencies" + str(i) + ".csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(FIELDS2)
    write.writerows(inputLatency)


  time.sleep(5)

  # Closes the game
  closeGame(element=element)
 
  # Closes the automation session
  driver.close()
  
  # Creates the latency graphs
  inputLatency = list(zip(*inputLatency))
  plt.figure(figsize=(21,11))
  plt.ylim(0, 300)
  plt.yticks(range(0, 300, 50))
  plt.xticks(range(0, int(CAPTURE_LENGTH) + 10, 10))
  plt.xlabel("Time (s)")
  plt.plot(inputLatency[0], inputLatency[1], '-o', label="Ping (ms)")
  plt.plot(inputLatency[0], inputLatency[3], '-o', label="Input Latency (ms)")
  plt.plot(inputLatency[0], inputLatency[2], '-o', label="Packet Loss")
  plt.legend(loc="upper left")
  plt.savefig(testFolder + "Latencies" + str(i) + ".jpg")

  # Creates the metrics graph
  resolutionLabels = ['480 x 360 (16:9)', '960 x 540 (16:9)', '1280 x 720 (16:9)', '1366 x 768 (16:9)', '1600 x 900 (16:9)', '1920 x 1080 (16:9)']
  metrics = list(zip(*metrics))
  plt.figure(figsize=(21,11))
  plt.ylim(0, 300)
  plt.yticks(range(0, 300, 50))
  plt.xticks(range(0, int(CAPTURE_LENGTH) + 10, 10))
  plt.xlabel("Time (s)")
  plt.plot(metrics[0], metrics[1], '-o', label="Stream FPS")
  plt.plot(metrics[0], metrics[2], '-o', label="Ping (ms)")
  plt.plot(metrics[0], metrics[3], '-o', label="Packet Loss")
  plt.plot(metrics[0], metrics[4], '-o', label="Used Bandwidth (Mbps)")
  plt.legend(loc="upper left")
  SecondaryYAxis = plt.twinx()
  SecondaryYAxis.set_ylim(-1,6)
  SecondaryYAxis.set_ylabel("Resolution")
  plt.plot(metrics[0], metrics[5], '-o', label="Resolution", yunits=UnitData(resolutionLabels), color="black")
  plt.legend(loc="upper right")
  plt.savefig(testFolder + "Metrics" + str(i) + ".jpg")

# Pixel location diagnosis

# while True:
#     x, y = pyautogui.position()
    # pixel = pyautogui.pixel(957,1006)

    # if pixel[0] > 200:
    #     print("boost used")

    # print("Position")
    # print(str(x) + ',' + str(y))
    # print("Color")
    # print(pixel)
