from flask import request, Blueprint
from database import Photos, Users, Albums, db
from werkzeug.utils import secure_filename
import validateToken
from PIL import Image
from PIL.ExifTags import TAGS
import base64
from os import path, remove

from dotenv import dotenv_values
config = dotenv_values(".env")

photosBlueprint = Blueprint("photosBlueprint", __name__)
@photosBlueprint.route("/api/v1/photos", methods=["POST", "PATCH", "GET", "DELETE"])
@validateToken.validateToken
def photos(currentUser):
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            return {"string" : "No file part in the request"}, 400
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {"string" : "No selected file"}, 400

        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(path.join(config["UPLOAD_FOLDER"], filename))

        orientation = createThumbnail(filename)

        photo = Photos(**request.form)
        photo.photoName = filename.split(".")[0]
        photo.userID = currentUser.userID
        photo.orientation = orientation
        photo.photoPath = path.join(config["UPLOAD_FOLDER"], filename)
        photo.thumbPath = path.join(config["THUMB_FOLDER"], filename)
        photo.photoType = filename.split(".")[-1]
        db.session.add(photo)
        db.session.commit()
        return {"string": "Created photo."}
    elif request.method == "PATCH":
        return {"string": "Updating photo."}
    elif request.method == "GET":
        if "favorites" in request.args and request.args.get("favorites") == "true":
            photos = Users.query.filter_by(email=currentUser.email).first().photos.filter_by(favorite=True).all()
        else:
            photos = Users.query.filter_by(email=currentUser.email).first().photos

        output = []

        for photo in photos:
            image = open(photo.thumbPath, "rb")
            encoded = base64.b64encode(image.read()).decode("utf-8")
            output += [{"image": encoded, "imageID": photo.photoID, "orientation": photo.orientation, "type": photo.photoType, "favorite": photo.favorite}]
            
        return {"data": output}
    elif request.method == "DELETE":
        photo = Photos.query.filter_by(photoID=request.json["photoID"]).first()
        remove(photo.photoPath)
        Photos.query.filter_by(photoID=request.json["photoID"]).delete()
        db.session.commit()
        return {"string": "Deleted photo."}

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config["ALLOWED_EXTENSIONS"]

def saveImage():
    return {"string": "Saving image."}

def createThumbnail(filename):
    try:
        image = Image.open(config["UPLOAD_FOLDER"] + "/" + filename)
        metadata = image.getexif()
        orientation = 1
        for tagID in metadata:
            # get the tag name
            tag = TAGS.get(tagID, tagID)
            if tag == "Orientation":
                orientation = metadata.get(tagID)

        size = 512, 512
        image.thumbnail(size)

        if orientation != 1:
            #image = Image.open(config["THUMB_FOLDER"] + "/" + filename)
            if orientation == 6:
                image.rotate(-90, expand=True).save(config["THUMB_FOLDER"] + "/" + filename)
            elif orientation == 8:
                image.rotate(90, expand=True).save(config["THUMB_FOLDER"] + "/" + filename)
            elif orientation == 3:
                image.rotate(180, expand=True).save(config["THUMB_FOLDER"] + "/" + filename)
        else:
            image.save(config["THUMB_FOLDER"] + "/" + filename)

        if image.format == "PNG":
            if image.height > image.width:
                return "portrait"
            else:
                return "landscape"
        elif orientation == 1 or orientation == 3:
            if image.height > image.width:
                return "portrait"
            else:
                return "landscape"
        else: 
            return "portrait"

    except IOError:
        return IOError

@photosBlueprint.route("/api/v1/photo/favorite", methods=["POST"])
@validateToken.validateToken
def favorite(currentUser):
    photo = Photos.query.filter_by(userID=currentUser.userID, photoID=request.json["photoID"])
    photo.update({"favorite": bool(request.json["setFavorite"])})
    db.session.commit()
    return {
        "result": "Successfully updated favorites.",
        "isFavorite": photo.first().favorite
    }

@photosBlueprint.route("/api/v1/photo/album", methods=["POST", "DELETE"])
@validateToken.validateToken
def album(currentUser):
    if request.method == "POST":
        photoType = type(request.json["photoID"])
        albumType = type(request.json["albumID"])
        if photoType == int and albumType == int:
            album = Albums.query.filter_by(albumID=request.json["albumID"]).first()
            album.photos.append(Photos.query.filter_by(photoID=request.json["photoID"]).first())
            db.session.commit()
            return {"string": "Added photo to album."}
        elif photoType == list and albumType == int:
            album = Albums.query.filter_by(albumID=request.json["albumID"]).first()
            for photo in request.json["photoID"]:
                album.photos.append(Photos.query.filter_by(photoID=photo).first())
            db.session.commit()
            return {"string": "Added photos to album."}
        elif photoType == int and albumType == list:
            for album in request.json["albumID"]:
                Albums.query.filter_by(albumID=album).first().photos.append(Photos.query.filter_by(photoID=request.json["photoID"]).first())
            db.session.commit()
            return {"string": "Added photo to albums."}
        else:
            return {"string": "Invalid request."}
    elif request.method == "DELETE":
        print("Bye")
        return {"string": "Removing photo from album."}