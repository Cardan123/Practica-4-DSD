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

tiempo = []

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
        i += 1
        # send book's name to client
        clientConnectionsBooks[connection].send(str(book).encode('ascii'))
    else:
        img['file'] = 'preview.png'
        message = 'Libros terminados'
        clientConnectionsBooks[connection].send(message.encode('ascii'))

def createClientThread(connection, c):
    while True:
        data = c.recv(1024)
        tiempo.append(data.decode('ascii'))
        print(tiempo)
    c.close()


def createRequestThread(connection2, c2):
    while True:
        data2 = c2.recv(1024)
        print(data2)
        sendBookInfo(connection2)
    c2.close()


def acceptConnections():
    numOfConnections = 0
    host = '192.168.1.65'  # modify the ip addr as you need
    port = 12350
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
    hostRequestBook = '192.168.1.65'  # modify the ip addr as you need
    portRequestBook = 12351
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



# -----------
#   GUI
# -----------
window = tk.Tk()
window.geometry('1000x760')
window.title("Server Tiempo")



# Creating and starting the socket-listening thread
socketThread = threading.Thread(target=acceptConnections)
socketThread.start()

# Socket to listen request
socketRequestThread = threading.Thread(target=acceptRequestBooks)
socketRequestThread.start()




window.mainloop()