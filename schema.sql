CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    user_lvl INT
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INT,
    beer_id INT,
    score INT,
    comment TEXT,
    created_at TIMESTAMP
);

CREATE TABLE beer (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    alcohol_content REAL,
    type_id INT,
    country_id INT,
    brewery_id INT,
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE types (
    id SERIAL PRIMARY KEY,
    type TEXT UNIQUE
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    country TEXT UNIQUE
);

CREATE TABLE breweries (
    id SERIAL PRIMARY KEY,
    brewery TEXT UNIQUE
);

