import tkinter as tk
import threading
from time import strftime,sleep
from random import randint
import socket
import re

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

def validateHour(hour):
    hours=int(hour.split(':')[0])
    mins=int(hour.split(':')[1])
    secs=int(hour.split(':')[2])
    if secs>=60:
        secs=0
        mins+=1
        if mins>=60:
            mins=0
            hours+=1
            if hours>=24:
                hours=0
    return str(hours).zfill(2)+':'+str(mins).zfill(2)+':'+str(secs).zfill(2)

def receiveData():
    global factor
    global pause
    while True:
        #receiving book
        code = (sock2.recv(1024)).decode('ascii')
        tiempo = (sock2.recv(1024)).decode('ascii')
        print(code)
        txtVarClk0.set(code)
        
def generateRandomHour():
    h=str(randint(0,23))
    m=str(randint(0,59))
    s=str(randint(0,59))
    return h.zfill(2)+':'+m.zfill(2)+':'+s.zfill(2)

def runClock():
    global tiempo
    time_new = tiempo
    global pause
    global factor
    while pause==False:
        time_new=validateHour(time_new.split(':')[0]+':'+time_new.split(':')[1]+':'+str(int(time_new.split(':')[2])+1).zfill(2))
        sock4.send(time_new.encode('ascii'))
        sock.send(time_new.encode('ascii'))
        txtVarClk.set(time_new)
        sleep(1*factor)

def sendRequestBook(request):
    sock2.send(request.encode('ascii'))
    sock3.send(request.encode('ascii'))
    txtVarClkresult.set(request)

def sendResetBook(request):
    print('Reset SEND')
    sock5.send(request.encode('ascii'))
    sock6.send(request.encode('ascii'))

def requestBook():
    request='Libro Pedido'
    threadSendRequest=threading.Thread(target=lambda: sendRequestBook(request))
    threadSendRequest.start()

def resetBooks():
    print('Reset button')
    request='Reset'
    threadSendReset=threading.Thread(target=lambda: sendResetBook(request))
    threadSendReset.start()

tiempo = generateRandomHour()
window = tk.Tk()
window.geometry('520x420')
window.title('Client')
txtVarClk=tk.StringVar(window)
txtVarClkresult=tk.StringVar(window, value='No has realizado ninguna petición')
txtVarClk0=tk.StringVar(window, value='Vista previa Título')

lblClk=tk.Label(window,textvar=txtVarClk,bg="black",fg="green",font="consoles 40 bold").pack(pady=(65,30))
lblClkstatus=tk.Label(window,text='Estatus Petición:',font="consoles 10 bold").pack(pady=(10,10))
lblClkresult=tk.Label(window,textvar=txtVarClkresult,font="consoles 14").pack(pady=(15,30))
lblClk0 = tk.Label(window, textvar=txtVarClk0, anchor='e', fg="red", font="consoles 20 bold").pack(pady=(15,30))

button = tk.Button(window, text="Pedir libro", fg="black", command=requestBook)
button.pack()

buttonreset = tk.Button(window, text="Reiniciar libros", fg="black", command=resetBooks)
buttonreset.pack()

threadSend=threading.Thread(target=lambda: runClock(tiempo))
threadSend.start()

threadReceive=threading.Thread(target=lambda: receiveData())
threadReceive.start()

window.mainloop()
sock.close()
sock4.close()