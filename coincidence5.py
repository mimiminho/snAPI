from snAPI.Main import *
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt
from time import time, sleep
print("Switched to:", matplotlib.get_backend())

if __name__ == "__main__":
    sn = snAPI(libType=LibType.MH)
    sn.getDevice()

    # alternatively read data from file
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T2)

    # enable this to get info about loading config
    # sn.setLogLevel(logLevel=LogLevel.Config, onOff=True)
    sn.loadIniConfig("config\MH.ini")

    coincidenceAll = sn.manipulators.coincidence([0, 1], windowTime=1e-4, mode=CoincidenceMode.CountAll, keepChannels=True)
    coincidenceOnce = sn.manipulators.coincidence([0, 1], windowTime=250, mode=CoincidenceMode.CountOnce, keepChannels=True)
    
    # Initialize variables for calculating 1-second average coincidence counts
    avg_coincidence_all = 0
    avg_coincidence_once = 0
    count_all = 0
    count_once = 0
    start_time = time()

    # measure 10s
    sn.timeTrace.measure(10000, waitFinished=False, savePTU=False)

    while True:
        finished = sn.timeTrace.isFinished()
        counts, times = sn.timeTrace.getData()
        
        # Calculate coincidence counts within the last second
        current_time = time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1.0:
            avg_coincidence_all = count_all / elapsed_time
            avg_coincidence_once = count_once / elapsed_time
            start_time = current_time
            count_all = 0
            count_once = 0
        
        count_all += sum(counts[coincidenceAll])
        count_once += sum(counts[coincidenceOnce])

        plt.clf()
        plt.plot(times, counts[0], linewidth=2.0, label='sync')
        plt.plot(times, counts[1], linewidth=2.0, label='chan1')
        plt.plot(times, counts[3], linewidth=2.0, label='chan3')
        plt.plot(times, counts[coincidenceAll], linewidth=2.0, label='coincidenceAll')
        plt.plot(times, counts[coincidenceOnce], linewidth=2.0, label='coincidenceOnce')

        plt.xlabel('Time [s]')
        plt.ylabel('Counts[Cts/s]')

        # Display 1-second average coincidence counts on the plot
        plt.text(0.1, 0.9, f'Avg Coincidence (All): {avg_coincidence_all:.2f} Cts/s', transform=plt.gca().transAxes)
        plt.text(0.1, 0.8, f'Avg Coincidence (Once): {avg_coincidence_once:.2f} Cts/s', transform=plt.gca().transAxes)

        plt.legend()
        plt.title("TimeTrace")
        plt.pause(0.1)

        if finished:
            break

    plt.show(block=True)
