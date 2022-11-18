from PyQt5.QtCore import QDateTime

import pickle as pkl
import gc

class Project():

    def __init__(self):
        self.name = ""
        self.creationDate = QDateTime.currentDateTime().toString()
        self.lastModifDate = self.creationDate
        self.needToBeSaved = False
        self.author = ""
        self.description = ""
        self.path = None

        self.hydrogramList = []
        self.hydrogramSelected = None
        self.hydrogramSelectedIndex = None

        self.granulometryList = []
        self.granulometrySelected = None
        self.granulometrySelectedIndex = None

        self.sedimentogramList = []
        self.sedimentogramSelected = None
        self.sedimentogramSelectedIndex = None

        self.profileList = []
        self.profileSelected = None
        self.profileSelectedIndex = None
        
        self.modelList = []
        self.modelSelected = None
        self.modelSelectedIndex = None

    def getHydrogram(self, name):
        for h in self.hydrogramList:
            if h.name == name:
                return h
        return None 

    def getGranulometry(self, name):
        for g in self.granulometryList:
            if g.name == name:
                return g
        return None 

    def getSedimentogram(self, name):
        for s in self.sedimentogramList:
            if s.name == name:
                return s
        return None 

    def getProfile(self, name):
        for p in self.profileList:
            if p.name == name:
                return p
        return None 

    def getModel(self, name):
        for m in self.modelList:
            if m.name == name:
                return m
        return None 

    def getHydrogramNameList(self):
        return [h.name for h in self.hydrogramList]

    def getGranulometryNameList(self):
        return [g.name for g in self.granulometryList]

    def getSedimentogramNameList(self):
        return [s.name for s in self.sedimentogramList]

    def getProfileNameList(self):
        return [p.name for p in self.profileList]

    def getModelNameList(self):
        return [m.name for m in self.modelList]

    def addHydrogram(self, hydrogram):
        self.hydrogramList.append(hydrogram)
        self.updateModifDate()
        self.needToBeSaved = True

    def addGranulometry(self, granulometry):
        self.granulometryList.append(granulometry)
        self.updateModifDate()
        self.needToBeSaved = True

    def addSedimentogram(self, sedimentogram):
        self.sedimentogramList.append(sedimentogram)
        self.updateModifDate()
        self.needToBeSaved = True

    def addProfile(self, profile):
        self.profileList.append(profile)
        self.updateModifDate()
        self.needToBeSaved = True

    def addModel(self, model):
        self.modelList.append(model)
        self.updateModifDate()
        self.needToBeSaved = True

    def setHydrogramSelected(self, name):
        for i, h in enumerate(self.hydrogramList):
            if h.name == name:
                self.updateModifDate()
                self.hydrogramSelected = h
                self.hydrogramSelectedIndex = i
                return

    def setGranulometrySelected(self, name):
        for i, g in enumerate(self.granulometryList):
            if g.name == name:
                self.updateModifDate()
                self.granulometrySelected = g
                self.granulometrySelectedIndex = i
                return

    def setSedimentogramSelected(self, name):
        for i, s in enumerate(self.sedimentogramList):
            if s.name == name:
                self.updateModifDate()
                self.sedimentogramSelected = s
                self.sedimentogramSelectedIndex = i
                return

    def setProfileSelected(self, name):
        for i, p in enumerate(self.profileList):
            if p.name == name:
                self.updateModifDate()
                self.profileSelected = p
                self.profileSelectedIndex = i
                return

    def setModelSelected(self, name):
        for i, m in enumerate(self.modelList):
            if m.name == name:
                self.updateModifDate()
                self.modelSelected = m
                self.modelSelectedIndex = i
                return

    def setNoModelSelected(self):
        self.updateModifDate()
        self.modelSelected = None
        self.modelSelectedIndex = None

    def deleteHydrogram(self, h):
        for i, h2 in enumerate(self.hydrogramList):
            if h2 == h:
                self.hydrogramList.pop(i)
                self.updateModifDate()
                if len(self.hydrogramList) == 0:
                    self.hydrogramSelected = None
                    self.hydrogramSelectedIndex = None
                else:
                    self.hydrogramSelectedIndex = max(0, self.hydrogramSelectedIndex - 1)
                    self.hydrogramSelected = self.hydrogramList[self.hydrogramSelectedIndex]
                self.needToBeSaved = True
                return
        return

    def deleteGranulometry(self, g):
        for i, g2 in enumerate(self.granulometryList):
            if g2 == g:
                self.granulometryList.pop(i)
                self.updateModifDate()
                if len(self.granulometryList) == 0:
                    self.granulometrySelected = None
                    self.granulometrySelectedIndex = None
                else:
                    self.granulometrySelectedIndex = max(0, self.granulometrySelectedIndex - 1)
                    self.granulometrySelected = self.granulometryList[self.granulometrySelectedIndex]
                self.needToBeSaved = True
                return
        return

    def deleteSedimentogram(self, s):
        for i, s2 in enumerate(self.sedimentogramList):
            if s2 == s:
                self.sedimentogramList.pop(i)
                self.updateModifDate()
                if len(self.sedimentogramList) == 0:
                    self.sedimentogramSelected = None
                    self.sedimentogramSelectedIndex = None
                else:
                    self.sedimentogramSelectedIndex = max(0, self.sedimentogramSelectedIndex - 1)
                    self.sedimentogramSelected = self.sedimentogramList[self.sedimentogramSelectedIndex]
                self.needToBeSaved = True
                return
        return

    def deleteProfile(self, p):
        for i, p2 in enumerate(self.profileList):
            if p2 == p:
                self.profileList.pop(i)
                self.updateModifDate()
                if len(self.profileList) == 0:
                    self.profileSelected = None
                    self.profileSelectedIndex = None
                else:
                    self.profileSelectedIndex = max(0, self.profileSelectedIndex - 1)
                    self.profileSelected = self.profileList[self.profileSelectedIndex]
                self.needToBeSaved = True
                return
        return

    def deleteModel(self, m):
        for i, m2 in enumerate(self.modelList):
            if m2 == m:
                self.modelList.pop(i)
                self.updateModifDate()
                if len(self.modelList) == 0:
                    self.modelSelected = None
                    self.modelSelectedIndex = None
                else:
                    self.modelSelectedIndex = max(0, self.modelSelectedIndex - 1)
                    self.modelSelected = self.modelList[self.modelSelectedIndex]
                self.needToBeSaved = True
                return
        return

    def save(self):
        memory = self.needToBeSaved 
        try:
            self.needToBeSaved = False
            f = open(self.path, 'wb')
            gc.disable()
            pkl.dump(self, f, protocol=-1)
            gc.enable()
            f.close()
        except TypeError as e:
            self.needToBeSaved = memory
            raise(e)

    def saveAs(self, path):
        self.path = path
        self.save()

    def updateModifDate(self):
        self.lastModifDate = QDateTime.currentDateTime().toString()

    def __str__(self):
        return f"Nom du projet : {self.name}\nDate de création : {self.creationDate}\nNom du créateur : {self.author}\nDernière modification : {self.lastModifDate}\nChemin : {self.path}\n\n\n\nDescription : \n\n{self.description}\n\n\n\n{' ** Modifications non enregistrées **' if self.needToBeSaved else ''}"