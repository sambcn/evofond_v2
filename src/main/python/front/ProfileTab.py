from urllib.parse import quote_plus
from PyQt5.QtWidgets import (
    QVBoxLayout, QMessageBox, QTableView, QHeaderView, QGridLayout, QWidget, QMenu, QAction,
    QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QAbstractItemView, QPushButton
)

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.Profile import Profile
from front.DialogNewProfile import DialogNewProfile
from front.DialogEditProfileGranulo import DialogEditProfileGranulo
from front.DialogDelete import DialogDelete
from front.TableModel import TableModel
from front.ProfileGranuloTable import ProfileGranuloTable
from front.MplCanvas import MplCanvas, NavigationToolbar

import pandas as pd

class ProfileTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Profil", tabBar.getResource("images\\profile.jpg"))

        self.layoutList = QVBoxLayout()

        self.layoutList.addWidget(QLabel("Liste des profils : "))
        self.profileList = QListWidget()
        self.setProfileList()        
        self.profileList.currentTextChanged.connect(self.profileChoiceChanged)
        self.layoutList.addWidget(self.profileList)
        self.newProfileButton = QPushButton(" NEW")
        self.newProfileButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newProfileButton.released.connect(self.newProfileButtonReleased)
        self.layoutList.addWidget(self.newProfileButton)
        self.editProfileButton = QPushButton(" EDIT")
        self.editing = False
        self.editProfileButton.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editProfileButton.released.connect(self.editProfileButtonReleased)
        self.layoutList.addWidget(self.editProfileButton)
        self.copyProfileButton = QPushButton(" COPY")
        self.copyProfileButton.setIcon(QIcon(self.getResource("images\\copy.png")))
        self.copyProfileButton.released.connect(self.copyProfileButtonReleased)
        self.layoutList.addWidget(self.copyProfileButton)
        self.deleteProfileButton = QPushButton(" DELETE")
        self.deleteProfileButton.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.deleteProfileButton.released.connect(self.deleteProfileButtonReleased)
        self.layoutList.addWidget(self.deleteProfileButton)

        self.tableLayout = QVBoxLayout()
        self.table = QTableView()
        self.table.setFont(QFont('Arial font', 10))
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeader(header)
        self.setTableData()
        self.tableLayout.addWidget(self.table)

        self.tableLayout.addWidget(QLabel("Gestion de la granulométrie :"))
        self.granuloTable = QTableView()
        header = self.granuloTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.granuloTable.setHorizontalHeader(header)
        self.granuloModel = ProfileGranuloTable(self)
        self.granuloTable.setModel(self.granuloModel)
        self.tableLayout.addWidget(self.granuloTable)
        self.editGranuloButton = QPushButton(" Modifier")
        self.editGranuloButton.setIcon(QIcon(self.getResource("images\\edit.png")))
        self.editGranuloButton.released.connect(self.editGranuloButtonReleased)
        self.tableLayout.addWidget(self.editGranuloButton)

        self.tableLayout.addWidget(QLabel("Données à tracer : "), alignment=Qt.AlignTop)

        self.plotOptionsLayout = QGridLayout()
        self.plotOptionsLayout.addWidget(QLabel("Abscisse"), 0, 0)
        self.plotOptionsLayout.addWidget(QLabel("Ordonnée 1"), 0, 1)
        self.plotOptionsLayout.addWidget(QLabel("Ordonnée 2"), 0, 2)
        
        self.varList1 = QListWidget()
        self.varList1.itemSelectionChanged.connect(self.plotData)
        self.varList2 = QListWidget()
        self.varList2.setSelectionMode(QAbstractItemView.ExtendedSelection)          
        self.varList2.itemSelectionChanged.connect(self.plotData)
        self.varList3 = QListWidget()
        self.varList3.setSelectionMode(QAbstractItemView.ExtendedSelection)   
        self.varList3.itemSelectionChanged.connect(self.plotData)
        self.updateVarLists() 
        
        self.plotOptionsLayout.addWidget(self.varList1, 1, 0)
        self.plotOptionsLayout.addWidget(self.varList2, 1, 1)
        self.plotOptionsLayout.addWidget(self.varList3, 1, 2)
    
        w = QWidget()
        w.setLayout(self.plotOptionsLayout)
        w.setFont(QFont('Arial font', 10))
        self.tableLayout.addWidget(w)        

        self.plotLayout = QVBoxLayout()
        self.sc = MplCanvas()
        self.plotLayout.addWidget(self.sc)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotData()
        
        self.layout1 = QHBoxLayout()
        self.layout1.addLayout(self.layoutList)
        self.layout1.addLayout(self.tableLayout)
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.plotLayout)

    def contextMenuOnTable(self, pos):
        context = QMenu(self)
        if self.editing:
            addUpperLine = QAction("Insérer une ligne au-dessus", self.table)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.table)
            deleteLine = QAction("Supprimer cette ligne", self.table)
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.table.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.table.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.table.indexAt(pos)))
            context.addAction(addUpperLine)
            context.addAction(addLowerLine)
            context.addAction(deleteLine)
            context.exec(self.table.mapToGlobal(pos))

    def editGranuloButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return
        dlg = DialogEditProfileGranulo(self, p)
        if dlg.exec():
            p.granulo = dlg.newGranulo
            self.granuloModel.refreshData()

    def newProfileButtonReleased(self):
        dlg = DialogNewProfile(self)
        if dlg.exec():
            newProfile = Profile(**dlg.profileArgs)
            self.getProject().addProfile(newProfile)
            self.getProject().setProfileSelected(newProfile.name)
            item = QListWidgetItem(newProfile.name)
            self.profileList.addItem(item)
            self.profileList.setCurrentItem(item)
            return
        pass

    def editProfileButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                self.model.restore()
            else:
                self.getProject().needToBeSaved = True
            self.editProfileButton.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editProfileButton.setText(" EDIT")
            self.profileList.setEnabled(True)
            self.newProfileButton.setEnabled(True)
            self.copyProfileButton.setEnabled(True)
            self.deleteProfileButton.setEnabled(True)
            self.editGranuloButton.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editProfileButton.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editProfileButton.setText(" STOP EDITING")
            self.profileList.setEnabled(False)
            self.newProfileButton.setEnabled(False)
            self.copyProfileButton.setEnabled(False)
            self.deleteProfileButton.setEnabled(False)
            self.editGranuloButton.setEnabled(False)
            self.disableOtherTabs()
        self.editing = not(self.editing)
        self.model.changeEditionMode()
        return

    def copyProfileButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return
        else:
            newName = p.name + " (1)"
        i = 1
        while newName in [prof.name for prof in self.getProject().profileList]:
            i += 1
            newName = p.name + f" ({i})"
        newProfile = p.copy(newName)
        self.getProject().addProfile(newProfile)
        item = QListWidgetItem(newProfile.name)
        self.profileList.addItem(item)
        return

    def deleteProfileButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return
        dlg = DialogDelete(p.name, parent=self)
        if dlg.exec():
            self.getProject().deleteProfile(p)
            self.profileList.takeItem(self.profileList.currentRow())
        return

    def sectionTypeListIndexChanged(self, i):
        self.tableLayout.setCurrentIndex(i)
        self.plotOptionsLayout.setCurrentIndex(i)
        self.plotData()
        return

    def setTableData(self):
        if self.getProject().profileSelected == None:
            self.table.setModel(None)
        else:
            p = self.getProject().profileSelected
            self.model = TableModel(self, p)
            self.table.setModel(self.model)
            
    def makeProfileListEmpty(self):
        for i in range(self.profileList.count()-1, -1, -1):
            self.profileList.takeItem(i)
        return
        
    def setProfileList(self):
        self.makeProfileListEmpty()
        for i, p in enumerate(self.getProject().profileList):
            item = QListWidgetItem(p.name)
            item.setSelected(i == self.getProject().profileSelectedIndex)
            self.profileList.addItem(item)
        return

    def refresh(self):
        self.setProfileList()
        return

    def profileChoiceChanged(self, name):
        self.getProject().setProfileSelected(name)
        self.setTableData()
        self.granuloModel.refreshData()
        self.updateVarLists()

    def makeVarListsEmpty(self):
        for i in range(self.varList1.count()-1, -1, -1):
            self.varList1.takeItem(i)
            self.varList2.takeItem(i)
            self.varList3.takeItem(i)

    def updateVarLists(self):
        self.makeVarListsEmpty()
        if self.getProject().profileSelected != None:     
            for c in self.getProject().profileSelected.data.columns:
                self.varList1.addItem(c)
                self.varList2.addItem(c)
                self.varList3.addItem(c)
        return

    def plotData(self):
        if self.getProject().profileSelected == None:
            return
        else:
            df = self.getProject().profileSelected.data
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.lines.clear()
            if twinAx != a:
                twinAx.remove()
        a.set_prop_cycle(None)
        atLeastOneCurve = False
        lines = []

        x = self.varList1.currentRow()
        y1 = ProfileTab.getIndexSelectedList(self.varList2)
        y2 = ProfileTab.getIndexSelectedList(self.varList3)

        xlabel = df.columns[x] if x != -1 else ""
        y1label = ""
        y2label = ""

        for y1Index in y1:
            atLeastOneCurve = True
            subdf = df[~(df[df.columns[x]].isnull()) & ~(df[df.columns[y1Index]].isnull())]
            lines += a.plot(subdf[subdf.columns[x]], subdf[subdf.columns[y1Index]], label=subdf.columns[y1Index].replace("\n",""))
            if y1label != "":
                y1label += " - " 
            y1label += subdf.columns[y1Index].replace("\n","")

        if y2 != []:
            atLeastOneCurve = True
            twinAxeList = a.get_shared_x_axes().get_siblings(a)
            twinAxeList.pop(twinAxeList.index(a))
            if twinAxeList == []:
                twinAxe = a.twinx()
            else:
                twinAxe = twinAxeList[0]
            twinAxe.set_ylabel(y2label)

        for i, y2Index in enumerate(y2):
            subdf = df[~(df[df.columns[x]].isnull()) & ~(df[df.columns[y2Index]].isnull())]
            lines += twinAxe.plot(subdf[subdf.columns[x]], subdf[subdf.columns[y2Index]], label=subdf.columns[y2Index].replace("\n",""), linestyle="dashed")
            if i == len(y2)-1:
                y2label += subdf.columns[y2Index].replace("\n","")
                twinAxe.set_ylabel(y2label)
            else:
                y2label += subdf.columns[y2Index].replace("\n","") + " - "

        a.set_xlabel(xlabel)
        a.set_ylabel(y1label)

        if atLeastOneCurve: 
            self.sc.axes.legend(lines, [l.get_label() for l in lines])
        else:
            l = self.sc.axes.get_legend()
            if l != None: 
                l.remove()
        
        a.relim()
        a.autoscale()
        self.sc.draw()
        
        return



    # static function

    def getIndexSelectedList(qlist):
        result = []
        for i in range(qlist.count()):
            if qlist.item(i).isSelected():
                result.append(i)
        return result

