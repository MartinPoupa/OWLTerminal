import serial
from datetime import datetime
import threading
import time
import getpass
import sys
from termcolor import colored

def serialRead(Serial):
    global pause
    while True:
        try:
            bytestoRead = Serial.readline()
            if(bytestoRead != ""):
                now = datetime.now()
                curentTime = now.strftime("%H:%M:%S.%f")
                serialMessage = bytestoRead.decode("utf-8").replace("\n","").replace("\r","")
                print("\n" + curentTime +  colored(" -->", 'green') + " : " + serialMessage, end = "")
        except Exception as e:
            print("\n" + str(e)) 
            exit()       
                
def serialWrite(Serial):
    global pause
    while True:
        try:
            buffer = getpass.getpass("")
            if(buffer != ""):
                now = datetime.now()
                curentTime = now.strftime("%H:%M:%S.%f")
                Serial.write((buffer + "\n").encode("UTF-8"))
                
                print(curentTime + colored(" <--", 'red') + " : " + buffer, end = "")
        except Exception as e:
            print("\n" + str(e)) 
            exit()

port = sys.argv[1]
baud = int(sys.argv[2])

Serial = serial.Serial()
Serial.port = port
Serial.baudrate = baud
Serial.close()
Serial.open()

serialReadThread = threading.Thread(target=serialRead, args=(Serial,))
serialWriteThread = threading.Thread(target=serialWrite, args=(Serial,))
serialReadThread.start()
serialWriteThread.start()

    
        
