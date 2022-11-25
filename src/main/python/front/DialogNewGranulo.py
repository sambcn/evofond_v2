from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QLabel, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont

from front.Granulometry import Granulometry

class DialogNewGranulo(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New granulometry")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###

        self.argsGranulo = dict()

        self.hLayout = QHBoxLayout()

        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom de la granulométrie")
        nameField.textChanged.connect(self.nameChanged)
        self.argsGranulo["name"] = nameField.text()
        self.hLayout.addWidget(nameField)

        self.gridLayout = QGridLayout()

        self.gridLayout.addWidget(QLabel("dm = "), 0, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.dmChanged)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 0, 1)
        self.argsGranulo['dm'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("d30 = "), 1, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.d30Changed)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 1, 1)
        self.argsGranulo['d30'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("d50 = "), 2, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.d50Changed)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 2, 1)
        self.argsGranulo['d50'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("d90 = "), 3, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.d90Changed)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 3, 1)
        self.argsGranulo['d90'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("d84tb = "), 4, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.d84tbChanged)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 4, 1)
        self.argsGranulo['d84tb'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("d84bs = "), 5, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.d84bsChanged)
        doubleBoxDm.setSuffix("   cm")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 5, 1)
        self.argsGranulo['d84bs'] = doubleBoxDm.value() / 100

        self.gridLayout.addWidget(QLabel("Gr = "), 6, 0)
        doubleBoxDm = QDoubleSpinBox()
        doubleBoxDm.setDecimals(2)
        doubleBoxDm.valueChanged.connect(self.grChanged)
        doubleBoxDm.setSuffix("    ")
        doubleBoxDm.setMinimum(0)
        doubleBoxDm.setMaximum(999999.99)
        self.gridLayout.addWidget(doubleBoxDm, 6, 1)
        self.argsGranulo['Gr'] = doubleBoxDm.value()

        self.hLayout.addLayout(self.gridLayout)
        ###

        self.layout.addLayout(self.hLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def nameChanged(self, s):
        self.argsGranulo['name'] = s

    def dmChanged(self, x):
        self.argsGranulo['dm'] = x / 100
    
    def d30Changed(self, x):
        self.argsGranulo['d30'] = x / 100
    
    def d50Changed(self, x):
        self.argsGranulo['d50'] = x / 100
    
    def d90Changed(self, x):
        self.argsGranulo['d90'] = x / 100
    
    def d84tbChanged(self, x):
        self.argsGranulo['d84tb'] = x / 100
    
    def d84bsChanged(self, x):
        self.argsGranulo['d84bs'] = x / 100
    
    def grChanged(self, x):
        self.argsGranulo['Gr'] = x

    def check(self):
        if self.argsGranulo['name'].split() == []:
            QMessageBox.critical(self, "Error : no name for the new granulometry", "Please give a valid name to the granulometry")
            return
        elif self.argsGranulo["name"] in self.parent().getProject().getGranulometryNameList():
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        self.granulometry = Granulometry(self.argsGranulo['name'], self.argsGranulo['dm'], self.argsGranulo['d30'], self.argsGranulo['d50'], self.argsGranulo['d90'], self.argsGranulo['d84tb'], self.argsGranulo['d84bs'], self.argsGranulo['Gr'])
        self.accept()

