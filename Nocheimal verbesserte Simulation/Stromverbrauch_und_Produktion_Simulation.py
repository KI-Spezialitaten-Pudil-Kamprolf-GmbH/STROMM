import random
import time

from Verbraucher import Verbraucher
from Kraftwerk import Kraftwerk, KraftwerkStatus, Windpark
from Energiespeicher import Energiespeicher
from math import ceil

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
    grundbedarf=1000,
    uhrzeit_bedarf_funktion=wohngebiet1_uhrzeit_bedarf_funktion
)

anzahl_kraftwerke = int(input("Wieviele Kraftwerksblöcke?"))
blockleistung = int(input("Was ist die Blockleistung?"))
# Kraftwerke erstellen und in Liste speichern
kraftwerke = []
for i in range(anzahl_kraftwerke):
    kraftwerke.append(Kraftwerk(
        initStatus=KraftwerkStatus.P00,
        initStatusMap={
            KraftwerkStatus.P00: 0,
            KraftwerkStatus.P0005: ((blockleistung/100)*5),
            KraftwerkStatus.P0510: ((blockleistung/100)*10),
            KraftwerkStatus.P1015: ((blockleistung/100)*15),
            KraftwerkStatus.P1520: ((blockleistung/100)*20),
            KraftwerkStatus.P2025: ((blockleistung/100)*25),
            KraftwerkStatus.P2530: ((blockleistung/100)*30),
            KraftwerkStatus.P3035: ((blockleistung/100)*35),
            KraftwerkStatus.P3540: ((blockleistung/100)*40),
            KraftwerkStatus.P4045: ((blockleistung/100)*45),
            KraftwerkStatus.P4550: ((blockleistung/100)*50),
            KraftwerkStatus.P5055: ((blockleistung/100)*55),
            KraftwerkStatus.P5560: ((blockleistung/100)*60),
            KraftwerkStatus.P6065: ((blockleistung/100)*65),
            KraftwerkStatus.P6570: ((blockleistung/100)*70),
            KraftwerkStatus.P7075: ((blockleistung/100)*75),
            KraftwerkStatus.P7580: ((blockleistung/100)*80),
            KraftwerkStatus.P8085: ((blockleistung/100)*85),
            KraftwerkStatus.P8590: ((blockleistung/100)*90),
            KraftwerkStatus.P9095: ((blockleistung/100)*95),
            KraftwerkStatus.P100: blockleistung
        }
    ))

industrie1 = Verbraucher(
    grundbedarf=1250
)
windpark1 = Windpark(
    initStatus=KraftwerkStatus.P100,
    initStatusMap={
        KraftwerkStatus.P00: 0,
        KraftwerkStatus.P100: 500
    }
)
pumpspeicherwerk = Energiespeicher(
    kapazitaet=2000,
    ladeverlust_anteil=0.1,
    entladeverlust_anteil=0.2
)

while True:
    if uhrzeit == 23:
        uhrzeit = 0
    else:
        uhrzeit += 1

    # Energiebedarf berechnen
    energiebedarf = wohngebiet1.berechne_bedarf(uhrzeit) + industrie1.berechne_bedarf(uhrzeit)
    energiebedarf = energiebedarf - windpark1.get_leistung()

    # Kohlekraftwerke steuern
    benoetigte_leistung = ceil((energiebedarf / blockleistung) * (100 / anzahl_kraftwerke))

    for kraftwerk in kraftwerke:
        if benoetigte_leistung >= 100:
            quit()
        if benoetigte_leistung == 100:
            kraftwerk.set_status(  KraftwerkStatus.P100)
        if benoetigte_leistung < 100 and benoetigte_leistung >= 95:
            kraftwerk.set_status(  KraftwerkStatus.P9095)
        if benoetigte_leistung < 95 and benoetigte_leistung >= 90:
            kraftwerk.set_status(  KraftwerkStatus.P9095)
        if benoetigte_leistung < 90 and benoetigte_leistung >= 85:
            kraftwerk.set_status(  KraftwerkStatus.P8590)
        if benoetigte_leistung < 85 and benoetigte_leistung >= 80:
            kraftwerk.set_status(  KraftwerkStatus.P8085)
        if benoetigte_leistung < 80 and benoetigte_leistung >= 75:
            kraftwerk.set_status(  KraftwerkStatus.P7580)
        if benoetigte_leistung < 75 and benoetigte_leistung >= 70:
            kraftwerk.set_status(  KraftwerkStatus.P7075)
        if benoetigte_leistung < 70 and benoetigte_leistung >= 65:
            kraftwerk.set_status(  KraftwerkStatus.P6570)
        if benoetigte_leistung < 65 and benoetigte_leistung >= 60:
            kraftwerk.set_status( KraftwerkStatus.P6065)
        if benoetigte_leistung < 60 and benoetigte_leistung >= 55:
            kraftwerk.set_status(  KraftwerkStatus.P5560)
        if benoetigte_leistung < 55 and benoetigte_leistung > 50:
            kraftwerk.set_status(  KraftwerkStatus.P5055)
        if benoetigte_leistung < 50 and benoetigte_leistung >= 45:
            kraftwerk.set_status(  KraftwerkStatus.P4550)
        if benoetigte_leistung < 45 and benoetigte_leistung >= 40:
            kraftwerk.set_status(  KraftwerkStatus.P4045)
        if benoetigte_leistung < 40 and benoetigte_leistung >= 35:
            kraftwerk.set_status(  KraftwerkStatus.P3540)
        if benoetigte_leistung < 35 and benoetigte_leistung >= 30:
            kraftwerk.set_status(  KraftwerkStatus.P3035)
        if benoetigte_leistung < 30 and benoetigte_leistung >= 25:
            kraftwerk.set_status(  KraftwerkStatus.P2530)
        if benoetigte_leistung < 25 and benoetigte_leistung >= 20:
            kraftwerk.set_status(  KraftwerkStatus.P2025)
        if benoetigte_leistung < 20 and benoetigte_leistung >= 15:
            kraftwerk.set_status(  KraftwerkStatus.P1520)
        if benoetigte_leistung < 15 and benoetigte_leistung >= 10:
            kraftwerk.set_status( KraftwerkStatus.P1015)
        if benoetigte_leistung < 10 and benoetigte_leistung >= 5:
            kraftwerk.set_status(  KraftwerkStatus.P0510)
        if benoetigte_leistung < 5 and benoetigte_leistung > 0:
            kraftwerk.set_status( KraftwerkStatus.P0005)
        if benoetigte_leistung == 0:
            kraftwerk.set_status(  KraftwerkStatus.P00)

    # Überschuss berechnen
    ueberschuss = sum(kraftwerk.get_leistung() for kraftwerk in kraftwerke) - energiebedarf

    # Ausgabe
    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt: {energiebedarf} MW")
    for i, kraftwerk in enumerate(kraftwerke):
        print(f"Kohlekraftwerk {i+1}: {kraftwerk.status} mit {kraftwerk.get_leistung()} MW")
    print(f"Überschuss: {ueberschuss} MW")
    print("-" * 30)

    time.sleep(1)