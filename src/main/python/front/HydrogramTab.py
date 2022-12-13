from PyQt5.QtWidgets import (
   QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTableView, QListWidgetItem, QHeaderView, QMessageBox, QMenu, QAction,
   QAbstractItemView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.TableModel import TableModel
from front.MplCanvas import MplCanvas, NavigationToolbar
from front.DialogNewHydrogram import DialogNewHydrogram
from front.DialogDelete import DialogDelete
from front.DialogQuestionAnswer import DialogQuestionAnswer
from utils import getAccumulatedVolume

import numpy as np

class HydrogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Hydrogramme", tabBar.getResource("images\\42699-water-wave-icon.png"))
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des hydrogrammes : "))
        self.hydrogramList = QListWidget()
        self.setHydrogramList()        
        self.hydrogramList.currentTextChanged.connect(self.hydrogramChoiceChanged)
        self.layoutList.addWidget(self.hydrogramList)
        self.hydrogramList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.hydrogramList.customContextMenuRequested.connect(self.contextMenuOnList)
       
        self.binWidget = QPushButton(" DELETE")
        self.binWidget.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.binWidget.released.connect(self.deleteButtonReleased)
        self.copyWidget = QPushButton(" COPY")
        self.copyWidget.setIcon(QIcon(self.getResource("images\\copy.png")))
        self.copyWidget.released.connect(self.copyButtonReleased)
        self.renameWidget = QPushButton(" RENAME")
        self.renameWidget.setIcon(QIcon(self.getResource("images\\rename.png")))
        self.renameWidget.released.connect(self.renameButtonReleased)
        self.editWidget = QPushButton(" EDIT")
        self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editWidget.released.connect(self.editButtonReleased)
        self.propertiesWidget = QPushButton(" PROPERTIES")
        self.propertiesWidget.setIcon(QIcon(self.getResource("images\\properties.png")))
        self.propertiesWidget.released.connect(self.propertiesButtonReleased)
        self.editing = False
        self.newHydrogramButton = QPushButton(" NEW")
        self.newHydrogramButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newHydrogramButton.released.connect(self.newHydrogramButtonReleased)
        self.layoutList.addWidget(self.newHydrogramButton)
        self.layoutList.addWidget(self.renameWidget)
        self.layoutList.addWidget(self.editWidget)
        self.layoutList.addWidget(self.copyWidget)
        self.layoutList.addWidget(self.binWidget)
        self.layoutList.addWidget(self.propertiesWidget)

        self.hydrogramData = QTableView()
        self.hydrogramData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.hydrogramData.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.hydrogramData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hydrogramData.setHorizontalHeader(header)
        self.layoutData = QVBoxLayout()
        self.layoutData.addWidget(self.hydrogramData, alignment=Qt.AlignHCenter)
        self.displayHydrogramData()

        self.layoutPlot = QVBoxLayout()
        self.plotLabel = QLabel()
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
        item = self.hydrogramList.itemAt(pos)
        if item != None:
            self.getProject().setHydrogramSelected(item.text())
            rename = QAction("Renommer", self.hydrogramList)
            edit = QAction("Editer", self.hydrogramList)
            copy = QAction("Copier", self.hydrogramList)
            delete = QAction("Supprimer", self.hydrogramList)
            properties = QAction("Propriétés", self.hydrogramList)
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
            newHydrogram = QAction("Nouveau hydrogramme", self.hydrogramList)
            newHydrogram.triggered.connect(self.newHydrogramButtonReleased)
            context.addAction(newHydrogram)
        context.exec(self.hydrogramList.mapToGlobal(pos))


    def contextMenuOnTable(self, pos):
        context = QMenu(self)
        copy = QAction("Copier", self.hydrogramData)
        copy.triggered.connect(self.model.copy)
        context.addAction(copy)
        if self.editing:
            paste = QAction("Coller", self.hydrogramData)
            addUpperLine = QAction("Insérer une ligne au-dessus", self.hydrogramData)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.hydrogramData)
            deleteLine = QAction("Supprimer cette ligne", self.hydrogramData)
            paste.triggered.connect(self.model.paste(self.hydrogramData.indexAt(pos)))
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.hydrogramData.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.hydrogramData.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.hydrogramData.indexAt(pos)))
            context.addAction(paste)
            context.addAction(addUpperLine)
            context.addAction(addLowerLine)
            context.addAction(deleteLine)
        context.exec(self.hydrogramData.mapToGlobal(pos))

    def newHydrogramButtonReleased(self):
        dlg = DialogNewHydrogram(parent=self)
        if dlg.exec():
            newHydogram = dlg.hydrogram
            self.getProject().addHydrogram(newHydogram)
            self.getProject().setHydrogramSelected(newHydogram.name)
            item = QListWidgetItem(newHydogram.name)
            self.hydrogramList.addItem(item)
            self.hydrogramList.setCurrentItem(item)
        return

    def editButtonReleased(self):
        h = self.getProject().hydrogramSelected
        m = self.model
        if h == None or m == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                m.restore()
            else:
                self.getProject().needToBeSaved = True
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" EDIT")
            self.hydrogramList.setEnabled(True)
            self.newHydrogramButton.setEnabled(True)
            self.copyWidget.setEnabled(True)
            self.binWidget.setEnabled(True)
            self.renameWidget.setEnabled(True)
            self.propertiesWidget.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" STOP EDITING")
            self.hydrogramList.setEnabled(False)
            self.newHydrogramButton.setEnabled(False)
            self.copyWidget.setEnabled(False)
            self.binWidget.setEnabled(False)
            self.renameWidget.setEnabled(False)
            self.propertiesWidget.setEnabled(False)
            self.disableOtherTabs()
        self.editing = not(self.editing)
        m.changeEditionMode()
        return

    def renameButtonReleased(self):
        h = self.getProject().hydrogramSelected
        if h == None:
            return
        dlg = DialogQuestionAnswer(self, f"Choississez un nouveau nom pour l'hydrogramme {h.name}")
        if dlg.exec():
            newName = dlg.answer
            if newName.split() == []:
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est invalide")
                return
            if newName == h.name:
                QMessageBox.information(self, "Nom identique", "Le nom est inchangé")
                return
            if newName in self.getProject().getHydrogramNameList():
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est déjà pris par un autre hydrogramme")
                return
            h.name = newName
            self.setHydrogramList()
        return

    def deleteButtonReleased(self):
        h = self.getProject().hydrogramSelected
        if h == None:
            return
        dlg = DialogDelete(h.name, parent=self)
        if dlg.exec():
            self.getProject().deleteHydrogram(h)
            self.hydrogramList.takeItem(self.hydrogramList.currentRow())
        return

    def copyButtonReleased(self):
        h = self.getProject().hydrogramSelected
        if h == None:
            return
        newName = h.name + " (1)"
        i = 1
        while newName in self.getProject().getHydrogramNameList():
            i += 1
            newName = h.name + f" ({i})"
        hCopy = h.copy(newName)
        self.getProject().addHydrogram(hCopy)
        item = QListWidgetItem(hCopy.name)
        self.hydrogramList.addItem(item)
        return

    def propertiesButtonReleased(self):
        h = self.getProject().hydrogramSelected
        if h == None:
            return
        QMessageBox.information(self, f"propriétés de {h.name}", h.properties)

    def hydrogramChoiceChanged(self, name):
        self.getProject().setHydrogramSelected(name)
        self.displayHydrogramData()
        self.plotData()
        return

    def displayHydrogramData(self):
        if self.getProject().hydrogramSelected == None:
            self.model = None
            self.hydrogramData.setModel(None)
        else:
            self.model = TableModel(self, self.getProject().hydrogramSelected)
            self.hydrogramData.setModel(self.model)

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

        if self.getProject().hydrogramSelected == None:
            self.sc.draw()
            return
        else:
            df = self.getProject().hydrogramSelected.data

        subdf = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[1]].isnull())]
        timeInHour = np.array(subdf[subdf.columns[0]])/3600
        lines += a.plot(timeInHour, subdf[subdf.columns[1]], label="Débit [m3/s]", color="blue")
        a.set_xlabel("t [h]")
        a.set_ylabel(subdf.columns[1])
        a.relim()
        a.autoscale()

        twinAx = a.twinx()
        vAccumulated = getAccumulatedVolume(subdf[subdf.columns[0]], subdf[subdf.columns[1]])
        lines += twinAx.plot(timeInHour, vAccumulated, label="Volume cumulé [m3]", color="blue", linestyle="dashdot")
        twinAx.set_ylabel("Volume cumulé (m3)")

        if len(vAccumulated) > 0:
            self.plotLabel.setText(f"Volume liquide cumulé : {vAccumulated[-1]:.3f}m3")
        a.legend(lines, [l.get_label() for l in lines])
        self.sc.draw()
        return
        
    def setHydrogramList(self):
        hSelected = self.getProject().hydrogramSelected
        self.hydrogramList.clear()
        for h in self.getProject().hydrogramList:
            self.hydrogramList.addItem(h.name)
            if h == hSelected:
                self.hydrogramList.setCurrentRow(self.hydrogramList.count()-1)
        return

    def refresh(self):
        self.setHydrogramList()
        self.displayHydrogramData()
        self.plotData()
        return
