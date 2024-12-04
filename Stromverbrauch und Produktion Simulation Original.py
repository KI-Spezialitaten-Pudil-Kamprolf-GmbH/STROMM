import random
import time 

class Wohngebiet:
    def __init__(self):
        self.bedarf = 0

    def berechne_bedarf(self, uhrzeit):
        if 0 <= uhrzeit <= 6:
            self.bedarf = random.randint(1, 2)
        elif 7 <= uhrzeit <= 9:
            self.bedarf = random.randint(100, 120)
        elif 10 <= uhrzeit <= 16:
            self.bedarf = random.randint(10, 20)
        elif 17 <= uhrzeit <= 20:
            self.bedarf = random.randint(125, 160)
        elif 21 <= uhrzeit <= 23:
            self.bedarf = random.randint(25, 35)
        return self.bedarf

class Kohlekraftwerk:
    def __init__(self):
        self.status = "Shutdown"
        self.leistung = 0

    def set_status(self, neuer_status):
        status_map = {
            "Shutdown": 0,
            "Low_Power": 400,
            "Mid_Power": 1100,
            "Max_Power": 2000,
        }
        self.status = neuer_status
        self.leistung = status_map[neuer_status]

class Windpark:
     def __init__(self):
        self.produktion = 0

     def berechne_produktion(self, uhrzeit):
        if 0 <= uhrzeit <= 6:
            self.produktion = random.randint(10, 20)
        elif 7 <= uhrzeit <= 9:
            self.produktion = random.randint(15, 30)
        elif 10 <= uhrzeit <= 16:
            self.produktion = random.randint(50, 75)
        elif 17 <= uhrzeit <= 20:
            self.produktion = random.randint(25, 50)
        elif 21 <= uhrzeit <= 23:
            self.produktion = random.randint(10, 20)
        return self.produktion

class Industriegebiet:
    def __init__(self):
        self.bedarf = 0
    
    def energieverbrauch_Industriegebiet(self):
        self.bedarf = 1250
        return self.bedarf

class Pumpspeicherkraftwerk:
    def __init__(self):
        self.capacitiy = 0

        

# Simulation
uhrzeit = 0
wohngebiet = Wohngebiet()
kraftwerk = Kohlekraftwerk()
Industrie = Industriegebiet()
windpark = Windpark()
while True:
    if uhrzeit == 23:
        uhrzeit = 0
    else:
        uhrzeit += 1

    # Energiebedarf berechnen
    energiebedarf = wohngebiet.berechne_bedarf(uhrzeit) + Industrie.energieverbrauch_Industriegebiet()
    #print(energiebedarf) #Kontrolle ob Windpark einbezogen wird
    energiebedarf = energiebedarf - windpark.berechne_produktion(uhrzeit)

    # Kohlekraftwerk steuern (sehr einfache Logik hier)
    if energiebedarf > 1100:
        kraftwerk.set_status("Max_Power")
    elif energiebedarf > 400:
        kraftwerk.set_status("Mid_Power")
    else:
        kraftwerk.set_status("Low_Power")

    # Ausgabe
    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt (Derzeit nur auf Kohlekraftwerk): {energiebedarf} MW")
    print(f"Kohlekraftwerk: {kraftwerk.status} mit {kraftwerk.leistung} MW")
    print("-" * 30)

    # (Für Debugging oder Simulation bricht er nach einer Iteration ab) (Nicht mehr) (Jetzt wartet er einfach kurz)
    time.sleep(1)
