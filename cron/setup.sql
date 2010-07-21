CREATE TABLE users (
	email VARCHAR(75) NOT NULL, 
	letters_sent INTEGER, 
	replys_completed INTEGER, 
	replys_dropped INTEGER, 
	PRIMARY KEY (email)
);
