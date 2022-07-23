import atexit
#from mysql.connector import connect
from flask_sqlalchemy import SQLAlchemy

engine = SQLAlchemy.create_engine("mysql://root:@localhost:3306/filmstrip")
usersMetaData = SQLAlchemy.MetaData()

users = SQLAlchemy.Table('users', usersMetaData,
    SQLAlchemy.Column('username', SQLAlchemy.String(255)),
    SQLAlchemy.Column('firstName', SQLAlchemy.String(255)),
    SQLAlchemy.Column('lastName', SQLAlchemy.String(255)),
    SQLAlchemy.Column('email', SQLAlchemy.String(length=255)),
    SQLAlchemy.Column('userId', SQLAlchemy.Integer, primary_key=True, Nullable=False),
    SQLAlchemy.Column('password', SQLAlchemy.BINARY(length=60)),
    SQLAlchemy.Column('needsNewToken', SQLAlchemy.BOOLEAN, default=False),
    SQLAlchemy.Column('registrationMethod', SQLAlchemy.String(length=255), default="username")
)
    

#connection = connect(host='localhost', user='root', database='filmstrip')
connection = engine.connect()
connection.execute(users.select())

cursor = connection.cursor(buffered=True)

import atexit
@atexit.register
def shutdown():
    connection.close()
    cursor.close()
    print("Done")