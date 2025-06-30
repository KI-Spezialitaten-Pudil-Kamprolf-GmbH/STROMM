# Konzeptionelle Überprüfung der deutschen Übersetzung und Logik am 2024-07-16 abgeschlossen. Keine funktionalen Probleme festgestellt.
from typing import List # Keep this if city_demands or other lists are defined directly here
# (Based on previous state, List was used for city_demands in the scenario)

# Annahme: power_grid_simulation.py ist jetzt effektiv grid_logic.py
# Wenn der tatsächliche Dateiname immer noch power_grid_simulation.py ist, verwende diesen im Import.
from power_grid_simulation import StromNetz # Grid -> StromNetz

# Importiere die übersetzten Klassennamen aus grid_components.py
from grid_components import Kraftwerk, SolarKraftwerk, WindKraftwerk, EnergieSpeicher, Verbraucher
# SonnenZustand und WindZustand werden von Grid.__init__ für Standardparameter verwendet,
# und potenziell, wenn wir ein spezifisches initiales Wetter einstellen wollen.
from weather import SonnenZustand, WindZustand, WetterSimulator # Importiere übersetzte Namen

# pprint könnte von den print-Anweisungen des Szenarios verwendet werden (nicht explizit in der letzten Version, aber gute Praxis)
import pprint

