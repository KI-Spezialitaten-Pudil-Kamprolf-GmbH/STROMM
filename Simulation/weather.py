import enum
import random

# --- Wetterzustand-Aufzählungen und Faktoren ---

class SonnenZustand(enum.Enum):
    KLAR = 0
    TEILWEISE_BEWOELKT = 1
    BEDECKT = 2

class WindZustand(enum.Enum):
    RUHIG = 0  # oder STILL
    LEICHTE_BRISE = 1
    MAESSIGER_WIND = 2
    STARKER_WIND = 3

SONNENZUSTAND_FAKTOREN = {
    SonnenZustand.KLAR: 1.0,
    SonnenZustand.TEILWEISE_BEWOELKT: 0.6,
    SonnenZustand.BEDECKT: 0.2
}

WINDZUSTAND_FAKTOREN = {
    WindZustand.RUHIG: 0.0,
    WindZustand.LEICHTE_BRISE: 0.3,
    WindZustand.MAESSIGER_WIND: 0.7,
    WindZustand.STARKER_WIND: 1.0
}

# Tägliche Solar-Multiplikatorkurve (24-Stunden-Zyklus)
TAEGLICHE_SOLAR_MULTIPLIKATOREN = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # 0-5 Uhr
    0.1, 0.3, 0.5, 0.7, 0.9, 1.0,  # 6-11 Uhr
    1.0, 0.9, 0.8, 0.6, 0.4, 0.1,  # 12-17 Uhr
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0   # 18-23 Uhr
]

# --- Wetterübergangs-Wahrscheinlichkeitsmatrizen ---

# Für SonnenZustand (KLAR, TEILWEISE_BEWOELKT, BEDECKT)
SONNENUEBERGANGSMATRIX = [
    # Von KLAR zu:
    [0.7, 0.2, 0.1],  # KLAR, TEILWEISE_BEWOELKT, BEDECKT
    # Von TEILWEISE_BEWOELKT zu:
    [0.3, 0.5, 0.2],  # KLAR, TEILWEISE_BEWOELKT, BEDECKT
    # Von BEDECKT zu:
    [0.1, 0.4, 0.5]   # KLAR, TEILWEISE_BEWOELKT, BEDECKT
]

# Für WindZustand (RUHIG, LEICHTE_BRISE, MAESSIGER_WIND, STARKER_WIND)
WINDUEBERGANGSMATRIX = [
    # Von RUHIG zu:
    [0.6, 0.3, 0.1, 0.0], # RUHIG, LEICHTE_BRISE, MAESSIGER_WIND, STARKER_WIND
    # Von LEICHTE_BRISE zu:
    [0.2, 0.5, 0.2, 0.1], # RUHIG, LEICHTE_BRISE, MAESSIGER_WIND, STARKER_WIND
    # Von MAESSIGER_WIND zu:
    [0.05, 0.25, 0.5, 0.2],# RUHIG, LEICHTE_BRISE, MAESSIGER_WIND, STARKER_WIND
    # Von STARKER_WIND zu:
    [0.05, 0.15, 0.4, 0.4] # RUHIG, LEICHTE_BRISE, MAESSIGER_WIND, STARKER_WIND
]

class WetterSimulator:
    def __init__(self, initialer_sonnenzustand: SonnenZustand = SonnenZustand.KLAR,
                 initialer_windzustand: WindZustand = WindZustand.RUHIG):
        self.aktueller_sonnenzustand: SonnenZustand = initialer_sonnenzustand
        self.aktueller_windzustand: WindZustand = initialer_windzustand

        # Referenzen auf globale Konstanten speichern für Bequemlichkeit
        self.sonnen_zustaende: list[SonnenZustand] = list(SonnenZustand)
        self.wind_zustaende: list[WindZustand] = list(WindZustand)
        self.sonnenuebergangsmatrix: list[list[float]] = SONNENUEBERGANGSMATRIX
        self.winduebergangsmatrix: list[list[float]] = WINDUEBERGANGSMATRIX
        self.sonnenzustand_faktoren: dict[SonnenZustand, float] = SONNENZUSTAND_FAKTOREN
        self.windzustand_faktoren: dict[WindZustand, float] = WINDZUSTAND_FAKTOREN
        self.taegliche_solar_multiplikatoren: list[float] = TAEGLICHE_SOLAR_MULTIPLIKATOREN

    def aktualisiere_zustand(self, zeitschritt: int) -> None:
        # Sonnenzustand aktualisieren
        aktueller_sonnen_index = self.sonnen_zustaende.index(self.aktueller_sonnenzustand)
        naechste_sonnen_wahrscheinlichkeiten = self.sonnenuebergangsmatrix[aktueller_sonnen_index]
        self.aktueller_sonnenzustand = random.choices(self.sonnen_zustaende, weights=naechste_sonnen_wahrscheinlichkeiten, k=1)[0]

        # Windzustand aktualisieren
        aktueller_wind_index = self.wind_zustaende.index(self.aktueller_windzustand)
        naechste_wind_wahrscheinlichkeiten = self.winduebergangsmatrix[aktueller_wind_index]
        self.aktueller_windzustand = random.choices(self.wind_zustaende, weights=naechste_wind_wahrscheinlichkeiten, k=1)[0]

    def lese_solar_ausgabefaktor(self, zeitschritt: int) -> float:
        basisfaktor = self.sonnenzustand_faktoren.get(self.aktueller_sonnenzustand, 0.0)
        # zeitschritt im Grid beginnt bei 1, für 24-Stunden-Zyklus gibt (zeitschritt-1) % 24 den Index 0-23
        taeglicher_multiplikator = self.taegliche_solar_multiplikatoren[(zeitschritt - 1) % 24]
        return basisfaktor * taeglicher_multiplikator

    def lese_wind_ausgabefaktor(self) -> float:
        return self.windzustand_faktoren.get(self.aktueller_windzustand, 0.0)

    def lese_aktuelle_wetterbeschreibung(self) -> str:
        return f"Sonne: {self.aktueller_sonnenzustand.name}, Wind: {self.aktueller_windzustand.name}"
