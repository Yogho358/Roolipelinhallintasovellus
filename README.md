# Roolipelinhallintasovellus

Sovellus, joka auttaa roolipelin hallinnointia. Kyseessä on taisteluroolipeli, jossa ensin valitaan hahmon käyttämä ase. Kaikki hahmot osaavat kaikkien aseiden perushyökkäyksen, ja hahmon kehittyessä se oppii uusia erikoishyökkäyksiä käyttämälleen aseelle. Eli hahmon opittavissa olevat kyvyt riippuvat käytetystä aseesta, ja jos hahmo on saanut kokemusta useammasta aseesta, sillä voi olla useita taitopuita. Lisäksi peli ottaa huomioon, millaisella areenalla taistelu käydään, ja miten eri aseet ja taidot soveltuvat erilaisille areenoille.

Sovellus tallettaa tietokantaan pelaajahahmoja, vihollisia, aseita, taitoja ja areenoita, ja niiden välisiä suhteita. Tietokantaan pitäisi olla helppoa tallettaa tietoa ja löytää eri tilanteisiin relevanttia tietoa. Sovelluksella on kaksi käyyäjäroolia, pelaaja ja pelinjohtaja.

Pelaaja voi:

* Luoda hahmon
* Vaihtaa asetta
* Tasonnousun yhteydessä valita uuden taidon aseelle
* Etsiä olemassa olevia aseita ja taitoja

Pelinjohtaja voi:

* Luoda vihollisia, aseita, taitoja ja areenoita
* Luoda taistelutilanteita yhdistelemällä pelihahmoja, vihollisia ja areenoita, jolloin hän saa tietoja kuinka areena vaikuttaa pelihahmojen aseisiin ja taitoihin

# Loppupalautus

Sovellus on edelleen osoitteessa https://powerful-cliffs-38993.herokuapp.com/.

Sovellus nykykunnossaan jokseenkin vastaa suunnitelmaa, paitsi ajanpuutteen takia taitosysteemiä ei ole tehty, ja taisteluyhteenveto ei ole viimeistelty. Molemmat asiat saisi suhteellisen pienellä vaivalla toteutettua, tulisivat käyttämään samoja tekniikoita mitä sovelluksessa on jo nyt, eikä mitään uusia tapoja käyttää tietokantaa yms. tarvittaisi.

# Käyttöohje

Sovellusta ei voi käyttää rekisteröitymättä ja kirjautumatta sisään. Kirjautumisen jälkeen käyttäjt voivat luoda hahmoja ja muokata niiden ominaisuuksia. Pelaajan roolissa olevilla käyttäjillä ei ole juuri muuta tekemistä kuin seurata ja muokata omia hahmojaan, ja liittyä peleihin. Hahmo voi olla liittynyt vain yhteen peliin. Peliin liittyäkseen jonkun on ensin luotava sellainen. Kaikki käyttäjät voivat luoda pelejä. Pelin luoja johtaa peliä, ja hän voi päättää, millaisia aseita ja vihollisia pelissä on. Pelaajat eivät voi vaihtaa asetta ennnenkuin ovat pelissä, koska uuden aseen voi valita vain aseista, jotka pelinjohtaja on liittänyt peliin.

Aseita lisätään peliin listalta, jossa on kaikki sovelluksessa olevat aseet. Pelinjohtosivulla voi luoda uusia aseita, jotka sitten voi liittää peliinsä, ja myös muut pelinjohtajat voivat liittää omiin peleihinsä.

Vihollisia luodaan siten, että ensin pelinjohtosivulla luodaan vihollistyyppi. Sitten kun tyyppi valitaan liitettäväksi peliin, sovellus luo tietokantaan uuden tyyppiä edustavan hahmon, jota pelinjohtaja sitten voi muokata. Pelinjohtajat voivat lisätä hahmoja kaikista tyypeistä, jotka joku peelinjohtaja on luonut.

