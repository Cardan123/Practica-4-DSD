import tkinter as tk
import threading
from time import strftime,sleep
from random import randint
import socket
import re

host='192.168.1.64'  #modify the ip addr as you need (server that gives the HOUR)
port=12350          #(MAIN SERVER, port that gives hour)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))
pause=False
factor=1.0

host2='192.168.1.64'  #modify the ip addr as you need 
port2=12351          #(MAIN SERVER, port that gives the BOOKS)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2.connect((host2,port2))

host3='192.168.1.64'  #modify the ip addr as you need 
port3=12352          #(BACKUPSERVER, port that gives BOOKS)
sock3 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock3.connect((host3,port3))

host4='192.168.1.64'  #modify the ip addr as you need 
port4=12353          #(BACKUPSERVER, port that gives hour)
sock4 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock4.connect((host4,port4))

def receiveData():
    global factor
    global pause
    while True:
        #receiving book
        code = (sock2.recv(1024)).decode('ascii')
        print(code)
        txtVarClk0.set(code)

def sendRequestBook(request):
    sock2.send(request.encode('ascii'))
    sock4.send(request.encode('ascii'))
    txtVarClkresult.set(request)

def sendResetBook(request):
    print('Reset SEND')
    sock.send(request.encode('ascii'))
    sock3.send(request.encode('ascii'))

def requestBook():
    request='Libro Pedido'
    threadSendRequest=threading.Thread(target=lambda: sendRequestBook(request))
    threadSendRequest.start()

def resetBooks():
    print('Reset button')
    request='Reset'
    threadSendReset=threading.Thread(target=lambda: sendResetBook(request))
    threadSendReset.start()

window = tk.Tk()
window.geometry('520x420')
window.title('Client')
txtVarClkresult=tk.StringVar(window, value='No has realizado ninguna petición')
txtVarClk0=tk.StringVar(window, value='Vista previa Título')

lblClkstatus=tk.Label(window,text='Estatus Petición:',font="consoles 10 bold").pack(pady=(10,10))
lblClkresult=tk.Label(window,textvar=txtVarClkresult,font="consoles 14").pack(pady=(15,30))
lblClk0 = tk.Label(window, textvar=txtVarClk0, anchor='e', fg="red", font="consoles 20 bold").pack(pady=(15,30))

button = tk.Button(window, text="Pedir libro", fg="black", command=requestBook)
button.pack()

buttonreset = tk.Button(window, text="Reiniciar libros", fg="black", command=resetBooks)
buttonreset.pack()

threadReceive=threading.Thread(target=lambda: receiveData())
threadReceive.start()

window.mainloop()
sock.close()
sock4.close()


