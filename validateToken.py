from functools import wraps
from flask import request
import jwt
import datetime
from db import cursor, connection

from dotenv import dotenv_values
config = dotenv_values(".env")

def validateToken(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if request.method == "POST" and request.path == "/api/v1/user":
            currentUser = None
            return f(currentUser, *args, **kwargs)
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, config["JWT_SECRET"], algorithms=["HS512"])
            returnUser = "SELECT * FROM users WHERE username = %s"
            values = (data["username"],)

            cursor.execute(returnUser, values)
            currentUser = cursor.fetchone()
            if currentUser is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if data["exp"] < datetime.now():
                return {
                    "message": "User needs to login again!",
                    "data": None,
                    "error": "Authentication token expired"
                }, 401
            if currentUser[6] == True:
                return {
                    "message": "User needs to login again!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except Exception as exception:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(exception)
            }, 500

        return f(currentUser, *args, **kwargs)

    return decorated

def invalidate(currentUser):
    updateUser = "UPDATE users SET needsNewToken = true WHERE email = %s"
    values = (currentUser[3],)
    cursor.execute(updateUser, values)
    connection.commit()
    return None;