from PyQt5.QtWidgets import (
    QMainWindow
)
from PyQt5.QtGui import QIcon

from front.TabBar import TabBar

class MainWindow(QMainWindow):

    def __init__(self, appctxt, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.appctxt = appctxt

        self.setWindowTitle("Evofond")
        self.setWindowIcon(QIcon(self.getResource("images\\evofond.jpg")))

        self.tabs = TabBar(parent=self)

        self.setCentralWidget(self.tabs)
        self.showMaximized()

    def getResource(self, path):
        return self.appctxt.get_resource(path)

    def closeEvent(self, event):
        # do stuff
        if not(self.tabs.projectTab.leavingProjectCheck()):
            event.ignore()
        elif not(self.tabs.resultsTab.leavingCheck()):
            event.ignore()
        else:
            event.accept() # let the window close

    def processEvents(self):
        self.appctxt.app.processEvents()