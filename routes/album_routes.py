from main import app, db_connection, auth_required
from flask import request, jsonify
from datetime import date
import boto3

# TODO: PSB-8
@app.get("/api/album")
def get_album():
    SELECT_ALBUM_QUERY = "SELECT albumId, AlbumName, dateOfCreation FROM Albums WHERE ownerId = %s AND AlbumName = %s"
    user = request.args.get("userId")
    name = request.args.get("albumName")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_ALBUM_QUERY, (user, name,))
            result = cursor.fetchone()
    new_element = {}
    new_element["albumId"] = result[0]
    new_element["albumName"] = result[1]
    new_element["dateOfCreation"] = result[2]

    return new_element

# TODO: PSB-9

@app.get("/api/albums")
def get_albums():
    SELECT_USER_QUERY = "SELECT albumId, AlbumName, dateOfCreation FROM Albums WHERE ownerId = %s"
    s = request.args.get("userId")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_USER_QUERY, (s,))
            db_result = cursor.fetchall() 
    
    response = []
    for x in db_result:
        new_element = {}
        new_element["albumId"] = x[0]
        new_element["albumName"] = x[1]
        new_element["dateOfCreation"] = x[2]
        response.append(new_element)

    return response

# TODO: PSB-18
@app.route("/api/create-album", methods=["POST"])
@auth_required
def create_album(decoded_token):
    name = request.args.get("name")
    ownerId = decoded_token["user"]
    dateOfCreation = str(date.today())

    INSERT_ALBUM_QUERY = """INSERT INTO Albums (AlbumName, ownerId, dateOfCreation) 
    VALUES (%s, %s, %s)
    RETURNING albumId;
    """

    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(INSERT_ALBUM_QUERY, (name, ownerId, dateOfCreation,))
            albumId = cursor.fetchone()[0]
    
    return jsonify({ "albumid": albumId, "message": "Album created." })

# TODO: PSB-20
@app.delete("/api/album")
@auth_required
def delete_album(decoded_token):
    userId = decoded_token['user']
    albumName = request.args.get("albumName")
    
    SELECT_PHOTO = (
        """
        SELECT filePath FROM Photos 
        WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s AND AlbumName = %s)
        AND filePath LIKE '%%photoshare-app%%';
        """
    )
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_PHOTO, (userId, albumName))
            photos_to_delete = cursor.fetchall()
    
    s3 = boto3.client("s3")
    bucket_name = "photoshare-app"
    
    for record in photos_to_delete:
        filename = record[0].split('/')[-1]
        s3.delete_object(
            Bucket=bucket_name,
            Key=filename
        )
    
    DELETE_ALBUM = (
        """
        DELETE FROM Albums WHERE ownerId = %s AND AlbumName = %s;
        """
    )
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(DELETE_ALBUM, (userId, albumName))
    
    return { "message": "Album deleted successfully." }