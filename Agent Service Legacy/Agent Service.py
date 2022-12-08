#SecureX USB agent service handler

#THIS IS THE LEGACY AGENT SERVICE

import psutil
import time
import os
from datetime import datetime

import subprocess

# print("SecureX-USB-Agent.exe" in (p.name() for p in psutil.process_iter()))

# for p in psutil.process_iter():
#     print(p.name())


def pushLog(logInfo):
    if(not os.path.isdir('logs')):
        os.mkdir('logs')
        logfile = open('logs/ServiceLog.log','w+')
        logfile.close()
        pushLog(logInfo)
    else:
        logfile = open('logs/ServiceLog.log','a')
        timeNow = datetime.now()
        timeFrame = timeNow.strftime("%d/%m/%Y %H:%M:%S")
        logLine = f"{timeFrame}\t {logInfo}\n"
        logfile.write(logLine)
        logfile.close()


if __name__ == "__main__":
    pushLog("Starting Agent Service......")
    while(True):
        time.sleep(5)
        if("SecureX-USB-Agent.exe" not in (p.name() for p in psutil.process_iter())):
            pushLog("Agent could not found......")
            pushLog("Agent starting.........")
            #print("Starting")
            #os.startfile(r"SecureX-USB-Agent.exe")
            subprocess.Popen('SecureX-USB-Agent.exe')