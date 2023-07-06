import json, time, subprocess, threading, os, csv, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import matplotlib.pyplot as plt
from matplotlib.category import UnitData
from pyvirtualdisplay import Display
from mss import mss
from PIL import Image
from datetime import datetime
import matplotlib.dates as mdates




#------------------------- Variables and Constants  ------------------------------ 

KEY_DELAY = 1
CAPTURE_LENGTH = "120"
FIELDS = ["Time", "Timestamp", "Stream FPS", "Ping", "Packet Loss", "Used Bandwidth", "Resolution", "Available Bandwidth"]
FIELDS2 = ["Time", "Timestamp", "Ping", "Packet Loss", "Input Latency"]

INTERFACE = "enp2s0"

PROFILE_PATH = "/home/pouriatolouei/.config/google-chrome/"
CAPTURE_PATH = "/home/pouriatolouei/Documents/StarLinkGamingScripts/Results/temp/"
PLAYER_TYPE = sys.argv[1]
EXHAUST_POS_X = 960
EXHAUST_POS_Y = 965

SEC = 0
TIME = 1
PING = 2
PACKETLOSS = 3

INPUTLATENCY = 4

FPS = 4
USEDBAND = 5
RESOLUTION = 6
AVAILBAND = 7

#-------------------------------- Methods ---------------------------------------- 

def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


#  Send a raw command via the devtools protocol
def dispatchKeyEvent(driver,  name, options = {}):
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
def launchGame() -> WebElement:
  # Starts a Rocket league game session on GFN
  driver.get("https://play.geforcenow.com/mall/#/streamer?launchSource=GeForceNOW&cmsId=100871611&shortName=rocket_league_egs&appLaunchMode=Default&bgImageUrl=https:%2F%2Fimg.nvidiagrid.net%2Fapps%2F100871511%2FZZ%2FHERO_IMAGE_01_ba30a70f-6050-47ca-8303-bfaad8439a6b.jpg")

  # Waits until the "start playing" prompt comes up and clicks on it (timesout after 1 hour)
  WebDriverWait(driver, 3600).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-focus-indicator.font-button2.text-button-icon.mat-raised-button.mat-button-base.mat-accent"))).click()

  # Waits until the game loads on the remote systen (usually takes around 30 seconds)
  time.sleep(5)

  # Locates the video stream
  element = driver.find_element(By.TAG_NAME, "video")

  # Brings up the stats overlay
  time.sleep(KEY_DELAY)
  element.send_keys("n")

  # Waits until the game loads on the remote systen (usually takes around 30 seconds)
  time.sleep(55)

  # Presses the enter key to start the game 
  element.send_keys(Keys.ENTER)

  return element

# Starts a private match in Rocket League
def launchMatch():
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
def captureTraffic():
  succesfullyCreated = False
  global roundNum
  roundNum = 1

  while not succesfullyCreated:
    try:
      os.mkdir(CAPTURE_PATH + str(roundNum))
      succesfullyCreated = True
      path = CAPTURE_PATH + str(roundNum) + "/"
    except FileExistsError:
      roundNum += 1
 
  # Calls tshark in the command prompt
  subprocess.run("/usr/bin/tshark -i " + INTERFACE + " -w " + path + "Capture" + str(roundNum) + ".pcap" + " -a duration:" + CAPTURE_LENGTH, shell=True)

# Collects in-game network metrics from GFN overlay 
def captureMetrics():
  timeout = int(CAPTURE_LENGTH) # duration of gameplay
  startTime = time.time() # Keeps track of the starting time

  while time.time() < startTime + timeout:
      metric = [] # stores all the metrics for each interval

      sec = time.time() - startTime # seconds passed since the start of collection
      actualTime = datetime.now()
      
      # Locates all the web elements where the metric are displayed
      ping = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[3]/span')
      packetLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[1]')
      streamFPS = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[2]/span')
      # frameLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[1]')
      # frameLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[1]/div/span[2]')
      # packetLossTotal = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[2]')
      resolution = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[5]/div/span')
      bandwidthUsed = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[4]/div/span[1]')
      bandwidthAvailable = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[3]/div/span[1]')

      # Adds them to the list
      metric.append(sec)
      metric.append(actualTime)
      metric.append(int(ping.text))
      metric.append(int(packetLoss.text))
      metric.append(int(streamFPS.text))
      metric.append(int(bandwidthUsed.text))
      metric.append(resolution.text)
      metric.append(int(bandwidthAvailable.text))

      # Adds the metrics of each interval to the list of all the intervals
      metrics.append(metric)
      time.sleep(1)

# Captures the boost action by observing pixel color change towards red in the exhaust 
def captureAction(measurements):
    start_time = time.time() # staring time of capture
    captured = False
    # Keeps looking for pixel color change
    while not captured:
        # Captures pixel inside the car exhaust
        pixel = capture_screenshot().getpixel((EXHAUST_POS_X, EXHAUST_POS_Y))

        # Checks to see if the pixel has become more red to confirm boost action 
        # or times out after 0.5 second
        if (pixel[0] > 200) or (time.time() - start_time) >= 1:
            # Captures the time
            action_time = time.time()
            measurements.append(action_time)
            captured = True

# Boosts the car and captures the time the key was pressed
def boost(measurements):
   
  # Collects the ping corresponding to the key press
   ping = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[2]/div[3]/span')
   packetLoss = driver.find_element(By.XPATH, '//*[@id="fullscreen-container"]/nv-igo/nv-osd/div/div[2]/div/div[2]/div/nv-statistics-overlay/div/div/div/div[3]/div[2]/div/span[1]')
   measurements.append(int(ping.text))
   measurements.append(int(packetLoss.text))
   
   holdKey('x', driver, 0.07) # Presses the boost key for the average key press time
   
   # Captures the time
   key_time = time.time() 
   measurements.append(key_time)

