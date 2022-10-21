import time
import ctypes
import os
from datetime import datetime


import win32com.client
import subprocess
from threading import Thread

developer_mode = False;

whitelisted_usb = ["USB Root Hub (USB 3.0)", "USB Composite Device", "USB xHCI Compliant Host Controller","Generic USB Hub"]

#whitelisted_usb = "USB Root Hub (USB 3.0) USB Composite Device Generic USB Hub"

usb_devices = {}
usb_device_status = {}
usb_device_list = []


def showAlert(title,text):
    #alert(text=text, title=title, button='OK')
    pushLog(f"Alert : {title}")
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, text, title, 0)

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



def disableUSB(devcon,device):
    pprint(f"Disabling {device} ......")
    try:
        if(usb_device_status[device] == "OK"):

            pprint(usb_devices[device])
            pushLog(f"Inside device remove thread : {device}")
            proc = subprocess.run([devcon, 'remove', usb_devices[device]],capture_output=True)
            out = proc.stdout.decode().strip()
            pushLog(f"devcon output : {device} : {out}")
            if(out):
                msgBox_Thread = Thread(target=showAlert, args=('Alert', 'You are not allowed to use the plugged USB device'), daemon=True)
                msgBox_Thread.start()
            

        else:
            pprint("Already disabled or Device error!")
            pushLog(f"Already disabled or Device error : {device}")
    except:
        pass
    return 0


def disableUSB_daemon():
    for device in usb_device_list:
        pass
        #pprint(usb_devices[device])
    return 0


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
          
    except Exception as error:
        pprint('error', error)
    
    return 0
    


def remove_whitelist(whitelist,array):
    for el in array:
        el = el.strip()
        if(el in whitelist):
            array.remove(el)
        else:
            pass
    return array

       


def usbWatchdog_service(devcon):
    usb_device_list_old = []
    new_devices = []

    pushLog(f"Starting the device remove daemon.......")
    disableUSB_Thread = Thread(target=disableUSB_daemon, args=(), daemon=True)
    disableUSB_Thread.start()

    pushLog("Agent start")

    while True:

        #subprocess.run([devcon, 'hwids', '=usb'], capture_output=True, text=True)
        get_usb_device()

        # if(len(usb_device_list_old)==0):
        #     usb_device_list_old = usb_device_list.copy()

        if(set(usb_device_list) != set(usb_device_list_old)):
            new_devices = (list(set(usb_device_list).difference(set(usb_device_list_old))))


            if(len(new_devices) > 0):
                for dev in new_devices:
                    pprint(f"{dev} -> {usb_device_status[dev]}")

                    pushLog(f"New device connected : {dev}:{usb_devices[dev]}")

                    pushLog(f"Device remove thread start for {dev}")
                    disable_USB_Device_Thread = Thread(target=disableUSB, args=(devcon,dev))
                    disable_USB_Device_Thread.start()
                    disable_USB_Device_Thread.join()
                    pushLog(f"Device remove thread ended for {dev}")
                    
                    #disableUSB(dev)

            usb_device_list_old = usb_device_list.copy()
        else:
            usb_device_list_old = usb_device_list.copy()

        #pprint(usb_device_list)
        #pprint(usb_devices)
        #time.sleep(1)

        try:
            if( not (disableUSB_Thread.is_alive())):
                #pushLog(f"Starting the device remove daemon.......")
                disableUSB_Thread = Thread(target=disableUSB_daemon, args=(), daemon=True)
                disableUSB_Thread.start()
                disableUSB_Thread.join()      
                #pushLog(f"Daemon crashed or stopped")   
        except:
            break
        
        #time.sleep(0.2)


if __name__ == "__main__":
    pass
    #pprint(os.getcwd())
    #usbWatchdog_service(f"{os.getcwd()}\devcon")