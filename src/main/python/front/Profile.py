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
                self.data = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b0 [m] \n(largeur du fond)':[None], 'b0_min [m] \n(largeur minimale du fond)':[None], 'f_left [m/m] \n(fruit rive gauche)':[None], 'f_right [m/m] \n(fruit rive gauche)':[None]})
        else:
            self.data = data
        if not(isinstance(granulo, pd.DataFrame)):
            self.granulo = pd.DataFrame({"nom":[], "x début":[], "x fin":[]})
        else:
            self.granulo = granulo

    def setData(self, newData):
        self.data = newData

    def copy(self, name):
        return Profile(name, self.type, self.data.copy())

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