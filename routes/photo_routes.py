from main import app, db_connection, auth_required
from flask import request, jsonify
import boto3
import uuid

# TODO: PSB-6
@app.route("/api/upload", methods=["POST"])
@auth_required
def photo_upload(decoded_token):
    userId = decoded_token['user']
    
    caption = request.args.get('caption')
    albumName = request.args.get('albumName')
    
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    
    def file_allowed(filename: str):
        ALLOWED_EXTENSIONS = { 'png', 'jpg', 'gif' }
        return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS
    
    if not file_allowed(filename):
        return "Invalid file.", 400
    
    new_filename = uuid.uuid4().hex + '.' + filename.rsplit('.')[1].lower()
    s3 = boto3.resource("s3")
    bucket_name = "photoshare-app"
    s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename, ExtraArgs={ 'ACL': 'public-read' })
    
    INSERT_PHOTO = (
        """
        INSERT INTO Photos (albumId, caption, filePath)
        VALUES ((SELECT albumId FROM Albums WHERE ownerId = %s AND AlbumName = %s), %s, %s);
        """
    )
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(INSERT_PHOTO, (userId, albumName, caption, new_filename))
            
    url = "https://%s.s3.us-west-1.amazonaws.com/%s" % (bucket_name, new_filename)
    
    return { "message": "Uploaded.", "url": url }, 201

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
    # print(result)
    return jsonify(result)

# TODO: PSB-21