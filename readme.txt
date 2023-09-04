Tämä projekti perustuu yliopiston peruskurssilla lisätehtävänä palauttamaani
graafiseen käyttöliittymään, johon sain idean toteuttaa shakkipelin
Tkinter-kirjaston napeilla. Kurssilla palauttamassani versiossa graafinen
osuus oli yhdistetty pelin teoreettiseen pyörittämiseen, mutta päätin
myöhemmin erotella ne toisistaan. Teoreettinen osuus on nyt tiedostossa
"teorialauta.py" ja käyttöliittymä "shakki_gui.py".

Koneoppimisesta kiinnostuneena halusin tuoda mukaan jonkinlaisen
shakkikoneen ja lähdinkin kehittelemään tapaa kouluttaa sellaista.
Onnistuin tekemään alkeellisen evolutiivisen tekoälyn, mutta ilman
tehostavia algoritmeja kehittyminen ja toiminta on heikkoa. Koulutus on
toteutettu tiedostossa "koulutus.py". Tiedosto "paras.txt" sisältää koulutetun
version datan ja "haastaja.txt" on koulutuksessa testattavia muutoksia varten.

Projekti on (kenties ikuisesti) keskeneräinen, sen graafiset elementit ovat
alkeellisia eivätkä käyttäydy täysin toivotulla tavalla. Tulevana tavoitteena
tälle projektille on kuitenkin algoritmillinen parantelu ja sen jälkeen
jonkinlainen syväoppimisen implementaatio.

Versiohistoria ennen versiohallinnan implementaatiota:
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.1 GUI yhdistettynä teorialautaan (palautettu ohjelmoinnin peruskurssille).
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.2 Alkuperäisen GUI-luokan attribuutit ja metodit erotettuina kahteen
    luokkaan (Shakkilauta ja Teorialauta), joilla omat tiedostot
    ("shakki_gui.py" ja "teorialauta.py").
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.3 Lisätty, muokattu ja poistettu metodeja Shakkilaudalta vastaamaan uutta
    suunnitelmaa. Mahdollistettu matin tarkistelua varten rekursiivinen
    ohjelmointi, jossa Shakkilauta voi muodostaa uusia Shakkilautoja
    (saattaa olla myöhemmin hyötyä shakkikoneen toteuttamisessa).
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.4 Lisätty, muokattu ja poistettu metodeja ShakkiGUI:lta vastaamaan uutta
    suunnitelmaa sekä Shakkilaudan uutta toimintaa.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.5 Lisätty yksinpeli: Hyvin alkeellinen shakkikone, joka harkitsee tulevan
    siirron arvoa materiaalieron perusteella.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.6 Lisätty koulutustiedosto, jossa on alkeellinen evolutiivisen tekoälyn
    implementaatio.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.7 Optimoitu, kaunisteltu, kommentoitu ja lisätty versionhallintaan.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(0.8?) Hakualgoritmien ja tekoälyn koulutusalgoritmin optimointi.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(0.9?) Syväoppimisen implementaatio.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(1.0?) Graafinen käyttöliittymä ja ulkoasu on hiottu lopulliseen muotoonsa.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -