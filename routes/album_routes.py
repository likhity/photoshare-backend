from main import app, db_connection, auth_required
from flask import request, jsonify
from datetime import date

# TODO: PSB-8
@app.get("/api/album")
def get_album():
    SELECT_ALBUM_QUERY = "SELECT * FROM Albums WHERE ownerId = %s AND AlbumName = %s"
    user = request.args.get("userId")
    name = request.args.get("albumName")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_ALBUM_QUERY, (user, name,))
            result = cursor.fetchone()
    return jsonify(result)

# TODO: PSB-9

@app.get("/api/albums")
def get_albums():
    SELECT_USER_QUERY = "SELECT * FROM Albums WHERE ownerId = %s"
    s = request.args.get("userId")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_USER_QUERY, (s,))
            result = cursor.fetchall() 
    return result
# TODO: PSB-18
@app.route("/api/create-album")
@auth_required
def create_album(decoded_token):
    name = request.args.get("name")
    ownerId = decoded_token["user"]
    dateOfCreation = str(date.today())

    INSERT_ALBUM_QUERY = """INSERT INTO Albums (AlbumName, ownerId, dateOfCreation) 
    VALUES (%s, %s, %s);
    RETURNING albumId;
    """

    with db_connection:
        with db_connection.cursor() as cursor:
            # insert the new user with the HASHED password
            cursor.execute(INSERT_ALBUM_QUERY, (AlbumName, ownerId, dateOfCreation,))
            albumId = cursor.fetchone()[0]
    
    return jsonify({ "albumid": albumId, "message": "Album created." })

# TODO: PSB-20