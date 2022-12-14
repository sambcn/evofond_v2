from PyQt5.QtWidgets import (
   QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTableView, QListWidgetItem, QHeaderView, QMessageBox, QMenu, QAction,
   QCheckBox, QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.TableModel import TableModel
from front.MplCanvas import MplCanvas, NavigationToolbar
from front.DialogNewSedimentogram import DialogNewSedimentogram
from front.DialogDelete import DialogDelete
from front.DialogQuestionAnswer import DialogQuestionAnswer
from utils import getAccumulatedVolume

import numpy as np
import pandas as pd

class SedimentogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Sédimentogramme", tabBar.getResource("images\\stone.png"))
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des sédimentogrammes : "))
        self.sedimentogramList = QListWidget()
        self.setSedimentogramList()        
        self.sedimentogramList.currentTextChanged.connect(self.sedimentogramChoiceChanged)
        self.layoutList.addWidget(self.sedimentogramList)
        self.sedimentogramList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sedimentogramList.customContextMenuRequested.connect(self.contextMenuOnList)
       
        self.binWidget = QPushButton(" DELETE")
        self.binWidget.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.binWidget.released.connect(self.deleteButtonReleased)
        self.copyWidget = QPushButton(" COPY")
        self.copyWidget.setIcon(QIcon(self.getResource("images\\copy.png")))
        self.copyWidget.released.connect(self.copyButtonReleased)
        self.editWidget = QPushButton(" EDIT")
        self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editWidget.released.connect(self.editButtonReleased)
        self.renameWidget = QPushButton(" RENAME")
        self.renameWidget.setIcon(QIcon(self.getResource("images\\rename.png")))
        self.renameWidget.released.connect(self.renameButtonReleased)
        self.propertiesWidget = QPushButton(" PROPERTIES")
        self.propertiesWidget.setIcon(QIcon(self.getResource("images\\properties.png")))
        self.propertiesWidget.released.connect(self.propertiesButtonReleased)
        self.editing = False
        self.newSedimentogramButton = QPushButton(" NEW")
        self.newSedimentogramButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newSedimentogramButton.released.connect(self.newSedimentogramButtonReleased)
        self.layoutList.addWidget(self.newSedimentogramButton)
        self.layoutList.addWidget(self.renameWidget)
        self.layoutList.addWidget(self.editWidget)
        self.layoutList.addWidget(self.copyWidget)
        self.layoutList.addWidget(self.binWidget)
        self.layoutList.addWidget(self.propertiesWidget)

        self.sedimentogramData = QTableView()
        self.sedimentogramData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sedimentogramData.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.sedimentogramData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sedimentogramData.setHorizontalHeader(header)
        self.layoutData = QVBoxLayout()
        self.layoutData.addWidget(self.sedimentogramData, alignment=Qt.AlignHCenter)
        self.displayData()

        self.layoutPlot = QVBoxLayout()
        self.plotHydrogramDataCheckbox = QCheckBox(" Afficher les données hydrauliques")
        self.plotHydrogramDataCheckbox.stateChanged.connect(self.plotHydrogramDataCheckboxChecked)
        self.hydrogramList = QComboBox()
        self.hydrogramList.currentTextChanged.connect(self.plotData)
        self.setHydrogramList()
        self.plotLabel = QLabel()
        self.plotLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layoutPlot.addWidget(self.plotHydrogramDataCheckbox, alignment=Qt.AlignTop)
        self.layoutPlot.addWidget(self.hydrogramList, alignment=Qt.AlignTop)
        self.layoutPlot.addWidget(self.plotLabel, alignment=Qt.AlignTop)
        self.sc = MplCanvas()
        self.layoutPlot.addWidget(self.sc, stretch=100)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.layoutPlot.addWidget(self.toolbar)
        self.plotData()

        layoutInter = QHBoxLayout()
        layoutInter.addLayout(self.layoutList)
        layoutInter.addLayout(self.layoutData)
        self.layout.addLayout(layoutInter)
        self.layout.addLayout(self.layoutPlot)

    def contextMenuOnList(self, pos):
        context = QMenu(self)
        item = self.sedimentogramList.itemAt(pos)
        if item != None:
            self.getProject().setSedimentogramSelected(item.text())
            rename = QAction("Renommer", self.sedimentogramList)
            edit = QAction("Editer", self.sedimentogramList)
            copy = QAction("Copier", self.sedimentogramList)
            delete = QAction("Supprimer", self.sedimentogramList)
            properties = QAction("Propriétés", self.sedimentogramList)
            rename.triggered.connect(self.renameButtonReleased)
            edit.triggered.connect(self.editButtonReleased)
            copy.triggered.connect(self.copyButtonReleased)
            delete.triggered.connect(self.deleteButtonReleased)
            properties.triggered.connect(self.propertiesButtonReleased)
            context.addAction(rename)
            context.addAction(edit)
            context.addAction(copy)
            context.addAction(delete)
            context.addAction(properties)
        else:
            newSedimentogram = QAction("Nouveau sédimentogramme", self.sedimentogramList)
            newSedimentogram.triggered.connect(self.newSedimentogramButtonReleased)
            context.addAction(newSedimentogram)
        context.exec(self.sedimentogramList.mapToGlobal(pos))
    
    def contextMenuOnTable(self, pos):
        context = QMenu(self)
        copy = QAction("Copier", self.table)
        copy.triggered.connect(self.model.copy)
        context.addAction(copy)
        if self.editing:
            paste = QAction("Coller", self.sedimentogramData)
            addUpperLine = QAction("Insérer une ligne au-dessus", self.sedimentogramData)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.sedimentogramData)
            deleteLine = QAction("Supprimer cette ligne", self.sedimentogramData)
            paste.triggered.connect(self.model.paste(self.sedimentogramData.indexAt(pos)))
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.sedimentogramData.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.sedimentogramData.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.sedimentogramData.indexAt(pos)))
            context.addAction(paste)
            context.addAction(addUpperLine)
            context.addAction(addLowerLine)
            context.addAction(deleteLine)
        context.exec(self.sedimentogramData.mapToGlobal(pos))

    def newSedimentogramButtonReleased(self):
        dlg = DialogNewSedimentogram(parent=self)
        if dlg.exec():
            newSedimentogram = dlg.sedimentogram
            self.getProject().addSedimentogram(newSedimentogram)
            self.getProject().setSedimentogramSelected(newSedimentogram.name)
            item = QListWidgetItem(newSedimentogram.name)
            self.sedimentogramList.addItem(item)
            self.sedimentogramList.setCurrentItem(item)
        return

    def renameButtonReleased(self):
        s = self.getProject().sedimentogramSelected
        if s == None:
            return
        dlg = DialogQuestionAnswer(self, f"Choississez un nouveau nom pour l'hydrogramme {s.name}")
        if dlg.exec():
            newName = dlg.answer
            if newName.split() == []:
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est invalide")
                return
            if newName == s.name:
                QMessageBox.information(self, "Nom identique", "Le nom est inchangé")
                return
            if newName in self.getProject().getSedimentogramNameList():
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est déjà pris par un autre sédimentogramme")
                return
            s.name = newName
            self.setSedimentogramList()
        return

    def editButtonReleased(self):
        h = self.getProject().sedimentogramSelected
        if h == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                self.model.restore()
            else:
                self.getProject().needToBeSaved = True
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" EDIT")
            self.sedimentogramList.setEnabled(True)
            self.newSedimentogramButton.setEnabled(True)
            self.copyWidget.setEnabled(True)
            self.binWidget.setEnabled(True)
            self.renameWidget.setEnabled(True)
            self.propertiesWidget.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" STOP EDITING")
            self.sedimentogramList.setEnabled(False)
            self.newSedimentogramButton.setEnabled(False)
            self.copyWidget.setEnabled(False)
            self.binWidget.setEnabled(False)
            self.renameWidget.setEnabled(False)
            self.propertiesWidget.setEnabled(False)
            self.disableOtherTabs()
        self.editing = not(self.editing)
        self.model.changeEditionMode()
        return

    def deleteButtonReleased(self):
        s = self.getProject().sedimentogramSelected
        if s == None:
            return
        dlg = DialogDelete(s.name, parent=self)
        if dlg.exec():
            self.getProject().deleteSedimentogram(s)
            self.sedimentogramList.takeItem(self.sedimentogramList.currentRow())
        return

    def copyButtonReleased(self):
        s = self.getProject().sedimentogramSelected
        if s == None:
            return
        newName = s.name + " (1)"
        i = 1
        while newName in self.getProject().getSedimentogramNameList():
            i += 1
            newName = s.name + f" ({i})"
        sCopy = s.copy(newName)
        self.getProject().addSedimentogram(sCopy)
        item = QListWidgetItem(sCopy.name)
        self.sedimentogramList.addItem(item)
        return

    def propertiesButtonReleased(self):
        s = self.getProject().sedimentogramSelected
        if s == None:
            return
        QMessageBox.information(self, f"propriétés de {s.name}", s.properties)

    def sedimentogramChoiceChanged(self, name):
        self.getProject().setSedimentogramSelected(name)
        self.displayData()
        self.plotData()
        return

    def plotHydrogramDataCheckboxChecked(self):
        if self.plotHydrogramDataCheckbox.isChecked():
            self.hydrogramList.setEnabled(True)
        else:
            self.hydrogramList.setEnabled(False)
        self.plotData()

    def displayData(self):
        if self.getProject().sedimentogramSelected == None:
            self.model = None
            self.sedimentogramData.setModel(None)
        else:
            self.model = TableModel(self, self.getProject().sedimentogramSelected)
            self.sedimentogramData.setModel(self.model)

    def plotData(self):
        self.plotLabel.setText("")
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.lines.clear()
            twinAx.collections.clear()
            l = twinAx.get_legend()
            if l != None: 
                l.remove()
            if twinAx != a:
                twinAx.remove()
        a.set_prop_cycle(None)
        lines = []

        if self.getProject().sedimentogramSelected == None:
            self.sc.draw()
            return
        else:
            df = self.getProject().sedimentogramSelected.data

        subdf = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[1]].isnull())]
        timeInHour = np.array(subdf[subdf.columns[0]])/3600
        lines += a.plot(timeInHour, subdf[subdf.columns[1]], label="Débit [m3/s]", color="orange")
        a.set_xlabel("t [h]")
        a.set_ylabel(subdf.columns[1])
        a.relim()
        a.autoscale()

        twinAx = a.twinx()
        vAccumulated = getAccumulatedVolume(subdf[subdf.columns[0]], subdf[subdf.columns[1]])
        hydroName = self.hydrogramList.currentText()
        hydroExists = hydroName in self.getProject().getHydrogramNameList()
        if hydroExists:
            dfHydro = self.getProject().getHydrogram(hydroName).data 
            subdfHydro = dfHydro[~(dfHydro[dfHydro.columns[0]].isnull()) & ~(dfHydro[dfHydro.columns[1]].isnull())]
            timeInHourHydro = np.array(subdfHydro[subdfHydro.columns[0]])/3600
            vWaterAccumulated = getAccumulatedVolume(subdfHydro[subdfHydro.columns[0]], subdfHydro[subdfHydro.columns[1]])
        
        if self.plotHydrogramDataCheckbox.isChecked() and hydroExists:
            lines += twinAx.plot(timeInHourHydro, subdfHydro[subdfHydro.columns[1]], label="Débit liquide [m3/s]", color="blue", linestyle="dashed")
            twinAx.set_ylabel(subdfHydro.columns[1])
        else:
            lines += twinAx.plot(timeInHour, vAccumulated, label="Volume cumulé [m3]", color="orange", linestyle="dashdot")
            twinAx.set_ylabel("Volume cumulé [m3]")
        
        if len(vAccumulated) > 0 and hydroExists and len(vWaterAccumulated) > 0 :
            self.plotLabel.setText(f"Volume solide cumulé : {vAccumulated[-1]:.3f}m3\nVolume liquide cumulé : {vWaterAccumulated[-1]:.3f}m3\nConcentration volumique (m3/m3) : {vAccumulated[-1]/vWaterAccumulated[-1]:.3f}")
        a.legend(lines, [l.get_label() for l in lines])
        self.sc.draw()
        return
        
    def setSedimentogramList(self):
        sSelected = self.getProject().sedimentogramSelected
        self.sedimentogramList.clear()
        for i, s in enumerate(self.getProject().sedimentogramList):
            self.sedimentogramList.addItem(s.name)
            if s == sSelected:
                self.sedimentogramList.setCurrentRow(i)
        return

    def setHydrogramList(self):
        self.hydrogramList.setEnabled(self.plotHydrogramDataCheckbox.isChecked())
        self.hydrogramList.clear()
        self.hydrogramList.addItems(self.getProject().getHydrogramNameList())

    def refresh(self):
        self.setHydrogramList()
        self.setSedimentogramList()
        return
