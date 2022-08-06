from flask import request, Blueprint, jsonify
from database import Albums, db, Users
import validateToken
import base64

albumsBlueprint = Blueprint("albumsBlueprint", __name__)
@albumsBlueprint.route("/api/v1/albums", methods=["POST", "PATCH", "GET", "DELETE"])
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
        photos = Albums.query.filter_by(userID=currentUser.userID, albumID=request.args.get("albumID")).first().photos.all()
        output = []

        for photo in photos:
            image = open(photo.thumbPath, "rb")
            encoded = base64.b64encode(image.read()).decode("utf-8")
            output += [{"image": encoded, "imageID": photo.photoID, "orientation": photo.orientation, "type": photo.photoType, "favorite": photo.favorite}]
            
        return {"data": output}

    elif request.method == "DELETE":
        Albums.query.filter_by(albumName=request.json["albumName"], userID = currentUser.userID).delete()
        db.session.commit()
        return {"string": "Deleted album."}
