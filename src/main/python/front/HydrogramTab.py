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

class HydrogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Hydrogramme", tabBar.getResource("images\\42699-water-wave-icon.png"))
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des hydrogrammes : "))
        self.hydrogramList = QListWidget()
        self.setHydrogramList()        
        self.hydrogramList.currentTextChanged.connect(self.hydrogramChoiceChanged)
        self.layoutList.addWidget(self.hydrogramList)
       
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
        self.newHydrogramButton = QPushButton(" NEW")
        self.newHydrogramButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newHydrogramButton.released.connect(self.newHydrogramButtonReleased)
        self.layoutList.addWidget(self.newHydrogramButton)
        self.layoutList.addWidget(self.editWidget)
        self.layoutList.addWidget(self.copyWidget)
        self.layoutList.addWidget(self.binWidget)

        self.hydrogramData = QTableView()
        self.hydrogramData.setContextMenuPolicy(Qt.CustomContextMenu)
        self.hydrogramData.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.hydrogramData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hydrogramData.setHorizontalHeader(header)
        self.layoutData = QVBoxLayout()
        self.layoutData.addWidget(self.hydrogramData, alignment=Qt.AlignHCenter)
        self.displayHydrogramData()

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
            addUpperLine = QAction("Insérer une ligne au-dessus", self.hydrogramData)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.hydrogramData)
            deleteLine = QAction("Supprimer cette ligne", self.hydrogramData)
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.hydrogramData.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.hydrogramData.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.hydrogramData.indexAt(pos)))
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
        if h == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                self.model.restore()
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" EDIT")
            self.hydrogramList.setSelectionMode(QAbstractItemView.SingleSelection)
            self.newHydrogramButton.setEnabled(True)
            self.copyWidget.setEnabled(True)
            self.binWidget.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editWidget.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editWidget.setText(" STOP EDITING")
            self.hydrogramList.setSelectionMode(QAbstractItemView.NoSelection)
            self.newHydrogramButton.setEnabled(False)
            self.copyWidget.setEnabled(False)
            self.binWidget.setEnabled(False)
            self.disableOtherTabs()
        self.editing = not(self.editing)
        self.model.changeEditionMode()
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
        self.getProject().setHydrogramSelected(hCopy.name)
        item = QListWidgetItem(hCopy.name)
        self.hydrogramList.addItem(item)
        self.hydrogramList.setCurrentItem(item)
        return

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
        if self.getProject().hydrogramSelected == None:
            return
        else:
            df = self.getProject().hydrogramSelected.data
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

    def makeHydrogramListEmpty(self):
        for i in range(self.hydrogramList.count()-1, -1, -1):
            self.hydrogramList.takeItem(i)
        return
        
    def setHydrogramList(self):
        self.makeHydrogramListEmpty()
        for i, h in enumerate(self.getProject().hydrogramList):
            item = QListWidgetItem(h.name)
            item.setSelected(i == self.getProject().hydrogramSelectedIndex)
            self.hydrogramList.addItem(item)
        return

    def refresh(self):
        self.setHydrogramList()
        return
