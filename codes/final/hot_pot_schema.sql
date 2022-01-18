CREATE TABLE Store (
    Tel VARCHAR(12) PRIMARY KEY ,
    Addr VARCHAR(255) NOT NULL,
	Comment_num Int CHECK ((Comment_num>=0) or (Comment_num is NULL)),
	Price_level Float CHECK ((Price_level>=0 and Price_level<=5) or (Price_level is NULL)),
	Store_name VARCHAR(255),
	Brand VARCHAR(255) Not NULL,
	City CHAR(3) Not NULL,
	District CHAR(3) Not NULL,
	Avg_rating Float CHECK ((Avg_rating>=1 and Avg_rating<=5) or (Avg_rating is NULL)),
	FOREIGN KEY (Brand) REFERENCES Hot_pot(Brand) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (City, District) REFERENCES Region(City, District) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Region (
	City CHAR(3),
	District CHAR(3),
	PRIMARY KEY (City, District)
);

CREATE TABLE Hot_pot (
	Brand VARCHAR(255) PRIMARY KEY 
);

CREATE TABLE Service (
	Lng Float,
	Lat Float,
	Tel VARCHAR(12) PRIMARY KEY REFERENCES Store(Tel) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Commentor (
	Commentor1 VARCHAR(255), 
	Commentor2 VARCHAR(255), 
	Commentor3 VARCHAR(255), 	
	Tel VARCHAR(12) PRIMARY KEY REFERENCES Store(Tel) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Operation (
	Open_Day Int Not NULL CHECK (Open_Day>=0 and Open_Day<=6), 
	Begin_ Int Not NULL CHECK (Begin_>=0 and Open_Day<=2400), 
	End_ Int Not NULL CHECK (End_>=0 and Open_Day<=2400),
	Tel VARCHAR(12),
	PRIMARY KEY (Tel, Open_Day, Begin_, End_),
	FOREIGN KEY(Tel) REFERENCES Store(Tel) ON DELETE CASCADE ON UPDATE CASCADE
);


