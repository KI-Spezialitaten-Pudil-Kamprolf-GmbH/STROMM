import random
import time
from Verbraucher import Verbraucher
from Kraftwerk import Kraftwerk, KraftwerkStatus, Windpark
from Energiespeicher import Energiespeicher
from math import ceil, floor

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
kraftwerke = []
for i in range(anzahl_kraftwerke):
    kraftwerke.append(Kraftwerk(
        initStatus=KraftwerkStatus.P_0,
        initStatusMap={
            KraftwerkStatus.P_0: 0,
            KraftwerkStatus.P_1: ((blockleistung/100)*1),
            KraftwerkStatus.P_2: ((blockleistung/100)*2),
            KraftwerkStatus.P_3: ((blockleistung/100)*3),
            KraftwerkStatus.P_4: ((blockleistung/100)*4),
            KraftwerkStatus.P_5: ((blockleistung/100)*5),
            KraftwerkStatus.P_6: ((blockleistung/100)*6),
            KraftwerkStatus.P_7: ((blockleistung/100)*7),
            KraftwerkStatus.P_8: ((blockleistung/100)*8),
            KraftwerkStatus.P_9: ((blockleistung/100)*9),
            KraftwerkStatus.P_10: ((blockleistung/100)*10),
            KraftwerkStatus.P_11: ((blockleistung/100)*11),
            KraftwerkStatus.P_12: ((blockleistung/100)*12),
            KraftwerkStatus.P_13: ((blockleistung/100)*13),
            KraftwerkStatus.P_14: ((blockleistung/100)*14),
            KraftwerkStatus.P_15: ((blockleistung/100)*15),
            KraftwerkStatus.P_16: ((blockleistung/100)*16),
            KraftwerkStatus.P_17: ((blockleistung/100)*17),
            KraftwerkStatus.P_18: ((blockleistung/100)*18),
            KraftwerkStatus.P_19: ((blockleistung/100)*19),
            KraftwerkStatus.P_20: ((blockleistung/100)*20),
            KraftwerkStatus.P_21: ((blockleistung/100)*21),
            KraftwerkStatus.P_22: ((blockleistung/100)*22),
            KraftwerkStatus.P_23: ((blockleistung/100)*23),
            KraftwerkStatus.P_24: ((blockleistung/100)*24),
            KraftwerkStatus.P_25: ((blockleistung/100)*25),
            KraftwerkStatus.P_26: ((blockleistung/100)*26),
            KraftwerkStatus.P_27: ((blockleistung/100)*27),
            KraftwerkStatus.P_28: ((blockleistung/100)*28),
            KraftwerkStatus.P_29: ((blockleistung/100)*29),
            KraftwerkStatus.P_30: ((blockleistung/100)*30),
            KraftwerkStatus.P_31: ((blockleistung/100)*31),
            KraftwerkStatus.P_32: ((blockleistung/100)*32),
            KraftwerkStatus.P_33: ((blockleistung/100)*33),
            KraftwerkStatus.P_34: ((blockleistung/100)*34),
            KraftwerkStatus.P_35: ((blockleistung/100)*35),
            KraftwerkStatus.P_36: ((blockleistung/100)*36),
            KraftwerkStatus.P_37: ((blockleistung/100)*37),
            KraftwerkStatus.P_38: ((blockleistung/100)*38),
            KraftwerkStatus.P_39: ((blockleistung/100)*39),
            KraftwerkStatus.P_40: ((blockleistung/100)*40),
            KraftwerkStatus.P_41: ((blockleistung/100)*41),
            KraftwerkStatus.P_42: ((blockleistung/100)*42),
            KraftwerkStatus.P_43: ((blockleistung/100)*43),
            KraftwerkStatus.P_44: ((blockleistung/100)*44),
            KraftwerkStatus.P_45: ((blockleistung/100)*45),
            KraftwerkStatus.P_46: ((blockleistung/100)*46),
            KraftwerkStatus.P_47: ((blockleistung/100)*47),
            KraftwerkStatus.P_48: ((blockleistung/100)*48),
            KraftwerkStatus.P_49: ((blockleistung/100)*49),
            KraftwerkStatus.P_50: ((blockleistung/100)*50),
            KraftwerkStatus.P_51: ((blockleistung/100)*51),
            KraftwerkStatus.P_52: ((blockleistung/100)*52),
            KraftwerkStatus.P_53: ((blockleistung/100)*53),
            KraftwerkStatus.P_54: ((blockleistung/100)*54),
            KraftwerkStatus.P_55: ((blockleistung/100)*55),
            KraftwerkStatus.P_56: ((blockleistung/100)*56),
            KraftwerkStatus.P_57: ((blockleistung/100)*57),
            KraftwerkStatus.P_58: ((blockleistung/100)*58),
            KraftwerkStatus.P_59: ((blockleistung/100)*59),
            KraftwerkStatus.P_60: ((blockleistung/100)*60),
            KraftwerkStatus.P_61: ((blockleistung/100)*61),
            KraftwerkStatus.P_62: ((blockleistung/100)*62),
            KraftwerkStatus.P_63: ((blockleistung/100)*63),
            KraftwerkStatus.P_64: ((blockleistung/100)*64),
            KraftwerkStatus.P_65: ((blockleistung/100)*65),
            KraftwerkStatus.P_66: ((blockleistung/100)*66),
            KraftwerkStatus.P_67: ((blockleistung/100)*67),
            KraftwerkStatus.P_68: ((blockleistung/100)*68),
            KraftwerkStatus.P_69: ((blockleistung/100)*69),
            KraftwerkStatus.P_70: ((blockleistung/100)*70),
            KraftwerkStatus.P_71: ((blockleistung/100)*71),
            KraftwerkStatus.P_72: ((blockleistung/100)*72),
            KraftwerkStatus.P_73: ((blockleistung/100)*73),
            KraftwerkStatus.P_74: ((blockleistung/100)*74),
            KraftwerkStatus.P_75: ((blockleistung/100)*75),
            KraftwerkStatus.P_76: ((blockleistung/100)*76),
            KraftwerkStatus.P_77: ((blockleistung/100)*77),
            KraftwerkStatus.P_78: ((blockleistung/100)*78),
            KraftwerkStatus.P_79: ((blockleistung/100)*79),
            KraftwerkStatus.P_80: ((blockleistung/100)*80),
            KraftwerkStatus.P_81: ((blockleistung/100)*81),
            KraftwerkStatus.P_82: ((blockleistung/100)*82),
            KraftwerkStatus.P_83: ((blockleistung/100)*83),
            KraftwerkStatus.P_84: ((blockleistung/100)*84),
            KraftwerkStatus.P_85: ((blockleistung/100)*85),
            KraftwerkStatus.P_86: ((blockleistung/100)*86),
            KraftwerkStatus.P_87: ((blockleistung/100)*87),
            KraftwerkStatus.P_88: ((blockleistung/100)*88),
            KraftwerkStatus.P_89: ((blockleistung/100)*89),
            KraftwerkStatus.P_90: ((blockleistung/100)*90),
            KraftwerkStatus.P_91: ((blockleistung/100)*91),
            KraftwerkStatus.P_92: ((blockleistung/100)*92),
            KraftwerkStatus.P_93: ((blockleistung/100)*93),
            KraftwerkStatus.P_94: ((blockleistung/100)*94),
            KraftwerkStatus.P_95: ((blockleistung/100)*95),
            KraftwerkStatus.P_96: ((blockleistung/100)*96),
            KraftwerkStatus.P_97: ((blockleistung/100)*97),
            KraftwerkStatus.P_98: ((blockleistung/100)*98),
            KraftwerkStatus.P_99: ((blockleistung/100)*99),
            KraftwerkStatus.P_100: blockleistung
        }
    ))

