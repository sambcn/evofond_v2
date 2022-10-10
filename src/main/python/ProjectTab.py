from Tab import Tab
from Project import Project
from PyQt5.QtWidgets import (
   QPushButton, QVBoxLayout, QLabel, QFileDialog
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QIcon

from DialogEditProject import DialogEditProject

import pickle as pkl


class ProjectTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Projet", "..\\icons\\base\\project.png")
        
        self.currentProject = Project()
        self.newProjectButton = QPushButton(" Nouveau projet")
        self.newProjectButton.setIcon(QIcon("..\\icons\\base\\add.png"))
        self.newProjectButton.released.connect(self.newProjectButtonReleased)
        self.loadProjectButton = QPushButton(" Charger projet")
        self.loadProjectButton.setIcon(QIcon("..\\icons\\base\\load.png"))
        self.loadProjectButton.released.connect(self.loadProjectButtonReleased)
        self.saveProjectButton = QPushButton(" Enregistrer")
        self.saveProjectButton.setIcon(QIcon("..\\icons\\base\\save.png"))
        self.saveProjectButton.released.connect(self.saveProjectButtonReleased)
        self.saveAsProjectButton = QPushButton(" Enregistrer sous")
        self.saveAsProjectButton.setIcon(QIcon("..\\icons\\base\\saveAs.png"))
        self.saveAsProjectButton.released.connect(self.saveAsProjectButtonReleased)
        self.text = QLabel(str(self.currentProject))
        self.editTextButton = QPushButton(" Modifier")
        self.editTextButton.setIcon(QIcon("..\\icons\\base\\edit.png"))
        self.editTextButton.released.connect(self.editTextButtonRealeased)
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout1.addWidget(self.newProjectButton)
        self.layout1.addWidget(self.loadProjectButton)
        self.layout1.addWidget(self.saveProjectButton)
        self.layout1.addWidget(self.saveAsProjectButton)
        self.layout2.addWidget(self.text, alignment= (Qt.AlignBottom | Qt.AlignHCenter))
        self.layout2.addWidget(self.editTextButton, alignment=(Qt.AlignTop | Qt.AlignHCenter))
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)

    def newProjectButtonReleased(self):
        self.currentProject = Project()
        self.editTextButtonRealeased()
        self.updateText()
        self.tabBar.refresh()
        return

    def loadProjectButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.evf")
        if dlg.exec():
            self.currentProject = pkl.load(open(dlg.selectedFiles()[-1], 'rb'))
            self.updateText()
            self.tabBar.refresh()
        return

    def saveProjectButtonReleased(self):
        try:
            self.currentProject.save()
            self.updateText()
        except TypeError:
            self.saveAsProjectButtonReleased()
        return

    def saveAsProjectButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setNameFilter("*.evf")
        dlg.setDefaultSuffix(".evf")
        if dlg.exec():
            self.currentProject.saveAs(dlg.selectedFiles()[-1])
            self.updateText()
        return

    def editTextButtonRealeased(self):
        dlg = DialogEditProject(self)
        if dlg.exec():
            projet = self.getProject()
            args = dlg.args
            projet.name = args["name"]
            projet.author = args["author"]
            projet.description = args["description"]
            projet.updateModifDate()
            self.updateText()
        return

    def updateText(self):
        self.text.setText(str(self.currentProject))
        return
    


