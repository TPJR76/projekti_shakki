"""
Tässä tiedostossa on pohja shakkikoneen kouluttamiselle. Nykyinen
toiminta kehittää algoritmin painotuksia ja vinoumia automaattisesti
neliöidyn virheen sekä määritetyn oppimisnopeuden avulla.
"""

from teorialauta import Teorialauta
from random import randint
import time

# Globaaleina vakioina koulutuksen parametreja
PELIEN_MAKSIMI = 100
# Laatu paranee, jos arvioinnissa pystytään ennustamaan tulevia asemia
ARVIOINNIN_MAKSIMISYVYYS = 3
OPPIMISNOPEUS = 0.1


def muuttujat_tiedostosta(tiedostonimi):
    """
    Tämä funktio kerää painotukset ja vinoumat tiedoston ensimmäiseltä riviltä.

    :param tiedostonimi: str, tiedoston nimi, josta painotukset etsitään.
    :return: [float, ...], [float, ...], painotukset ja vinoumat.
    """

    painotukset = []
    vinoumat = []

    with open(tiedostonimi, "r") as tiedosto:
        for tiedoston_rivi in tiedosto:
            if not tiedoston_rivi:
                return None

            indeksi = 0
            for luku in tiedoston_rivi.rstrip().split(";"):
                if not luku:
                    return painotukset, vinoumat
                if indeksi < 5:
                    painotukset.append(float(luku))
                else:
                    vinoumat.append(float(luku))
                indeksi += 1

    return None


