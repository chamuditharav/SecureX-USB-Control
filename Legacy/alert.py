
from ctypes import windll

def showAlertNative(title,text):
    #pushLog(f"Alert : {title}")
    MessageBox = windll.user32.MessageBoxW
    #MessageBox(None, text, title, 16)
    MessageBox(None, text, title, 0x40010)



showAlertNative("TEST","Test")