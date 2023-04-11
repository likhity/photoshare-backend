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
        
        return all_photos, 200
    
#ALL PHOTOS




#ONLY USERID
    userId = request.args.get('userId')

    #if we have a userId param. and only 1 var. in params
    if userId is not None and len(request.args) == 1:

        #query for all photos given userId
        ALL_PHOTO_GIVEN_ID_QUERY = """
            SELECT * 
            FROM Photos 
            WHERE ownerId = %s;
            """  
        
        #execute query w/userId and return
        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve ALL photos given userId
                cursor.execute(ALL_PHOTO_GIVEN_ID_QUERY, userId)
                all_photos_given_Id = cursor.fetchall()
        
        return all_photos_given_Id, 200
#ONLY USERID




#TAG(S) && NO USERID
    all_tags = request.args.get("tags")
    #userId = request.args.get("userId") done before last function (above)
    #if I have 1<=tags and no userId
    if all_tags and userId is None:

        # we have at least 1 tag so we make base query
        TAG_QUERY = """
                SELECT * 
                FROM Photos 
                WHERE PhotoId IN (SELECT PhotoId FROM Tags WHERE Tag = %s"""
        
        # get all tags into tags_array
        tags_array = all_tags.split(",")

        # add "OR Tag = %s" for each other additional tag
        for x in len(tags_array) - 1:
            TAG_QUERY = TAG_QUERY + " OR Tag = %s"  

        TAG_QUERY += ");"                   #add the ");"" for the query 

        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags
                cursor.execute(TAG_QUERY, tags_array)
                all_photos_given_tags = cursor.fetchall()
        
        return all_photos_given_tags, 200
#TAG(S) && NO USERID






#TAGS && USERID
    #if we have tags and a userId
    if all_tags and userId is not None:
        TAG_PLUS_USERID_QUERY = """
            SELECT * 
            FROM Photos 
            WHERE ownerId = %s AND PhotoId IN (SELECT PhotoId FROM Tags WHERE Tag = %s"""
        
        tags_array = all_tags.split(",")

        # add "OR Tag = %s" for each other additional tag
        for x in len(tags_array) - 1:
            TAG_PLUS_USERID_QUERY = TAG_PLUS_USERID_QUERY + " OR Tag = %s"  

        TAG_PLUS_USERID_QUERY += ");"                   #add the ");"" for the query 

        with db_connection:
            with db_connection.cursor() as cursor:
                # retrieve all photos with given tags
                cursor.execute(TAG_PLUS_USERID_QUERY, (userId, tags_array))
                all_photos_given_tags_and_userId = cursor.fetchall()
        
        return all_photos_given_tags_and_userId, 200
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