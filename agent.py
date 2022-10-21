import time
import win32com.client
import subprocess


whitelisted_usb = ["USB Root Hub (USB 3.0)", "USB Composite Device", "USB xHCI Compliant Host Controller","Generic USB Hub"]

#whitelisted_usb = "USB Root Hub (USB 3.0) USB Composite Device Generic USB Hub"

usb_devices = {}
usb_device_status = {}
usb_device_list = []

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
                usb_devices[usb.description] = hid[0] + "\\" + hid[1]
                usb_device_status[usb.description] = usb.Status
                usb_device_list.append(usb.description)
          
    except Exception as error:
        print('error', error)
    


def remove_whitelist(whitelist,array):
    for el in array:
        el = el.strip()
        if(el in whitelist):
            array.remove(el)
        else:
            pass
    return array

def main():
    usb_device_list_old = []
    new_devices = []

    while True:
        get_usb_device()

        if(len(usb_device_list_old)==0):
            usb_device_list_old = usb_device_list.copy()

        elif(set(usb_device_list_old) != set(usb_device_list)):
            new_devices = (list(set(usb_device_list).difference(set(usb_device_list_old))))
            usb_device_list_old = usb_device_list.copy()

            if(len(new_devices) > 0):
                for dev in new_devices:
                    print(f"{dev} -> {usb_device_status[dev]}")
        else:
            usb_device_list_old = usb_device_list.copy()

        print(usb_device_list)
        print(usb_devices)
        time.sleep(1)

if __name__ == "__main__":
    main()
    
    #get_usb_device()
    #x = remove_whitelist(whitelisted_usb,usb_device_list)
    #print(x)

    # for el in usb_device_list:
    #     print(el in whitelisted_usb)
   
    #print("USB Root Hub (USB 3.0)" in whitelisted_usb)