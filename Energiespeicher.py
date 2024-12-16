import sys


class Energiespeicher:
    # TODO: Evtl. auf Englisch wechseln; Deutsch sieht teils merkwürdig aus...
    kapazitaet = 0
    gespeichert = 0
    ladeverlust_anteil = 0.0
    entladeverlust_anteil = 0.0
    def __init__(self, kapazitaet, ladeverlust_anteil, entladeverlust_anteil):
        self.kapazitaet = kapazitaet
        self.gespeichert = 0
        self.ladeverlust_anteil = ladeverlust_anteil
        self.entladeverlust_anteil = entladeverlust_anteil
    
    # Return: Menge an Energie, die nicht gespeichert werden konnte
    def speichern(self, neuaufnahme):
        freie_kapazitaet = self.kapazitaet - self.gespeichert
        neuaufnahme_mit_verlust = neuaufnahme * (1.0 - self.ladeverlust_anteil)
        if (freie_kapazitaet < neuaufnahme_mit_verlust):
            print("Freie Kapazität kleiner als Neuaufnahme; Nur Teil wird gespeichert.", file=sys.stderr)
            self.gespeichert += freie_kapazitaet
            # Nicht ideal simuliert: Obwohl nicht alles gespeichert wurde, wird der Gesamtverlust mit eingerechnet
            return neuaufnahme_mit_verlust - freie_kapazitaet
        else:
            self.gespeichert += neuaufnahme_mit_verlust
            return 0
    
    # Return: Menge an Energie, die entladen wurde
    def entladen(self, angefragte_menge):
        # Entladbar: Menge an Energie, die für den Verbraucher aus dem Speicher verfügbar ist
        entladbar = self.gespeichert * (1.0 - self.entladeverlust_anteil)
        # Entleerung: Menge an Energie, die für die angefragte Menge aus dem Speicher gezogen wird
        entleerung = angefragte_menge + (angefragte_menge * self.entladeverlust_anteil)

        if (entleerung > entladbar):
            print("Angefragte Menge vom Speicherwerk größer als gespeicherte Menge.")
            self.gespeichert = 0
            return angefragte_menge - entladbar
        else:
            self.gespeichert -= entleerung
            return angefragte_menge