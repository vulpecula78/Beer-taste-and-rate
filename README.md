# Beer-taste-and-rate

### Aineopintojen harjoitustyö: Tietokantasovellus

### Olut arvosteluja: Maista ja kerro mielipiteesi

Tällä sovelluksella käyttäjät voivat pisteyttää ja antaa mielipiteensä oluista, sekä tarkastella muiden antamia arvosteluja. Tietokannasta voi hakea oluita nimen perusteella, sekä rajata hakua maittain tai oluttyypin mukaan. Sovellus näyttää myös viimeisimmät lisäykset, sekä parhaan pisteiden keskiarvon omaavat oluet.

Käyttäjät voivat arvostella oluen numeerisesti arvosana-asteikolla 1 - 10, sekä kirjoittaa lyhyen kommentin oluesta. Oluen arvosana muodostuu kaikkien kyseisen oluen arvosanojen keskiarvosta. Kaikki oluen saamat arvostelut ovat luettavissa.

Käyttäjätasoja on kolme: admin, käyttäjä ja vieras. Admin voi täysin hallinnoida tietokantaa: Poistamalla käyttäjiä, kommentteja, oluita, panimoita, valmistusmaita, sekä tarvittaessa moderoida kommentteja. Käyttäjä voi pisteytyksen ja arvostelun lisäksi myös tarvittaessa muokata omaa arvostelua, sekä lisätä tietokantaan oluen. Vieraalla on vain oikeus selata oluita ja niiden arvosteluja.


  Sovelluksen testaaminen:

   Sovellus löytyy osoitteesta https://tsoha-beerrate.herokuapp.com/ 
   
   Sovellukseen voi kirjautua käyttäjätunnuksilla:
   * Testaaja, salasana: testaaja
   * pääkäyttäjänä Admin, salasana: password
   * Sovellusta voi myös testata luomalla uusi käyttäjä.


Kehitettäviä asioita ovat:
 * sovelluksen ulkoasu 
 * viestien lähettäminen ylläpidolle
 * käyttäjä asetukset, kuten salasanan vaihto.
 * Keskustelupalsta
