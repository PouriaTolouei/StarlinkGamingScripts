import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


# Loads my chrome profile, so that GFN doesn't require login
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\pouri\\AppData\\Local\\Google\\Chrome\\User Data") 
driver = webdriver.Chrome(options=options)

# Starts a Rocket league game session on GFN
driver.get("https://play.geforcenow.com/mall/#/streamer?launchSource=GeForceNOW&cmsId=100871611&shortName=rocket_league_egs&appLaunchMode=Default&bgImageUrl=https:%2F%2Fimg.nvidiagrid.net%2Fapps%2F100871511%2FZZ%2FHERO_IMAGE_01_ba30a70f-6050-47ca-8303-bfaad8439a6b.jpg")

# Waits until the "start playing" prompt comes up and clicks on it (timesout after 1 hour)
WebDriverWait(driver, 3600).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-focus-indicator.font-button2.text-button-icon.mat-raised-button.mat-button-base.mat-accent"))).click()

# Waits until the game loads on the remote systen
time.sleep(30)

# Clicks on the video stream to start the game (doesn't seem to work)
element = driver.find_element(By.TAG_NAME, "video")

# Enters the game
element.send_keys(Keys.ENTER)

# The remaining keystrokes navigate to start a private match 
for i in range(7):
    time.sleep(0.1)
    element.send_keys(Keys.ARROW_UP)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

time.sleep(0.1)
element.send_keys(Keys.ARROW_LEFT)

time.sleep(0.1)
element.send_keys(Keys.ARROW_RIGHT)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

for i in range(2):
    time.sleep(0.1)
    element.send_keys(Keys.ARROW_RIGHT)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

time.sleep(0.1)
element.send_keys(Keys.ARROW_RIGHT)

time.sleep(0.1)
element.send_keys(Keys.ARROW_LEFT)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

time.sleep(0.1)
element.send_keys(Keys.ARROW_UP)

time.sleep(0.1)
element.send_keys(Keys.ARROW_DOWN)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

for i in range(2):
    time.sleep(0.1)
    element.send_keys(Keys.ARROW_DOWN)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

time.sleep(4)
element.send_keys(Keys.ARROW_UP)

time.sleep(0.1)
element.send_keys(Keys.ARROW_DOWN)

time.sleep(0.1)
element.send_keys(Keys.ENTER)

time.sleep(7)

# Moves the car forward for 3 seconds and then backward for 3 seconds
holdKey('w', driver, 3)
holdKey('s', driver, 3)


# Keeps the automation session open
time.sleep(20000)


# for i in range(3):
#     time.sleep(1)
#     element.send_keys(Keys.ARROW_LEFT)

# time.sleep(1)
# element.send_keys(Keys.ENTER)

# for i in range(2):
#     time.sleep(1)
#     element.send_keys(Keys.ARROW_RIGHT)

# time.sleep(1)
# element.send_keys(Keys.ARROW_DOWN)

# time.sleep(1)
# element.send_keys(Keys.ENTER)






