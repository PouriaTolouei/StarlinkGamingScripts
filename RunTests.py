import paramiko, threading, time

HOST = "100.99.232.31"
GUEST = "100.64.165.41"


def runTest(ip: str):
    # Create an SSH client instance 
    client = paramiko.SSHClient() 
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Connect to the server 
    client.connect(ip, username="pouriatolouei", password="pt230213") 

    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("DISPLAY=:0 nohup python3 /home/pouriatolouei/Documents/StarLinkGamingScripts/GFNAutomationLinux.py") 

    print(ip)
    # Print the errors 
    errors = stderr.readlines()
    for error in errors:
        print(error.strip())

    print(stdout.readlines())


for i in range (1, 11):
    print("################## Round " + str(i) +  " ##################")

    host = threading.Thread(target=runTest, args=[HOST])
    guest = threading.Thread(target=runTest, args=[GUEST])

    host.start()
    time.sleep(5)
    guest.start()
    
    host.join()
    guest.join()