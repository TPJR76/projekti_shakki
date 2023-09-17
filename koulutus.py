"""
Tässä tiedostossa on pohja shakkikoneen kouluttamiselle. Nykyinen versio
mahdollistaa datan muodostamisen.
"""

from teorialauta import Teorialauta, shakkilaudan_koordinaatit
from random import randint


class PuunAlkio:
    def __init__(self, tilanne=Teorialauta.ALOITUSASEMAT, arvo=0.0):
        """

        """

        self.edellinen = None
        self.seuraavat = []
        self.tilanne = tilanne
        self.arvo = arvo

    def __str__(self):
        asemat = self.tilanne
        rivi = self.muodosta_sarjanumero() + ";"

        for nappulatyyppi in asemat.keys():
            for asema in asemat[nappulatyyppi]:
                rivi += asema
                if asema != asemat[nappulatyyppi][-1]:
                    rivi += "-"
            rivi += ";"

        rivi += str(self.arvo) + "\n"
        return rivi

    def haara(self):
        if not self.edellinen:
            return 0

        haara = 1
        for alkio in self.edellinen.seuraavat:
            if alkio == self:
                return haara

            haara += 1

        return haara

    def muodosta_sarjanumero(self):
        if self.haara() == 0:
            return "0"

        sarjanumero = ""
        alkio = self

        while alkio.edellinen:
            sarjanumero = str(alkio.haara()) + sarjanumero
            alkio = alkio.edellinen
            if alkio.edellinen:
                sarjanumero = "-" + sarjanumero

        return sarjanumero

    def etsi_tilanne(self, tilanne):
        juuri = self

        while True:
            if juuri.tilanne == tilanne:
                return juuri

            if juuri.seuraavat:
                juuri = juuri.seuraavat[0]
                continue

            if not juuri.edellinen:
                return None

            if juuri == juuri.edellinen.seuraavat[-1]:
                tarkistus = juuri
                viimeinen = True

                while tarkistus.edellinen:
                    if tarkistus != tarkistus.edellinen.seuraavat[-1]:
                        aiempi_haara = tarkistus.haara()
                        juuri = tarkistus.edellinen.seuraavat[aiempi_haara]
                        viimeinen = False
                        break

                    tarkistus = tarkistus.edellinen

                if viimeinen:
                    return None

            else:
                juuri = juuri.edellinen.seuraavat[juuri.haara()]

    def lisaa_seuraava(self, tilanne, arvo):
        uusi_alkio = PuunAlkio(tilanne, arvo)
        uusi_alkio.edellinen = self
        self.seuraavat.append(uusi_alkio)


def data_tiedostosta(tiedostonimi):
    data = PuunAlkio()
    juuri = data
    juuren_syvyys = 1

    with open(tiedostonimi, "r") as tiedosto:
        for rivi in tiedosto:

            # Painotusrivi täytyy jättää huomioitta
            if len(rivi.rstrip().split(";")) == 4:
                continue

            sarjanumero = rivi.rstrip().split(";")[0]
            haarat = sarjanumero.split("-")
            nykyinen_syvyys = len(haarat)

            # Liikutaan eteepäin puussa
            if nykyinen_syvyys > juuren_syvyys:
                haara = int(haarat[-1])
                juuri = juuri.seuraavat[haara-1]

            # Liikutaan taaksepäin puussa
            while nykyinen_syvyys < juuren_syvyys:
                juuri = juuri.edellinen
                juuren_syvyys -= 1

            nappulatyypin_asemat = rivi.rstrip().split(";")[1:-1]
            tilanne = {}

            indeksi = 0
            for sijainnit in nappulatyypin_asemat:
                avain = list(Teorialauta.ALOITUSASEMAT.keys())[indeksi]
                sijainnit = sijainnit.split("-")
                tilanne.update({avain: sijainnit})
                indeksi += 1

            arvo = float(rivi.rstrip().split(";")[-1])

            juuri.lisaa_seuraava(tilanne, arvo)

    return data


