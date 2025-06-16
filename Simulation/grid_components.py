from typing import List
# Importiere die übersetzten Namen aus weather.py
from weather import WetterSimulator, SonnenZustand, WindZustand

# Hinweis: enum wird hier möglicherweise nicht benötigt, wenn plant_type in PowerPlant ein String bleibt.

class Kraftwerk: # Formerly PowerPlant
    """Stellt ein Kraftwerk im Netz dar."""
    def __init__(self, name: str, kapazitaet_mw: float, kraftwerkstyp: str): # capacity_mw -> kapazitaet_mw, plant_type -> kraftwerkstyp
        self.name: str = name
        self.kapazitaet_mw: float = kapazitaet_mw
        self.kraftwerkstyp: str = kraftwerkstyp
        self.aktuelle_leistung_mw: float = 0.0 # current_output_mw -> aktuelle_leistung_mw
        self.ist_an: bool = False # is_on -> ist_an

    def einschalten(self) -> None: # turn_on -> einschalten
        """Schaltet das Kraftwerk ein."""
        self.ist_an = True
        self.aktuelle_leistung_mw = self.kapazitaet_mw # Standardmäßig volle Kapazität

    def ausschalten(self) -> None: # turn_off -> ausschalten
        """Schaltet das Kraftwerk aus."""
        self.ist_an = False
        self.aktuelle_leistung_mw = 0.0

    def passe_leistung_an(self, leistung_mw: float) -> None: # adjust_output -> passe_leistung_an, mw -> leistung_mw
        """Passt die Leistung des Kraftwerks an, unter Berücksichtigung seiner Kapazität, wenn es eingeschaltet ist."""
        if self.ist_an:
            if leistung_mw < 0:
                self.aktuelle_leistung_mw = 0.0
            elif leistung_mw > self.kapazitaet_mw:
                self.aktuelle_leistung_mw = self.kapazitaet_mw
            else:
                self.aktuelle_leistung_mw = leistung_mw

    def aktualisiere_leistung(self, zeitschritt: int, wetter_simulator: WetterSimulator = None) -> None: # update_output -> aktualisiere_leistung, time_step -> zeitschritt
        """Aktualisiert die Leistung der Anlage basierend auf externen Faktoren (z.B. Wetter).
        Wird von Unterklassen wie SolarKraftwerk und WindKraftwerk überschrieben.
        WetterSimulator ist hier optional, damit nicht-erneuerbare Anlagen diese Methodensignatur verwenden können,
        ohne dass ihnen eine WetterSimulator-Instanz übergeben werden muss, wenn sie diese nicht verwenden."""
        pass


class SolarKraftwerk(Kraftwerk): # SolarPlant -> SolarKraftwerk, inherits from Kraftwerk
    """Stellt ein Solarkraftwerk dar."""
    def __init__(self, name: str, kapazitaet_mw: float):
        super().__init__(name, kapazitaet_mw, kraftwerkstyp="erneuerbar") # "renewable" -> "erneuerbar"

    def aktualisiere_leistung(self, zeitschritt: int, wetter_simulator: WetterSimulator) -> None: # update_output -> aktualisiere_leistung, time_step -> zeitschritt
        if self.ist_an:
            sonnenlicht_faktor = wetter_simulator.lese_solar_ausgabefaktor(zeitschritt)
            self.aktuelle_leistung_mw = self.kapazitaet_mw * sonnenlicht_faktor
        else:
            self.aktuelle_leistung_mw = 0.0


class WindKraftwerk(Kraftwerk): # WindPlant -> WindKraftwerk, inherits from Kraftwerk
    """Stellt ein Windkraftwerk dar."""
    def __init__(self, name: str, kapazitaet_mw: float):
        super().__init__(name, kapazitaet_mw, kraftwerkstyp="erneuerbar") # "renewable" -> "erneuerbar"

    def aktualisiere_leistung(self, zeitschritt: int, wetter_simulator: WetterSimulator) -> None: # update_output -> aktualisiere_leistung, time_step -> zeitschritt
        if self.ist_an:
            wind_faktor = wetter_simulator.lese_wind_ausgabefaktor()
            self.aktuelle_leistung_mw = self.kapazitaet_mw * wind_faktor
        else:
            self.aktuelle_leistung_mw = 0.0


