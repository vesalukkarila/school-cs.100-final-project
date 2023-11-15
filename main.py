"""
COMP.CS.100  Python-ohjelma tehtävä 3 viikko 13
Graafiset käyttöliittymät
Itse tehty projektityö, hirsipuupeli
Tekijä: Vesa Lukkarila vesa.lukkarila@tuni.fi
Opiskelijanumero: 150372523
"""

"""
Hirsipuupeli, joka lienee alkeellinen, mutta lisäpisteitä kalastellaan
Radiobutton komponentilla, sekä random ja string toimintojen käytöllä.

Ohjelma arpoo valittavan kysymyksen sanakirjasta ja sen perusteella valitsee oikean 
vastauksen sekä valinnaisen lisävihjeen. Käyttäjä syöttää syötekenttään 
arvattavan kirjaimen yksi kerrallaan ja painaa "Arvaa"-nappia 
Ohjelma tarkistaa esiintyykä kirjain vastauksessa. Väärän
syötteen myötä hirsipuukuva etenee. Peli päättyy, jos vääriä syötteitä 
annetaan 6 kpl. Syötteiksi hyväksytään pienet aakkoset ja vain yksi kerrallaan. 
Ei siis ääkkösiä/isoja aakkosia/numeroita/erikoismerkkejä, jotka kaikki 
edistävät hirsipuuta.
Myös saman syötteen anto kahdesti edistää hirsipuun rakentumista.
Virheilmoitukset vääristä syötteistä näkyy käyttöliittymässä.
Hirsipuukuvat on tehty draw.io ohjelmalla.
"""


from tkinter import *
import string
import random

KUVAT = \
    ["hr1.png", "hr2.png", "hr3.png", "hr4.png",
     "hr5.png", "hr6.png", "hr7.png", "hrvoitto.png"]