if __name__ == "__main__":
    # 1. StromNetz-Instanz erstellen
    # Wir können initiales Wetter angeben oder Standardwerte verwenden (KLAR, RUHIG)
    # Hier verwenden wir die übersetzten Enum-Mitglieder für die Initialisierung
    stromnetz = StromNetz(initialer_sonnenzustand=SonnenZustand.KLAR, initialer_windzustand=WindZustand.LEICHTE_BRISE)

    # 2. Komponenten instanziieren
    # Verwende die übersetzten Klassennamen. Attribute wie name, kapazitaet_mw, kraftwerkstyp werden beim Erstellen übergeben.
    kraftwerk1 = Kraftwerk(name="Coal Plant 1", kapazitaet_mw=500, kraftwerkstyp="fossil")
    kraftwerk3 = Kraftwerk(name="Peaker Plant", kapazitaet_mw=100, kraftwerkstyp="fossil")

    solar_kraftwerk = SolarKraftwerk(name="Solar Farm", kapazitaet_mw=150)
    wind_kraftwerk = WindKraftwerk(name="Wind Turbine Array", kapazitaet_mw=100)

    batterie = EnergieSpeicher(name="Main Battery", kapazitaet_mwh=300, max_laderate_mw=75, max_entladerate_mw=75, effizienz=0.9)
    # Zugriff auf Attribute mit übersetzten Namen
    batterie.aktueller_fuellstand_mwh = 150  # Initial charge

    city_demands: List[float] = [
        400, 380, 370, 360, 380, 450, # 00:00 - 05:00
        550, 650, 700, 720, 730, 740, # 06:00 - 11:00
        750, 740, 720, 700, 680, 650, # 12:00 - 17:00
        600, 550, 500, 480, 450, 420  # 18:00 - 23:00
    ]
    # Verwende die übersetzte Klasse Verbraucher
    stadt = Verbraucher(name="City Demand", bedarfsverlauf_ueber_zeit=city_demands)
    industrie = Verbraucher(name="Industrial Zone", bedarf_mw=200) # Constant demand

    # 3. Instanzen zum Netz hinzufügen - verwende übersetzte StromNetz-Methoden
    stromnetz.fuege_kraftwerk_hinzu(kraftwerk1)
    stromnetz.fuege_kraftwerk_hinzu(kraftwerk3)
    stromnetz.fuege_kraftwerk_hinzu(solar_kraftwerk)
    stromnetz.fuege_kraftwerk_hinzu(wind_kraftwerk)
    stromnetz.fuege_speicher_hinzu(batterie)
    stromnetz.fuege_verbraucher_hinzu(stadt)
    stromnetz.fuege_verbraucher_hinzu(industrie)

    # Initiale Kraftwerkszustände setzen - verwende übersetzte Methoden der Kraftwerke
    kraftwerk1.einschalten()
    kraftwerk3.ausschalten()
    solar_kraftwerk.ausschalten()
    wind_kraftwerk.ausschalten()

    print(f"--- Initiale Kraftwerkszustände (vor Simulationsschleife) ---")
    for kw in stromnetz.kraftwerke:
        # Die .name, .kraftwerkstyp, .kapazitaet_mw Attribute sind bereits in grid_components.py definiert (und blieben meist Englisch oder wurden dort übersetzt)
        # .ist_an wurde in grid_components.py zu ist_an
        print(f"{kw.name} ({kw.kraftwerkstyp}): {'Eingeschaltet' if kw.ist_an else 'Ausgeschaltet'}, Kapazität: {kw.kapazitaet_mw} MW")
    print(f"Initialer Batteriestand: {batterie.aktueller_fuellstand_mwh:.2f} MWh")
    print(f"Initiales Wetter: {stromnetz.wetter_simulator.lese_aktuelle_wetterbeschreibung()}")
    print("-" * 40)

    # 4. Simulation für 24 Zeitschritte
    for schritt_num in range(24): # step -> schritt_num
        print(f"\n>>> Simuliere Schritt {stromnetz.aktueller_zeitschritt + 1} (Stunde {schritt_num}) <<<")

        aktueller_stadt_bedarf = stadt.lese_bedarf(stromnetz.aktueller_zeitschritt + 1)
        aktueller_industrie_bedarf = industrie.lese_bedarf(stromnetz.aktueller_zeitschritt + 1)
        prognostizierter_gesamtbedarf = aktueller_stadt_bedarf + aktueller_industrie_bedarf

        if stromnetz.aktueller_zeitschritt == 0:
            print(f"Wetter für bevorstehenden Schritt (Initial): {stromnetz.wetter_simulator.lese_aktuelle_wetterbeschreibung()}")
            kommender_solarfaktor = stromnetz.wetter_simulator.lese_solar_ausgabefaktor(1)
            kommender_windfaktor = stromnetz.wetter_simulator.lese_wind_ausgabefaktor()
        else:
            print(f"Wetter für bevorstehenden Schritt: {stromnetz.wetter_simulator.lese_aktuelle_wetterbeschreibung()}")
            kommender_solarfaktor = stromnetz.wetter_simulator.lese_solar_ausgabefaktor(stromnetz.aktueller_zeitschritt + 1)
            kommender_windfaktor = stromnetz.wetter_simulator.lese_wind_ausgabefaktor()

        potenzielle_erneuerbare_erzeugung = 0
        initiale_online_erneuerbare_kapazitaet = 0
        for kw in stromnetz.kraftwerke:
            if kw.ist_an and kw.kraftwerkstyp == "erneuerbar":
                initiale_online_erneuerbare_kapazitaet += kw.kapazitaet_mw
                if isinstance(kw, SolarKraftwerk):
                    potenzielle_erneuerbare_erzeugung += kw.kapazitaet_mw * kommender_solarfaktor
                elif isinstance(kw, WindKraftwerk):
                    potenzielle_erneuerbare_erzeugung += kw.kapazitaet_mw * kommender_windfaktor

        initiale_online_fossile_kapazitaet = sum(kw.kapazitaet_mw for kw in stromnetz.kraftwerke if kw.ist_an and kw.kraftwerkstyp == "fossil")
        aktuelle_fossile_erzeugung = sum(kw.aktuelle_leistung_mw for kw in stromnetz.kraftwerke if kw.ist_an and kw.kraftwerkstyp == "fossil")

        print("--- Vor-Schritt Zusammenfassung ---")
        print(f"Prognostizierter Gesamtbedarf: {prognostizierter_gesamtbedarf:.2f} MW")
        print(f"Initiale Online-Kapazität Erneuerbare (nominal): {initiale_online_erneuerbare_kapazitaet:.2f} MW")
        print(f"Initiale Online-Kapazität Fossil (nominal): {initiale_online_fossile_kapazitaet:.2f} MW")
        print(f"Potenzielle tatsächliche Erneuerbare-Erzeugung (von ANLAGEN für bevorstehenden Schritt): {potenzielle_erneuerbare_erzeugung:.2f} MW")
        print(f"Aktuelle tatsächliche Fossil-Erzeugung (von ANLAGEN): {aktuelle_fossile_erzeugung:.2f} MW")
        print(f"Aktueller Batteriestand: {batterie.aktueller_fuellstand_mwh:.2f} MWh")
        print("-" * 20)

        stromnetz.simuliere_schritt(dauer_stunden=1.0)
        status = stromnetz.lese_netzzustand()

        print(f"--- Netzzustand nach Schritt {status['zeitschritt']} ---")
        print(f"Wetter während Schritt {status['zeitschritt']}: {stromnetz.wetter_simulator.lese_aktuelle_wetterbeschreibung()}")

        # Deutsche Schlüssel aus status direkt verwenden und ggf. lesbarer formatieren
        status_anzeige = {
            'zeitschritt': "Zeitschritt",
            'gesamter_bedarf_mw': "Gesamter Bedarf (MW)",
            'gesamte_erzeugung_mw': "Gesamte Erzeugung (MW)",
            'gesamte_speicherung_mwh': "Gesamte Speicherung (MWh)",
            'speicherkapazitaet_mwh': "Speicherkapazität (MWh)",
            'ungedeckter_bedarf_mw': "Ungedeckter Bedarf (MW)",
            'ueberschuss_leistung_mw': "Überschussleistung (MW)"
        }
        for schluessel, anzeige_name in status_anzeige.items():
            wert = status[schluessel]
            if isinstance(wert, float):
                print(f"{anzeige_name}: {wert:.2f}")
            else:
                print(f"{anzeige_name}: {wert}")

        print("--- Kraftwerksstatus ---")
        for kw in stromnetz.kraftwerke:
            print(f"{kw.name}: {'Eingeschaltet' if kw.ist_an else 'Ausgeschaltet'}, Leistung: {kw.aktuelle_leistung_mw:.2f} MW / {kw.kapazitaet_mw:.2f} MW")
        print("--- Speicherstatus ---")
        for s in stromnetz.energiespeicher_einheiten:
            print(f"{s.name}: {s.aktueller_fuellstand_mwh:.2f} MWh / {s.kapazitaet_mwh:.2f} MWh (Laderate: {s.max_laderate_mw} MW, Entladerate: {s.max_entladerate_mw} MW)")
        print("-" * 20)
