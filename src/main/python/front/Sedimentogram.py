import pandas as pd
import numpy as np

from utils import calcSedimentogram

class Sedimentogram():

    def __init__(self, sedimentoArgs):
        self.name = sedimentoArgs["name"]
        self.properties = f"méthode de création : {sedimentoArgs['type']}\n"        
        if sedimentoArgs["type"] == "Classique":
            self.initClassical(sedimentoArgs)
        elif sedimentoArgs["type"] == "Importer":
            self.initImport(sedimentoArgs)
        elif sedimentoArgs["type"] == "Manuel":
            self.data = pd.DataFrame({'t [s]':[None], 'Qs [m3/s]':[None]})
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
        self.data = pd.DataFrame({'t [s]':t, 'Qs [m3/s]':Qs})
        self.properties += f"hydrogramme utilisé : {sedimentoArgs['hydrogram'].name}\n"        
        self.properties += f"loi de transport solide : {lawName}\n"        
        self.properties += f"pente d'apport : {s*100:.3f}%\n"        
        self.properties += f"largeur amont : {b}m\n"        

    def initImport(self, sedimentoArgs):
        data = pd.read_csv(sedimentoArgs["path"])
        
        if data.shape[1] < 2:
            raise ValueError("Sedimentogram data must have at least two columns to describe Qs(t)")
        
        self.data = data[[data.columns[0], data.columns[1]]]
        self.data = self.data.rename(columns={self.data.columns[0]:"t [s]", self.data.columns[1]:"Qs [m3/s]"})
        self.properties += f"chemin du fichier importé : {sedimentoArgs['path']}\n"        
            
    def copy(self, name):
        return Sedimentogram({"name":name, "data":self.data.copy(), "type":"copy"})

    def __eq__(self, other):
        if isinstance(other, Sedimentogram):
            return self.name == other.name
        else:
            return super().__eq__(other)

