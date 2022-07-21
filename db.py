import atexit
from mysql.connector import connect

connection = connect(host='localhost', user='root', database='filmstrip')
cursor = connection.cursor(buffered=True)

import atexit
@atexit.register
def shutdown():
    connection.close()
    cursor.close()
    print("Done")