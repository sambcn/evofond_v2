from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QHBoxLayout, QLineEdit, QGridLayout, QLabel, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtGui import QFont

class DialogExportData(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Export data")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###


        
        ###

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


