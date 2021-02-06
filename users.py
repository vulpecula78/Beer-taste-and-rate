from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username , password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["username"] = username
            return True
        else:
           return False

def create_user(username, password):
    hash_value = generate_password_hash(password)
    print(hash_value)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return True