class Hirsipuu:

    def __init__(self):
        """
        Luokan rakentaja.
        """

        self.__paaikkuna = Tk()
        self.__paaikkuna.title("Hirsipuupeli")
        self.__sallitut_merkit = string.ascii_lowercase

        # Kutsutaan apufunktiota kysymyksen arvontaa varten, kyseisen
        # apufunktion attribuutteihin (self.__vastaus ja self.__kysymys)
        # tallentamia tietoja tarvitaan tästä edespäin.
        self.kysymys_arvonta()

        #Luodaan käyttöliittymän komponentit
        self.__keskenerainen_vastaus = "_ "*len(self.__vastaus)
        self.__vihje = Label(self.__paaikkuna, text=self.__kysymys)
        self.__arvattava_sana = Label\
            (self.__paaikkuna, text=(self.__keskenerainen_vastaus))
        self.__syote_kentta = Entry(self.__paaikkuna)
        self.__arvaus_nappi = Button\
            (self.__paaikkuna, text="Arvaa kirjain!", command=self.onko_merkki_sallittu)
        self.__ilmoitus_kentta = Label(self.__paaikkuna, text="")
        self.__uusi_peli = Button \
            (self.__paaikkuna, text="Uusi peli", command=self.uusi_peli)
        self.__lopeta = Button \
            (self.__paaikkuna, text="Lopeta", command=self.lopeta)

        #Luodaan Label lisävihjeelle ja Radiobutton:t lisävihjevalinnalle.
        self.__lisa_vihje = Label(self.__paaikkuna, text="")
        var = IntVar()
        self.__radio1 = Radiobutton(self.__paaikkuna, text="Lisävihje, kiitos!!",
                                    variable=var, value=1,
                                    command=self.vihje)
        self.__radio2 = Radiobutton(self.__paaikkuna, text="Ei tartte auttaa!",
                                    variable=var, value=2,
                                    command=self.ei_vihjetta)

        # Tuodaan kuvat olion attribuuttiin ja alustetaan laskuri, joka
        # indeksoi näytettävää kuvaa.
        self.__kuva_laskuri = 0
        self.__kuva_lista = []
        for kuva in KUVAT:
            self.__kuva_lista.append(PhotoImage(file=kuva))
        self.__hirsipuu_kuva = Label\
            (image=self.__kuva_lista[self.__kuva_laskuri])

        #Komponenttien paikalleen asetus
        self.__vihje.grid()
        self.__arvattava_sana.grid()
        self.__syote_kentta.grid()
        self.__arvaus_nappi.grid()
        self.__lisa_vihje.grid()
        self.__radio1.grid()
        self.__radio2.grid()
        self.__ilmoitus_kentta.grid()
        self.__hirsipuu_kuva.grid()
        self.__uusi_peli.grid()
        self.__lopeta.grid()


    def kysymys_arvonta(self):
        """
        Funktio valitsee satunnaisesti sanakirjasta kysymys-vastaus parin
        ja tallentaa tiedot olion attribuutteihin.
        """

        skirja = {"Kaupunki?": "oulu", "Automerkki?": "opel",
                  "Eläin?": "koira", "Pikkulintu?": "talitintti",
                  "Miehen nimi?": "pekka"}
        kysymys = random.choice(list(skirja.keys()))
        vastaus = skirja[kysymys]
        self.__kysymys = kysymys
        self.__vastaus = vastaus


    def onko_merkki_sallittu(self):
        """
        Funktio tarkistaa onko annettu syöte sallittu ja reagoi
        virhetilanteisiin.
        """

        # Merkkijono paikkallislistaksi helpomman käsittelyn vuoksi.
        paljastuva_sana_listana = self.__keskenerainen_vastaus.split(" ")
        syote = self.__syote_kentta.get()

        if len(syote) != 1:
            self.__ilmoitus_kentta.configure(text="Syötä vain 1 kirjain")
            self.hirteen()
        elif syote not in self.__sallitut_merkit:
            self.__ilmoitus_kentta.configure\
                (text="Ei isoja kirjaimia, ääkkösiä tai erikoismerkkejä!")
            self.hirteen()
            return
        elif syote in paljastuva_sana_listana:
            self.__ilmoitus_kentta.configure\
                (text="Olet jo arvannut tätä kirjainta!")
            self.hirteen()
            return

        else:
            self.merkki_on_sallittu()


    def merkki_on_sallittu(self):
        """
        Funktio tarkistaa onko käyttäjän syöte arvattavassa sanassa ja
        ilmoittaa oikein/väärin vastauksesta viestikentässä.
        """

        # Merkkijono paikkallislistaksi helpomman käsittelyn vuoksi.
        paljastuva_sana_listana = self.__keskenerainen_vastaus.split(" ")
        syote = self.__syote_kentta.get()
        ind = 0

        # Verrataan syötettä vastauksen kirjaimiin. Yhtäsuuruuden tapahtuessa
        # muutetaan listan alkiota vastaavasta indeksikohdasta
        if syote in self.__vastaus:
            for kirjain in self.__vastaus:
                if kirjain == syote:
                    paljastuva_sana_listana.insert(ind + 1, syote)
                    paljastuva_sana_listana.pop(ind)
                    ind += 1
                    self.tyhjenna_syote_kentta()
                    if "_" not in paljastuva_sana_listana:
                        self.voitto()
                else:
                    ind += 1
                    self.tyhjenna_syote_kentta()
            self.__ilmoitus_kentta.configure(text="Hienoa, jatka!")
        else:
            self.__ilmoitus_kentta.configure\
                (text="Voi pahus, olet joutumassa hirteen!")
            self.hirteen()

        # Muutetaan lista takaisin merkkijonoksi ja lisätään välilyönnit
        # selkeämmän esityksen vuoksi graafisessa käyttöliittymässä.
        self.__keskenerainen_vastaus=((" ").join(paljastuva_sana_listana))
        self.__arvattava_sana.configure(text=self.__keskenerainen_vastaus)


    def voitto(self):
        """
        Käyttäjän veikattua oikein funktio näyttää voittokuvan ja tyhjentää
        viestikentät. Tämän jälkeen pelin voi aloittaa alusta tai sulkea.
        """

        self.__ilmoitus_kentta.configure(text="")
        self.__lisa_vihje.configure(text="")
        self.__hirsipuu_kuva.configure(image=self.__kuva_lista[-1])
        self.__arvaus_nappi.configure(state=DISABLED)
        self.__radio1.configure(state=DISABLED)
        self.__radio2.configure(state=DISABLED)


    def hirteen(self):
        """
        Muokkaa näytettävää kuvaa hirsipuun lähestyessä. Tarkistaa, onko
        kaikki kuusi yritystä käytetty, jolloin peli loppuu.
        """

        self.tyhjenna_syote_kentta()
        self.__kuva_laskuri += 1
        self.__hirsipuu_kuva.configure\
            (image=self.__kuva_lista[self.__kuva_laskuri])
        if self.__kuva_laskuri == 6:
            self.__ilmoitus_kentta.configure\
                (text="")
            self.__lisa_vihje.configure(text="")
            self.__arvaus_nappi.configure(state=DISABLED)
            self.__radio1.configure(state=DISABLED)
            self.__radio2.configure(state=DISABLED)


    def vihje(self):
        """
        Funktio etsii sanakirjasta oikean vihjeen kysymykselle ja
        tallentaa vihjeen olion attribuuttiin.
        """

        vihje_sanakirja = {"Kaupunki?": "Hailuodon lähellä",
                           "Automerkki?": "___ Corsa",
                           "Eläin?": "Vuf vuf!",
                           "Pikkulintu?": "Lintulaudan vakiovieras",
                           "Miehen nimi?": "_____ Puupää"}
        vihje = vihje_sanakirja[self.__kysymys]
        self.__lisa_vihje.configure(text=vihje)
        self.__radio1.configure(state=DISABLED)
        self.__radio2.configure(state=DISABLED)


    def ei_vihjetta(self):
        """
        Muuttaa vihjekentän tekstin.
        """

        self.__lisa_vihje.configure(text="Oikea asenne!")
        self.__radio1.configure(state=DISABLED)
        self.__radio2.configure(state=DISABLED)


    def tyhjenna_syote_kentta(self):
        """
        Tyhjentää käyttäjän syötteen.
        """

        self.__syote_kentta.delete(0, END)


    def uusi_peli(self):
        """
        Lopettaa nykyisen ja aloittaa uuden ikkunan.
        """

        self.lopeta()
        main()


    def lopeta(self):
        """
        Lopettaa käyttöliittymän.
        """

        self.__paaikkuna.destroy()


    def start(self):
        """
         Käynnistää pääikkunan.
        """

        self.__paaikkuna.mainloop()


def main():
    hr = Hirsipuu()
    hr.start()

if __name__ == "__main__":
    main()