import random
import datetime
from kraftwerke import Kraftwerk
from energiespeicher import Pumpspeicher
from verbraucher import Verbraucher

class Stromnetz:
    def __init__(self):
        # Das Stromnetz, das Kraftwerke, Verbraucher und Leitungen verwaltet.
        self.kraftwerke = []
        self.verbraucher = []
        self.pumpspeicher = None  #Optionaler Pumpspeicher

    def kraftwerk_hinzufuegen(self, kraftwerk):
        self.kraftwerke.append(kraftwerk)

    def verbraucher_hinzufuegen(self, verbraucher):
        self.verbraucher.append(verbraucher)

    def pumpspeicher_hinzufuegen(self, pumpspeicher):
        self.pumpspeicher = pumpspeicher

    def steuerung(self):
        """
        Steuerungslogik:
        1. Gesamtverbrauch berechnen
        2. Produktion durch erneuerbare Energien berechnen
        2.1 Bei Überschuss im Pumpspeicher lagern (Ladeverluste beachten)
        3. Von dem verbleibenden Verbrauch möglichst viel durch den Speicher auffüllen (Entladeverlust berücksichtigen)
        4. Verbleibende Defizite durch die fossilen Energieträger zuproduzieren
        5. Finale Reste auch im Speicher lagern.
        """
        gesamtverbrauch = sum(verbraucher.verbrauchen() for verbraucher in self.verbraucher)
        gesamtproduktion_erneuerbar = sum(kraftwerk.produzieren() for kraftwerk in self.kraftwerke if kraftwerk.typ in ("Wind", "Solar"))
        gesamtproduktion_steuerbar = 0  # Wird später berechnet

        differenz = gesamtverbrauch - gesamtproduktion_erneuerbar  # Defizit oder Überschuss

        # 2.1 Überschuss in den Pumpspeicher lagern (Ladeverluste beachten)
        if self.pumpspeicher:
            if differenz < 0: # Überschuss an erneuerbarer Energie
                leistung_laden = min(-differenz, self.pumpspeicher.max_leistung_laden, self.pumpspeicher.kapazitaet - self.pumpspeicher.aktueller_fuellstand)
                tatsaechlich_geladen = self.pumpspeicher.laden(leistung_laden)
                differenz += tatsaechlich_geladen  # Reduziere den Überschuss
                print(f"Pumpspeicher geladen: {tatsaechlich_geladen:.2f} MW")

        # 3. Verbrauch durch den Speicher auffüllen (Entladeverluste berücksichtigen)
        if self.pumpspeicher:
            if differenz > 0:  # Defizit
                leistung_entladen = min(differenz, self.pumpspeicher.max_leistung_entladen)
                tatsaechlich_entladen = self.pumpspeicher.entladen(leistung_entladen)
                differenz -= tatsaechlich_entladen  # Reduziere das Defizit
                print(f"Pumpspeicher entladen: {tatsaechlich_entladen:.2f} MW")

        # 4. Verbleibende Defizite durch fossile Energieträger decken
        if differenz > 0: #Immernoch Defizit
            for kraftwerk in self.kraftwerke:
                if kraftwerk.typ not in ("Wind", "Solar"):  # Steuerbare Kraftwerke
                    neue_leistung = kraftwerk.aktuelle_leistung + differenz
                    #Sicherstellen, dass die Leistung im zulässigen Bereich liegt
                    neue_leistung = max(0, min(neue_leistung, kraftwerk.max_leistung))
                    delta = neue_leistung - kraftwerk.aktuelle_leistung #Wie viel Leistung hinzugefügt wurde
                    kraftwerk.anpassen_leistung(neue_leistung)
                    differenz -= delta #Reduziere das Defizit
                    gesamtproduktion_steuerbar += delta
                    print(f"{kraftwerk.typ}-Kraftwerk {kraftwerk.name} Leistung erhöht um {delta:.2f} MW")
                    if differenz <= 0:
                       break #Nicht alle Kraftwerke müssen hochgefahren werden

        # 5. Finale Reste auch im Speicher lagern (Ladeverluste beachten)
        if self.pumpspeicher:
            if differenz < 0:  # Es gibt einen Überschuss, nachdem die fossilen Energieträger hinzugefügt wurden
                leistung_laden = min(-differenz, self.pumpspeicher.max_leistung_laden, self.pumpspeicher.kapazitaet - self.pumpspeicher.aktueller_fuellstand)
                tatsaechlich_geladen = self.pumpspeicher.laden(leistung_laden)
                differenz += tatsaechlich_geladen
                print(f"Pumpspeicher geladen (Rest): {tatsaechlich_geladen:.2f} MW")

        #Gibt aus, wie gross der Fehler am Schluss war
        print(f"Verbleibende Differenz: {differenz:.2f} MW")

    def aktualisiere_erneuerbare(self):
        """
        Passt die Leistung von Wind- und Solarkraftwerken zufällig an.
        """
        for kraftwerk in self.kraftwerke:
            if kraftwerk.typ == "Wind":
                # Zufällige Leistung zwischen 0 und max_leistung
                kraftwerk.aktuelle_leistung = random.uniform(0, kraftwerk.max_leistung)
            elif kraftwerk.typ == "Solar":
                # Zufällige Leistung, die auch die Tageszeit berücksichtigt
                jetzt = datetime.datetime.now()
                stunde = jetzt.hour

                if 5 <= stunde < 7:  # Morgens
                    faktor = random.uniform(0.2, 0.4)
                elif 7 <= stunde < 17:  # Tagsüber
                    faktor = random.uniform(0.4, 1.0)  # Zwischen 40% und 100% der maximalen Leistung
                elif 17 <= stunde < 19:  # Abends
                    faktor = random.uniform(0.4, 1.0)  # Zwischen 40% und 100% der maximalen Leistung am Abend
                else:  # Nachts
                    faktor = random.uniform(0.0, 0.2)  # Nachts zwischen 0% und 20%

                kraftwerk.aktuelle_leistung = faktor * kraftwerk.max_leistung

    def simuliere_schritt(self):
        # Simuliert einen einzelnen Zeitschritt des Stromnetzes.
        print("\n--- Simuliere Zeitschritt ---")

        # 1. Berechne den Gesamtverbrauch
        gesamtverbrauch = sum(verbraucher.verbrauchen() for verbraucher in self.verbraucher)
        print(f"Gesamtverbrauch: {gesamtverbrauch:.2f} MW")

        # 2. Aktualisiere die Leistung der erneuerbaren Energien
        self.aktualisiere_erneuerbare() # Rufe die Funktion zur Aktualisierung der erneuerbaren Energien auf

        # 3. Berechne die Gesamtproduktion
        gesamtproduktion = sum(kraftwerk.produzieren() for kraftwerk in self.kraftwerke)
        if self.pumpspeicher:
            #Hier wird die "Produktion" des Pumpspeichers nicht direkt addiert, da sie bereits in der Steuerung berücksichtigt wird.
            pass
        print(f"Gesamtproduktion (ohne PS-Entladung): {gesamtproduktion:.2f} MW")
        if self.pumpspeicher:
           print(f"Gesamtproduktion (mit PS-Entladung) {gesamtproduktion + (self.pumpspeicher.max_leistung_entladen * self.pumpspeicher.entlade_effizienz):.2f}")

        # 4. Steuerung des Netzes
        self.steuerung()  # Rufe die Steuerungsfunktion auf

        # 5. Überprüfe, ob die Produktion den Verbrauch deckt
        gesamtproduktion_nach_steuerung = sum(kraftwerk.produzieren() for kraftwerk in self.kraftwerke) #Produktion neu berechnen, da sich diese in der Steuerung geändert hat
        if self.pumpspeicher:
            differenz = gesamtverbrauch - (gesamtproduktion_nach_steuerung)
            if differenz > 0:
               print("WARNUNG: Die Produktion deckt den Verbrauch nicht!")

        # 6. Gib einen Überblick über den Zustand des Netzes
        print("\n--- Kraftwerke ---")
        for kraftwerk in self.kraftwerke:
            print(kraftwerk)

        print("\n--- Verbraucher ---")
        for verbraucher in self.verbraucher:
            print(verbraucher)

        if self.pumpspeicher:
            print("\n--- Pumpspeicher ---")
            print(self.pumpspeicher)

