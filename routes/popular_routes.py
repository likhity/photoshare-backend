from main import app, db_connection, auth_required
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
    
    # execute query and retrieve all info related + return to frontend
    with db_connection:
        with db_connection.cursor() as cursor:
            # retrieve most popular tags
            cursor.execute(MOST_POPULAR_TAGS_QUERY)
            most_popular_tags_list = cursor.fetchall()

    response = []

    for x in most_popular_tags_list:
        new_object = {}
        new_object['tag'] = x[0]
        new_object['numPosts'] = x[1]
        response.append(new_object)

    return response
# TODO: PSB-11

# TODO: PSB-12