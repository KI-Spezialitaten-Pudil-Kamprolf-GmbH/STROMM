import random
import time

from Verbraucher import Verbraucher

from Kraftwerk import Kraftwerk, KraftwerkStatus, Windpark
from Energiespeicher import Energiespeicher

#TODO: Von Überobjekt "Element" erben, in dem update(+zeit) als Funktion festgelegt ist

# Simulation
uhrzeit = 0
def wohngebiet1_uhrzeit_bedarf_funktion(uhrzeit):
    if 0 <= uhrzeit <= 6:
        return random.randint(1, 2)
    elif 7 <= uhrzeit <= 9:
        return random.randint(100, 120)
    elif 10 <= uhrzeit <= 16:
        return random.randint(10, 20)
    elif 17 <= uhrzeit <= 20:
        return random.randint(125, 160)
    elif 21 <= uhrzeit <= 23:
        return random.randint(25, 35)
wohngebiet1 = Verbraucher(
    grundbedarf = 1000, 
    # TODO: Syntax für Inline-Deklaration finden & verwenden
    uhrzeit_bedarf_funktion = wohngebiet1_uhrzeit_bedarf_funktion
)
kraftwerk1 = Kraftwerk(
    initStatus = KraftwerkStatus.P00,
    initStatusMap = {
        KraftwerkStatus.P00: 0,
        KraftwerkStatus.P0005: 100,
        KraftwerkStatus.P0510: 200,
        KraftwerkStatus.P1015: 300,
        KraftwerkStatus.P1520: 400,
        KraftwerkStatus.P2025: 500,
        KraftwerkStatus.P2530: 600,
        KraftwerkStatus.P3035: 700,
        KraftwerkStatus.P3540: 800,
        KraftwerkStatus.P4045: 900,
        KraftwerkStatus.P4550: 1000,
        KraftwerkStatus.P5055: 1100,
        KraftwerkStatus.P5560: 1200,
        KraftwerkStatus.P6065: 1300,
        KraftwerkStatus.P6570: 1400,
        KraftwerkStatus.P7075: 1500,
        KraftwerkStatus.P7580: 1600,
        KraftwerkStatus.P8085: 1700,
        KraftwerkStatus.P8590: 1800,
        KraftwerkStatus.P9095: 1900,
        KraftwerkStatus.P100: 2000
    }
)
# kraftwerk2 = Kraftwerk(
#    initStatus = KraftwerkStatus.P00,
#    initStatusMap = {
#        KraftwerkStatus.P00: 20,
#        KraftwerkStatus.P00: 500,
#        KraftwerkStatus.P00: 1500,
#        KraftwerkStatus.P00: 2600
#    }
# )


industrie1 = Verbraucher(
    grundbedarf = 1250
)
windpark1 = Windpark(
    initStatus = KraftwerkStatus.P100,
    initStatusMap = {
        KraftwerkStatus.P00: 0,
        KraftwerkStatus.P100: 500
    }
)
pumpspeicherwerk = Energiespeicher(
    kapazitaet = 2000,
    ladeverlust_anteil = 0.1,
    entladeverlust_anteil = 0.2
)

