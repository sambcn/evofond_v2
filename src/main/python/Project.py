from PyQt5.QtCore import QDateTime

from Hydrogram import Hydrogram
from Profile import Profile

import pandas as pd
import pickle as pkl

class Project():

    def __init__(self):
        self.name = ""
        self.creationDate = QDateTime.currentDateTime().toString()
        self.lastModifDate = self.creationDate
        self.needToBeSaved = False
        self.author = ""
        self.description = ""
        self.hydrogramList = []
        self.hydrogramSelected = None
        self.hydrogramSelectedIndex = None
        self.path = None
        self.profileList = []
        self.profileSelected = None
        self.profileSelectedIndex = 0

    def getHydrogramNameList(self):
        return [h.name for h in self.hydrogramList]

    def addHydrogram(self, hydrogram):
        self.hydrogramList.append(hydrogram)
        self.updateModifDate()
        self.needToBeSaved = True

    def addProfile(self, profile):
        self.profileList.append(profile)
        self.updateModifDate()
        self.needToBeSaved = True

    def setHydrogramSelected(self, name):
        for i, h in enumerate(self.hydrogramList):
            if h.name == name:
                self.updateModifDate()
                self.hydrogramSelected = h
                self.hydrogramSelectedIndex = i
                self.needToBeSaved = True
                return

    def setProfileSelected(self, name):
        for i, p in enumerate(self.profileList):
            if p.name == name:
                self.updateModifDate()
                self.profileSelected = p
                self.profileSelectedIndex = i
                self.needToBeSaved = True
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
                    self.hydrogramSelectedIndex = max(0, self.hydrogramSelectedIndex - 1)
                    self.hydrogramSelected = self.hydrogramList[self.hydrogramSelectedIndex]
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

    def save(self):
        memory = self.needToBeSaved 
        try:
            self.needToBeSaved = False
            pkl.dump(self, open(self.path, 'wb'))
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