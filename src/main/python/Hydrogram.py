import pandas as pd
import numpy as np

class Hydrogram():

    def __init__(self, hydroArgs):
        self.name = hydroArgs["name"]
        if hydroArgs["type"] == "Lavabre":
            self.initLavabre(hydroArgs)
        elif hydroArgs["type"] == "Importer":
            self.data = pd.DataFrame({'t (s)':[0], 'Q (m3/s)':[0]})
        elif hydroArgs["type"] == "Manuel":
            self.data = pd.DataFrame({'t (s)':[0], 'Q (m3/s)':[0]})
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
    
    def copy(self, name):
        return Hydrogram({"name":name, "data":self.data.copy(), "type":"copy"})


    def __eq__(self, other):
        if isinstance(other, Hydrogram):
            return self.name == other.name
        else:
            return super().__eq__(other)

