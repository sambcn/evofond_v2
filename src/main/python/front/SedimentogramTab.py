from PyQt5.QtWidgets import (
   QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QTableView, QListWidgetItem, QHeaderView, QMessageBox, QMenu, QAction,
   QAbstractItemView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.TableModel import TableModel
from front.MplCanvas import MplCanvas, NavigationToolbar
from front.DialogNewSedimentogram import DialogNewSedimentogram
from front.DialogDelete import DialogDelete

class SedimentogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Sédimentogramme", tabBar.getResource("images\\stone.png"))
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des sédimentogrammes : "))
        self.sedimentogramList = QListWidget()
        self.setSedimentogramList()        
        self.sedimentogramList.currentTextChanged.connect(self.sedimentogramChoiceChanged)
        self.layoutList.addWidget(self.sedimentogramList)
       
        self.binWidget = QPushButton(" DELETE")
        self.binWidget.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.binWidget.released.connect(self.deleteButtonReleased)
        self.copyWidget = QPushButton(" COPY")
        self.copyWidget.setIcon(QIcon(self.getResource("images\\copy.png")))
        self.copyWidget.released.connect(self.copyButtonReleased)
        self.editWidget = QPushButton(" EDIT")
        self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editWidget.released.connect(self.editButtonReleased)
        self.editing = False
        self.newSedimentogramButton = QPushButton(" NEW")
        self.newSedimentogramButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newSedimentogramButton.released.connect(self.newSedimentogramButtonReleased)
        self.layoutList.addWidget(self.newSedimentogramButton)
        self.layoutList.addWidget(self.editWidget)
        self.layoutList.addWidget(self.copyWidget)
        self.layoutList.addWidget(self.binWidget)

        self.sedimentogramData = QTableView()
        self.sedimentogramData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sedimentogramData.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.sedimentogramData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sedimentogramData.setHorizontalHeader(header)
        self.layoutData = QVBoxLayout()
        self.layoutData.addWidget(self.sedimentogramData, alignment=Qt.AlignHCenter)
        self.displayData()

        self.layoutPlot = QVBoxLayout()
        self.sc = MplCanvas()
        self.layoutPlot.addWidget(self.sc)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.layoutPlot.addWidget(self.toolbar)
        self.plotData()

        layoutInter = QHBoxLayout()
        layoutInter.addLayout(self.layoutList)
        layoutInter.addLayout(self.layoutData)
        self.layout.addLayout(layoutInter)
        self.layout.addLayout(self.layoutPlot)
    
    def contextMenuOnTable(self, pos):
        context = QMenu(self)
        if self.editing:
            addUpperLine = QAction("Insérer une ligne au-dessus", self.sedimentogramData)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.sedimentogramData)
            deleteLine = QAction("Supprimer cette ligne", self.sedimentogramData)
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.sedimentogramData.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.sedimentogramData.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.sedimentogramData.indexAt(pos)))
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

    def editButtonReleased(self):
        h = self.getProject().sedimentogramSelected
        if h == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                self.model.restore()
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" EDIT")
            self.sedimentogramList.setSelectionMode(QAbstractItemView.SingleSelection)
            self.newSedimentogramButton.setEnabled(True)
            self.copyWidget.setEnabled(True)
            self.binWidget.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" STOP EDITING")
            self.sedimentogramList.setSelectionMode(QAbstractItemView.NoSelection)
            self.newSedimentogramButton.setEnabled(False)
            self.copyWidget.setEnabled(False)
            self.binWidget.setEnabled(False)
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
        self.getProject().setSedimentogramSelected(sCopy.name)
        item = QListWidgetItem(sCopy.name)
        self.sedimentogramList.addItem(item)
        self.sedimentogramList.setCurrentItem(item)
        return

    def sedimentogramChoiceChanged(self, name):
        self.getProject().setSedimentogramSelected(name)
        self.displayData()
        self.plotData()
        return

    def displayData(self):
        if self.getProject().sedimentogramSelected == None:
            self.model = None
            self.sedimentogramData.setModel(None)
        else:
            self.model = TableModel(self, self.getProject().sedimentogramSelected)
            self.sedimentogramData.setModel(self.model)

    def plotData(self):
        if self.getProject().sedimentogramSelected == None:
            return
        else:
            df = self.getProject().sedimentogramSelected.data
        self.sc.axes.lines.clear()
        self.sc.axes.set_prop_cycle(None)
        subdf = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[1]].isnull())]
        self.sc.axes.plot(subdf[subdf.columns[0]], subdf[subdf.columns[1]])
        self.sc.axes.set_xlabel(subdf.columns[0])
        self.sc.axes.set_ylabel(subdf.columns[1])
        self.sc.axes.relim()
        self.sc.axes.autoscale()
        self.sc.draw()
        return

    def makeSedimentogramListEmpty(self):
        for i in range(self.sedimentogramList.count()-1, -1, -1):
            self.sedimentogramList.takeItem(i)
        return
        
    def setSedimentogramList(self):
        self.makeSedimentogramListEmpty()
        for i, s in enumerate(self.getProject().sedimentogramList):
            item = QListWidgetItem(s.name)
            item.setSelected(i == self.getProject().sedimentogramSelectedIndex)
            self.sedimentogramList.addItem(item)
        return

    def refresh(self):
        self.setSedimentogramList()
        return
