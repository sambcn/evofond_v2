from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLineEdit, QLabel, QPlainTextEdit
from PyQt5.QtCore import Qt

class DialogEditProject(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowTitle("Modification projet")

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QGridLayout()

        self.projet = parent.getProject()
        self.args = {"name":self.projet.name, "author":self.projet.author, "description":self.projet.description}
        
        label = QLabel("Nom du projet : ")
        line = QLineEdit()
        line.textChanged.connect(self.nameChanged)
        line.setPlaceholderText("Entrez le nom du projet")   
        line.setText(self.args["name"])     
        self.layout.addWidget(label, 0, 0, alignment=(Qt.AlignTop | Qt.AlignRight))
        self.layout.addWidget(line, 0, 1)

        label = QLabel("Nom du créateur : ")
        line = QLineEdit()
        line.textChanged.connect(self.authorChanged)
        line.setPlaceholderText("Entrez le nom du créateur")       
        line.setText(self.args["author"]) 
        self.layout.addWidget(label, 1, 0, alignment=(Qt.AlignTop | Qt.AlignRight))
        self.layout.addWidget(line, 1, 1)

        label = QLabel("Description : ")
        self.descriptionBloc = QPlainTextEdit()
        self.descriptionBloc.textChanged.connect(self.descriptionChanged)
        self.descriptionBloc.setPlaceholderText("Entrez la description du projet")        
        self.descriptionBloc.setPlainText(self.args["description"])
        self.layout.addWidget(label, 2, 0, alignment=(Qt.AlignTop | Qt.AlignRight))
        self.layout.addWidget(self.descriptionBloc, 2, 1)


        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def nameChanged(self, s):
        self.args["name"] = s

    def authorChanged(self, s):
        self.args["author"] = s

    def descriptionChanged(self):
        self.args["description"] = self.descriptionBloc.toPlainText()                 