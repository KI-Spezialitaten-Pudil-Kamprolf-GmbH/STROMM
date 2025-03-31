import random

class Kraftwerk:
    def __init__(self, name, typ, max_leistung, aktuelle_leistung=0):
        # Ein Kraftwerk, das Energie produziert.
        # Args:
        #   name (str): Der Name des Kraftwerks.
        #   typ (str): Der Typ des Kraftwerks (z.B. "Kohle", "Wind", "Solar", "Atom", "Gas"). Beeinflusst die Steuerbarkeit.
        #   max_leistung (float): Die maximale Leistung, die das Kraftwerk erzeugen kann (in MW).
        #   aktuelle_leistung (float): Die aktuelle Leistung des Kraftwerks (in MW). Startet bei 0.
        self.name = name
        self.typ = typ
        self.max_leistung = max_leistung
        self.aktuelle_leistung = aktuelle_leistung

    def anpassen_leistung(self, neue_leistung):
        # Passt die Leistung des Kraftwerks an, wenn möglich.
        # Args:
        #   neue_leistung (float): Die gewünschte neue Leistung (in MW).
        # Returns:
        #   bool: True, wenn die Anpassung erfolgreich war, False, wenn nicht.
        if neue_leistung <= self.max_leistung and neue_leistung >= 0:
            if self.typ == "Wind":
                print("Windkraftanlagen können nicht aktiv gesteuert werden. Aktuelle Leistung bleibt erhalten.")
                return False # Windkraft ist schwer steuerbar
            elif self.typ == "Solar":
                print("Solarkraftanlagen können nicht aktiv gesteuert werden. Aktuelle Leistung bleibt erhalten.")
                return False # Solarkraft ist schwer steuerbar
            else:
                self.aktuelle_leistung = neue_leistung
                return True
        else:
            print(f"Fehler: Die gewünschte Leistung {neue_leistung} MW liegt außerhalb des zulässigen Bereichs (0 - {self.max_leistung} MW).")
            return False

    def produzieren(self):
        # Gibt die aktuelle produzierte Leistung zurück. In einer realistischeren Simulation
        # könnte dies von äußeren Faktoren (z.B. Windgeschwindigkeit, Sonneneinstrahlung) abhängen.
        return self.aktuelle_leistung

    def __str__(self):
        return f"{self.name} ({self.typ}): {self.aktuelle_leistung:.2f} MW / {self.max_leistung:.2f} MW"