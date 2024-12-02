import random

# TODO: Overrides hinzufügen

class Verbraucher:
    grundbedarf = 0
    def __init__(self, grundbedarf, bedarf_uhrzeit_funktion):
        self.grundbedarf = grundbedarf
        self.bedarf_uhrzeit_funktion = bedarf_uhrzeit_funktion(int | int)

    def berechne_bedarf(self, uhrzeit):
        pass

class Wohngebiet(Verbraucher):
    def berechne_bedarf(self, uhrzeit, bedarf_uhrzeit_funktion):
        pass

class Industriegebiet(Verbraucher):
    def berechne_bedarf(self, uhrzeit):
        return 1250