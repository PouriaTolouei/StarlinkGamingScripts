import matplotlib, csv, os, statistics
import matplotlib.pyplot as plt

AVERAGE = 0
DEVIATION = 1

PING = 1
PACKETLOSS = 2
INPUTLATENCY = 3

pingStats = [[], [], []]

packetLossStats = [[], [], []]

inputLatencyStats = [[], [], []]

def storeStats(stats, metrics):
    stats[0].append(statistics.mean(metrics))
    stats[1].append(statistics.stdev(metrics))

def graphBoxPlot(stats, statType, yLabel, fileName, min, max, step):
    plt.figure(figsize =(20, 14))
    plt.ylim(min, max)
    plt.yticks(range(min, max, step))
    plt.boxplot(stats[statType])
    plt.ylabel(yLabel)
    plt.savefig(fileName + ".jpg")

exists = True
i = 1

while exists:
    try:
        pings = []
        packetLosses = []
        inputLatencies = []

        os.chdir(str(i))
        print(os.getcwd())

        with open('Latencies' + str(i) + '.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    pings.append(float(row[PING]))
                    packetLosses.append(float(row[PACKETLOSS]))
                    inputLatencies.append(float(row[INPUTLATENCY]))
                
                line_count += 1
            

            storeStats(pingStats, pings)
            storeStats(packetLossStats, packetLosses)
            storeStats(inputLatencyStats, inputLatencies)
        
        os.chdir('..')
        i += 1
        
    except FileNotFoundError:
        exists = False

graphBoxPlot(pingStats, AVERAGE, "Ping (ms)", "PingAverages", 20, 130, 10)
graphBoxPlot(pingStats, DEVIATION, "Ping (ms)", "PingDeviations", 0, 110, 10)

graphBoxPlot(inputLatencyStats, AVERAGE, "Input Latency (ms)", "InputLatencyAverages", 40, 210, 10)
graphBoxPlot(inputLatencyStats, DEVIATION, "Input Latency (ms)", "InputLatencyDeviations", 0, 210, 10)

# graphBoxPlot(inputLatencyStats, AVERAGE, "Packet Loss", "PacketLossAverages", -1, 11, 1)
# graphBoxPlot(inputLatencyStats, DEVIATION, "Packet Loss", "PacketLossDeviations", 0, 110, 10)






