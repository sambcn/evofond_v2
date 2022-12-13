import pandas as pd
import numpy as np

class Hydrogram():

    def __init__(self, hydroArgs):
        self.name = hydroArgs["name"]
        self.properties = f"méthode de création : {hydroArgs['type']}\n"
        if hydroArgs["type"] == "Lavabre":
            self.initLavabre(hydroArgs)
        elif hydroArgs["type"] == "Importer":
            self.initImport(hydroArgs)
        elif hydroArgs["type"] == "Manuel":
            self.data = pd.DataFrame({'t [s]':[None], 'Q [m3/s]':[None]})
        elif hydroArgs["type"] == "copy":
            self.data = hydroArgs["data"]

    def initLavabre(self, hydroArgs):
        t = np.arange(0, hydroArgs['d'], hydroArgs['dt'])
        Qmax = hydroArgs["Qmax"]
        Qbase = hydroArgs["Qmin"]
        tm = hydroArgs["tmax"]
        alpha = hydroArgs["alpha"]
        Q=np.array([(Qmax-Qbase)*2*np.power(ti/tm,alpha)/(1+np.power(ti/tm,2*alpha))+Qbase for ti in t])
        self.data = pd.DataFrame({'t [s]':t, 'Q [m3/s]':Q})
        self.properties += f"d : {hydroArgs['d']}s\n"
        self.properties += f"dt : {hydroArgs['dt']}s\n"
        self.properties += f"Qmax : {Qmax}m3/s\n"
        self.properties += f"Qbase : {Qbase}m3/s\n"
        self.properties += f"tm : {tm}s\n"
        self.properties += f"alpha : {alpha}\n"

    def initImport(self, hydroArgs):
        data = pd.read_csv(hydroArgs["path"])
        
        if data.shape[1] < 2:
            raise ValueError("Hydrogram data must have at least two columns to describe Q(t)")
        
        self.data = data[[data.columns[0], data.columns[1]]]
        self.data = self.data.rename(columns={data.columns[0]:"t [s]", data.columns[1]:"Q [m3/s]"})
        self.properties += f"chemin du fichier importé : {hydroArgs['path']}"
            
    def copy(self, name):
        return Hydrogram({"name":name, "data":self.data.copy(), "type":"copy"})

    def __eq__(self, other):
        if isinstance(other, Hydrogram):
            return self.name == other.name
        else:
            return super().__eq__(other)

