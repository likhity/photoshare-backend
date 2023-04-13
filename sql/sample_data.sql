INSERT INTO Users (userId,firstName,lastName,email,homeTown,dateOfBirth,password,gender,contribution) 
VALUES
(1,'Phillida','Whordley','pwhordley0@alexa.com','Xuedian','1998-12-06','$2b$12$K5Velpf0D1n88IBkkqtsxeKSYdJuJrIsaMNXnS0fbSedb5oo9q1AK','Female',1),
(2,'Karon','Bruford','kbruford1@bbc.co.uk','Masākin','1984-06-13','$2b$12$5RYuaJu1PmCifCTw5oRz5OwAbt6/jKluJ19llm8wtwlmUa51vmFFm','Male',1),
(3,'Northrop','Petrov','npetrov2@delicious.com','Yonglong','1985-11-30','$2b$12$lYikh3z4Xj.lTzgF/b2KR.1BEQn0zrB3gMhuzYj9MwXLXvkO8LELK','Male',0),
(4,'Lek','Arne','larne3@uiuc.edu','Berlin','1993-05-15','$2b$12$dqne6Vk80k/xpovYMpkeYuy7AeVw9JQ3l5GuqIl88wpCfvNhXiZdK','Male',1),
(5,'Bria','Yaus','byaus4@comsenz.com','Aloja','1985-05-06','$2b$12$A9Rm7/NdPD7M9n8k.GBLd.0KZsU082gDaG466tTwiYXZVpMmciSTK','Female',1),
(6,'Elnora','Dounbare','edounbare5@washington.edu','Jackson','1973-04-04','$2b$12$faxNi/nPWNVwUKmDFhuIYOc4jUJN6CUNXjPcBoRIkC22ILQjH7wra','Female',0),
(7,'Dorthy','Mowlam','dmowlam6@washingtonpost.com','Fort Worth','1994-09-11','$2b$12$h.cEmpxykh4JsNsmF2UzTOgDSgoTto5NbcpBcK4f9qYHYUHPFBo3y','Female',0),
(8,'Giff','Gronaller','ggronaller7@weebly.com','Tyringe','1989-11-01','$2b$12$6BpiOlz4NYwAloi0sPkmz.yXokI5KcPO5OMXxNaYa1REhtBR6lDOG','Male',1),
(9,'Licha','de Almeida','ldealmeida8@simplemachines.org','Kasaoka','1983-02-04','$2b$12$PfL5hrZ6SVBkefDN6P8fK.JV./AiIdBOa1xHxp8orfX18Ula99402','Female',1),
(10,'Donelle','Babe','dbabe9@meetup.com','Casal Novo','1981-03-23','$2b$12$DSywoqQWWZt.sTStUcPFhO23AMtXSDjFiMsC/p5IvCIoFWTZXTZCi','Female',2),
(11,'Sheev','Palpatine','awhitwhama@topsy.com','Neringa','1985-04-29','$2b$12$f673.idvU76miCMZ.wH.teQJc.QAIL92LeGsLYHP1hTbdR7351s1u','Male',2);

INSERT INTO Albums (albumId,AlbumName,ownerId,dateOfCreation)
VALUES
(1,'My Pets',4,'2023-02-01'),
(2,'Europe Tour',8,'2023-02-19'),
(3,'Me and My BFFs ❤️',5,'2022-11-15'),
(4,'Shaggy',9,'2022-06-10'),
(5,'Famous quotes',10,'2022-03-19'),
(6,'My Love',2,'2022-03-18'),
(7,'Mountain Biking Pics',11,'2022-08-10'),
(8,'My favs',2,'2022-03-22'),
(9,'Beautiful moments',1,'2022-03-19'),
(10,'Awwwwww',4,'2022-05-06'),
(11,'Seattle',11,'2022-03-18');

