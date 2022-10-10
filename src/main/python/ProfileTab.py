import string
from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QStackedLayout, QTableView, QHeaderView, QGridLayout, QWidget, QCheckBox, QLabel

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from Tab import Tab
from RectangularProfileTableModel import RectangularProfileTableModel
from TrapezoidalProfileTableModel import TrapezoidalProfileTableModel
from MplCanvas import MplCanvas, NavigationToolbar

import pandas as pd

class ProfileTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Profil", "..\\icons\\base\\profile.jpg")

        self.paramLayout = QVBoxLayout()
        self.sectionTypeList = QComboBox()
        self.sectionTypeList.addItem(QIcon("..\\icons\\base\\rectangularSection.png"), "Rectangulaire")
        self.sectionTypeList.addItem(QIcon("..\\icons\\base\\trapezoidalSection.png"), "Trapézoïdale")
        self.sectionTypeList.currentIndexChanged.connect(self.sectionTypeListIndexChanged)
        self.paramLayout.addWidget(self.sectionTypeList)

        self.tableLayout = QStackedLayout()
        self.rectangularData = QTableView()
        self.rectangularModel = RectangularProfileTableModel(self)
        self.rectangularData.setModel(self.rectangularModel)
        self.rectangularData.setFont(QFont('Arial font', 10))
        header = self.rectangularData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rectangularData.setHorizontalHeader(header)
        self.trapezoidalData = QTableView()
        self.trapezoidalModel = TrapezoidalProfileTableModel(self)
        self.trapezoidalData.setModel(self.trapezoidalModel)
        self.trapezoidalData.setFont(QFont('Arial font', 10))
        header = self.trapezoidalData.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.trapezoidalData.setHorizontalHeader(header)
        self.tableLayout.addWidget(self.rectangularData)
        self.tableLayout.addWidget(self.trapezoidalData)

        self.plotLayout = QVBoxLayout()
        self.plotLayout.addWidget(QLabel("Données à tracer : "), alignment=Qt.AlignTop)
        self.plotOptionsLayout = QStackedLayout()
        self.rectangularPlotOptionsLayout = QGridLayout()
        self.rectangularCheckBox1 = QCheckBox("z")
        self.rectangularCheckBox1.stateChanged.connect(self.plotProfileData)
        self.rectangularPlotOptionsLayout.addWidget(self.rectangularCheckBox1, 0, 0, alignment=Qt.AlignTop)
        self.rectangularCheckBox2 = QCheckBox("z_min")
        self.rectangularCheckBox2.stateChanged.connect(self.plotProfileData)
        self.rectangularPlotOptionsLayout.addWidget(self.rectangularCheckBox2, 1, 0, alignment=Qt.AlignTop)
        self.rectangularCheckBox3 = QCheckBox("b")
        self.rectangularCheckBox3.stateChanged.connect(self.plotProfileData)
        self.rectangularPlotOptionsLayout.addWidget(self.rectangularCheckBox3, 2, 0, alignment=Qt.AlignTop)
        self.rectangularPlotOptionsWidget = QWidget()
        self.rectangularPlotOptionsWidget.setLayout(self.rectangularPlotOptionsLayout)
        self.plotOptionsLayout.addWidget(self.rectangularPlotOptionsWidget)

        self.trapezoidalPlotOptionsLayout = QGridLayout()
        self.trapezoidalCheckBox1 = QCheckBox("z")
        self.trapezoidalCheckBox1.stateChanged.connect(self.plotProfileData)
        self.trapezoidalPlotOptionsLayout.addWidget(self.trapezoidalCheckBox1, 0, 0, alignment=Qt.AlignTop)
        self.trapezoidalCheckBox2 = QCheckBox("z_min")
        self.trapezoidalCheckBox2.stateChanged.connect(self.plotProfileData)
        self.trapezoidalPlotOptionsLayout.addWidget(self.trapezoidalCheckBox2, 1, 0, alignment=Qt.AlignTop)
        self.trapezoidalCheckBox3 = QCheckBox("b0")
        self.trapezoidalCheckBox3.stateChanged.connect(self.plotProfileData)
        self.trapezoidalPlotOptionsLayout.addWidget(self.trapezoidalCheckBox3, 2, 0, alignment=Qt.AlignTop)
        self.trapezoidalCheckBox4 = QCheckBox("b0_min")
        self.trapezoidalCheckBox4.stateChanged.connect(self.plotProfileData)
        self.trapezoidalPlotOptionsLayout.addWidget(self.trapezoidalCheckBox4, 3, 0, alignment=Qt.AlignTop)
        self.trapezoidalPlotOptionsWidget = QWidget()
        self.trapezoidalPlotOptionsWidget.setLayout(self.trapezoidalPlotOptionsLayout)
        self.plotOptionsLayout.addWidget(self.trapezoidalPlotOptionsWidget)

        self.plotLayout.addLayout(self.plotOptionsLayout)
        self.sc = MplCanvas()
        self.plotLayout.addWidget(self.sc, stretch=60)
        self.toolbar = NavigationToolbar(self.sc, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotProfileData()
        
        self.layout.addLayout(self.paramLayout)
        self.layout.addLayout(self.tableLayout)
        self.layout.addLayout(self.plotLayout)

    def sectionTypeListIndexChanged(self, i):
        self.tableLayout.setCurrentIndex(i)
        self.plotOptionsLayout.setCurrentIndex(i)
        self.plotProfileData()
        return

    def plotProfileData(self):
        a = self.sc.axes
        for twinAx in a.get_shared_x_axes().get_siblings(a):
            twinAx.lines.clear()
            if twinAx != a:
                twinAx.remove()
        atLeastOneCurve = False
        lines = []
        if self.sectionTypeList.currentIndex() == 0:
            df = self.rectangularModel.data
            if self.rectangularCheckBox1.isChecked(): # z
                atLeastOneCurve = True
                sub_df = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[1]].isnull())]
                lines += self.sc.axes.plot(sub_df[df.columns[0]], sub_df[df.columns[1]], label="z", color="blue")
            if self.rectangularCheckBox2.isChecked(): # z_min
                atLeastOneCurve = True
                sub_df = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[2]].isnull())]
                lines += self.sc.axes.plot(sub_df[df.columns[0]], sub_df[df.columns[2]], label="z_min", color="red", linestyle="dashed")
            if self.rectangularCheckBox3.isChecked(): # b
                twinAxeList = a.get_shared_x_axes().get_siblings(a)
                twinAxeList.pop(twinAxeList.index(a))
                if twinAxeList == []:
                    twinAxe = a.twinx()
                else:
                    twinAxe = twinAxeList[0]
                atLeastOneCurve = True
                sub_df = df[~(df[df.columns[0]].isnull()) & ~(df[df.columns[3]].isnull())]
                lines += twinAxe.plot(sub_df[df.columns[0]], sub_df[df.columns[3]], label="b", color="grey", linestyle="dashdot")

        if atLeastOneCurve: 
            self.sc.axes.legend(lines, [l.get_label() for l in lines])
        self.sc.draw()
        
        return