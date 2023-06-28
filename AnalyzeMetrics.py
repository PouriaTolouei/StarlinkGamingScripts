import matplotlib, csv, os, statistics
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates


NONE = -1
AVERAGE = 0
DEVIATION = 1

SEC = 0
TIME = 1
PING = 2
PACKETLOSS = 3

INPUTLATENCY = 4

FPS = 4
USEDBAND = 5
RESOLUTION = 6

latenciesTime = []
metricsTime = []
pings = []
inputLatencies = []
packetLosses = []

pingStats = [[], []]
inputLatencyStats = [[], []]
totalPacketLosses = []


def storeStats(stats, metrics):
    stats[0].append(statistics.mean(metrics))
    stats[1].append(statistics.stdev(metrics))

def graphBoxPlot(stats, statType, yLabel, fileName, min, max, step):
    plt.figure(figsize =(20, 14))
    plt.ylim(min, max)
    plt.yticks(range(min, max, step))
    if statType == NONE:
        plt.boxplot(stats)
    else:
        plt.boxplot(stats[statType])
    plt.ylabel(yLabel)
    plt.savefig(fileName + ".jpg")
    plt.clf()

def graphDistr(metrics, fileName):
    plt.figure(figsize =(20, 14))
    count, bins_count = np.histogram(metrics)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], pdf, color="red", label="PDF")
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
    plt.savefig(fileName + "Distr.jpg")
    plt.margins(0)
    plt.clf()

def extractData():
    exists = True
    i = 1

    while exists:
        try:
            os.chdir(str(i))
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
            i += 1
            
        except FileNotFoundError:
            exists = False


extractData()
graphBoxPlot(pings, NONE, "Ping (ms)", "Pings", 0, 160, 10)
graphBoxPlot(pingStats, AVERAGE, "Ping (ms)", "PingAverages", 0, 160, 10)
graphBoxPlot(pingStats, DEVIATION, "Ping (ms)", "PingDeviations", 0, 110, 10)
graphDistr(pings, "Pings")

graphBoxPlot(inputLatencies, NONE, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
graphBoxPlot(inputLatencyStats, AVERAGE, "Input Latency (ms)", "InputLatencyAverages", 0, 260, 10)
graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency (ms)", "InputLatencyDeviations", 0, 210, 10)
graphDistr(inputLatencies, "InputLatencies")

graphBoxPlot(totalPacketLosses, NONE, "Packet Loss", "TotalPacketLoss", 0, 2100, 100)
graphDistr(totalPacketLosses, "TotalPacketLoss")









