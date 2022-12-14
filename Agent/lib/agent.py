import time
#import ctypes

from ctypes import windll
import os
from datetime import datetime

from lib import genDevcon
from hashlib import sha256


import win32com.client
import subprocess
import signal
from threading import Thread


from tkinter import *
from tkinter import messagebox


import psutil


developer_mode = False;

#whitelisted_usb = ["USB Root Hub (USB 3.0)", "USB Composite Device", "USB xHCI Compliant Host Controller","Generic USB Hub", "07A10603AD5E64C2"]



usb_devices = {}
usb_device_status = {}
usb_device_list = []


thread_status = {}



def pushLog(logInfo):
    if(not os.path.isdir(f'{os.getcwd()}/logs')):
        os.mkdir(f'{os.getcwd()}/logs')
        logfile = open(f'{os.getcwd()}/logs/logs.log','w+')
        logfile.close()
        pushLog(logInfo)
    else:
        logfile = open(f'{os.getcwd()}/logs/logs.log','a')
        timeNow = datetime.now()
        timeFrame = timeNow.strftime("%d/%m/%Y %H:%M:%S")
        logLine = f"{timeFrame}\t {logInfo}\n"
        logfile.write(logLine)
        logfile.close()



def alertCom():
    try:
        with open(f'{os.getcwd()}/intercept.sx','w+') as alertCom:
            alertCom.write(f"{bytes('SH_MSGBX', 'ascii').hex()}")
            alertCom.close()
    except:
        pass


def showAlertTk(title,text):
        top = Tk()
        top.withdraw()
        top.wm_attributes("-topmost", 1)
        messagebox.showerror(title=title, message=text, parent=top)
        top.mainloop()
        top.destroy()


def showAlertNative(title,text):
    alertCom()
    #MessageBox = windll.user32.MessageBoxW
    #MessageBox(None, text, title, 16)
    #MessageBox(None, text, title, 0x1000|16) #0x1010


def pprint(context):
    if (developer_mode):
        print(context)



def devconIntegrity(path):
    if(not (os.path.exists("lib/"))):
        pushLog("No lib file detected!!!!!!")
        pushLog("Generating a new lib folder ........")
        os.mkdir("lib")
        pushLog("lib folder generated ........")

    elif(not (os.path.exists(f"{path}.exe"))):
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
            pass
            #pushLog("Devcon is valid")



def getRemovableDeviceLetters():
    disks = psutil.disk_partitions()
    tempArray = []
    for disk in disks:
        if(("fixed" not in disk.opts) and (os.path.exists(f"{disk.mountpoint[0]}:/"))):
            tempArray.append(disk.mountpoint[0])

    return tempArray


def seriousFailSafe():
    pass
    #pushLog(f"SERIOUS FAILSAFE INITIATED ..............................")
    while(len(getRemovableDeviceLetters())>0):
        drives = getRemovableDeviceLetters()
        # print(drives)
        pushLog(f"Detected removable disks : {drives}")
        for drive in drives:
            cmd = '$driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).ParseName("'+drive+':").InvokeVerb("Eject")'
            try:
                pushLog(f"Ejecting : {drive}")
                process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy','Unrestricted',"-windowstyle","hidden", cmd],shell=False)
                process.communicate()
            except:
                pass
        time.sleep(2)
    #pushLog(f"SERIOUS FAILSAFE ENDED ..............................")



