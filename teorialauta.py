"""
Tämä tiedosto esittelee luokan Teorialauta, joka vastaa shakkipelin
teoreettisesta pyörittämisestä. Tätä tiedostoa on kehitetty vastaamaan niin
graafisen käyttöliittymän kuin shakkikoneen kouluttamisen tarpeisiin.
"""

from copy import deepcopy


class Teorialauta:
    # Pelin lähtöasema
    ALOITUSASEMAT = [
        0b0000000000000000000000000000000000000000000000001111111100000000,
        0b0000000000000000000000000000000000000000000000000000000010000001,
        0b0000000000000000000000000000000000000000000000000000000001000010,
        0b0000000000000000000000000000000000000000000000000000000000100100,
        0b0000000000000000000000000000000000000000000000000000000000001000,
        0b0000000000000000000000000000000000000000000000000000000000010000,
        0b0000000011111111000000000000000000000000000000000000000000000000,
        0b1000000100000000000000000000000000000000000000000000000000000000,
        0b0100001000000000000000000000000000000000000000000000000000000000,
        0b0010010000000000000000000000000000000000000000000000000000000000,
        0b0000100000000000000000000000000000000000000000000000000000000000,
        0b0001000000000000000000000000000000000000000000000000000000000000]

    def __init__(self, siirtonumero=None, lahtoasemat=None,
                 liikkumistiedot=None, shakit=None):
        """
        Rakentaa teorialaudan eli aloittaa uuden teoreettisen shakkipelin
        lähtöasemasta.
        """

        if not siirtonumero:
            self.__siirtonumero = 1
        else:
            self.__siirtonumero = deepcopy(siirtonumero)

        # Laudan asetelma
        if not lahtoasemat:
            self.__asemat = deepcopy(Teorialauta.ALOITUSASEMAT)
        else:
            self.__asemat = deepcopy(lahtoasemat)

        # Castlingia varten pidetään kirjaa näistä
        if not liikkumistiedot:
            self.__valkoisen_vasen_torni_lahtoasemassa = True
            self.__valkoisen_vasen_reitti_uhattuna = False
            self.__valkoisen_oikea_torni_lahtoasemassa = True
            self.__valkoisen_oikea_reitti_uhattuna = False
            self.__valkoisen_kuningas_lahtoasemassa = True
            self.__mustan_vasen_torni_lahtoasemassa = True
            self.__mustan_vasen_reitti_uhattuna = False
            self.__mustan_oikea_torni_lahtoasemassa = True
            self.__mustan_oikea_reitti_uhattuna = False
            self.__mustan_kuningas_lahtoasemassa = True

        else:
            self.__valkoisen_vasen_torni_lahtoasemassa, \
                self.__valkoisen_vasen_reitti_uhattuna, \
                self.__valkoisen_oikea_torni_lahtoasemassa, \
                self.__valkoisen_oikea_reitti_uhattuna, \
                self.__valkoisen_kuningas_lahtoasemassa, \
                self.__mustan_vasen_torni_lahtoasemassa, \
                self.__mustan_vasen_reitti_uhattuna, \
                self.__mustan_oikea_torni_lahtoasemassa, \
                self.__mustan_oikea_reitti_uhattuna, \
                self.__mustan_kuningas_lahtoasemassa \
                = deepcopy(liikkumistiedot)

        if not shakit:
            self.__valkoinen_shakissa = False
            self.__musta_shakissa = False
        else:
            self.__valkoinen_shakissa = shakit[0]
            self.__musta_shakissa = shakit[1]

        self.__linnoittaminen = False

        self.__voittaja = None

    def tee_siirto(self, asema, siirto):
        """
        Funktio, jolla asemat muuttuvat annetun siirron mukaisesti.

        :param asema: int, indeksi, jolla lähtöruudun löytää
                         binäärilaudoilta.
        :param siirto: int, indeksi, jolla siirtoruudun löytää
                         binäärilaudoilta.
        """

        valkoisen_siirto = self.__siirtonumero % 2 == 1
        if valkoisen_siirto:
            ennen_shakissa = self.__valkoinen_shakissa
        else:
            ennen_shakissa = self.__musta_shakissa

        # Normaali siirtäminen
        # Käydään läpi tallennettuja asemia

        indeksi = 0

        for i in range(0, 12):
            if self.__asemat[i] >> siirto & 1 == 1:
                self.__asemat[i] &= ~(1 << siirto)

        for i in range(0, 12):
            if self.__asemat[i] >> asema & 1 == 1:
                self.__asemat[i] |= (1 << siirto)
                self.__asemat[i] &= ~(1 << asema)

        # Linnoittamista varten:
        if (indeksi == 1 and asema == 0) or \
                (indeksi >= 6 and siirto == 0):
            self.__valkoisen_vasen_torni_lahtoasemassa = False

        if (indeksi == 1 and asema == 7) or \
                (indeksi >= 6 and siirto == 7):
            self.__valkoisen_oikea_torni_lahtoasemassa = False

        if (indeksi == 7 and asema == 56) or \
                (indeksi < 6 and siirto == 56):
            self.__mustan_vasen_torni_lahtoasemassa = False

        if (indeksi == 7 and asema == 63) or \
                (indeksi < 6 and siirto == 63):
            self.__mustan_oikea_torni_lahtoasemassa = False

        if asema == 4 or (indeksi >= 6 and siirto == 4):
            self.__valkoisen_kuningas_lahtoasemassa = False
        if asema == 60 or (indeksi < 6 and siirto == 60):
            self.__mustan_kuningas_lahtoasemassa = False

        indeksi += 1

        # Jos linnoittaminen tapahtuu, myös tornit siirtyvät
        if self.__linnoittaminen:

            if asema == 4 and siirto == 2:
                self.__asemat[1] &= ~(1 << 0)
                self.__asemat[1] |= (1 << 3)

            elif asema == 4 and siirto == 6:
                self.__asemat[1] &= ~(1 << 7)
                self.__asemat[1] |= (1 << 5)

            elif asema == 60 and siirto == 58:
                self.__asemat[7] &= ~(1 << 56)
                self.__asemat[7] |= (1 << 59)

            elif asema == 60 and siirto == 62:
                self.__asemat[7] &= ~(1 << 63)
                self.__asemat[7] |= (1 << 61)

            else:
                self.__linnoittaminen = False

        # Kuningattareksi nousu sotilaalle laudan päädyssä
        if self.__asemat[0] >> siirto & 1 == 1 and (56 <= siirto <= 63):
            self.__asemat[0] &= ~(1 << siirto)
            self.__asemat[4] |= (1 << siirto)

        if self.__asemat[6] >> siirto & 1 == 1 and (0 <= siirto <= 7):
            self.__asemat[6] &= ~(1 << siirto)
            self.__asemat[10] |= (1 << siirto)

        # Päivitä siirtonumero ja shakkitilanne
        self.__siirtonumero += 1
        self.tarkista_shakit()

        if valkoisen_siirto:
            if (ennen_shakissa and self.__valkoinen_shakissa) \
                    or self.__asemat[5] == 0:
                self.__voittaja = "musta"

        else:
            if (ennen_shakissa and self.__musta_shakissa) \
                    or self.__asemat[11] == 0:
                self.__voittaja = "valkoinen"

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

        :return: [int, ...], listat jokaisen nappulatyypin bittilaudoista.
        """

        return self.__asemat

    def liikkumistiedot(self):
        """
        Apufunktio, joka palauttaa liikkumistiedot, joita seurataan
        linnoittamisen varalta.

        :return: [bool, ...]; onko jokin nappuloista liikkunut.
        """

        return self.__valkoisen_vasen_torni_lahtoasemassa, \
            self.__valkoisen_vasen_reitti_uhattuna, \
            self.__valkoisen_oikea_torni_lahtoasemassa, \
            self.__valkoisen_oikea_reitti_uhattuna, \
            self.__valkoisen_kuningas_lahtoasemassa, \
            self.__mustan_vasen_torni_lahtoasemassa, \
            self.__mustan_vasen_reitti_uhattuna, \
            self.__mustan_oikea_torni_lahtoasemassa, \
            self.__mustan_oikea_reitti_uhattuna, \
            self.__mustan_kuningas_lahtoasemassa

    def shakit(self):
        """
        Apufunktio, joka palauttaa tiedon shakkitilanteesta.

        return: bool, bool, onko kuninkaat shakissa.
        """

        return self.__valkoinen_shakissa, self.__musta_shakissa

    def voittaja(self):
        """
        Apufunktio, joka palauttaa tiedon voittajasta.

        return: str/None, voittanut puoli.
        """

        return self.__voittaja

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

        valkoisen_materiaali = bin(self.__asemat[0]).count('1') \
            + bin(self.__asemat[1]).count('1')*5 \
            + bin(self.__asemat[2]).count('1')*3 \
            + bin(self.__asemat[3]).count('1')*3 \
            + bin(self.__asemat[4]).count('1')*9

        mustan_materiaali = bin(self.__asemat[6]).count('1') \
            + bin(self.__asemat[7]).count('1')*5 \
            + bin(self.__asemat[8]).count('1')*3 \
            + bin(self.__asemat[9]).count('1')*3 \
            + bin(self.__asemat[10]).count('1')*9

        return valkoisen_materiaali, mustan_materiaali

    def ruudun_nappulan_tiedot(self, asema):
        """
        Apufunktio, joka palauttaa tietoa annetusta ruudussa olevasta
        nappulasta.

        :param asema: int, indeksi ruudulle, jossa etsitty nappula on.
        :return: str, str, int; nappulan väri, tyyppi sekä bittilauta sen
                 mahdollisista siirroista.
        """

        vari = "White"
        tyyppi = ""
        siirrot = 0

        for i in range(0, 12):
            if i == 6:
                vari = "Black"

            if self.__asemat[i] >> asema & 1 == 1:
                if i == 0 or i == 6:
                    tyyppi = "Sotilas"
                    siirrot = self.sotilaan_liike(asema)
                elif i == 1 or i == 7:
                    tyyppi = "Torni"
                    siirrot = self.tornin_liike(asema)
                elif i == 2 or i == 8:
                    tyyppi = "Ratsu"
                    siirrot = self.ratsun_liike(asema)
                elif i == 3 or i == 9:
                    tyyppi = "Lähetti"
                    siirrot = self.lahetin_liike(asema)
                elif i == 4 or i == 10:
                    tyyppi = "Kuningatar"
                    siirrot = self.kuningattaren_liike(asema)
                elif i == 5 or i == 11:
                    tyyppi = "Kuningas"
                    siirrot = self.kuninkaan_liike(asema)

                return vari, tyyppi, siirrot

    def tarkista_shakit(self):
        """
        Apufunktio, jolla voi päivittää, onko kuninkaat shakitettuina.
        """

        # Oletetaan, että kuninkaat eivät ole shakissa
        self.__valkoinen_shakissa = False
        self.__musta_shakissa = False

        for avain in self.puolen_kaikki_siirrot("musta"):
            lauta = self.puolen_kaikki_siirrot("musta")[avain]

            if self.__asemat[5] & lauta != 0:
                self.__valkoinen_shakissa = True

            if lauta >> 1 & 1 == 1 or lauta >> 2 & 1 == 1 or \
                    lauta >> 3 & 1 == 1:
                self.__valkoisen_vasen_reitti_uhattuna = True

            if lauta >> 5 & 1 == 1 or lauta >> 6 & 1 == 1:
                self.__valkoisen_oikea_reitti_uhattuna = True

        for avain in self.puolen_kaikki_siirrot("valkoinen"):
            lauta = self.puolen_kaikki_siirrot("valkoinen")[avain]

            if self.__asemat[11] & lauta != 0:
                self.__musta_shakissa = True

            if lauta >> 57 & 1 == 1 or lauta >> 58 & 1 == 1 or \
                    lauta >> 59 & 1 == 1:
                self.__mustan_vasen_reitti_uhattuna = True

            if lauta >> 61 & 1 == 1 or lauta >> 62 & 1 == 1:
                self.__mustan_oikea_reitti_uhattuna = True

    def puolen_kaikki_siirrot(self, puoli):
        """
        Apufunktio, joka palauttaa puolen kaikki mahdolliset siirrot.

        :param puoli: str, valittu puoli, musta tai valkoinen.
        :return: {int: int}, sanakirja nappulan sijainnista linkitettyinä
                 sen mahdollisten siirtymäruutujen bittilautaan.
        """

        siirrot = {}

        if puoli == "valkoinen":
            alku = 0
            loppu = 6
        else:
            alku = 6
            loppu = 12

        for asema in range(64):
            for i in range(alku, loppu):
                if self.__asemat[i] >> asema & 1 == 1:
                    if i == 0 or i == 6:
                        siirrot.update(
                            {asema: self.sotilaan_liike(asema, False)})
                    elif i == 1 or i == 7:
                        siirrot.update(
                            {asema: self.tornin_liike(asema, False)})
                    elif i == 2 or i == 8:
                        siirrot.update(
                            {asema: self.ratsun_liike(asema, False)})
                    elif i == 3 or i == 9:
                        siirrot.update(
                            {asema: self.lahetin_liike(asema, False)})
                    elif i == 4 or i == 10:
                        siirrot.update(
                            {asema: self.kuningattaren_liike(asema, False)})
                    elif i == 5 or i == 11:
                        siirrot.update(
                            {asema: self.kuninkaan_liike(asema, False)})

        return siirrot

    def sotilaan_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii valkoisen sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Sotilaat voivat liikkua
        kaksi askelta eteen ensimmäisellä siirrollaan, sen jälkeen vain
        yhden. Sotilas voi myös syödä vastustajan pelinappulan yhden
        askeleen päästä viistottain.

        :param asema: int, indeksi ruudulle, josta sotilas lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        siirrot = 0

        valkoiset = 0
        for i in range(0, 6):
            valkoiset |= self.__asemat[i]

        mustat = 0
        for i in range(6, 12):
            mustat |= self.__asemat[i]

        if valkoiset >> asema & 1 == 1:
            omat = valkoiset
            vastustajat = mustat

            kerroin = 1
            alaraja = 7
            ylaraja = 16
        else:
            omat = mustat
            vastustajat = valkoiset
            kerroin = -1

            alaraja = 47
            ylaraja = 56

        varatut = omat | vastustajat

        siirto = asema + kerroin*8
        if varatut >> siirto & 1 == 0:
            siirrot |= (1 << siirto)

            if alaraja < asema < ylaraja:
                siirto = asema + kerroin*16
                if varatut >> siirto & 1 == 0:
                    siirrot |= (1 << siirto)

        siirto = asema + kerroin*8 - 1
        if siirto >= 0:
            if vastustajat >> siirto & 1 == 1:
                siirrot |= (1 << siirto)

        siirto = asema + kerroin * 8 + 1
        if siirto <= 63:
            if vastustajat >> siirto & 1 == 1:
                siirrot |= (1 << siirto)

        # Estetään shakkiin siirtäminen, jos vaadittu
        if esta_shakki:
            return self.esta_siirtaminen_shakkiin(asema, siirrot)

        return siirrot

    def tornin_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii tornin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Torni voi liikkua
        suorasti niin pitkälle, kunnes kohtaa seinän tai nappulan.

        :param asema: int, indeksi ruudulle, josta torni lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        # Viitataan tornin siirtosuuntiin näin:
        # * y *
        # v T o
        # * a *

        siirrot = 0

        valkoiset = 0
        for i in range(0, 6):
            valkoiset |= self.__asemat[i]

        mustat = 0
        for i in range(6, 12):
            mustat |= self.__asemat[i]

        if valkoiset >> asema & 1 == 1:
            omat = valkoiset
            vastustajat = mustat
        else:
            omat = mustat
            vastustajat = valkoiset

        # Pääseekö suuntiin [y, o, a, v]
        paasyt = [True, True, True, True]

        for kerroin in range(0, 8):
            # y
            if paasyt[0]:
                y = asema + (kerroin+1)*8

                if asema + kerroin*8 < 56 and omat >> y & 1 == 0:
                    siirrot |= (1 << y)

                    if vastustajat >> y & 1 == 1:
                        paasyt[0] = False
                else:
                    paasyt[0] = False

            # o
            if paasyt[1]:
                o = asema+kerroin + 1

                if (asema+kerroin) % 8 != 7 and omat >> o & 1 == 0:
                    siirrot |= (1 << o)

                    if vastustajat >> o & 1 == 1:
                        paasyt[1] = False

                else:
                    paasyt[1] = False

            # a
            if paasyt[2]:
                a = asema - (kerroin+1)*8

                if asema - kerroin*8 > 7 and omat >> a & 1 == 0:
                    siirrot |= (1 << a)

                    if vastustajat >> a & 1 == 1:
                        paasyt[2] = False

                else:
                    paasyt[2] = False

            # v
            if paasyt[3]:
                v = asema-kerroin - 1

                if (asema-kerroin) % 8 != 0 and omat >> v & 1 == 0:
                    siirrot |= (1 << v)

                    if vastustajat >> v & 1 == 1:
                        paasyt[3] = False

                else:
                    paasyt[3] = False

        # Estetään shakkiin siirtäminen, jos vaadittu
        if esta_shakki:
            return self.esta_siirtaminen_shakkiin(asema, siirrot)

        return siirrot

    def ratsun_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii ratsun liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Ratsu voi liikkua
        L-kirjaimen mukaisesti eli kaksi eteen, yhden sivulle.

        :param asema: int, indeksi ruudulle, josta ratsu lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        # Viitataan ratsun mahdollisiin siirtoihin näin:
        # * 1 * 2 *
        # 3 * * * 4
        # * * R * *
        # 5 * * * 6
        # * 7 * 8 *

        siirrot = 0

        # Kahteen kertaan laskeminen vältetään tarkistamalla nämä etukäteen
        o1 = asema % 8 < 7
        o2 = asema % 8 < 6
        v1 = asema % 8 > 0
        v2 = asema % 8 > 1

        # Siirrot 1 ja 2
        if asema < 48:
            if v1:
                siirrot |= (1 << asema + 15)
            if o1:
                siirrot |= (1 << asema + 17)

        # Siirrot 3 ja 4
        if asema < 56:
            if v2:
                siirrot |= (1 << asema + 6)
            if o2:
                siirrot |= (1 << asema + 10)

        # Siirrot 5 ja 6
        if asema > 7:
            if v2:
                siirrot |= (1 << asema - 10)
            if o2:
                siirrot |= (1 << asema - 6)

        # Siirrot 7 ja 8
        if asema > 15:
            if v1:
                siirrot |= (1 << asema - 17)
            if o1:
                siirrot |= (1 << asema - 15)

        # Lopuksi poistetaan siirroista sellaiset ruudut,
        # jotka ovat varattuina omille nappuloille

        if self.__asemat[2] >> asema & 1 == 1:
            alku = 0
            loppu = 6
        else:
            alku = 6
            loppu = 12

        omat = 0
        for i in range(alku, loppu):
            omat |= self.__asemat[i]

        siirrot &= ~omat

        # Estetään shakkiin siirtäminen, jos vaadittu
        if esta_shakki:
            return self.esta_siirtaminen_shakkiin(asema, siirrot)

        return siirrot

    def lahetin_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii lähetin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Lähetti voi liikkua
        viistottain niin pitkälle, kunnes kohtaa seinän tai nappulan.

        :param asema: int, indeksi ruudulle, josta lähetti lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        # Viitataan lähetin siirtosuuntiin näin:
        # yv * yo
        # *  L  *
        # av * ao

        siirrot = 0

        valkoiset = 0
        for i in range(0, 6):
            valkoiset |= self.__asemat[i]

        mustat = 0
        for i in range(6, 12):
            mustat |= self.__asemat[i]

        if valkoiset >> asema & 1 == 1:
            omat = valkoiset
            vastustajat = mustat
        else:
            omat = mustat
            vastustajat = valkoiset

        # Pääseekö suuntiin [y, o, a, v]
        paasyt = [True, True, True, True]

        for kerroin in range(0, 8):
            # yv
            if paasyt[0]:
                yv = asema + (kerroin + 1) * 8 - (kerroin + 1)

                if (asema + kerroin * 8 < 56 and (asema - kerroin) % 8 != 0
                        and omat >> yv & 1 == 0):
                    siirrot |= (1 << yv)

                    if vastustajat >> yv & 1 == 1:
                        paasyt[0] = False
                else:
                    paasyt[0] = False

            # yo
            if paasyt[1]:
                yo = asema + (kerroin + 1) * 8 + (kerroin + 1)

                if (asema + kerroin * 8 < 56 and (asema + kerroin) % 8 != 7
                        and omat >> yo & 1 == 0):
                    siirrot |= (1 << yo)

                    if vastustajat >> yo & 1 == 1:
                        paasyt[1] = False

                else:
                    paasyt[1] = False

            # ao
            if paasyt[2]:
                ao = asema - (kerroin + 1) * 8 + (kerroin + 1)

                if (asema - kerroin * 8 > 7 and (asema + kerroin) % 8 != 7
                        and omat >> ao & 1 == 0):
                    siirrot |= (1 << ao)

                    if vastustajat >> ao & 1 == 1:
                        paasyt[2] = False

                else:
                    paasyt[2] = False

            # av
            if paasyt[3]:
                av = asema - (kerroin+1)*8 - (kerroin+1)

                if (asema - kerroin * 8 > 7 and (asema - kerroin) % 8 != 0
                        and omat >> av & 1 == 0):
                    siirrot |= (1 << av)

                    if vastustajat >> av & 1 == 1:
                        paasyt[3] = False

                else:
                    paasyt[3] = False

        # Estetään shakkiin siirtäminen, jos vaadittu
        if esta_shakki:
            return self.esta_siirtaminen_shakkiin(asema, siirrot)

        return siirrot

    def kuningattaren_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii kuningattaren liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Kuningattaren liikkeessä
        yhdistyvät tornin sekä lähetin liikkumismahdollisuudet,
        joten funktiokin on myös toteutettu siten.

        :param asema: int, indeksi ruudulle, josta kuningatar lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        return self.tornin_liike(asema, esta_shakki) | self.lahetin_liike(
            asema, esta_shakki)

    def kuninkaan_liike(self, asema, esta_shakki=True):
        """
        Apufunktio, joka tutkii kuninkaan liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet sisältävän bittilaudan. Kuningas voi liikkua
        yhden askeleen joka suuntaan laudalla.

        :param asema: int, indeksi ruudulle, josta kuningas lähtee.
        :param esta_shakki: bool, eliminoidaanko pelin häviävät siirrot.
        :return: int, bittilauta siirtomahdollisuuksista.
        """

        # Viitataan kuninkaan siirtoihin näin:
        # yv y yo
        # v  K  o
        # av a ao

        siirrot = 0

        valkoiset = 0
        for i in range(0, 6):
            valkoiset |= self.__asemat[i]

        mustat = 0
        for i in range(6, 12):
            mustat |= self.__asemat[i]

        # Pääseekö suuntiin [y, o, a, v]
        paasyt = [asema < 56, asema % 8 != 7, asema > 7, asema % 8 != 0]

        if paasyt[0]:
            # y
            siirrot |= (1 << (asema + 8))

            if paasyt[1]:
                # yo
                siirrot |= (1 << (asema + 9))
            if paasyt[3]:
                # yv
                siirrot |= (1 << (asema + 7))

        if paasyt[2]:
            # a
            siirrot |= (1 << (asema - 8))

            if paasyt[1]:
                # ao
                siirrot |= (1 << (asema - 7))
            if paasyt[3]:
                # av
                siirrot |= (1 << (asema - 9))

        if paasyt[1]:
            # o
            siirrot |= (1 << (asema + 1))
        if paasyt[3]:
            # v
            siirrot |= (1 << (asema - 1))

        # Poistetaan siirroista ruudut, joissa on omia nappuloita
        if self.__asemat[5] >> asema & 1 == 1:
            siirrot &= ~valkoiset

        else:
            siirrot &= ~mustat

        # Tutkitaan vielä linnoittamisen mahdollisuutta
        varatut = valkoiset | mustat

        # Valkoiselle
        if self.__valkoisen_kuningas_lahtoasemassa and asema == 4:
            if self.__valkoisen_vasen_torni_lahtoasemassa and \
                not self.__valkoisen_vasen_reitti_uhattuna and \
                varatut >> 1 & 1 == 0 and varatut >> 2 & 1 == 0 and \
                    varatut >> 3 & 1 == 0:
                siirrot |= (1 << 2)
                self.__linnoittaminen = True

            if self.__valkoisen_oikea_torni_lahtoasemassa and \
                not self.__valkoisen_oikea_reitti_uhattuna and \
                    varatut >> 5 & 1 == 0 and varatut >> 6 & 1 == 0:
                siirrot |= (1 << 6)
                self.__linnoittaminen = True

        # Mustalle
        if self.__mustan_kuningas_lahtoasemassa and asema == 60:
            if self.__mustan_vasen_torni_lahtoasemassa and \
                not self.__mustan_vasen_reitti_uhattuna and \
                varatut >> 57 & 1 == 0 and varatut >> 58 & 1 == 0 and \
                    varatut >> 59 & 1 == 0:
                siirrot |= (1 << 58)
                self.__linnoittaminen = True

            if self.__mustan_oikea_torni_lahtoasemassa and \
                not self.__mustan_oikea_reitti_uhattuna and \
                    varatut >> 61 & 1 == 0 and varatut >> 62 & 1 == 0:
                siirrot |= (1 << 62)
                self.__linnoittaminen = True

        # Estetään shakkiin siirtäminen, jos vaadittu
        if esta_shakki:
            return self.esta_siirtaminen_shakkiin(asema, siirrot)

        return siirrot

    def esta_siirtaminen_shakkiin(self, asema, siirrot):
        """
        Apufunktio, joka suodattaa pois automaattisesti häviävät siirrot.

        :param asema: int, indeksi ruudulle, josta nappula on.
        :param siirrot: int, bittilauta siirtomahdollisuuksista.
        :return: int, bittilauta suodatetuista siirtomahdollisuuksista.
        """

        indeksi = 0

        siirrot_alkup = siirrot
        while siirrot:
            if siirrot & 1:
                valkoisen_siirto = self.__siirtonumero % 2 == 1

                uusi_lauta = Teorialauta(self.__siirtonumero, self.__asemat,
                                         self.liikkumistiedot(),
                                         self.shakit())
                uusi_lauta.tee_siirto(asema, indeksi)

                if (valkoisen_siirto and uusi_lauta.__valkoinen_shakissa) or \
                        (not valkoisen_siirto and uusi_lauta.__musta_shakissa):
                    siirrot_alkup &= ~(1 << indeksi)

            siirrot >>= 1
            indeksi += 1

        return siirrot_alkup
