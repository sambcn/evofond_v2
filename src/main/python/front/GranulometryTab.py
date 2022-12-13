from PyQt5.QtWidgets import (
    QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QTableView, QHeaderView
)
from PyQt5.QtGui import QIcon

from front.Tab import Tab
from front.DialogNewGranulo import DialogNewGranulo
from front.DialogDelete import DialogDelete
from front.GranuloTableView import GranuloTableModel

class GranulometryTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Granulométrie", tabBar.getResource("images\\granulo.png"))

        self.granuloListLayout = QVBoxLayout()
        self.granuloListLayout.addWidget(QLabel("Liste des granulométries : "))
        self.granuloList = QListWidget()
        for g in self.getProject().getGranulometryNameList():
            self.granuloList.addItem(g)
        self.granuloList.currentTextChanged.connect(self.granuloNameChanged)
        self.granuloListLayout.addWidget(self.granuloList)

        
        self.newGranuloButton = QPushButton(" NEW")
        self.newGranuloButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newGranuloButton.released.connect(self.newGranuloButtonReleased)
        self.granuloListLayout.addWidget(self.newGranuloButton)
        self.deleteGranuloButton = QPushButton(" DELETE")
        self.deleteGranuloButton.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.deleteGranuloButton.released.connect(self.deleteGranuloButtonReleased)
        self.granuloListLayout.addWidget(self.deleteGranuloButton)
        # self.copyGranuloButton = QPushButton(" COPY")
        # self.copyGranuloButton.setIcon(QIcon(self.getResource("images\\copy.png")))
        # self.copyGranuloButton.released.connect(self.copyGranuloButtonReleased)
        # self.granuloListLayout.addWidget(self.copyGranuloButton)

        self.table = QTableView()
        self.model = GranuloTableModel(self)
        header = self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeader(header)
        self.table.setModel(self.model)

        self.layout.addLayout(self.granuloListLayout)
        self.layout.addWidget(self.table, stretch=100)
    
    def granuloNameChanged(self, s):
        self.getProject().setGranulometrySelected(s)
        return

    def newGranuloButtonReleased(self):
        dlg = DialogNewGranulo(parent=self)
        if dlg.exec():
            granulo = dlg.granulometry
            self.getProject().addGranulometry(granulo)
            self.getProject().setGranulometrySelected(granulo.name)
            item = QListWidgetItem(granulo.name)
            self.granuloList.addItem(item)
            self.granuloList.setCurrentItem(item)
            self.model.refreshData()


    def deleteGranuloButtonReleased(self):
        g = self.getProject().granulometrySelected
        if g == None:
            return
        dlg = DialogDelete(g.name, parent=self)
        if dlg.exec():
            self.getProject().deleteGranulometry(g)
            self.granuloList.takeItem(self.granuloList.currentRow())
            self.model.refreshData()
        return

    # def copyGranuloButtonReleased(self):
    #     g = self.getProject().granulometrySelected
    #     if g == None:
    #         return
    #     newName = g.name + " (1)"
    #     i = 1
    #     while newName in self.getProject().getGranulometryNameList():
    #         i += 1
    #         newName = g.name + f" ({i})"
    #     gCopy = g.copy(newName)
    #     self.getProject().addGranulometry(gCopy)
    #     item = QListWidgetItem(gCopy.name)
    #     self.granuloList.addItem(item)
    #     self.model.refreshData()
    #     return
        
    def setGranuloList(self):
        gSelected = self.getProject().granulometrySelected
        self.granuloList.clear()
        for g in self.getProject().granulometryList:
            self.granuloList.addItem(g.name)
            if g == gSelected:
                self.granuloList.setCurrentRow(self.granuloList.count()-1)
        return

    def refresh(self):
        self.setGranuloList()
        self.model.refreshData()
        return

