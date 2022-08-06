from flask import request, Blueprint, jsonify
from database import db, Users
import bcrypt
import validateToken

userBlueprint = Blueprint("userBlueprint", __name__)
@userBlueprint.route("/api/v1/user", methods=["GET", "POST", "PATCH", "DELETE"])
@validateToken.validateToken
def user(currentUser):
    ## Method to get user info ##
    if request.method == "GET":  
        result ={
            "username": currentUser.username,
            "firstName": currentUser.firstName,
            "lastName": currentUser.lastName,
            "email": currentUser.email,
            "userID": currentUser.userID,
            "needsNewToken": currentUser.needsNewToken,
            "registrationMethod": currentUser.registrationMethod
        }
        return result
    ## Method to create user ##
    elif request.method == "POST":
        checkUsername = Users.query.filter_by(username=request.json["username"]).first()
        if checkUsername is not None:
            return {"result": "Username taken"}

        checkEmail = Users.query.filter_by(email=request.json["email"]).first()
        if checkEmail is not None:
            return {"result": "Email already exists in the database"}
        
        user = Users(**request.json)
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(request.form["password"].encode("utf-8"), salt)
        user.password = password

        db.session.add(user)
        db.session.commit()
        return {"string": "Created user."}

    ## Method to update user information ##
    elif request.method == "PATCH":
        user = Users.query.filter_by(userID=currentUser.userID).update(dict(request.json))
        db.session.commit()
        return {"string": "Updating user."}

    ## Method to delete user ##
    elif request.method == "DELETE":
        if bcrypt.checkpw(request.json["password"].encode("utf-8"), currentUser.password):
            Users.query.filter_by(userID = currentUser.userID).delete()
            db.session.commit()
            return {"string": "Deleted user."}
        else:
            return {"string": "Incorrect password"}

@userBlueprint.route("/api/v1/user/albums", methods=["GET"])
@validateToken.validateToken
def userAlbums(currentUser):
    albums = Users.query.filter_by(email=currentUser.email).first().albums
    return jsonify(albums)