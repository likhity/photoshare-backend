from main import app, db_connection, auth_required
from flask import request, jsonify

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

# TODO: PSB-20