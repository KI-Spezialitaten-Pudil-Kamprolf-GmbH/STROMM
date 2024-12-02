import random
import time

from Verbraucher import Wohngebiet, Industriegebiet

from Kraftwerk import Kohlekraftwerk, KraftwerkStatus, Windpark


class Pumpspeicherkraftwerk:
    def __init__(self):
        self.capacitiy = 0

        

# Simulation
uhrzeit = 0
def wohngebiet1_bedarf_uhrzeit_funktion(uhrzeit):
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
wohngebiet1 = Wohngebiet(
    grundbedarf = 0, 
    wohngebiet1_bedarf_uhrzeit_funktion
)
kraftwerk1 = Kohlekraftwerk(
    initStatus = KraftwerkStatus.SHUTDOWN,
    initStatusMap = {
        KraftwerkStatus.SHUTDOWN: 0,
        KraftwerkStatus.LOW_POWER: 400,
        KraftwerkStatus.MID_POWER: 1100,
        KraftwerkStatus.MAX_POWER: 2000
    }
)
kraftwerk2 = Kohlekraftwerk(
    initStatus = KraftwerkStatus.SHUTDOWN,
    initStatusMap = {
        KraftwerkStatus.SHUTDOWN: -20,
        KraftwerkStatus.LOW_POWER: 500,
        KraftwerkStatus.MID_POWER: 1500,
        KraftwerkStatus.MAX_POWER: 2600
    }
)
industrie1 = Industriegebiet(

)
windpark1 = Windpark()

while True:
    if uhrzeit == 23:
        uhrzeit = 0
    else:
        uhrzeit += 1

    # Energiebedarf berechnen
    energiebedarf = wohngebiet1.berechne_bedarf(uhrzeit) + industrie1.energieverbrauch_Industriegebiet()
    #print(energiebedarf) #Kontrolle ob Windpark einbezogen wird
    energiebedarf = energiebedarf - windpark1.berechne_produktion(uhrzeit)

    # Kohlekraftwerk steuern (sehr einfache Logik hier)
    if energiebedarf > 1100:
        kraftwerk1.set_status("Max_Power")
    elif energiebedarf > 400:
        kraftwerk1.set_status("Mid_Power")
    else:
        kraftwerk1.set_status("Low_Power")

    # Ausgabe
    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt (Derzeit nur auf Kohlekraftwerk): {energiebedarf} MW")
    print(f"Kohlekraftwerk: {kraftwerk1.status} mit {kraftwerk1.leistung} MW")
    print("-" * 30)

    # (Für Debugging oder Simulation bricht er nach einer Iteration ab) (Nicht mehr) (Jetzt wartet er einfach kurz)
    time.sleep(1)

