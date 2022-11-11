import wmi

import win32com.client

DRIVE_TYPES = {
  0 : "Unknown",
  1 : "No Root Directory",
  2 : "Removable Disk",
  3 : "Local Disk",
  4 : "Network Drive",
  5 : "Compact Disc",
  6 : "RAM Disk"
}

def USB():
    #wmi = win32com.client.GetObject ("winmgmts:")
    for usb in win32com.client.GetObject ("winmgmts:").InstancesOf ("Win32_USBHub"):

        print(dir(usb))


        print(usb.AddRef)
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
  
#
#USB()


c = wmi.WMI ()
for drive in c.Win32_LogicalDisk ():
    # prints all the drives details including name, type and size
    
    if(drive.DriveType == 2):
      print(drive)
      print (drive.Caption, drive.VolumeName, DRIVE_TYPES[drive.DriveType])

    
  
