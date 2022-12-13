from utils import AVAILABLE_HYDRAULIC_MODEL

class Model():

    def __init__(self, name):
        self.name = name
        self.hydrogram = None
        self.sedimentogram = None
        self.profile = None
        self.sedimentTransportLaw = None
        self.interpolation = False
        self.dx = None
        self.hydroModel = None
        self.frictionLaw = None
        self.upstreamCondition = None
        self.downstreamCondition = None
        self.cfl = 1.0
        self.dt = None
        self.dtForSave = None

    def copy(self, newName):
        m = Model(newName)
        m.hydrogram = self.hydrogram
        m.sedimentogram = self.sedimentogram
        m.profile = self.profile
        m.sedimentTransportLaw = self.sedimentTransportLaw
        m.interpolation = self.interpolation
        m.dx = self.dx
        m.hydroModel = self.hydroModel
        m.frictionLaw = self.frictionLaw
        m.upstreamCondition = self.upstreamCondition
        m.downstreamCondition = self.downstreamCondition
        m.cfl = self.cfl
        m.dt = self.dt
        m.dtForSave = self.dtForSave
        return m

    def __str__(self):
        string = f"modèle = {self.name}\n"
        string += f"hydrogramme = {self.hydrogram}\n"
        string += f"sedimentogramme = {self.sedimentogram}\n"
        string += f"profil = {self.profile}\n"
        string += f"loi de transport = {self.sedimentTransportLaw}\n"
        string += f"interpolation = {self.interpolation}\n"
        string += f"dx = {self.dx}\n"
        string += f"modèle hydraulique = {self.hydroModel}\n"
        if self.hydroModel == AVAILABLE_HYDRAULIC_MODEL[1]:
            string += f"loi de frottement = {self.frictionLaw}\n"
            string += f"condition amont = {self.upstreamCondition}\n"
            string += f"condition avale = {self.downstreamCondition}\n"
        if self.dt == None:
            string += f"cfl = {self.cfl}\n"
        else:
            string += f"dt = {self.dt}\n"
        if self.dtForSave == None:
            string += f"dtForSave = 'Sauvegarde complète'\n"
        else:
            string += f"dtForSave = {self.dtForSave}\n"
        return string

    def getBoolState(self, project):
        if self.getStringState(project) == "":
            return True
        else:
            return False

    def getStringState(self, project):
        s = ""
        if self.hydrogram == None:
            s += "- hydrogramme manquant\n"
        elif not(self.hydrogram in project.getHydrogramNameList()):
            s += f'- hydrogramme "{self.hydrogram}" inconnu\n'
        if self.sedimentogram == None:
            s += "- sédimentogramme manquant\n"
        elif not(self.sedimentogram in project.getSedimentogramNameList()):
            s += f'- sedimentogramme "{self.sedimentogram}" inconnu\n'
        if self.profile == None:
            s += "- profil manquant \n"
        elif not(self.profile in project.getProfileNameList()):
            s += "- loi de transport solide manquante \n"
        if self.sedimentTransportLaw == None:
            s += f'- profil "{self.profile}" inconnu \n'
        if self.interpolation:
            if self.dx == None:
                s += "- pas d'interpolation manquant \n"
            elif self.dx <= 0:
                s += "- le pas d'interpolation doit être > 0 \n"
        if self.upstreamCondition == None:
            s += "- condition amont manquante \n"
        elif (type(self.upstreamCondition) == int or type(self.upstreamCondition) == float) and self.upstreamCondition <= 0:
            s += "- la condition amont doit être strictement positive\n"
        if self.downstreamCondition == None:
            s += "- condition avale manquante \n"
        elif (type(self.downstreamCondition) == int or type(self.downstreamCondition) == float and self.downstreamCondition <= 0):
            s += "- la condition avale doit être strictement positive\n"

        if s != "":
            s = "INCOMPLET\n\n\n" + s
        return s
