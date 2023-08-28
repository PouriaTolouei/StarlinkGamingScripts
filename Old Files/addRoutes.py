# -*- coding: utf-8 -*-


import geoip2.database
import requests
import subprocess


# The API endpoint
url = 'https://ipranges.nvidiangn.net/v1/ips'


reader = geoip2.database.Reader('C:\\Users\\uvic\\Documents\\GeoLite2-City_20230509\\GeoLite2-City.mmdb')

ipsArray = requests.get(url).json()['ipList']
ipsArrayClean = []
endingNums = []

# Removes the ending of the ip addresses
for i in range(len(ipsArray)):
    cutIndex = 0;
    while ipsArray[i][cutIndex] != '/' :
        cutIndex += 1

    ipsArrayClean.append(ipsArray[i][0:cutIndex])
    endingNums.append(int(ipsArray[i][cutIndex + 1:]))


for i in range(len(ipsArrayClean)):
    maskNum = "255.255.255."
    if endingNums[i] == 24:
        maskNum += "0"
    elif endingNums[i] == 25:
         maskNum += "128"
    elif endingNums[i] == 26:
        maskNum += "192"
    elif endingNums[i] == 27:
        maskNum += "224"
    elif endingNums[i] == 28:
        maskNum += "240"
    elif endingNums[i] == 29:
        maskNum += "248"
    elif endingNums[i] == 30:
        maskNum += "252"
    elif endingNums[i] == 31:
        maskNum += "254"
    elif endingNums[i] == 32:
        maskNum += "255"
    
    subprocess.run("route -p add " + ipsArrayClean[i] + " mask " + maskNum + " 192.168.1.1 IF 10")
    # subprocess.run("route -p DELETE " + ipsArrayClean[i])

