from tkinter import *
import tkinter as tk
from datetime import datetime
import random
from time import sleep
import threading
import socket
import mysql.connector

HOST='192.168.1.65'
BKHOST = "192.168.1."
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
BCKPORT = 65433        # Port to listen on (non-privileged ports are > 1023)
TIMEPORT = 60432
now = datetime.now() # Fecha y hora actuales
random.seed(99)

mydb = mysql.connector.connect(
    host="localhost",
    user="cardan",
    password="password",
    database="Central"
)
mycursor = mydb.cursor()
sqlformula = "INSERT INTO requestBooks (ip, hora, libros) VALUES(%s,%s,%s)"

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
