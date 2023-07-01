import matplotlib, csv, os, statistics
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates
from astropy.visualization import hist

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

# Array of metrics
latenciesTime = [] # Times from the metrics files
metricsTime = [] # Times from the latencies files
pings = []
inputLatencies = []
packetLosses = []

# Array of metric stats
pingStats = [[], []]
inputLatencyStats = [[], []]
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

    for i in range(len(metricsTimeSeconds)):
        totalPacketLossAtSeconds[metricsTimeSeconds[i]] += packetLosses[i]
        pingsAtSeconds[metricsTimeSeconds[i]].append(pings[i])

    for i in range (len(latenciesTimeSeconds)):
        inputLatenciesAtSeconds[latenciesTimeSeconds[i]].append(inputLatencies[i])

    for i in range(len(seconds)):
        averagePingAtSeconds.append(statistics.mean(pingsAtSeconds[i]))
        averageInputLatencyAtSeconds.append(statistics.mean(inputLatenciesAtSeconds[i]))

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

# Reads all the raw data from the CSV files in round folders and organizes them into arrays
def extractData():
    exists = True
    i = 1
    j = 1

    while exists:
        try:
            os.chdir("Test" + str(i) + "/" + str(j))
            print(os.getcwd())

            roundPings = []
            roundPacketLosses = []
            roundInputLatencies = []

            with open('Latencies' + str(i) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        latenciesTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        inputLatencies.append(float(row[INPUTLATENCY]))
                        roundInputLatencies.append(float(row[INPUTLATENCY]))
                    
                    line_count += 1

            with open('Metrics' + str(i) + '.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        metricsTime.append(datetime.strptime(row[TIME], '%Y-%m-%d %H:%M:%S.%f'))
                        pings.append(float(row[PING]))
                        roundPings.append(float(row[PING]))
                        packetLosses.append(float(row[PACKETLOSS]))
                        roundPacketLosses.append(float(row[PACKETLOSS]))
                    
                    line_count += 1
            
            storeStats(pingStats, roundPings)
            storeStats(inputLatencyStats, roundInputLatencies)
            totalPacketLosses.append(sum(roundPacketLosses))
            os.chdir('..')
            j += 1
            
            
        except FileNotFoundError:
            i += 1
            if os.path.exists("/home/pouriatolouei/Documents/StarLinkGamingScripts/Results/Test" + str(i)) == False:
                exists = False
        

    organizeDataBySecond()


#-------------------------------- Execution ---------------------------------------- 

extractData()

graphBoxPlot(pings, NONE, "Ping (ms)", "Pings", 0, 260, 10)
graphBoxPlot(pingStats, AVERAGE, "Average Ping (ms)", "PingAverages", 0, 260, 10)
graphBoxPlot(pingStats, DEVIATION, "Ping Standard Deviation (ms)", "PingDeviations", 0, 110, 10)
graphDistr(pings, "Ping (ms)", "Pings", 0, 260, 10)
graphBar(averagePingAtSeconds, "Average Ping (ms)", "AveragePing", 0, 85, 5)

graphBoxPlot(inputLatencies, NONE, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
graphBoxPlot(inputLatencyStats, AVERAGE, "Average Input Latency (ms)", "InputLatencyAverages", 0, 260, 10)
graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency Standard Deviation (ms)", "InputLatencyDeviations", 0, 210, 10)
graphDistr(inputLatencies, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
graphBar(averageInputLatencyAtSeconds, "Average Input Latency (ms)", "AverageInputLatency", 0, 190, 10)

graphBoxPlot(totalPacketLosses, NONE, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
graphDistr(totalPacketLosses, "Total Packet Loss", "TotalPacketLoss", 0, 3600, 100)
graphBar(totalPacketLossAtSeconds, "Total Packet Loss", "TotalPacketLoss", 0, 1100, 100)












