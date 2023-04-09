from main import app, db_connection, JWT_SECRET_KEY, auth_required
import time
import jwt
from datetime import datetime, timedelta
from flask import request, jsonify

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
  homeTown = data["homeTown"]
  dateOfBirth = data["dateOfBirth"]
  password = data["password"]
  
  INSERT_USER_QUERY = (
    """
      INSERT INTO Users (firstName, lastName, email, homeTown, dateOfBirth, password)
      VALUES (%s, %s, %s, %s, %s, %s)
      RETURNING userId;
    """
  )
  with db_connection:
    with db_connection.cursor() as cursor:
      cursor.execute(INSERT_USER_QUERY, (firstName, lastName, email, homeTown, dateOfBirth, password))
      userId = cursor.fetchone()[0]
  
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
  with db_connection:
    with db_connection.cursor() as cursor:
      cursor.execute(SELECT_USER_QUERY, (email,))
      result = cursor.fetchone()
      
  if result and result[2] == password:
    # A JWT is valid for 8 hours since first creation
    jwtMaxAge = 8 * 60 * 60 * 1000
    
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