from main import app, db_connection, auth_required
from flask import request, jsonify

# TODO: PSB-11

# TODO: PSB-14

# TODO: PSB-15
@app.route("/api/user-info")
def get_user_info():
    SELECT_USER_QUERY = "SELECT * FROM Users WHERE userId = %s"
    user = request.args.get("userId")
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_USER_QUERY, (user,))
            result = cursor.fetchone()

    new_element = {}
    new_element["userId"] = result[0]
    new_element["firstName"] = result[1]
    new_element["lastName"] = result[2]
    new_element["email"] = result[3]
    new_element["hometown"] = result[4]
    new_element["dateOfBirth"] = result[5]
    new_element["gender"] = result[7]
    new_element["contribution"] = result[8]
    return new_element
