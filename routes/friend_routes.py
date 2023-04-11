from main import app, db_connection, auth_required

from flask import request, jsonify
import datetime #needed for friendship dates

# TODO: PSB-16
@app.route("/api/suggested-friends", methods=['GET'])
@auth_required
def suggested_friends(decoded_token):

    # query for suggested friends
    SUGGESTED_FRIENDS_QUERY = (
        """
        SELECT result.userId, firstName, lastName FROM Users
        JOIN
        (SELECT friendId as userId, COUNT(*) AS numFriends FROM Friends WHERE userId IN (SELECT friendId FROM Friends WHERE userId = 5) GROUP BY friendId ORDER BY numFriends DESC) AS result
        ON Users.userId = result.userid
        ORDER BY result.numFriends DESC;
        """)
    
    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve suggested friends (based on ids)
            cursor.execute(SUGGESTED_FRIENDS_QUERY, (decoded_token["user"],))
            suggested_friends_list = cursor.fetchall()


    response = []

    for x in suggested_friends_list:
        new_object = {}
        new_object['userId'] = x[0]
        new_object['firstName'] = x[1]
        new_object['lastName'] = x[2]
        response.append(new_object)

    return response
    
# TODO: PSB-17
# expect /api/add-friend?friendId=12
@app.route("/api/add-friend", methods=['POST'])
@auth_required
def add_friend(decoded_token):
    # query for creating friend_ship
    CREATE_FRIENDSHIP_QUERY = (
        """
            INSERT INTO Friends (userId, friendId, dateOfFriendship)
            VALUES (%s, %s, %s);
        """)
    
    # get userID from token
    userID = decoded_token["user"]
    
    # get id of the person being added
    friendID = request.args.get("friendId")

    # get todays date
    current_day = datetime.date.today()                                 #2019-07-25

    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve suggested friends (based on ids)
            cursor.execute(CREATE_FRIENDSHIP_QUERY, (userID, friendID, current_day))

    return  f"{userID} added Friend {friendID} was added on {current_day}", 201

# TODO: PSB-19
# /api/friends?userId=58
@app.route("/api/friends", methods=['GET'])
# no authentication needed since we can see everyones friends
def friends():

    # query for getting all user friends
    GET_ALL_FRIENDS = (
        """
            SELECT userId, firstName, lastName 
            FROM Users 
            WHERE userId IN (SELECT friendId FROM Friends WHERE userId = %s);
        """)
    
    # get userID from url
    userID = request.args.get("userId")
    
    # execute query and retrieve all userIds friends
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve all friends
            cursor.execute(GET_ALL_FRIENDS, (userID))
            all_friends = cursor.fetchall()


    response = []
    # we have retrived all info but only return userId, FName, LName
    for x in all_friends:
        new_object = {}
        new_object['userId'] = x[0]
        new_object['firstName'] = x[1]
        new_object['lastName'] = x[2]
        response.append(new_object)
    return response, 200

