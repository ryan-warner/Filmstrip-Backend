from flask import request, Blueprint, jsonify, url_for
from database import Photos, Users, db
from werkzeug.utils import secure_filename
import validateToken
from os import path

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

        photo = Photos(**request.form)
        photo.userID = currentUser.userID
        photo.photoPath = path.join(config["UPLOAD_FOLDER"], filename)
        photo.thumbPath = path.join(config["THUMB_FOLDER"], filename)
        db.session.add(photo)
        db.session.commit()
        return {"string": "Created photo."}
    elif request.method == "PATCH":
        return {"string": "Updating photo."}
    elif request.method == "GET":
        return {"string": "Getting photo."}
    elif request.method == "DELETE":
        file.delete(path.join(config["UPLOAD_FOLDER"], filename))
        return {"string": "Deleted photo."}

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config["ALLOWED_EXTENSIONS"]

def saveImage():
    return {"string": "Saving image."}

def createThumbnail():
    return {"string": "Creating thumbnail."}

