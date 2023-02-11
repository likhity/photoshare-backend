import os
import time
import psycopg2
from dotenv import load_dotenv
from flask import *

# load_dotenv() loads all environment 
# variables from .env file so we can
# easily access them using os.getenv()
load_dotenv()

app = Flask(__name__)
# get the DATABASE_URL environment variable that was stored in the .env file
db_url = os.getenv('DATABASE_URL')
# connect to database
connection = psycopg2.connect(db_url)

#### SQL QUERIES ####
CREATE_USERS_QUERY = (
  """
    CREATE TABLE IF NOT EXISTS Users (
      userId serial PRIMARY KEY,
      firstName VARCHAR(50) NOT NULL,
      lastName VARCHAR(50) NOT NULL,
      email VARCHAR(320) UNIQUE NOT NULL,
      homeTown VARCHAR(100) NOT NULL,
      dateOfBirth DATE NOT NULL,
      password VARCHAR(50) NOT NULL
    );
  """
)

INSERT_USER_QUERY = (
  """
    INSERT INTO Users (firstName, lastName, email, homeTown, dateOfBirth, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING userId;
  """
)
#### END OF SQL QUERIES ####

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
  with connection:
    with connection.cursor() as cursor:
      cursor.execute(CREATE_USERS_QUERY)
      cursor.execute(INSERT_USER_QUERY, (firstName, lastName, email, homeTown, dateOfBirth, password))
      userId = cursor.fetchone()[0]
  return { "id": userId, "message": f"User {firstName} {lastName} created." }, 201