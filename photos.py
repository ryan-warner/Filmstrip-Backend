from flask import request, Blueprint, jsonify, send_from_directory, url_for
from database import Photos, Users, db
from werkzeug.utils import secure_filename
import validateToken
from PIL import Image
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
            #file.save(path.join(config["UPLOAD_FOLDER"], filename))

        createThumbnail(filename)

        photo = Photos(**request.form)
        photo.photoName = filename.split(".")[0]
        photo.userID = currentUser.userID
        photo.photoPath = path.join(config["UPLOAD_FOLDER"], filename)
        photo.thumbPath = path.join(config["THUMB_FOLDER"], filename)
        #db.session.add(photo)
        #db.session.commit()
        return {"string": "Created photo."}
    elif request.method == "PATCH":
        return {"string": "Updating photo."}
    elif request.method == "GET":
        photos = Users.query.filter_by(email=currentUser.email).first().photos
        #print(photos[0].photoPath)
        output = []
        for photo in photos:

            #print(photo.photoPath)
            output.append(url_for("photosBlueprint.public", filename=photo.photoPath))
            print(output[0])
            
            return {"string" : "hi"}#send_from_directory(config["UPLOAD_FOLDER"], photo.photoPath.split("/")[-1])
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
        size = 512, 512
        image.thumbnail(size)
        image.save(config["THUMB_FOLDER"] + "/" + filename)
    except IOError:
        return IOError
