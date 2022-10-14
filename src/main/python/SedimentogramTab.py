from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QLabel

from Tab import Tab

class SedimentogramTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Sédimentogramme", tabBar.getResource("images\\stone.png"))

        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(QLabel("Liste des sédimentogrammes : "))
        self.hydrogramList = QListWidget()
        # self.setHydrogramList()        
        # self.hydrogramList.currentTextChanged.connect(self.hydrogramChoiceChanged)
        self.layoutList.addWidget(self.hydrogramList)

        