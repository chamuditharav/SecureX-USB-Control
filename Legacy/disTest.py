import subprocess
import signal
import os
import time

import win32ui

import win32com.client



import wmi

def getLetter(deviceID):
    #logical_disk = wmi.WMI().query("SELECT * FROM Win32_LogicalDisk WHERE DeviceID=USB\\VID_0718&PID_0638\\07A10603AD5E64C2")
    logical_disk = wmi.WMI().query("SELECT * FROM Win32_LogicalDisk WHERE DriveType=2")
    print('Drive letter: {}'.format(logical_disk.DeviceID))







def USB():
    #wmi = win32com.client.GetObject ("winmgmts:")
    for usb in win32com.client.GetObject ("winmgmts:").InstancesOf ("Win32_USBHub"):
        # print usb.DeviceID
        # pprint.pprint (dir(usb))
        # pprint.pprint (vars(usb))
        # print usb.__dict__


        print ('Device ID:', usb.DeviceID)
        print ('Name:', usb.name)
        print ('System Name:', usb.SystemName)
        print ('Caption:', usb.Caption)
        print ('ClassCode:', usb.ClassCode)
        print ('CreationClassName:', usb.CreationClassName)
        print ('CurrentConfigValue:', usb.CurrentConfigValue)
        print ('Description:', usb.Description)
        print ('PNPDeviceID:', usb.PNPDeviceID)
        print ('Status:', usb.Status)
        print(usb.CurrentConfigValue)
        
        print ('\n')
        pass
    # Fetches the list of all usb devices:


#res = subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True)

#print(res)

#rr = res.split(",")

#print("\n")
#print(rr)

#USB\VID_0718&PID_0638

# proc = subprocess.run(["devcon", 'remove', "USB\\VID_0718&PID_0638"]) #USB\VID_0EA0&PID_2168
#proc = subprocess.run(["devcon", 'remove', "USB\\VID_0718&PID_0638"], stderr=subprocess.PIPE, stdout=subprocess.PIPE) #USB\VID_0EA0&PID_2168



"""
time.sleep(2)
proc = proc = subprocess.run(["devcon", 'remove', "USB\\VID_0718&PID_0638"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

time.sleep(2)

out = proc.stdout.decode().strip()

print(proc)
print("1 device(s) were removed" in out)

#os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

time.sleep(2)

#./devcon.exe remove "USB\VID_0718&PID_0638"


"""


#subprocess.run(['devcon', 'enable', "USB\\VID_0EA0&PID_2168"])




'''

def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        return True
    else:
        return False

if process_exists('CalculatorApp.exe'):
    print("dsadsad")
else:
    print("84855151")
    '''


def Logical():
    #wmi = win32com.client.GetObject ("winmgmts:")
    for drive in win32com.client.GetObject ("winmgmts:").InstancesOf ("Win32_logicalDisk"):
        # print usb.DeviceID
        # pprint.pprint (dir(usb))
        # pprint.pprint (vars(usb))
        # print usb.__dict__

        print(drive.Caption, drive.VolumeName, drive.PNPDeviceID)

        # print ('Device ID:', usb.DeviceID)
        # print ('Name:', usb.name)
        # print ('System Name:', usb.SystemName)
        # print ('Caption:', usb.Caption)
        # print ('ClassCode:', usb.ClassCode)
        # print ('CreationClassName:', usb.CreationClassName)
        # print ('CurrentConfigValue:', usb.CurrentConfigValue)
        # print ('Description:', usb.Description)
        # print ('PNPDeviceID:', usb.PNPDeviceID)
        # print ('Status:', usb.Status)
        # print(usb.CurrentConfigValue)
        
        # print ('\n')
        pass
    # Fetches the list of all usb devices:


#Logical()



subprocess.run(["devcon", 'remove', "USB\VID_0718&PID_062*"]) #USB\VID_0EA0&PID_2168