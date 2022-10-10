from PyQt5.QtCore import QDateTime

from Hydrogram import Hydrogram

import pickle as pkl

class Project():

    def __init__(self):
        self.name = ""
        self.creationDate = QDateTime.currentDateTime().toString()
        self.lastModifDate = self.creationDate
        self.author = ""
        self.description = ""
        self.hydrogramList = []
        self.hydrogramSelected = None
        self.hydrogramSelectedIndex = None
        self.path = None

    def getHydrogramNameList(self):
        return [h.name for h in self.hydrogramList]

    def addHydrogram(self, hydrogram):
        self.hydrogramList.append(hydrogram)
        self.updateModifDate()

    def setHydrogramSelected(self, name):
        for i, h in enumerate(self.hydrogramList):
            if h.name == name:
                self.updateModifDate()
                self.hydrogramSelected = h
                self.hydrogramSelectedIndex = i
                return

    def deleteHydrogram(self, h):
        for i, h2 in enumerate(self.hydrogramList):
            if h2 == h:
                self.hydrogramList.pop(i)
                self.updateModifDate()
                if len(self.hydrogramList) == 0:
                    self.hydrogramSelected = None
                    self.hydrogramSelectedIndex = None
                else:
                    self.hydrogramSelected = self.hydrogramList[0]
                    self.hydrogramSelectedIndex = 0
                return
        return

    def save(self):
        pkl.dump(self, open(self.path, 'wb'))

    def saveAs(self, path):
        self.path = path
        self.save()

    def updateModifDate(self):
        self.lastModifDate = QDateTime.currentDateTime().toString()

    def __str__(self):
        return f"Nom du projet : {self.name}\nDate de création : {self.creationDate}\nNom du créateur : {self.author}\nDernière modification : {self.lastModifDate}\nChemin : {self.path}\n\n\n\nDescription : \n\n{self.description}\n"