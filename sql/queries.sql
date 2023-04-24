--create tabes
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

--select album query
SELECT albumId, AlbumName, dateOfCreation FROM Albums WHERE ownerId = %s AND AlbumName = %s;

--select albums query
SELECT albumId, AlbumName, dateOfCreation FROM Albums WHERE ownerId = %s;

--insert album query
INSERT INTO Albums (AlbumName, ownerId, dateOfCreation) 
VALUES (%s, %s, %s)
RETURNING albumId;

--delete album query
DELETE FROM Albums WHERE ownerId = %s AND AlbumName = %s;

--insert user query
INSERT INTO Users (firstName, lastName, email, homeTown, dateOfBirth, password, gender)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING userId;

--select user for logging in
SELECT userId, email, password FROM Users WHERE email = %s;

--suggested friends query
SELECT result.userId, firstName, lastName FROM Users
JOIN
(SELECT friendId as userId, COUNT(*) AS numFriends FROM Friends WHERE userId IN (SELECT friendId FROM Friends WHERE userId = 5) GROUP BY friendId ORDER BY numFriends DESC) AS result
ON Users.userId = result.userid
ORDER BY result.numFriends DESC;

--create friendship
INSERT INTO Friends (userId, friendId, dateOfFriendship)
VALUES (%s, %s, %s);

--get all friends
SELECT 
    Users.userId, 
    Users.firstName, 
    Users.lastName, 
    Friends.dateOfFriendship
FROM 
    Friends 
    JOIN Users ON Friends.friendId = Users.userId
WHERE 
    Friends.userId = %s;

--get popular tags
SELECT Tag, COUNT(*) AS numPosts
FROM Tags 
GROUP BY Tag 
ORDER BY COUNT(*) DESC LIMIT 50;

--top 10 users query
SELECT userId, firstName, lastName, contribution 
FROM Users 
ORDER BY contribution 
DESC LIMIT 10;

--you may also like recommendations
SELECT *
FROM Photos
WHERE PhotoId IN (SELECT photoID FROM
(SELECT PhotoId, COUNT(*) AS numTags 
FROM Tags 
WHERE Tag IN (SELECT Tag 
FROM Tags 
WHERE PhotoId IN (SELECT PhotoId 
FROM Photos 
WHERE albumId IN 
(SELECT albumId 
FROM Albums 
WHERE ownerId = %s))) 
GROUP BY PhotoId ORDER BY numTags DESC LIMIT 5) AS result)

-- search by first name
SELECT * 
FROM Users
WHERE firstName LIKE %s;

--search by first and last name
SELECT *
FROM Users
WHERE firstName = %s AND lastName LIKE %s;

--search by first and last name with exact match
SELECT *
FROM Users
WHERE firstName = %s AND lastName = %s;


SELECT *
FROM Users
WHERE firstName = %s AND lastName = %s AND CAST(userId AS TEXT) LIKE %s;

SELECT * FROM Users WHERE userId = %s

--add photo query
INSERT INTO Photos (albumId, caption, filePath, dateOfCreation)
VALUES ((SELECT albumId FROM Albums WHERE ownerId = %s AND AlbumName = %s), %s, %s, %s)
RETURNING photoId, caption, albumId, filePath, dateOfCreation;

-- updates contribution score
UPDATE Users SET contribution = contribution + 1 WHERE userId = %s

-- inserts tags
INSERT INTO Tags (Tag, PhotoId)
VALUES (%s, %s);

-- insert likes query
INSERT INTO Likes (userId, PhotoId) 
VALUES (%s, %s)

-- delete like query
DELETE FROM Likes WHERE userid = %s AND photoid = %s;

-- insert comments
INSERT INTO Comments (CommentText, commenterId, PhotoId, dateOfCreation) VALUES (%s, %s, %s, %s);
--update contribution
UPDATE Users SET contribution = contribution + 1 WHERE userId = %s;

-- gets all photos
SELECT * 
FROM Photos 
ORDER BY dateOfCreation DESC;

-- all photos given ids
SELECT * 
FROM Photos 
WHERE albumId IN 
    (SELECT albumId 
    FROM Albums 
    WHERE ownerId = %s);

-- all photos given tags and userid
SELECT Photos.*, COUNT(Tags.Tag) as MatchedTags
FROM Photos
JOIN Albums ON Albums.albumId = Photos.albumId
JOIN Tags ON Tags.PhotoId = Photos.photoId
WHERE Albums.ownerId = %s
AND Tags.Tag = ANY(%s)
GROUP BY Photos.photoId
ORDER BY MatchedTags DESC;

--photos given tag and username
SELECT *
FROM photos p
INNER JOIN albums a ON p.albumid = a.albumid
INNER JOIN users u ON a.ownerid = u.userid
WHERE a.albumname = %s AND u.userid = %s;

-- select individial photo
SELECT filePath FROM Photos 
WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s) 
AND photoId = %s;
--delete photo
DELETE FROM Photos WHERE photoId = %s;
UPDATE Users SET contribution = contribution - 1 WHERE userId = %s;
--search comments
SELECT Comments.*, Users.firstName, Users.lastName
FROM Comments JOIN Users ON Comments.commenterId = Users.userId
WHERE photoId = %s AND CommentText LIKE %s
--select comments
SELECT Comments.*, Users.firstName, Users.lastName
FROM Comments JOIN Users ON Comments.commenterId = Users.userId
WHERE photoId = %s


--get all photo information
SELECT 
    Photos.PhotoId,
    Photos.caption,
    Photos.albumId,
    Photos.filePath,
    Users.firstName,
    Users.lastName,
    Users.userId AS ownerId,
    COUNT(Likes.PhotoId) AS numLikes,
    ARRAY_AGG(DISTINCT(Tags.Tag)) AS tags,
    Photos.dateOfCreation
FROM 
    Photos
    JOIN Albums ON Photos.albumId = Albums.albumId
    JOIN Users ON Albums.ownerId = Users.userId
    LEFT JOIN Likes ON Photos.PhotoId = Likes.PhotoId
    LEFT JOIN Tags ON Photos.PhotoId = Tags.PhotoId
WHERE 
    Photos.PhotoId = %s
GROUP BY 
    Photos.PhotoId,
    Photos.caption,
    Photos.albumId,
    Photos.filePath,
    Users.firstName,
    Users.lastName,
    Users.userId;

--get number of likes for photo
SELECT COUNT(*)
FROM Likes
WHERE photoid = %s;

--see if user already liked the photo
SELECT COUNT(*)
FROM Likes
WHERE photoId = %s AND userId = %s;