def muodosta_ruudun_arvo(pelilauta, ruutu, muuttujat):
    """
    Tämä funktio muodostaa yhden ruudun arvon. Tässä versiossa se ottaa
    huomioon nappulan arvon, nappulan etäisyyden keskustasta, nappulan
    siirtomahdollisuudet, ruutua uhkaavat nappulat, ruutua puolustavat
    nappulat sekä onko kuningas shakissa.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param ruutu: str, pelilaudan koordinaatti.
    :param muuttujat: [float, ...], [float, ...]; listat painotuksista ja
                      vinoumista.
    :return: int/float, yhden ruudun arvo pelitilanteessa.
    """

    asemat = pelilauta.asemat()

    # Nappulan arvo ja etäisyys
    nappuloiden_arvot = [1, 5, 3, 3, 9, 0, -1, -5, -3, -3, -9, 0]

    nappulan_arvo = 0
    nappulan_etaisyys = 0
    nappulan_siirtomahdollisuudet = 0
    shakissa = 0

    for i in range(0, 13):
        if i == 12:
            break

        if asemat[i] >> ruutu & 1 == 1:
            nappulan_arvo = nappuloiden_arvot[i]

            puoli, _, siirrot = pelilauta.ruudun_nappulan_tiedot(ruutu)
            nappulan_siirtomahdollisuudet = 0

            # Lasketaan nappulan etäisyys keskustasta (lyhyin Manhattanin
            # etäisyys kohderuudun ja neljän keskimmäisen ruudun välillä)
            if puoli == "White":
                nappulan_etaisyys = -min(
                    abs(ruutu % 8 - 27 % 8) + abs(ruutu // 8 - 27 // 8),
                    abs(ruutu % 8 - 28 % 8) + abs(ruutu // 8 - 28 // 8),
                    abs(ruutu % 8 - 35 % 8) + abs(ruutu // 8 - 35 // 8),
                    abs(ruutu % 8 - 36 % 8) + abs(ruutu // 8 - 36 // 8))

                while siirrot:
                    siirrot &= (siirrot-1)
                    nappulan_siirtomahdollisuudet += 1
            else:
                nappulan_etaisyys = min(
                    abs(ruutu % 8 - 27 % 8) + abs(ruutu // 8 - 27 // 8),
                    abs(ruutu % 8 - 28 % 8) + abs(ruutu // 8 - 28 // 8),
                    abs(ruutu % 8 - 35 % 8) + abs(ruutu // 8 - 35 // 8),
                    abs(ruutu % 8 - 36 % 8) + abs(ruutu // 8 - 36 // 8))

                while siirrot:
                    siirrot &= (siirrot-1)
                    nappulan_siirtomahdollisuudet -= 1

            break

    # Ruudun uhkaajat
    valkoisen_siirrot = pelilauta.puolen_kaikki_siirrot("valkoinen")
    mustan_siirrot = pelilauta.puolen_kaikki_siirrot("musta")

    ruudun_uhkaajat = 0
    for avain in valkoisen_siirrot:
        if valkoisen_siirrot[avain] >> ruutu & 1:
            if asemat[11] >> ruutu & 1:
                shakissa = 1

            ruudun_uhkaajat += 1

    for avain in mustan_siirrot:
        if mustan_siirrot[avain] >> ruutu & 1:
            if asemat[5] >> ruutu & 1:
                shakissa = -1

            ruudun_uhkaajat -= 1

    w1, w2, w3, w4, w5 = muuttujat[0]
    b1, b2, b3, b4, b5 = muuttujat[1]

    return (w1*nappulan_arvo+b1 + w2*nappulan_etaisyys+b2
            + w3*nappulan_siirtomahdollisuudet+b3 + w4*ruudun_uhkaajat+b4
            + w5*shakissa+b5)


def muodosta_pelitilanteen_arvo(pelilauta, muuttujat, rekursio=True):
    """
    Tämä funktio muodostaa pelitilanteen arvon yksittäisten ruutujen
    perusteella. Jos rekursio on sallittuna, funktio voi arvioida nykyistä
    asemaa seuraavien tilanteiden perusteella.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param muuttujat: [float, ...], [float, ...]; listat painotuksista ja
                      vinoumista.
    :param rekursio: bool, sallitaanko arvon muodostuksen rekursio.
    :return: int/float, pelitilanteen arvo lukuna.
    """

    voittaja = pelilauta.voittaja()
    if voittaja == "valkoinen":
        return 1

    if voittaja == "musta":
        return -1

    arvo = 0
    for indeksi in range(0, 64):
        arvo += muodosta_ruudun_arvo(pelilauta, indeksi, muuttujat)

    if rekursio:
        uusi_arvo = 0

        for _ in range(0, ARVIOINNIN_MAKSIMISYVYYS):
            uusi_lauta = Teorialauta(pelilauta.siirtonumero(),
                                     pelilauta.asemat(),
                                     pelilauta.liikkumistiedot())

            if uusi_lauta.siirtonumero() % 2 == 1:
                sijainti, siirto, uusi_arvo = arvioi_paras_siirto(
                    uusi_lauta, "valkoinen", muuttujat, False)

            else:
                sijainti, siirto, uusi_arvo = arvioi_paras_siirto(
                    uusi_lauta, "musta", muuttujat, False)

            uusi_lauta.tee_siirto(sijainti, siirto)
            if uusi_lauta.voittaja() is not None:
                break

        arvo += 0.5 * uusi_arvo

    # Vältetään arvon menemästä yli rajan kaikissa tilanteissa
    if arvo >= 1:
        return 0.99999

    if arvo <= -1:
        return -0.99999

    return round(arvo, 5)


def arvioi_paras_siirto(pelilauta, puoli, muuttujat, rekursio=True):
    """
    Tämä funktio etsii parhaan siirron tulevan pelitilanteen arvojen
    perusteella. Jos sitä ei löydy, muodostaa uuden arvon.
    Tallentaa tulevat arvot huomioiden lasketut arvot tiedostoon.
    Tämän ominaisuuden avulla myös pelaajien pelaamien otteluiden
    tilanteet voidaan tallentaa.

    :param pelilauta: Teorialauta, pelitilanne, josta parasta siirtoa etsitään.
    :param puoli: str, puoli, jolla siirtäjä on.
    :param muuttujat: [float, ...], [float, ...]; listat painotuksista ja
                       vinoumista.
    :param rekursio: bool, sallitaanko arvon muodostuksen rekursio.
    :return: int, int, float / None, None, None; ruudut, josta lähdetään ja
             johon siirrytään sekä siirron arvo.
    """

    siirrot = pelilauta.puolen_kaikki_siirrot(puoli)
    parhaat_siirrot = []

    if puoli == "valkoinen":
        paras_arvo = -1
    else:
        paras_arvo = 1

    siirtonumero = pelilauta.siirtonumero()
    asemat = pelilauta.asemat()
    liikkumistiedot = pelilauta.liikkumistiedot()

    for asema in siirrot:
        indeksi = 0

        while siirrot[asema]:
            if siirrot[asema] & 1:
                uusi_lauta = Teorialauta(siirtonumero, asemat,
                                         liikkumistiedot)

                uusi_lauta.tee_siirto(asema, indeksi)

                arvo = muodosta_pelitilanteen_arvo(
                    uusi_lauta, muuttujat, rekursio)

                if puoli == "valkoinen" and arvo > paras_arvo:
                    parhaat_siirrot = [[asema, indeksi, arvo]]
                    paras_arvo = arvo

                if puoli == "musta" and arvo < paras_arvo:
                    parhaat_siirrot = [[asema, indeksi, arvo]]
                    paras_arvo = arvo

                if arvo == paras_arvo:
                    parhaat_siirrot.append([asema, indeksi, arvo])

            siirrot[asema] >>= 1
            indeksi += 1

    if not parhaat_siirrot:
        return None, None, None

    if len(parhaat_siirrot) == 1:
        return (parhaat_siirrot[0][0], parhaat_siirrot[0][1],
                parhaat_siirrot[0][2])

    satunnainen_indeksi = randint(0, len(parhaat_siirrot)-1)

    return parhaat_siirrot[satunnainen_indeksi][0], \
        parhaat_siirrot[satunnainen_indeksi][1], \
        parhaat_siirrot[satunnainen_indeksi][2]


def alusta_muuttujat(tiedostonimi):
    """
    Tämä funktio alustaa muuttujille satunnaiset arvot tiedostoon.

    :param tiedostonimi: str, tiedosto, johon muuttujat tallennetaan.
    """

    rivi = ""
    for _ in range(0, 10):
        rivi += "{:.5f};".format(randint(-100, 100)*0.00001)

    with open(tiedostonimi, "w") as tiedosto:
        tiedosto.write(rivi)

    return


def keskiarvo_nelio_virhe(y, y_arvioidut):
    """
    Tämä funktio laskee ja palauttaa neliöityjen virheiden keskiarvon.

    :param y: int, tavoitearvo.
    :param y_arvioidut: [float, ...], lista muodostetuista arvioista.
    :return: float, neliöidyn virheen keskiarvo.
    """

    summa = 0
    for y_arvioitu in y_arvioidut:
        summa += (y-y_arvioitu)**2

    return summa/len(y_arvioidut)


def koulutus():
    """
    Tämä funktio vastaa shakkikoneen varsinaisesta kouluttamisesta.
    Pyörittää teoreettista shakkipeliä itseään vastaan, ja vertaa ottelun
    tulosta matkan varrella muodostettuihin ennusteisiin.
    """

    tiedostonimi = "tulokset.txt"
    pelinumero = 1
    suunta = 1

    edellinen_virhe = 4

    while True:

        if pelinumero == PELIEN_MAKSIMI:
            print("Koulutus päättyi.")
            break

        print(pelinumero, ". peli", sep="")

        pelilauta = Teorialauta()
        ennustukset = []

        muuttujat = muuttujat_tiedostosta(tiedostonimi)

        # Jos tiedosto oli tyhjä, alustetaan uudet muuttujat
        if not muuttujat:
            alusta_muuttujat(tiedostonimi)
            muuttujat = muuttujat_tiedostosta(tiedostonimi)

        aloitusaika = time.time()

        # Tehdään siirtoja niin kauan, kuin peli on käynnissä
        while True:
            siirtonumero = pelilauta.siirtonumero()
            # print(siirtonumero)

            # Rajoitetaan pelin pituus sataan siirtoon
            if siirtonumero == 100:
                print("Tasapeli.")
                break

            # Arvioidaan vuorossa olevalle puolelle paras siirto
            if siirtonumero % 2 == 1:
                sijainti, siirto, arvo = arvioi_paras_siirto(
                    pelilauta, "valkoinen", muuttujat, False)
            else:
                sijainti, siirto, arvo = arvioi_paras_siirto(
                    pelilauta, "musta", muuttujat, False)

            # Toteutetaan paras siirto
            pelilauta.tee_siirto(sijainti, siirto)

            # Lisätään ennustuksiin tuore ennustus
            ennustukset.append(arvo)

            # Tarkistetaan, johtiko siirto voittoon
            voittaja = pelilauta.voittaja()
            if voittaja:

                if voittaja == "valkoinen":
                    virhe = keskiarvo_nelio_virhe(1, ennustukset)

                else:
                    virhe = keskiarvo_nelio_virhe(-1, ennustukset)

                suoritusaika = time.time() - aloitusaika

                # Tulostetaan ottelun tietoja
                print("Voittaja:", voittaja)
                print("Siirtoja:", siirtonumero)
                print("Suoritusaika:", suoritusaika, "s")
                print("Suoritusaika per siirto:", suoritusaika/siirtonumero,
                      "s/siirto")
                print("Virhe:", virhe)

                # Yksinkertainen ja jokseenkin tehoton tapa päivittää
                # painot ja vinoumat neliöidyn virheen keskiarvon avulla
                # TÄYTYY VIELÄ KEHITTÄÄ
                for i in range(0, 5):

                    # Jos virhe on kasvanut, vaihdetaan muutosten suuntaa
                    if virhe > edellinen_virhe:
                        if suunta == 1:
                            suunta = -1
                        else:
                            suunta = 1

                    muuttujat[0][i] += (suunta * OPPIMISNOPEUS
                                        * muuttujat[0][i] * virhe)

                    # muuttujan ei ole tarkoitus supeta nollaan
                    if muuttujat[0][i] > -0.00005:
                        if muuttujat[0][i] < -0.00001:
                            muuttujat[0][i] = -muuttujat[0][i]

                        elif muuttujat[0][i] <= 0:
                            muuttujat[0][i] = 0.00005

                        elif muuttujat[0][i] < 0.00001:
                            muuttujat[0][i] = -0.00005

                        elif muuttujat[0][i] < 0.00005:
                            muuttujat[0][i] = -muuttujat[0][i]

                    # jos virhe on yli 1, arviointi suosii liikaa jompaa
                    # kumpaa puolta, mitä voi kontrolloida vinoumilla
                    if virhe > 1:
                        if (voittaja == "valkoinen" and muuttujat[1][i] >= 0) \
                                or (voittaja == "musta" and muuttujat[1][i]
                                    < 0):
                            muuttujat[1][i] += (OPPIMISNOPEUS
                                                * muuttujat[1][i] * virhe)

                        if (voittaja == "musta" and muuttujat[1][i] >= 0) \
                                or (voittaja == "valkoinen" and muuttujat[1][i]
                                    < 0):
                            muuttujat[1][i] -= (OPPIMISNOPEUS
                                                * muuttujat[1][i] * virhe)

                        # muuttujan ei ole tarkoitus supeta nollaan
                        if muuttujat[1][i] > -0.00005:
                            if muuttujat[1][i] < -0.00001:
                                muuttujat[1][i] = -muuttujat[1][i]

                            elif muuttujat[1][i] <= 0:
                                muuttujat[1][i] = 0.00005

                            elif muuttujat[1][i] < 0.00001:
                                muuttujat[1][i] = -0.00005

                            elif muuttujat[1][i] < 0.00005:
                                muuttujat[1][i] = -muuttujat[1][i]

                edellinen_virhe = virhe

                rivi = ""
                for muuttuja in (muuttujat[0]+muuttujat[1]):
                    rivi += "{:.5f};".format(muuttuja)

                with open(tiedostonimi, "w") as tiedosto:
                    tiedosto.write(rivi)

                break

        pelinumero += 1


def main():
    koulutus()


if __name__ == "__main__":
    main()
