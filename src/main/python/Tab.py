from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon


class Tab(QWidget):

    def __init__(self, tabBar, label, iconPath):
        super().__init__()
        self.tabBar = tabBar
        self.layout = QHBoxLayout()
        self.label = " " + label
        self.setLayout(self.layout)
        self.icon = QIcon(iconPath)

    def getProject(self):
        return self.tabBar.getProject()

    def refresh(self):
        return
