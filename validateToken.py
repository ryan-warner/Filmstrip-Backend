from functools import wraps
from flask import request
from database import db, Users
import jwt
import datetime

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
            currentUser = Users.query.filter_by(username=data["username"]).first()
            if currentUser is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if datetime.datetime.fromtimestamp(data["exp"]) < datetime.datetime.now():
                return {
                    "message": "User needs to login again!",
                    "data": None,
                    "error": "Authentication token expired"
                }, 401
            if currentUser.needsNewToken == True:
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

        if request.path == "/api/v1/auth/verify":
            return f(*args, **kwargs)

        return f(currentUser, *args, **kwargs)

    return decorated

def invalidate(currentUser):
    Users.query.filter_by(email=currentUser.email).update(dict(needsNewToken=True))
    db.session.commit()
    return None;