INSERT INTO Photos (PhotoId,caption,albumId,dateOfCreation,filePath)
VALUES
(1,'My Dog is cute!',10,'2021-11-18','https://media-be.chewy.com/wp-content/uploads/2022/09/27095535/cute-dogs-pembroke-welsh-corgi.jpg'),
(2,'To be or not to be',5,'2023-11-18','https://i.ytimg.com/vi/nuH4EHB2eiA/maxresdefault.jpg'),
(3,'Berlin is a cool place',2,'2022-11-18','https://compote.slate.com/images/21e6a1b3-858d-436d-b9ff-f7057e8cc690.jpg'),
(4,'Space shuttle',11,'2019-11-18','https://cdn.britannica.com/91/72291-004-BAE955B3/space-shuttle-Endeavour-landing-Edwards-Air-Force-May-2000.jpg'),
(5,'Biking and hiking',7,'2018-11-18','https://h5d9a9f8.rocketcdn.me/wp-content/uploads/2017/09/hike-a-bike-4.jpg'),
(6,'Aladdin flying carpet',9,'2020-11-18','https://cdn.nazmiyalantiquerugs.com/wp-content/uploads/2016/05/flying-magic-carpets-of-aladdin-nazmiyal-antique-rugs-599x449.jpg'),
(7,'I love ice cream',8,'2017-11-18','https://t3.ftcdn.net/jpg/04/43/73/58/360_F_443735896_QLONgfc1LdfAlgJXMeMJrwLFjBhdj6t1.jpg'),
(8,'Chillin with da homies',3,'2016-11-18','https://i.redd.it/l7d6nvd0nk261.jpg'),
(9,'My cat is so cute',4,'2015-11-18','https://images.unsplash.com/photo-1529778873920-4da4926a72c2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y3V0ZSUyMGNhdHxlbnwwfHwwfHw%3D&w=1000&q=80'),
(10,'I love democracy, I love the Republic',5,'2014-11-18','https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.kym-cdn.com%2Fentries%2Ficons%2Ffacebook%2F000%2F028%2F497%2Fpalp.jpg');

INSERT INTO Comments (CommentId,CommentText,commenterId,PhotoId,dateOfCreation)
VALUES
(1,'Dog, african wild',5,7,'2022-08-17'),
(2,'Bushbuck',5,10,'2022-10-17'),
(3,'Banded mongoose',4,5,'2022-08-30'),
(4,'Mocking cliffchat',3,3,'2023-01-20'),
(5,'Roseate cockatoo',8,7,'2022-10-15'),
(6,'Owl, madagascar hawk',1,5,'2022-12-19'),
(7,'Andean goose',3,2,'2023-01-06'),
(8,'Sheep, american bighorn',9,10,'2022-12-19'),
(9,'Green heron',7,10,'2022-10-06'),
(10,'Hen, sage',6,7,'2022-07-05'),
(11,'Fork-tailed drongo',7,5,'2022-06-29'),
(12,'Grey lourie',3,9,'2022-06-18');

INSERT INTO Likes (userId,PhotoId)
VALUES
(5,9),
(7,6),
(2,9),
(10,10),
(8,4),
(9,2),
(10,8),
(9,4),
(7,1),
(8,10),
(1,2);

INSERT INTO Tags (TagId,Tag,PhotoId)
VALUES
(1,'chillin',8),
(2,'icecream',7),
(3,'homie',8),
(4,'dog',1),
(5,'berlin',3),
(6,'friends',8),
(7,'cute',9),
(8,'inspirational',2),
(9,'cute',1),
(10,'pet',1),
(11,'aww',1);

INSERT INTO Friends (userId,friendId,dateOfFriendship)
VALUES
(11,4,'2022-08-21'),
(11,5,'2022-07-22'),
(9,1,'2022-04-22'),
(5,9,'2022-08-06'),
(1,5,'2022-08-03'),
(5,10,'2023-01-20'),
(10,7,'2022-09-29'),
(1,10,'2022-09-25'),
(9, 11, '2023-04-11'),
(9, 7, '2023-04-11');
