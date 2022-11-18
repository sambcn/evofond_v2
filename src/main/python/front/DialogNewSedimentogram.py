from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from front.Sedimentogram import Sedimentogram
from utils import SEDIMENT_TRANSPORT_LAW_DICT

class DialogNewSedimentogram(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("New sedimentogram")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        ###

        self.sedimentoArgs = dict()
        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        self.methodList = QComboBox()
        self.methodList.addItem("Classique")
        self.methodList.addItem("Importer")
        self.methodList.addItem("Manuel")
        self.methodList.currentIndexChanged.connect(self.indexChanged)
        self.methodList.currentTextChanged.connect(self.textChanged)
        self.sedimentoArgs["type"] = self.methodList.currentText()
        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom du sedimentogramme")
        nameField.textChanged.connect(self.nameChanged)
        self.sedimentoArgs["name"] = nameField.text()
        vlayout.addWidget(self.methodList)
        vlayout.addWidget(nameField)
        hlayout.addLayout(vlayout)

        self.slayout = QStackedLayout()

        self.classicalGridLayout = QGridLayout()
        self.classicalGridLayout.addWidget(QLabel("Granulométrie : "), 0, 0)
        self.classicalGridLayout.addWidget(QLabel("Hydrogramme associé : "), 1, 0)
        self.classicalGridLayout.addWidget(QLabel("Loi de transport solide : "), 2, 0)
        self.classicalGridLayout.addWidget(QLabel("Pente d'apport = "), 3, 0)
        self.classicalGridLayout.addWidget(QLabel("Largeur amont = "), 4, 0)

        self.granulometryList = QComboBox()
        self.granulometryList.currentTextChanged.connect(self.classicalGranulometryChanged)
        for g in self.parent().getProject().getGranulometryNameList():
            self.granulometryList.addItem(g)
        self.classicalGridLayout.addWidget(self.granulometryList, 0, 1)
        self.sedimentoArgs['granulometry'] = self.granulometryList.currentText()    

        self.hydrogramList = QComboBox()
        self.hydrogramList.currentTextChanged.connect(self.classicalHydrogramChanged)
        for g in self.parent().getProject().getHydrogramNameList():
            self.hydrogramList.addItem(g)
        self.classicalGridLayout.addWidget(self.hydrogramList, 1, 1)
        self.sedimentoArgs['hydrogram'] = self.hydrogramList.currentText()    

        self.sedimentTransportLawList = QComboBox()
        self.sedimentTransportLawList.currentTextChanged.connect(self.classicalLawChanged)
        self.sedimentTransportLawList.addItems(SEDIMENT_TRANSPORT_LAW_DICT.keys())
        self.classicalGridLayout.addWidget(self.sedimentTransportLawList, 2, 1)
        self.sedimentoArgs['law'] = self.sedimentTransportLawList.currentText()    

        self.doubleBoxSlope = QDoubleSpinBox()
        self.doubleBoxSlope.valueChanged.connect(self.classicalSlopeChanged)
        self.doubleBoxSlope.setSingleStep(0.1)
        self.doubleBoxSlope.setDecimals(3)
        self.doubleBoxSlope.setSuffix("   %")
        self.doubleBoxSlope.setMinimum(0)
        self.doubleBoxSlope.setMaximum(999.999)
        self.classicalGridLayout.addWidget(self.doubleBoxSlope, 3, 1)
        self.sedimentoArgs['slope'] = self.doubleBoxSlope.value()/100 # conversion % en m/m

        self.doubleBoxWidth = QDoubleSpinBox()
        self.doubleBoxWidth.valueChanged.connect(self.classicalWidthChanged)
        self.doubleBoxWidth.setSuffix("   m")
        self.doubleBoxWidth.setMinimum(0)
        self.doubleBoxWidth.setMaximum(999999.99)
        self.classicalGridLayout.addWidget(self.doubleBoxWidth, 4, 1)
        self.sedimentoArgs['width'] = self.doubleBoxSlope.value()    
        
        self.classicalGridWidget = QWidget()
        self.classicalGridWidget.setLayout(self.classicalGridLayout)
        self.slayout.addWidget(self.classicalGridWidget)


        importWidget = QPushButton(" Parcourir ")
        importWidget.released.connect(self.importButtonReleased)
        importlayout = QGridLayout()
        importlayout.addWidget(QLabel("selected file : "), 0, 0, alignment=Qt.AlignRight)
        self.selectedFile = QLabel("")
        self.selectedFile.setStyleSheet("border: 1px solid black;padding: 8px; font-family: 'Arial font'; font-size: 14px")
        importlayout.addWidget(self.selectedFile, 0, 1, alignment=Qt.AlignVCenter)
        importlayout.addWidget(importWidget, 0, 2, alignment=(Qt.AlignVCenter | Qt.AlignLeft))
        interwidget = QWidget()
        interwidget.setFont(QFont('Arial font', 12))
        interwidget.setLayout(importlayout)
        self.slayout.addWidget(interwidget)

        self.slayout.addWidget(QWidget())

        hlayout.addLayout(self.slayout)

        self.layout.addLayout(hlayout)

        ###
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def classicalGranulometryChanged(self, g):
        self.sedimentoArgs["granulometry"] = g

    def classicalHydrogramChanged(self, h):
        self.sedimentoArgs["hydrogram"] = h

    def classicalLawChanged(self, l):
        self.sedimentoArgs["law"] = l

    def classicalSlopeChanged(self, s):
        self.sedimentoArgs["slope"] = s/100 # conversion % en m/m

    def classicalWidthChanged(self, w):
        self.sedimentoArgs["width"] = w

    def importButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.csv *.txt")
        if dlg.exec():
            self.sedimentoArgs["path"] = dlg.selectedFiles()[-1]
            self.selectedFile.setText(self.sedimentoArgs["path"])

    def nameChanged(self, s):
        self.sedimentoArgs["name"] = s

    def indexChanged(self, i):
        self.slayout.setCurrentIndex(i)

    def textChanged(self, s):
        self.sedimentoArgs["type"] = s

    def check(self):
        if self.sedimentoArgs["name"].split() == []:
            QMessageBox.critical(self, "Error : no name for the new sedimentogram", "Please give a valid name to the sedimentogram")
            return
        elif self.sedimentoArgs["name"] in self.parent().getProject().getSedimentogramNameList():
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        if self.sedimentoArgs["type"] == self.methodList.itemText(0):
            if self.granulometryList.count() == 0:
                QMessageBox.critical(self, "Error : no granulometry", "Please create at least one granulometry before building a sedimentogram")
                return
            if self.hydrogramList.count() == 0:
                QMessageBox.critical(self, "Error : no hydrogram", "Please create at least one hydrogram before building a sedimentogram")
                return
            if self.sedimentoArgs["width"] <= 0 :
                QMessageBox.critical(self, "Error : width zero", "Please give a positive width")
                return
            if self.sedimentoArgs["slope"] <= 0 :
                QMessageBox.critical(self, "Error : slope zero", "Please give a positive slope")
                return
            hName = self.sedimentoArgs["hydrogram"]
            gName = self.sedimentoArgs["granulometry"]
            self.sedimentoArgs["hydrogram"] = self.parent().getProject().getHydrogram(hName)
            self.sedimentoArgs["granulometry"] = self.parent().getProject().getGranulometry(gName)            
            self.sedimentogram = Sedimentogram(self.sedimentoArgs)
        if self.sedimentoArgs["type"] == self.methodList.itemText(1):
            if not("path" in self.sedimentoArgs.keys()):
                QMessageBox.critical(self, "Error : no file selected", "Please choose a file (.csv or .txt)")
                return
            try:
                self.sedimentogram = Sedimentogram(self.sedimentoArgs)
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error : could not open te file", "The file could not be converted. \n Please check that you gave a .csv with at least two columns (time t - sediment discharge Qs)")
                return
            except ValueError:
                QMessageBox.critical(self, "Error : not enough columns", "Less than 2 columns detected. \n Please check that you gave a .csv with at least two columns (time t - sediment discharge Qs)")
                return
        if self.sedimentoArgs["type"] == self.methodList.itemText(2):
            self.sedimentogram = Sedimentogram(self.sedimentoArgs)
        self.accept()