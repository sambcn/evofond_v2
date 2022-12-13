from urllib.parse import quote_plus
from PyQt5.QtWidgets import (
    QVBoxLayout, QMessageBox, QTableView, QHeaderView, QGridLayout, QWidget, QMenu, QAction,
    QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QAbstractItemView, QPushButton, QFileDialog
)

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.Profile import Profile
from front.DialogNewProfile import DialogNewProfile
from front.DialogQuestionAnswer import DialogQuestionAnswer
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
        self.profileList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.profileList.customContextMenuRequested.connect(self.contextMenuOnList)        
        
        self.layoutList.addWidget(self.profileList)
        self.newProfileButton = QPushButton(" NEW")
        self.newProfileButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.newProfileButton.released.connect(self.newProfileButtonReleased)
        self.layoutList.addWidget(self.newProfileButton)
        self.importProfileButton = QPushButton(" IMPORT")
        self.importProfileButton.setIcon(QIcon(self.getResource("images\\export.png")))
        self.importProfileButton.released.connect(self.importProfileButtonReleased)
        self.layoutList.addWidget(self.importProfileButton)
        self.renameWidget = QPushButton(" RENAME")
        self.renameWidget.setIcon(QIcon(self.getResource("images\\rename.png")))
        self.renameWidget.released.connect(self.renameButtonReleased)
        self.layoutList.addWidget(self.renameWidget)
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
        self.table.setFont(QFont('Arial font', 8))
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.contextMenuOnTable)
        header = self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalHeader(header)
        self.setTableData()
        self.tableLayout.addWidget(self.table)

        self.addColumnButton = QPushButton(" Ajouter une colonne")
        self.addColumnButton.setIcon(QIcon(self.getResource("images\\add.png")))
        self.tableLayout.addWidget(self.addColumnButton, alignment=Qt.AlignLeft)
        self.addColumnButton.released.connect(self.addColumnButtonReleased)
        self.addColumnButton.setEnabled(False)

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
        self.sc.toggle.connect(self.toggleFigure)
        self.toolbar = NavigationToolbar(self.sc, self)

        self.plotWidget = QWidget(parent=self)
        self._vlaout = QVBoxLayout()
        self._vlaout.addWidget(self.sc)
        self._vlaout.addWidget(self.toolbar)
        self.plotWidget.setLayout(self._vlaout)
        self.plotLayout.addWidget(self.plotWidget)

        self.plotData()
        
        self.layout.addLayout(self.layoutList)
        self.layout.addLayout(self.tableLayout)
        self.layout.addLayout(self.plotLayout, stretch=100)

    def contextMenuOnTable(self, pos):
        context = QMenu(self)
        copy = QAction("Copier", self.table)
        copy.triggered.connect(self.model.copy)
        context.addAction(copy)
        if self.editing:
            paste = QAction("Coller", self.table)
            addUpperLine = QAction("Insérer une ligne au-dessus", self.table)
            addLowerLine = QAction("Insérer une ligne en-dessous", self.table)
            deleteLine = QAction("Supprimer cette ligne", self.table)
            paste.triggered.connect(self.model.paste(self.table.indexAt(pos)))
            addUpperLine.triggered.connect(self.model.addUpperLineForConnection(self.table.indexAt(pos)))
            addLowerLine.triggered.connect(self.model.addLowerLineForConnection(self.table.indexAt(pos)))
            deleteLine.triggered.connect(self.model.deleteLineForConnection(self.table.indexAt(pos)))
            context.addAction(paste)
            context.addAction(addUpperLine)
            context.addAction(addLowerLine)
            context.addAction(deleteLine)
        context.exec(self.table.mapToGlobal(pos))

    def contextMenuOnList(self, pos):
        context = QMenu(self)
        item = self.profileList.itemAt(pos)
        if item != None:
            self.getProject().setProfileSelected(item.text())
            rename = QAction("Renommer", self.profileList)
            importData = QAction("Importer des données", self.profileList)
            edit = QAction("Editer", self.profileList)
            copy = QAction("Copier", self.profileList)
            delete = QAction("Supprimer", self.profileList)
            rename.triggered.connect(self.renameButtonReleased)
            importData.triggered.connect(self.importProfileButtonReleased)
            edit.triggered.connect(self.editProfileButtonReleased)
            copy.triggered.connect(self.copyProfileButtonReleased)
            delete.triggered.connect(self.deleteProfileButtonReleased)
            context.addAction(rename)
            context.addAction(importData)
            context.addAction(edit)
            context.addAction(copy)
            context.addAction(delete)
        else:
            newProfile = QAction("Nouveau profil", self.profileList)
            newProfile.triggered.connect(self.newProfileButtonReleased)
            context.addAction(newProfile)
        context.exec(self.profileList.mapToGlobal(pos))

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

    def importProfileButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            QMessageBox.critical(self, "pas de profil selectionné", "veuillez choisir un profil dans lequel importer vos données")
            return
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.csv")
        if dlg.exec():
            path = dlg.selectedFiles()[-1]
            p.importData(path)
            self.model.layoutChanged.emit()

    def renameButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return
        dlg = DialogQuestionAnswer(self, f"Choississez un nouveau nom pour le profil {p.name}")
        if dlg.exec():
            newName = dlg.answer
            if newName.split() == []:
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est invalide")
                return
            if newName == p.name:
                QMessageBox.information(self, "Nom identique", "Le nom est inchangé")
                return
            if newName in self.getProject().getProfileNameList():
                QMessageBox.critical(self, "Nom invalide", "Le nom choisi est déjà pris par un autre profil")
                return
            p.name = newName
            self.setProfileList()

    def editProfileButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return True
        if self.editing:
            if QMessageBox.question(self, "Fin d'édition", "Voulez-vous enregistrer les modifications ?") == QMessageBox.No:
                self.model.restore()
                header = self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.table.setHorizontalHeader(header)
            else:
                self.getProject().needToBeSaved = True
            self.editProfileButton.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editProfileButton.setText(" EDIT")
            self.profileList.setEnabled(True)
            self.newProfileButton.setEnabled(True)
            self.importProfileButton.setEnabled(True)
            self.renameWidget.setEnabled(True)
            self.copyProfileButton.setEnabled(True)
            self.deleteProfileButton.setEnabled(True)
            self.addColumnButton.setEnabled(False)
            self.editGranuloButton.setEnabled(True)
            self.enableOtherTabs()
        else:
            self.editProfileButton.setIcon(QIcon(self.getResource("images\\edit.png")))
            self.editProfileButton.setText(" STOP EDITING")
            self.profileList.setEnabled(False)
            self.newProfileButton.setEnabled(False)
            self.importProfileButton.setEnabled(False)
            self.copyProfileButton.setEnabled(False)
            self.renameWidget.setEnabled(False)
            self.deleteProfileButton.setEnabled(False)
            self.addColumnButton.setEnabled(True)
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

    def addColumnButtonReleased(self):
        p = self.getProject().profileSelected
        if p == None:
            return
        dlg = DialogQuestionAnswer(self, "Nom de la nouvelle colonne : ")
        if dlg.exec():
            p.addColumn(dlg.answer)
            self.model.layoutChanged.emit()
            header = self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.setHorizontalHeader(header)
            self.updateVarLists()

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
        return
        
    def setProfileList(self):
        pSelected = self.getProject().profileSelected
        self.profileList.clear()
        for p in self.getProject().getProfileNameList():
            self.profileList.addItem(p)
        if pSelected != None:
            self.profileList.setCurrentRow(self.getProject().profileList.index(pSelected))
        return

    def refresh(self):
        self.setProfileList()
        self.updateVarLists()
        self.plotData()
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

