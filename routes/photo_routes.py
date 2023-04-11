from main import app, db_connection, auth_required
from flask import request, jsonify
# from werkzeug.utils import secure_filename

# TODO: PSB-6
# @app.route("/api/upload", methods=["POST"])
# def fileUpload():
#     file = request.files['file'] 
#     filename = secure_filename(file.filename)

# TODO: PSB-5
@app.post("/api/like-photo")
@auth_required
def like_photo(decoded_token):
    photoId = request.args.get("photoId")
    userId = decoded_token["user"]
    
    INSERT_LIKE_QUERY = """INSERT INTO Likes (userId, PhotoId) 
    VALUES (%s, %s)
    """

    with db_connection:
        with db_connection.cursor() as cursor:
            # insert the new user with the HASHED password
            cursor.execute(INSERT_LIKE_QUERY, (userId, photoId,))
    
    return jsonify({ "message": "Succeeded." })



# TODO: PSB-23

# TODO: PSB-7

# TODO: PSB-13
@app.route("/api/photo")
def get_photoInfo():
    SELECT_PHOTO_QUERY = "SELECT * FROM Photos WHERE PhotoId = %s;"
    photo = request.args.get("photoId")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_PHOTO_QUERY, (photo,))
            result = cursor.fetchone()
    
    response = []
    new_element = {}
    new_element["photoId"] = result[0]
    new_element["albumName"] = result[1]
    new_element["albumId"] = result[2]
    new_element["URL"] = result[3]
    response.append(new_element)

    return response
    

# TODO: PSB-21