class EnergieSpeicher: # EnergyStorage -> EnergieSpeicher
    """Stellt eine Energiespeichereinheit dar."""
    def __init__(self, name: str, kapazitaet_mwh: float, max_laderate_mw: float, max_entladerate_mw: float, effizienz: float = 0.9):
        self.name: str = name
        self.kapazitaet_mwh: float = kapazitaet_mwh # capacity_mwh -> kapazitaet_mwh
        self.aktueller_fuellstand_mwh: float = 0.0 # current_storage_mwh -> aktueller_fuellstand_mwh
        self.max_laderate_mw: float = max_laderate_mw # max_charge_rate_mw -> max_laderate_mw
        self.max_entladerate_mw: float = max_entladerate_mw # max_discharge_rate_mw -> max_entladerate_mw
        if not 0 <= effizienz <= 1: # efficiency -> effizienz
            raise ValueError("Effizienz muss zwischen 0 und 1 liegen.") # Efficiency must be between 0 and 1.
        self.effizienz: float = effizienz

    def laden(self, leistung_zum_laden_mw: float, dauer_stunden: float) -> float: # charge -> laden, power_to_charge_mw -> leistung_zum_laden_mw, duration_hours -> dauer_stunden
        """Lädt die Speichereinheit. Gibt die tatsächlich geladene Energie in MWh zurück."""
        if leistung_zum_laden_mw <= 0 or dauer_stunden <= 0:
            return 0.0

        max_moegliche_ladung_dieser_schritt_mwh = self.max_laderate_mw * dauer_stunden
        angeforderte_ladung_mwh = leistung_zum_laden_mw * dauer_stunden
        tatsaechliche_ladung_vor_verlust_mwh = min(angeforderte_ladung_mwh, max_moegliche_ladung_dieser_schritt_mwh)

        zu_speichernde_energie_mwh = tatsaechliche_ladung_vor_verlust_mwh * self.effizienz
        kann_speichern_mwh = self.kapazitaet_mwh - self.aktueller_fuellstand_mwh
        endgueltig_hinzugefuegte_energie_mwh = min(zu_speichernde_energie_mwh, kann_speichern_mwh)

        self.aktueller_fuellstand_mwh += endgueltig_hinzugefuegte_energie_mwh
        return endgueltig_hinzugefuegte_energie_mwh

    def entladen(self, leistung_zum_entladen_mw: float, dauer_stunden: float) -> float: # discharge -> entladen, power_to_discharge_mw -> leistung_zum_entladen_mw, duration_hours -> dauer_stunden
        """Entlädt die Speichereinheit. Gibt die tatsächlich entladene Energie in MWh zurück."""
        if leistung_zum_entladen_mw <= 0 or dauer_stunden <= 0:
            return 0.0

        max_moegliche_entladung_dieser_schritt_mwh = self.max_entladerate_mw * dauer_stunden
        angeforderte_entladung_mwh = leistung_zum_entladen_mw * dauer_stunden
        tatsaechliche_energie_zum_entladen_mwh = min(angeforderte_entladung_mwh, max_moegliche_entladung_dieser_schritt_mwh)

        kann_bereitstellen_mwh = self.aktueller_fuellstand_mwh
        endgueltig_bereitgestellte_energie_mwh = min(tatsaechliche_energie_zum_entladen_mwh, kann_bereitstellen_mwh)

        self.aktueller_fuellstand_mwh -= endgueltig_bereitgestellte_energie_mwh
        return endgueltig_bereitgestellte_energie_mwh


class Verbraucher: # Facility -> Verbraucher
    """Stellt einen Stromverbraucher dar."""
    def __init__(self, name: str, bedarf_mw: float = 0, bedarfsverlauf_ueber_zeit: List[float] = None): # demand_mw -> bedarf_mw, demands_over_time -> bedarfsverlauf_ueber_zeit
        self.name: str = name
        if bedarfsverlauf_ueber_zeit:
            self.bedarfsverlauf_ueber_zeit: List[float] = bedarfsverlauf_ueber_zeit
            self.bedarf_mw: float = bedarfsverlauf_ueber_zeit[0] # Initialer Bedarf
        else:
            self.bedarfsverlauf_ueber_zeit: List[float] = None
            self.bedarf_mw: float = bedarf_mw


    def lese_bedarf(self, zeitschritt: int) -> float: # get_demand -> lese_bedarf, time_step -> zeitschritt
        """Gibt den Strombedarf des Verbrauchers zu einem gegebenen Zeitschritt zurück."""
        if self.bedarfsverlauf_ueber_zeit:
            # zeitschritt im Grid beginnt bei 1, Listenindex ist 0-basiert
            return self.bedarfsverlauf_ueber_zeit[(zeitschritt -1) % len(self.bedarfsverlauf_ueber_zeit)]
        return self.bedarf_mw
