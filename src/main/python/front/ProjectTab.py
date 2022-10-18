from PyQt5.QtWidgets import (
   QPushButton, QHBoxLayout, QLabel, QFileDialog, QMessageBox, QVBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

from front.DialogEditProject import DialogEditProject
from front.Tab import Tab
from front.Project import Project

import pickle as pkl


class ProjectTab(Tab):
    
    def __init__(self, tabBar):
        super(ProjectTab, self).__init__(tabBar, "Projet", tabBar.getResource("images\\project.png"))
        
        self.currentProject = Project()
        self.newProjectButton = QPushButton(" Nouveau projet")
        self.newProjectButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newProjectButton.released.connect(self.newProjectButtonReleased)
        self.loadProjectButton = QPushButton(" Charger projet")
        self.loadProjectButton.setIcon(QIcon(self.getResource("images\\load.png")))
        self.loadProjectButton.released.connect(self.loadProjectButtonReleased)
        self.saveProjectButton = QPushButton(" Enregistrer")
        self.saveProjectButton.setIcon(QIcon(self.getResource("images\\save.png")))
        self.saveProjectButton.released.connect(self.saveProjectButtonReleased)
        self.saveAsProjectButton = QPushButton(" Enregistrer sous")
        self.saveAsProjectButton.setIcon(QIcon(self.getResource("images\\saveAs.png")))
        self.saveAsProjectButton.released.connect(self.saveAsProjectButtonReleased)
        self.text = QLabel(str(self.currentProject))
        self.editTextButton = QPushButton(" Modifier")
        self.editTextButton.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editTextButton.released.connect(self.editTextButtonRealeased)
        self.imageONFRTM = QLabel()
        pixmap = QPixmap(self.getResource('images\\onfrtm.png'))
        pixmap = pixmap.scaled(QSize(300,300), Qt.KeepAspectRatio)
        self.imageONFRTM.setPixmap(pixmap)
        
        self.vLayout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layout2 = QHBoxLayout()        
        self.layout1.addWidget(self.newProjectButton)
        self.layout1.addWidget(self.loadProjectButton)
        self.layout1.addWidget(self.saveProjectButton)
        self.layout1.addWidget(self.saveAsProjectButton)
        self.layout2.addWidget(self.text, alignment=Qt.AlignRight)
        self.layout2.addWidget(self.editTextButton, alignment=(Qt.AlignLeft))
        self.layout2.addWidget(self.imageONFRTM, alignment=(Qt.AlignBottom | Qt.AlignRight))
        self.vLayout.addLayout(self.layout1)
        self.vLayout.addLayout(self.layout2)
        self.layout.addLayout(self.vLayout)

    def newProjectButtonReleased(self):
        if not(self.leavingProjectCheck()):
            return
        self.currentProject = Project()
        self.editTextButtonRealeased()
        self.updateText()
        self.tabBar.refresh()
        return

    def loadProjectButtonReleased(self):
        if not(self.leavingProjectCheck()):
            return
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.evf")
        if dlg.exec():
            try:
                self.currentProject = pkl.load(open(dlg.selectedFiles()[-1], 'rb'))
                self.updateText()
                self.tabBar.refresh()
            except (AttributeError, EOFError):
                QMessageBox.critical(self, "Impossible d'ouvrir ce fichier", "Le fichier sélectionné est corrompu, impossible de le lire")
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

    def leavingProjectCheck(self):
        if self.getProject().needToBeSaved:
            button = QMessageBox.question(self, "Modifications non enregistrées", "Souhaitez vous enregistrez avant de quitter ?")
            if button == QMessageBox.Yes:
                self.saveProjectButtonReleased()
                if self.getProject().needToBeSaved:
                    return False
                return True
            if button == QMessageBox.No:
                return True
        else:
            return True