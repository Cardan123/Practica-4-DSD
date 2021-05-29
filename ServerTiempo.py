import tkinter as tk
from time import strftime, sleep
import socket
import threading
from tkinter import simpledialog
import json
from PIL import ImageTk, Image
import random
from datetime import datetime
import sys
import os

host = '192.168.3.3'  #modify the ip addr as you need (server that gives the HOUR)
port = 12345          #(MAIN SERVER, port that gives hour)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))
pause  = False
factor = 1.0

host4 = '192.168.3.3'  #modify the ip addr as you need 
port4 = 12347          #(BACKUPSERVER, port that gives hour)
sock4 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock4.connect((host4,port4))

def runClock(hour):
    print("hola")

def receiveData():
    print("hola")




threadSend=threading.Thread(target=lambda: runClock(2))
threadSend.start()

threadReceive=threading.Thread(target=lambda: receiveData())
threadReceive.start()

sock.close()
sock4.close()
