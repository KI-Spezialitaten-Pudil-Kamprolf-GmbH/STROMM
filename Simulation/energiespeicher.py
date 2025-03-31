class Pumpspeicher:
    def __init__(self, name, max_leistung_laden, max_leistung_entladen, kapazitaet, aktueller_fuellstand=0, lade_effizienz=0.9, entlade_effizienz=0.9):
        #Ein Pumpspeicherkraftwerk, das überschüssige Energie speichert und bei Bedarf wieder abgibt.
        #Args:
        #    name (str): Der Name des Pumpspeichers.
        #    max_leistung_laden (float): Die maximale Leistung, mit der der Speicher geladen werden kann (in MW).
        #    max_leistung_entladen (float): Die maximale Leistung, mit der der Speicher entladen werden kann (in MW).
        #    kapazitaet (float): Die maximale Speicherkapazität (in MWh).
        #    aktueller_fuellstand (float): Der aktuelle Füllstand des Speichers (in MWh).
        #    lade_effizienz (float): Effizienz beim Laden (0 bis 1).
        #    entlade_effizienz (float): Effizienz beim Entladen (0 bis 1).
        self.name = name
        self.max_leistung_laden = max_leistung_laden
        self.max_leistung_entladen = max_leistung_entladen
        self.kapazitaet = kapazitaet
        self.aktueller_fuellstand = aktueller_fuellstand
        self.lade_effizienz = lade_effizienz
        self.entlade_effizienz = entlade_effizienz

    def laden(self, leistung, zeit_schritt=1):
        #Lädt den Speicher mit der gegebenen Leistung für einen Zeitschritt (angenommen 1 Stunde).
        #Args:
        #    leistung (float): Die Ladeleistung (in MW).
        #    zeit_schritt (int): Die Dauer des Ladevorgangs (in Stunden).
        #Returns:
        #    float: Die tatsächlich geladene Leistung (in MW).
        leistung = min(leistung, self.max_leistung_laden) #Begrenze die Ladeleistung
        energie_hinzu = leistung * zeit_schritt * self.lade_effizienz #Energie, die hinzugefügt wird (MWh), unter Berücksichtigung der Effizienz

        if self.aktueller_fuellstand + energie_hinzu <= self.kapazitaet:
            self.aktueller_fuellstand += energie_hinzu
            return leistung
        else:
            tatsaechliche_ladung = (self.kapazitaet - self.aktueller_fuellstand) / (zeit_schritt * self.lade_effizienz)
            self.aktueller_fuellstand = self.kapazitaet
            return tatsaechliche_ladung

    def entladen(self, leistung, zeit_schritt=1):
        #Entlädt den Speicher mit der gegebenen Leistung für einen Zeitschritt (angenommen 1 Stunde).
        #Args:
        #    leistung (float): Die Entladeleistung (in MW).
        #    zeit_schritt (int): Die Dauer des Entladevorgangs (in Stunden).
        #Returns:
        #    float: Die tatsächlich entladene Leistung (in MW).
        leistung = min(leistung, self.max_leistung_entladen) #Begrenze die Entladeleistung
        energie_weg = leistung * zeit_schritt / self.entlade_effizienz #Energie, die entnommen wird (MWh), unter Berücksichtigung der Effizienz

        if self.aktueller_fuellstand >= energie_weg:
            self.aktueller_fuellstand -= energie_weg
            return leistung
        else:
            tatsaechliche_entladung = self.aktueller_fuellstand / (zeit_schritt / self.entlade_effizienz)
            self.aktueller_fuellstand = 0
            return tatsaechliche_entladung

    def produzieren(self):
        #Gibt die aktuelle produzierte Leistung zurück (beim Entladen).
        return 0 #Die Leistung wird durch die entladen-Funktion bereitgestellt.

    def __str__(self):
        return f"{self.name}: Füllstand = {self.aktueller_fuellstand:.2f} MWh / {self.kapazitaet:.2f} MWh"