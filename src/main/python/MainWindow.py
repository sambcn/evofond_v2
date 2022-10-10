from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QHBoxLayout, QStyle, 
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QTabWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from TabBar import TabBar

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.setWindowTitle("Evofond")
        self.setWindowIcon(QIcon("..\\icons\\base\\evofond.jpg"))

        self.tabs = TabBar()

        self.setCentralWidget(self.tabs)
        self.showMaximized()
