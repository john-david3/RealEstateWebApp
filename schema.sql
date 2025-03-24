DROP TABLE IF EXISTS properties;

CREATE TABLE properties
(
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    county VARCHAR(30) NOT NULL,
    post_code CHAR(7) NOT NULL,
    price INTEGER NOT NULL, 
    house_type VARCHAR(24),
    bedroom INTEGER NOT NULL,
    bathroom INTEGER NOT NULL,
    photo TEXT NOT NULL,
    description TEXT NOT NULL,
    bid_amount INTEGER NOT NULL DEFAULT 0
);

INSERT INTO properties (full_name, email, address, county, post_code, price, house_type, bedroom, bathroom, photo, description)
VALUES  ('Brian Quinn', 'b.quinn129@yahoo.com', '123 Bóthar Buí, Tralee','Roscommon', 'X12F011', 214000, 'Detached House', 2, 2, 'botharbui.jpg', 'very nice house, lots of space'),
        ('Michael Box', 'mikeyb1916e@gmail.com', '6 Sing Street, Aghalour', 'Roscommon','X23A9PQ', 130000, 'Detached House', 2, 1, 'singstreet.jpg', 'very nice house, lots of space'),
        ('Ann Nonymous', 'annnonymous772@gmail.com', '99 Dons Avenue, Dundrum', 'Dublin', 'K92D5FE', 510000, 'Terraced House', 3, 2, 'donsavenue.webp', 'very nice house, lots of space'),
        ('Dimitry Teyap', 'scored11forwestham@gmail.com', '1 Heavens Kitchen, Youghal', 'Cork','V76F8JK', 400000, 'Semi-Detached House', 2, 2, 'heavenskitchen.webp', 'very nice house, lots of space'),
        ('Susan Doyle', 'susandoyle0161@outlook.com', '21 Plummet Road, Portlaoise', 'Laois','H15G3LM', 150000, 'Detached House', 2, 1, 'plummetroad.jpg', 'very nice house, lots of space'),
        ('Muireann Rowan', 'iusedanrngforthis17@gmail.com', '5 House Apartments, Ballincollig', 'Cork', 'Z33N7RS', 200000, 'Apartment', 1, 1, 'houseapt.jpg', 'very nice house, lots of space'),
        ('Rayne Wooney', 'spoonerism250@yahoo.com', '250 Scorers Lane, Swords', 'Dublin','R49P2TY', 752000, 'Duplex', 4, 2, 'scorerslane.jpg', 'very nice house, lots of space'),
        ('Jon Dave Whyte', 'whytejondave2@outlook.com', '66 Ash Street, Jobstown', 'Dublin', 'B71Q6WX', 550000, 'Terraced House', 3, 2, 'ashstreet.webp', 'very nice house, lots of space'),
        ('Richard Brunson', 'd3f0n0tv1rg1nm3d14@gmail.com', '4 Real Place, Heavenstown','Laois', 'M89S1ZC', 700000, 'Bungalow', 2, 3, 'realplace.jpg', 'very nice house, lots of space'),
        ('Mark Cuban', 'actualmarkcuban420@protonmail.com', 'Billionaire Mansion, Dalkey','Dublin', 'W67V4NF', 1500000, 'Detached House', 4, 4, 'billionairemansion.jpg', 'very nice house, lots of space'),
        ('Meadhbh McGrory', 'here4equality15@icloud.com', '18 Road Street Avenue, Tramore', 'Waterford', 'F54T2DE', 205000, 'Semi-Detached House', 2, 2, 'roadstreetavenue.webp', 'very nice house, lots of space'),
        ('Freyja Albertsson', 'freyisalb354@gmail.com', 'Áras an Uacthair Reoite, Kilmise', 'Waterford','L98K6BH', 197000, 'Detached House', 3, 1, 'kilmise.jpg', 'very nice house, lots of space')
;

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id VARCHAR(16) PRIMARY KEY,
    email VARCHAR(32) NOT NULL,
    password VARCHAR(50) NOT NULL
);

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews
(  
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(16) NOT NULL,
    review TEXT NOT NULL
);

DROP TABLE IF EXISTS reviews_1;
DROP TABLE IF EXISTS reviews_4;
DROP TABLE IF EXISTS reviews_3;
DROP TABLE IF EXISTS reviews_2;
DROP TABLE IF EXISTS reviews_5;
DROP TABLE IF EXISTS reviews_7;

DROP TABLE IF EXISTS listings_for_approval;

CREATE TABLE listings_for_approval
(
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    county VARCHAR(30) NOT NULL,
    post_code CHAR(7) NOT NULL,
    price INTEGER NOT NULL, 
    house_type VARCHAR(24),
    bedroom INTEGER NOT NULL,
    bathroom INTEGER NOT NULL,
    photo TEXT NOT NULL,
    description TEXT NOT NULL
);
SELECT * FROM listings_for_approval

DROP TABLE IF EXISTS enquiries;

CREATE TABLE enquiries
(
    enquiry_id INTEGER PRIMARY KEY NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(50) NOT NULL,
    enquiry TEXT NOT NULL,
    owner_email VARCHAR(255) NOT NULL,
    property_name VARCHAR(100) NOT NULL
);