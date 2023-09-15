from snAPI.Main import *
import matplotlib
matplotlib.use('TkAgg',force=True)
from matplotlib import pyplot as plt
print("Switched to:",matplotlib.get_backend())

if __name__ == "__main__":
    sn = snAPI(libType=LibType.MH)
    sn.getDevice()
    
    # alternatively read data from file
    sn.setLogLevel(LogLevel.DataFile, True)
    sn.initDevice(MeasMode.T2)
    
    # enable this to get info about loading config
    #sn.setLogLevel(logLevel=LogLevel.Config, onOff=True)
    sn.loadIniConfig("config\MH.ini")
    
    coincidenceAll = sn.manipulators.coincidence([0,1], windowTime=1e-4, mode=CoincidenceMode.CountAll, keepChannels=True)
    coincidenceOnce = sn.manipulators.coincidence([0,1], windowTime=250, mode=CoincidenceMode.CountOnce, keepChannels=True)
    # measure 10s
    sn.timeTrace.measure(10000, waitFinished=False, savePTU=False)
    
    while True: 
        finished = sn.timeTrace.isFinished()
        counts, times = sn.timeTrace.getData() 
        plt.clf()
        plt.plot(times, counts[0], linewidth=2.0, label='sync')
        plt.plot(times, counts[1], linewidth=2.0, label='chan1')
        plt.plot(times, counts[3], linewidth=2.0, label='chan3')
        plt.plot(times, counts[coincidenceAll], linewidth=2.0, label='coincidenceAll')
        plt.plot(times, counts[coincidenceOnce], linewidth=2.0, label='coincidenceOnce')

        plt.xlabel('Time [s]')
        plt.ylabel('Counts[Cts/s]')
        plt.legend()
        plt.title("TimeTrace")
        plt.pause(0.1)
        
        if finished:
            break
    
    # Calculate and display the average count per second
    average_count = sum(counts[coincidenceAll]) / 10.0  # Assuming 10 seconds measurement
    print(f"Average Count per Second: {average_count}")

    plt.show(block=True)
