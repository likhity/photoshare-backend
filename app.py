import os
import time
import psycopg2
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
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
CREATE_TABLES = (
  """
  CREATE TABLE IF NOT EXISTS Users (
    userId serial PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(320) UNIQUE NOT NULL,
    homeTown VARCHAR(100),
    dateOfBirth DATE NOT NULL,
    password VARCHAR(50) NOT NULL,
    gender VARCHAR(50),
    contribution REAL DEFAULT 0,
    CHECK (gender = 'Male' OR gender = 'Female')
  );

  CREATE TABLE IF NOT EXISTS Albums (
    albumId serial PRIMARY KEY,
    AlbumName VARCHAR(50) NOT NULL,
    ownerId serial,
    dateOfCreation DATE NOT NULL,
    FOREIGN KEY (ownerId) REFERENCES Users(userId) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS Photos (
    PhotoId serial PRIMARY KEY,
    caption VARCHAR(100) NOT NULL,
    albumId serial,
    filePath VARCHAR(100) NOT NULL,
    FOREIGN KEY (albumId) REFERENCES Albums(albumId) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS Comments (
    CommentId serial PRIMARY KEY,
    CommentText VARCHAR(500) NOT NULL,
    commenterId serial,
    PhotoId serial,
    dateOfCreation DATE NOT NULL,
    FOREIGN KEY (commenterId) REFERENCES Users(userId) ON DELETE CASCADE,
    FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS Likes (
    userId serial,
    PhotoId serial,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE,
    FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE,
    PRIMARY KEY (userId, PhotoId)
  );

  CREATE TABLE IF NOT EXISTS Tags (
    TagId serial PRIMARY KEY,
    Tag VARCHAR(50) NOT NULL,
    PhotoId serial,
    FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE,
    CHECK (Tag ~ '^[a-z]+$')
  );

  CREATE TABLE IF NOT EXISTS Friends (
    userId serial,
    friendId serial,
    dateOfFriendship DATE NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE,
    FOREIGN KEY (friendId) REFERENCES Users(userId) ON DELETE CASCADE,
    PRIMARY KEY (userId, friendId)
  );
  """
)
#### END OF SQL QUERIES ####

with connection:
  with connection.cursor() as cursor:
    cursor.execute(CREATE_TABLES)

@app.route("/api/time")
def get_current_time():
  return { "time": time.time() }

import auth_routes
import friend_routes
import photo_routes
import album_routes
import popular_routes
import user_routes