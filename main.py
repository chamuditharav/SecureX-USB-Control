import time
from tkinter import * 
from tkinter import messagebox

import win32com.client
import subprocess
from threading import Thread


usb_device_status = {}
usb_devices = {}

whitelisted_usb = ["USB Composite Device", "USB Root Hub (USB 3.0)","Intel(R)"]

def disable_usb(device):
    print(f"Disabling {device} ......")
    #print(usb_devices)
    while True:
        #subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)
        try:
            if(usb_device_status[device] == "OK"):
                    print({usb_device_status[device]})
                    messagebox.showerror('ALERT',f'You are not allowed to use the plugged USB device')
                    subprocess.run(['devcon', 'disable', device])
                    time.sleep(1)
        except:
            pass


def enable_usb(hid):
    subprocess.run(['devcon', 'enable', hid])
 

def get_usb_device():
    usb_devices.clear()
    usb_device_status.clear()
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOf("Win32_USBHub"):
            if (usb.description not in whitelisted_usb):
                hid = str(usb.DeviceID)
                hid = hid.split("\\")
                fhid = hid[0] + "\\" + hid[1]
                usb_devices[usb.description] = fhid
                usb_device_status[fhid] = usb.Status
            else:
                pass

    except Exception as error:
        print('error', error)


def main():
    usb_ = []
    new_devices = []
    while True:
        
        subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)
        get_usb_device()
        if(len(usb_)==0):
            usb_ = usb_devices.copy()
        elif(not(usb_ == usb_devices)):
            new_devices = (list(set(usb_devices).difference(set(usb_))))
            if(len(new_devices)>0):
                print(new_devices)
                for new_device in new_devices:
                    print(f"{new_device} -> {usb_devices[new_device]}")
                    #print(usb_device_status)
                    #print(usb_devices)
                    #disable_usb(usb_devices[new_device])
                    #print(usb_device_status)

                    dis_usb_Thread = Thread(target=disable_usb, args=(usb_devices[new_device],))
                    dis_usb_Thread.start()
                    #messagebox.showerror('ALERT',f'You are not allowed to use the plugged USB device')

            usb_ = usb_devices.copy()
            #print(new_device)
        else:
            usb_ = usb_devices.copy()


if __name__ == "__main__":
    main()
    #get_usb_device()
    #print(usb_devices)

   