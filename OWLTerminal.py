import serial
from datetime import datetime
import threading
import time
import getpass
import sys
from termcolor import colored
import glob


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def serialRead(Serial):
    global pause
    while True:
        try:
            bytestoRead = Serial.readline()
            if(bytestoRead != ""):
                now = datetime.now()
                curentTime = now.strftime("%H:%M:%S.%f")
                serialMessage = bytestoRead.decode("utf-8").replace("\n","").replace("\r","")
                print(curentTime +  colored(" -->", 'green') + " : " + serialMessage)
                # print(curentTime + " --> : " + serialMessage)
        except Exception as e:
            print(str(e)) 
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
                sys.stdout.write("\033[F")
                print(curentTime + colored(" <--", 'red') + " : " + buffer)
                # print(curentTime + " <-- : " + buffer)
        except Exception as e:
            print(str(e)) 
            exit()
port = ""
baud = 0
ports = serial_ports()
try:
    port = sys.argv[1]
    baud = int(sys.argv[2])
except:
    pass
    
if(port == ""):
    for i in range(len(ports)):
        print(str(i) + " : " + str(ports[i]))
    print(str(len(ports)) + " : different port")
    numberPort = int(input("type port number: "))
    if len(ports) > numberPort:
        port = ports[numberPort].replace("tty.", "cu.")
    else:
        port = input("type port name: ")

if(baud == 0):
    baud = int(input("baudrate: "))


Serial = serial.Serial()
Serial.port = port
Serial.baudrate = baud
Serial.close()
Serial.open()

serialReadThread = threading.Thread(target=serialRead, args=(Serial,))
serialWriteThread = threading.Thread(target=serialWrite, args=(Serial,))
serialReadThread.start()
serialWriteThread.start()

    
        
