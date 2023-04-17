from main import app, db_connection, auth_required
from flask import request, jsonify
import boto3
import uuid
import datetime

# TODO: PSB-6
@app.route("/api/upload", methods=["POST"])
@auth_required
def photo_upload(decoded_token):
    userId = decoded_token['user']
    
    caption = request.args.get('caption')
    albumName = request.args.get('albumName')
    tags = request.args.get('tags')
    
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
        INSERT INTO Photos (albumId, caption, filePath, dateOfCreation)
        VALUES ((SELECT albumId FROM Albums WHERE ownerId = %s AND AlbumName = %s), %s, %s, %s)
        RETURNING photoId, caption, albumId, filePath, dateOfCreation;
        """
    )
    
    UPDATE_CONTRIBUTION = (
        "UPDATE Users SET contribution = contribution + 1 WHERE userId = %s"
    )
    
    url = "https://%s.s3.us-west-1.amazonaws.com/%s" % (bucket_name, new_filename)
    current_day = datetime.date.today()
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(INSERT_PHOTO, (userId, albumName, caption, url, current_day))
            result = cursor.fetchone()
            # update the user's contribution score
            cursor.execute(UPDATE_CONTRIBUTION, (userId,))
    
    if tags:
        tags = tags.split(',')
        INSERT_TAG = (
            """
            INSERT INTO Tags (Tag, PhotoId)
            VALUES (%s, %s);
            """
        )
        for tag in tags:
            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(INSERT_TAG, (tag, result[0]))
    
    return { 
            "photoId": result[0], 
            "caption": result[1], 
            "albumId": result[2], 
            "url": result[3],
            "dateOfCreation": result[4]
           }, 201

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
@app.route("/api/add-comment", methods=['POST'])
@auth_required
def add_comment(decoded_token):
    data = request.get_json()
    photoId = data["photoId"]
    userId = decoded_token["user"]
    comment = data["comment"]
    current_day = datetime.date.today()  
    INSERT_COMMENT_QUERY = """INSERT INTO Comments (CommentText, commenterId, PhotoId, dateOfCreation) VALUES (%s, %s, %s, %s);
    """
    UPDATE_CONTRIBUTION = """UPDATE Users SET contribution = contribution + 1 WHERE userId = %s;
    """

    with db_connection:
        with db_connection.cursor() as cursor:
            # insert the new user with the HASHED password
            cursor.execute(INSERT_COMMENT_QUERY, (comment, userId, photoId, current_day,))
            cursor.execute(UPDATE_CONTRIBUTION, (userId,))
    
    return jsonify({ "message": "Succeeded." })
# TODO: PSB-7

@app.route("/api/photos", methods=['GET'])
# no need for authentication
def get_photos():

#ALL PHOTOS

    #if we have no params.
    if not request.args:

        # all photos query 
        ALL_PHOTO_QUERIES = """
            SELECT * 
            FROM Photos 
            ORDER BY dateOfCreation DESC;
            """
        
        # execute query and return 
        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve ALL photos
                cursor.execute(ALL_PHOTO_QUERIES)
                all_photos = cursor.fetchall()
        
        response = []

        for x in  all_photos:

            new_object = {}
            new_object['photoId'] = x[0]
            new_object['caption'] = x[1]
            new_object['albumId'] = x[2]
            new_object['filepath'] = x[3]
            new_object['dateOfCreation'] = x[4]
            response.append(new_object)


        return response, 200
    
#ALL PHOTOS




#ONLY USERID
    userId = request.args.get('userId')

    #if we have a userId param. and only 1 var. in params
    if userId is not None and len(request.args) == 1:

        #query for all photos given userId
        #query needs to join album and photos and get owner id from album
        ALL_PHOTO_GIVEN_ID_QUERY = """
            SELECT * 
            FROM Photos 
            WHERE albumId IN 
                (SELECT albumId 
                 FROM Albums 
                 WHERE ownerId = %s);
            """  
        
        #execute query w/userId and return
        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve ALL photos given userId
                cursor.execute(ALL_PHOTO_GIVEN_ID_QUERY, (userId,))
                all_photos_given_Id = cursor.fetchall()

        
        response = []

        for x in  all_photos_given_Id:

            new_object = {}
            new_object['photoid'] = x[0]
            new_object['caption'] = x[1]
            new_object['albumId'] = x[2]
            new_object['filepath'] = x[3]
            new_object['dateOfCreation'] = x[4]
            response.append(new_object)
        
        return response, 200
#ONLY USERID




#TAG(S) && NO USERID
    all_tags = request.args.get("tags")
    #userId = request.args.get("userId") done before last function (above)
    #if I have 1<=tags and no userId
    if all_tags and userId is None:

        # we have at least 1 tag so we make base query
        TAG_QUERY = (
            """
            SELECT DISTINCT Photos.*, COUNT(Tags.Tag) as MatchedTags
            FROM Photos
            JOIN Tags ON Tags.PhotoId = Photos.photoId
            WHERE Tags.Tag = ANY(%s)
            GROUP BY Photos.photoId
            ORDER BY MatchedTags DESC;
            """)
        
        # get all tags into tags_array
        tags_array = all_tags.split(",")

        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags
                cursor.execute(TAG_QUERY, (tags_array,))
                all_photos_given_tags = cursor.fetchall()

        response = []

        for x in  all_photos_given_tags:

            new_object = {}
            new_object['photoid'] = x[0]
            new_object['caption'] = x[1]
            new_object['albumId'] = x[2]
            new_object['filepath'] = x[3]
            new_object['dateOfCreation'] = x[4]
            response.append(new_object)
        
        return response, 200
#TAG(S) && NO USERID






#TAGS && USERID
    #if we have tags and a userId           #note: userId can be currentUser or another user's 
    if all_tags and userId is not None:
        TAG_PLUS_USERID_QUERY = (

            # query returns photos that have the most matched tags on top (DESC) and match given userId
            """
            SELECT Photos.*, COUNT(Tags.Tag) as MatchedTags
            FROM Photos
            JOIN Albums ON Albums.albumId = Photos.albumId
            JOIN Tags ON Tags.PhotoId = Photos.photoId
            WHERE Albums.ownerId = %s
            AND Tags.Tag = ANY(%s)
            GROUP BY Photos.photoId
            ORDER BY MatchedTags DESC;""")
        
        # get array of tags to search
        tags_array = all_tags.split(",")

        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags and userId
                cursor.execute(TAG_PLUS_USERID_QUERY, (userId, tags_array))
                all_photos_given_tags_and_userId = cursor.fetchall()
        
        #create appropriate response
        response = []
        for x in  all_photos_given_tags_and_userId:
            new_object = {}
            new_object['photoid'] = x[0]
            new_object['caption'] = x[1]
            new_object['albumId'] = x[2]
            new_object['filepath'] = x[3]
            new_object['dateOfCreation'] = x[4]
            response.append(new_object)
        
        return response, 200
#TAGS && USERID



#ALBUM NAME AND USERID
    albumName = request.args.get("albumName")

    # if we have a userId & albumName
    if userId is not None and albumName is not None:
        USERID_AND_ALBUMNAME_QUERY = """
        SELECT *
        FROM photos p
        INNER JOIN albums a ON p.albumid = a.albumid
        INNER JOIN users u ON a.ownerid = u.userid
        WHERE a.albumname = %s AND u.userid = %s;"""

        
        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags
                cursor.execute(USERID_AND_ALBUMNAME_QUERY, (albumName, userId))
                all_photos_given_albumName_and_userId = cursor.fetchall()
        

        #create appropriate response
        response = []
        for x in  all_photos_given_albumName_and_userId:
            new_object = {}
            new_object['photoid'] = x[0]
            new_object['caption'] = x[1]
            new_object['albumId'] = x[2]
            new_object['filepath'] = x[3]
            new_object['dateOfCreation'] = x[4]
            response.append(new_object)
        
        return response, 200
#ALBUM NAME AND USERID

    #default (ERR)
    return "something went wrong bozo", 400



        
        







# TODO: PSB-13
@app.route("/api/photo")
def get_photoInfo():
    SELECT_PHOTO_QUERY = (
        """
        SELECT 
            Photos.PhotoId,
            Photos.caption,
            Photos.albumId,
            Photos.filePath,
            Users.firstName,
            Users.lastName,
            Users.userId AS ownerId,
            COUNT(Likes.PhotoId) AS numLikes,
            ARRAY_AGG(DISTINCT(Tags.Tag)) AS tags
        FROM 
            Photos
            JOIN Albums ON Photos.albumId = Albums.albumId
            JOIN Users ON Albums.ownerId = Users.userId
            LEFT JOIN Likes ON Photos.PhotoId = Likes.PhotoId
            LEFT JOIN Tags ON Photos.PhotoId = Tags.PhotoId
        WHERE 
            Photos.PhotoId = %s
        GROUP BY 
            Photos.PhotoId,
            Photos.caption,
            Photos.albumId,
            Photos.filePath,
            Users.firstName,
            Users.lastName,
            Users.userId;
        """
    )
    photoId = request.args.get("photoId")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_PHOTO_QUERY, (photoId,))
            result = cursor.fetchone()
    
    response = {}
    response["photoId"] = result[0]
    response["caption"] = result[1]
    response["albumId"] = result[2]
    response["url"] = result[3]
    response["firstName"] = result[4]
    response["lastName"] = result[5]
    response["ownerId"] = result[6]
    response["numLikes"] = result[7]
    response["tags"] = result[8]
    
    return response
    

# TODO: PSB-21
@app.delete("/api/photo")
@auth_required
def delete_photo(decoded_token):
    userId = decoded_token['user']
    photoId = request.args.get('photoId')
    
    SELECT_PHOTO = (
        """
        SELECT filePath FROM Photos 
        WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s) 
        AND photoId = %s;
        """
    )
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_PHOTO, (userId, photoId))
            result = cursor.fetchone()
    
    if not result:
        return { "message": f"Failed. You do not own the photo with id {photoId}." }, 400
    
    filename = result[0].split('/')[-1]
    
    s3 = boto3.client("s3")
    bucket_name = "photoshare-app"
    
    s3.delete_object(
        Bucket=bucket_name,
        Key=filename
    )
    
    DELETE_PHOTO = (
        """
        DELETE FROM Photos WHERE photoId = %s;
        UPDATE Users SET contribution = contribution - 1 WHERE userId = %s;
        """
    )
    
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(DELETE_PHOTO, (photoId, userId))
            
    return { "message": "Photo deleted successfully." }
    
# TODO: PSB-24
@app.get("/api/comments")
def get_comments():
    photoId = request.args.get("photoId")
    searchString = request.args.get("search")
    
    if searchString:
        SELECT_COMMENTS_SEARCH = (
            """
            SELECT Comments.*, Users.firstName, Users.lastName
            FROM Comments JOIN Users ON Comments.commenterId = Users.userId
            WHERE photoId = %s AND CommentText LIKE %s
            """
        )
        with db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute(SELECT_COMMENTS_SEARCH, (photoId, f"%{searchString}%"))
                db_result = cursor.fetchall() 
    else:
        SELECT_COMMENTS = (
            """
            SELECT Comments.*, Users.firstName, Users.lastName
            FROM Comments JOIN Users ON Comments.commenterId = Users.userId
            WHERE photoId = %s
            """
        )
        with db_connection:
            with db_connection.cursor() as cursor:
                cursor.execute(SELECT_COMMENTS, (photoId,))
                db_result = cursor.fetchall()
    
    response = []
    for x in db_result:
        new_element = {}
        new_element["commentId"] = x[0]
        new_element["commentText"] = x[1]
        new_element["commenterId"] = x[2]
        new_element["photoId"] = x[3]
        new_element["dateOfCreation"] = x[4]
        new_element["commenterName"] = x[5] + " " + x[6]
        response.append(new_element)

    return response

