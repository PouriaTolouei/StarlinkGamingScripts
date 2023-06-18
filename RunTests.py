import subprocess
import paramiko

# Create an SSH client instance 
client = paramiko.SSHClient() 
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
 
# Connect to the server 
client.connect("100.64.165.41", username="pouriatolouei", password="pt230213") 

for i in range (1, 2):
    print("################## Round " + str(i) +  " ##################")
    # Execute commands on the server 
    stdin, stdout, stderr = client.exec_command("DISPLAY=:0 nohup python3 /home/pouriatolouei/Documents/StarLinkGamingScripts/GFNAutomationLinux.py") 
    
    # Print the errors 
    errors = stderr.readlines()
    for error in errors:
        print(error.strip())
    
    print(stdout.readlines())

# Close the SSH connection 
client.close() 