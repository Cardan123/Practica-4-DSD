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

host='192.168.1.64'  #modify the ip addr as you need (server that gives the HOUR)
port=12345          #(MAIN SERVER, port that gives hour)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))
pause=False
factor=1.0

host2='192.168.1.64'  #modify the ip addr as you need 
port2=12346          #(MAIN SERVER, port that gives the BOOKS)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2.connect((host2,port2))

host3='192.168.1.64'  #modify the ip addr as you need 
port3=12348          #(BACKUPSERVER, port that gives BOOKS)
sock3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock3.connect((host3,port3))

host4='192.168.1.64'  #modify the ip addr as you need 
port4=12347          #(BACKUPSERVER, port that gives hour)
sock4 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock4.connect((host4,port4))

host5='192.168.1.64'  #modify the ip addr as you need 
port5=12349          #(BACKUPSERVER, port that listen the RESET BUTTON)
sock5 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock5.connect((host5,port5))

host6='192.168.1.64'  #modify the ip addr as you need (server)
port6=12341          #(MAINSERVER, port that listen the RESET BUTTON)
sock6 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock6.connect((host6,port6))

sock.close()
sock4.close()

