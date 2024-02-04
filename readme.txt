OHJE KÄYTTÖÖN
-------------------------------------------------------------------------------
Tallentamalla tiedostot samaan kansioon ja ajamalla shakki_gui.py voit testata
shakin ja shakkikoneen toimintaa. Ajamalla koulutus.py voi seurata, kuinka
koulutus pyörii. Nopeuden ei kuulukaan olla näillä toteutusmetodeilla päätä
huimaava.
-------------------------------------------------------------------------------
PROJEKTISTA
-------------------------------------------------------------------------------
Tämä shakkiprojekti koostuu kolmesta rajapinnasta:
- teorialauta
- graafinen käyttöliittymä
- shakkikoneen koulutus

Teorialauta ja graafinen käyttöliittymä on eroteltu alkuperäisestä ohjelmasta,
joka oli graafisen käyttöliittymän lisätehtävänä yliopistokurssilla.
Myöhemmin lähdin kehittelemään shakkikonetta ja yksinpelimahdollisuutta
tavoitteenani ymmärtää koneoppimista paremmin käytännössä, minkä takia olen
vältellyt tyypillisiä koneoppimiskirjastoja.

Kehitys on ollut epälineaarista, eikä alkuperäistä ohjelmaa
tehty  versionhallintaan, joten olen pitänyt vain karkeaa versiohistoriaa.
-------------------------------------------------------------------------------
VERSIOHISTORIA
-------------------------------------------------------------------------------
1.0 Graafisena käyttöliittymänä toteutettu shakkipeli.
-------------------------------------------------------------------------------
1.1 Teorialauta ja graafinen käyttöliittymä eroteltuina,
    muutamia muita laadullisia parannnuksia.
-------------------------------------------------------------------------------
1.2 Lisättynä koulutuksen hahmotelma, joka evolutiivisesti kehittää painotuksia
    pistämällä kahdet painotukset vastakkain, voittaja selviytyy
    ja häviäjää muutetaan. Julkaistu GitHubissa.
-------------------------------------------------------------------------------
1.3 Poistettu GitHubista. Koulutuksen tehokkuutta parannettu muuttamalla
    tietorakenteet käyttämään koordinaattien sijaan bittilautoja ja muita
    algoritmisia parannuksia.
-------------------------------------------------------------------------------
1.4 Koulutusmalli muutettu, nyt kone pelaa peliä itseään vastaan ja vertaa
    lopputulosta pelin aikana tehtyihin arvioihin. Lasketun virheen avulla
    muutetaan painotuksia (weight) ja vinoumia (bias).
    Julkaistu uudelleen GitHubissa.
-------------------------------------------------------------------------------
(1.5?) Syväoppimista tms. kehittyneempiä koneoppimisen malleja.
-------------------------------------------------------------------------------
(2.0?) Graafinen käyttöliittymä hiottu loppuun, teorialaudan toiminta
       optimoitu, koneoppimisen algoritmeissa ja yksinpelissä saavutettu
       riittävä sulavuus.
-------------------------------------------------------------------------------