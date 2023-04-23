from main import app, db_connection, auth_required, db_lock
from flask import request

# TODO: PSB-10
@app.route("/api/popular-tags", methods=['GET'])
def most_popular_tags():
    # query for most popular tags
    MOST_POPULAR_TAGS_QUERY = (
        """
        SELECT Tag, COUNT(*) AS numPosts
        FROM Tags 
        GROUP BY Tag 
        ORDER BY COUNT(*) DESC LIMIT 50;
        """)
    
    db_lock.acquire()
    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve most popular tags
            cursor.execute(MOST_POPULAR_TAGS_QUERY)
            most_popular_tags_list = cursor.fetchall()
    db_lock.release()

    response = []

    for x in most_popular_tags_list:
        new_object = {}
        new_object['tag'] = x[0]
        new_object['numPosts'] = x[1]
        response.append(new_object)

    return response
# TODO: PSB-11
@app.route("/api/top-10-users", methods=["GET"])
def top_10_users():
    # query for top 10 users
    TOP_10_USERS_QUERY = (
        """
        SELECT userId, firstName, lastName, contribution 
        FROM Users 
        ORDER BY contribution 
        DESC LIMIT 10;
        """)
    
    db_lock.acquire()
    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve top 10 users
            cursor.execute(TOP_10_USERS_QUERY)
            top_10_users_list = cursor.fetchall()
    db_lock.release()

    response = []

    for x in top_10_users_list:
        new_object = {}
        new_object['userId'] = x[0]
        new_object['firstName'] = x[1]
        new_object['lastName'] = x[2]
        new_object['contributions'] = x[3]
        response.append(new_object)

    return response
    
# TODO: PSB-12
@app.route("/api/photo-recommendations", methods=['GET'])
@auth_required
def photo_recommendations(decoded_token):
    # query for photo recommendations
    ownerID = decoded_token["user"]
    PHOTO_RECOMMENDATIONS_QUERY = (
        """
        SELECT *
        FROM Photos
        WHERE PhotoId IN (SELECT photoID FROM
        (SELECT PhotoId, COUNT(*) AS numTags 
        FROM Tags 
        WHERE Tag IN (SELECT Tag FROM Tags WHERE PhotoId IN (SELECT PhotoId FROM Photos WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s))) GROUP BY PhotoId ORDER BY numTags DESC LIMIT 5) AS result)
        """)
    
    db_lock.acquire()
    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve photo recommendations
            cursor.execute(PHOTO_RECOMMENDATIONS_QUERY, (decoded_token["user"],))
            photo_recommendations_list = cursor.fetchall()
    db_lock.release()

    response = []

    for x in photo_recommendations_list:
        new_object = {}
        new_object['photoId'] = x[0]
        new_object['caption'] = x[1]
        new_object['albumId'] = x[2]
        new_object['filepath'] = x[3]
        new_object['dateOfCreation'] = x[4]
        response.append(new_object)

    return response
