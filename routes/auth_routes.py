from main import app, request, db_connection
import time

@app.route("/api/time")
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
  return { "id": userId, "message": f"User {firstName} {lastName} created." }, 201
