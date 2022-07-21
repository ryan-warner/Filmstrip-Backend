from flask import request, Blueprint, jsonify
from db import cursor, connection
import bcrypt
import jwt
import datetime
from validateToken import invalidate
import validateToken

from dotenv import dotenv_values
config = dotenv_values(".env")

authBlueprint = Blueprint("authBlueprint", __name__)
@authBlueprint.route("/api/v1/auth/login", methods=["POST"])
def login():
    returnUser = "SELECT * FROM users WHERE username = %s OR email = %s"
    values = (request.json['userIdentifier'],request.json['userIdentifier'])

    cursor.execute(returnUser, values)
    result = cursor.fetchone()
    
    if result is None:
        return {"result": "User not found"}
    elif bcrypt.checkpw(request.json["password"].encode("utf-8"), result[5]):

        updateUser = "UPDATE users SET needsNewToken = false WHERE email = %s"
        values = (result[3],)
        cursor.execute(updateUser, values)
        connection.commit()

        encoded = jwt.encode({"username": result[0], "email": result[3], "exp": datetime.datetime.now() + datetime.timedelta(days=7)}, config["JWT_SECRET"], algorithm="HS512")
        response = jsonify(result="Success",token=encoded)
        #response.headers.add("Access-Control-Allow-Origin","http://localhost:3000")
        #response.headers.add("content-type","application/json; charset=utf-8")
        return response
        
    else: 
        return {"result": "Incorrect password"}

@authBlueprint.route("/api/v1/auth/logout", methods=["POST"])
@validateToken.validateToken
def logout(currentUser):
    invalidate(currentUser)
    return {"string": "Logging out user."}

@authBlueprint.route("/api/v1/auth/verify", methods=["GET"])
@validateToken.validateToken
def verify():
    return {
            "message": "Token valid",
            "data": None,
            "error": "None"
        }, 200