def tiedosto_datasta(data, tiedostonimi):
    lisaa_rivi_tiedostoon(str(data), tiedostonimi)

    if not data.seuraavat:
        return
    for alkio in data.seuraavat:
        tiedosto_datasta(alkio, tiedostonimi)


def lisaa_rivi_tiedostoon(lisattava_rivi, tiedostonimi):
    """
    Tämä funktio kirjaa rivin tiedostoon.

    :param lisattava_rivi: str, tiedostoon kirjoitettavat tiedot.
    :param tiedostonimi: str, tiedosto, johon rivi lisätään.
    """

    rivit = []
    rivinumero = 0
    oikea_rivinumero = None

    with open(tiedostonimi, "r") as tiedosto:
        for tiedoston_rivi in tiedosto:

            # Painotusrivi täytyy jättää huomioitta
            if len(tiedoston_rivi.rstrip().split(";")) == 4:
                continue

            # Jos lisättävä rivi on jo tiedostossa, jatkaminen on turhaa
            if tiedoston_rivi == lisattava_rivi:
                return

            if tiedoston_rivi.rstrip().split(";")[:-1] == \
                    lisattava_rivi.rstrip().split(";")[:-1]:
                oikea_rivinumero = rivinumero

            rivit += tiedoston_rivi
            rivinumero += 1

    if not oikea_rivinumero:
        with open(tiedostonimi, "a") as tiedosto:
            tiedosto.write(lisattava_rivi)

    else:
        rivit[oikea_rivinumero] = lisattava_rivi
        with open(tiedostonimi, "w") as tiedosto:
            for rivi in rivit:
                tiedosto.write(rivi)


def painotukset_tiedostosta(tiedostonimi):
    """
    Tämä funktio kerää painotukset tiedoston ensimmäiseltä riviltä.

    :param tiedostonimi: str, tiedoston nimi, josta painotukset etsitään.
    :return: [float, ...], painotukset.
    """

    painotukset = []

    with open(tiedostonimi, "r") as tiedosto:
        for tiedoston_rivi in tiedosto:
            for painotus in tiedoston_rivi.rstrip().split(";"):
                painotukset.append(float(painotus))
            return painotukset


def muuta_painotuksia():
    """
    Tämä funktio vaihtaa haastajatiedoston painotuksien muutoksista.
    Muutoksen suuruutta voi kontrolloida muuttamalla jakajia ja kertojia.
    """

    haastajan_painotukset = painotukset_tiedostosta("haastaja.txt")
    parhaan_painotukset = painotukset_tiedostosta("paras.txt")
    indeksi = randint(0, 3)

    if haastajan_painotukset[indeksi] > parhaan_painotukset[indeksi]:
        haastajan_painotukset[indeksi] -= 0.00002

    else:
        haastajan_painotukset[indeksi] += 0.00001

    with open("haastaja.txt", "w") as tiedosto:
        tiedosto.write(str(haastajan_painotukset[0])+";"
                       + str(haastajan_painotukset[1])+";"
                       + str(haastajan_painotukset[2])+";"
                       + str(haastajan_painotukset[3])+"\n")


