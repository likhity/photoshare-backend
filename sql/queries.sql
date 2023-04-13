-- Names: Joaquin Uribe, Likhit Vyas Yarramsetti, Abhisekhar Bharadwaj Gandavarapu, Alexander Hixson

CREATE TABLE Users (
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
--create albums table with a foreign key to albums
CREATE TABLE Albums (
  albumId serial PRIMARY KEY,
  AlbumName VARCHAR(50) NOT NULL,
  ownerId serial,
  dateOfCreation DATE NOT NULL,
  FOREIGN KEY (ownerId) REFERENCES Users(userId) ON DELETE CASCADE
);

-- create a photo table with a foreign key to the album table upon deletion of the album, the photos will be deleted as well
CREATE TABLE Photos (
  PhotoId serial PRIMARY KEY,
  caption VARCHAR(100) NOT NULL,
  albumId serial,
  filePath VARCHAR(100) NOT NULL,
  FOREIGN KEY (albumId) REFERENCES Albums(albumId) ON DELETE CASCADE
);

-- create a table for the comments with a unique comment id and with following attributes: text, commenter, photoid, and date of comment
CREATE TABLE Comments (
  CommentId serial PRIMARY KEY,
  CommentText VARCHAR(500) NOT NULL,
  commenterId serial,
  PhotoId serial,
  dateOfCreation DATE NOT NULL,
  FOREIGN KEY (commenterId) REFERENCES Users(userId) ON DELETE CASCADE,
  FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE
);

--create a table for the likes with a unique like id and with following attributes: userid, photoid
CREATE TABLE Likes (
  userId serial,
  PhotoId serial,
  FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE,
  FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE,
  PRIMARY KEY (userId, PhotoId)
);

--create a table for the tags with a unique tag id and with following attributes: tag (single word and all lower cased with no spaces), photoid. Many photos can belong to the same tag in different albums.also, a tag can be used in multiple photos in the same album check the take is a single word and lowerspaced, with only alphabetic characters
CREATE TABLE Tags (
  TagId serial PRIMARY KEY,
  Tag VARCHAR(50) NOT NULL,
  PhotoId serial,
  FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId) ON DELETE CASCADE,
  CHECK (Tag ~ '^[a-z]+$')
);

--create a table for the friends with a unique friend id and with following attributes: userid, friendid, date of friendship. a user can have multiple friends and a friend can have multiple users
CREATE TABLE Friends (
  userId serial,
  friendId serial,
  dateOfFriendship DATE NOT NULL,
  FOREIGN KEY (userId) REFERENCES Users(userId) ON DELETE CASCADE,
  FOREIGN KEY (friendId) REFERENCES Users(userId) ON DELETE CASCADE,
  PRIMARY KEY (userId, friendId)
);


----user management queries below----
-- this query creates a new "friendship" between two users (front end will ensure you cannot friend yourself)
INSERT INTO Friends (userId, friendId, dateOfFriendship)
VALUES (%s, %s, 'yyyy-mm-dd');


--register a new user
INSERT INTO Users (firstName, lastName, email, homeTown, dateOfBirth, password)
VALUES (%s, %s, %s, %s, %s, %s);

--this query searches for a users by name and displays the results in order of last name and date of birth showing hometown and gender if applicable
SELECT firstName, lastName, dateOfBirth, gender, homeTown FROM Users WHERE firstName = %s AND lastName = %s ORDER BY lastName, dateOfBirth;

--display a list of user's friends (self or other) users
SELECT * FROM Users WHERE userId IN (SELECT friendId FROM Friends WHERE userId = %s);



--display the top 10 users with the contribution points
SELECT userId, firstName, lastName, contribution FROM Users ORDER BY contribution DESC LIMIT 10;




--see if the user exists for logging in
SELECT userId from Users where email = %s AND password = %s;
--delete user and all albums and photos and comments and likes and tags and friends
DELETE FROM Users WHERE userId = %s;

----photo/album queries below----
--show all photos for browsing
SELECT * FROM Photos ORDER BY dateOfCreation DESC;
--show all albums for browsing
SELECT * FROM Albums ORDER BY dateOfCreation DESC;



