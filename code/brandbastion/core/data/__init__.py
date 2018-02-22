import mysql.connector


DATA_PATH = '../../../data'

cnx = None
cursor = None

if not (cnx or cursor):
    cnx = mysql.connector.connect(user='root', database='brandbastion', password = 'root')
    cursor = cnx.cursor()

    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
