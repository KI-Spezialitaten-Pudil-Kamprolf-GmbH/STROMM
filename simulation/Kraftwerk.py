from enum import Enum
from typing import override
import random



class KraftwerkStatus(Enum):
    SHUTDOWN = 0
    LOW_POWER = 1
    MID_POWER = 2
    MAX_POWER = 3

class Kraftwerk:
    status = KraftwerkStatus.SHUTDOWN
    status_map = { KraftwerkStatus.SHUTDOWN: 0 }
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
        if (neuer_status not in {KraftwerkStatus.SHUTDOWN, KraftwerkStatus.MAX_POWER}):
            raise AttributeError("Windpark unterstützt folgende Modi: SHUTDOWN, MAX_POWER")
        self.status = neuer_status