--select all photos from an album
Select * FROM Photos WHERE Albums.albumId = Photos.albumId;
--select album from a photo
SELECT * FROM Albums where Photos.albumId = Albums.albumId;


--show all photos for a user/self
SELECT * FROM Photos WHERE Photos.albumId = Albums.albumId AND Albums.ownerId = %s;
--select all albums for a user/self
SELECT * FROM Albums WHERE ownerId = %s;


--select all photos given ownerId
SELECT * FROM Photos WHERE ownerId = %s;
--select all photos given ownerId and tags
SELECT * FROM Photos WHERE PhotoId IN (SELECT PhotoId FROM Tags WHERE ownerId = %s AND Tag = %s;



--select album id
SELECT 
--create album
INSERT INTO Albums (AlbumName, ownerId, dateOfCreation) VALUES (%s, %s, 'yyyy-mm-dd');
--upload photo to album and increase contribution
INSERT INTO Photos (caption, albumId, filePath) VALUES (%s, %s, %s);
UPDATE Users SET contribution = contribution + 1 WHERE userId = %s;
--delete album and all photos in album
DELETE FROM Albums WHERE albumId = %s;
--delete photo and all likes and comments on photo
DELETE FROM Photos WHERE PhotoId = %s;

--modify album name if owned by user (will be supplied by ui/front end)
UPDATE Albums SET AlbumName = %s WHERE albumId = %s AND ownerId = %s;

----tag queries below----
--search photos by tag
SELECT * FROM Photos WHERE PhotoId IN (SELECT PhotoId FROM Tags WHERE Tag = %s);

--search tags
SELECT DISTINCT * FROM Tags WHERE  Tag = %s;

--display all user's photos that have been tagged with a specific tag (will be supplied by ui/front end for self display)
SELECT * FROM Photos WHERE PhotoId IN (SELECT PhotoId FROM Tags WHERE Tag = %s) AND Photos.albumId = Albums.albumId AND Albums.ownerId = %s;

--select all photos with a specific tag
SELECT * FROM Photos WHERE PhotoId IN (SELECT PhotoId FROM Tags WHERE Tag = %s);
--select most popular tags
SELECT Tag, COUNT(*) FROM Tags GROUP BY Tag ORDER BY COUNT(*) DESC LIMIT 50;
--search all user's photos that have multiple tags
SELECT * FROM Photos WHERE PhotoId IN (SELECT PhotoId FROM Tags GROUP BY PhotoId HAVING COUNT(*) > 1) AND Photos.albumId = Albums.albumId AND Albums.ownerId = %s;


--comments/like queries below--

--add comment to photo and update user's contribution (contrib)
INSERT INTO Comments (CommentText, commenterId, PhotoId, dateOfCreation) VALUES (%s, %s, %s, 'yyyy-mm-dd');
UPDATE Users SET contrib = contrib + 1 WHERE userId = %s;
--like a photo and update photo's like count

INSERT INTO Likes (userId, PhotoId) VALUES (%s, %s);


--retrieve like count for a photo
SELECT COUNT(*) FROM Likes WHERE PhotoId = %s;
--search comments of users by text search. users with the most relevant comments will be displayed first down to the least relevant(how to determine relevancy???)
SELECT * FROM Comments WHERE CommentText LIKE %s ORDER BY dateOfCreation DESC;
-----recommendations queries below-----
--get list of friends of friends ordered by how many times each reccomended friend appears in the list
SELECT friendId, COUNT(*) AS numFriends FROM Friends WHERE userId IN (SELECT friendId FROM Friends WHERE userId = %s) GROUP BY friendId ORDER BY numFriends DESC;

--get list of reccommended photos by taking the 5 most common tags of the user's photos, ordered by how many tags mactch the photo
SELECT PhotoId, COUNT(*) AS numTags FROM Tags WHERE Tag IN (SELECT Tag FROM Tags WHERE PhotoId IN (SELECT PhotoId FROM Photos WHERE albumId IN (SELECT albumId FROM Albums WHERE ownerId = %s))) GROUP BY PhotoId ORDER BY numTags DESC LIMIT 5;
