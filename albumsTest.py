import json
from flask import request, Blueprint, jsonify
from testDB import Albums, db, Users
import validateToken

albumsBlueprintTest = Blueprint("albumsBlueprintTest", __name__)
@albumsBlueprintTest.route("/api/v2/albums", methods=["POST", "PATCH", "GET", "DELETE"])
@validateToken.validateToken
def albums(currentUser):
    if request.method == "POST":
        album = Albums(**request.json)
        album.userID = currentUser.userID
        db.session.add(album)
        db.session.commit()
        return {"string": "Created album."}

    elif request.method == "PATCH":
        albumID = request.json["albumID"]
        del request.json["albumID"]
        album = Albums.query.filter_by(albumID=albumID).update(dict(request.json))
        db.session.commit()
        return {"string": "Updating album."}

    elif request.method == "GET":
        albums = Users.query.filter_by(email=currentUser.email).first().albums
        return jsonify(albums)

    elif request.method == "DELETE":
        Albums.query.filter_by(albumName=request.json["albumName"], userID = currentUser.userID).delete()
        db.session.commit()
        return {"string": "Deleted album."}
