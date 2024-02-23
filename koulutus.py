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
OPPIMISNOPEUS = 0.01


def muuttujat_tiedostosta(tiedostonimi):
    """
    Tämä funktio kerää painotukset ja vinouman tiedoston ensimmäiseltä
    riviltä.

    :param tiedostonimi: str, tiedoston nimi, josta painotukset etsitään.
    :return: [float, ...], painotukset ja vinouma.
    """

    muuttujat = []

    with open(tiedostonimi, "r") as tiedosto:
        for tiedoston_rivi in tiedosto:
            if not tiedoston_rivi:
                return None

            indeksi = 0
            for luku in tiedoston_rivi.rstrip().split(";"):
                if not luku:
                    return muuttujat

                muuttujat.append(float(luku))

                indeksi += 1

    return None


def muodosta_koko_x(pelilauta, rekursio):
    """
    Tämä funktio muodostaa pelitilanteen arvon yksittäisten ruutujen
    perusteella. Jos rekursio on sallittuna, funktio voi arvioida nykyistä
    asemaa seuraavien tilanteiden perusteella.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param rekursio: bool, sallitaanko arvon muodostuksen rekursio.
    :return: [int, ..], yhden ruudun arvo pelitilanteessa.
    """

    puolten_kaikki_siirrot = (pelilauta.puolen_kaikki_siirrot("valkoinen"),
                              pelilauta.puolen_kaikki_siirrot("musta"))

    asemat = pelilauta.asemat()

    x = [0, 0, 0, 0, 0]
    for indeksi in range(0, 64):
        x_lisays = muodosta_ruudun_x(pelilauta, indeksi,
                                     puolten_kaikki_siirrot, asemat)
        for i in range(0, 5):
            x[i] += x_lisays[i]

    if rekursio:
        uusi_x = [0, 0, 0, 0, 0]

        for _ in range(0, ARVIOINNIN_MAKSIMISYVYYS):
            uusi_lauta = Teorialauta(pelilauta.siirtonumero(),
                                     pelilauta.asemat(),
                                     pelilauta.liikkumistiedot(),
                                     pelilauta.shakit())

            if uusi_lauta.siirtonumero() % 2 == 1:
                sijainti, siirto, uusi_x = arvioi_paras_siirto(
                    uusi_lauta, "valkoinen", False)

            else:
                sijainti, siirto, uusi_x = arvioi_paras_siirto(
                    uusi_lauta, "musta", False)

            uusi_lauta.tee_siirto(sijainti, siirto)
            if uusi_lauta.voittaja() is not None:
                break

            pelilauta = uusi_lauta

        for i in range(0, 5):
            x[i] = 0.5 * (x[i] + uusi_x[i])

    return x


def muodosta_ruudun_x(pelilauta, ruutu, puolten_kaikki_siirrot, asemat):
    """
    Tämä funktio muodostaa yhden ruudun x-vektorin. Tässä versiossa se ottaa
    huomioon nappulan arvon, nappulan etäisyyden keskustasta, nappulan
    siirtomahdollisuudet, ruutua uhkaavat nappulat, ruutua puolustavat
    nappulat sekä onko kuningas shakissa.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param ruutu: str, pelilaudan koordinaatti.
    :param puolten_kaikki_siirrot: {int: int, ...}, {int: int, ...};
                                    sanakirjat, joissa lähtöindeksit
                                    on linkitetty nappulan
                                    siirtomahdollisuuksien bittilautaan.
    :param asemat: [int, ...], pelilaudan tilanne kuvattuna nappulatyyppien
                   sijaintien bittilautoina.
    :return: [int, ..], yhden ruudun arvo pelitilanteessa.
    """

    # Nappulan arvo ja etäisyys
    nappuloiden_arvot = [1, 5, 3, 3, 9, 0, -1, -5, -3, -3, -9, 0]

    nappulan_arvo = 0
    nappulan_etaisyys = 0
    nappulan_siirtomahdollisuudet = 0
    shakissa = 0

    for i in range(0, 12):

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
    valkoisen_siirrot = puolten_kaikki_siirrot[0]
    mustan_siirrot = puolten_kaikki_siirrot[1]

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

    return [nappulan_arvo, nappulan_etaisyys, nappulan_siirtomahdollisuudet,
            ruudun_uhkaajat, shakissa]


