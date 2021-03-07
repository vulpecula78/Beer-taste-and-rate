from app import app
from flask import render_template, request, redirect, session, flash
from db import db

#addbeer into database
def addbeer(name, alcohol, beertype, country, brewery, description):
    try:
        sql = "INSERT INTO beer (name, alcohol_content, type_id, country_id, brewery_id, description, created_at) VALUES (:name, :alcohol_content, :type_id, :country_id, :brewery_id, :description, NOW())"
        db.session.execute(sql, {"name":name, "alcohol_content":alcohol, "type_id":beertype, "country_id":country, "brewery_id":brewery, "description":description})
        db.session.commit()
    except:
        return False
    return True

#add brewery into database
def addbrewery(brewery):
    try:
        sql = "INSERT INTO breweries (brewery) VALUES (:brewery)"
        db.session.execute(sql, {"brewery":brewery})
        db.session.commit()
    except:
        return False
    return True

#add country into database
def addcountry(country):
    try:
        sql = "INSERT INTO countries (country) VALUES (:country)"
        db.session.execute(sql, {"country":country})
        db.session.commit()
    except:
        return False
    return True

#add beertype into data base
def addtype(type):
    try:
        sql = "INSERT INTO types (type) VALUES (:type)"
        db.session.execute(sql, {"type":type})
        db.session.commit()
    except:
        return False
    return True

#add user review of beer
def addreview(comment, score, beer, username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    sql = "SELECT id FROM beer WHERE name=:beer"
    result = db.session.execute(sql, {"beer":beer})
    beer_id = result.fetchone()[0]
    try:
        sql = "INSERT INTO ratings (user_id, beer_id, score, comment, created_at) VALUES (:user_id, :beer_id, :score, :comment, NOW())"
        db.session.execute(sql, {"user_id":user_id, "beer_id":beer_id, "score":score, "comment":comment})
        db.session.commit()
    except:
        return False
    return True

# edit review
def editreview(comment, score, comment_id):
    try:
        sql = "UPDATE ratings SET score=:score, comment=:comment WHERE id=:comment_id"
        db.session.execute(sql, {"comment":comment, "score":score, "comment_id":comment_id})
        db.session.commit()
    except:
        return False
    return True

#search for beer
def find(name, country_id, type_id):
    try:        
        if country_id != "Kaikki" and type_id != "Kaikki":
            sql = "SELECT name FROM beer WHERE name ILIKE :name AND country_id=:country_id AND type_id=:type_id LIMIT 8"
            result = db.session.execute(sql, {"name":"%"+name+"%", "country_id":country_id, "type_id":type_id}) 
        elif country_id != "Kaikki" and type_id == "Kaikki":
            sql = "SELECT name FROM beer WHERE name ILIKE :name AND country_id=:country_id LIMIT 8"
            result = db.session.execute(sql, {"name":"%"+name+"%", "country_id":country_id}) 
        elif country_id == "Kaikki" and type_id != "Kaikki":
            sql = "SELECT name FROM beer WHERE name ILIKE :name AND type_id=:type_id LIMIT 8"
            result = db.session.execute(sql, {"name":"%"+name+"%", "type_id":type_id})
        else:
            sql = "SELECT name FROM beer WHERE name ILIKE :name LIMIT 8"
            result = db.session.execute(sql, {"name":"%"+name+"%"})
        foundedbeer = result.fetchall()
    except:
        return False
    return foundedbeer

def beerdata(beer):
    sql = """SELECT name, alcohol_content, types.type, breweries.brewery, countries.country, description FROM beer
            JOIN breweries ON beer.brewery_id = breweries.id JOIN types ON beer.type_id = types.id JOIN countries ON beer.country_id = countries.id WHERE name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    beerdata = result.fetchall()
    return beerdata
    
def best():
    try:
        result = db.session.execute("SELECT beer.name, AVG(score)::numeric(10,2), count(score) FROM ratings JOIN beer ON beer.id = beer_id GROUP BY beer.name ORDER BY AVG(score) DESC LIMIT 5")
        bests = result.fetchall()
        return bests
    except:
        return None

def latest():
    try:
        result = db.session.execute("SELECT name FROM beer ORDER BY created_at DESC LIMIT 5") 
        olut = result.fetchall()
        return olut
    except:
        return None

def ratings(beer):
    try:
        sql = """SELECT ratings.id, users.username, score,  comment, TO_CHAR(ratings.created_at, 'DD-MM-YYYY HH24:MI') FROM ratings JOIN beer ON beer.id = ratings.beer_id JOIN users ON users.id = ratings.user_id WHERE beer.name=:beer"""
        result = db.session.execute(sql, {"beer":beer})
        ratings = result.fetchall()
        return ratings
    except:
        return None
    
def avgscore(beer):
    try:
        sql = "SELECT AVG(score)::numeric(10,2) FROM ratings JOIN beer ON beer.id = beer_id WHERE beer.name=:beer GROUP BY beer.name"
        result = db.session.execute(sql, {"beer":beer})
        avgscore = result.fetchone()
        return avgscore
    except:
        return 0
    
def rated(ratings):
    user = session.get('username')
    for item in ratings:
        if item[1] == user:
            rated = True
            return rated      
    rated = False
    return rated
        
