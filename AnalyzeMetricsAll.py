import csv, os, statistics
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

#------------------------- Variables and Constants  ------------------------------ 
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

# Categories 
resolutionCategories = ['480 x 360 (16:9)', '960 x 540 (16:9)', '1280 x 720 (16:9)', '1366 x 768 (16:9)', '1600 x 900 (16:9)', '1920 x 1080 (16:9)']
fpsCategories = list(range(0, 91))
seconds = list(range(0, 60))

#-------------------------------- Methods ---------------------------------------- 

# For each metrics passed in, it calculates and stores the mean and standard deviation
def storeStats(stats, metrics):
    stats[0].append(statistics.mean(metrics))
    stats[1].append(statistics.stdev(metrics))

# Organize and store total packet losses, average pings, and average input latencies by seconds in a minute
def organizeDataBySecond():
    for time in metricsTime:
        metricsTimeSeconds.append(time.time().second)

    for time in latenciesTime:
        latenciesTimeSeconds.append(time.time().second)

    for i in range (60):
        totalPacketLossAtSeconds.append(0)
        pingsAtSeconds.append([])
        inputLatenciesAtSeconds.append([])
        availableBandwidthsAtSeconds.append([])
        usedBandwidthAtSeconds.append([])

    for i in range(len(metricsTimeSeconds)):
        totalPacketLossAtSeconds[metricsTimeSeconds[i]] += packetLosses[i]
        pingsAtSeconds[metricsTimeSeconds[i]].append(pings[i])
        availableBandwidthsAtSeconds[metricsTimeSeconds[i]].append(availableBandwidths[i])
        usedBandwidthAtSeconds[metricsTimeSeconds[i]].append(usedBandWidths[i])

    for i in range (len(latenciesTimeSeconds)):
        inputLatenciesAtSeconds[latenciesTimeSeconds[i]].append(inputLatencies[i])

    for i in range(len(seconds)):
        averagePingAtSeconds.append(statistics.mean(pingsAtSeconds[i]))
        averageInputLatencyAtSeconds.append(statistics.mean(inputLatenciesAtSeconds[i]))
        averageAvailableBandwidthAtSeconds.append(statistics.mean(availableBandwidthsAtSeconds[i]))
        averageUsedBandwidthAtSeconds.append(statistics.mean(usedBandwidthAtSeconds[i]))

# Graphs boxplot for the metric passed in
def graphBoxPlot(stats, statType, yLabel, fileName, minm, maxm, step):
    plt.figure(figsize =(20, 14))
    plt.ylim(minm, maxm)
    plt.yticks(range(minm, maxm, step))
    if statType == NONE:
        plt.boxplot(stats)
    else:
        plt.boxplot(stats[statType])
    plt.ylabel(yLabel)
    plt.savefig(fileName + ".jpg")
    plt.clf()
    plt.close()

# Graphs CDF for the metric passed in
def graphDistr(metrics, xLabel, fileName, minm, maxm, step):
    plt.figure(figsize =(20, 14))
    plt.xlim(minm, maxm)
    plt.xticks(range(minm, maxm, step))
    plt.ylim(0, 1.1)
    plt.yticks(np.arange(0, 1.1, 0.1))
    x = np.sort(metrics)
    y = np.arange(len(metrics) + 1) / float(len(metrics))
    x = np.insert(x, 0, x[0] - 1)
    plt.plot(x, y, marker='o', label='CDF')
    plt.legend(loc="upper left")
    plt.xlabel(xLabel)
    plt.ylabel('Likelihood of occurrence')
    plt.savefig(fileName + "Distr.jpg")
    plt.margins(0)
    plt.clf()
    plt.close()

#  Graphs bar graphs forshowing metrics by seconds in a minute
def graphSecondsBar(metrics, ylabel, fileName, minm, maxm, step): 
    plt.figure(figsize =(20, 14))
    plt.xlim(-1, 60)
    plt.xticks(range(0, 60, 1))
    plt.ylim(minm, maxm)
    plt.yticks(range(minm, maxm, step))
    plt.bar(seconds, metrics)
    plt.xlabel("Second")
    plt.ylabel(ylabel)
    plt.savefig(fileName + "AtSeconds.jpg")
    plt.clf()
    plt.close()