def muodosta_ruudun_arvo(pelilauta, ruutu, painotukset):
    """
    Tämä funktio muodostaa yhden ruudun arvon. Tässä versiossa se ottaa
    huomioon nappulan arvon, nappulan etäisyyden, nappulan
    siirtomahdollisuudet, ruutua uhkaavat nappulat ja ruutua puolustavat
    nappulat.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param ruutu: str, pelilaudan koordinaatti.
    :param painotukset: [float, ...], painotukset eri tiedoille.
    :return: int/float, yhden ruudun arvo pelitilanteessa.
    """

    # Arvo
    nappuloiden_arvot = {"valkoisen sotilaat": 1, "valkoisen tornit": 5,
                         "valkoisen ratsut": 3, "valkoisen lähetit": 3,
                         "valkoisen kuningatar": 9, "valkoisen kuningas": 0,
                         "mustan sotilaat": -1, "mustan tornit": -5,
                         "mustan ratsut": -3, "mustan lähetit": -3,
                         "mustan kuningatar": -9, "mustan kuningas": 0}
    asemat = pelilauta.asemalistat()

    nappulan_arvo = 0
    for nappula, linkitetty_arvo in nappuloiden_arvot.items():
        if ruutu in asemat.get(nappula, []):
            nappulan_arvo = linkitetty_arvo
            break

    # Etäisyys
    alkuetaisyydet = {"valkoisen sotilaat": 2, "valkoisen tornit": 1,
                      "valkoisen ratsut": 1, "valkoisen lähetit": 1,
                      "valkoisen kuningatar": 1, "valkoisen kuningas": 1,
                      "mustan sotilaat": 7, "mustan tornit": 8,
                      "mustan ratsut": 8, "mustan lähetit": 8,
                      "mustan kuningatar": 8, "mustan kuningas": 8}

    nappulan_etaisyys = 0
    for nappula, alkuetaisyys in alkuetaisyydet.items():
        if ruutu in asemat.get(nappula, []):
            ruudun_etaisyys = int(ruutu[-1])
            nappulan_etaisyys = ruudun_etaisyys - alkuetaisyys
            break

    # Siirtomahdollisuudet
    nappulan_siirtomahdollisuudet = 0
    if pelilauta.ruudun_nappulan_tiedot(ruutu):
        puoli, _, siirrot = pelilauta.ruudun_nappulan_tiedot(ruutu)
        if puoli == "White":
            nappulan_siirtomahdollisuudet = len(siirrot)
        else:
            nappulan_siirtomahdollisuudet = -len(siirrot)

    # Ruudun uhkaajat
    valkoisen_siirrot = pelilauta.puolen_kaikki_siirrot("valkoinen")
    mustan_siirrot = pelilauta.puolen_kaikki_siirrot("musta")

    ruudun_uhkaajat = 0
    for avain in valkoisen_siirrot:
        if ruutu in valkoisen_siirrot[avain]:
            if ruutu == pelilauta.asemalistat()["mustan kuningas"]:
                ruudun_uhkaajat += 10
            ruudun_uhkaajat += 1

    for avain in mustan_siirrot:
        if ruutu in mustan_siirrot[avain]:
            if ruutu == pelilauta.asemalistat()["valkoisen kuningas"]:
                ruudun_uhkaajat -= 10
            else:
                ruudun_uhkaajat -= 1

    w1, w2, w3, w4 = painotukset

    return w1*nappulan_arvo + w2*nappulan_etaisyys \
        + w3*nappulan_siirtomahdollisuudet + w4*ruudun_uhkaajat


def muodosta_pelitilanteen_arvo(pelilauta, data, painotukset, rekursio=True):
    """
    Tämä funktio muodostaa pelitilanteen arvon yksittäisten ruutujen
    perusteella. Jos rekursio on sallittuna, funktio voi kutsua
    arvioi_paras_siirto -funktiota, joka kutsuu uudelleen tätä funktiota.

    :param pelilauta: Teorialauta, pelitilanne, jota arvioidaan.
    :param data: PuunAlkio, tallennetut tiedot asemien arvoista.
    :param painotukset: [float, ...], painotukset, joilla pelitilanteet
                        arvioidaan.
    :param rekursio: bool, sallitaanko arvon muodostuksen rekursio.
    :return: int/float, pelitilanteen arvo lukuna.
    """

    if pelilauta.tarkista_voitto() == "valkoinen":
        return 1

    if pelilauta.tarkista_voitto() == "musta":
        return -1

    arvo = 0
    for ruutu in shakkilaudan_koordinaatit():
        arvo += muodosta_ruudun_arvo(pelilauta, ruutu, painotukset)

    if rekursio:
        uusi_lauta = Teorialauta()

        for _ in range(0, 3):
            uusi_lauta = Teorialauta()
            uusi_lauta.aloita_kesken_pelin(pelilauta.siirtonumero(),
                                           pelilauta.asemalistat(),
                                           pelilauta.liikkumistiedot())

            if uusi_lauta.siirtonumero() % 2 == 1:
                sijainti, siirto = arvioi_paras_siirto(
                    uusi_lauta, "valkoinen", data, painotukset, False)

            else:
                sijainti, siirto = arvioi_paras_siirto(
                    uusi_lauta, "musta", data, painotukset, False)

            uusi_lauta.tee_siirto(sijainti, siirto)
            if uusi_lauta.tarkista_voitto() is not None:
                break

        arvo += 0.5 * muodosta_pelitilanteen_arvo(
            uusi_lauta, data, painotukset, False)

    # Vältetään arvon menemästä yli rajan kaikissa tilanteissa
    if arvo >= 1:
        return 0.99999

    if arvo <= -1:
        return -0.99999

    return round(arvo, 5)


