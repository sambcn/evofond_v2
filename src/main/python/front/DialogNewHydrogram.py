from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from front.Hydrogram import Hydrogram

class DialogNewHydrogram(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("New hydrogram")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        ###

        self.hydroArgs = dict()
        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        self.methodList = QComboBox()
        self.methodList.addItem("Importer")
        self.methodList.addItem("Lavabre")
        self.methodList.addItem("Manuel")
        self.methodList.currentIndexChanged.connect(self.indexChanged)
        self.methodList.currentTextChanged.connect(self.textChanged)
        self.hydroArgs["type"] = self.methodList.currentText()
        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom de l'hydrogramme")
        nameField.textChanged.connect(self.nameChanged)
        self.hydroArgs["name"] = nameField.text()
        vlayout.addWidget(self.methodList)
        vlayout.addWidget(nameField)
        hlayout.addLayout(vlayout)

        self.slayout = QStackedLayout()

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

        lavabreLayout = QHBoxLayout()
        lavabreLayout1 = QGridLayout()
        
        lavabreLayout1.addWidget(QLabel("d = "), 0, 0)
        lavabreLayout1.addWidget(QLabel("dt = "), 1, 0)
        lavabreLayout1.addWidget(QLabel("Q_max = "), 2, 0)
        lavabreLayout1.addWidget(QLabel("Q_min = "), 3, 0)
        lavabreLayout1.addWidget(QLabel("t_max = "), 4, 0)
        lavabreLayout1.addWidget(QLabel("alpha = "), 5, 0)

        self.doubleBoxDuration = QDoubleSpinBox()
        self.doubleBoxDuration.valueChanged.connect(self.lavabreDurationChanged)
        self.doubleBoxDuration.setSuffix("   h")
        self.doubleBoxDuration.setMinimum(0)
        self.doubleBoxDuration.setMaximum(999999.99)
        lavabreLayout1.addWidget(self.doubleBoxDuration, 0, 1)
        self.hydroArgs['d'] = self.doubleBoxDuration.value()*3600
        self.doubleBoxTimeStep = QDoubleSpinBox()
        self.doubleBoxTimeStep.valueChanged.connect(self.lavabreTimeStepChanged)
        self.doubleBoxTimeStep.setSuffix("   s")
        self.doubleBoxTimeStep.setMinimum(0)
        self.doubleBoxTimeStep.setMaximum(self.doubleBoxDuration.value())
        lavabreLayout1.addWidget(self.doubleBoxTimeStep, 1, 1)
        self.hydroArgs['dt'] = self.doubleBoxDuration.value()
        self.doubleBoxQmax = QDoubleSpinBox()
        self.doubleBoxQmax.valueChanged.connect(self.lavabreQmaxChanged)
        self.doubleBoxQmax.setSuffix("   m3/s")
        self.doubleBoxQmax.setMinimum(0)
        self.doubleBoxQmax.setMaximum(999.99)
        lavabreLayout1.addWidget(self.doubleBoxQmax, 2, 1)
        self.hydroArgs['Qmax'] = self.doubleBoxQmax.value()
        self.doubleBoxQmin = QDoubleSpinBox()
        self.doubleBoxQmin.valueChanged.connect(self.lavabreQminChanged)
        self.doubleBoxQmin.setSuffix("   m3/s")
        self.doubleBoxQmin.setMinimum(0)
        lavabreLayout1.addWidget(self.doubleBoxQmin, 3, 1)
        self.hydroArgs['Qmin'] = self.doubleBoxQmin.value()
        self.doubleBoxTmax = QDoubleSpinBox()
        self.doubleBoxTmax.valueChanged.connect(self.lavabreTmaxChanged)
        self.doubleBoxTmax.setSuffix("   h")
        self.doubleBoxTmax.setMinimum(0)
        self.doubleBoxDuration.setMaximum(999999.99)
        lavabreLayout1.addWidget(self.doubleBoxTmax, 4, 1)
        self.hydroArgs['tmax'] = self.doubleBoxTmax.value()*3600
        self.doubleBoxAlpha = QDoubleSpinBox()
        self.doubleBoxAlpha.valueChanged.connect(self.lavabreAlphaChanged)
        self.doubleBoxAlpha.setSuffix("    ")
        self.doubleBoxAlpha.setMinimum(0)
        lavabreLayout1.addWidget(self.doubleBoxAlpha, 5, 1)
        self.hydroArgs['alpha'] = self.doubleBoxAlpha.value()

        lavabreLayout1.addWidget(QLabel("    (durée de l'évènement)"), 0, 2)
        lavabreLayout1.addWidget(QLabel("    (pas de temps)"), 1, 2)
        lavabreLayout1.addWidget(QLabel("    (débit maximum)"), 2, 2)
        lavabreLayout1.addWidget(QLabel("    (débit minimum)"), 3, 2)
        lavabreLayout1.addWidget(QLabel("    (instant du pic de crue)"), 4, 2)
        lavabreLayout1.addWidget(QLabel("    (degré des polynomes de la formule de Lavabre)"), 5, 2)

        lavabreLayout2 = QGridLayout()
        image = QLabel()
        image.setPixmap(QPixmap(self.parent().getResource('images\\lavabreFormula.png')))
        lavabreLayout2.addWidget(image, 0, 0)

        lavabreLayout.addLayout(lavabreLayout1)
        lavabreLayout.addLayout(lavabreLayout2)
        lavabreWidget = QWidget()
        lavabreWidget.setLayout(lavabreLayout)
        self.slayout.addWidget(lavabreWidget)

        self.slayout.addWidget(QWidget())

        hlayout.addLayout(self.slayout)

        self.layout.addLayout(hlayout)

        ###
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def importButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setNameFilter("*.csv *.txt")
        if dlg.exec():
            self.hydroArgs["path"] = dlg.selectedFiles()[-1]
            self.selectedFile.setText(self.hydroArgs["path"])

    def nameChanged(self, s):
        self.hydroArgs["name"] = s

    def indexChanged(self, i):
        self.slayout.setCurrentIndex(i)

    def textChanged(self, s):
        self.hydroArgs["type"] = s

    def lavabreDurationChanged(self, v):
        v_sec = v*3600
        self.hydroArgs["d"] = v_sec
        self.doubleBoxTmax.setMaximum(v)
        self.doubleBoxTimeStep.setMaximum(v_sec)
    
    def lavabreTimeStepChanged(self, v):
        self.hydroArgs["dt"] = v

    def lavabreQminChanged(self, v):
        self.hydroArgs["Qmin"] = v
        self.doubleBoxQmax.setMinimum(v)

    def lavabreQmaxChanged(self, v):
        self.hydroArgs["Qmax"] = v
        self.doubleBoxQmin.setMaximum(v)

    def lavabreTmaxChanged(self, v):
        self.hydroArgs["tmax"] = v*3600

    def lavabreAlphaChanged(self, v):
        self.hydroArgs["alpha"] = v

    def check(self):
        if self.hydroArgs["name"].split() == []:
            QMessageBox.critical(self, "Error : no name for the new hydrogram", "Please give a valid name to the hydrogram")
            return
        elif self.hydroArgs["name"] in self.parent().getProject().getHydrogramNameList():
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        if self.hydroArgs["type"] == self.methodList.itemText(0):
            if not("path" in self.hydroArgs.keys()):
                QMessageBox.critical(self, "Error : no file selected", "Please choose a file (.csv or .txt)")
                return
            try:
                self.hydrogram = Hydrogram(self.hydroArgs)
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Error : could not open te file", "The file could not be converted. \n Please check that you gave a .csv with at least two columns (time t - water discharge Q)")
                return
            except ValueError:
                QMessageBox.critical(self, "Error : not enough columns", "Less than 2 columns detected. \n Please check that you gave a .csv with at least two columns (time t - water discharge Q)")
                return
        if self.hydroArgs["type"] == self.methodList.itemText(1):
            if self.hydroArgs["d"]==0:
                QMessageBox.critical(self, "Error : duration must be strictly positive", "You must give d > 0")
                return
            elif self.hydroArgs["dt"]==0:
                QMessageBox.critical(self, "Error : time step must be strictly positive", "You must give dt > 0")
                return
            elif self.hydroArgs["tmax"]==0:
                QMessageBox.critical(self, "Error : t_max must be strictly positive", "You must give t_max > 0")
                return
            self.hydrogram = Hydrogram(self.hydroArgs)
        if self.hydroArgs["type"] == self.methodList.itemText(2):
            self.hydrogram = Hydrogram(self.hydroArgs)
        self.accept()