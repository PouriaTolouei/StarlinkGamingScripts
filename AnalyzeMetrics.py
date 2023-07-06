import matplotlib, csv, os, statistics
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates

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

resolutionLabels = ['480 x 360 (16:9)', '960 x 540 (16:9)', '1280 x 720 (16:9)', '1366 x 768 (16:9)', '1600 x 900 (16:9)', '1920 x 1080 (16:9)']

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

    for i in range(len(metricsTimeSeconds)):
        totalPacketLossAtSeconds[metricsTimeSeconds[i]] += packetLosses[i]
        pingsAtSeconds[metricsTimeSeconds[i]].append(pings[i])
        availableBandwidthsAtSeconds[metricsTimeSeconds[i]].append(availableBandwidths[i])

    for i in range (len(latenciesTimeSeconds)):
        inputLatenciesAtSeconds[latenciesTimeSeconds[i]].append(inputLatencies[i])

    for i in range(len(seconds)):
        averagePingAtSeconds.append(statistics.mean(pingsAtSeconds[i]))
        averageInputLatencyAtSeconds.append(statistics.mean(inputLatenciesAtSeconds[i]))
        averageAvailableBandwidthAtSeconds.append(statistics.mean(availableBandwidthsAtSeconds[i]))

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
def graphBar(metrics, ylabel, fileName, minm, maxm, step):
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

# Graphs a bar graph of the observed resolutions 
def graphResolutionBar():
    resolutionsCount = {}
    for label in resolutionLabels:
        resolutionsCount[label] = 0

    for resolution in resolutions:
        resolutionsCount[resolution] += 1

    counts = list(resolutionsCount.values())

    plt.figure(figsize =(20, 14))
    plt.bar(resolutionLabels, counts)
    plt.xlabel("Resolution")
    plt.ylabel("Frequency")
    plt.savefig("ResolutionsBar.jpg")
    plt.clf()
    plt.close()


# Reads all the raw data from the CSV files in round folders and organizes them into arrays
def extractData():
    exists = True
    roundNum = 1

    while exists:
        try:
            os.chdir(str(roundNum))
            print(os.getcwd())

            roundPings = []
            roundPacketLosses = []
            roundInputLatencies = []
            roundUsedBandwidths = []
            roundAvailableBandwidths = []

            with open('Latencies' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        latenciesTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        inputLatencies.append(float(row[INPUTLATENCY]))
                        roundInputLatencies.append(float(row[INPUTLATENCY]))
                    
                    line_count += 1

            with open('Metrics' + str(roundNum) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        metricsTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        pings.append(int(row[PING]))
                        roundPings.append(int(row[PING]))
                        packetLosses.append(int(row[PACKETLOSS]))
                        roundPacketLosses.append(int(row[PACKETLOSS]))
                        usedBandWidths.append(int(row[USEDBAND]))
                        roundUsedBandwidths.append(int(row[USEDBAND]))
                        availableBandwidths.append(int(row[AVAILBAND]))
                        roundAvailableBandwidths.append(int(row[AVAILBAND]))
                        resolutions.append(row[RESOLUTION])
                    
                    line_count += 1
            
            storeStats(pingStats, roundPings)
            storeStats(inputLatencyStats, roundInputLatencies)
            storeStats(usedBandwidthStats, roundUsedBandwidths)
            storeStats(availableBandwidthStats, roundAvailableBandwidths)
            totalPacketLosses.append(sum(roundPacketLosses))
            os.chdir('..')
            roundNum += 1
            
            
        except FileNotFoundError:
            exists = False
        

    organizeDataBySecond()


#-------------------------------- Execution ---------------------------------------- 
exists = True
testNum = 1 
os.chdir("Results")
while exists:
    try:

        # Array of metrics
        latenciesTime = [] # Times from the metrics files
        metricsTime = [] # Times from the latencies files
        pings = []
        inputLatencies = []
        packetLosses = []
        usedBandWidths = []
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
        seconds = list(range(0, 60))
        # Array of data oragnized by seconds in a minute
        totalPacketLossAtSeconds = []
        pingsAtSeconds = []
        averagePingAtSeconds = []
        inputLatenciesAtSeconds = []
        averageInputLatencyAtSeconds = []
        availableBandwidthsAtSeconds = []
        averageAvailableBandwidthAtSeconds = []

        os.chdir("Test" + str(testNum))
        extractData()

        graphBoxPlot(pings, NONE, "Ping (ms)", "Pings", 0, 260, 10)
        # graphBoxPlot(pingStats, AVERAGE, "Average Ping (ms)", "PingAverages", 0, 260, 10)
        graphBoxPlot(pingStats, DEVIATION, "Ping Standard Deviation (ms)", "PingDeviations", 0, 110, 10)
        graphDistr(pings, "Ping (ms)", "Pings", 0, 260, 10)
        graphBar(averagePingAtSeconds, "Average Ping (ms)", "AveragePing", 0, 85, 5)

        graphBoxPlot(inputLatencies, NONE, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
        # graphBoxPlot(inputLatencyStats, AVERAGE, "Average Input Latency (ms)", "InputLatencyAverages", 0, 260, 10)
        graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency Standard Deviation (ms)", "InputLatencyDeviations", 0, 210, 10)
        graphDistr(inputLatencies, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
        graphBar(averageInputLatencyAtSeconds, "Average Input Latency (ms)", "AverageInputLatency", 0, 190, 10)

        graphBoxPlot(usedBandWidths, NONE, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2)
        # graphBoxPlot(usedBandwidthStats, AVERAGE, "Average Used BandWidth (Mbps)", "UsedBandwidthAverages", 0, 52, 2)
        graphBoxPlot(usedBandwidthStats, DEVIATION, "Used BandWidth Standard Deviation (Mbps)", "UsedBandwidthDeviations", 0, 20, 1)
        graphDistr(usedBandWidths, "Used BandWidth (Mbps)", "UsedBandwidths", 0, 52, 2)

        graphBoxPlot(availableBandwidths, NONE, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10)
        # graphBoxPlot(availableBandwidthStats, AVERAGE, "Average Available BandWidth (Mbps)", "AvailableBandwidthAverages", 0, 105, 5)
        graphBoxPlot(availableBandwidthStats, DEVIATION, "Used BandWidth Standard Deviation (Mbps)", "AvailableBandwidthDeviations", 0, 50, 2)
        graphDistr(availableBandwidths, "Available BandWidth (Mbps)", "AvailableBandwidths", 0, 160, 10)
        graphBar(averageAvailableBandwidthAtSeconds, "Average Available BandWidth (Mbps)", "AverageAvailableBandwidth", 0, 160, 10)

        graphBoxPlot(totalPacketLosses, NONE, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
        graphDistr(totalPacketLosses, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
        graphBar(totalPacketLossAtSeconds, "Total Packet Loss", "TotalPacketLoss", 0, 1100, 100)

        graphResolutionBar()

        os.chdir('..')
        testNum += 1
    
    except FileNotFoundError:
        exists = False














