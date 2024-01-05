import csv, os, statistics, sys
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

#------------------------- Variables and Constants  ------------------------------ 
# Filenames and Labels
FOLDERNAME1 = "Vic"
LABEL1 = "Victoria Starlink"
FOLDERNAME2 = "Ott"
LABEL2 = "Ottawa Starlink"

# Boxplot stat types
NONE = -1
AVERAGE = 0
DEVIATION = 1

# Metrics array positions
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

# Graphs boxplot for the metric passed in
def graphBoxPlot(metrics1, metrics2, yLabel, fileName, minm, maxm, step, width, height):
    metrics = {'Victoria Telus 1': metrics1, 'Victoria Telus 2': metrics2}
    plt.figure(figsize =(width, height))
    plt.ylim(minm, maxm)
    plt.yticks(range(minm, maxm, step))
    plt.boxplot(metrics.values(), labels=metrics.keys())
    plt.ylabel(yLabel)
    plt.savefig(fileName + ".svg", format = 'svg', dpi=600)
    plt.clf()
    plt.close()

# Graphs boxplot for the metric passed in
def graphBoxPlotDecimal(metrics1, metrics2, yLabel, fileName, minm, maxm, step, width, height):
    metrics = {LABEL1: metrics1, LABEL2: metrics2}
    plt.figure(figsize =(width, height))  
    plt.ylim(minm, maxm)
    plt.yticks(np.arange(minm, maxm, step))
    plt.boxplot(metrics.values(), labels=metrics.keys())
    plt.ylabel(yLabel)
    plt.savefig(fileName + ".svg", format = 'svg', dpi=600)
    plt.clf()
    plt.close()

# Graphs CDF for the metric passed in
def graphDistr(metrics1, metrics2, xLabel, fileName, minm, maxm, step, width, height):
    plt.figure(figsize =(width, height))
    plt.xlim(minm, maxm)
    plt.xticks(range(minm, maxm, step))
    plt.ylim(0, 1.1)
    plt.yticks(np.arange(0, 1.1, 0.1))
    x1 = np.sort(metrics1)
    y1 = np.arange(len(metrics1) + 1) / float(len(metrics1))
    x1 = np.insert(x1, 0, x1[0] - 1)
    set1 = {}
    for i in range(len(x1)):
        set1[x1[i]] = y1[i]

    x2 = np.sort(metrics2)
    y2 = np.arange(len(metrics2) + 1) / float(len(metrics2))
    x2 = np.insert(x2, 0, x2[0] - 1)
    set2 = {}
    for i in range(len(x2)):
        set2[x2[i]] = y2[i]

    plt.plot(set1.keys(), set1.values(), marker='', label=LABEL1+' CDF', color='red')
    plt.plot(set2.keys(), set2.values(), marker='', label=LABEL2+' CDF', color='blue')
    plt.legend(loc="upper left")
    plt.xlabel(xLabel)
    plt.ylabel('Likelihood of occurrence')
    plt.savefig(fileName + "Distr.svg", format = 'svg', dpi=600)
    plt.margins(0)
    plt.clf()
    plt.close()


