import numpy as np

from back.sedimentTransport.lefort2015 import Lefort2015
from back.sedimentTransport.lefortsogreah1991 import LefortSogreah1991
from back.sedimentTransport.meunier1989 import Meunier1989
from back.sedimentTransport.meyerpeter1948 import MeyerPeter1948
from back.sedimentTransport.piton2016 import Piton2016
from back.sedimentTransport.pitonrecking2017 import PitonRecking2017
from back.sedimentTransport.rickenmann1990 import Rickenmann1990
from back.sedimentTransport.rickenmann1991 import Rickenmann1991

from back.granulometry import Granulometry as granuloBack

AVAILABLE_HYDRAULIC_MODEL = [
    "Régime critique",
    "Régime varié avec loi de frottement"
]

AVAILABLE_FRICTION_LAW = [
    "Ferguson",
    "Manning-Strickler"
]

AVAILABLE_LIMITS = [
    "Personalisée",
    "Hauteur critique",
    "Hauteur normale"
]

AVAILABLE_SECTION_TYPES = [
    "Rectangular",
    "Trapezoidal"
    ]

SEDIMENT_TRANSPORT_LAW_DICT = {
    "Meunier1989": Meunier1989 ,
    "Lefort2015": Lefort2015,
    "LefortSogreah1991": LefortSogreah1991,
    "MeyerPeter1948": MeyerPeter1948,
    "Piton2016": Piton2016,
    "PitonRecking2017": PitonRecking2017,
    "Rickenmann1990": Rickenmann1990,
    "Rickenmann1991": Rickenmann1991
}

def calcSedimentogram(lawName, QList, width, slope, granulometry):
    law = SEDIMENT_TRANSPORT_LAW_DICT[lawName]()
    granulometryBack = convertGranuloFromFrontToBack(granulometry)
    QsList = []
    for Q in QList:
        QsList.append(law.compute_Qs_formula(width, granulometryBack, Q, slope))
    return QsList

def convertGranuloFromFrontToBack(granulometry):
    return granuloBack(granulometry.dm, granulometry.d30, granulometry.d50, granulometry.d90, granulometry.d84tb, granulometry.d84bs, granulometry.Gr)

def time_to_string(t, decimals=3):
    """return a string to print a given time t in seconds with the format Ah Bm Cs"""
    hours = int(t) // 3600
    minutes = (int(t) - 3600*hours) // 60
    seconds = t%60
    if not(decimals in range(6)):
        raise ValueError("decimals must be an integer between 0 and 5")
    if decimals == 0:
        seconds_str = f"{seconds:.0f}s"
    if decimals == 1:
        seconds_str = f"{seconds:.1f}s"
    if decimals == 2:
        seconds_str = f"{seconds:.2f}s"
    if decimals == 3:
        seconds_str = f"{seconds:.3f}s"
    if decimals == 4:
        seconds_str = f"{seconds:.4f}s"
    if decimals == 5:
        seconds_str = f"{seconds:.5f}s"
    if hours == 0:
        if minutes == 0:
            return seconds_str
        else:
            return f"{minutes}min " + seconds_str
    else:
        return f"{hours}h {minutes}min " + seconds_str

def getAccumulatedVolume(t, Q):
    V = [np.trapz(Q[:i], t[:i]) for i in range(1, len(t)+1)]
    return V