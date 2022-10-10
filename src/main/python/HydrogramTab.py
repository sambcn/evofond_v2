from multiprocessing.sharedctypes import Value
from Hydrogram import Hydrogram
from Tab import Tab
from PyQt5.QtWidgets import (
   QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QDialog, QTableView, QListWidgetItem, QHeaderView 
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from HydrogramTableModel import HydrogramTableModel
from MplCanvas import MplCanvas, NavigationToolbar
from DialogNewHydrogram import DialogNewHydrogram
from DialogDelete import DialogDelete

class HydrogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Hydrogramme", ".\\src\\main\\icons\\base\\42699-water-wave-icon.png")
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des hydrogrammes : "))
        self.hydrogramList = QListWidget()
        self.setHydrogramList()        
        self.hydrogramList.currentTextChanged.connect(self.hydrogramChoiceChanged)
        self.layoutList.addWidget(self.hydrogramList)
       

        binWidget = QPushButton(" DELETE")
        binWidget.setIcon(QIcon(".\\src\\main\\icons\\base\\trash.png"))
        binWidget.released.connect(self.deleteButtonReleased)
        copyWidget = QPushButton(" COPY")
        copyWidget.setIcon(QIcon(".\\src\\main\\icons\\base\\copy.png"))
        copyWidget.released.connect(self.copyButtonReleased)
        editWidget = QPushButton(" EDIT")
        editWidget.setIcon(QIcon(".\\src\\main\\icons\\base\\edit.png"))
        newHydrogramButton = QPushButton(" NEW")
        newHydrogramButton.setIcon(QIcon(".\\src\\main\\icons\\base\\add.png"))
        newHydrogramButton.released.connect(self.newHydrogramButtonReleased)
        self.layoutList.addWidget(newHydrogramButton)
        self.layoutActions = QHBoxLayout()
        self.layoutActions.addWidget(editWidget)
        self.layoutActions.addWidget(copyWidget)
        self.layoutActions.addWidget(binWidget)
        self.layoutList.addLayout(self.layoutActions)

        self.hydrogramData = QTableView()
        header = self.hydrogramData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hydrogramData.setHorizontalHeader(header)
        self.layoutData = QVBoxLayout()
        self.layoutData.addWidget(self.hydrogramData, alignment=Qt.AlignHCenter)
        self.displayHydrogramData()

        self.layoutPlot = QVBoxLayout()
        self.sc = MplCanvas()
        self.layoutPlot.addWidget(self.sc)
        df = self.model.data
        self.plot, = self.sc.axes.plot(df[df.columns[0]], df[df.columns[1]])
        self.toolbar = NavigationToolbar(self.sc, self)
        self.layoutPlot.addWidget(self.toolbar)
        self.plotHydrogramData()

        layoutInter = QHBoxLayout()
        layoutInter.addLayout(self.layoutList)
        layoutInter.addLayout(self.layoutData)
        self.layout.addLayout(layoutInter)
        self.layout.addLayout(self.layoutPlot)
    
    def newHydrogramButtonReleased(self):
        dlg = DialogNewHydrogram(parent=self)
        if dlg.exec():
            newHydogram = Hydrogram(dlg.hydroArgs)
            self.getProject().addHydrogram(newHydogram)
            self.getProject().setHydrogramSelected(newHydogram.name)
            item = QListWidgetItem(newHydogram.name)
            self.hydrogramList.addItem(item)
            self.hydrogramList.setCurrentItem(item)
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
        new_name = h.name + " (1)"
        i = 1
        while new_name in self.getProject().getHydrogramNameList():
            i += 1
            new_name = h.name + f" ({i})"
        h_copy = h.copy(new_name)
        self.getProject().addHydrogram(h_copy)
        self.getProject().setHydrogramSelected(h_copy.name)
        item = QListWidgetItem(h_copy.name)
        self.hydrogramList.addItem(item)
        self.hydrogramList.setCurrentItem(item)
        return

    def hydrogramChoiceChanged(self, name):
        self.getProject().setHydrogramSelected(name)
        self.displayHydrogramData()
        self.plotHydrogramData()
        return

    def displayHydrogramData(self):
        self.model = HydrogramTableModel(self.getProject().hydrogramSelected)
        self.hydrogramData.setModel(self.model)
        return

    def plotHydrogramData(self):
        df = self.model.data
        self.plot.set_xdata(df[df.columns[0]])
        self.plot.set_ydata(df[df.columns[1]])
        self.sc.axes.set_xlabel(df.columns[0])
        self.sc.axes.set_ylabel(df.columns[1])
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
