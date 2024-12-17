from enum import Enum
from typing import override
#import random


class KraftwerkStatus(Enum):
    P00 = 0
    P0005 = 1
    P0510 = 2
    P1015 = 3
    P1520 = 4
    P2025 = 5
    P2530 = 6
    P3035 = 7
    P3540 = 8
    P4045 = 9
    P4550 = 10
    P5055 = 11
    P5560 = 12
    P6065 = 13
    P6570 = 14
    P7075 = 15
    P7580 = 16
    P8085 = 17
    P8590 = 18
    P9095 = 19
    P100 = 20


class Kraftwerk:
    status = KraftwerkStatus.P00
    status_map = { KraftwerkStatus.P00: 0 }
    leistung = 0
    def __init__(self, initStatus, initStatusMap):
        self.status = initStatus
        self.status_map = initStatusMap
        self.leistung = self.status_map[self.status]
    
    def set_status(self, neuer_status):
        if (neuer_status not in self.status_map):
            raise TypeError("Neuer Status nicht auf Kraftwerk verfügbar.")
        self.status = neuer_status
    
    def get_leistung(self):
        return self.status_map[self.status]

class Windpark(Kraftwerk):
    @override
    def set_status(self, neuer_status):
        if (neuer_status not in {KraftwerkStatus.P00, KraftwerkStatus.P100}):
            raise AttributeError("Windpark unterstützt folgende Modi: P00, P100")
        self.status = neuer_status