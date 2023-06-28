import matplotlib, csv, os, statistics
import matplotlib.pyplot as plt
import scapy
from scapy.all import *

NONE = -1
AVERAGE = 0
DEVIATION = 1

PING = 1
PACKETLOSS = 2
INPUTLATENCY = 3

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
                    pings.append(float(row[PING]))
                    roundPings.append(float(row[PING]))
                    packetLosses.append(float(row[PACKETLOSS]))
                    roundPacketLosses.append(float(row[PACKETLOSS]))
                    inputLatencies.append(float(row[INPUTLATENCY]))
                    roundInputLatencies(float(row[INPUTLATENCY]))
                
                line_count += 1
            
            storeStats(pingStats, roundPings)
            storeStats(inputLatencyStats, roundInputLatencies)
            totalPacketLosses.append(sum(roundInputLatencies))
        
        
        os.chdir('..')
        i += 1
        
    except FileNotFoundError:
        exists = False





graphBoxPlot(pings, NONE, "Ping (ms)", "Pings", 0, 160, 10)
graphBoxPlot(pingStats, AVERAGE, "Ping (ms)", "PingAverages", 0, 160, 10)
graphBoxPlot(pingStats, DEVIATION, "Ping (ms)", "PingDeviations", 0, 110, 10)

graphBoxPlot(inputLatencies, NONE, "Input Latency (ms)", "InputLatencies", 0, 260, 10)
graphBoxPlot(inputLatencyStats, AVERAGE, "Input Latency (ms)", "InputLatencyAverages", 0, 260, 10)
graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency (ms)", "InputLatencyDeviations", 0, 210, 10)

graphBoxPlot(totalPacketLosses, NONE, "Packet Loss", "TotalPacketLoss", 0, 2100, 100)






