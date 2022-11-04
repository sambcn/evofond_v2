from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont

from front.Model import Model

class DialogNewModel(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("New model")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###

        nameField = QLineEdit()
        nameField.setPlaceholderText("Nom du modèle")
        nameField.textChanged.connect(self.nameChanged)
        self.name = nameField.text()

        ###

        self.layout.addWidget(nameField)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def nameChanged(self, s):
        self.name = s

    def check(self):
        if self.name.split() == []:
            QMessageBox.critical(self, "Error : no name for the new model", "Please give a valid name to the model")
            return
        elif self.name in self.parent().getProject().getModelNameList():
            QMessageBox.critical(self, "Error : name already taken", "This name is already taken, please find another one")
            return
        self.model = Model(self.name)
        self.accept()