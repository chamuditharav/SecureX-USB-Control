
import subprocess
import signal
import os
import time

import win32ui

import win32com.client

from threading import Thread


import win32api
import win32con
import win32file


import wmi








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
    tempArray = {}
    for drive in win32com.client.GetObject ("winmgmts:").InstancesOf ("Win32_logicalDisk"):
        if(drive.DriveType == 2):
            #print(drive.Caption, drive.VolumeName, drive.DriveType)
            tempArray[drive.Caption] = [drive.VolumeName,drive.DriveType]
    
    print(tempArray)



#Logical()



#subprocess.run(["devcon", 'remove', "USB\VID_0718&PID_062*"]) #USB\VID_0EA0&PID_2168


#USB()


import psutil

global drives

drives = []



def devHandle():
    while True:
        print(len(drives))
        if(len(drives)>0):
            for drive in drives:
                print(drive)
                # T2 = Thread(target=enc,args=(drive,))
                # T2.start()
                # T2.join()


def updateDrive():
    while True:
        drives.clear()
        disks = psutil.disk_partitions()
        tempArray = []
        for disc in disks:
            if("fixed" not in disc.opts):
                tempArray.append(disc.mountpoint[0])

        return tempArray




def main():
    while True:    
        deviceArray = updateDrive()
        drives = deviceArray.copy()
        #(drives)
        time.sleep(1)




file_whitelist = ["System Volume Information"]
def enc(driveLetter):
    dirs = []
    try:
        rootdir = f'{driveLetter}:/'
        for file in os.listdir(rootdir):
            if(file not in file_whitelist):
                dir = os.path.join(rootdir, file)
                if os.path.isdir(dir):
                    dirs.append
    except:
        pass




def getLetter():
    #logical_disk = wmi.WMI().query("SELECT * FROM Win32_LogicalDisk WHERE DeviceID=USB\\VID_0718&PID_0638\\07A10603AD5E64C2")
    logical_disk = wmi.WMI().query("SELECT * FROM Win32_LogicalDisk WHERE DriveType=2")
    #print('Drive letter: {}'.format(logical_disk.DeviceID))
    print(logical_disk)



if __name__ == "__main__":
    #Logical()
    USB()

    
    # T1 = Thread(target=devHandle, args=())
    # T1.start()

    # main()

    #enc("H")

    """  drives = updateDrive()
    print(drives)

    for drive in drives:

        tmpFile = open(f'{os.getcwd()}/tmp.ps1','w')
        tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
        tmpFile.write('$driveEject.Namespace(17).ParseName("'+drive+':").InvokeVerb("Eject")')
        tmpFile.close()
        
        try:
            process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy','Unrestricted','./tmp.ps1'])
            process.communicate()
        except:
            print("Couldn't disable")
        time.sleep(2)
    """
    
    """
    while(len(updateDrive())>0):
        drives = updateDrive()
        print(drives)

        #disk = "I"
        for disk in drives:
            #tmpFile = open(f'{os.getcwd()}/tmp.ps1','w')
            #tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
            #tmpFile.write('$driveEject.Namespace(17).ParseName("'+disk+':").InvokeVerb("Eject")')
            #tmpFile.close()
            cmd = '$driveEject = New-Object -comObject Shell.Application; $driveEject.Namespace(17).ParseName("'+disk+':").InvokeVerb("Eject")'
            try:
                print(f"Ejecting : {disk}")
                process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy','Unrestricted', cmd])
                process.communicate()
            except:
                pass
        time.sleep(2)

    """

    """    disk = "H"
    tmpFile = open('tmp.ps1','w')
    tmpFile.write('$driveEject = New-Object -comObject Shell.Application\n')
    tmpFile.write('$driveEject.Namespace(17).ParseName("'+disk+':").InvokeVerb("Eject")')
    tmpFile.close()
    process = subprocess.Popen(['powershell.exe', '-ExecutionPolicy','Unrestricted','./tmp.ps1'])
    process.communicate()
    """

    #subprocess.run(["devcon", 'remove', "USB\VID_0718&PID_062*"])
