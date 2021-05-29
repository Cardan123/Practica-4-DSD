# SERVER

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
import pickle


# conection drive to postgresql
import psycopg2

json_filename = 'books.json'
clientThreads = []  # List of client threads
clientIPs = []  # List of client IPs
clientConnections = []  # List of clients connection tuple
clientClockSpeeds = [0, 0, 0, 0]  # Speed of each clock
masterClockSpeed = 0
factor = 1.0

clientThreadsBook = []  # List of client threads
clientIPsBooks = []  # List of client IPs
clientConnectionsBooks = []  # List of clients connection tuple
factor2 = 1.0
pause = False  # Pause flag fors master clock


clientIPsBooks3 = []  # List of client IPs
clientConnectionsBooks3 = []  # List of clients connection tuple
clientThreadsBook3 = []  # List of client threads

host='192.168.1.65'  #modify the ip addr as you need (server that gives the HOUR)
port=12350          #(MAIN SERVER, port that gives hour)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((host,port))
pause=False
factor=1.0

host2='192.168.1.65'  #modify the ip addr as you need 
port2=12351          #(MAIN SERVER, port that gives the BOOKS)
sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2.connect((host2,port2))

books = [
    {'ISBN': '0984782869', 'name': 'Cracking the coding interview', 'author': 'Gayle Laakmann',
        'editorial': 'Careercup', 'price': 569, 'portada': 'cracking.png'},
    {'ISBN': '9780132350884', 'name': 'Clean Code', 'author': 'Robert Martin',
        'editorial': 'Prentice Hall', 'price': 818, 'portada': 'cleancode.png'},
    {'ISBN': '0135957052', 'name': 'The Pragmatic Programmer', 'author': 'David Thomas',
        'editorial': 'Addison-Wesley Professional', 'price': 818, 'portada': 'pragmatic.png'},
    {'ISBN': '0201633612', 'name': 'Design Patterns', 'author': 'Erich Gamma',
        'editorial': 'Addison-Wesley Professional', 'price': 1286, 'portada': 'design.png'},
    {'ISBN': '9780262033848', 'name': 'Introduction to Algorithms', 'author': 'Thomas H Cormen',
        'editorial': 'MIT Press', 'price': 1390, 'portada': 'algorithms.png'},
    {'ISBN': '1492052205', 'name': 'Architecture Patterns with Python', 'author': 'Harry Percival',
        'editorial': 'O Reilly Media', 'price': 1016, 'portada': 'architecture.png'},
    {'ISBN': '0135404673', 'name': 'Intro to Python for Computer Science', 'author': 'Paul Deitel',
        'editorial': 'Pearson', 'price': 1534, 'portada': 'python.png'},
    {'ISBN': '1108422098', 'name': 'Data-Driven Science and Engineering', 'author': 'Steven L Brunton',
        'editorial': 'Cambridge University Press', 'price': 1256, 'portada': 'data.png'}
]

tiempo = ['0:0:0','0:0:0','0:0:0','0:0:0']
def validateMasterHour(hour):
    hours = int(hour.split(':')[0])
    mins = int(hour.split(':')[1])
    secs = int(hour.split(':')[2])
    if secs >= 60:
        secs = 0
        mins += 1
        if mins >= 60:
            mins = 0
            hours += 1
            if hours >= 24:
                hours = 0
    return str(hours).zfill(2)+':'+str(mins).zfill(2)+':'+str(secs).zfill(2)


def editMasterHour():
    global pause
    pause = True
    hour = simpledialog.askstring("Editar hora maestra", "Escribe la nueva hora (HH:MM:SS)",
                                  parent=window, initialvalue=txtVarClk0.get())
    if hour == None:  # if the user selects "cancel"
        hour = txtVarClk0.get()
    pause = False
    masterClkThread = threading.Thread(target=lambda: runMasterClock(hour))
    masterClkThread.start()