# Reads all the raw data from the CSV files in round folders and organizes them into arrays
def extractData(latenciesTime, metricsTime, inputLatencies, pings, packetLosses, usedBandWidths, availableBandwidths, frames, resolutions, totalPacketLosses):
    roundNum = 1

    # Keeps extracting data while the round folders exist
    while roundNum <= 20 :
        try:
            # Enters each round folder and prints it to confirm
            os.chdir(str(roundNum))
            print(os.getcwd())

            roundPacketLosses = []

            # Reads the Latencies(roundNum).csv file
            with open('Latencies' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        latenciesTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        inputLatencies.append(float(row[INPUTLATENCY]))
                    
                    line_count += 1

            # Reads the Metrics(roundNum).csv file
            with open('Metrics' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        metricsTime.append(datetime.strptime(row[TIME][0:19], '%Y-%m-%d %H:%M:%S'))
                        pings.append(int(row[PING]))
                        packetLosses.append(int(row[PACKETLOSS]))
                        roundPacketLosses.append(int(row[PACKETLOSS]))
                        usedBandWidths.append(int(row[USEDBAND]))
                        availableBandwidths.append(int(row[AVAILBAND]))
                        frames.append(int(row[FPS]))
                        resolutions.append(row[RESOLUTION])
                    
                    line_count += 1
            
            totalPacketLosses.append(sum(roundPacketLosses))

            # Exits round folder and moves on to the next
            os.chdir('..')
            roundNum += 1
        
        except FileNotFoundError:
            roundNum += 1
            pass
        

#-------------------------------- Execution ---------------------------------------- 
# Array of metrics
latenciesTime1 = [] # Times from the metrics files
metricsTime1 = [] # Times from the latencies files
pings1 = []
inputLatencies1 = []
packetLosses1 = []
usedBandWidths1 = []
frames1 = []
resolutions1 = []
availableBandwidths1 = []
totalPacketLosses1 = []
packetLossRatios1 = []

latenciesTime2 = [] # Times from the metrics files
metricsTime2 = [] # Times from the latencies files
pings2 = []
inputLatencies2 = []
packetLosses2 = []
usedBandWidths2 = []
frames2 = []
resolutions2 = []
availableBandwidths2 = []
totalPacketLosses2 = []
packetLossRatios2 = []

testNum = 1 
folderNames = [FOLDERNAME1, FOLDERNAME2]
data = {folderNames[0]: [latenciesTime1, metricsTime1, inputLatencies1, pings1, packetLosses1, usedBandWidths1, availableBandwidths1, frames1, resolutions1, totalPacketLosses1], folderNames[1]: [latenciesTime2, metricsTime2, inputLatencies2, pings2, packetLosses2, usedBandWidths2, availableBandwidths2, frames2, resolutions2, totalPacketLosses2]}

for folderName in folderNames:
    os.chdir(folderName)
    os.chdir("Results")
    # Keeps analyzing while the test folders exist
    for i in range(1,5):
    
        # Enters each test folder for analysis
        os.chdir("Test" + str(i))
        extractData(data[folderName][0], data[folderName][1], data[folderName][2], data[folderName][3], data[folderName][4], data[folderName][5], data[folderName][6], data[folderName][7], data[folderName][8], data[folderName][9])

        # Exits the test folder and moves on to the next
        os.chdir('..')
    
    os.chdir('..')
    os.chdir('..')

try:
    os.mkdir("Analysis")
except:
    pass

os.chdir("Analysis")

for totalPacketloss1 in totalPacketLosses1:
    packetLossRatios1.append((totalPacketloss1 / 250000)*100)

for totalPacketloss2 in totalPacketLosses2:
    packetLossRatios2.append((totalPacketloss2 / 250000)*100)




# Graph generation
graphBoxPlot(pings1, pings2, "Ping (ms)", "Pings", 0, 260, 10, 6, 8)
graphDistr(pings1, pings2, "Ping (ms)", "Pings", 0, 260, 10, 11, 9)

graphBoxPlot(inputLatencies1, inputLatencies2, "Input Latency (ms)", "InputLatencies", 0, 260, 10, 6, 8)
graphDistr(inputLatencies1, inputLatencies2, "Input Latency (ms)", "InputLatencies", 0, 260, 10, 11, 9)

graphBoxPlot(usedBandWidths1, usedBandWidths2, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2, 6, 8)
graphDistr(usedBandWidths1, usedBandWidths2, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2, 11, 9)

graphBoxPlot(availableBandwidths1, availableBandwidths2, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10, 6, 8)
graphDistr(availableBandwidths1, availableBandwidths2, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10, 11, 9)

graphBoxPlot(totalPacketLosses1, totalPacketLosses2, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 200, 6, 8)
graphDistr(totalPacketLosses1, totalPacketLosses2, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 200, 11, 9)
graphBoxPlotDecimal(packetLossRatios1, packetLossRatios2, "Total Packet Loss (%)", "PacketLossRatios", 0, 1.1, 0.1, 6, 8)