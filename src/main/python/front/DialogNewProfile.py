from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QComboBox, QWidget, QDoubleSpinBox, QGridLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont

class DialogNewProfile(QDialog):

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("New profile")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        ###

        self.argsLayout = QGridLayout()
        self.profileArgs = dict()

        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom du profile")
        nameField.textChanged.connect(self.nameChanged)
        self.profileArgs["name"] = nameField.text()
        self.argsLayout.addWidget(nameField, 0, 0)

        typeSelection = QComboBox()
        typeSelection.addItem(QIcon(self.parent().getResource("images\\rectangularSection.png")), "Rectangular")
        typeSelection.addItem(QIcon(self.parent().getResource("images\\trapezoidalSection.png")), "Trapezoidal")
        typeSelection.currentTextChanged.connect(self.typeChanged)
        self.profileArgs["type"] = typeSelection.currentText()
        self.argsLayout.addWidget(typeSelection, 1, 0)

        ###
        self.layout.addLayout(self.argsLayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def nameChanged(self, s):
        self.profileArgs["name"] = s
        return

    def typeChanged(self, s):
        self.profileArgs["type"] = s
        return

    def check(self):
        p = self.parent().getProject()
        if self.profileArgs["name"] == "":
            QMessageBox.critical(self, "Error : no name for the new profile", "Please give a valid name to the profile")
            return
        if self.profileArgs["name"] in [prof.name for prof in p.profileList]:
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        self.accept()