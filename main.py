import os

from lib import agent, genDevcon
from hashlib import sha256


def devconIntegrity():
    if(not (os.path.exists("lib/devcon.exe"))):
        devconMake = open("lib/devcon.exe",'wb')
        devconMake.write(bytes.fromhex(genDevcon.devcon_bkp))
        devconMake.close()
    
    else:
        devconFile = open("lib/devcon.exe",'rb')
        content = devconFile.read()
        devconFile.close()

        if(not(sha256(content).hexdigest()) == genDevcon.devconHash):
            os.remove("lib/devcon.exe")
            devconMake = open("lib/devcon.exe",'wb')
            devconMake.write(bytes.fromhex(genDevcon.devcon_bkp))
            devconMake.close()
        # else:
        #     devcon = f"{os.getcwd()}\lib\devcon"
        #     agent.usbWatchdog_service(devcon)

if __name__ == "__main__":

    try:

        devconIntegrity()
        devcon = f"{os.getcwd()}\lib\devcon"
        agent.usbWatchdog_service(devcon,0.1)
    
    except:
        agent.pushLog("Program exec error")


    #file = open("lib/devcon.exe",'rb')
    #content = file.read()

    #print(sha256(content).hexdigest())