industrie1 = Verbraucher(grundbedarf=1250)

windpark1 = Windpark(
    initStatus=KraftwerkStatus.P_100,
    initStatusMap={
        KraftwerkStatus.P_0: 0,
        KraftwerkStatus.P_100: 500
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

    energiebedarf = wohngebiet1.berechne_bedarf(uhrzeit) + industrie1.berechne_bedarf(uhrzeit)
    energiebedarf = energiebedarf - windpark1.get_leistung()
    benoetigte_leistung = ceil((energiebedarf / blockleistung) * (100 / anzahl_kraftwerke))

    for kraftwerk in kraftwerke:
        if benoetigte_leistung >= 100:
            quit()
        # Optimierte if-Bedingungen:
        if 0 < benoetigte_leistung <= 100:
            kraftwerk.set_status(getattr(KraftwerkStatus, f"P_{int(benoetigte_leistung)}"))

    ueberschuss = sum(kraftwerk.get_leistung() for kraftwerk in kraftwerke) - energiebedarf

    print(f"Uhrzeit: {uhrzeit} Uhr")
    print(f"Energiebedarf insgesamt: {energiebedarf} MW")
    for i, kraftwerk in enumerate(kraftwerke):
        print(f"Kohlekraftwerk {i+1}: {kraftwerk.status} mit {kraftwerk.get_leistung()} MW")
    print(f"Überschuss: {ueberschuss} MW")
    print("-" * 30)

    time.sleep(1)