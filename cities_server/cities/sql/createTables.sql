PRAGMA foreign_keys = ON;

CREATE TABLE Cities(
    city_id INTEGER PRIMARY KEY,
    city_name VARCHAR(64) NOT NULL,
    state_name VARCHAR(64) NOT NULL,
    longitude REAL NOT NULL,
    latitude REAL NOT NULL,
    climate VARCHAR(64) NOT NULL,
    Avg_Hotel_Price INTEGER NOT NULL,
    closest_airport VARCHAR(64) NOT NULL
);

CREATE TABLE Activities(
    activity_id INTEGER PRIMARY KEY,
    activity_name VARCHAR(64) NOT NULL
);

CREATE TABLE City_Activities(
    city_id Integer REFERENCES Cities(city_id) ON DELETE CASCADE,
    activity_id Integer REFERENCES Activities(activity_id) ON DELETE CASCADE,
    rating DECIMAL(15,1),
    PRIMARY KEY (city_id, activity_id)
);

CREATE TABLE Specific_Activities(
    city_id Integer REFERENCES Cities(city_id) ON DELETE CASCADE,
    activity_id Integer REFERENCES Activities(activity_id) ON DELETE CASCADE,
    specific_activity_id Integer,
    activity_name VARCHAR(64) NOT NULL,
    rating Float,
    number_ratings Integer,
    weighted_rating DECIMAL(11,1),
    PRIMARY KEY (city_id, activity_name)
);

CREATE TABLE Cuisines(
    cuisine_id INTEGER PRIMARY KEY,
    cuisine_name VARCHAR(64) NOT NULL
);

CREATE TABLE City_Restaurants(
    city_id Integer REFERENCES Cities(city_id) ON DELETE CASCADE,
    cuisine_id Integer REFERENCES Cuisines(cuisine_id) ON DELETE CASCADE,
    restaurant_id Integer,
    restaurant_name VARCHAR(64) NOT NULL,
    rating Integer,
    number_ratings Integer,
    weighted_rating DECIMAL(11,1),
    PRIMARY KEY (restaurant_id)
);