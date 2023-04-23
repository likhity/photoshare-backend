from main import app, db_connection, db_lock, JWT_SECRET_KEY, auth_required
import time
import jwt
from datetime import datetime, timedelta
from flask import request, jsonify
import bcrypt

@app.route("/api/time")
@auth_required
def get_current_time():
    return { "time": time.time() }

@app.post('/api/register')
def create_user():
    data = request.get_json()
    firstName = data["firstName"]
    lastName = data["lastName"]
    email = data["email"]
    gender = data["gender"]
    homeTown = data["homeTown"]
    dateOfBirth = data["dateOfBirth"]
    password = data["password"]
    
    # Every function in the bcrypt library only
    # takes in and returns bytes, never strings.
    # So we have to convert the strings to bytes to use bcrypt.
    pw_bytes = bytes(password, 'utf-8')
    
    # hash the password
    hash_bytes = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    # bcrypt.hashpw() returns the hashed pw in bytes,
    # so we must turn the bytes back into a string 
    # that we can insert into database
    hashed_password = hash_bytes.decode()
    
    SELECT_USER_QUERY = (
        """
            SELECT email FROM Users WHERE email = %s;
        """
    )
    
    INSERT_USER_QUERY = (
        """
            INSERT INTO Users (firstName, lastName, email, homeTown, dateOfBirth, password, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING userId;
        """
    )
    lockedRelased = False
    db_lock.acquire()
    try:
        with db_connection:
            with db_connection.cursor() as cursor:
                # check if the email already exists
                cursor.execute(SELECT_USER_QUERY, (email,))
                existing_user = cursor.fetchone()
                
                # if the email already exists, return an error response
                if existing_user is not None:
                    db_lock.release()
                    lockedRelased = True
                    return jsonify({"message": "Email already exists."}), 409
                
                # insert the new user with the HASHED password
                cursor.execute(INSERT_USER_QUERY, (firstName, lastName, email, homeTown, dateOfBirth, hashed_password, gender))
                userId = cursor.fetchone()[0]
    finally:
        if lockedRelased is False:
            db_lock.release()
    
    # A JWT is valid for 8 hours since first creation
    jwtMaxAge = 8 * 60 * 60 * 1000
    
    token = jwt.encode({
            'user': userId,
            'expiration': str(datetime.utcnow() + timedelta(hours=8))
        }, JWT_SECRET_KEY, algorithm="HS256")
    
    response = jsonify({ "id": userId, "message": "User created." })
    response.set_cookie(key="jwt", value=token, max_age=jwtMaxAge, httponly=True)
    return response, 201


@app.route("/api/login", methods=['POST'])
def login():
    form_data = request.get_json()
    email = form_data['email']
    password = form_data['password']
    
    SELECT_USER_QUERY = "SELECT userId, email, password FROM Users WHERE email = %s;"
    db_lock.acquire()
    with db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(SELECT_USER_QUERY, (email,))
            # result will be an array like so: [userId, email, password]
            result = cursor.fetchone()
    db_lock.release()
            
    if result and bcrypt.checkpw(bytes(password, 'utf-8'), bytes(result[2], 'utf-8')):
        # A JWT is valid for 8 hours since first creation
        jwtMaxAge = 8 * 60 * 60
        
        token = jwt.encode({
            'user': result[0],
            'expiration': str(datetime.utcnow() + timedelta(hours=8))
        }, JWT_SECRET_KEY, algorithm="HS256")
        
        response = jsonify({ "id": result[0] })
        response.set_cookie(key="jwt", value=token, max_age=jwtMaxAge, httponly=True)
        return response
    else:
        return { "error": "Authentication failed." }, 401

@app.route("/api/logout")
def logout():
    response = jsonify({ "message": "Logged out." })
    response.set_cookie(key="jwt", value="", max_age=1)
    return response