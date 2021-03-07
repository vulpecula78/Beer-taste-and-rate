from app import app
from flask import render_template, request, redirect, session, flash
from db import db
import beers, users, admins

#---------------------------------------Main----------------------------------------------------------
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/main")
def main():
    bests = beers.best()
    olut = beers.latest()
    result = db.session.execute("SELECT * FROM countries")
    country = result.fetchall()
    result = db.session.execute("SELECT * FROM types")
    types = result.fetchall()
    return render_template("main.html", olut = olut, bests = bests, country = country, types = types)

@app.route("/findbeer", methods=["POST"])
def findbeer():
    name = request.form["name"]
    country = request.form["country"]
    types = request.form["types"]
    search = beers.find(name, country, types)
    if (search):
        olut = beers.latest()
        bests = beers.best()
        result = db.session.execute("SELECT * FROM countries")
        country = result.fetchall()
        result = db.session.execute("SELECT * FROM types")
        types = result.fetchall()
        session["founded"] = True 
        return render_template("/main.html", search = search, olut = olut, bests = bests, country = country, types = types)
    else:
        if session.get('founded'):
            del session["founded"]
        flash("Haku ei palauttanut yhtään tulosta.")
    return redirect("/main")
#---------------------------------------Admin----------------------------------------------------------
@app.route("/admins", methods=["POST"])
def admin():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    result = db.session.execute("SELECT * FROM countries")
    country = result.fetchall()
    result = db.session.execute("SELECT * FROM types")
    types = result.fetchall()
    result = db.session.execute("SELECT * FROM breweries")
    brewery = result.fetchall()
    result = db.session.execute("SELECT * FROM users")
    users = result.fetchall()
    result = db.session.execute("SELECT * FROM beer")
    beers = result.fetchall()
    return render_template("/admins.html", country = country, types = types, brewery = brewery, users = users, beers = beers)

@app.route("/rm_country", methods=["POST"])
def rm_country():
    country = request.form["country"]
    if admins.rm_country(country):
        flash("Maa poistettu tietokannasta")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa maata tietokannasta!")
        return redirect("/admins")

@app.route("/rm_type", methods=["POST"])
def rm_type():
    types = request.form["types"]
    if admins.rm_type(types):
        flash("Oluttyyppi poistettu tietokannasta")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa oluttyyppiä tietokannasta!")
        return redirect("/admins")
    
@app.route("/rm_brewery", methods=["POST"])
def rm_brewery():
    brewery = request.form["brewery"]
    if admins.rm_brewery(brewery):
        flash("Panimo poistettu tietokannasta")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa panimoa tietokannasta!")
        return redirect("/admins")
    
@app.route("/rm_user", methods=["POST"])
def rm_user():
    user = request.form["user"]
    if admins.rm_user(user):
        flash("Käyttäjä poistettu tietokannasta")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa käyttäjää tietokannasta!")
        return redirect("/admins")
    
@app.route("/rm_beer", methods=["POST"])
def rm_beer():
    beer = request.form["beer"]
    if admins.rm_beer(beer):
        flash("Olut poistettu tietokannasta")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa olutta tietokannasta!")
        return redirect("/admins")
    
@app.route("/rm_comment", methods=["POST"])
def rm_comment():
    id = request.form["ratings_id"]
    if admins.rm_comment(id):
        flash("Kommentti poistettu")
        return redirect("/admins")
    else:
        flash("Virhe poistettaessa kommenttia tietokannasta!")
        return redirect("/admins")
    
@app.route("/list_ratings", methods=["POST"])
def list_ratings():
    name = request.form["name"]
    ratings = admins.list_ratings(name)
    result = db.session.execute("SELECT * FROM countries")
    country = result.fetchall()
    result = db.session.execute("SELECT * FROM types")
    types = result.fetchall()
    result = db.session.execute("SELECT * FROM breweries")
    brewery = result.fetchall()
    result = db.session.execute("SELECT * FROM users")
    users = result.fetchall()
    result = db.session.execute("SELECT * FROM beer")
    beers = result.fetchall()
    if (ratings):
        session["ratings"] = True
        return render_template("/admins.html", ratings = ratings, country = country, types = types, brewery = brewery, users = users, beers = beers)
    else:
        if session.get('founded'):
            del session["founded"]
        flash("Haku ei palauttanut yhtään tulosta.")
        return redirect("/admins")
    
