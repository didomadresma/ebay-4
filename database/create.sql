

DROP TABLE IF EXISTS Users;


CREATE TABLE Users(
	userID TEXT PRIMARY KEY,
	rating REAL NOT NULL,
	location TEXT,
	country TEXT
);

DROP TABLE IF EXISTS Items;
CREATE TABLE Items(
	itemID INTEGER PRIMARY KEY,
	name TEXT,
	currently REAL,
	buyPrice REAL,
	firstBid REAL,
	numberOfBids INTEGER,
	started DATETIME,
	ends DATETIME CHECK(ends > started),
	sellerID TEXT,
	description TEXT,

	FOREIGN KEY(sellerID) REFERENCES Users (userID)
	
);


DROP TABLE IF EXISTS Bids;
CREATE TABLE Bids(
	itemID INTEGER ,
	userID TEXT ,
	time DATETIME,
	amount REAL,
	PRIMARY KEY(itemID, userID, amount),
	FOREIGN KEY(itemID) REFERENCES Items (itemID)
	FOREIGN KEY(userID) REFERENCES Users (userID)

);


DROP TABLE IF EXISTS Categories;
CREATE TABLE Categories(
	itemID INTEGER,
	category TEXT NOT NULL,
	PRIMARY KEY(itemID, category)
	FOREIGN KEY(itemID) REFERENCES Items (itemID)
);

DROP TABLE if exists Current_Time; 
CREATE TABLE Current_Time (
	curtime DATETIME NOT NULL
) ; 
INSERT into Current_Time values ("2001-12-20 00:00:01"); 
SELECT curtime from Current_Time;
