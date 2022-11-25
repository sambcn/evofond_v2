import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtCore import pyqtSignal, Qt

class MplCanvas(FigureCanvasQTAgg):

    toggle = pyqtSignal()

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle.emit()
