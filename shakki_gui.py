"""
Tähän tiedostoon on toteutettu graafinen käyttöliittymä. Käyttöliittymän avulla
käyttäjä voi pelata shakkia joko kaksinpelinä tai yksinpelinä.
"""

from tkinter import *
from teorialauta import Teorialauta
from koulutus import arvioi_paras_siirto, muuttujat_tiedostosta


# Ulkoasu
IKKUNAN_TAUSTAVARI = "#424242"
IKKUNAN_FONTTI = "Kozuka Gothic Pro B", 18, "bold"
IKKUNAN_FONTIN_VARI = "#ffffff"
PELILAUDAN_FONTTI = "Kozuka Gothic Pro B", 12
# Shakkilaudan ruudut
TUMMA_RUUTU = "#66452d"
VAALEA_RUUTU = "#c9a565"


class Shakkilauta:
    def __init__(self):
        """
        Rakentaa käyttöliittymän pohjan ja siirtyy automaattisesti
        päävalikkoon. Fontin koko muuttaa toistaiseksi myös ruudukon kokoa,
        joten tämä voi vaatia muutoksia.
        """

        # Määritetään pääikkunä
        self.__paaikkuna = Tk()
        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.configure(bg=IKKUNAN_TAUSTAVARI, relief="solid")
        self.__paaikkuna.resizable(width=False, height=False)
        # Ideana asettaa ikkuna hieman koko näyttöä pienemmäksi
        # ja keskelle näyttöä
        self.__ruudun_koko = self.__paaikkuna.winfo_screenheight() // 10
        self.__maksimileveys_tekstille = self.__ruudun_koko // 8
        ikkunan_leveys = str(self.__ruudun_koko * 8)
        ikkunan_korkeus = str(self.__ruudun_koko * 9)
        leveyden_keskikohta = str(self.__paaikkuna.winfo_screenwidth()//2
                                  - int(ikkunan_leveys)//2)
        self.__paaikkuna.geometry(ikkunan_leveys+"x"+ikkunan_korkeus
                                  + "+"+leveyden_keskikohta+"+"+"0")

        self.__pelilauta = None
        self.__muuttujat = muuttujat_tiedostosta("tulokset.txt")

        self.__ruudut_nappeina = []
        # Pelimuodot
        # 0 = ei peliä
        # 1 = kaksinpeli
        # 2 = yksinpeli valkoisella
        # 3 = yksinpeli mustalla
        self.__pelimuoto = 0

        # Alustetaan pelin napit
        # Kahden pelaajan välinen ottelu
        self.__kaksinpeli = Button(self.__paaikkuna, relief="flat",
                                   overrelief="flat")
        # Pelaaja vastaan tietokone
        self.__yksinpeli_valk = Button(self.__paaikkuna, relief="flat",
                                       overrelief="flat")

        self.__yksinpeli_must = Button(self.__paaikkuna, relief="flat",
                                       overrelief="flat")
        # Koko näytölle asettaminen
        self.__koko_naytto = Button(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                                    activebackground=IKKUNAN_TAUSTAVARI,
                                    relief="flat", overrelief="flat",
                                    text="Koko näyttö", font=IKKUNAN_FONTTI,
                                    fg=IKKUNAN_FONTIN_VARI,
                                    activeforeground=IKKUNAN_FONTIN_VARI,
                                    command=self.koko_naytto)
        # Sulkeminen
        self.__sulje = Button(self.__paaikkuna,
                              bg=IKKUNAN_TAUSTAVARI,
                              activebackground=IKKUNAN_TAUSTAVARI,
                              relief="flat", overrelief="flat",
                              text="Sulje peli", font=IKKUNAN_FONTTI,
                              fg=IKKUNAN_FONTIN_VARI,
                              activeforeground=IKKUNAN_FONTIN_VARI,
                              command=self.__paaikkuna.destroy)
        # Päivitettävä teksti
        self.__tilateksti = Label(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                                  font=IKKUNAN_FONTTI, fg=IKKUNAN_FONTIN_VARI)

        # Käynnistetään päävalikko
        self.paavalikko()

    def paavalikko(self):
        """
        Muodostaa päävalikon, josta oikea suoritustapa voidaan valita.
        """

        # Tuhoa tarvittaessa käynnissä ollut peli
        for ruutu in self.__ruudut_nappeina:
            ruutu.destroy()

        self.__pelimuoto = 0
        self.__tilateksti.configure(text="Päävalikko")
        self.__tilateksti.grid(row=0, column=0, columnspan=4, sticky="nsew",
                               ipadx=0, ipady=0, padx=0, pady=0)
        self.__koko_naytto.grid(row=0, column=4, columnspan=2, sticky="nsew",
                                ipadx=0, ipady=0, padx=0, pady=0)
        self.__sulje.configure(text="Sulje peli",
                               command=self.__paaikkuna.destroy)
        self.__sulje.grid(row=0, column=6, columnspan=2, sticky="nsew",
                          ipadx=0, ipady=0, padx=0, pady=0)
        self.__kaksinpeli.configure(bg=IKKUNAN_TAUSTAVARI,
                                    activebackground=IKKUNAN_TAUSTAVARI,
                                    text="Kaksinpeli", font=IKKUNAN_FONTTI,
                                    fg=IKKUNAN_FONTIN_VARI,
                                    activeforeground=IKKUNAN_FONTIN_VARI,
                                    command=self.kaksinpeli)
        self.__kaksinpeli.grid(row=1, column=2, rowspan=2, columnspan=4,
                               sticky="nsew")
        self.__yksinpeli_valk.configure(bg=IKKUNAN_TAUSTAVARI,
                                        activebackground=IKKUNAN_TAUSTAVARI,
                                        text="Yksinpeli valkoisella",
                                        font=IKKUNAN_FONTTI,
                                        fg=IKKUNAN_FONTIN_VARI,
                                        activeforeground=IKKUNAN_FONTIN_VARI,
                                        command=lambda tieto="valkoinen":
                                            self.yksinpeli(tieto))
        self.__yksinpeli_valk.grid(row=3, column=2, rowspan=2, columnspan=4,
                                   sticky="nsew")
        self.__yksinpeli_must.configure(bg=IKKUNAN_TAUSTAVARI,
                                        activebackground=IKKUNAN_TAUSTAVARI,
                                        text="Yksinpeli mustalla",
                                        font=IKKUNAN_FONTTI,
                                        fg=IKKUNAN_FONTIN_VARI,
                                        activeforeground=IKKUNAN_FONTIN_VARI,
                                        command=lambda tieto="musta":
                                        self.yksinpeli(tieto))
        self.__yksinpeli_must.grid(row=5, column=2, rowspan=2, columnspan=4,
                                   sticky="nsew")

        for sarake in range(0, 8):
            self.__paaikkuna.grid_columnconfigure(index=sarake, pad=0,
                                                  minsize=self.__ruudun_koko)
        for rivi in range(0, 9):
            self.__paaikkuna.grid_rowconfigure(index=rivi, pad=0,
                                               minsize=self.__ruudun_koko)

        self.__paaikkuna.grid_anchor("n")

    def kaksinpeli(self):
        """
        Apufunktio, toiminnallisuus päävalikon napille, jolla kaksi käyttäjää
        voi pelata vastakkain.
        """

        self.__pelimuoto = 1
        self.pelin_aloitus()
        self.laudan_pohja()
        self.aseta_nappulat_ja_tarkista_shakit()
        self.kaksinpelin_vuorot()

    def kaksinpelin_vuorot(self):
        """
        Apufunktio, joka hoitaa yksinpelin vuoronvaihtotoimenpiteet. Näitä
        ovat siirtonumeron päivitys, voiton tarkistaminen ja sen jälkeen
        siirron mahdollistaminen sekä pelaajalle että tietokoneelle.
        """

        # Päivitetään tilateksti
        self.__tilateksti.configure(text="Siirto " + str(
            self.__pelilauta.siirtonumero()))

        # Voitto tarkistetaan eri tavalla kahden pelaajan välisissä otteluissa
        valkoinen_siirtovuorossa = self.__pelilauta.siirtonumero() % 2 == 1

        if valkoinen_siirtovuorossa:
            alku = 0
            loppu = 6
        else:
            alku = 6
            loppu = 12

        asemat = 0
        for i in range(alku, loppu):
            asemat |= self.__pelilauta.asemat()[i]

        # Tarkastatetaan, onko siirtäjällä enää siirtoja jäljellä
        # Oletuksena ei
        siirtoja_jaljella = False
        for ruutu in range(0, 64):
            if asemat >> ruutu & 1 == 0:
                continue

            _, _, siirrot = \
                self.__pelilauta.ruudun_nappulan_tiedot(ruutu)

            # Siirtoja löytyy
            if siirrot:
                siirtoja_jaljella = True

        if not siirtoja_jaljella:
            if valkoinen_siirtovuorossa:
                # Musta on voittanut pelin
                self.__tilateksti.configure(text="Peli on päättynyt, "
                                                 "musta voitti!")

            else:
                # Valkoinen on voittanut pelin
                self.__tilateksti.configure(text="Peli on päättynyt, "
                                                 "valkoinen voitti!")

            return

        self.aktivoi_oikean_puolen_napit()

    def yksinpeli(self, puoli):
        """
        Apufunktio, toiminnallisuus päävalikon napille, jolla käyttäjä voi
        pelata yksinpeliä tietokonetta vastaan.
        """

        self.pelin_aloitus()
        self.laudan_pohja()
        self.aseta_nappulat_ja_tarkista_shakit()

        if puoli == "valkoinen":
            self.__pelimuoto = 2
        else:
            self.__pelimuoto = 3

        self.yksinpelin_vuorot()

    def yksinpelin_vuorot(self):
        """
        Apufunktio, joka hoitaa yksinpelin vuoronvaihtotoimenpiteet. Näitä
        ovat siirtonumeron päivitys, voiton tarkistaminen ja sen jälkeen
        siirron mahdollistaminen sekä pelaajalle että tietokoneelle.
        """

        # Päivitetään tilateksti
        self.__tilateksti.configure(text="Siirto " + str(
            self.__pelilauta.siirtonumero()))

        # Tarkistetaan voitto
        if self.__pelilauta.voittaja() == "valkoinen":
            # Valkoinen on voittanut pelin
            self.__tilateksti.configure(text="Peli on päättynyt, valkoinen "
                                             "voitti!")
            return
        if self.__pelilauta.voittaja() == "musta":
            # Musta on voittanut pelin
            self.__tilateksti.configure(text="Peli on päättynyt, "
                                             "musta voitti!")
            return

        # Siirtonumerosta ja pelimuodosta riippuen mahdollistetaan pelaajan
        # tai tietokoneen siirrot
        if self.__pelilauta.siirtonumero() % 2 == 1:
            if self.__pelimuoto == 2:
                self.aktivoi_oikean_puolen_napit()

            else:
                sijainti, siirto, _ = arvioi_paras_siirto(self.__pelilauta,
                                                          "valkoinen",
                                                          self.__muuttujat,
                                                          False)
                self.tee_siirto(sijainti, siirto)

        else:
            if self.__pelimuoto == 3:
                self.aktivoi_oikean_puolen_napit()

            else:
                sijainti, siirto, _ = arvioi_paras_siirto(self.__pelilauta,
                                                          "musta",
                                                          self.__muuttujat,
                                                          False)
                self.tee_siirto(sijainti, siirto)

    def pelin_aloitus(self):
        """
        Lisää pelissä käytettävät nappulat toerialaudalle ja lisää
        graafiseen käyttöliittymään napit.
        """

        # Lähtöasemat nappuloille
        self.__pelilauta = Teorialauta()

        # Shakkilauta on 8x8, range(64) on numerot 0-63
        self.__ruudut_nappeina = []
        for _ in range(64):
            self.__ruudut_nappeina.append(Button(self.__paaikkuna,
                                                 relief="flat",
                                                 overrelief="flat"))

        # Lisätään laudan jokainen attribuutti taulukkoon
        # Haluan ensimmäisen attribuutin olevan shakkilaudan koordinaateissa
        # a1, toisen a2 jne.
        # Napit täytetään alhaalta ylöspäin (taulukon riveille 1-8) ja
        # vasemmalta oikealle (sarakkeisiin 0-7).
        rivi = 8
        sarake = 0
        for i in range(64):
            self.__ruudut_nappeina[i].grid(row=rivi, column=sarake,
                                           sticky="nsew",
                                           columnspan=1,
                                           ipadx=0, ipady=0,
                                           padx=0, pady=0)
            if sarake == 7:
                rivi -= 1
                sarake = 0
            else:
                sarake += 1

        # Pelin käydessä sulkeminen tarkoittaa poistumista päävalikkoon
        self.__sulje.configure(text="Päävalikkoon", command=self.paavalikko)

    def laudan_pohja(self):
        """
        Tyhjentää laudan napit sekä asettaa ruuduille oikeat taustavärit.
        """

        # Koonfiguroidaan napit silmukkana
        ehto = 0
        for ruutu in self.__ruudut_nappeina:
            # Aloitetaan tyhjistä napeista
            ruutu.configure(text="", command=NONE, state=DISABLED)

            # joka toinen ruutu on tumma ja joka toinen vaalea
            if ehto % 2 == 0:
                taustavari = TUMMA_RUUTU
            else:
                taustavari = VAALEA_RUUTU

            ruutu.configure(bg=taustavari, activebackground=taustavari)

            ehto += 1

            # 8. ja 9. ruutu halutaan samanvärisiksi, sitten 16. ja 17. jne.
            if ehto in range(8, 64, 9):
                ehto += 1

    def aseta_nappulat_ja_tarkista_shakit(self):
        """
        Lisää nappuloille siirtomahdollisuudet näyttävät ja siirtämisen
        mahdollistavat napit. Tarkkailee myös shakkia ja merkkaa shakitetun
        kuninkaan punaisella.
        """

        # Tarvitaan Teorialaudan nappulakohtaiset asemalistat sekä
        # yhteenlasketut asemat
        asemat = \
            0b0000000000000000000000000000000000000000000000000000000000000000
        for i in range(0, 12):
            asemat |= self.__pelilauta.asemat()[i]

        for ruutu in range(0, 64):
            if asemat >> ruutu & 1 == 0:
                continue

            puolen_vari, tyyppiteksti, siirrot = \
                self.__pelilauta.ruudun_nappulan_tiedot(ruutu)
            self.__ruudut_nappeina[ruutu].configure(
                font=PELILAUDAN_FONTTI, text=tyyppiteksti,
                fg=puolen_vari, disabledforeground=puolen_vari,
                activeforeground=puolen_vari,
                command=lambda tieto1=ruutu, tieto2=siirrot:
                self.nayta_siirrot(tieto1, tieto2))

        # Merkataan shakissa oleva kuningas punaisella
        shakit = self.__pelilauta.shakissa()
        if shakit[0]:
            self.__ruudut_nappeina[
                self.__pelilauta.asemat()[5].bit_length() - 1] \
                .configure(bg="Red", activebackground="Red")
        if shakit[1]:
            self.__ruudut_nappeina[
                self.__pelilauta.asemat()[11].bit_length() - 1] \
                .configure(bg="Red", activebackground="Red")

    def nayta_siirrot(self, lahtoasema, siirrot):
        """
        Tämä komento ajetaan pelilaudan nappulaa vastaavaa nappia painettaessa.
        Tyhjentää laudan vanhentuneista siirtonapeista ja lisää laudalle
        nappulan siirtämisen mahdollistavat siirtonapit.

        :param lahtoasema: str, painetun napin lähtökoordinaatit merkkijonona.
        :param siirrot: [str, ...]; lista nappulan mahdollisista siirroista
                        koordinaattien merkkijoina.
        """

        # Poistetaan vanhentuneet siirtonapit lataamalla lauta uudestaan
        self.laudan_pohja()
        self.aseta_nappulat_ja_tarkista_shakit()
        self.aktivoi_oikean_puolen_napit()

        indeksit = []
        indeksi = 0

        while siirrot:
            if siirrot & 1:
                indeksit.append(indeksi)
            siirrot >>= 1
            indeksi += 1

        for indeksi in indeksit:
            self.__ruudut_nappeina[indeksi].configure(
                state=NORMAL, text="Siirto", fg="grey",
                font=PELILAUDAN_FONTTI,
                activeforeground="grey",
                command=lambda tieto1=lahtoasema, tieto2=indeksi:
                self.tee_siirto(tieto1, tieto2))

    def tee_siirto(self, sijainti, siirto):
        """
        Tämä komento ajetaan siirtonappia painettaessa. Se poistaa ensin
        siirtonapit laudalta. Sitten se siirtää nappulan valittuun paikkaan
        päivittämällä tietolistat ja laudan.

        :param sijainti: str, siirrettävän nappulan koordinaatit merkkijonona.
        :param siirto: str, siirryttävän ruudun koordinaatit merkkijonona.
        """

        # Tee siirto teorialaudalla
        self.__pelilauta.tee_siirto(sijainti, siirto)

        # Päivitä lauta
        self.laudan_pohja()
        # Jos peli ei jatku, älä aseta nappuloita uudestaan
        # if not self.__pelilauta.tarkista_voitto():
        self.aseta_nappulat_ja_tarkista_shakit()
        if self.__pelimuoto == 1:
            self.kaksinpelin_vuorot()
        if self.__pelimuoto == 2:
            self.yksinpelin_vuorot()
        if self.__pelimuoto == 3:
            self.yksinpelin_vuorot()

    def aktivoi_oikean_puolen_napit(self):
        """
        Apufunktio, joka siirtonumeron perusteella aktivoi vuorossa olevan
        pelaajan napit ja deaktivoi vastapuolen napit.
        """

        valkoiset = \
            0b0000000000000000000000000000000000000000000000000000000000000000
        for i in range(0, 6):
            valkoiset |= self.__pelilauta.asemat()[i]

        mustat = \
            0b0000000000000000000000000000000000000000000000000000000000000000
        for i in range(6, 12):
            mustat |= self.__pelilauta.asemat()[i]

        # Päättelee siirtovuorossa olevan puolen
        if self.__pelilauta.siirtonumero() % 2 == 1:
            omat = valkoiset
            vastustajat = mustat
        else:
            omat = mustat
            vastustajat = valkoiset

        omat_indeksit = []
        omat_indeksi = 0

        while omat:
            if omat & 1:
                omat_indeksit.append(omat_indeksi)
            omat >>= 1
            omat_indeksi += 1

        vastustajat_indeksit = []
        vastustajat_indeksi = 0

        while vastustajat:
            if vastustajat & 1:
                vastustajat_indeksit.append(vastustajat_indeksi)
            vastustajat >>= 1
            vastustajat_indeksi += 1

        for indeksi in vastustajat_indeksit:
            self.__ruudut_nappeina[indeksi].configure(state=DISABLED)
        for indeksi in omat_indeksit:
            self.__ruudut_nappeina[indeksi].configure(state=NORMAL)

    def koko_naytto(self):
        """
        Asettaa ikkunan koko näytölle sekä muuttaa napin toiminnoksi palaamaan
        alkuperäiseen ikkunaan.
        """

        self.__paaikkuna.overrideredirect(False)
        self.__paaikkuna.attributes('-fullscreen', True)
        self.__koko_naytto.configure(text="Ikkunaksi",
                                     command=self.pois_koko_naytosta)

    def pois_koko_naytosta(self):
        """
        Asettaa ikkunan koko näytöltä takaisin alkuperäiseen kokoon sekä
        muuttaa napin toiminnoksi palaamaan koko näytölle.
        """

        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.attributes('-fullscreen', False)
        self.__koko_naytto.configure(text="Koko näyttö",
                                     command=self.koko_naytto)

    def aloita(self):
        """
        Käynnistää pääikkunan silmukan, ts. käynnistää käyttöliittymän ikkunan.
        """

        self.__paaikkuna.mainloop()


def main():
    # otetaan käyttöön Shakkilauta
    lauta = Shakkilauta()
    # käynnistetään grafiikka
    lauta.aloita()


if __name__ == "__main__":
    main()
