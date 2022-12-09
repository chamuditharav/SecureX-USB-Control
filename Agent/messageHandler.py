import os
import time
from tkinter import *
from tkinter import messagebox

from ctypes import windll


def showAlertTk(title,text):
        top = Tk()
        top.withdraw()
        top.wm_attributes("-topmost", 1)
        messagebox.showerror(title=title, message=text, parent=top)
        top.mainloop()
        top.destroy()


def showAlertNative(title,text):
    #pushLog(f"Alert : {title}")
    MessageBox = windll.user32.MessageBoxW
    #MessageBox(None, text, title, 16)
    MessageBox(None, text, title, 0x1000|16) #0x1010


while True:
    if(os.path.exists(f"{os.getcwd()}/intercept.sx")):
        try:
            with open(f'{os.getcwd()}/intercept.sx','r') as alertCom:
                msg = alertCom.read()
                if(msg == "53485f4d53474258"):
                    showAlertNative('SecureX USB Agent Alert', 'You are not allowed to use the plugged USB device')
                alertCom.close()
            os.remove(f'{os.getcwd()}/intercept.sx')
        except:
            pass
    else:
        pass

    time.sleep(1)
    