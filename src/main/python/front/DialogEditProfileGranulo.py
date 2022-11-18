from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import pandas as pd

class DialogEditProfileGranulo(QDialog):

    def __init__(self, parent, profile):
        super().__init__(parent)
        self.profile = profile
        self.newGranulo = profile.granulo.copy()

        self.setWindowTitle("Gestion de la granulométrie du profil")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###
        self.buttonLayout = QHBoxLayout()
        self.addButton = QPushButton(" Ajouter une granulométrie")
        self.addButton.setIcon(QIcon(parent.getResource("images\\add.png")))
        self.addButton.released.connect(self.addButtonReleased)
        self.buttonLayout.addWidget(self.addButton)
        self.removeButton = QPushButton(" Retirer une granulométrie")
        self.removeButton.setIcon(QIcon(parent.getResource("images\\minus.png")))
        self.removeButton.released.connect(self.removeButtonReleased)
        self.buttonLayout.addWidget(self.removeButton)

        self.matrixLayout = QGridLayout()
        self.setMatrixLayout()

        ###

        self.layout.addLayout(self.buttonLayout)
        self.layout.addLayout(self.matrixLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def addButtonReleased(self):
        newLine = pd.DataFrame({self.newGranulo.columns[0]:[None], self.newGranulo.columns[1]:[self.profile.data[self.profile.data.columns[0]].min()], self.newGranulo.columns[2]:[self.profile.data[self.profile.data.columns[0]].max()]})
        self.newGranulo = pd.concat([self.newGranulo, newLine], ignore_index=True)
        self.setMatrixLayout()

    def removeButtonReleased(self):
        if self.newGranulo.shape[0] > 0:
            self.newGranulo = self.newGranulo.drop(self.newGranulo.index[-1])
            self.setMatrixLayout()

    def clearMatrixLayout(self):
        for i in reversed(range(self.matrixLayout.count())): 
            self.matrixLayout.itemAt(i).widget().setParent(None)

    def setMatrixLayout(self):
        self.clearMatrixLayout()
        for i in range(self.newGranulo.shape[0]):
            self.matrixLayout.addWidget(QLabel("Granulométrie : "), i, 0, alignment=Qt.AlignRight)
            granuloList = QComboBox()
            self.setUpGranuloList(granuloList, i, 0)
            self.matrixLayout.addWidget(granuloList, i, 1)

            self.matrixLayout.addWidget(QLabel("x début : "), i, 2,  alignment=Qt.AlignRight)
            doubleBox = QDoubleSpinBox()
            self.setUpDoubleBox(doubleBox, i, 1)
            self.matrixLayout.addWidget(doubleBox, i, 3)

            self.matrixLayout.addWidget(QLabel("x fin : "), i, 4,  alignment=Qt.AlignRight)
            doubleBox = QDoubleSpinBox()
            self.setUpDoubleBox(doubleBox, i, 2)
            self.matrixLayout.addWidget(doubleBox, i, 5)
            

    def setUpGranuloList(self, qlist, i, j, value=None):
        for g in self.parent().getProject().getGranulometryNameList():
            qlist.addItem(g)
        qlist.setCurrentText(self.newGranulo.iloc[i, j] if value==None else value)
        def nameChanged(s):
            self.newGranulo.iloc[i, j] = s
            return
        qlist.currentTextChanged.connect(nameChanged)
        nameChanged(qlist.currentText())
        return

    def setUpDoubleBox(self, doubleBox, i, j, value=None):
        doubleBox.setDecimals(3)
        xmin = self.profile.data[self.profile.data.columns[0]].min()
        xmax = self.profile.data[self.profile.data.columns[0]].max()
        doubleBox.setMinimum(xmin)
        doubleBox.setMaximum(xmax)
        if self.newGranulo.iloc[i, j] != None:
            doubleBox.setValue(self.newGranulo.iloc[i, j] if value==None else value)
        def valChanged(x):
            self.newGranulo.iloc[i, j] = x
            return
        doubleBox.valueChanged.connect(valChanged)
        valChanged(doubleBox.value())
        return

    def check(self):
        xList = self.profile.getAbscissaList()
        if xList != []:
            if min(xList) < self.newGranulo[self.newGranulo.columns[1]].min():
                QMessageBox.critical(self, "Erreur : les abscisses choisies ne recouvrent pas le profil", f"Le plus petit abscisse donné est plus grand que le minimum des abscisses du profile ({self.newGranulo[self.newGranulo.columns[1]].min()} > {min(xList)})")
                return
            if max(xList) > self.newGranulo[self.newGranulo.columns[2]].max():
                QMessageBox.critical(self, "Erreur : les abscisses choisies ne recouvrent pas le profil", f"Le plus grand abscisse donné est plus petit que le maximum des abscisses du profile ({self.newGranulo[self.newGranulo.columns[2]].max()} < {max(xList)})")
                return
        self.accept()

