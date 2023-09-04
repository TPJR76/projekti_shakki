"""
Tämä tiedosto esittelee luokan Teorialauta, joka vastaa shakkipelin
teoreettisesta pyörittämisestä. Tätä tiedostoa on kehitetty vastaamaan niin
graafisen käyttöliittymän kuin shakkikoneen kouluttamisen tarpeisiin.
"""

from copy import deepcopy


class Teorialauta:
    # Shakkilaudan koordinaattikirjaimet
    KIRJAIMET = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # Pelin lähtöasema
    ALOITUSASEMAT = {"valkoisen sotilaat":
                     ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                     "valkoisen tornit": ["a1", "h1"],
                     "valkoisen ratsut": ["b1", "g1"],
                     "valkoisen lähetit": ["c1", "f1"],
                     "valkoisen kuningatar": ["d1"],
                     "valkoisen kuningas": ["e1"],
                     "mustan sotilaat":
                     ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                     "mustan tornit": ["a8", "h8"],
                     "mustan ratsut": ["b8", "g8"],
                     "mustan lähetit": ["c8", "f8"],
                     "mustan kuningatar": ["d8"],
                     "mustan kuningas": ["e8"]}

    def __init__(self):
        """
        Rakentaa teorialaudan eli aloittaa uuden teoreettisen shakkipelin
        lähtöasemasta.
        """

        self.__siirtonumero = 1

        # Laudan asetelma
        self.__asemalistat = deepcopy(Teorialauta.ALOITUSASEMAT)
        self.__valkoisen_asemat = []
        self.__mustan_asemat = []
        self.paivita_asemat()

        # Castlingia varten pidetään kirjaa näistä
        self.__valkoisen_vasen_torni_lahtoasemassa = True
        self.__valkoisen_oikea_torni_lahtoasemassa = True
        self.__valkoisen_kuningas_lahtoasemassa = True
        self.__mustan_vasen_torni_lahtoasemassa = True
        self.__mustan_oikea_torni_lahtoasemassa = True
        self.__mustan_kuningas_lahtoasemassa = True
        self.__linnoittaminen = False

    def aloita_kesken_pelin(self, siirtonumero, asemalistat, liikkumistiedot):
        """
        Funktio, jolla toisen pelin tiedoilla voidaan aloittaa kesken pelin.

        :param siirtonumero: int, kuinka mones siirto on tulossa.
        :param asemalistat: {str: [str, ...]}, nappulatyypin nimi linkitettynä
                            ruutujen listaan.
        :param liikkumistiedot: [bool, ...], tiedot nappuloista,
               joita tarkkaillaan linnoittamista varten.
        """

        self.__siirtonumero = deepcopy(siirtonumero)
        self.__asemalistat = deepcopy(asemalistat)
        self.__valkoisen_vasen_torni_lahtoasemassa, \
            self.__valkoisen_oikea_torni_lahtoasemassa, \
            self.__valkoisen_kuningas_lahtoasemassa, \
            self.__mustan_vasen_torni_lahtoasemassa, \
            self.__mustan_oikea_torni_lahtoasemassa, \
            self.__mustan_kuningas_lahtoasemassa = deepcopy(liikkumistiedot)

    def tee_siirto(self, sijainti, siirto):
        """
        Funktio, jolla asemat muuttuvat annetun siirron mukaisesti.

        :param sijainti: str, ruutu, josta nappula lähtee.
        :param siirto: str, ruutu, johon nappula siirtyy.
        """

        # Normaali siirtäminen
        # Käydään läpi tallennettuja asemia
        for avain in self.__asemalistat:
            for asema in self.__asemalistat[avain]:
                if asema == sijainti:
                    # Poistetaan tiedoista nappulan sijaintiruutu ja
                    # lisätään sen paikalle annettu siirtoruutu
                    indeksi = self.__asemalistat[avain].index(sijainti)
                    self.__asemalistat[avain].pop(indeksi)
                    self.__asemalistat[avain].insert(indeksi, siirto)
                if asema == siirto:
                    # Nappulan syöminen
                    self.__asemalistat[avain].remove(siirto)

        # Tarkkaillaan seuraavien nappuloiden liikkeitä linnoittamista varten:
        if sijainti == "a1" or \
                (sijainti in self.__mustan_asemat and siirto == "a1"):
            self.__valkoisen_vasen_torni_lahtoasemassa = False
        if sijainti == "a8" or \
                (sijainti in self.__valkoisen_asemat and siirto == "a8"):
            self.__mustan_vasen_torni_lahtoasemassa = False
        if sijainti == "h1" or \
                (sijainti in self.__mustan_asemat and siirto == "h1"):
            self.__valkoisen_oikea_torni_lahtoasemassa = False
        if sijainti == "h8" or \
                (sijainti in self.__valkoisen_asemat and siirto == "h8"):
            self.__mustan_oikea_torni_lahtoasemassa = False
        if sijainti == "e1" or \
                (sijainti in self.__mustan_asemat and siirto == "e1"):
            self.__valkoisen_kuningas_lahtoasemassa = False
        if sijainti == "e8" or \
                (sijainti in self.__valkoisen_asemat and siirto == "e8"):
            self.__mustan_kuningas_lahtoasemassa = False

        # Jos linnoittaminen tapahtuu, myös tornit siirtyvät
        if self.__linnoittaminen:
            if siirto == "c1" and sijainti == "e1":
                self.__asemalistat["valkoisen tornit"].remove("a1")
                self.__asemalistat["valkoisen tornit"].append("d1")
            elif siirto == "g1" and sijainti == "e1":
                self.__asemalistat["valkoisen tornit"].remove("h1")
                self.__asemalistat["valkoisen tornit"].append("f1")
            elif siirto == "c8" and sijainti == "e8":
                self.__asemalistat["mustan tornit"].remove("a8")
                self.__asemalistat["mustan tornit"].append("d8")
            elif siirto == "g8" and sijainti == "e8":
                self.__asemalistat["mustan tornit"].remove("h8")
                self.__asemalistat["mustan tornit"].append("f8")
            else:
                self.__linnoittaminen = False

        # Kuningattareksi nousu sotilaalle laudan päädyssä
        if siirto in self.__asemalistat["valkoisen sotilaat"] and siirto in \
                ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
            self.__asemalistat["valkoisen sotilaat"].remove(siirto)
            self.__asemalistat["valkoisen kuningatar"].append(siirto)
        if siirto in self.__asemalistat["mustan sotilaat"] and siirto in \
                ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
            self.__asemalistat["mustan sotilaat"].remove(siirto)
            self.__asemalistat["mustan kuningatar"].append(siirto)

        # Päivitä siirtonumero ja asemalistat
        self.__siirtonumero += 1
        self.paivita_asemat()

    def paivita_asemat(self):
        """
        Apufunktio, joka päivittää listat puolten varaamista ruuduista.
        """

        avaimet = self.__asemalistat.keys()
        self.__valkoisen_asemat = []
        self.__mustan_asemat = []

        # Alkuperäisessä tietorakenteessa olevien avaimien avulla voi löytää
        # kaikki puolten varaamat ruudut
        for avain in avaimet:
            if "valkoisen" in avain:
                self.__valkoisen_asemat += self.__asemalistat[avain]
            if "mustan" in avain:
                self.__mustan_asemat += self.__asemalistat[avain]

    def tarkista_voitto(self):
        """
        Apufunktio, joka yksinkertaisesti tarkistaa, onko puolella enää
        kuningasta. Tähän voisi lisätä myös tarkistuksen siitä, onko kuningas
        matitettu.

        :return: str/None, puoli, joka on voittanut.
        """

        if not self.__asemalistat["mustan kuningas"]:
            return "valkoinen"
        if not self.__asemalistat["valkoisen kuningas"]:
            return "musta"
        return None

    def shakitetut_kuninkaat(self):
        """
        Apufunktio, jolla voi selvittää, onko kuningas shakitettu.

        :return: str/None, str/None; jos shakitettu, sijainti, muuten None
        """

        # Oletetaan, että kuninkaat eivät ole shakissa
        valkoinen_shakitettu_kuningas = None
        musta_shakitettu_kuningas = None
        for sijainti in self.puolen_kaikki_siirrot("valkoinen"):
            if self.__asemalistat["mustan kuningas"][0] in \
                    self.puolen_kaikki_siirrot("valkoinen")[sijainti]:
                musta_shakitettu_kuningas = self.__asemalistat[
                    "mustan kuningas"][0]
        for sijainti in self.puolen_kaikki_siirrot("musta"):
            if self.__asemalistat["valkoisen kuningas"][0] in \
                    self.puolen_kaikki_siirrot("musta")[sijainti]:
                valkoinen_shakitettu_kuningas = self.__asemalistat[
                    "valkoisen kuningas"][0]

        return valkoinen_shakitettu_kuningas, musta_shakitettu_kuningas

    def siirtonumero(self):
        """
        Apufunktio, joka palauttaa senhetkisen siirtonumeron.

        :return: int, siirtonumero.
        """

        return self.__siirtonumero

    def asemat(self):
        """
        Apufunktio, joka palauttaa listat molempien puolien varaamista
        ruuduista.

        :return: [str, ...], [str, ...]; listat puolien varaamista
                 ruuduista (valkoinen, musta).
        """

        return self.__valkoisen_asemat, self.__mustan_asemat

    def asemalistat(self):
        """
        Apufunktio, joka palauttaa nappulatyyppeihin linkitetyt asemalistat.

        :return: {str: [str, ...]}, nappulatyypin nimi linkitettynä ruutujen
                 listaan.
        """

        return self.__asemalistat

    def liikkumistiedot(self):
        """
        Apufunktio, joka palauttaa liikkumistiedot, joita seurataan
        linnoittamisen varalta.

        :return: [bool, ...]; onko jokin nappuloista liikkunut.
        """

        return self.__valkoisen_vasen_torni_lahtoasemassa, \
            self.__valkoisen_oikea_torni_lahtoasemassa, \
            self.__valkoisen_kuningas_lahtoasemassa, \
            self.__mustan_vasen_torni_lahtoasemassa, \
            self.__mustan_oikea_torni_lahtoasemassa, \
            self.__mustan_kuningas_lahtoasemassa

    def puolten_kokonaismateriaali(self):
        """
        Apufunktio, joka määrittää puolten materiaalin arvon yleisesti
        käytetyllä taulukolla:
        Sotilas = 1 piste
        Ratsu = 3 pistettä
        Lähetti = 3 pistettä
        Torni = 5 pistettä
        Kuningatar = 9 pistettä

        :return: int, int; materiaalin arvo kokonaislukuna.
        """

        valkoisen_materiaali = \
            len(self.__asemalistat["valkoisen sotilaat"]) \
            + len(self.__asemalistat["valkoisen lähetit"])*3 \
            + len(self.__asemalistat["valkoisen ratsut"])*3 \
            + len(self.__asemalistat["valkoisen tornit"])*5 \
            + len(self.__asemalistat["valkoisen kuningatar"])*9
        mustan_materiaali = \
            len(self.__asemalistat["mustan sotilaat"]) \
            + len(self.__asemalistat["mustan lähetit"])*3 \
            + len(self.__asemalistat["mustan ratsut"])*3 \
            + len(self.__asemalistat["mustan tornit"])*5 \
            + len(self.__asemalistat["mustan kuningatar"])*9

        return valkoisen_materiaali, mustan_materiaali

    def ruudun_nappulan_tiedot(self, ruutu):
        """
        Apufunktio, joka palauttaa tietoa annetusta ruudussa olevasta
        nappulasta.

        :param ruutu: str, nappulan sijainti.
        :return: str, str, [str, ...]; nappulan väri, nimi sekä lista sen
                 mahdollisista siirroista
        """

        nappulatiedot = {
            "valkoisen sotilaat": ("White", "Sotilas",
                                   self.valkoisen_sotilaan_liike),
            "valkoisen tornit": ("White", "Torni", self.tornin_liike),
            "valkoisen ratsut": ("White", "Ratsu", self.ratsun_liike),
            "valkoisen lähetit": ("White", "Lähetti", self.lahetin_liike),
            "valkoisen kuningatar": ("White", "Kuningatar",
                                     self.kuningattaren_liike),
            "valkoisen kuningas": ("White", "Kuningas", self.kuninkaan_liike),
            "mustan sotilaat": ("Black", "Sotilas",
                                self.mustan_sotilaan_liike),
            "mustan tornit": ("Black", "Torni", self.tornin_liike),
            "mustan ratsut": ("Black", "Ratsu", self.ratsun_liike),
            "mustan lähetit": ("Black", "Lähetti", self.lahetin_liike),
            "mustan kuningatar": ("Black", "Kuningatar",
                                  self.kuningattaren_liike),
            "mustan kuningas": ("Black", "Kuningas", self.kuninkaan_liike),
        }

        for nappula, (vari, tyyppi, liike) in nappulatiedot.items():
            if ruutu in self.__asemalistat.get(nappula, []):
                siirrot = liike(ruutu)
                return vari, tyyppi, siirrot

    def puolen_kaikki_siirrot(self, puoli):
        """
        Apufunktio, joka palauttaa puolen kaikki mahdolliset siirrot.

        :param puoli: str, valittu puoli, musta tai valkoinen.
        :return: {str: [str, ...]}, sanakirja puolen nappuloiden ruuduista
                 linkitettyinä siitä mahdollisten siirtymäruutujen listaan.
        """

        siirrot = {}

        if puoli == "valkoinen":
            for ruutu in self.__asemalistat["valkoisen sotilaat"]:
                if self.valkoisen_sotilaan_liike(ruutu):
                    siirrot.update({
                        ruutu: self.valkoisen_sotilaan_liike(ruutu)})
            puolen = "valkoisen "
        else:
            for ruutu in self.__asemalistat["mustan sotilaat"]:
                if self.mustan_sotilaan_liike(ruutu):
                    siirrot.update({ruutu: self.mustan_sotilaan_liike(ruutu)})
            puolen = "mustan "

        muut_nappulat = {
            "tornit": self.tornin_liike,
            "lähetit": self.lahetin_liike,
            "ratsut": self.ratsun_liike,
            "kuningatar": self.kuningattaren_liike,
            "kuningas": self.kuninkaan_liike
        }

        for nappula, liike in muut_nappulat.items():
            for ruutu in self.__asemalistat[puolen+nappula]:
                if liike(ruutu):
                    siirrot.update({ruutu: liike(ruutu)})

        return siirrot

    def valkoisen_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii valkoisen sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.
        Koska nappulat siirtyvät eri väreillä eri suuntaan, ne on eroteltu
        omiksi metodeikseen.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        aseman_kirjain = asema[0]
        y = int(asema[1])

        # Syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if kirjain + str(y + 1) in self.__mustan_asemat:
                siirrot.append(kirjain + str(y + 1))

        # Yhden siirto eteenpäin
        if aseman_kirjain + str(y + 1) not in \
                self.__mustan_asemat + self.__valkoisen_asemat:
            siirrot.append(aseman_kirjain + str(y + 1))

            # Kahden siirto eteenpäin
            if y == 2 and aseman_kirjain + "4" not in \
                    self.__mustan_asemat + self.__valkoisen_asemat:
                siirrot.append(aseman_kirjain + str(y + 2))

        return siirrot

    def mustan_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii mustan sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        aseman_kirjain = asema[0]
        y = int(asema[1])

        # Syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if kirjain + str(y - 1) in self.__valkoisen_asemat:
                siirrot.append(kirjain + str(y - 1))

        # Yhden siirto eteenpäin
        if aseman_kirjain + str(y - 1) not in \
                self.__mustan_asemat + self.__valkoisen_asemat:
            siirrot.append(aseman_kirjain + str(y - 1))

            # Kahden siirto eteenpäin
            if y == 7 and aseman_kirjain + "5" not in (
                    self.__mustan_asemat + self.__valkoisen_asemat):
                siirrot.append(aseman_kirjain + str(y - 2))

        return siirrot

    def tornin_liike(self, asema):
        """
        Apufunktio, joka tutkii tornin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Torni voi liikkua suorasti niin pitkälle kuin
        vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta torni lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        valkoinen, musta = self.asemat()
        if asema in valkoinen:
            oma_puoli, vast_puoli = valkoinen, musta
        else:
            oma_puoli, vast_puoli = musta, valkoinen

        aseman_kirjain = asema[0]
        y = int(asema[1])
        x = Teorialauta.KIRJAIMET.index(aseman_kirjain)

        # Viitataan kommenteissa tornin suuntiin näin:
        # * 1 *
        # 2 T 3
        # * 4 *

        # Pääseekö suuntiin [1, 2, 3, 4]
        paasyt = [True, True, True, True]

        for kerroin in range(1, 9):
            # Tallennetaan mahdolliset siirtymät pareiksi listaan muodossa
            # [[delta_x, delta_y]].
            siirtymat = []

            # Tarkistetaan suuntaan 1 pääsy
            if paasyt[0] and y + kerroin <= 8:
                siirtymat.append([0, kerroin])
            else:
                siirtymat.append([0, 0])

            # Suunta 2
            if paasyt[1] and x - kerroin >= 0:
                siirtymat.append([-kerroin, 0])
            else:
                siirtymat.append([0, 0])

            # Suunta 3
            if paasyt[2] and x + kerroin <= 7:
                siirtymat.append([kerroin, 0])
            else:
                siirtymat.append([0, 0])

            # Suunta 4
            if paasyt[3] and y - kerroin >= 1:
                siirtymat.append([0, -kerroin])
            else:
                siirtymat.append([0, 0])

            # Käsitellään kaikki suunnat
            for indeksi in range(0, 4):
                delta_x = siirtymat[indeksi][0]
                delta_y = siirtymat[indeksi][1]

                # Jos siirtymää ei ole, suuntaa ei tarvitse käsitellä nyt
                # eikä myöskään silmukan jatkuessa.
                if delta_x == 0 and delta_y == 0:
                    paasyt[indeksi] = False
                    continue

                ruutu = Teorialauta.KIRJAIMET[x + delta_x] + str(y + delta_y)
                if ruutu in oma_puoli:
                    paasyt[indeksi] = False
                elif ruutu in vast_puoli:
                    paasyt[indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)

        return siirrot

    def ratsun_liike(self, asema):
        """
        Apufunktio, joka tutkii ratsun liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Ratsu voi liikkua L-kirjaimen mukaisesti eli
        kaksi eteen, yhden sivulle. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta ratsu lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        valkoinen, musta = self.asemat()
        if asema in valkoinen:
            oma_puoli, vast_puoli = valkoinen, musta
        else:
            oma_puoli, vast_puoli = musta, valkoinen

        aseman_kirjain = asema[0]
        y = int(asema[1])
        x = Teorialauta.KIRJAIMET.index(aseman_kirjain)

        # Tallennetaan mahdolliset siirtymät pareiksi listaan muodossa
        # [[delta_x, delta_y]].
        siirtymat = []

        # Viitataan kommenteissa hevosen mahdollisiin siirtoihin näin:
        # * 1 * 2 *
        # 3 * * * 4
        # * * H * *
        # 5 * * * 6
        # * 7 * 8 *

        # Tarkistetaan siirrot 1 ja 2
        if y <= 6:
            # Siirto 1
            if x >= 1:
                siirtymat.append([-1, 2])

            # Siirto 2
            if x <= 6:
                siirtymat.append([1, 2])

        # Siirrot 3 ja 4
        if y <= 7:
            if x >= 2:
                siirtymat.append([-2, 1])
            if x <= 5:
                siirtymat.append([2, 1])

        # Siirrot 5 ja 6
        if y >= 2:
            if x >= 2:
                siirtymat.append([-2, -1])
            if x <= 5:
                siirtymat.append([2, -1])

        # Siirrot 7 ja 8
        if y >= 3:
            # Siirto 7
            if x >= 1:
                siirtymat.append([-1, -2])

            # Siirto 8
            if x <= 6:
                siirtymat.append([1, -2])

        # Muodostetaan ruudut merkkijonoina siirtymien perusteella ja
        # lisätään mahdollisiin siirtoihin
        for siirtyma in siirtymat:
            delta_x = siirtyma[0]
            delta_y = siirtyma[1]
            ruutu = Teorialauta.KIRJAIMET[x + delta_x] + str(y + delta_y)
            siirrot.append(ruutu)

        # Lopuksi poistetaan siirroista sellaiset ruudut,
        # jotka ovat varattuina omille nappuloille
        for ruutu in oma_puoli:
            if ruutu in siirrot:
                siirrot.remove(ruutu)

        return siirrot

    def lahetin_liike(self, asema):
        """
        Apufunktio, joka tutkii lähetin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Lähetti voi liikkua viistottain niin pitkälle
        kuin vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta lähetti lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        valkoinen, musta = self.asemat()
        if asema in valkoinen:
            oma_puoli, vast_puoli = valkoinen, musta
        else:
            oma_puoli, vast_puoli = musta, valkoinen

        aseman_kirjain = asema[0]
        y = int(asema[1])
        x = Teorialauta.KIRJAIMET.index(aseman_kirjain)

        # Viitataan kommenteissa lähetin suuntiin näin:
        # 1 * 2
        # * L *
        # 3 * 4

        # Pääseekö suuntiin [1, 2, 3, 4]

        paasyt = [True, True, True, True]
        for kerroin in range(1, 9):
            # Tallennetaan mahdolliset siirtymät pareiksi listaan muodossa
            # [[delta_x, delta_y]].
            siirtymat = []

            # Tarkistetaan suuntaan 1 pääsy
            if paasyt[0] and x - kerroin >= 0 and y + kerroin <= 8:
                siirtymat.append([-kerroin, kerroin])
            else:
                siirtymat.append([0, 0])

            # Suunta 2
            if paasyt[1] and x + kerroin <= 7 and y + kerroin <= 8:
                siirtymat.append([kerroin, kerroin])
            else:
                siirtymat.append([0, 0])

            # Suunta 3
            if paasyt[2] and x - kerroin >= 0 and y - kerroin >= 1:
                siirtymat.append([-kerroin, -kerroin])
            else:
                siirtymat.append([0, 0])

            # Suunta 4
            if paasyt[3] and x + kerroin <= 7 and y - kerroin >= 1:
                siirtymat.append([kerroin, -kerroin])
            else:
                siirtymat.append([0, 0])

            # Käsitellään kaikki suunnat
            for indeksi in range(0, 4):
                delta_x = siirtymat[indeksi][0]
                delta_y = siirtymat[indeksi][1]

                # Jos siirtymää ei ole, suuntaa ei tarvitse käsitellä nyt
                # eikä myöskään silmukan jatkuessa.
                if delta_x == 0 or delta_y == 0:
                    paasyt[indeksi] = False
                    continue

                ruutu = Teorialauta.KIRJAIMET[x + delta_x] + str(y + delta_y)
                if ruutu in oma_puoli:
                    paasyt[indeksi] = False
                elif ruutu in vast_puoli:
                    paasyt[indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)

        return siirrot

    def kuningattaren_liike(self, asema):
        """
        Apufunktio, joka tutkii kuningattaren liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Kuningattaren liikkeessä yhdistyvät tornin
        sekä lähetin liikkumismahdollisuudet, joten funktiokin on
        toteutettu siten.

        :param asema: str, ruudun koordinaatit, josta kuningatar lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        return self.tornin_liike(asema) + self.lahetin_liike(asema)

    def kuninkaan_liike(self, asema):
        """
        Apufunktio, joka tutkii kuninkaan liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Kuningas voi liikkua yhden askeleen joka
        suuntaan laudalla. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta kuningas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []

        valkoinen, musta = self.asemat()
        if asema in valkoinen:
            oma_puoli, vast_puoli = valkoinen, musta
        else:
            oma_puoli, vast_puoli = musta, valkoinen

        aseman_kirjain = asema[0]
        y = int(asema[1])
        x = Teorialauta.KIRJAIMET.index(aseman_kirjain)

        # Tallennetaan mahdolliset siirtymät pareiksi listaan muodossa
        # [[delta_x, delta_y]].
        siirtymat = []

        # Ylöspäin pääsee, jos ei olla jo laudan ylälaidassa
        if y <= 7:
            # Keskelle pääsee ilman lisärajoituksia
            siirtymat.append((0, 1))

            # Vasemmalle pääsee, jos ei jo olla vasemmassa laidassa
            if x >= 1:
                siirtymat.append((-1, 1))

            # Oikealle pääsee, jos ei jo olla oikeassa laidassa
            if x <= 6:
                siirtymat.append((1, 1))

        # Alaspäin peilaten
        if y >= 2:
            siirtymat.append((0, -1))

            if x >= 1:
                siirtymat.append((-1, -1))

            if x <= 6:
                siirtymat.append((1, -1))

        # Lisätään vielä suoraan sivulle menevät askeleet
        if x >= 1:
            siirtymat.append((-1, 0))
        if x <= 6:
            siirtymat.append((1, 0))

        # Muodostetaan ruudut merkkijonoina siirtymien perusteella ja
        # lisätään mahdollisiin siirtoihin
        for siirtyma in siirtymat:
            delta_x = siirtyma[0]
            delta_y = siirtyma[1]
            ruutu = Teorialauta.KIRJAIMET[x + delta_x] + str(y + delta_y)
            siirrot.append(ruutu)

        # Lopuksi poistetaan siirroista sellaiset ruudut,
        # jotka ovat varattuina omille nappuloille
        for ruutu in oma_puoli:
            if ruutu in siirrot:
                siirrot.remove(ruutu)

        # Tutkitaan linnoittamisen mahdollisuus

        # Valkoiselle
        if self.__valkoisen_kuningas_lahtoasemassa and asema == "e1":
            if self.__valkoisen_vasen_torni_lahtoasemassa and \
                    all([ruutu not in oma_puoli + vast_puoli for ruutu in
                         ["b1", "c1", "d1"]]):
                siirrot.append("c1")
                self.__linnoittaminen = True
            if self.__valkoisen_oikea_torni_lahtoasemassa and \
                    all([ruutu not in oma_puoli + vast_puoli for ruutu in
                         ["f1", "g1"]]):
                siirrot.append("g1")
                self.__linnoittaminen = True

        # Mustalle
        if self.__mustan_kuningas_lahtoasemassa and asema == "e8":
            if self.__mustan_vasen_torni_lahtoasemassa and \
                    all([ruutu not in oma_puoli + vast_puoli for ruutu in
                         ["b8", "c8", "d8"]]):
                siirrot.append("c8")
                self.__linnoittaminen = True
            if self.__mustan_oikea_torni_lahtoasemassa and \
                    all([ruutu not in oma_puoli + vast_puoli for ruutu in
                         ["f8", "g8"]]):
                siirrot.append("g8")
                self.__linnoittaminen = True

        return siirrot


def viereiset_kirjaimet(kirjain):
    """
    Apufunktio nappuloiden siirtomahdollisuuksien tutkimiseen. Palauttaa
    laudan koordinaattikirjaimen viereiset kirjaimet tai viereisen kirjaimen.

    :param kirjain: str, koordinaattikirjain.
    :return: str / str, str; viereiset koordinaattikirjaimet.
    """

    indeksi = Teorialauta.KIRJAIMET.index(kirjain)
    if indeksi == 0:
        return Teorialauta.KIRJAIMET[1]
    if indeksi == 7:
        return Teorialauta.KIRJAIMET[6]
    return Teorialauta.KIRJAIMET[indeksi-1], Teorialauta.KIRJAIMET[indeksi+1]


def shakkilaudan_koordinaatit():
    """
    Apufunktio, joka palauttaa shakkilaudan ruudut merkkijonojen listana
    ["a1", "a2", ..., "e8"].

    :return: [str, ...]; shakkilaudan ruudut.
    """

    ruudut = []
    for kirjain in Teorialauta.KIRJAIMET:
        for numero in range(1, 9):
            ruudut.append(kirjain + str(numero))
    return ruudut
