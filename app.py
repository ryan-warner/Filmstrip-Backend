from flask import Flask, request
from mysql.connector import connect
import bcrypt

# export FLASK_DEBUG=1

app = Flask(__name__)
connection = connect(host='localhost', user='root', database='filmstrip')
cursor = connection.cursor()

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    returnUser = "SELECT * FROM users WHERE username = %s OR email = %s"
    values = (request.form['userIdentifier'],request.form['userIdentifier'])

    cursor.execute(returnUser, values)
    result = cursor.fetchone()
    
    if result is None:
        return {"result": "User not found"}
    elif bcrypt.checkpw(request.form["password"].encode("utf-8"), result[5]):
        return {"result": "Success"}
    else: 
        return {"result": "Incorrect password"}

@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return {"string": "Logging out user."}

@app.route("/api/v1/user", methods=["GET", "POST", "PATCH", "DELETE"])
def user():
    if request.method == "GET":
        getUser = "SELECT * FROM users WHERE email = %s"
        values = (request.args["email"],)
        cursor.execute(getUser, values)
        result = cursor.fetchone()
        
        # Pull password with bytes(result[5])
        print(bcrypt.checkpw("69P@rkroad5065".encode("utf-8"), bytes(result[5])))
        
        return {
            "username": result[0],
            "firstName": result[1],
            "lastName": result[2],
            "fullName": result[1] + " " + result[2],
            "email": result[3]
        }
    elif request.method == "POST":
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), salt)
        print(len(password))
        print(password)

        values = (request.form["username"], request.form["firstName"], request.form["lastName"], request.form["email"], password)
        registerUser = "INSERT INTO users" \
            "(username, firstName, lastName, email, password)" \
            "VALUES (%s, %s, %s, %s, %s)"
        
        cursor.execute(registerUser, values)
        connection.commit()
        
        cursor.execute("SELECT * FROM users")
        for x in cursor:
            print(x)

        return {"string": "Creating user."}
    
    elif request.method == "PATCH":
        return {"string": "Updating user."}

    elif request.method == "DELETE":
        getUser = "SELECT * FROM users WHERE email = %s"
        values = (request.form["email"],)
        cursor.execute(getUser, values)
        result = cursor.fetchone()

        if bcrypt.checkpw(request.form["password"].encode("utf-8"), bytes(result[5])):
            deleteUser = "DELETE FROM users WHERE email = %s"
            values = (request.form["email"],)

            cursor.execute(deleteUser, values)
            connection.commit()
            return {"string": "User Deleted"}
        else:
            return {"string": "Incorrect password"}

@app.route("/api/v1/user/photos", methods=["GET"])
def getPhotos():
    return {"string": "Getting photos."}