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
        fields = []
        values = []
        for item in request.json:
            if item == "updateName":
                fields += ["albumName"]
                values += [request.json[item]]
                continue;
            elif item == "updateDescription":
                fields += ["albumDescription"]
                values += [request.json[item]]
                continue;
            elif item == "updateCamera":
                fields += ["albumCamera"]
                values += [request.json[item]]
                continue;
            elif item == "updateFormat":
                fields += ["albumFormat"]
                values += [request.json[item]]
                continue;
            elif item == "updateFilm":
                fields += ["albumFilm"]
                values += [request.json[item]]
                continue;
            elif item != "albumName":
                return {
                    "message": "Invalid field provided.",
                    "data": None,
                    "error": "Incorrect format"
                }

        updateAlbum = "UPDATE albums SET "

        for field in fields:
            if fields.index(field) < len(fields) - 1:
                updateAlbum += field + " = %s, "
            else:
                updateAlbum += field + " = %s WHERE userID = %s AND albumName = %s;"
        values += [currentUser[4], request.json["albumName"]]

        cursor.execute(updateAlbum, values)
        connection.commit()

        return {"string": "Updating album."}

    elif request.method == "GET":
        getAlbums = "SELECT * FROM albums WHERE userID = %s"
        values = (currentUser[4],)
        cursor.execute(getAlbums, values)
        albums = cursor.fetchall()
        return {
                "message": "Retrieved albums.",
                "albums": albums
            }

    elif request.method == "DELETE":
        checkAlbum = "SELECT * FROM albums WHERE albumName = %s AND userID = %s"
        values = (request.json["albumName"], currentUser[4])

        cursor.execute(checkAlbum, values)
        if cursor.fetchone() is None:
            return {"result": "Album does not exist"}

        deleteAlbum = "DELETE FROM albums WHERE albumName = %s AND userID = %s"
        cursor.execute(deleteAlbum, values)
        connection.commit()

        return {"string": "Deleted album."}
