from snAPI.Main import *
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt
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
    # measure 10s
    sn.timeTrace.measure(10000, waitFinished=False, savePTU=False)

    # Create two subplots
    fig, axs = plt.subplots(2)

    while True:
        finished = sn.timeTrace.isFinished()
        counts, times = sn.timeTrace.getData()
        
        # Plot data on the first subplot (bar chart)
        axs[0].cla()
        axs[0].bar(['sync', 'chan1', 'chan3', 'coincidenceAll', 'coincidenceOnce'], counts[-1], color=['r', 'g', 'b', 'c', 'm'])
        axs[0].set_ylabel('Counts[Cts/s]')
        axs[0].set_title('Bar Chart')

        # Plot data on the second subplot (line chart)
        axs[1].cla()
        axs[1].plot(times, counts[0], 'r-', linewidth=2.0, label='sync')
        axs[1].plot(times, counts[1], 'g-', linewidth=2.0, label='chan1')
        axs[1].plot(times, counts[3], 'b-', linewidth=2.0, label='chan3')
        axs[1].plot(times, counts[coincidenceAll], 'c-', linewidth=2.0, label='coincidenceAll')
        axs[1].plot(times, counts[coincidenceOnce], 'm-', linewidth=2.0, label='coincidenceOnce')
        axs[1].set_xlabel('Time [s]')
        axs[1].set_ylabel('Counts[Cts/s]')
        axs[1].legend()
        axs[1].set_title('Line Chart')

        plt.pause(0.05)

        if finished:
            break

    # Calculate average_count
    average_count = sum(counts[coincidenceOnce]) / 10.0  # Assuming 10 seconds measurement

    # Create a new window to display average_count
    plt.figure()
    plt.text(0.5, 0.5, f'Average Count per Second: {average_count}', fontsize=12, ha='center', va='center')
    plt.axis('off')
    plt.show()
