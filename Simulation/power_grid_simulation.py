from typing import List, Dict

# Imports from our new modules
# Importiere die übersetzten Namen aus weather.py
from weather import WetterSimulator, SonnenZustand, WindZustand
# Importiere die übersetzten Klassennamen aus grid_components.py
from grid_components import Kraftwerk, SolarKraftwerk, WindKraftwerk, EnergieSpeicher, Verbraucher


class StromNetz: # Grid -> StromNetz
    """Stellt das Stromnetz dar, das Anlagen, Speicher und Verbraucher verwaltet."""
    def __init__(self, initialer_sonnenzustand: SonnenZustand = SonnenZustand.KLAR,
                 initialer_windzustand: WindZustand = WindZustand.RUHIG): # initial_sun_state -> initialer_sonnenzustand, initial_wind_state -> initialer_windzustand
        self.kraftwerke: List[Kraftwerk] = []
        self.energiespeicher_einheiten: List[EnergieSpeicher] = [] # energy_storage_units -> energiespeicher_einheiten
        self.verbraucher_anlagen: List[Verbraucher] = [] # facilities -> verbraucher_anlagen
        self.aktueller_zeitschritt: int = 0 # current_time_step -> aktueller_zeitschritt
        self.wetter_simulator = WetterSimulator(initialer_sonnenzustand, initialer_windzustand)
        self.letzter_schritt_gesamter_bedarf_mw: float = 0.0 # last_step_total_demand_mw -> letzter_schritt_gesamter_bedarf_mw
        self.letzter_schritt_gesamte_erzeugung_mw: float = 0.0 # last_step_total_generation_mw -> letzter_schritt_gesamte_erzeugung_mw
        self.letzter_schritt_ungedeckter_bedarf_mw: float = 0.0 # last_step_unmet_demand_mw -> letzter_schritt_ungedeckter_bedarf_mw
        self.letzter_schritt_ueberschuss_leistung_mw: float = 0.0 # last_step_surplus_power_mw -> letzter_schritt_ueberschuss_leistung_mw

    def fuege_kraftwerk_hinzu(self, kraftwerk_obj: Kraftwerk) -> None:
        """Fügt ein Kraftwerk zum Netz hinzu."""
        self.kraftwerke.append(kraftwerk_obj)

    def fuege_speicher_hinzu(self, speicher_obj: EnergieSpeicher) -> None:
        """Fügt eine Energiespeichereinheit zum Netz hinzu."""
        self.energiespeicher_einheiten.append(speicher_obj)

    def fuege_verbraucher_hinzu(self, verbraucher_obj: Verbraucher) -> None:
        """Fügt einen Verbraucher zum Netz hinzu."""
        self.verbraucher_anlagen.append(verbraucher_obj)

    def simuliere_schritt(self, dauer_stunden: float = 1.0) -> None: # simulate_step -> simuliere_schritt, duration_hours -> dauer_stunden
        """Simuliert einen Zeitschritt des Netzbetriebs."""

        if self.aktueller_zeitschritt == 0 :
             pass
        else:
            self.wetter_simulator.aktualisiere_zustand(self.aktueller_zeitschritt)


        self.aktueller_zeitschritt += 1

        gesamter_bedarf_mw = sum(v.lese_bedarf(self.aktueller_zeitschritt) for v in self.verbraucher_anlagen)

        online_erzeugungskapazitaet_mw = sum(kw.kapazitaet_mw for kw in self.kraftwerke if kw.ist_an)
        aktueller_energiespeicherstand_mwh = sum(s.aktueller_fuellstand_mwh for s in self.energiespeicher_einheiten)
        gesamte_speicherkapazitaet_mwh = sum(s.kapazitaet_mwh for s in self.energiespeicher_einheiten) if self.energiespeicher_einheiten else 0

        if gesamter_bedarf_mw > online_erzeugungskapazitaet_mw:
            offline_erneuerbare_kraftwerke = [kw for kw in self.kraftwerke if not kw.ist_an and kw.kraftwerkstyp == "erneuerbar"]
            offline_fossile_kraftwerke = [kw for kw in self.kraftwerke if not kw.ist_an and kw.kraftwerkstyp == "fossil"]

            while gesamter_bedarf_mw > online_erzeugungskapazitaet_mw and offline_erneuerbare_kraftwerke:
                zu_aktivierendes_kraftwerk = offline_erneuerbare_kraftwerke.pop(0)
                # String Literal übersetzt
                print(f"Steuerungslogik: Erneuerbares Kraftwerk {zu_aktivierendes_kraftwerk.name} wird wegen hoher Nachfrage eingeschaltet.")
                zu_aktivierendes_kraftwerk.einschalten()
                online_erzeugungskapazitaet_mw += zu_aktivierendes_kraftwerk.kapazitaet_mw

            while gesamter_bedarf_mw > online_erzeugungskapazitaet_mw and offline_fossile_kraftwerke:
                zu_aktivierendes_kraftwerk = offline_fossile_kraftwerke.pop(0)
                # String Literal übersetzt
                print(f"Steuerungslogik: Fossiles Kraftwerk {zu_aktivierendes_kraftwerk.name} wird wegen hoher Nachfrage eingeschaltet.")
                zu_aktivierendes_kraftwerk.einschalten()
                online_erzeugungskapazitaet_mw += zu_aktivierendes_kraftwerk.kapazitaet_mw

        speicher_voll_schwelle = 0.95 * gesamte_speicherkapazitaet_mwh if gesamte_speicherkapazitaet_mwh > 0 else 0
        sollte_erzeugung_reduzieren = (
            gesamte_speicherkapazitaet_mwh > 0 and
            online_erzeugungskapazitaet_mw > gesamter_bedarf_mw * 1.2 and
            aktueller_energiespeicherstand_mwh >= speicher_voll_schwelle
        )

        if sollte_erzeugung_reduzieren:
            online_fossile_kraftwerke = [
                kw for kw in self.kraftwerke if kw.ist_an and kw.kraftwerkstyp == "fossil"
            ]
            online_fossile_kraftwerke.sort(key=lambda kw: kw.kapazitaet_mw)

            if online_fossile_kraftwerke:
                abzuschaltendes_kraftwerk = online_fossile_kraftwerke[0]
                # String Literal übersetzt
                print(f"Steuerungslogik: Fossiles Kraftwerk {abzuschaltendes_kraftwerk.name} (Kapazität: {abzuschaltendes_kraftwerk.kapazitaet_mw} MW) wird wegen Überschusserzeugung und vollem Speicher abgeschaltet.")
                abzuschaltendes_kraftwerk.ausschalten()
                online_erzeugungskapazitaet_mw -= abzuschaltendes_kraftwerk.kapazitaet_mw

        for kw in self.kraftwerke:
            if isinstance(kw, (SolarKraftwerk, WindKraftwerk)):
                kw.aktualisiere_leistung(self.aktueller_zeitschritt, self.wetter_simulator)
            else:
                kw.aktualisiere_leistung(self.aktueller_zeitschritt)

        gesamte_erzeugung_mw = sum(kw.aktuelle_leistung_mw for kw in self.kraftwerke if kw.ist_an)

        netto_leistung_mw = gesamte_erzeugung_mw - gesamter_bedarf_mw # net_power_mw -> netto_leistung_mw
        ungedeckter_bedarf_mw = 0.0 # unmet_demand_mw -> ungedeckter_bedarf_mw
        ueberschuss_leistung_mw = 0.0 # surplus_power_mw -> ueberschuss_leistung_mw

        if netto_leistung_mw > 0:
            verfuegbar_zum_laden_mw = netto_leistung_mw # available_to_charge_mw -> verfuegbar_zum_laden_mw
            for speicher in self.energiespeicher_einheiten:
                geladene_mwh = speicher.laden(verfuegbar_zum_laden_mw, dauer_stunden)
                geladene_mw = geladene_mwh / dauer_stunden if dauer_stunden > 0 else 0
                verfuegbar_zum_laden_mw -= geladene_mw
            ueberschuss_leistung_mw = max(0, verfuegbar_zum_laden_mw)
        elif netto_leistung_mw < 0:
            benoetigt_aus_speicher_mw = -netto_leistung_mw # needed_from_storage_mw -> benoetigt_aus_speicher_mw
            for speicher in self.energiespeicher_einheiten:
                entladene_mwh = speicher.entladen(benoetigt_aus_speicher_mw, dauer_stunden)
                entladene_mw = entladene_mwh / dauer_stunden if dauer_stunden > 0 else 0
                benoetigt_aus_speicher_mw -= entladene_mw
            ungedeckter_bedarf_mw = max(0, benoetigt_aus_speicher_mw)

        self.letzter_schritt_gesamter_bedarf_mw = gesamter_bedarf_mw
        self.letzter_schritt_gesamte_erzeugung_mw = gesamte_erzeugung_mw
        self.letzter_schritt_ungedeckter_bedarf_mw = ungedeckter_bedarf_mw
        self.letzter_schritt_ueberschuss_leistung_mw = ueberschuss_leistung_mw

    def lese_netzzustand(self) -> Dict[str, float]: # get_grid_status -> lese_netzzustand
        """Gibt den aktuellen Status des Netzes zurück."""
        return {
            'zeitschritt': self.aktueller_zeitschritt, # 'time_step' -> 'zeitschritt'
            'gesamter_bedarf_mw': self.letzter_schritt_gesamter_bedarf_mw, # 'total_demand_mw' -> 'gesamter_bedarf_mw'
            'gesamte_erzeugung_mw': self.letzter_schritt_gesamte_erzeugung_mw, # 'total_generation_mw' -> 'gesamte_erzeugung_mw'
            'gesamte_speicherung_mwh': sum(s.aktueller_fuellstand_mwh for s in self.energiespeicher_einheiten), # 'total_storage_mwh' -> 'gesamte_speicherung_mwh'
            'speicherkapazitaet_mwh': sum(s.kapazitaet_mwh for s in self.energiespeicher_einheiten), # 'storage_capacity_mwh' -> 'speicherkapazitaet_mwh'
            'ungedeckter_bedarf_mw': self.letzter_schritt_ungedeckter_bedarf_mw, # 'unmet_demand_mw' -> 'ungedeckter_bedarf_mw'
            'ueberschuss_leistung_mw': self.letzter_schritt_ueberschuss_leistung_mw, # 'surplus_power_mw' -> 'ueberschuss_leistung_mw'
        }

# Der if __name__ == "__main__": Block wurde gemäß den Anweisungen entfernt.
