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
    return jsonify(result)
