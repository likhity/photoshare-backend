from main import app, db_connection, auth_required
from flask import request, jsonify
# from werkzeug.utils import secure_filename

# TODO: PSB-6
# @app.route("/api/upload", methods=["POST"])
# def fileUpload():
#     file = request.files['file'] 
#     filename = secure_filename(file.filename)

# TODO: PSB-5

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
    # print(result)
    return jsonify(result)

# TODO: PSB-21