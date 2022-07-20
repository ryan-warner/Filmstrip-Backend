from flask import request, Blueprint
from db import cursor, connection
import bcrypt
import validateToken

userBlueprint = Blueprint("userBlueprint", __name__)
@userBlueprint.route("/api/v1/user", methods=["GET", "POST", "PATCH", "DELETE"])
@validateToken.validateToken
def user(currentUser):
    if request.method == "GET":        
        return {
            "username": currentUser[0],
            "firstName": currentUser[1],
            "lastName": currentUser[2],
            "fullName": currentUser[1] + " " + currentUser[2],
            "email": currentUser[3]
        }
    elif request.method == "POST":

        checkUser = "SELECT * FROM users WHERE username = %s OR email = %s"
        values = (request.form["username"], request.form["email"])
        cursor.execute(checkUser, values)

        if cursor.fetchone() is not None:
            return {"result": "User already exists"}

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), salt)

        values = (request.form["username"], request.form["firstName"], request.form["lastName"], request.form["email"], password)
        registerUser = "INSERT INTO users" \
            "(username, firstName, lastName, email, password)" \
            "VALUES (%s, %s, %s, %s, %s)"
        
        cursor.execute(registerUser, values)
        connection.commit()

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