Kun pelissä on pelaajahahmoja, vihollisia ja toivottavasti kaikille aseita, pelinjohtaja voi luoda taistelun valitsemalla osallisiksi kaikki siihen osallistuvat hahmot, ja näkee siitä yhteenvedon. Itse peliä sitten olisi tarkoitus pelata esim. nopilla, ja pelaajat sitten pitäisivät sovelluksen avulla kirjaa hahmoistaan ja pelinjohtaja vihollisistaan.


# Välipalautus 1

Sovellus on osoitteessa https://powerful-cliffs-38993.herokuapp.com/

Sovellusta käyttääkseen on pakko kirjautua sisään, ja tarkoituksena on, että minkä tahansa yrittäminen ilman sisäänkirjautumista ohjaa käyttäjän login-sivulle. Sovelluksessa on nyt valmiina kaksi käyttäjää, käyttäjänimet testman ja test, molempien salasana on test. Uusia käyttäjiä voi rekisteröidä vapaasti.

### Nykytilanne

Käyttäjät voivat luoda hahmoja ja tarkastella niiden tietoja, mutta tietoja ei voi vielä muuttaa eikä hahmolla tehdä mitään. Jokainen käyttäjä voi luoda pelejä, joiden pelinjohtajaksi hän tulee, ja nähdä listan olemassaolevista peleistä, joihin hän voi liittyä pelaajaksi, tai jättää pelin.

Ulkoasun toteutus on sen verran alkutekijöissään, että lähes kaikki on hajautettu omille sivuilleen eikä mitään järkevää navigoimista voi tehdä. Virheellisistä syötteistä yms. ei vielä tule käyttäjälle hyvää viestiä, mutta olemassaolevien toimintojen toimivuus ja turvallisuus on otettu huomioon, paitsi tekstisyötteiden tarkastusta ei vielä ole.

# Välipalautus 2

Lue ensin edellisen palautuksen ohjeet, ne pätevät edelleen.

Käyttäjät voivat luoda hahmoja ja tarkastella niiden tietoja, mutta tietoja ei voi vielä muuttaa eikä hahmolla tehdä mitään. Jokainen käyttäjä voi luoda pelejä, joiden pelinjohtajaksi hän tulee, ja nähdä listan olemassaolevista peleistä, joihin hän voi liittyä pelaajaksi, tai jättää pelin. 

Pelinjohtaja voi hallinnoida luomaansa peliä liittämällä siihen jo tietokannassa olevia aseita. Aseita voi myös luoda lisää. Aseen luominen lisää aseen tietokantaan, josta se on kaikkien pelinjohtajien valittavissa omaan peliinsä, ja myös luojan täytyy muistaa liittää vasta luomansa ase omaan peliinsä.

Pelaajat voivat liittää omia hahmojaan peliin pelin sivulta. Uusia hahmoja luodaan hahmot-sivulta. Kun hahmo on liitetty peliin, sille voi valita uuden aseen pelinjohtajan peliin liittämistä aseista.

Ulkoasua ja käytettävyyttä on paranneltu vähän, huomattavimpana navigointipalkin lisääminen.

# TODO

Syötekenttien validointi ja virheellisistä sytötteistä raportointi käyttäjälle.

Pelinjohtaja voi luoda ja liittää peliin npc-hahmoja samalla tavalla kuin aseita.

Pelinjohtaja voi luoda ja liittää peliin taitoja samalla tavalla kuin aseita.

Hahmoille voi antaa taitoja, ja niiden muitakin ominaisuuksia voi muokata tasonnousun yms. yhteydessä.

Pelinjohtaja voi luoda taistelun, johon hän voi liittää pelissä olevia pelaaja- ja npc-hahmoja, ja ominaisuuksia kuten taistelualueen koko. Taistelunäkymä sitten näyttää esim. kuinka helppoa hahmon on osua muihin hahmoihin taitojen, ominaisuuksie, aseide, areenana yms. perusteella ja paljonko vahinkoa se voi tehdä.

Parempi ulkoasu.
