from app import app, request, connection

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
  with connection:
    with connection.cursor() as cursor:
      cursor.execute(INSERT_USER_QUERY, (firstName, lastName, email, homeTown, dateOfBirth, password))
      userId = cursor.fetchone()[0]
  return { "id": userId, "message": f"User {firstName} {lastName} created." }, 201
