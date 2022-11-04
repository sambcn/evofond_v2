from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
)
from PyQt5.QtGui import QFont, QIcon

class DialogQuestionAnswer(QDialog):

    def __init__(self, parent, question):

        super().__init__(parent)
        self.setWindowTitle("Question")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###
        self.label = QLabel(question)
        self.qline = QLineEdit()
        self.qline.textChanged.connect(self.anwserChanged)
        self.answer = self.qline.text()
        ###

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.qline)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def anwserChanged(self, s):
        self.answer = s