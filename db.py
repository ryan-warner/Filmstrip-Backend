from mysql.connector import connect

connection = connect(host='localhost', user='root', database='filmstrip')
cursor = connection.cursor()