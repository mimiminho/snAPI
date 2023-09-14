from snAPI.Main import *
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt
import numpy as np

print("Switched to:", matplotlib.get_backend())

if (__name__ == "__main__"):

    sn = snAPI(libType=LibType.MH)
    sn.getDevice()

    # alternatively read data from file
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T2)

    # enable this to get info about loading config
    # sn.setLogLevel(logLevel=LogLevel.Config, onOff=True)
    sn.loadIniConfig("config\MH.ini")

    coincidenceAll = sn.manipulators.coincidence([0, 1], windowTime=1e7, mode=CoincidenceMode.CountAll, keepChannels=True)
    coincidenceOnce = sn.manipulators.coincidence([0, 1], windowTime=1e7, mode=CoincidenceMode.CountOnce, keepChannels=True)
    # measure 10s
    sn.timeTrace.measure(10000, waitFinished=False, savePTU=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    prev_time = None
    counts_sum = [0] * len(counts)

    while True:
        finished = sn.timeTrace.isFinished()
        counts, times = sn.timeTrace.getData()
        ax1.clear()
        ax1.plot(times, counts[0], linewidth=2.0, label='sync')
        ax1.plot(times, counts[1], linewidth=2.0, label='chan1')
        ax1.plot(times, counts[3], linewidth=2.0, label='chan3')
        ax1.set_xlabel('Time [s]')
        ax1.set_ylabel('Counts [Cts/s]')
        ax1.legend()
        ax1.set_title("TimeTrace")
        
        # Calculate and display average counts per second
        if prev_time is not None:
            time_diff = times[-1] - prev_time
            counts_avg = [(count - prev_count) / time_diff for count, prev_count in zip(counts, counts_sum)]
            ax1.annotate(f'Sync Avg: {counts_avg[0]:.2f}', (times[-1], counts[0]), xytext=(5, 0), textcoords='offset points', fontsize=10, color='blue')
            ax1.annotate(f'Chan1 Avg: {counts_avg[1]:.2f}', (times[-1], counts[1]), xytext=(5, 15), textcoords='offset points', fontsize=10, color='green')
            ax1.annotate(f'Chan3 Avg: {counts_avg[3]:.2f}', (times[-1], counts[3]), xytext=(5, 30), textcoords='offset points', fontsize=10, color='red')
            counts_sum = counts.copy()
        
        prev_time = times[-1]

        ax2.clear()
        ax2.plot(times, counts[coincidenceAll], linewidth=2.0, label='coincidenceAll')
        ax2.plot(times, counts[coincidenceOnce], linewidth=2.0, label='coincidenceOnce')
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Counts [Cts/s]')
        ax2.legend()
        ax2.set_title("Coincidence Counts")
        
        # Calculate and display average counts per second for coincidence data
        if prev_time is not None:
            coincidence_avg_all = (counts[coincidenceAll][-1] - counts_sum[coincidenceAll]) / time_diff
            coincidence_avg_once = (counts[coincidenceOnce][-1] - counts_sum[coincidenceOnce]) / time_diff
            ax2.annotate(f'CoincidenceAll Avg: {coincidence_avg_all:.2f}', (times[-1], counts[coincidenceAll][-1]), xytext=(5, 0), textcoords='offset points', fontsize=10, color='blue')
            ax2.annotate(f'CoincidenceOnce Avg: {coincidence_avg_once:.2f}', (times[-1], counts[coincidenceOnce][-1]), xytext=(5, 15), textcoords='offset points', fontsize=10, color='green')
            counts_sum[coincidenceAll] = counts[coincidenceAll][-1]
            counts_sum[coincidenceOnce] = counts[coincidenceOnce][-1]

        plt.pause(0.1)

        if finished:
            break

    plt.show(block=True)