def failSafeRemove(devcon,device):
    pushLog(f"Fail safe device remove triggered for {device}")
    try:
        pushLog("Checking devcon integrity")
        devconIntegrity(devcon)

        failSafeProc = subprocess.Popen([devcon, 'remove', usb_devices[device]],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = failSafeProc.communicate()
        out = stdout.decode().strip()
        pushLog(f"devcon output [FAILSAFE] : {device} : {out}")

        if(("1 device(s) were removed" in out) or ("1 device(s) disabled" in out)):
                msgBox_Thread = Thread(target=showAlertNative, args=('SecureX USB Agent Alert', 'You are not allowed to use the plugged USB device'), daemon=False)
                msgBox_Thread.start()
        else:
            pushLog(f"SERIOUS FAILSAFE INITIATED ..............................")
            seriousFailSafeEject_Thread = Thread(target=seriousFailSafe, args=())
            seriousFailSafeEject_Thread.start()
            seriousFailSafeEject_Thread.join()
            pushLog(f"SERIOUS FAILSAFE ENDED ..............................")
                
    except Exception as e:
        pushLog(f"Fail safe remove -> {e}")

"""
def preCheckEject(devcon):
    pushLog(f"Pre chech eject initiated")
    while(len(usb_devices)>0):
        for device in usb_devices:
            #print(device)
            if(usb_device_status[device]=="OK"):
                try:
                    pushLog("Checking devcon integrity")
                    devconIntegrity(devcon)

                    ejectDisableProc = subprocess.Popen([devcon, 'remove', usb_devices[device]],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = ejectDisableProc.communicate()
                    out = stdout.decode().strip()
                    pushLog(f"devcon output [PRE CHECK EJECT] : {device} : {out}")

                    if(("1 device(s) were removed" in out) or ("1 device(s) disabled" in out)):
                        pushLog(f"{device} Ejected !")
                            
                except Exception as e:
                    pushLog(f"Eject disable faild -> {e}")
    pushLog(f"Pre chech eject ended")
"""


def disableUSB(devcon,device):
    pprint(f"Disabling {device} ......")
    try:
        if(usb_device_status[device] == "OK"):

            pprint(usb_devices[device])
            pushLog(f"Inside device remove thread : {device}")

            pushLog("Checking devcon integrity")
            devconIntegrity(devcon)


            proc = subprocess.Popen([devcon, 'disable', usb_devices[device]],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = proc.communicate()
            out = stdout.decode().strip()

            pushLog(f"devcon output : {device} : {out}")
            if(("1 device(s) were removed" in out) or ("1 device(s) disabled" in out)):
                msgBox_Thread = Thread(target=showAlertNative, args=('SecureX USB Agent Alert', 'You are not allowed to use the plugged USB device'), daemon=False)
                msgBox_Thread.start()
                #msgBox_Thread.join()
            elif("The 1 device(s) are ready to be disabled" in out):
                pushLog(f"Fail Safe Remove triggering ...........")
                time.sleep(2)
                failSafeRemove(devcon,device)


        elif(usb_device_status[device]=="Error"):
            pass

        else:
            pprint("Already disabled or Device error!")
            pushLog(f"Already disabled or Device error : {device}")
    except Exception as e:
        pushLog(f"Disable USB crashed -> {e}")


def removeUSBNoAlert(devcon,device):
    try:
        if(usb_device_status[device] == "OK"):
            pprint(usb_devices[device])
            pushLog(f"Inside device remove thread : {device}")
            pushLog("Checking devcon integrity")
            devconIntegrity(devcon)
            proc = subprocess.Popen([devcon, 'remove', usb_devices[device]],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            stdout, stderr = proc.communicate()
            out = stdout.decode().strip()

            pushLog(f"devcon output : {device} : {out}")

        elif(usb_device_status[device]=="Error"):
            pass

        else:
            pprint("Already disabled or Device error!")
            pushLog(f"Already disabled or Device error : {device}")
    except Exception as e:
        pushLog(f"Disable USB crashed -> {e}")





def disableUSB_daemon(devcon):
    pprint(len(usb_devices))
    if(len(usb_devices)>0):
        #pushLog(f"Enabled device(s) detected .......")
        for device in usb_devices:
            if(usb_device_status[device]=="OK"):
                try:
                    pushLog(f"Forced disable check [DAEMON] : {device}")

                    disableUSB(devcon,device)
                    
                    # disable_USB_Device_Daemon_Thread = Thread(target=disableUSB, args=(devcon,device))
                    # disable_USB_Device_Daemon_Thread.start()
                    # disable_USB_Device_Daemon_Thread.join()
                except Exception as e:
                    pushLog(f"USB disable daemon crashed [DAEMON] -> {e}")
            elif(usb_device_status[device]=="Error"):
                #print("THIS")
                pass

        #pushLog(f"Device(s) disabled .......")
 


def get_usb_device(whitelisted_usb):
    usb_devices.clear()
    usb_device_status.clear()
    usb_device_list.clear()
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            if((usb.description.strip() not in whitelisted_usb) and (usb.DeviceID.strip().split("\\")[-1] not in whitelisted_usb)):
                #pushLog(f"HWID -> {usb.DeviceID.strip()}")
                hid = str(usb.DeviceID)
                hid = hid.split("\\")
                dev_description = f"{usb.description}:{len(usb_devices)+1}"
                usb_devices[dev_description] = hid[0] + "\\" + hid[1]
                usb_device_status[dev_description] = usb.Status
                usb_device_list.append(dev_description)
                

            elif((usb.DeviceID.strip().split("\\")[-1] in whitelisted_usb) and (usb.Status == "Error")):
                #Enable whitelisted usb if disabled accidentally
                pushLog(f"Enabling whitelisted USB -> {usb.DeviceID}")
          
    except Exception as e:
        pushLog(f"UpdateUSB crashed -> {e}")
        pprint('error', e)
    
    return 0
    

def precheck(devcon):
    pprint(len(usb_devices))
    if(len(usb_devices)>0):
        #pushLog(f"Enabled device(s) detected .......")
        for device in usb_devices:
            if(usb_device_status[device]=="OK"):
                try:
                    pushLog(f"Precheck disable : {device}")

                    removeUSBNoAlert(devcon,device)

                except Exception as e:
                    pushLog(f"Precheck disable error -> {e}")
            elif(usb_device_status[device]=="Error"):
                pass
       

def usbWatchdog_service(devcon,limit,whitelisted_usb,whitelisted_users,loggedUser):
    usb_device_list_old = []
    new_devices = []


    pushLog("-"*100)
    pushLog("Agent start")
    #pushLog(f"User : {os.getlogin()}")


    # get_usb_device(whitelisted_usb)
    # #preCheckEject(devcon)

    # disable_Daemon = Thread(target=disableUSB_daemon, args=(devcon,))
    # disable_Daemon.start()
    # disable_Daemon.join()

    get_usb_device(whitelisted_usb)
    precheck(devcon)

    pushLog(f"Removing all ejectable devices")
    startupEject_Thread = Thread(target=seriousFailSafe, args=())
    startupEject_Thread.start()
    startupEject_Thread.join()
    pushLog(f"All ejectable devices are removed")




    while True:
        # get_usb_device(whitelisted_usb)
        # disableUSB_daemon(devcon)

        get_usb_device(whitelisted_usb)

        #devconIntegrity(devcon)

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

                        #disableUSB(devcon,dev)

                        pushLog(f"Device disable thread ended for {dev}")
                    
                    elif(usb_device_status[dev] == "Error"):
                        pushLog(f"Connected a device that already disabled {dev}")

                        msgBox_Thread = Thread(target=showAlertNative, args=('SecureX USB Agent Alert', 'You are not allowed to use the plugged USB device'), daemon=False)
                        msgBox_Thread.start()


            get_usb_device(whitelisted_usb)                    
            usb_device_list_old = usb_device_list.copy()
        else:
            usb_device_list_old = usb_device_list.copy()


        #pprint(usb_device_list)
        #pprint(usb_devices)
        #time.sleep(1)

        # disable_Daemon = Thread(target=disableUSB_daemon, args=(devcon,))
        # disable_Daemon.start()
        # disable_Daemon.join()

        disableUSB_daemon(devcon)
        
        time.sleep(limit)
    
 


if __name__ == "__main__":
    pass
