from snAPI.Main import *
import tkinter as tk
from tkinter import ttk

def update_display():
    counts, _ = sn.timeTrace.getData() 
    sync_label.config(text="Sync Counts: {}".format(counts[0]))
    chan1_label.config(text="Channel 1 Counts: {}".format(counts[1]))
    chan3_label.config(text="Channel 3 Counts: {}".format(counts[3]))
    coincidenceAll_label.config(text="Coincidence All Counts: {}".format(counts[coincidenceAll]))
    coincidenceOnce_label.config(text="Coincidence Once Counts: {}".format(counts[coincidenceOnce]))
    root.after(100, update_display)  # 업데이트 주기 (밀리초 단위)

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
    
    root = tk.Tk()
    root.title("Real-time Data Display")
    
    sync_label = ttk.Label(root, text="Sync Counts: 0")
    sync_label.pack()
    
    chan1_label = ttk.Label(root, text="Channel 1 Counts: 0")
    chan1_label.pack()
    
    chan3_label = ttk.Label(root, text="Channel 3 Counts: 0")
    chan3_label.pack()
    
    coincidenceAll_label = ttk.Label(root, text="Coincidence All Counts: 0")
    coincidenceAll_label.pack()
    
    coincidenceOnce_label = ttk.Label(root, text="Coincidence Once Counts: 0")
    coincidenceOnce_label.pack()
    
    update_display()
    root.mainloop()
