import paramiko, threading, time, sys

HOST = sys.argv[1]
GUEST = sys.argv[2]
ROUNDS = int(sys.argv[3])

# Creates the test folder on a remote system
def createFolder(ip: str) -> int:
     # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username="username", password="password") 

    # Execute commands on the server 
    testNum = 1
    succesfullyCreated = False

    # Create a folder with the current current iteraion of test in its name
    while not succesfullyCreated:
            stdin, stdout, stderr = client.exec_command("mkdir /home/pouriatolouei/Documents/StarLinkGamingScripts/Results/Test" + str(testNum))
            error = stderr.readline().strip()
            if error == "mkdir: cannot create directory ‘/home/pouriatolouei/Documents/StarLinkGamingScripts/Results/Test" + str(testNum) + "’: File exists":
                testNum += 1
            else:
                succesfullyCreated = True
    print(stderr.readlines())
    return testNum

# Runs the test script on a remote system
def runTest(ip: str, type: str):
    # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username="pouriatolouei", password="pt230213") 

    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("DISPLAY=:0 nohup python3 /home/pouriatolouei/Documents/StarLinkGamingScripts/GFNAutomationLinux.py " + type) 

    print(ip)
    # Print the errors 
    errors = stderr.readlines()
    for error in errors:
        print(error.strip())

    print(stdout.readlines())

# Moves the collected data into the created folder on a remote system
def moveFiles(ip: str, testNum: int):
     # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username="username", password="password") 

    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("mv /home/pouriatolouei/Documents/StarLinkGamingScripts/Results/temp/* /home/pouriatolouei/Documents/StarLinkGamingScripts/Results/Test" + str(testNum)) 
    print(stderr.readlines())


# ----------------------------------- Execution -----------------------------------------

# Creates the test folder on each of the remote systems
testNumHost = createFolder(HOST)
testNumGuest = createFolder(GUEST)
# Ouputs the created directory for confirmation
print(testNumHost)
print(testNumGuest)

# Runs the test on the remote systems ROUNDS x 5 times
for i in range (0, ROUNDS):
    for j in range (1, 6):
        print("################## Round " + str((5*i)+j) +  " ##################")

        host = threading.Thread(target=runTest, args=[HOST, "host"])
        guest = threading.Thread(target=runTest, args=[GUEST, "host"])

        host.start()
        guest.start()
        
        host.join()
        guest.join()

    print("################## Cooldown ##################")
    time.sleep(300)

# Moves the collected data to the create folders on the remote systems
moveFiles(HOST, testNumHost)
moveFiles(GUEST, testNumGuest)