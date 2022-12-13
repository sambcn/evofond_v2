from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QCheckBox,
    QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class DialogPlotProfileDataOnResults(QDialog):

    def __init__(self, parent):
        super().__init__(parent)


        self.setWindowTitle("Affichage des données d'un profil")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()

        ###
        self.profileList = QComboBox()
        self.profileList.addItems(parent.getProject().getProfileNameList())
        if parent.profileName in parent.getProject().getProfileNameList():
            self.profileList.setCurrentText(parent.profileName)
        self.profileList.currentTextChanged.connect(self.profileChanged)
        self.profileName = self.profileList.currentText()

        self.checkBoxListLayout = QGridLayout()
        self.setCheckBoxes(self.profileList.currentText())
        ###

        self.layout.addWidget(self.profileList)
        self.layout.addLayout(self.checkBoxListLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def profileChanged(self, profileName):
        self.setCheckBoxes(profileName)
        self.profileName = profileName

    def clearCheckBoxListLayout(self):
        for i in reversed(range(self.checkBoxListLayout.count())): 
            self.checkBoxListLayout.itemAt(i).widget().setParent(None)

    def setCheckBoxes(self, profileName):
        self.clearCheckBoxListLayout()
        profile = self.parent().getProject().getProfile(profileName)
        if profile == None:
            return
        data = profile.data
        sameProfile = (profileName == self.parent().profileName)
        self.dataAxis1 = dict()
        self.dataAxis2 = dict()
        self.checkBoxListLayout.addWidget(QLabel("Axe 1 (gauche)"), 0, 0, alignment=Qt.AlignHCenter)
        self.checkBoxListLayout.addWidget(QLabel("Nom de la donnée"), 0, 1, alignment=Qt.AlignHCenter)
        self.checkBoxListLayout.addWidget(QLabel("Axe 2 (droite)"), 0, 2, alignment=Qt.AlignHCenter)

        for i in range(1, data.shape[1]):
            checkBoxAxis1 = QCheckBox("")
            colName = data.columns[i]
            label = QLabel(" ".join(colName.split()))
            checkBoxAxis2 = QCheckBox("")
            if sameProfile:
                checkBoxAxis1.setChecked(colName in self.parent().dataAxis1.keys())
                checkBoxAxis2.setChecked(colName in self.parent().dataAxis2.keys())
            checkBoxAxis1.stateChanged.connect(self.checkBoxConnection(checkBoxAxis1, data, colName, True))
            checkBoxAxis2.stateChanged.connect(self.checkBoxConnection(checkBoxAxis2, data, colName, False))
            self.checkBoxListLayout.addWidget(checkBoxAxis1, i, 0, alignment=Qt.AlignHCenter)
            self.checkBoxListLayout.addWidget(label, i, 1, alignment=Qt.AlignHCenter)
            self.checkBoxListLayout.addWidget(checkBoxAxis2, i, 2, alignment=Qt.AlignHCenter)
            
    def checkBoxConnection(self, checkBox, data, key, axis1):
        def checkBoxStateChanged():
            d = self.dataAxis1 if axis1 else self.dataAxis2
            if checkBox.isChecked():
                subdata = data[~(data[data.columns[0]].isnull()) & ~(data[key].isnull())]
                d[key] = (subdata[subdata.columns[0]], subdata[key])
            else:
                d.pop(key, None)
        return checkBoxStateChanged

