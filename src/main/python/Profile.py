from multiprocessing.sharedctypes import Value

import pandas as pd

class Profile():

    def __init__(self, name, type, data=None):
        """
        First column of data must ALWAYS be absscissa
        """
        self.name = name
        AVAILABLE_TYPES = ["Rectangular", "Trapezoidal"]
        if not(type in AVAILABLE_TYPES):
            raise ValueError("Profile type must be in {AVAILABLE_TYPES}")
        self.type = type
        if not(isinstance(data, pd.DataFrame)):
            if type == "Rectangular":
                self.data = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b [m] \n(largeur)':[None]})
            elif type == "Trapezoidal":
                self.data = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b0 [m] \n(largeur du fond)':[None], 'b0_min [m] \n(largeur minimale du fond)':[None], 'f_left [m/m] \n(fruit rive gauche)':[None], 'f_right [m/m] \n(fruit rive gauche)':[None]})
        else:
            self.data = data

    def setData(self, newData):
        self.data = newData

    def copy(self, name):
        return Profile(name, self.type, self.data.copy())

    def __eq__(self, other):
        if isinstance(other, Profile):
            return self.name == other.name
        else:
            return super().__eq__(other)
