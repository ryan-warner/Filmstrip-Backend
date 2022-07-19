from flask import Flask, request
from mysql.connector import connect
import uuid

app = Flask(__name__)
connection = connect(host='localhost', user='root', database='filmstrip')
cursor = connection.cursor()

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    return {"token": "logging in"}

@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return {"string": "Logging out user."}

@app.route("/api/v1/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        return {
            "name": "Ryan Warner",
            "username": "ryan-warner",
            "email": "ryan.warner@gatech.edu"
        }
    else:
        #print(cursor.execute("INSERT INTO users VALUES ('ryan-warner','Ryan','Warner','ryan.warner@gatech.edu','" + str(uuid.uuid4()) + "');"))

        cursor.execute("INSERT INTO users VALUES ('ryan-warner','Ryan','Warner','ryan.warner@gatech.edu',123)")
        connection.commit()
        cursor.execute("SELECT * FROM users")
        for x in cursor:
            print(x)

        return {"string": "Creating user."}

@app.route("/api/v1/user/photos", methods=["GET"])
def getPhotos():
    return {"string": "Getting photos."}