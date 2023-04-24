import os
import psycopg2
import jwt
from dotenv import load_dotenv
from flask import request, Flask
from functools import wraps
import inspect
from threading import Lock

# load_dotenv() loads all environment 
# variables from .env file so we can
# easily access them using os.getenv()
load_dotenv()

# create Flask app
app = Flask(__name__)

# get the DATABASE_URL environment variable that was stored in the .env file
db_url = os.getenv('DATABASE_URL')
# connect to database
db_connection = psycopg2.connect(db_url)

db_lock = Lock()

CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS Users (
        userId serial PRIMARY KEY,
        firstName VARCHAR(50) NOT NULL,
        lastName VARCHAR(50) NOT NULL,
        email VARCHAR(320) UNIQUE NOT NULL,
        homeTown VARCHAR(100),
        dateOfBirth DATE NOT NULL,
        password VARCHAR(100) NOT NULL,
        gender VARCHAR(50),
        contribution REAL DEFAULT 0,
        CHECK (gender = 'Male' OR gender = 'Female')
    );

    CREATE TABLE IF NOT EXISTS Albums (
        albumId serial PRIMARY KEY,
        AlbumName VARCHAR(50) NOT NULL,
        ownerId serial,
        dateOfCreation DATE NOT NULL,
        CONSTRAINT uc_Albums UNIQUE (ownerId, AlbumName),
        FOREIGN KEY (ownerId) REFERENCES Users(userId) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Photos (
        PhotoId serial PRIMARY KEY,
        caption VARCHAR(100) NOT NULL,
        albumId serial,
        filePath VARCHAR(300) NOT NULL,
        dateOfCreation DATE NOT NULL,
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
        
    SELECT setval('users_userid_seq', (SELECT MAX(userid) FROM Users));
    SELECT setval('albums_albumid_seq', (SELECT MAX(albumId) FROM Albums));
    SELECT setval('photos_photoid_seq', (SELECT MAX(photoid) FROM Photos));
    SELECT setval('comments_commentid_seq', (SELECT MAX(commentid) FROM Comments));
    SELECT setval('tags_tagid_seq', (SELECT MAX(tagid) FROM Tags));
    """
)

db_lock.acquire()
with db_connection:
    with db_connection.cursor() as cursor:
        cursor.execute(CREATE_TABLES)
db_lock.release()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt')
                
        if not token:
            return "Unauthorized", 401
        
        try:
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except:
            return "Unauthorized", 401
        
        if 'decoded_token' in inspect.signature(func).parameters:
            return func(decoded, *args, **kwargs)
        else:
            return func(*args, **kwargs)

    return decorated

def auth_required_soft(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt')

        if token:
            try:
                decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
                
                if 'decoded_token' in inspect.signature(func).parameters:
                    return func(decoded, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except:
                return func(*args, **kwargs)
        
    return decorated

import routes.auth_routes
import routes.friend_routes
import routes.photo_routes
import routes.album_routes
import routes.popular_routes
import routes.user_routes