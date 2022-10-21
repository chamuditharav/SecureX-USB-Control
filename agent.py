import time
from tkinter import * 
from tkinter import messagebox

import win32com.client
import subprocess
from threading import Thread


whitelisted_usb = ["USB Root Hub (USB 3.0)", "USB Composite Device", "USB xHCI Compliant Host Controller","Generic USB Hub"]

#whitelisted_usb = "USB Root Hub (USB 3.0) USB Composite Device Generic USB Hub"

usb_devices = {}
usb_device_status = {}
usb_device_list = []



def disableUSB(device):
    print(f"Disabling {device} ......")
    print(usb_devices)
    return 0


def disableUSB_daemon():
    for device in usb_device_list:
        pass
        #print(usb_devices[device])
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
        print('error', error)
    
    return 0
    


def remove_whitelist(whitelist,array):
    for el in array:
        el = el.strip()
        if(el in whitelist):
            array.remove(el)
        else:
            pass
    return array

       


def usbWatchdog_service():
    usb_device_list_old = []
    new_devices = []

    disableUSB_Thread = Thread(target=disableUSB_daemon, args=())
    disableUSB_Thread.start()

    while True:

        subprocess.run(['lib/devcon', 'hwids', '=usb'], capture_output=True, text=True)
        get_usb_device()

        # if(len(usb_device_list_old)==0):
        #     usb_device_list_old = usb_device_list.copy()

        if(set(usb_device_list) != set(usb_device_list_old)):
            new_devices = (list(set(usb_device_list).difference(set(usb_device_list_old))))


            if(len(new_devices) > 0):
                for dev in new_devices:
                    print(f"{dev} -> {usb_device_status[dev]}")

                    disableUSB(dev)

            usb_device_list_old = usb_device_list.copy()
        else:
            usb_device_list_old = usb_device_list.copy()

        #print(usb_device_list)
        #print(usb_devices)
        #time.sleep(1)

        try:
            if( not (disableUSB_Thread.is_alive())):
                disableUSB_Thread = Thread(target=disableUSB_daemon, args=())
                disableUSB_Thread.start()
                disableUSB_Thread.join()         
        except:
            break
        
        time.sleep(2)


if __name__ == "__main__":
    usbWatchdog_service()