def editMasterSpeed(power):
    global factor
    global masterClockSpeed
    masterClockSpeed = masterClockSpeed+power
    factor = pow(2, masterClockSpeed)


def runMasterClock(hour):
    time_new = hour
    tiempo[0] = time_new
    global pause
    global factor
    while pause == False:
        time_new = validateMasterHour(time_new.split(
            ':')[0]+':'+time_new.split(':')[1]+':'+str(int(time_new.split(':')[2])+1).zfill(2))
        txtVarClk0.set(time_new)
        sleep(1*factor)


def sendBookInfo(connection):
    # generate random book
    lengBooks = len(books)
    lengBooks -= 1
    # get address and port cliente that requests
    print(clientConnectionsBooks[connection].getsockname()[0])
    print(clientConnectionsBooks[connection].getsockname()[1])
    if lengBooks >= 1:
        i = 0
        book = books[i]['name']
        image = books[i]['portada']
        print(books.pop(i))
        print('book')
        # replace the image book
        img['file'] = image
        now = datetime.now()
        request_time = now.strftime("%H:%M:%S")
        iprequest = clientConnectionsBooks[connection].getsockname()[0]
        # connect to database each request, you have to create a PostgreSQL
        conn = psycopg2.connect(
            dbname='postgres', user='cardan', password='12345', host='localhost', port='5432')
        cursor = conn.cursor()
        query = '''INSERT INTO requestBooks(ip, hora, libro) VALUES (%s,%s,%s);'''
        # values to send to database
        cursor.execute(query, (iprequest, request_time, book))
        print('Data saved')
        conn.commit()
        conn.close()
        i += 1
        # send book's name to client
        clientConnectionsBooks[connection].send(str(book).encode('ascii'))
    else:
        img['file'] = 'preview.png'
        message = 'Libros terminados'
        clientConnectionsBooks[connection].send(message.encode('ascii'))


def editSpeed(connection, power):
    clientClockSpeeds[connection] = clientClockSpeeds[connection]+power
    clientFactor = pow(2, clientClockSpeeds[connection])
    clientConnections[connection].send(str(clientFactor).encode('ascii'))

# run enviroment for the "newThread" thread: reads the data sent from clients
# and puts the data into the corresponding StringVar for clocks update

def createClientThread(connection, c):
    while True:
        data = c.recv(1024)
        print(data)
        txtVarClks[connection].set(data.decode('ascii'))
        if(connection != 3):
            tiempo[connection+1] = (data.decode('ascii'))
        print(tiempo)
    c.close()


def createRequestThread(connection2, c2):
    while True:
        data2 = c2.recv(1024)
        print(data2)
        sendBookInfo(connection2)
    c2.close()


def createResetThread(connection2, c3):
    while True:
        data2 = c3.recv(1024)
        print(data2)
        global books 
        books = [
            {'ISBN': '0984782869', 'name': 'Cracking the coding interview', 'author': 'Gayle Laakmann',
             'editorial': 'Careercup', 'price': 569, 'portada': 'cracking.png'},
            {'ISBN': '9780132350884', 'name': 'Clean Code', 'author': 'Robert Martin',
             'editorial': 'Prentice Hall', 'price': 818, 'portada': 'cleancode.png'},
            {'ISBN': '0135957052', 'name': 'The Pragmatic Programmer', 'author': 'David Thomas',
             'editorial': 'Addison-Wesley Professional', 'price': 818, 'portada': 'pragmatic.png'},
            {'ISBN': '0201633612', 'name': 'Design Patterns', 'author': 'Erich Gamma',
             'editorial': 'Addison-Wesley Professional', 'price': 1286, 'portada': 'design.png'},
            {'ISBN': '9780262033848', 'name': 'Introduction to Algorithms', 'author': 'Thomas H Cormen',
             'editorial': 'MIT Press', 'price': 1390, 'portada': 'algorithms.png'},
            {'ISBN': '1492052205', 'name': 'Architecture Patterns with Python', 'author': 'Harry Percival',
             'editorial': 'O Reilly Media', 'price': 1016, 'portada': 'architecture.png'},
            {'ISBN': '0135404673', 'name': 'Intro to Python for Computer Science', 'author': 'Paul Deitel',
             'editorial': 'Pearson', 'price': 1534, 'portada': 'python.png'},
            {'ISBN': '1108422098', 'name': 'Data-Driven Science and Engineering', 'author': 'Steven L Brunton',
             'editorial': 'Cambridge University Press', 'price': 1256, 'portada': 'data.png'}
        ]
    c3.close()

