from PyQt5.QtWidgets import QTabWidget, QShortcut
from PyQt5.QtGui import QFont, QKeySequence

from front.ProjectTab import ProjectTab 
from front.HydrogramTab import HydrogramTab 
from front.GranulometryTab import GranulometryTab 
from front.SedimentogramTab import SedimentogramTab 
from front.ProfileTab import ProfileTab 
from front.ModelTab import ModelTab 
from front.ResultsTab import ResultsTab 

class TabBar(QTabWidget):

    def __init__(self, parent=None):
        super(TabBar, self).__init__(parent=parent)
        
        self.projectTab = ProjectTab(self)
        self.hydrogramtTab = HydrogramTab(self)
        self.granulometryTab = GranulometryTab(self)
        self.sedimentogramTab = SedimentogramTab(self)
        self.profileTab = ProfileTab(self)
        self.modelTab = ModelTab(self)
        self.resultsTab = ResultsTab(self)

        self.insertTab(0, self.projectTab, self.projectTab.icon, self.projectTab.label)
        self.insertTab(1, self.hydrogramtTab, self.hydrogramtTab.icon, self.hydrogramtTab.label)
        self.insertTab(2, self.granulometryTab, self.granulometryTab.icon, self.granulometryTab.label)
        self.insertTab(3, self.sedimentogramTab, self.sedimentogramTab.icon, self.sedimentogramTab.label)
        self.insertTab(4, self.profileTab, self.profileTab.icon, self.profileTab.label)
        self.insertTab(5, self.modelTab, self.modelTab.icon, self.modelTab.label)
        self.insertTab(6, self.resultsTab, self.resultsTab.icon, self.resultsTab.label)

        self.tabBarClicked.connect(self.clicked)

        self.setFont(QFont('Arial font', 12))

        self.newproject_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.newproject_shortcut.activated.connect(self.projectTab.newProjectButtonReleased)
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_shortcut.activated.connect(self.projectTab.loadProjectButtonReleased)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.projectTab.saveProjectButtonReleased)

        return

    def getProject(self):
        return self.projectTab.currentProject

    def refresh(self):
        for i in range(self.count()):
            self.widget(i).refresh()

    def clicked(self, index):
        if self.widget(index) != None:
            self.widget(index).refresh()
    
    def getResource(self, path):
        return self.parent().getResource(path)

    def processEvents(self):
        self.parent().processEvents()
        