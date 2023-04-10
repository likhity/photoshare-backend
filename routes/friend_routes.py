from main import app, db_connection, auth_required
from flask import request

# TODO: PSB-16

# TODO: PSB-17

# TODO: PSB-19
# /api/friends?userId=58
@app.route("/api/my-friends", methods=['GET'])
@auth_required
def my_friends(decoded_token):

    # query for getting all user friends
    GET_MY_FRIENDS = (
        """
            SELECT * 
            FROM Users 
            WHERE userId IN (SELECT friendId FROM Friends WHERE userId = %s);
        """)
    
    # get userID from token
    userID = decoded_token["user"]
    
    # execute query and retrieve all friends
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve all friends
            cursor.execute(GET_MY_FRIENDS, (userID))
            all_my_friends = cursor.fetchall()
    return all_my_friends, 201