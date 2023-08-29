import paramiko, threading, time, sys

HOST = sys.argv[1]
HOST_USERNAME = sys.argv[2]
HOST_PASSWORD = sys.argv[3]
HOST_TYPE = sys.argv[4]

GUEST = sys.argv[5]
GUEST_USERNAME = sys.argv[6]
GUEST_PASSWORD = sys.argv[7]
GUEST_TYPE = sys.argv[8]

ROUNDS = int(sys.argv[9])

CAPTURE_PATH = "/home/pouriatolouei/Documents/StarLinkGamingScripts/"

# Creates the test folder on a remote system and returns the current test iteration on that system
def createFolder(ip: str, user: str, passcode: str) -> int:
    # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username=user, password=passcode) 

    # Execute commands on the server 
    testNum = 1
    succesfullyCreated = False

    # Create a folder with the current current iteraion of test in its name
    while not succesfullyCreated:
            stdin, stdout, stderr = client.exec_command("mkdir " + CAPTURE_PATH + "Results/Test" + str(testNum))
            error = stderr.readline().strip()
            if error == "mkdir: cannot create directory ‘" + CAPTURE_PATH + "Results/Test" + str(testNum) + "’: File exists":
                testNum += 1
            else:
                succesfullyCreated = True
    print(stderr.readlines())
    return testNum

# Runs the test script on a remote system
def runTest(ip: str, type: str, user: str, passcode: str):
    # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username=user, password=passcode) 

    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("DISPLAY=:0 nohup python3 " + CAPTURE_PATH + "GFNAutomationLinux.py " + type) 

    print(ip)
    # Print the errors 
    errors = stderr.readlines()
    for error in errors:
        print(error.strip())

    print(stdout.readlines())

# Moves the collected data into the created folder on a remote system
def moveFiles(ip: str, testNum: int, user: str, passcode: str):
     # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username=user, password=passcode) 

    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("mv " + CAPTURE_PATH + "Results/temp/* " + CAPTURE_PATH + "Results/Test" + str(testNum)) 
    print(stderr.readlines())


# ----------------------------------- Execution -----------------------------------------

# Creates the test folder on each of the remote systems
testNumHost = createFolder(HOST, HOST_USERNAME, HOST_PASSWORD)
testNumGuest = createFolder(GUEST, GUEST_USERNAME, GUEST_PASSWORD)
# Ouputs the created directory for confirmation
print(testNumHost)
print(testNumGuest)

# Runs the test on the remote systems ROUNDS x 5 times
for i in range (0, ROUNDS):
    for j in range (1, 6):
        print("################## Round " + str((5*i)+j) +  " ##################")

        host = threading.Thread(target=runTest, args=[HOST, HOST_TYPE, HOST_USERNAME, HOST_PASSWORD])
        guest = threading.Thread(target=runTest, args=[GUEST, GUEST_TYPE, GUEST_USERNAME, GUEST_PASSWORD])

        host.start()
        guest.start()
        
        host.join()
        guest.join()

    print("################## Cooldown ##################")
    time.sleep(300)

# Moves the collected data to the create folders on the remote systems
moveFiles(HOST, testNumHost, HOST_USERNAME, HOST_PASSWORD)
moveFiles(GUEST, testNumGuest, GUEST_USERNAME, GUEST_PASSWORD)
