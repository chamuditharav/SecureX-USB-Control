
from ctypes import windll

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10


def showAlertNative(title,text):
    #pushLog(f"Alert : {title}")
    MessageBox = windll.user32.MessageBoxW
    #MessageBox(None, text, title, 16)
    MessageBox(None, text, title, 0x1000|16) #1010



showAlertNative("TEST","Test")