def arvioi_paras_siirto(pelilauta, puoli, data, painotukset, rekursio=True):
    """
    Tämä funktio etsii datasta parhaan siirron tulevan pelitilanteen
    arvojen perusteella. Jos sitä ei löydy, muodostaa uuden arvon.
    Tallentaa tulevat arvot huomioiden lasketut arvot tiedostoon.
    Tämän ominaisuuden avulla myös pelaajien pelaamien otteluiden
    tilanteet voidaan tallentaa.

    :param pelilauta: Teorialauta, pelitilanne, josta parasta siirtoa etsitään.
    :param puoli: str, puoli, jolla siirtäjä on.
    :param data: PuunAlkio, tallennetut tiedot asemien arvoista.
    :param painotukset: [float, ...], painotukset, joilla pelitilanteet
                        arvioidaan.
    :param rekursio: bool, sallitaanko arvon muodostuksen rekursio.
    :return: str, str / None, None; ruutu, josta lähdetään ja ruutu,
             johon siirrytään.
    """

    siirrot = pelilauta.puolen_kaikki_siirrot(puoli)
    parhaat_siirrot = []

    if puoli == "valkoinen":
        paras_arvo = -1
    else:
        paras_arvo = 1

    for asema in siirrot:
        for siirto in siirrot[asema]:

            uusi_lauta = Teorialauta()
            uusi_lauta.aloita_kesken_pelin(
                pelilauta.siirtonumero(), pelilauta.asemalistat(),
                pelilauta.liikkumistiedot())

            uusi_lauta.tee_siirto(asema, siirto)

            arvo = None
            tilanteen_alkio = data.etsi_tilanne(uusi_lauta.asemalistat)
            if tilanteen_alkio:
                arvo = tilanteen_alkio.arvo()

            if not arvo:
                arvo = muodosta_pelitilanteen_arvo(
                    uusi_lauta, data, painotukset, rekursio)

            if puoli == "valkoinen" and arvo > paras_arvo:
                parhaat_siirrot = [asema+"-"+siirto]
                paras_arvo = arvo

            if puoli == "musta" and arvo < paras_arvo:
                parhaat_siirrot = [asema+"-"+siirto]
                paras_arvo = arvo

            if arvo == paras_arvo:
                parhaat_siirrot.append(asema+"-"+siirto)

    if not parhaat_siirrot:
        return None, None

    if len(parhaat_siirrot) == 1:
        return parhaat_siirrot[0].split("-")

    return parhaat_siirrot[randint(0, len(parhaat_siirrot)-1)].split("-")


