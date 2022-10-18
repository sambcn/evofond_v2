from back.sedimentTransport.lefort2015 import Lefort2015
from back.sedimentTransport.lefortsogreah1991 import LefortSogreah1991
from back.sedimentTransport.meunier1989 import Meunier1989
from back.sedimentTransport.meyerpeter1948 import MeyerPeter1948
from back.sedimentTransport.piton2016 import Piton2016
from back.sedimentTransport.pitonrecking2017 import PitonRecking2017
from back.sedimentTransport.rickenmann1990 import Rickenmann1990
from back.sedimentTransport.rickenmann1991 import Rickenmann1991

from back.granulometry import Granulometry as granuloBack

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
    granulometryBack = granuloBack(granulometry.dm, granulometry.d30, granulometry.d50, granulometry.d90, granulometry.d84tb, granulometry.d84bs, granulometry.Gr)
    QsList = []
    for Q in QList:
        QsList.append(law.compute_Qs_formula(width, granulometryBack, Q, slope))
    return QsList
