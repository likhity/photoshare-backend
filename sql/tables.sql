CREATE TABLE Users (
  userId serial PRIMARY KEY,
  firstName VARCHAR(50) NOT NULL,
  lastName VARCHAR(50) NOT NULL,
  email VARCHAR(320) UNIQUE NOT NULL,
  homeTown VARCHAR(100) NOT NULL,
  dateOfBirth DATE NOT NULL,
  password VARCHAR(50) NOT NULL,
  gender VARCHAR(50) NOT NULL,
  CHECK (gender = 'Male' OR gender = 'Female')
);

CREATE TABLE Albums (
  albumId serial PRIMARY KEY,
  AlbumName VARCHAR(50) NOT NULL,
  ownerID serial,
  dateOfCreation DATE NOT NULL,
  FOREIGN KEY (ownerID) REFERENCES Users(ownerID) ON DELETE CASCADE
);

-- create a photo table with a foreign key to the album table upon deletion of the album, the photos will be deleted as well
CREATE TABLE Photos (
  PhotoId serial PRIMARY KEY,
  caption VARCHAR(100) NOT NULL,
  albumID serial,
  filePath VARCHAR(100) NOT NULL,
  FOREIGN KEY (albumID) REFERENCES Albums(albumID) ON DELETE CASCADE
);

-- create a table for the comments with a unique comment id and with following attributes: text, commenter, photoid, and date of comment
CREATE TABLE Comments (
  CommentId serial PRIMARY KEY,
  CommentText VARCHAR(500) NOT NULL,
  commenterID serial,
  PhotoId serial,
  dateOfCreation DATE NOT NULL,
  FOREIGN KEY (commenterID) REFERENCES Users(userID) ON DELETE CASCADE,
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