def initialisiere_und_simuliere():
    """
    Initialisiert das Stromnetz, erstellt die Komponenten und startet die Simulation.
    """
    from verbraucher import Verbraucher
    from energiespeicher import Pumpspeicher
    from kraftwerke import Kraftwerk

    kraftwerks_definitionen = []
    kraftwerkstypen = ["Kohle", "Wind", "Solar", "Gas", "Atom"]

    # Interaktive Abfrage der Kraftwerke
    for typ in kraftwerkstypen:
        try:
            anzahl = int(input(f"Wie viele {typ}-Kraftwerke soll es geben? "))
            if anzahl < 0:
                print("Anzahl muss >= 0 sein. Setze auf 0.")
                anzahl = 0

            for i in range(anzahl):
                while True:
                    try:
                        max_leistung = float(input(f"Maximale Leistung für {typ}-Kraftwerk {i + 1} (in MW): "))
                        if max_leistung <= 0:
                            print("Die maximale Leistung muss größer als 0 sein.")
                            continue  # Zurück zur Eingabeaufforderung für diese Leistung
                        break  # Akzeptable Leistung eingegeben
                    except ValueError:
                        print("Ungültige Eingabe für die maximale Leistung. Bitte eine Zahl eingeben.")

                kraftwerks_definitionen.append({"name": f"{typ}-Kraftwerk {i + 1}", "typ": typ, "max_leistung": max_leistung})

        except ValueError:
            print("Ungültige Eingabe für die Anzahl. Überspringe diesen Kraftwerkstyp.")

    # 1. Kraftwerke erstellen
    kraftwerke = []
    for definition in kraftwerks_definitionen:
        try:
            name = definition['name']
            typ = definition['typ']
            max_leistung = float(definition['max_leistung'])  # Stelle sicher, dass es eine Zahl ist

            if typ not in ("Kohle", "Wind", "Solar", "Gas", "Atom"):
                print(f"Warnung: Ungültiger Kraftwerkstyp '{typ}' für Kraftwerk '{name}'. Überspringe dieses Kraftwerk.")
                continue  # Überspringe dieses Kraftwerk

            if max_leistung <= 0:
                print(f"Warnung: Die maximale Leistung für Kraftwerk '{name}' muss größer als 0 sein. Überspringe dieses Kraftwerk.")
                continue

            kraftwerk = Kraftwerk(name, typ, max_leistung)
            kraftwerke.append(kraftwerk)

        except (KeyError, ValueError) as e:
            print(f"Fehler beim Erstellen eines Kraftwerks: {e}.  Überprüfe die Kraftwerksdefinitionen.")

    # 2. Verbraucher erstellen
    verbraucher_stadt = Verbraucher("Stadt X", 600)
    verbraucher_fabrik = Verbraucher("Fabrik Y", 400)

    # 3. Pumpspeicher erstellen
    pumpspeicher = Pumpspeicher("Pumpspeicher E", 200, 200, 800, 400, 0.9, 0.9)  #max_laden, max_entladen, Kapazität, Initialer Füllstand, Ladeeffizienz, Entladeeffizienz

    # 4. Stromnetz erstellen
    stromnetz = Stromnetz()
    for kraftwerk in kraftwerke:
        stromnetz.kraftwerk_hinzufuegen(kraftwerk)

    stromnetz.verbraucher_hinzufuegen(verbraucher_stadt)
    stromnetz.verbraucher_hinzufuegen(verbraucher_fabrik)

    # Simulation starten
    try:
        anzahl_schritte = int(input("Anzahl der Simulationsschritte: "))
    except ValueError:
        print("Ungültige Eingabe für die Anzahl der Simulationsschritte.  Verwende Standardwert 3.")
        anzahl_schritte = 3

    for _ in range(anzahl_schritte):  # Simuliere die Zeitschritte
        stromnetz.simuliere_schritt()

if __name__ == "__main__":
    initialisiere_und_simuliere()