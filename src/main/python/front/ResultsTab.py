from ctypes import alignment
from PyQt5.QtWidgets import (
    QPushButton, QListWidget, QVBoxLayout, QComboBox, QLabel, QListWidgetItem, QAbstractItemView, QGridLayout, QSlider, QWidget, QHBoxLayout,
    QMessageBox, QFileDialog, QApplication
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.MplCanvas import MplCanvas, NavigationToolbar
from frontToBack import simulateModel
from front.DialogNewSimulation import DialogNewSimulation
from front.DialogExportData import DialogExportData
from front.DialogDelete import DialogDelete
from front.DialogPlotProfileDataOnResults import DialogPlotProfileDataOnResults
from utils import time_to_string

import json

class ResultsTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Résultats", tabBar.getResource("images\\results.png"))

        self.resultList = []

        self.listLayout = QVBoxLayout()
        self.resultQList = QListWidget()
        self.listLayout.addWidget(self.resultQList)
        self.resultQList.currentTextChanged.connect(self.resultChoiceChanged)
        self.setResultList()

        self.saveResultButton = QPushButton(" SAVE")
        self.saveResultButton.setIcon(QIcon(self.getResource("images\\save.png")))
        self.saveResultButton.released.connect(self.saveResultButtonReleased)
        self.listLayout.addWidget(self.saveResultButton)
        self.loadResultButton = QPushButton(" LOAD")
        self.loadResultButton.setIcon(QIcon(self.getResource("images\\load.png")))
        self.loadResultButton.released.connect(self.loadResultButtonReleased)
        self.listLayout.addWidget(self.loadResultButton)
        self.deleteResultButton = QPushButton(" DELETE")
        self.deleteResultButton.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.deleteResultButton.released.connect(self.deleteResultButtonReleased)
        self.listLayout.addWidget(self.deleteResultButton)
        self.propertiesWidget = QPushButton(" PROPERTIES")
        self.propertiesWidget.setIcon(QIcon(self.getResource("images\\properties.png")))
        self.propertiesWidget.released.connect(self.propertiesButtonReleased)
        self.listLayout.addWidget(self.propertiesWidget)
        self.paramLayout = QVBoxLayout()

        self.newSimulationButton = QPushButton(" Nouvelle simulation")
        self.newSimulationButton.setIcon(QIcon(self.getResource("images\\run.png")))
        self.newSimulationButton.released.connect(self.newSimulation)
        self.paramLayout.addWidget(self.newSimulationButton)

        self.sliderLabel = QLabel("")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.plotData)
        self.paramLayout.addWidget(self.sliderLabel)
        self.paramLayout.addWidget(self.slider)

        self.dataLayout = QHBoxLayout()
        self.varList1 = QListWidget()
        self.varList1.itemSelectionChanged.connect(self.varList1changed)
        self.varList2 = QListWidget()
        self.varList2.setSelectionMode(QAbstractItemView.ExtendedSelection)          
        self.varList2.itemSelectionChanged.connect(self.plotData)
        self.varList3 = QListWidget()
        self.varList3.setSelectionMode(QAbstractItemView.ExtendedSelection)   
        self.varList3.itemSelectionChanged.connect(self.plotData)
        self.setVarLists()
        self.dataLayout.addWidget(self.varList1)
        self.dataLayout.addWidget(self.varList2)
        self.dataLayout.addWidget(self.varList3)
        w = QWidget()
        w.setLayout(self.dataLayout)
        w.setFont(QFont('Arial font', 10))
        self.paramLayout.addWidget(w)

        self.plotProfileDataButton = QPushButton(" Superposer les données d'un profil")
        self.plotProfileDataButton.setIcon(QIcon(self.getResource("images\\doubleplot.png")))
        self.plotProfileDataButton.released.connect(self.plotProfileDataButtonReleased)
        self.paramLayout.addWidget(self.plotProfileDataButton)
        self.dataAxis1 = dict()
        self.dataAxis2 = dict()
        self.profileName = None
        self.exportButton = QPushButton(" Exporter les données")
        self.exportButton.setIcon(QIcon(self.getResource("images\\export.png")))
        self.exportButton.released.connect(self.exportButtonReleased)
        self.paramLayout.addWidget(self.exportButton)

        self.plotLayout = QVBoxLayout()
        self.rescaleButton =QPushButton(" Réinitialiser l'échelle")
        self.rescaleButton.setIcon(QIcon(self.getResource("images\\refresh.png")))
        self.rescaleButton.released.connect(self.rescale)
        self.plotLayout.addWidget(self.rescaleButton)
        self.volumeLabel = QLabel("")
        self.volumeLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.plotLayout.addWidget(self.volumeLabel)
        self.sc = MplCanvas()
        self.sc.toggle.connect(self.toggleFigure)
        # self.plotLayout.addWidget(self.sc, stretch=100)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.plotWidget = QWidget(parent=self)
        self._vlaout = QVBoxLayout()
        self._vlaout.addWidget(self.sc)
        self._vlaout.addWidget(self.toolbar)
        self.plotWidget.setLayout(self._vlaout)
        self.plotLayout.addWidget(self.plotWidget, stretch=100)
        # self.plotLayout.addWidget(self.toolbar)
        self.plotData()

        self.layout.addLayout(self.listLayout)
        self.layout.addLayout(self.paramLayout)
        self.layout.addLayout(self.plotLayout, stretch=100)

    def getResult(self, name):
        for r in self.resultList:
            if r["name"] == name:
                return r
        return None
        
    def getResultNameList(self):
        return [r["name"] for r in self.resultList]        

    def addResult(self, result):
        self.resultList.append(result)
        item = QListWidgetItem(result["name"])
        self.resultQList.addItem(item)
        self.resultQList.setCurrentItem(item)

    def deleteResult(self, rName):
        for i, r in enumerate(self.resultList):
            if r["name"] == rName:
                self.resultList.pop(i)
                return
        return
        
    def newSimulation(self):
        dlg = DialogNewSimulation(parent=self)
        dlg.show()
        self.newSimulationButton.setEnabled(False)
        self.loadResultButton.setEnabled(False)

    def saveResultButtonReleased(self):
        if self.currentResult == None:
            return
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setNameFilter("*.json")
        dlg.setDefaultSuffix(".json")
        if dlg.exec():
            f = open(dlg.selectedFiles()[-1], 'w')
            waitingWindow = QMessageBox(self)
            waitingWindow.setIcon(QMessageBox.Information)
            waitingWindow.setWindowTitle("Sauvegarde en cours, ne quittez pas...")
            # waitingWindow.setText("Sauvegarde en cours, ne quittez pas...")
            waitingWindow.setAttribute(Qt.WA_DeleteOnClose)
            # waitingWindow.setStandardButtons(QMessageBox.NoButton)
            waitingWindow.setWindowFlag(Qt.WindowCloseButtonHint, False)
            waitingWindow.show()       
            self.currentResult["saved"] = True     
            json.dump(self.currentResult, f)
            waitingWindow.close()            
            f.close()
            QMessageBox.information(self, "Résultat sauvegardé", "Le résultat a été sauvegardé avec succès !")
        return

    def loadResultButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.json")
        if dlg.exec():
            f = open(dlg.selectedFiles()[-1], 'r')
            waitingWindow = QMessageBox(self)
            waitingWindow.setIcon(QMessageBox.Information)
            waitingWindow.setWindowTitle("Chargement du fichier en cours, ne quittez pas...")
            waitingWindow.setAttribute(Qt.WA_DeleteOnClose)
            waitingWindow.setWindowFlag(Qt.WindowCloseButtonHint, False)
            waitingWindow.show()
            result = json.load(f)
            waitingWindow.setWindowTitle("Vérification du format en cours, ne quittez pas...") 
            f.close
            if not(self.checkResultFormat(result)):
                waitingWindow.close()
                return
            waitingWindow.close()
            self.addResult(result)
            self.currentResult = result

    def propertiesButtonReleased(self):
        if self.currentResult == None:
            return
        QMessageBox.information(self, f"propriétés de {self.currentResult['name']}", self.currentResult['model'])

    def checkResultFormat(self, result):
        if type(result) != dict:
            return False
        keys = result.keys()
        neededKeys = ["name", "abscissa", "water_depth", "bottom_height", "minimal_bottom_height", "time", "energy", "water_discharge", "width"]
        for neededKey in neededKeys:
            if not(neededKey in keys):
                QMessageBox.critical(self, "Fichier résultat corrompu", "Le fichier résultat a un format différent du fichier attendu. Impossible de l'ouvrir.")
                return False
        if result["name"] in self.getResultNameList():
            QMessageBox.critical(self, "nom de résultat déjà existant", f"Le nom du fichier résultat est le même que {result['name']}, vous ne pouvez pas importer deux projets de même nom.")
            return False
        lenX = len(result["abscissa"])
        lenT = len(result["time"])
        _2Dvariables = ["water_depth", "bottom_height", "energy", "width", "water_discharge"]
        _spatialVariables = ["minimal_bottom_height"]
        _timeVariables = []
        for key in _2Dvariables:
            data = result[key]
            if len(data) != lenT:
                QMessageBox.critical(self, "Fichier résultat corrompu", "Le fichier résultat a un format différent du fichier attendu. Impossible de l'ouvrir.")
                return False
            for di in data:
                if len(di) != lenX:
                    QMessageBox.critical(self, "Fichier résultat corrompu", "Le fichier résultat a un format différent du fichier attendu. Impossible de l'ouvrir.")
                    return False
        for key in _spatialVariables:
            if len(result[key]) != lenX:
                QMessageBox.critical(self, "Fichier résultat corrompu", "Le fichier résultat a un format différent du fichier attendu. Impossible de l'ouvrir.")
                return False
        for key in _timeVariables:
            if len(result[key]) != lenT:
                QMessageBox.critical(self, "Fichier résultat corrompu", "Le fichier résultat a un format différent du fichier attendu. Impossible de l'ouvrir.")
                return False
        return True

    def deleteResultButtonReleased(self):
        resultName = self.resultQList.currentItem().text()
        if resultName in self.getResultNameList():
            dlg = DialogDelete(resultName, parent=self)
            if dlg.exec():
                self.deleteResult(self.resultQList.currentItem().text())
                self.resultQList.takeItem(self.resultQList.currentRow())
                self.currentResult = self.getResult(self.resultQList.currentItem().text()) if self.resultQList.currentItem() != None else None

    def resultChoiceChanged(self, s):
        self.currentResult = self.getResult(s)
        self.setVolumeInfo()
        self.setSlider()
        self.plotData()

    def setResultList(self):
        self.currentResult = None
        self.resultQList.clear()
        self.resultQList.addItems(self.getResultNameList())

    def refresh(self):
        return

    def plotProfileDataButtonReleased(self):
        dlg = DialogPlotProfileDataOnResults(parent=self)
        if dlg.exec():
            self.dataAxis1 = dlg.dataAxis1
            self.dataAxis2 = dlg.dataAxis2
            self.profileName = dlg.profileName
            self.plotData()

    def exportButtonReleased(self):
        if self.currentResult == None:
            QMessageBox.critical(self, "Erreur : pas de fichier résultat sélectionné", "Veuillez choisir un fichier résultat dans la liste.")
            return
        dlg = DialogExportData(self)
        dlg.exec()

    def setVarLists(self):
        self.varList1.clear()
        self.varList2.clear()
        self.varList3.clear()

        # var list 1 : abssica or time
        self.varList1.addItem("x [m] \n(abscisse)")
        self.varList1.addItem("t [s] \n(temps)")
        self.varList1.setCurrentRow(0)

        # var list 2 : height data
        self.varList2.addItem("h [m]\n(hauteur d'eau)")
        self.varList2.addItem("h_c [m]\n(hauteur d'eau critique)")
        self.varList2.addItem("z [m]\n(altitude du fond)")
        self.varList2.addItem("z_min [m]\n(altitude minimale du fond)")
        self.varList2.addItem("z_0 [m]\n(altitude initiale du fond)")
        self.varList2.addItem("H [m]\n(charge)")
        # self.varList2.addItem("h_n [m]\n(hauteur d'eau normale)")

        # var list 3 : other data
        self.varList3.addItem("b [m]\n (largeur du fond)")
        self.varList3.addItem("z-z0 [m]\n (variation du fond)")

    def setVolumeInfo(self):
        if self.currentResult != None:
            vIn = self.currentResult["volume_in"]
            vOut = self.currentResult["volume_out"]
            vStored = self.currentResult["volume_stored"]
            self.volumeLabel.setText(f"Volume entrant : {vIn:.2f}m3\nVolume sortant : {vOut:.2f}m3\nVolume stocké : {vStored:.2f}m3\nSomme : {(vIn - vOut - vStored):.2f}m3\n")

    def setSlider(self):
        if self.currentResult == None:
            return
        if self.varList1.currentRow() == 0:
            self.slider.setMaximum(len(self.currentResult["time"])-1)
        elif self.varList1.currentRow() == 1:
            self.slider.setMaximum(len(self.currentResult["abscissa"])-1)
        # self.slider.setValue(self.slider.maximum())

    def varList1changed(self):
        self.setSlider()
        self.plotData()
        return

    def toggleFigure(self):
        if self.plotWidget.parent():
            # store the current index in the layout
            self.layoutIndex = self.plotLayout.indexOf(self.plotWidget)
            self.plotWidget.setParent(None)
            # manually reparenting a widget requires to explicitly show it,
            # usually by calling show() or setVisible(True), but this is
            # automatically done when calling showFullScreen()
            self.plotWidget.showFullScreen()
        else:
            self.plotLayout.insertWidget(self.layoutIndex, self.plotWidget)

    def rescale(self):
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.relim()
            twinAx.autoscale()
        self.sc.draw()
    
    def plotData(self):
        if self.currentResult == None:
            return
        
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.lines.clear()
            twinAx.collections.clear()
            if twinAx != a:
                twinAx.remove()
        a.set_prop_cycle(None)
        atLeastOneCurve = False
        lines = []
        xLabel = ""
        y1Label = ""
        y2Label = ""

        i = self.slider.value()
        if self.varList1.currentRow() == 0:
            self.sliderLabel.setText(f"time = {time_to_string(self.currentResult['time'][i], decimals=2)}")
            x = self.currentResult["abscissa"]
            couple = [(i, j) for j in range(len(x))]
            xLabel = "x [m]"
        elif self.varList1.currentRow() == 1:
            self.sliderLabel.setText(f"abscissa = {self.currentResult['abscissa'][i]:.2f}m")
            x = self.currentResult["time"]
            couple = [(j, i) for j in range(len(x))]
            xLabel = "t [s]"

        y1IndexList = ResultsTab.getIndexSelectedList(self.varList2)
        
        if 0 in y1IndexList:
            h = [self.currentResult["bottom_height"][c[0]][c[1]] + self.currentResult["water_depth"][c[0]][c[1]] for c in couple]
            label = "h (hauteur d'eau) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, h, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 1 in y1IndexList:
            hc  = [self.currentResult["bottom_height"][c[0]][c[1]] + self.currentResult["critical_depth"][c[0]][c[1]] for c in couple]
            label = "h_c (hauteur critique) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, hc, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 2 in y1IndexList:
            z  = [self.currentResult["bottom_height"][c[0]][c[1]] for c in couple]
            label = "z (altitude du fond) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, z, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if self.varList1.currentRow() == 0 and 0 in y1IndexList and 2 in y1IndexList:
            a.fill_between(x, z, h, color="cyan")
        if 3 in y1IndexList:
            zmin  = [self.currentResult["minimal_bottom_height"][c[1]] for c in couple]
            label = "z_min (altitude minimale) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, zmin, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 4 in y1IndexList:
            z0  = [self.currentResult["bottom_height"][0][c[1]] for c in couple]
            label = "z_0 (altitude initiale) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, z0, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 5 in y1IndexList:
            H  = [self.currentResult["energy"][c[0]][c[1]] for c in couple]
            label = "H (charge) [m]"
            atLeastOneCurve = True
            lines +=  a.plot(x, H, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        # if 6 in y1IndexList:
        #     y1  = [self.currentResult["bottom_height"][c[0]][c[1]] + self.currentResult["normal_depth"][c[0]][c[1]] for c in couple]
        #     label = "h_n (hauteur normale)"
        #     atLeastOneCurve = True
        #     lines +=  a.plot(x, y1, label=label)
        #     if y1Label != "":
        #         y1Label += " - " 
        #     y1Label += label
        for key, val in self.dataAxis1.items():
            lines +=  a.plot(val[0], val[1], label=key)
            if y1Label != "":
                y1Label += " - " 
            y1Label += " ".join(key.split())

        y2IndexList = ResultsTab.getIndexSelectedList(self.varList3)

        if y2IndexList != [] or self.dataAxis2:
            atLeastOneCurve = True
            twinAxeList = a.get_shared_x_axes().get_siblings(a)
            twinAxeList.pop(twinAxeList.index(a))
            if twinAxeList == []:
                twinAxe = a.twinx()
            else:
                twinAxe = twinAxeList[0]  

        if 0 in y2IndexList:
            y2 = [self.currentResult["width"][c[0]][c[1]] for c in couple]
            label = "b (largeur) [m]"
            lines +=  twinAxe.plot(x, y2, label=label, linestyle="dashed")
            if y2Label != "":
                y2Label += " - " 
            y2Label += label
        if 1 in y2IndexList:
            y2  = [self.currentResult["bottom_height"][c[0]][c[1]] - self.currentResult["bottom_height"][0][c[1]] for c in couple]
            label = "z-z0 (variation du fond) [m]"
            lines +=  twinAxe.plot(x, y2, label=label, linestyle="dashed")
            if y2Label != "":
                y2Label += " - " 
            y2Label += label

        for key, val in self.dataAxis2.items():
            lines +=  twinAxe.plot(val[0], val[1], label=key, linestyle="dashed")
            if y2Label != "":
                y2Label += " - " 
            y2Label += " ".join(key.split())


        a.set_xlabel(xLabel)
        a.set_ylabel(y1Label)
        if y2IndexList != []:
            twinAxe.set_ylabel(y2Label)

        if atLeastOneCurve: 
            a.legend(lines, [l.get_label() for l in lines])
        else:
            l = a.get_legend()
            if l != None: 
                l.remove()
        
        self.sc.draw()
        return

    def getIndexSelectedList(qlist):
        result = []
        for i in range(qlist.count()):
            if qlist.item(i).isSelected():
                result.append(i)
        return result

    def leavingCheck(self):
        saved = True
        notSavedList = []
        for r in self.resultList:
            if not(r["saved"]):
                saved = False
                notSavedList.append(r["name"]) 

        if not(saved):
            button = QMessageBox.question(self, "Résultats non enregistrées", f"Les résultats suivants ne sont pas enregistrés : {notSavedList}. Ils ne seront pas récupérables, souhaitez vous quitter ?")
            if button == QMessageBox.Yes:
                return True
            if button == QMessageBox.No:
                return False
        return True

