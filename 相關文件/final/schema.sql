CREATE TABLE Store (
    Phonenumber CHAR(8) PRIMARY KEY ,
    Comment_num Integer NOT NULL,
	Avg_rating Float Not NULL,
	Brand VARCHAR(10) Not NULL,
	FOREIGN KEY (Brand) REFERENCES Hot_pot(Brand)
);

CREATE TABLE Hot_pot (
	Brand VARCHAR(10)PRIMARY KEY
);