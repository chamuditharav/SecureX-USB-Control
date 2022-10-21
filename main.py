import os
from lib import agent


if __name__ == "__main__":
    devcon = f"{os.getcwd()}\lib\devcon"
    agent.usbWatchdog_service(devcon)