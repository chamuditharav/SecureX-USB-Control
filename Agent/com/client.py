import socket
import time
import threading

import rsa
from cryptography.fernet import Fernet


clientID = "Client1"
keys = {"priK":"", "pubK":"", "shareKey":""}

# Connecting To Server

def con():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 65432))


def MSGencrypt(data):
    fernet = keys["shareKey"]
    enc = fernet.encrypt(data.encode())
    return(enc)
    


def MSGdecrypt(data):
    fernet = keys["shareKey"]
    dec = fernet.decrypt(bytes.fromhex(data))
    return(dec.decode())


def generateKeys(ksize=1024):
    (publicKey, privateKey) = rsa.newkeys(ksize)
    return publicKey, privateKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        print("Decryption Error!")

def saveKey(key):
    keys["shareKey"] = Fernet(key)
    #print(keys)
    print("Key Shared!")

def keyEx():
    print("Initializing key exchange.....")
    publicKey, privateKey = generateKeys()
    keys["priK"] = privateKey
    keys["pubK"] = publicKey

    send(f"NEW-CON:{keys['pubK']._save_pkcs1_pem().hex()}")

def receive():
    while True:
        try:
            dataFrame = client.recv(1024).decode('ascii')
            if (f"{clientID}:SVR-KEYEX-RPLY" in dataFrame):
                dataFrame = dataFrame.split(":")
                #print(dataFrame)
                
                #saveKey(decrypt(bytes.fromhex(dataFrame[2]),keys["priK"]))
                print("Key recieved!")
                print("Decrypting the key.......")
                encKey = decrypt(bytes.fromhex(dataFrame[2]),keys["priK"])
                print("Key decrypted!")
                print(encKey)
                keySave_thread = threading.Thread(target=saveKey, args=(encKey.encode(),))
                keySave_thread.start()
                
            elif (f"{clientID}:ENC-MSG" in dataFrame):
                dataFrame = dataFrame.split(":")
                print(f"{clientID} <-- SVR : {MSGdecrypt(dataFrame[2])}")
                print("\n")

            else:
                print(dataFrame)
        except:
            print("An Error Occured!")
            client.close()
            #con()
            #init_()
            break

def send(message):
    client.send(bytes(f"{clientID}:{message}", 'ascii'))

def sendEnc(message):
    #print(MSGencrypt(message).hex())
    send(f"ENC-MSG:{MSGencrypt(message).hex()}")
    #client.send(bytes(f"{clientID}:{message}", 'ascii'))


def mainLoop():
    keyEx()
    while True:
        if(not keys["shareKey"] == ""):

            terminal = str(input("> "))
            sendEnc(terminal)
            print(f"{clientID} --> SVR : {terminal}")
            time.sleep(2)
            


def init_():

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=mainLoop)
    write_thread.start()


if __name__ == "__main__":

    try:
        con()
        init_()
    except:
        print("An Error Occured!")