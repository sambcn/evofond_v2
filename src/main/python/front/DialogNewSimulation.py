from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, QListWidget, QLabel, QPushButton, QAbstractItemView, QListWidgetItem,
    QWidget, QProgressBar   
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from front.DialogQuestionAnswer import DialogQuestionAnswer
from frontToBack import simulateModel
from utils import time_to_string

class DialogNewSimulation(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowTitle("New simulation")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.rejected.connect(self.end)

        self.layout = QVBoxLayout()

        ###

        self.parent().disableOtherTabs()
        self.hlayout = QHBoxLayout()

        self.vlayout1 = QVBoxLayout()
        self.modelSelectionnedList = []
        self.nameResultDict = dict()
        self.modelList = QListWidget()
        self.modelList.addItems(self.parent().getProject().getModelNameList())
        self.modelList.setSelectionMode(QAbstractItemView.ExtendedSelection)          
        self.modelList.itemSelectionChanged.connect(self.modelSelectionChanged)
        self.vlayout1.addWidget(QLabel("Sélectionnez les modèles à simuler :"))
        self.vlayout1.addWidget(self.modelList)
        self.hlayout.addLayout(self.vlayout1)

        self.vlayout2 = QVBoxLayout()
        self.hlayout.addLayout(self.vlayout2)
        self.vlayout3 = QVBoxLayout()
        self.hlayout.addLayout(self.vlayout3)
        self.setNameResultList()

        self.runButton = QPushButton(" Exécuter")
        self.runButton.setIcon(QIcon(self.parent().getResource("images\\runMan.png")))
        self.runButton.released.connect(self.runButtonReleased)

        self.currentSimulationLayout = QGridLayout()
        self.currentSimulationWidget = QWidget()
        self.currentSimulationWidget.setLayout(self.currentSimulationLayout)
        self.currentSimulationWidget.setVisible(False)

        ###

        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.runButton)
        self.layout.addWidget(self.currentSimulationWidget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def modelSelectionChanged(self):
        self.modelSelectionnedList = []
        for i in range(self.modelList.count()):
            item = self.modelList.item(i)
            if item.isSelected():
                self.modelSelectionnedList.append(item.text())
        self.setNameResultList()

    def setNameResultList(self):
        keys = self.nameResultDict.keys()
        values = self.nameResultDict.values()
        DialogNewSimulation._clearLayout(self.vlayout2)
        DialogNewSimulation._clearLayout(self.vlayout3)
        for m in self.modelSelectionnedList:
            if not(m in keys):
                name = m
                index = 1
                while name in self.parent().getResultNameList() or name in values:
                    name = m + f" ({index})"
                    index += 1
                self.nameResultDict[m] = name
            self.vlayout2.addWidget(QLabel(f"Nom du résultat pour le modèle '{m}' : \t {self.nameResultDict[m]} \t "))
            changeButton = QPushButton("changer le nom")
            changeButton.released.connect(self.changeButtonReleased(m))
            self.vlayout3.addWidget(changeButton, alignment=Qt.AlignRight)

    def changeButtonReleased(self, m):
        def f():
            dlg = DialogQuestionAnswer(self, "Choisissez le nouveau nom : ")
            if dlg.exec():
                if dlg.answer in self.parent().getResultNameList():
                    QMessageBox.critical(self, "Nom déjà existant", "Ce nom existe déjà.")
                    return
                elif dlg.answer == self.nameResultDict[m]:
                    QMessageBox.warning(self, "Nom identique", "Ce nom est le même que le précédent.")
                    return
                elif dlg.answer in self.nameResultDict.values():
                    QMessageBox.critical(self, "Nom déjà pris pour un autre modèle", "Ce nom est déjà choisi pour un autre modèle de cette simulation")
                    return
                else:
                    self.nameResultDict[m] = dlg.answer
                    self.setNameResultList()
                    return
        return f

    def runButtonReleased(self):
        ### freeze widgets
        DialogNewSimulation._disableLayout(self.vlayout1)
        DialogNewSimulation._disableLayout(self.vlayout2)
        DialogNewSimulation._disableLayout(self.vlayout3)
        self.runButton.setEnabled(False)
        ###

        ### Make the simulation layout visible
        self.currentSimulationWidget.setVisible(True)
        self.pBarList = []
        self.modelSimulationLabelList = []
        self.stopButtonList = []
        for i, m in enumerate(self.modelSelectionnedList):
            self.currentSimulationLayout.addWidget(QLabel(self.nameResultDict[m]), 2*i, 0)
            pBar = QProgressBar()
            pBar.setTextVisible(True)
            self.currentSimulationLayout.addWidget(pBar, 2*i, 1)
            self.pBarList.append(pBar)
            stopButton = QPushButton(" stop")
            stopButton.setEnabled(False)
            stopButton.setIcon(QIcon(self.parent().getResource("images\\stop.png")))
            stopButton.released.connect(self.stopButtonReleased)
            self.stopButtonList.append(stopButton)
            self.currentSimulationLayout.addWidget(stopButton, 2*i, 2)
            label = QLabel("")
            self.currentSimulationLayout.addWidget(label, 2*i+1, 1)
            self.modelSimulationLabelList.append(label)
        ###

        p = self.parent().getProject()
        for i, m in enumerate(self.modelSelectionnedList):
            self.stopButtonList[i].setEnabled(True)
            self.stopSimulation = False
            self.currentModelIndex = i
            model = p.getModel(m)
            try:
                result = simulateModel(p, model, self)
            except ValueError as e:
                self.updateModelSimulationLabel(text=str(e))
                result = None

            self.stopButtonList[i].setEnabled(False)
            if result == None:
                continue
            result["name"] = self.nameResultDict[m]
            result["model"] = str(model)
            result["saved"] = False
            self.parent().addResult(result)
            

        return  

    def stopButtonReleased(self):
        button = QMessageBox.question(self, "Stop simulation", f"Are you sure to stop the current simulation ({self.nameResultDict[self.modelSelectionnedList[self.currentModelIndex]]}) ?")
        if button == QMessageBox.Yes:
            self.stopSimulation = True
            self.updateModelSimulationLabel(text="Simulation stoppée")

    def updateProgressBar(self, percentage):
        self.pBarList[self.currentModelIndex].setValue(percentage)

    def updateModelSimulationLabel(self, time=None, expectedTime=None, text=None):
        if text == None:
            self.modelSimulationLabelList[self.currentModelIndex].setStyleSheet('color: black; font-style: Arial font; font-size: 12pt ')        
            self.modelSimulationLabelList[self.currentModelIndex].setText(f"temps de calcul : {time_to_string(time)}\n{'temps total estimé : '+time_to_string(expectedTime, decimals=0) if expectedTime != None else ''}")
        else:
            self.modelSimulationLabelList[self.currentModelIndex].setStyleSheet('color: red; font-style: Arial font; font-size: 12pt ')        
            self.modelSimulationLabelList[self.currentModelIndex].setText(text)

    def closeEvent(self, event):
        event.ignore()
        self.end()

    def end(self):
        self.parent().enableOtherTabs()
        self.parent().newSimulationButton.setEnabled(True)
        self.parent().loadResultButton.setEnabled(True)
        self.reject()

    def processEvents(self):
        self.parent().processEvents()

    def _clearLayout(layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def _disableLayout(layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setEnabled(False)

    def _enableLayout(layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setEnabled(True)