while True:
    if uhrzeit == 23:
        uhrzeit = 0
    else:
        uhrzeit += 1

    # Energiebedarf berechnen
    energiebedarf = wohngebiet1.berechne_bedarf(uhrzeit) + industrie1.berechne_bedarf(uhrzeit)
    #print(energiebedarf) #Kontrolle ob Windpark einbezogen wird
    energiebedarf = energiebedarf - windpark1.get_leistung()

    # Kohlekraftwerk steuern (sehr einfache Logik hier)
    # Große Uberarbeitung nötig
    # 2000 MW pro Block


    benoetigte_leistung = (energiebedarf / 2000)*100
    if benoetigte_leistung == 100:
        kraftwerk1.set_status(KraftwerkStatus.P100)
    if benoetigte_leistung < 100 and benoetigte_leistung >= 95:
        kraftwerk1.set_status(KraftwerkStatus.P9095)
    if benoetigte_leistung < 95 and benoetigte_leistung >= 90:
        kraftwerk1.set_status(KraftwerkStatus.P9095)
    if benoetigte_leistung < 90 and benoetigte_leistung >= 85:
        kraftwerk1.set_status(KraftwerkStatus.P8590)
    if benoetigte_leistung < 85 and benoetigte_leistung >= 80:
        kraftwerk1.set_status(KraftwerkStatus.P8085)
    if benoetigte_leistung < 80 and benoetigte_leistung >= 75:
        kraftwerk1.set_status(KraftwerkStatus.P7580)
    if benoetigte_leistung < 75 and benoetigte_leistung >= 70:
        kraftwerk1.set_status(KraftwerkStatus.P7075)
    if benoetigte_leistung < 70 and benoetigte_leistung >= 65:
        kraftwerk1.set_status(KraftwerkStatus.P6570)
    if benoetigte_leistung < 65 and benoetigte_leistung >= 60:
        kraftwerk1.set_status(KraftwerkStatus.P6065)
    if benoetigte_leistung < 60 and benoetigte_leistung >= 55:
        kraftwerk1.set_status(KraftwerkStatus.P5560)
    if benoetigte_leistung < 55 and benoetigte_leistung > 50:
        kraftwerk1.set_status(KraftwerkStatus.P5055)
    if benoetigte_leistung < 50 and benoetigte_leistung >= 45:
        kraftwerk1.set_status(KraftwerkStatus.P4550)
    if benoetigte_leistung < 45 and benoetigte_leistung >= 40:
        kraftwerk1.set_status(KraftwerkStatus.P4045)
    if benoetigte_leistung < 40 and benoetigte_leistung >= 35:
        kraftwerk1.set_status(KraftwerkStatus.P3540)
    if benoetigte_leistung < 35 and benoetigte_leistung >= 30:
        kraftwerk1.set_status(KraftwerkStatus.P3035)
    if benoetigte_leistung < 30 and benoetigte_leistung >= 25:
        kraftwerk1.set_status(KraftwerkStatus.P2530)
    if benoetigte_leistung < 25 and benoetigte_leistung >= 20:
        kraftwerk1.set_status(KraftwerkStatus.P2025)
    if benoetigte_leistung < 20 and benoetigte_leistung >= 15:
        kraftwerk1.set_status(KraftwerkStatus.P1520)
    if benoetigte_leistung < 15 and benoetigte_leistung >= 10:
        kraftwerk1.set_status(KraftwerkStatus.P1015)
    if benoetigte_leistung < 10 and benoetigte_leistung >= 5:
        kraftwerk1.set_status(KraftwerkStatus.P0510)
    if benoetigte_leistung < 5 and benoetigte_leistung > 0:
        kraftwerk1.set_status(KraftwerkStatus.P0005)
    if benoetigte_leistung == 0:
        kraftwerk1.set_status(KraftwerkStatus.P00)


#    if energiebedarf > 1100:
#        kraftwerk1.set_status(KraftwerkStatus.MAX_POWER)
#    elif energiebedarf > 400:
#        kraftwerk1.set_status(KraftwerkStatus.MID_POWER)
#    else:
#        kraftwerk1.set_status(KraftwerkStatus.LOW_POWER)
    
    ueberschuss = kraftwerk1.get_leistung() - energiebedarf

    # Ausgabe
    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt (Derzeit nur auf einem Kohlekraftwerk): {energiebedarf} MW")
    print(f"Kohlekraftwerk: {kraftwerk1.status} mit {kraftwerk1.get_leistung()} MW")
    print(f"Überschuss: {ueberschuss} MW")
    print("-" * 30)

    # (Für Debugging oder Simulation bricht er nach einer Iteration ab) (Nicht mehr) (Jetzt wartet er einfach kurz)
    time.sleep(1)