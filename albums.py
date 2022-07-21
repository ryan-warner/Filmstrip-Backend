from flask import request, Blueprint
from db import cursor, connection
import validateToken

albumsBlueprint = Blueprint("albumsBlueprint", __name__)
@albumsBlueprint.route("/api/v1/albums", methods=["POST", "PATCH", "GET", "DELETE"])
@validateToken.validateToken
def albums(currentUser):
    if request.method == "POST":
        checkName = "SELECT * FROM albums WHERE albumName = %s"
        values = (request.json["albumName"],)
        cursor.execute(checkName, values)
        
        if cursor.fetchone() is not None:
            return {"result": "Album already exists"}
        
        fields = ["albumName"]
        values = [currentUser[4], request.json["albumName"]]
        for item in request.json:
            if item == "albumDescription":
                fields += [item]
                values += [request.json[item]]
                continue;
            elif item == "albumCamera":
                fields += [item]
                values += [request.json[item]]
                continue;
            elif item == "albumFormat":
                fields += [item]
                values += [request.json[item]]
                continue;
            elif item == "albumFilm":
                fields += [item]
                values += [request.json[item]]
                continue;
            elif item not in fields:
                return {
                    "message": "Invalid field provided.",
                    "data": None,
                    "error": "Incorrect format"
                }
        createAlbum = "INSERT INTO albums (userID, "
        valuesAdded = " VALUES (%s, "
        for field in fields:
            if fields.index(field) < len(fields) - 1:
                createAlbum += field + ", "
                valuesAdded += "%s, "
            else:
                createAlbum += field + ")"
                valuesAdded += "%s)"
        createAlbum += valuesAdded
        print(createAlbum)

        cursor.execute(createAlbum, values)
        connection.commit()

        return {"string": "Created album."}

    elif request.method == "PATCH":
        return {"string": "Updating album."}

    elif request.method == "GET":
        return {"string": "Getting albums."}

    elif request.method == "DELETE":
        return {"string": "Deleting album."}