# Graphs a bar graph with the categories of the metric passed in 
def graphBar(metrics, categories, xLabel, fileName):
    # Counts the categories of the metrics
    categoriesCount = {}
    for category in categories:
        categoriesCount[category] = 0
    for metric in metrics:
        categoriesCount[metric] += 1
    counts = list(categoriesCount.values())

    plt.figure(figsize =(20, 14))
    plt.bar(categories, counts)
    plt.xlabel(xLabel)
    plt.ylabel("Frequency")
    plt.savefig(fileName + ".jpg")
    plt.clf()
    plt.close()


# Reads all the raw data from the CSV files in round folders and organizes them into arrays
def extractData():
    roundNum = 1

    # Keeps extracting data while the round folders exist
    while roundNum <= 20 :
        try:
            # Enters each round folder and prints it to confirm
            os.chdir(str(roundNum))
            print(os.getcwd())

            # Temporary round arrays used for average and standard deviation calculations
            roundPings = []
            roundPacketLosses = []
            roundInputLatencies = []
            roundUsedBandwidths = []
            roundAvailableBandwidths = []

            # Reads the Latencies(roundNum).csv file
            with open('Latencies' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        latenciesTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        inputLatencies.append(float(row[INPUTLATENCY]))
                        roundInputLatencies.append(float(row[INPUTLATENCY]))
                    
                    line_count += 1

            # Reads the Metrics(roundNum).csv file
            with open('Metrics' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        metricsTime.append(datetime.strptime(row[TIME][0:19], '%Y-%m-%d %H:%M:%S'))
                        pings.append(int(row[PING]))
                        roundPings.append(int(row[PING]))
                        packetLosses.append(int(row[PACKETLOSS]))
                        roundPacketLosses.append(int(row[PACKETLOSS]))
                        usedBandWidths.append(int(row[USEDBAND]))
                        roundUsedBandwidths.append(int(row[USEDBAND]))
                        availableBandwidths.append(int(row[AVAILBAND]))
                        roundAvailableBandwidths.append(int(row[AVAILBAND]))
                        frames.append(int(row[FPS]))
                        resolutions.append(row[RESOLUTION])
                    
                    line_count += 1
            
            # Calculates and stores the stats
            storeStats(pingStats, roundPings)
            storeStats(inputLatencyStats, roundInputLatencies)
            storeStats(usedBandwidthStats, roundUsedBandwidths)
            storeStats(availableBandwidthStats, roundAvailableBandwidths)
            totalPacketLosses.append(sum(roundPacketLosses))

            # Exits round folder and moves on to the next
            os.chdir('..')
            roundNum += 1
        
        except FileNotFoundError:
            roundNum += 1
            pass
        

#-------------------------------- Execution ---------------------------------------- 
exists = True
testNum = 1 
groupNum = 1

# Enters the Results folder
os.chdir("Results")

while exists:
    # Array of metrics
    latenciesTime = [] # Times from the metrics files
    metricsTime = [] # Times from the latencies files
    pings = []
    inputLatencies = []
    packetLosses = []
    usedBandWidths = []
    frames = []
    resolutions = []
    availableBandwidths = []

    # Array of metric stats
    pingStats = [[], []]
    inputLatencyStats = [[], []]
    usedBandwidthStats = [[], []]
    availableBandwidthStats = [[], []]
    totalPacketLosses = []

    # Array of seconds
    metricsTimeSeconds = []
    latenciesTimeSeconds = []

    # Array of data oragnized by seconds in a minute
    totalPacketLossAtSeconds = []
    pingsAtSeconds = []
    averagePingAtSeconds = []
    inputLatenciesAtSeconds = []
    averageInputLatencyAtSeconds = []
    availableBandwidthsAtSeconds = []
    averageAvailableBandwidthAtSeconds = []
    usedBandwidthAtSeconds = []
    averageUsedBandwidthAtSeconds = []
    
    # Keeps analyzing while the test folders exist
    for i in range(4):
        try:
            # Enters each test folder for analysis
            os.chdir("Test" + str(testNum))
            extractData()

            # Exits the test folder and moves on to the next
            os.chdir('..')
            testNum += 1
        
        except FileNotFoundError:
            # Stops the analysis as no more test folders exist
            exists = False

    if exists:
        organizeDataBySecond()
        try:
            os.mkdir("Analysis" + str(groupNum))
        except:
            pass
        
        os.chdir("Analysis" + str(groupNum))

        # Graph generation
        graphBoxPlot(pings, NONE, "Ping (ms)", "Pings", 0, 260, 10)
        # graphBoxPlot(pingStats, AVERAGE, "Average Ping (ms)", "PingAverages", 0, 260, 10)
        graphBoxPlot(pingStats, DEVIATION, "Ping Standard Deviation (ms)", "PingDeviations", 0, 110, 10)
        graphDistr(pings, "Ping (ms)", "Pings", 0, 260, 10)
        graphSecondsBar(averagePingAtSeconds, "Average Ping (ms)", "AveragePing", 0, 85, 5)

        graphBoxPlot(inputLatencies, NONE, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
        # graphBoxPlot(inputLatencyStats, AVERAGE, "Average Input Latency (ms)", "InputLatencyAverages", 0, 260, 10)
        graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency Standard Deviation (ms)", "InputLatencyDeviations", 0, 210, 10)
        graphDistr(inputLatencies, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
        graphSecondsBar(averageInputLatencyAtSeconds, "Average Input Latency (ms)", "AverageInputLatency", 0, 190, 10)

        graphBoxPlot(usedBandWidths, NONE, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2)
        # graphBoxPlot(usedBandwidthStats, AVERAGE, "Average Used BandWidth (Mbps)", "UsedBandwidthAverages", 0, 52, 2)
        graphBoxPlot(usedBandwidthStats, DEVIATION, "Used BandWidth Standard Deviation (Mbps)", "UsedBandwidthDeviations", 0, 20, 1)
        graphDistr(usedBandWidths, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2)
        graphSecondsBar(averageUsedBandwidthAtSeconds, "Average Used BandWidth (Mbps)", "AverageUsedBandwidth", 0, 52, 2)

        graphBoxPlot(availableBandwidths, NONE, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10)
        # graphBoxPlot(availableBandwidthStats, AVERAGE, "Average Available BandWidth (Mbps)", "AvailableBandwidthAverages", 0, 105, 5)
        graphBoxPlot(availableBandwidthStats, DEVIATION, "Used BandWidth Standard Deviation (Mbps)", "AvailableBandwidthDeviations", 0, 50, 2)
        graphDistr(availableBandwidths, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10)
        graphSecondsBar(averageAvailableBandwidthAtSeconds, "Average Available BandWidth (Mbps)", "AverageAvailableBandwidth", 0, 160, 10)

        graphBoxPlot(totalPacketLosses, NONE, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
        graphDistr(totalPacketLosses, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
        graphSecondsBar(totalPacketLossAtSeconds, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)

        graphBar(resolutions, resolutionCategories, "Resolution", "Resolutions")
        graphBar(frames, fpsCategories, "FPS", "FPS")

        statFile = open("Stats.txt", "w+")
        statFile.write(f"Ping (Mean/Median/SD): {statistics.mean(pings)}/{statistics.median(pings)}/{statistics.stdev(pings)}\n")
        statFile.write(f"Input Latency (Mean/Median/SD): {statistics.mean(inputLatencies)}/{statistics.median(inputLatencies)}/{statistics.stdev(inputLatencies)}\n")
        statFile.write(f"Round Total Packetloss (Mean/Median/SD): {statistics.mean(totalPacketLosses)}/{statistics.median(totalPacketLosses)}/{statistics.stdev(totalPacketLosses)}")
        statFile.close()

        groupNum += 1
        os.chdir('..')