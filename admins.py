from app import app
from flask import render_template, request, redirect, session, flash
from db import db

def rm_country(id):
    try:
        sql = "DELETE FROM countries WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def rm_type(id):
    try:
        sql = "DELETE FROM types WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def rm_brewery(id):
    try:
        sql = "DELETE FROM breweries WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def rm_beer(id):
    try:
        sql = "DELETE FROM beer WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def rm_user(id):
    try:
        sql = "DELETE FROM users WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def rm_comment(id):
    try:
        sql = "DELETE FROM ratings WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True

def list_ratings(username):
    try:
        sql = "SELECT id FROM users WHERE username ILIKE :username"
        result = db.session.execute(sql, {"username":"%"+username+"%"})
        uid = result.fetchone()
        user_id = uid[0]
        sql = "SELECT ratings.id, users.username, comment FROM ratings JOIN users ON user_id = users.id WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        ratings = result.fetchall()
    except:
        return False
    return ratings

