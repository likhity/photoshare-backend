from main import app, db_connection, auth_required
from flask import request
import datetime #needed for friendship dates

# TODO: PSB-16

# TODO: PSB-17
#expect /api/add-friend?friendId=12
@app.route("/api/add-friend", methods=['POST'])
@auth_required
def add_friend(decoded_token):

    # query for creating friend_ship
    CREATE_FRIENDSHIP_QUERY = (
        """
            INSERT INTO Friends (userId, friendId, dateOfFriendship)
            VALUES (%s, %s, 'yyyy-mm-dd');
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
    return f"Friend { userID} added {friendID} was addedon {str(current_day)}"
# TODO: PSB-19