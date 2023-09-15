from snAPI.Main import *
import matplotlib
matplotlib.use('TkAgg', force=True)
from matplotlib import pyplot as plt
from time import time, sleep  # 추가된 import 문
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

    start_time = time()  # 시작 시간 기록
    avg_coincidence_all = 0.0  # 초기 값 설정
    avg_coincidence_once = 0.0  # 초기 값 설정

    while True:
        finished = sn.timeTrace.isFinished()
        counts, times = sn.timeTrace.getData()

        if time() - start_time >= 0.1:  # 0.1초마다 업데이트
            avg_coincidence_all = sum(counts[coincidenceAll]) / (time() - start_time)  # 누적 카운트를 시간으로 나누어 평균 계산
            avg_coincidence_once = sum(counts[coincidenceOnce]) / (time() - start_time)  # 누적 카운트를 시간으로 나누어 평균 계산
            start_time = time()  # 시작 시간 업데이트

        plt.clf()
        plt.plot(times, counts[0], linewidth=2.0, label='sync')
        plt.plot(times, counts[1], linewidth=2.0, label='chan1')
        plt.plot(times, counts[3], linewidth=2.0, label='chan3')
        plt.plot(times, counts[coincidenceAll], linewidth=2.0, label='coincidenceAll')
        plt.plot(times, counts[coincidenceOnce], linewidth=2.0, label='coincidenceOnce')

        plt.xlabel('Time [s]')
        plt.ylabel('Counts[Cts/s]')

        # Display average coincidence counts on the plot
        plt.text(0.1, 0.9, f'Avg Coincidence (All): {avg_coincidence_all:.2f} Cts/s', transform=plt.gca().transAxes)
        plt.text(0.1, 0.8, f'Avg Coincidence (Once): {avg_coincidence_once:.2f} Cts/s', transform=plt.gca().transAxes)

        plt.legend()
        plt.title("TimeTrace")
        plt.pause(0.1)

        if finished:
            break

    plt.show(block=True)
