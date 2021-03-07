CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
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

CREATE TABLE beer (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    alcohol_content REAL,
    type_id INT,
    country_id INT,
    brewery_id INT,
    description TEXT,
    created_at TIMESTAMP,
    CONSTRAINT fk_brewery
      FOREIGN KEY(brewery_id) 
	  REFERENCES breweries(id)
	  ON DELETE CASCADE,
    CONSTRAINT fk_country
      FOREIGN KEY(country_id) 
	  REFERENCES countries(id)
	  ON DELETE CASCADE,
    CONSTRAINT fk_type
      FOREIGN KEY(type_id) 
	  REFERENCES types(id)
	  ON DELETE CASCADE
);

CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INT,
    beer_id INT,
    score INT,
    comment TEXT,
    created_at TIMESTAMP,
    CONSTRAINT fk_beer
      FOREIGN KEY(beer_id) 
	  REFERENCES beer(id)
	  ON DELETE CASCADE,
    CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES users(id)
	  ON DELETE CASCADE
);

INSERT INTO users(username, password) VALUES ('Admin', 'pbkdf2:sha256:150000$9lgl6X1F$27e7e87a7d3c00b260060ceb27478338f92376ce8f45de4da4b3744de07fe711');
INSERT INTO users(username, password) VALUES ('Testaaja', 'pbkdf2:sha256:150000$o1YEtVN9$653e1c94efd142a89dab5f969edc40d6ef19ebf9f8eb756fc78757df49622598');



