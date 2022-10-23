import time
#import ctypes

from ctypes import windll
import os
from datetime import datetime

from lib import genDevcon
from hashlib import sha256


import win32com.client
import subprocess
from threading import Thread


from tkinter import *
from tkinter import messagebox

import win32api
import win32con
import win32file


developer_mode = False;

whitelisted_usb = ["USB Root Hub (USB 3.0)", "USB Composite Device", "USB xHCI Compliant Host Controller","Generic USB Hub"]

#whitelisted_usb = "USB Root Hub (USB 3.0) USB Composite Device Generic USB Hub"

usb_devices = {}
usb_device_status = {}
usb_device_list = []


thread_status = {}




def showAlertTk(title,text):
        top = Tk()
        top.withdraw()
        top.wm_attributes("-topmost", 1)
        messagebox.showerror(title=title, message=text, parent=top)
        #top.mainloop()
        top.destroy()


def showAlertNative(title,text):
    pushLog(f"Alert : {title}")
    MessageBox = windll.user32.MessageBoxW
    MessageBox(None, text, title, 16)

def pprint(context):
    if (developer_mode):
        print(context)

def pushLog(logInfo):
    if(not os.path.isdir('logs')):
        os.mkdir('logs')
        logfile = open('logs/logs.log','w+')
        logfile.close()
        pushLog(logInfo)
    else:
        logfile = open('logs/logs.log','a')
        timeNow = datetime.now()
        timeFrame = timeNow.strftime("%d/%m/%Y %H:%M:%S")
        logLine = f"{timeFrame}\t {logInfo}\n"
        logfile.write(logLine)
        logfile.close()



def devconIntegrity(path):
    pushLog("Checking devcon integrity")
    if(not (os.path.exists(f"{path}.exe"))):
        pushLog("No devcon detected!!!!!!")
        devconMake = open(f"{path}.exe",'wb')
        pushLog("Generating a new devcon ........")
        devconMake.write(bytes.fromhex(genDevcon.devcon_bkp))
        devconMake.close()
        pushLog("Devcon generated .........")
    
    else:
        devconFile = open(f"{path}.exe",'rb')
        content = devconFile.read()
        devconFile.close()

        if(not(sha256(content).hexdigest()) == genDevcon.devconHash):
            pushLog("Devcon hash mis-match")
            pushLog("Removing altered devcon")

            os.remove(f"{path}.exe")
            pushLog("Altered devcon removed")
            devconMake = open(f"lib/devcon.exe",'wb')
            pushLog("Generating a new devcon ........")

            devconMake.write(bytes.fromhex(genDevcon.devcon_bkp))
            devconMake.close()
            pushLog("Devcon generated .........")
        
        else:
            pushLog("Devcon is valid")



def detectRemovableDrives():
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
    rdrives = [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]
    return rdrives


def failSafe():
    drives = detectRemovableDrives()
    for drive in drives:
        os.system(f'powershell.exe -WindowStyle hidden $driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).ParseName("""{drive}""").InvokeVerb("""Eject"""); start-sleep -s 3')

    showAlertTk("SecureX USB agent","PLEASE REMOVE THE PLUGGED USB DEVICE!")


def disableUSB(devcon,device):
    pprint(f"Disabling {device} ......")
    try:
        if(usb_device_status[device] == "OK"):

            pprint(usb_devices[device])
            pushLog(f"Inside device remove thread : {device}")
            devconIntegrity(devcon)
            proc = subprocess.Popen([devcon, 'disable', usb_devices[device]],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = proc.communicate()
            out = stdout.decode().strip()

            pushLog(f"devcon output : {device} : {out}")
            if(("1 device(s) were removed" in out) or ("1 device(s) disabled" in out)):
                msgBox_Thread = Thread(target=showAlertTk, args=('SecureX USB agent', 'You are not allowed to use the plugged USB device'), daemon=False)
                msgBox_Thread.start()
                #msgBox_Thread.join()


        elif(usb_device_status[device]=="Error"):
            pass
        else:
            pprint("Already disabled or Device error!")
            pushLog(f"Already disabled or Device error : {device}")
    except Exception as e:
        pushLog(f"Disable USB crashed -> {e}")

  
    return 0





def disableUSB_daemon(devcon):
    pprint(len(usb_devices))
    if(len(usb_devices)>0):
        #pushLog(f"Starting the device disable check .......")
        for device in usb_devices:
            if(usb_device_status[device]=="OK"):
                try:
                    pushLog(f"Forced disable check : {device}")
                    disableUSB(devcon,device)
                except Exception as e:
                    pushLog(f"USB disable daemon crashed -> {e}")
            #pushLog(f"Device disable check ended .......")
 


def get_usb_device():
    usb_devices.clear()
    usb_device_status.clear()
    usb_device_list.clear()
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            if(usb.description.strip() not in whitelisted_usb):
                hid = str(usb.DeviceID)
                hid = hid.split("\\")
                dev_description = f"{usb.description}:{len(usb_devices)+1}"
                usb_devices[dev_description] = hid[0] + "\\" + hid[1]
                usb_device_status[dev_description] = usb.Status
                usb_device_list.append(dev_description)
          
    except Exception as e:
        pushLog(f"UpdateUSB crashed -> {e}")
        pprint('error', e)
    
    return 0
    

       

def usbWatchdog_service(devcon,limit):
    usb_device_list_old = []
    new_devices = []


    pushLog("-"*100)
    pushLog("Agent start")

    while True:
        get_usb_device()


        if(set(usb_device_list) != set(usb_device_list_old)):
            new_devices = (list(set(usb_device_list).difference(set(usb_device_list_old))))


            if(len(new_devices) > 0):
                for dev in new_devices:
                    pprint(f"{dev} -> {usb_device_status[dev]}")

                    pushLog(f"New device connected : {dev}:{usb_devices[dev]}")

                    if(usb_device_status[dev] == "OK"):

                        pushLog(f"Device disable thread start for {dev}")

                        disable_USB_Device_Thread = Thread(target=disableUSB, args=(devcon,dev))
                        disable_USB_Device_Thread.start()
                        disable_USB_Device_Thread.join()

                        pushLog(f"Device disable thread ended for {dev}")
                    
                    elif(usb_device_status[dev] == "Error"):
                        pushLog(f"Connected a device that already disabled {dev}")
                        msgBox_Thread = Thread(target=showAlertTk, args=('SecureX USB agent', 'You are not allowed to use the plugged USB device'), daemon=False)
                        msgBox_Thread.start()


            get_usb_device()                    
            usb_device_list_old = usb_device_list.copy()
        else:
            usb_device_list_old = usb_device_list.copy()


        #pprint(usb_device_list)
        #pprint(usb_devices)
        #time.sleep(1)

        disable_Daemon = Thread(target=disableUSB_daemon, args=(devcon,))
        disable_Daemon.start()
        disable_Daemon.join()

        #disableUSB_daemon(devcon)
        
        time.sleep(limit)


if __name__ == "__main__":
    pass
    #pprint(os.getcwd())
    #usbWatchdog_service(f"{os.getcwd()}\devcon")