from main import app, db_connection, auth_required
from flask import request, jsonify
import re

# TODO: PSB-11

# TODO: PSB-14
@app.route("/api/users", methods=['GET'])
def search_users():
    #url parameters
    search_string = request.args.get("search")

    #regex is going to get many cases such as 
    #1 just a string
    #2 string w/space
    #3 string space string
    #4 string space string#
    #5 string space string#[1-9][0-9]*
    full_match = re.fullmatch("([a-zA-Z]+)(\s([a-zA-Z]+(#([1-9][0-9]*)?)?)?)?", search_string)

    if not full_match:
        return "error",400

    #split our search string with spaces and #
    split = re.split(r'\s|#', search_string)
    #remove all empty strings resulting from previous split
    split = [s for s in split if s]

#assign variables given bounds
    if len(split) == 1: 
        firstName = split[0]

    if len(split) == 2:
        firstName = split[0]
        lastName = split[1]

    if len(split) == 3: 
        firstName = split[0]
        lastName = split[1]
        id = split[2]
#assign variables


    #if len(split) = 1 means we only have firstName
    if len(split) == 1: 

        #if we only have a firstName AND NO SPACE               (SUBSTRING MATCH FIRSTNAME)
        if ' ' not in search_string:

            #query to retrive all users where user input is beginning of firstNames
            FIRSTNAME_SUBSTR_QUERY = ("""
                SELECT * 
                FROM Users
                WHERE firstName LIKE %s
            """)

            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(FIRSTNAME_SUBSTR_QUERY, (firstName.title()+'%',)) #.title() sets string format to first letter capalized and rest lowercase
                    users_firstName_substr = cursor.fetchall()
            
            #generate response
            response = []
            for x in users_firstName_substr:
                new_object = {}
                new_object['userId'] = x[0]
                new_object['firstName'] = x[1]
                new_object['lastName'] = x[2]
                #x[3] no need to send email
                #x[4] ne need to send hometown
                #x[5] no need to send creationDate
                #x[6] no need to send hashedpassword
                #x[7] no need to send gender
                #x[8] no need to send contribution score 
                response.append(new_object)
            return response

        #if we only have a firstName AND SPACE                  (EXACT MATCH FIRSTNAME)
        if ' ' in search_string:

            EXACT_MATCH_FIRSTNAME = """
                SELECT *
                FROM Users
                WHERE firstName LIKE %s;
                """

            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(EXACT_MATCH_FIRSTNAME, (firstName.title(),)) #.title() sets string format to first letter capalized and rest lowercase
                    exact_first = cursor.fetchall()
            
            #generate response
            response = []
            for x in exact_first:
                new_object = {}
                new_object['userId'] = x[0]
                new_object['firstName'] = x[1]
                new_object['lastName'] = x[2]
                response.append(new_object)
            return response


    if len(split) == 2:

        #if we only have first AND lastName AND NO HASHTAG      (EXACT MATCH FIRSTNAME / SUBSTR MATCH LASTNAME)
        if '#' not in search_string:

            EXACT_FIRST_SUBSTR_LAST = ("""
                SELECT *
                FROM Users
                WHERE firstName = %s AND lastName LIKE %s;
            """)

            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(EXACT_FIRST_SUBSTR_LAST, (firstName.title(), lastName.title()+'%'))
                    exact_first_substr_last = cursor.fetchall()
            
            #generate response
            response = []
            for x in exact_first_substr_last:
                new_object = {}
                new_object['userId'] = x[0]
                new_object['firstName'] = x[1]
                new_object['lastName'] = x[2]
                response.append(new_object)
            return response
        
        #if we only have first AND lastName AND HAVE HASHTAG    (EXACT MATCH FIRSTNAME / EXACT MATCH LASTNAME)
        if '#' in search_string:

            EXACT_FIRST_EXACT_LAST = ("""
                SELECT *
                FROM Users
                WHERE firstName = %s AND lastName = %s;
            """)

            with db_connection:
                with db_connection.cursor() as cursor:
                    cursor.execute(EXACT_FIRST_EXACT_LAST, (firstName.title(), lastName.title()))
                    exact_first_exact_last = cursor.fetchall()
            
            #generate response
            response = []
            for x in exact_first_exact_last:
                new_object = {}
                new_object['userId'] = x[0]
                new_object['firstName'] = x[1]
                new_object['lastName'] = x[2]
                response.append(new_object)

            return response

#   this response means there are 3 vars                                   (EXACT MATCH FIRSTNAME / EXACT MATCH LASTNAME / SUBSTR MATCH USERID)

    EXACT_FIRST_EXACT_LAST_SUBSTR_ID = ("""
        SELECT *
        FROM Users
        WHERE firstName = %s AND lastName = %s AND CAST(userId AS TEXT) LIKE %s;
    """)

    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(EXACT_FIRST_EXACT_LAST_SUBSTR_ID, (firstName.title(), lastName.title(), id+'%'))
            exact_first_exact_last_substr_id = cursor.fetchall()
    
    #generate response
    response = []
    for x in exact_first_exact_last_substr_id:
        new_object = {}
        new_object['userId'] = x[0]
        new_object['firstName'] = x[1]
        new_object['lastName'] = x[2]
        response.append(new_object)

    return response
    
        




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