# run enviroment for the "socketThread" thread: starts the socket, puts the socket in listen mode
# and creates a new thread for each new client connection


def acceptConnections():
    numOfConnections = 0
    host = '192.168.1.64'  # modify the ip addr as you need
    port = 12345
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.bind((host, port))
    clientSocket.listen(5)
    while True:
        c, addr = clientSocket.accept()
        if(addr[0] not in clientIPs and numOfConnections <= 3):
            clientIPs.append(addr[0])
            newThread = threading.Thread(
                target=lambda: createClientThread(numOfConnections, c))
            clientThreads.append(newThread)
            clientThreads[numOfConnections].start()
            clientConnections.append(c)
            numOfConnections += 1
    clientSocket.close()


def acceptRequestBooks():
    numOfConnections2 = 0
    hostRequestBook = '192.168.1.64'  # modify the ip addr as you need
    portRequestBook = 12346
    clientBookSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientBookSocket.bind((hostRequestBook, portRequestBook))
    clientBookSocket.listen(5)
    while True:
        c, addr = clientBookSocket.accept()
        if(addr[0] not in clientIPsBooks and numOfConnections2 <= 3):
            clientIPsBooks.append(addr[0])
            newThread = threading.Thread(
                target=lambda: createRequestThread(numOfConnections2, c))
            clientThreadsBook.append(newThread)
            clientThreadsBook[numOfConnections2].start()
            clientConnectionsBooks.append(c)
            numOfConnections2 += 1
    clientBookSocket.close()


def acceptResetBooks():
    numOfConnections3 = 0
    hostRequestBook3 = '192.168.1.64'  # modify the ip addr as you need
    portRequestBook3 = 12341
    clientBookSocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientBookSocket3.bind((hostRequestBook3, portRequestBook3))
    clientBookSocket3.listen(5)
    while True:
        c, addr = clientBookSocket3.accept()
        if(addr[0] not in clientIPsBooks3 and numOfConnections3 <= 3):
            clientIPsBooks3.append(addr[0])
            newThread = threading.Thread(
                target=lambda: createResetThread(numOfConnections3, c))
            clientThreadsBook3.append(newThread)
            clientThreadsBook3[numOfConnections3].start()
            clientConnectionsBooks3.append(c)
            numOfConnections3 += 1
    clientBookSocket3.close()


##ServerTiempo
def sendTiempo(hour):
    time_new=hour
    global pause
    global factor
    while pause==False:
        dataTiempo = pickle.dumps(tiempo)
        sock.send(dataTiempo)
        sleep(1*factor)

# -----------
#   GUI
# -----------
window = tk.Tk()
window.geometry('1000x760')
window.title("Server Central")
txtVarClk0 = tk.StringVar(window, value='00:00:00')
txtVarClk1 = tk.StringVar(window, value='00:00:00')
txtVarClk2 = tk.StringVar(window, value='00:00:00')
txtVarClk3 = tk.StringVar(window, value='00:00:00')
txtVarClks = [txtVarClk1, txtVarClk2, txtVarClk3]
# with open(json_filename, 'r') as inside:
#     data = json.load(inside)
# text = tk.Text(window, state='normal', height=10, width=60)
# text.place(x=650, y=100)
# text.insert('1.0', str(data))

