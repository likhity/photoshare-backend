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
            FROM Photos 
            WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s AND albumId = %s);
            """
        
        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags
                cursor.execute(USERID_AND_ALBUMNAME_QUERY, (userId, albumName))
                all_photos_given_albumName_and_userId = cursor.fetchall()
        
        return all_photos_given_albumName_and_userId, 200
#ALBUM NAME AND USERID

    #default (ERR)
    return "something went wrong bozo", 400



        
        







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
    new_element["caption"] = result[1]
    new_element["albumId"] = result[2]
    new_element["URL"] = result[3]
    response.append(new_element)

    return response
    

# TODO: PSB-21