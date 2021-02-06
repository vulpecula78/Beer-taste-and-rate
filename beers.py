from app import app
from flask import render_template, request, redirect, session, flash
from db import db

def addbeer(name, alcohol, beertype, country, brewery, description):
    try:
        sql = "INSERT INTO beer (name, alcohol_content, type_id, country_id, brewery_id, description, created_at) VALUES (:name, :alcohol_content, :type_id, :country_id, :brewery_id, :description, NOW())"
        db.session.execute(sql, {"name":name, "alcohol_content":alcohol, "type_id":beertype, "country_id":country, "brewery_id":brewery, "description":description})
        db.session.commit()
    except:
        return False
    return True

def addbrewery(brewery):
    try:
        sql = "INSERT INTO breweries (brewery) VALUES (:brewery)"
        db.session.execute(sql, {"brewery":brewery})
        db.session.commit()
    except:
        return False
    return True

def addcountry(country):
    try:
        sql = "INSERT INTO countries (country) VALUES (:country)"
        db.session.execute(sql, {"country":country})
        db.session.commit()
    except:
        return False
    return True

def addtype(type):
    try:
        sql = "INSERT INTO types (type) VALUES (:type)"
        db.session.execute(sql, {"type":type})
        db.session.commit()
    except:
        return False
    return True

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

def find(name):
    try:
        sql = "SELECT name FROM beer WHERE name LIKE :name"
        result = db.session.execute(sql, {"name":"%"+name+"%"})
        foundedbeer = result.fetchone()[0]
    except:
        return False
    return foundedbeer
    