#---------------------------------------Beer----------------------------------------------------------
@app.route("/beer/<beer>")
def beer(beer):
    sql = """SELECT name, alcohol_content, types.type, breweries.brewery, countries.country, description FROM beer
            JOIN breweries ON beer.brewery_id = breweries.id JOIN types ON beer.type_id = types.id JOIN countries ON beer.country_id = countries.id WHERE name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    beerdata = result.fetchall()
    sql = """SELECT users.username, score,  comment, TO_CHAR(ratings.created_at, 'DD-MM-YYYY HH24:MI') FROM ratings JOIN beer ON beer.id = ratings.beer_id JOIN users ON users.id = ratings.user_id WHERE beer.name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    ratings = result.fetchall()
    sql = "SELECT AVG(score)::numeric(10,2) FROM ratings JOIN beer ON beer.id = beer_id WHERE beer.name=:beer GROUP BY beer.name"
    result = db.session.execute(sql, {"beer":beer})
    avgscore = result.fetchone()
    return render_template("/beer.html", beerdata = beerdata, ratings = ratings, avgscore = avgscore)
    
@app.route("/newbeer")
def newbeer():
    result = db.session.execute("SELECT * FROM types")
    tyyppi = result.fetchall()  
    result = db.session.execute("SELECT * FROM breweries")
    brewery = result.fetchall()
    result = db.session.execute("SELECT * FROM countries")
    country = result.fetchall()
    return render_template("/newbeer.html", tyyppi = tyyppi, brewery = brewery, country = country)

@app.route("/addbeer", methods=["POST"])
def addbeer():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
        flash("Panimon lisääminen tietokantaan epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/addcountry", methods=["POST"])
def addcountry():    
    country = request.form["country"]
    if beers.addcountry(country): 
        flash("Maa lisätty tietokantaan!")
    else:
        flash("Maan lisääminen tietokantaan epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/addtype", methods=["POST"])
def addtype():    
    beertype = request.form["beertype"]
    if beers.addtype(beertype): 
        flash("Oluttyyppi lisätty tietokantaan!")
    else:
        flash("Olutttyypin lisääminen tietokantaan epäonnistui.")
        return redirect("/brewery")
    return redirect("/brewery")

@app.route("/review/<beer>")
def review(beer):
    sql = """SELECT name, alcohol_content, types.type, breweries.brewery, countries.country, description FROM beer
            JOIN breweries ON beer.brewery_id = breweries.id JOIN types ON beer.type_id = types.id JOIN countries ON beer.country_id = countries.id WHERE name=:beer"""
    result = db.session.execute(sql, {"beer":beer})
    beerdata = result.fetchall()
    return render_template("/review.html", beerdata=beerdata)

@app.route("/new_review", methods=["POST"])
def new_review():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    review = request.form["review"]
    score = request.form["score"]
    beer = request.form["beer"]
    username = request.form["username"]
    if beers.addreview(review, score, beer, username):
        return redirect("/beer/"+beer)        
    else:
        flash("Arvostelun lisäämisessä tapahtui virhe.")
        return redirect("/review/"+beer)
    return render_template("/beer.html")

#--------------------------------------------User-----------------------------------------------------
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/main")
    else:
        flash("Käyttäjätunnus tai salasana ei kelpaa!!!")
        return redirect("/")

@app.route("/logout")
def logout():
    if session.get('founded'):
            del session["founded"]
    del session["csrf_token"]
    del session["username"]
    return redirect("/")

@app.route("/new_user")
def new_user():
    return render_template("new_user.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    if len(username) < 2:
        flash("Ei kelvollinen käyttäjänimi")
        return redirect("/new_user")
    if len(password) < 6:
        flash("Liian lyhyt salasana.")
        return redirect("/new_user")
    if users.create_user(username, password):
        session["username"] = username
        return redirect("/")
    else:
        flash("Käyttäjän lisääminen epäonnistui.")
        return redirect("/new_user")
 

