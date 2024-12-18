from enum import Enum
from typing import override
#import random


class KraftwerkStatus(Enum):
    P_0 = 0
    P_1 = 1
    P_2 = 2
    P_3 = 3
    P_4 = 4
    P_5 = 5
    P_6 = 6
    P_7 = 7
    P_8 = 8
    P_9 = 9
    P_10 = 10
    P_11 = 11
    P_12 = 12
    P_13 = 13
    P_14 = 14
    P_15 = 15
    P_16 = 16
    P_17 = 17
    P_18 = 18
    P_19 = 19
    P_20 = 20
    P_21 = 21
    P_22 = 22
    P_23 = 23
    P_24 = 24
    P_25 = 25
    P_26 = 26
    P_27 = 27
    P_28 = 28
    P_29 = 29
    P_30 = 30
    P_31 = 31
    P_32 = 32
    P_33 = 33
    P_34 = 34
    P_35 = 35
    P_36 = 36
    P_37 = 37
    P_38 = 38
    P_39 = 39
    P_40 = 40
    P_41 = 41
    P_42 = 42
    P_43 = 43
    P_44 = 44
    P_45 = 45
    P_46 = 46
    P_47 = 47
    P_48 = 48
    P_49 = 49
    P_50 = 50
    P_51 = 51
    P_52 = 52
    P_53 = 53
    P_54 = 54
    P_55 = 55
    P_56 = 56
    P_57 = 57
    P_58 = 58
    P_59 = 59
    P_60 = 60
    P_61 = 61
    P_62 = 62
    P_63 = 63
    P_64 = 64
    P_65 = 65
    P_66 = 66
    P_67 = 67
    P_68 = 68
    P_69 = 69
    P_70 = 70
    P_71 = 71
    P_72 = 72
    P_73 = 73
    P_74 = 74
    P_75 = 75
    P_76 = 76
    P_77 = 77
    P_78 = 78
    P_79 = 79
    P_80 = 80
    P_81 = 81
    P_82 = 82
    P_83 = 83
    P_84 = 84
    P_85 = 85
    P_86 = 86
    P_87 = 87
    P_88 = 88
    P_89 = 89
    P_90 = 90
    P_91 = 91
    P_92 = 92
    P_93 = 93
    P_94 = 94
    P_95 = 95
    P_96 = 96
    P_97 = 97
    P_98 = 98
    P_99 = 99
    P_100 = 100


class Kraftwerk:
    status = KraftwerkStatus.P_0
    status_map = { KraftwerkStatus.P_0: 0 }
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
        if (neuer_status not in {KraftwerkStatus.P_0, KraftwerkStatus.P_100}):
            raise AttributeError("Windpark unterstützt folgende Modi: 0%, 100%")
        self.status = neuer_status