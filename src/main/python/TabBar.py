from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtGui import QFont

from ProjectTab import ProjectTab 
from HydrogramTab import HydrogramTab 
from SedimentogramTab import SedimentogramTab 
from ProfileTab import ProfileTab 
from ModelTab import ModelTab 
from ResultsTab import ResultsTab 

class TabBar(QTabWidget):

    def __init__(self, parent=None):
        super(TabBar, self).__init__(parent=parent)
        
        self.projectTab = ProjectTab(self)
        self.hydrogramtTab = HydrogramTab(self)
        self.sedimentogramTab = SedimentogramTab(self)
        self.profileTab = ProfileTab(self)
        self.modelTab = ModelTab(self)
        self.resultsTab = ResultsTab(self)

        self.insertTab(0, self.projectTab, self.projectTab.icon, self.projectTab.label)
        self.insertTab(1, self.hydrogramtTab, self.hydrogramtTab.icon, self.hydrogramtTab.label)
        self.insertTab(2, self.sedimentogramTab, self.sedimentogramTab.icon, self.sedimentogramTab.label)
        self.insertTab(3, self.profileTab, self.profileTab.icon, self.profileTab.label)
        self.insertTab(4, self.modelTab, self.modelTab.icon, self.modelTab.label)
        self.insertTab(5, self.resultsTab, self.resultsTab.icon, self.resultsTab.label)

        self.tabBarClicked.connect(self.clicked)

        self.setFont(QFont('Arial font', 12))

        return

    def getProject(self):
        return self.projectTab.currentProject

    def refresh(self):
        for i in range(self.count()):
            self.widget(i).refresh()

    def clicked(self, index):
        if index == 0:
            self.projectTab.updateText()

    def getResource(self, path):
        return self.parent().getResource(path)