# Clock 0 (Master)
lblClk0a = tk.Label(window, text="Master Clock")
lblClk0a.grid(column=0, row=0, pady=(10, 0), padx=(30, 30), columnspan=3)
lblClk0 = tk.Label(window, textvar=txtVarClk0, anchor='e',
                   bg="black", fg="red", font="consoles 40 bold")
lblClk0.grid(column=0, row=1, pady=(10, 0), padx=(30, 30), columnspan=3)


# Clock 1
lblClk1a = tk.Label(window, text="Client 1")
lblClk1a.grid(column=4, row=0, pady=(10, 0), padx=(30, 30), columnspan=3)
lblClk1 = tk.Label(window, textvar=txtVarClk1, anchor='e',
                   bg="black", fg="green", font="consoles 40 bold")
lblClk1.grid(column=4, row=1, pady=(10, 0), padx=(30, 30), columnspan=3)


# Clock 2
lblClk2a = tk.Label(window, text="Client 2")
lblClk2a.grid(column=0, row=2, pady=(10, 0), padx=(30, 30), columnspan=3)
lblClk2 = tk.Label(window, textvar=txtVarClk2, anchor='e',
                   bg="black", fg="green", font="consoles 40 bold")
lblClk2.grid(column=0, row=3, padx=(30, 30), columnspan=3)

# lblC = tk.Label(window, textvar=txtVarClk5)
# lblC.grid(column=2, row=2, pady=(10, 0), padx=(30, 30), columnspan=3)

# Clock 3
lblClk3a = tk.Label(window, text="Client 3")
lblClk3a.grid(column=4, row=2, pady=(10, 0), padx=(30, 30), columnspan=3)
lblClk3 = tk.Label(window, textvar=txtVarClk3, anchor='e',
                   bg="black", fg="green", font="consoles 40 bold")
lblClk3.grid(column=4, row=3, padx=(30, 30), columnspan=3)

#Books in variable
lblBooksTitle = tk.Label(
    window, text="Available Books", font="consoles 14 bold")
lblBooksTitle.grid(column=7, row=0, pady=(10, 0), padx=(30, 30), columnspan=3)


def applytoLabel():
    n = len(books)
    element = ''
    for i in range(n):
        element = element + books[i]['name']+'\n'
    return element


lblBooks = tk.Label(window, text=applytoLabel(), font="consoles 12")
lblBooks.grid(column=7, row=1, pady=(10, 0), padx=(30, 30), columnspan=3)



# BOOK
# i=random.randint(0,7)
# book=books[i]
# image = books[i]['portada']
# canvas = tk.Canvas(window, width=300, height=300)
# canvas.grid(column=4, row=5, pady=(50, 0), padx=(30, 30), columnspan=3)
# img = tk.PhotoImage(file=image)
# img = img.zoom(10)
# img = img.subsample(32)
# canvas.create_image(0, 0, image=img, anchor="nw")

# display initial image
img = tk.PhotoImage(file="preview.png")
# img = img.zoom(10)
#img = img.subsample(2)
label = tk.Label(window, image=img)
label.grid(column=4, row=5, pady=(50, 0), padx=(30, 30), columnspan=3)

# Creating and starting master clock thread
masterClkThread = threading.Thread(
    target=lambda: runMasterClock(strftime('%H:%M:%S')))
masterClkThread.start()

#Send Tiempo
threadSend=threading.Thread(target=lambda: sendTiempo(txtVarClks))
threadSend.start()

# Creating and starting the socket-listening thread
socketThread = threading.Thread(target=acceptConnections)
socketThread.start()

# Socket to listen request
socketRequestThread = threading.Thread(target=acceptRequestBooks)
socketRequestThread.start()

# Socket to listen reset
socketResetThread = threading.Thread(target=acceptResetBooks)
socketResetThread.start()

window.mainloop()
sock.close()