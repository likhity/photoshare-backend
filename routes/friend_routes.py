from main import app, db_connection, auth_required
from flask import request

# TODO: PSB-16
@app.route("/api/suggested-friends", methods=['GET'])
@auth_required
def suggested_friends(data):

    #need userId from app? or token
    print(data)
    SUGGESTED_FRIENDS_QUERY = (
        """
            SELECT friendId, COUNT(*) AS numFriends 
            FROM Friends 
            WHERE userId IN 
                (SELECT friendId FROM Friends WHERE userId = %s) 
                GROUP BY friendId ORDER BY numFriends DESC;
        """)

    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve suggested friends (based on ids)
            cursor.execute(SUGGESTED_FRIENDS_QUERY, ())
            userId = cursor.fetchone()[0]
    
# TODO: PSB-17

# TODO: PSB-19
# /api/friends?userId=58
@app.route("/api/friends", methods=['GET'])
# no authentication needed since we can see everyones friends
def friends():

    # query for getting all user friends
    GET_ALL_FRIENDS = (
        """
            SELECT * 
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
    return all_friends, 201