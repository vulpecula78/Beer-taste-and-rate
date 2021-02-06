from app import app
from flask import render_template, request, redirect, session, flash
from db import db
import beers
import users

#---------------------------------------Main----------------------------------------------------------
@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/main")
def main():
    result = db.session.execute("SELECT name FROM beer ORDER BY created_at DESC LIMIT 5") 
    olut = result.fetchall()
    return render_template("main.html", olut=olut)

@app.route("/findbeer", methods=["POST"])
def findbeer():
    name = request.form["name"]
    result = beers.find(name)
    if (result):
        session["founded"] = result
        return redirect("/main")
    else:
        if session.get('founded'):
            del session["founded"]
        flash("Hakemaasi olutta ei löydy.")
    return redirect("/main")

#---------------------------------------Beer----------------------------------------------------------
@app.route("/beer")
def beer():
    beer = request.args.get('beer')
    sql = """SELECT name, alcohol_content, types.type, breweries.brewery, countries.country, description FROM beer
            JOIN breweries ON beer.brewery_id = breweries.id JOIN types ON beer.type_id = types.id JOIN countries ON beer.country_id = countries.id WHERE name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    beerdata = result.fetchall()
    sql = """SELECT ratings.created_at, users.username, comment, score FROM ratings JOIN beer ON beer.id = ratings.beer_id JOIN users ON users.id = ratings.user_id WHERE beer.name =:beer"""
    result = db.session.execute(sql, {"beer":beer})
    ratings = result.fetchall()
    return render_template("/beer.html", beerdata=beerdata, ratings = ratings)

    
@app.route("/newbeer")
def newbeer():
    result = db.session.execute("SELECT * FROM types")
    tyyppi = result.fetchall()  
    result = db.session.execute("SELECT * FROM breweries")
    brewery = result.fetchall()
    result = db.session.execute("SELECT * FROM countries")
    country = result.fetchall()
    return render_template("/newbeer.html", tyyppi=tyyppi, brewery=brewery, country=country)

@app.route("/addbeer", methods=["POST"])
def addbeer():
    name = request.form["name"]
    alcohol = request.form["alcohol"]
    beertype = request.form["tyyppi"]
    country = request.form["country"]
    brewery = request.form["panimo"]
    description = request.form["description"]
    if beers.addbeer(name, alcohol, beertype, country, brewery, description): 
        flash("Olut lisätty tietokantaan!")
        return redirect("/newbeer")
    else:
        flash("Oluen lisääminen tietokantaan epäonnistui. Tarkista tiedot.")
        return redirect("/newbeer") 
    return redirect("/main")  

@app.route("/brewery")
def brewery():
    return render_template("/brewery.html")

@app.route("/addbrewery", methods=["POST"])
def addbrecoutyp():
    brewery = request.form["brewery"]
    if beers.addbrewery(brewery): 
        flash("Panimo lisätty tietokantaan!")
    else:
        flash("Lisäys epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/addcountry", methods=["POST"])
def addcountry():    
    country = request.form["country"]
    if beers.addcountry(country): 
        flash("Maa lisätty tietokantaan!")
    else:
        flash("Lisäys epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/addtype", methods=["POST"])
def addtype():    
    beertype = request.form["beertype"]
    if beers.addtype(beertype): 
        flash("Olutlaji lisätty tietokantaan!")
    else:
        flash("Lisäys epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/review")
def review():
    beer = request.args.get('beer')
    sql = """SELECT name, alcohol_content, types.type, breweries.brewery, countries.country, description FROM beer
            JOIN breweries ON beer.brewery_id = breweries.id JOIN types ON beer.type_id = types.id JOIN countries ON beer.country_id = countries.id WHERE name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    beerdata = result.fetchall()
    return render_template("/review.html", beerdata=beerdata)

@app.route("/new_review", methods=["POST"])
def new_review():
    review=request.form["review"]
    score=request.form["score"]
    beer=request.form["beer"]
    username=request.form["username"]
    if beers.addreview(review, score, beer, username):
        return render_template("/beer.html")        
    else:
        flash("Lisäys epäonnistui.")
        return redirect("/review")
    return render_template("/beer.html")

#--------------------------------------------User-----------------------------------------------------
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/main")
    else:
        return redirect("/")
            #return render_template("error.html",message="Väärä tunnus tai salasana")
    #return redirect("/main")

@app.route("/logout")
def logout():
    if session.get('founded'):
            del session["founded"]
    del session["username"]
    return redirect("/")

@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    if users.create_user(username, password):
        session["username"] = username
        return redirect("/")
    else:
        flash("Käyttäjän lisääminen epäonnistui.")
        return redirect("/new_user")
 

