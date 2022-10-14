from multiprocessing.sharedctypes import Value
import pandas as pd
import numpy as np

class Hydrogram():

    def __init__(self, hydroArgs):
        self.name = hydroArgs["name"]
        if hydroArgs["type"] == "Lavabre":
            self.initLavabre(hydroArgs)
        elif hydroArgs["type"] == "Importer":
            self.initImport(hydroArgs)
        elif hydroArgs["type"] == "Manuel":
            self.data = pd.DataFrame({'t (s)':[None], 'Q (m3/s)':[None]})
        elif hydroArgs["type"] == "copy":
            self.data = hydroArgs["data"]

    def initLavabre(self, hydroArgs):
        NB_POINTS = 1000
        t = np.linspace(0, hydroArgs['d'], NB_POINTS)
        Qmax = hydroArgs["Qmax"]
        Qbase = hydroArgs["Qmin"]
        tm = hydroArgs["tmax"]
        alpha = hydroArgs["alpha"]
        Q=np.array([(Qmax-Qbase)*2*np.power(ti/tm,alpha)/(1+np.power(ti/tm,2*alpha))+Qbase for ti in t])
        self.data = pd.DataFrame({'t (s)':t, 'Q (m3/s)':Q})

    def initImport(self, hydroArgs):
        data = pd.read_csv(hydroArgs["path"])
        
        if data.shape[1] < 2:
            raise ValueError("Hydrogram data must have at least two columns to describe Q(t)")
        
        self.data = data[[data.columns[0], data.columns[1]]]
            
    def copy(self, name):
        return Hydrogram({"name":name, "data":self.data.copy(), "type":"copy"})

    def __eq__(self, other):
        if isinstance(other, Hydrogram):
            return self.name == other.name
        else:
            return super().__eq__(other)