# Drives the car around in the match
def driveCar():
  timeout = int(CAPTURE_LENGTH) # duration of gameplay
  startTime = time.time() # Keeps track of the starting time

  while time.time() < startTime + timeout:
      measurements = [] # Keeps track of the input latency measurements

      sec = time.time() - startTime # seconds passed since the start of input latency collection
      actualTime = datetime.now()
      measurements.append(sec)
      measurements.append(actualTime)
     
      boost(measurements)
      captureAction(measurements)

     
      # Calculates input latency (action time - key press time)
      measurements.append((measurements[5] - measurements[4]) * 1000)

      # Removes the timestamps as they are not relevant for analysis
      measurements.pop(5)
      measurements.pop(4)

      inputLatency.append(measurements)

      # Waits for the boost effect to fade away
      time.sleep(1)


def closeGame():
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

   time.sleep(15)


# Writes the metrics to a CSV file
def exportMetricsData():
  with open(testFolder + "Metrics" + str(roundNum) + ".csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(FIELDS)
    write.writerows(metrics)


 # Writes the input latency data to a CSV file
def exportLatenciesData():
  with open(testFolder + "Latencies" + str(roundNum) + ".csv", 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(FIELDS2)
    write.writerows(inputLatency)

# Creates the latency graphs
def createLatenciesGraph(inputLatency):
  inputLatency = list(zip(*inputLatency))
  plt.figure(figsize=(21,11))
  plt.plot(inputLatency[TIME], inputLatency[PING], '-o', label="Ping (ms)")
  plt.plot(inputLatency[TIME], inputLatency[INPUTLATENCY], '-o', label="Input Latency (ms)")
  plt.plot(inputLatency[TIME], inputLatency[PACKETLOSS], '-o', label="Packet Loss")
  plt.legend(loc="upper left")
  plt.ylim(0, 350)
  plt.yticks(range(0, 350, 50))
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
  plt.gca().xaxis.set_major_locator(mdates.SecondLocator([0, 10, 20, 30, 40 , 50]))
  plt.xlabel("Time (s)")
  plt.margins(0)
  plt.savefig(testFolder + "Latencies" + str(roundNum) + ".jpg")
  plt.clf()  


 # Creates the metrics graph
def createMetricsGraph(metrics):
  resolutionLabels = ['480 x 360 (16:9)', '960 x 540 (16:9)', '1280 x 720 (16:9)', '1366 x 768 (16:9)', '1600 x 900 (16:9)', '1920 x 1080 (16:9)']
  metrics = list(zip(*metrics))
  plt.figure(figsize=(21,11))
  plt.plot(metrics[TIME], metrics[PING], '-o', label="Ping (ms)")
  plt.plot(metrics[TIME], metrics[PACKETLOSS], '-o', label="Packet Loss")
  plt.plot(metrics[TIME], metrics[FPS], '-o', label="Stream FPS")
  plt.plot(metrics[TIME], metrics[USEDBAND], '-o', label="Used Bandwidth (Mbps)")
  plt.plot(metrics[TIME], metrics[AVAILBAND], '-o', label="Available Bandwidth (Mbps)")
  plt.legend(loc="upper left")
  plt.ylim(0, 300)
  plt.yticks(range(0, 300, 50))
  plt.xlabel("Time (s)")
  plt.margins(0)
  SecondaryYAxis = plt.twinx()
  SecondaryYAxis.set_ylim(-1,6)
  SecondaryYAxis.set_ylabel("Resolution")
  plt.plot(metrics[TIME], metrics[RESOLUTION], '-o', label="Resolution", yunits=UnitData(resolutionLabels), color="black")
  plt.legend(loc="upper right")
  plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
  plt.gca().xaxis.set_major_locator(mdates.SecondLocator([0, 10, 20, 30, 40 , 50]))
  plt.savefig(testFolder + "Metrics" + str(roundNum) + ".jpg")
  plt.clf()

#-------------------------------- Execution ---------------------------------------- 
# Sets up a virual display
display = Display(visible= False, size=(1920, 1080), use_xauth=True)
display.start()

# Resets the metrics array
metrics = []
inputLatency = []

# Loads my chrome profile, so that GFN doesn't require login
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=" + PROFILE_PATH)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
# Makes sure the window is maximized
driver.maximize_window()

# Launches the game and match
element = launchGame()

launchMatch()

# Waits for match to load
if PLAYER_TYPE == 'host':
  # Waits for the match to load
  time.sleep(19)
elif PLAYER_TYPE == 'guest':
  # Waits for the match to load
  time.sleep(11)

# Creates seperate threads for driving the car and capturing network traffic 
gamePlay = threading.Thread(target=driveCar)
dataCollection = threading.Thread(target=captureTraffic)
metricCollection = threading.Thread(target=captureMetrics)

# Runs both threads concurrently
gamePlay.start()
dataCollection.start()
metricCollection.start()

# Wait for the execution of the threads to complete before the rest of the program executes
gamePlay.join()
dataCollection.join()
metricCollection.join()

testFolder = CAPTURE_PATH + str(roundNum) + "/"

# Waits for the gameplay to settle down
time.sleep(5)

# Captures screenshot for troubleshooting
img = capture_screenshot()
img.save(testFolder + "Screenshot" + str(roundNum) + ".png")

# Closes the game
closeGame()

# Stopsthe virtual display
display.stop()

# Exports the data into CSV files
exportMetricsData()
exportLatenciesData()

# Creates graphs
createLatenciesGraph(inputLatency)
createMetricsGraph(metrics)
