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


if __name__ == "__main__":


#put while here
    try:
        devconIntegrity()
        devcon = f"{os.getcwd()}\lib\devcon"
        agent.usbWatchdog_service(devcon,0.01)
    except:
        agent.pushLog("Program exec error")

