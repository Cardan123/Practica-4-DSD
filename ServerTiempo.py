import mysql.connector

#conexion base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="db"
)

#instancia de la conexion de la base de datos
mycursor = mydb.cursor()
sqlformula = "select * from Equipos"

def selectdb():
    mycursor.execute(sqlformula)