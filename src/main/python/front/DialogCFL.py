from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QDoubleSpinBox
from PyQt5.QtGui import QFont

class DialogCFL(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Arial font', 12))

        self.setWindowTitle("Courant number modification")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.currentCfl = self.parent().getProject().modelSelected.cfl
        message = QLabel(f"Attention, vous allez modifier le nombre de courant pour ce modèle.\nPour rappel, prendre c>1 implique des accélérations notables du temps de calcul mais les résultats obtenus peuvent être instables.\nIl est recommandé de garder c=1, ou d'augmenter jusqu'à c=4 dans les cas où l'on souhaite un résultat rapide pour le régime varié.")
        self.doubleBox = QDoubleSpinBox()
        self.doubleBox.setValue(self.currentCfl)
        self.doubleBox.setDecimals(1)
        self.doubleBox.setMinimum(1)
        self.doubleBox.setMaximum(8)
        self.doubleBox.valueChanged.connect(self.cflChanged)

        self.layout.addWidget(self.doubleBox)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def cflChanged(self, v):
        self.currentCfl = v