def muodosta_dataa(painotukset):
    data = PuunAlkio()
    juuri = data
    pelilaudat = [Teorialauta()]
    maksimisyvyys = 3

    while True:
        uudet_laudat = []
        for pelilauta in pelilaudat:

            juuri = data.etsi_tilanne(pelilauta.asemalistat())

            if len(juuri.muodosta_sarjanumero().split("-")) \
                    == maksimisyvyys:
                continue

            if pelilauta.siirtonumero() % 2 == 1:
                siirrot = pelilauta.puolen_kaikki_siirrot("valkoinen")
            else:
                siirrot = pelilauta.puolen_kaikki_siirrot("musta")

            for asema in siirrot:
                for siirto in siirrot[asema]:
                    uusi_lauta = Teorialauta()
                    uusi_lauta.aloita_kesken_pelin(
                        pelilauta.siirtonumero(), pelilauta.asemalistat(),
                        pelilauta.liikkumistiedot())

                    uusi_lauta.tee_siirto(asema, siirto)

                    tilanne = uusi_lauta.asemalistat()
                    arvo = muodosta_pelitilanteen_arvo(
                        pelilauta, data, painotukset, False)

                    juuri.lisaa_seuraava(tilanne, arvo)

                    if not uusi_lauta.tarkista_voitto():
                        uudet_laudat.append(uusi_lauta)

        if len(juuri.muodosta_sarjanumero().split("-")) \
                == maksimisyvyys:
            return data
        pelilaudat = uudet_laudat


def evolutiivinen_kehittyminen():
    """
    Tömä funktio vastaa tiedostojen evolutiivisesta kehittämisestä.
    TODO: Päivitä funktion toiminta vastaamaan uutta datarakennetta.
    """

    # Avataan tiedostot
    parhaan_data = data_tiedostosta("paras.txt")
    parhaan_painotukset = painotukset_tiedostosta("paras.txt")
    haastajan_data = data_tiedostosta("haastaja.txt")
    haastajan_painotukset = painotukset_tiedostosta("haastaja.txt")

    pelinumero = 1
    tilanne = 0

    while pelinumero < 50:

        if tilanne > 50 - pelinumero or tilanne < -50 + pelinumero:
            break

        print(pelinumero, ". peli", sep="")

        pelilauta = Teorialauta()

        if pelinumero % 2 == 1:
            valkoisen_data = parhaan_data
            valkoisen_painotukset = parhaan_painotukset
            mustan_data = haastajan_data
            mustan_painotukset = haastajan_painotukset
            positiivinen_voittaja = "valkoinen"
            negatiivinen_voittaja = "musta"

        else:
            valkoisen_data = haastajan_data
            valkoisen_painotukset = haastajan_painotukset
            mustan_data = parhaan_data
            mustan_painotukset = parhaan_painotukset
            positiivinen_voittaja = "musta"
            negatiivinen_voittaja = "valkoinen"

        # Yksi ottelu
        while True:
            print(pelilauta.siirtonumero())

            if pelilauta.siirtonumero() == 100:
                # print("Tasapeli.")
                break

            if pelilauta.siirtonumero() % 2 != 0:
                sijainti, siirto = arvioi_paras_siirto(
                    pelilauta, "valkoinen", valkoisen_data,
                    valkoisen_painotukset)
            else:
                sijainti, siirto = arvioi_paras_siirto(
                    pelilauta, "musta", mustan_data, mustan_painotukset)

            pelilauta.tee_siirto(sijainti, siirto)

            if pelilauta.tarkista_voitto() == positiivinen_voittaja:
                # print("Paras voitti.")
                tilanne += 1
                break

            if pelilauta.tarkista_voitto() == negatiivinen_voittaja:
                # print("Haastaja voitti.")
                tilanne -= 1
                break

        pelinumero += 1
        print("Pelitilanne:", tilanne)

    # Korvaa paras haastajalla
    if tilanne <= -5:
        with open("haastaja.txt", "r") as haastaja:
            with open("paras.txt", "w") as paras:
                for rivi in haastaja:
                    paras.write(rivi)

        print("Haastaja voitti", -tilanne, "pelillä.")

    else:
        print("Paras voitti", tilanne, "pelillä.")

    muuta_painotuksia()


def main():
    # paras_data = muodosta_dataa(painotukset_tiedostosta("paras.txt"))
    # tiedosto_datasta(paras_data, "paras.txt")
    # haastajan_data = muodosta_dataa(painotukset_tiedostosta("haastaja.txt"))
    # tiedosto_datasta(haastajan_data, "haastaja.txt")
    # evolutiivinen_kehittyminen()
    pass


if __name__ == "__main__":
    main()
