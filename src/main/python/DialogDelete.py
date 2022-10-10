from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class DialogDelete(QDialog):

    def __init__(self, object, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Delete confirmation")

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(f"You are about to delete {object}. Are you sure ?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)