def muodosta_pelitilanteen_arvo(x, muuttujat):
    """
    Tämä funktio muodostaa pelitilanteen arvon yksittäisten ruutujen
    perusteella. Jos rekursio on sallittuna, funktio voi arvioida nykyistä
    asemaa seuraavien tilanteiden perusteella.

    :param x: [int/float, ...], vektori lasketuista pelitilanteeseen
              vaikuttavista arvoista.
    :param muuttujat: [float, ...], painotukset ja vinouma.
    :return: int/float, pelitilanteen arvo lukuna.
    """

    arvo = 0
    for i in range(0, 5):
        arvo += x[i] * muuttujat[i]

    # Lisätään vinouma
    arvo += muuttujat[-1]

    # Vältetään arvon menemästä yli rajan kaikissa tilanteissa
    if arvo >= 1:
        return 0.99999999

    if arvo <= -1:
        return -0.99999999

    return round(arvo, 8)


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
    shakit = pelilauta.shakit()

    for asema in siirrot:
        indeksi = 0

        while siirrot[asema]:
            if siirrot[asema] & 1:
                uusi_lauta = Teorialauta(siirtonumero, asemat,
                                         liikkumistiedot, shakit)

                uusi_lauta.tee_siirto(asema, indeksi)

                x = muodosta_koko_x(uusi_lauta, rekursio)

                if uusi_lauta.voittaja() == "valkoinen":
                    arvo = 1
                elif uusi_lauta.voittaja() == "musta":
                    arvo = -1
                else:
                    arvo = muodosta_pelitilanteen_arvo(muuttujat, x)

                if puoli == "valkoinen" and arvo > paras_arvo:
                    parhaat_siirrot = [[asema, indeksi, x]]
                    paras_arvo = arvo

                if puoli == "musta" and arvo < paras_arvo:
                    parhaat_siirrot = [[asema, indeksi, x]]
                    paras_arvo = arvo

                if arvo == paras_arvo:
                    parhaat_siirrot.append([asema, indeksi, x])

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
    # Arvon muodostus on suunniteltu siten,
    # että kertoimien ei kuulu olla negatiivisia
    for _ in range(0, 5):
        rivi += "{:.8f};".format(randint(5, 1000)*0.00000001)

    rivi += "{:.8f};".format(randint(-100, 100)*0.00000001)

    with open(tiedostonimi, "w") as tiedosto:
        tiedosto.write(rivi)

    return


def keskiarvo_virhe(y, y_arvioidut):
    """
    Tämä funktio laskee ja palauttaa virheen keskiarvon.

    :param y: int, tavoitearvo.
    :param y_arvioidut: [float, ...], lista muodostetuista arvioista.
    :return: float, virheen keskiarvo.
    """

    summa = 0
    for y_arvioitu in y_arvioidut:
        summa += y-y_arvioitu

    return summa/len(y_arvioidut)


def koulutus():
    """
    Tämä funktio vastaa shakkikoneen varsinaisesta kouluttamisesta.
    Pyörittää teoreettista shakkipeliä itseään vastaan, ja vertaa ottelun
    tulosta matkan varrella muodostettuihin ennusteisiin.
    """

    tiedostonimi = "tulokset.txt"
    pelinumero = 1

    while True:

        if pelinumero == PELIEN_MAKSIMI:
            print("Koulutus päättyi.")
            break

        print(pelinumero, ". peli", sep="")

        pelilauta = Teorialauta()
        ennustukset = []
        x_keskiarvo = []

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
            if siirtonumero == 200:
                print("Tasapeli.")
                break

            voittaja = None

            # Arvioidaan vuorossa olevalle puolelle paras siirto
            if siirtonumero % 2 == 1:
                sijainti, siirto, x = arvioi_paras_siirto(
                    pelilauta, "valkoinen", muuttujat, False)

                if not siirto:
                    voittaja = "musta"
            else:
                sijainti, siirto, x = arvioi_paras_siirto(
                    pelilauta, "musta", muuttujat, False)

                if not siirto:
                    voittaja = "valkoinen"

            if siirto:
                if not x_keskiarvo:
                    x_keskiarvo = x
                else:
                    for i in range(0, 5):
                        x_keskiarvo[i] = (x_keskiarvo[i] + x[i]) * 0.5

                pelilauta.tee_siirto(sijainti, siirto)
                voittaja = pelilauta.voittaja()

                # Lisätään ennustuksiin uuden tilanteen ennustus
                ennustukset.append(muodosta_pelitilanteen_arvo(x, muuttujat))

            # Tarkistetaan, johtiko vuoro voittoon
            if voittaja:

                if voittaja == "valkoinen":
                    virhe = keskiarvo_virhe(1, ennustukset)

                else:
                    virhe = keskiarvo_virhe(-1, ennustukset)

                suoritusaika = time.time() - aloitusaika

                # Tulostetaan ottelun tietoja
                print("Voittaja:", voittaja)
                print("Siirtoja:", siirtonumero)
                print("Suoritusaika:", suoritusaika, "s")
                print("Suoritusaika per siirto:", suoritusaika/siirtonumero,
                      "s/siirto")
                print("Virhe:", virhe)

                for i in range(0, 5):
                    muuttujat[i] += OPPIMISNOPEUS*virhe*x_keskiarvo[i]

                # jos virhe on yli 1, arviointi suosii liikaa jompaa kumpaa
                # puolta
                if abs(virhe) > 1:
                    muuttujat[-1] += OPPIMISNOPEUS*virhe

                # aletaan pienentämään vinoumaa,
                # kun tarkkuus alkaa olemaan hyvällä mallilla
                elif abs(virhe) < 0.3:
                    muuttujat[-1] = muuttujat[-1] * 0.5

                rivi = ""
                for muuttuja in muuttujat:
                    rivi += "{:.8f};".format(muuttuja)

                with open(tiedostonimi, "w") as tiedosto:
                    tiedosto.write(rivi)

                break

        pelinumero += 1


def main():
    koulutus()


if __name__ == "__main__":
    main()
