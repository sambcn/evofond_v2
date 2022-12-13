import pandas as pd

from utils import AVAILABLE_SECTION_TYPES

class Profile():

    def __init__(self, name, type, data=None, granulo=None):
        """
        First column of data must ALWAYS be absscissa
        """
        self.name = name
        if not(type in AVAILABLE_SECTION_TYPES):
            raise ValueError("Profile type must be in {AVAILABLE_SECTION_TYPES}")
        self.type = type
        if not(isinstance(data, pd.DataFrame)):
            if type == "Rectangular":
                self.data = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b [m] \n(largeur)':[None]})
            elif type == "Trapezoidal":
                self.data = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b0 [m] \n(largeur du fond)':[None], 'b0_min [m] \n(largeur minimale\n du fond)':[None], 'f_left [m/m] \n(fruit rive gauche)':[None], 'f_right [m/m] \n(fruit rive droite)':[None]})
        else:
            self.data = data
        if not(isinstance(granulo, pd.DataFrame)):
            self.granulo = pd.DataFrame({"nom":[], "x début":[], "x fin":[]})
        else:
            self.granulo = granulo

    def setData(self, newData):
        self.data = newData

    def importData(self, path):
        data = pd.read_csv(path)
        
        nbCol = self.data.shape[1]
        colNames = list(self.data.columns)
        if data.shape[1] < nbCol:
            raise ValueError(f"{self.type} profile data must have {nbCol} columns : {colNames}")
        
        self.data = data[[data.columns[i] for i in range(nbCol)]]
        colDict = dict()
        for nameInCSV, realName in zip(list(data.columns), colNames):
            colDict[nameInCSV] = realName
        self.data = self.data.rename(columns=colDict)

    def addColumn(self, colName):
        self.data[colName] = None

    def copy(self, name):
        return Profile(name, self.type, self.data.copy(), self.granulo.copy())

    def __eq__(self, other):
        if isinstance(other, Profile):
            return self.name == other.name
        else:
            return super().__eq__(other)

    def getAbscissaList(self):
        l = self.data[~(self.data[self.data.columns[0]].isnull())][self.data.columns[0]].values.tolist()
        return [float(x) for x in l]

    def getGranuloName(self, x):
        for i in range(self.granulo.shape[0]):
            if self.granulo.iloc[i, 1] <= x <= self.granulo.iloc[i, 2]:
                return self.granulo.iloc[i, 0]
        return None