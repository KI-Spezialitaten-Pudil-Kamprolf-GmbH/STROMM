import random

from typing import override

def init_uhrzeit_bedarf_funktion(uhrzeit):
    return 0

class Verbraucher:
    grundbedarf = 0
    uhrzeit_bedarf_funktion = init_uhrzeit_bedarf_funktion
    def __init__(self, grundbedarf, uhrzeit_bedarf_funktion=init_uhrzeit_bedarf_funktion):
        self.grundbedarf = grundbedarf
        self.uhrzeit_bedarf_funktion = uhrzeit_bedarf_funktion

    def berechne_bedarf(self, uhrzeit):
        return self.grundbedarf + int(self.uhrzeit_bedarf_funktion(uhrzeit))

# class Wohngebiet(Verbraucher):
#     # TODO: Herausfinden, wie man eine Subklasse vorerst leer lässt
#     @override
#     def __init__(self):
#         super.__init__(self)

# class Industriegebiet(Verbraucher):
#     # TODO: Herausfinden, wie man eine Subklasse vorerst leer lässt
#     @override
#     def __init__(self):
#         super.__init__(self)