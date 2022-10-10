from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap

class DialogNewHydrogram(QDialog):

    def __init__(self, parent=None):
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
        methodList = QComboBox()
        methodList.addItem("Lavabre")
        methodList.addItem("Importer")
        methodList.addItem("Manuel")
        methodList.currentIndexChanged.connect(self.indexChanged)
        methodList.currentTextChanged.connect(self.textChanged)
        self.hydroArgs["type"] = methodList.currentText()
        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom de l'hydrogramme")
        nameField.textChanged.connect(self.nameChanged)
        self.hydroArgs["name"] = nameField.text()
        vlayout.addWidget(methodList)
        vlayout.addWidget(nameField)
        hlayout.addLayout(vlayout)

        self.slayout = QStackedLayout()
        lavabreLayout = QHBoxLayout()
        lavabreLayout1 = QGridLayout()
        
        lavabreLayout1.addWidget(QLabel("d = "), 0, 0)
        lavabreLayout1.addWidget(QLabel("Q_max = "), 1, 0)
        lavabreLayout1.addWidget(QLabel("Q_min = "), 2, 0)
        lavabreLayout1.addWidget(QLabel("t_max = "), 3, 0)
        lavabreLayout1.addWidget(QLabel("alpha = "), 4, 0)

        self.doubleBoxDuration = QDoubleSpinBox()
        self.doubleBoxDuration.valueChanged.connect(self.lavabreDurationChange)
        self.doubleBoxDuration.setSuffix("   s")
        self.doubleBoxDuration.setMinimum(0)
        self.doubleBoxDuration.setMaximum(999999.99)
        lavabreLayout1.addWidget(self.doubleBoxDuration, 0, 1)
        self.hydroArgs['d'] = self.doubleBoxDuration.value()
        self.doubleBoxQmax = QDoubleSpinBox()
        self.doubleBoxQmax.valueChanged.connect(self.lavabreQmaxChange)
        self.doubleBoxQmax.setSuffix("   m3/s")
        self.doubleBoxQmax.setMinimum(0)
        lavabreLayout1.addWidget(self.doubleBoxQmax, 1, 1)
        self.hydroArgs['Qmax'] = self.doubleBoxQmax.value()
        self.doubleBoxQmin = QDoubleSpinBox()
        self.doubleBoxQmin.valueChanged.connect(self.lavabreQminChange)
        self.doubleBoxQmin.setSuffix("   m3/s")
        self.doubleBoxQmin.setMinimum(0)
        lavabreLayout1.addWidget(self.doubleBoxQmin, 2, 1)
        self.hydroArgs['Qmin'] = self.doubleBoxQmin.value()
        self.doubleBoxTmax = QDoubleSpinBox()
        self.doubleBoxTmax.valueChanged.connect(self.lavabreTmaxChange)
        self.doubleBoxTmax.setSuffix("   s")
        self.doubleBoxTmax.setMinimum(0)
        self.doubleBoxDuration.setMaximum(999999.99)
        lavabreLayout1.addWidget(self.doubleBoxTmax, 3, 1)
        self.hydroArgs['tmax'] = self.doubleBoxTmax.value()
        self.doubleBoxAlpha = QDoubleSpinBox()
        self.doubleBoxAlpha.valueChanged.connect(self.lavabreAlphaChange)
        self.doubleBoxAlpha.setSuffix("    ")
        self.doubleBoxAlpha.setMinimum(0)
        lavabreLayout1.addWidget(self.doubleBoxAlpha, 4, 1)
        self.hydroArgs['alpha'] = self.doubleBoxAlpha.value()

        lavabreLayout1.addWidget(QLabel("    (durée de l'évènement)"), 0, 2)
        lavabreLayout1.addWidget(QLabel("    (débit maximum)"), 1, 2)
        lavabreLayout1.addWidget(QLabel("    (débit minimum)"), 2, 2)
        lavabreLayout1.addWidget(QLabel("    (instant du pic de crue)"), 3, 2)
        lavabreLayout1.addWidget(QLabel("    (degré des polynomes de la formule de Lavabre)"), 4, 2)

        lavabreLayout2 = QGridLayout()
        image = QLabel()
        image.setPixmap(QPixmap('..\\icons\\base\\lavabreFormula.png'))
        lavabreLayout2.addWidget(image, 0, 0)

        lavabreLayout.addLayout(lavabreLayout1)
        lavabreLayout.addLayout(lavabreLayout2)
        lavabreWidget = QWidget()
        lavabreWidget.setLayout(lavabreLayout)
        self.slayout.addWidget(lavabreWidget)

        importWidget = QPushButton("parcourir")
        self.slayout.addWidget(importWidget)


        hlayout.addLayout(self.slayout)

        self.layout.addLayout(hlayout)

        ###
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def nameChanged(self, s):
        self.hydroArgs["name"] = s

    def indexChanged(self, i):
        self.slayout.setCurrentIndex(i)

    def textChanged(self, s):
        self.hydroArgs["type"] = s

    def lavabreDurationChange(self, v):
        self.hydroArgs["d"] = v
        self.doubleBoxTmax.setMaximum(v)

    def lavabreQminChange(self, v):
        self.hydroArgs["Qmin"] = v
        self.doubleBoxQmax.setMinimum(v)

    def lavabreQmaxChange(self, v):
        self.hydroArgs["Qmax"] = v
        self.doubleBoxQmin.setMaximum(v)

    def lavabreTmaxChange(self, v):
        self.hydroArgs["tmax"] = v

    def lavabreAlphaChange(self, v):
        self.hydroArgs["alpha"] = v

    def check(self):
        if self.hydroArgs["name"].split() == []:
            QMessageBox.critical(self, "Error : no name for the new hydrogram", "Please give a valid name to the hydrogram")
            return
        elif self.hydroArgs["name"] in self.parent().getProject().getHydrogramNameList():
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        elif self.hydroArgs["d"]==0:
            QMessageBox.critical(self, "Error : duration must be strictly positive", "You must give d > 0")
            return
        elif self.hydroArgs["tmax"]==0:
            QMessageBox.critical(self, "Error : t_max must be strictly positive", "You must give t_max > 0")
            return
        if True:
            self.accept()