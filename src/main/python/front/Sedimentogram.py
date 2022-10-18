import pandas as pd
import numpy as np

from utils import calcSedimentogram

class Sedimentogram():

    def __init__(self, sedimentoArgs):
        self.name = sedimentoArgs["name"]
        if sedimentoArgs["type"] == "Classique":
            self.initClassical(sedimentoArgs)
        elif sedimentoArgs["type"] == "Importer":
            self.initImport(sedimentoArgs)
        elif sedimentoArgs["type"] == "Manuel":
            self.data = pd.DataFrame({'t (s)':[None], 'Qs (m3/s)':[None]})
        elif sedimentoArgs["type"] == "copy":
            self.data = sedimentoArgs["data"]

    def initClassical(self, sedimentoArgs):
        h = sedimentoArgs["hydrogram"].data
        t = list(h[h.columns[0]])
        Q = list(h[h.columns[1]])
        lawName = sedimentoArgs["law"]
        b = sedimentoArgs["width"]
        s = sedimentoArgs["slope"]
        granulometry = sedimentoArgs["granulometry"]
        Qs = calcSedimentogram(lawName, Q, b, s, granulometry) 
        self.data = pd.DataFrame({'t (s)':t, 'Qs (m3/s)':Qs})

    def initImport(self, sedimentoArgs):
        data = pd.read_csv(sedimentoArgs["path"])
        
        if data.shape[1] < 2:
            raise ValueError("Sedimentogram data must have at least two columns to describe Qs(t)")
        
        self.data = data[[data.columns[0], data.columns[1]]]
            
    def copy(self, name):
        return Sedimentogram({"name":name, "data":self.data.copy(), "type":"copy"})

    def __eq__(self, other):
        if isinstance(other, Sedimentogram):
            return self.name == other.name
        else:
            return super().__eq__(other)

