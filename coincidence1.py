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

        ax2.clear()
        ax2.plot(times, counts[coincidenceAll], linewidth=2.0, label='coincidenceAll')
        ax2.plot(times, counts[coincidenceOnce], linewidth=2.0, label='coincidenceOnce')
        ax2.set_xlabel('Time [s]')
        ax2.set_ylabel('Counts [Cts/s]')
        ax2.legend()
        ax2.set_title("Coincidence Counts")

        plt.pause(0.1)

        if finished:
            break

    plt.show(block=True)
