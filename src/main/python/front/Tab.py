from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon


class Tab(QWidget):

    def __init__(self, tabBar, label, iconPath):
        super(Tab, self).__init__()
        self.tabBar = tabBar
        self.layout = QHBoxLayout()
        self.label = " " + label
        self.setLayout(self.layout)
        self.icon = QIcon(iconPath)

    def getProject(self):
        return self.tabBar.getProject()

    def refresh(self):
        return

    def getResource(self, path):
        return self.tabBar.getResource(path)

    def disableOtherTabs(self):
        for i in range(self.tabBar.count()):
            if self.tabBar.widget(i) != self:
                self.tabBar.setTabEnabled(i, False)

    def enableOtherTabs(self):
        for i in range(self.tabBar.count()):
            if self.tabBar.widget(i) != self:
                self.tabBar.setTabEnabled(i, True)

    def processEvents(self):
        self.tabBar.processEvents()
