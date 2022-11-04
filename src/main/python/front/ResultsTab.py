from ctypes import alignment
from PyQt5.QtWidgets import (
    QPushButton, QListWidget, QVBoxLayout, QComboBox, QLabel, QListWidgetItem, QAbstractItemView, QGridLayout, QSlider, QWidget, QHBoxLayout,
    QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.MplCanvas import MplCanvas, NavigationToolbar
from frontToBack import simulateModel
from front.DialogNewSimulation import DialogNewSimulation
from front.DialogExportData import DialogExportData

class ResultsTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Résultats", tabBar.getResource("images\\results.png"))

        self.listLayout = QVBoxLayout()
        self.resultList = QListWidget()
        self.listLayout.addWidget(self.resultList)
        self.resultList.currentTextChanged.connect(self.resultChoiceChanged)
        self.setResultList()

        self.deleteResultButton = QPushButton(" DELETE")
        self.deleteResultButton.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.deleteResultButton.released.connect(self.deleteResultButtonReleased)
        self.listLayout.addWidget(self.deleteResultButton)

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

        self.exportButton = QPushButton(" Exporter les données")
        self.exportButton.setIcon(QIcon(self.getResource("images\\export.png")))
        self.exportButton.released.connect(self.exportButtonReleased)
        self.paramLayout.addWidget(self.exportButton)

        self.plotLayout = QVBoxLayout()
        self.rescaleButton =QPushButton(" Réinitialiser l'échelle")
        self.rescaleButton.setIcon(QIcon(self.getResource("images\\refresh.png")))
        self.rescaleButton.released.connect(self.rescale)
        self.plotLayout.addWidget(self.rescaleButton)
        self.sc = MplCanvas()
        self.plotLayout.addWidget(self.sc, stretch=100)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotData()

        self.layout.addLayout(self.listLayout)
        self.layout.addLayout(self.paramLayout)
        self.layout.addLayout(self.plotLayout, stretch=100)
        
    def newSimulation(self):
        dlg = DialogNewSimulation(parent=self)
        dlg.show()
        self.newSimulationButton.setEnabled(False)

    def deleteResultButtonReleased(self):
        self.getProject().deleteResult(self.resultList.currentItem().text())
        self.resultList.takeItem(self.resultList.currentRow())
        self.currentResult = self.getProject().getResult(s)

    def resultChoiceChanged(self, s):
        self.currentResult = self.getProject().getResult(s)
        self.setSlider()

    def setResultList(self):
        self.currentResult = None
        self.resultList.clear()
        self.resultList.addItems(self.getProject().getResultNameList())

    def refresh(self):
        self.setResultList()

    def exportButtonReleased(self):
        if self.currentResult == None:
            QMessageBox.critical(self, "Erreur : pas de fichier résultat sélectionné", "Veuillez choisir un fichier résultat dans la liste.")
            return
        dlg = DialogExportData(self)
        if dlg.exec():
            pass

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

    def setSlider(self):
        if self.currentResult == None:
            return
        if self.varList1.currentRow() == 0:
            self.slider.setMaximum(len(self.currentResult["time"])-1)
        elif self.varList1.currentRow() == 1:
            self.slider.setMaximum(len(self.currentResult["abscissa"])-1)
        self.slider.setValue(self.slider.maximum())

    def varList1changed(self):
        self.setSlider()
        self.plotData()
        return

    def rescale(self):
        a = self.sc.axes
        a.relim()
        a.autoscale()
        self.sc.draw()
    
    def plotData(self):

        if self.currentResult == None:
            return
        
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.lines.clear()
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
            self.sliderLabel.setText(f"time = {self.currentResult['time'][i]:.3f}s")
            x = self.currentResult["abscissa"]
            couple = [(i, j) for j in range(len(x))]
            xLabel = "x (m)"
        elif self.varList1.currentRow() == 1:
            self.sliderLabel.setText(f"abscissa = {self.currentResult['abscissa'][i]:.3f}m")
            x = self.currentResult["time"]
            couple = [(j, i) for j in range(len(x))]
            xLabel = "t (s)"

        y1IndexList = ResultsTab.getIndexSelectedList(self.varList2)
        
        if 0 in y1IndexList:
            h = [self.currentResult["bottom_height"][c[0]][c[1]] + self.currentResult["water_depth"][c[0]][c[1]] for c in couple]
            label = "h (hauteur d'eau)"
            atLeastOneCurve = True
            lines +=  a.plot(x, h, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 1 in y1IndexList:
            hc  = [self.currentResult["bottom_height"][c[0]][c[1]] + self.currentResult["critical_depth"][c[0]][c[1]] for c in couple]
            label = "h_c (hauteur critique)"
            atLeastOneCurve = True
            lines +=  a.plot(x, hc, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 2 in y1IndexList:
            z  = [self.currentResult["bottom_height"][c[0]][c[1]] for c in couple]
            label = "z (altitude du fond)"
            atLeastOneCurve = True
            lines +=  a.plot(x, z, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 0 in y1IndexList and 2 in y1IndexList:
            a.fill_between(x, z, h, color="cyan")
        if 3 in y1IndexList:
            zmin  = [self.currentResult["minimal_bottom_height"][c[1]] for c in couple]
            label = "z_min (altitude minimale)"
            atLeastOneCurve = True
            lines +=  a.plot(x, zmin, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 4 in y1IndexList:
            z0  = [self.currentResult["bottom_height"][0][c[1]] for c in couple]
            label = "z_0 (altitude initiale)"
            atLeastOneCurve = True
            lines +=  a.plot(x, z0, label=label)
            if y1Label != "":
                y1Label += " - " 
            y1Label += label
        if 5 in y1IndexList:
            H  = [self.currentResult["energy"][c[0]][c[1]] for c in couple]
            label = "H (charge)"
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

        y2IndexList = ResultsTab.getIndexSelectedList(self.varList3)

        if y2IndexList != []:
            atLeastOneCurve = True
            twinAxeList = a.get_shared_x_axes().get_siblings(a)
            twinAxeList.pop(twinAxeList.index(a))
            if twinAxeList == []:
                twinAxe = a.twinx()
            else:
                twinAxe = twinAxeList[0]  

        if 0 in y2IndexList:
            y2 = [self.currentResult["width"][c[0]][c[1]] for c in couple]
            label = "b (largeur)"
            lines +=  twinAxe.plot(x, y2, label=label, linestyle="dashed")
            if y2Label != "":
                y2Label += " - " 
            y2Label += label
        if 1 in y2IndexList:
            y2  = [self.currentResult["bottom_height"][c[0]][c[1]] - self.currentResult["bottom_height"][0][c[1]] for c in couple]
            label = "z-z0 (variation du fond)"
            lines +=  twinAxe.plot(x, y2, label=label, linestyle="dashed")
            if y2Label != "":
                y2Label += " - " 
            y2Label += label

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


