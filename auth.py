from flask import request, Blueprint, jsonify
from database import db, Users
from validateToken import invalidate
import validateToken
import bcrypt
import jwt
import datetime

from dotenv import dotenv_values
config = dotenv_values(".env")

authBlueprint = Blueprint("authBlueprint", __name__)
@authBlueprint.route("/api/v1/auth/login", methods=["POST"])
def login():
    result = Users.query.filter(( Users.username ==request.json["userIdentifier"] ) | ( Users.email == request.json["userIdentifier"] )).first()
    print(result.password)
    if result is None or result.password is None:
        return {"result": "User not found"}
    elif bcrypt.checkpw(request.json["password"].encode("utf-8"), result.password):
        if result.needsNewToken:
            result.needsNewToken = False
            db.session.commit()

        encoded = jwt.encode({"username": result.username, "email": result.email, "exp": datetime.datetime.now() + datetime.timedelta(days=7)}, config["JWT_SECRET"], algorithm="HS512")
        response = jsonify(result="Success",token=encoded)
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
