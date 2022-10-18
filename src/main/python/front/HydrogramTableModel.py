from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class HydrogramTableModel(QAbstractTableModel):

    def __init__(self, tab, hydrogram):
        super(HydrogramTableModel, self).__init__()
        self.tab = tab
        self.editing = False
        self.hydrogram = hydrogram
        lastRow = dict()
        for i in range(hydrogram.data.shape[1]):
            lastRow[hydrogram.data.columns[i]] = [None]
        self.lastRow = pd.DataFrame(lastRow)
        self.backup = self.hydrogram.data.copy()

    def flags(self, index):
        if self.editing:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole: 
            try:
                self.hydrogram.data.iloc[index.row(),index.column()] = float(value)
                self.tab.plotData()
            except (TypeError, ValueError):
                self.hydrogram.data.iloc[index.row(),index.column()] = None
            if index.row() == self.rowCount(index)-1:
                self.hydrogram.data = pd.concat([self.hydrogram.data, self.lastRow], ignore_index=True)
                self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self.hydrogram.data.iloc[index.row(), index.column()]
            return "" if value==None else f"{value:.3f}"

    def rowCount(self, index):
        # The length of the outer list.
        return self.hydrogram.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.hydrogram.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
         if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.hydrogram.data.columns[section])

            if orientation == Qt.Vertical:
                return ""

    def addUpperLineForConnection(self, index):
        def _addUpperLine():
            df = self.hydrogram.data
            self.hydrogram.data = pd.concat([df.iloc[:index.row()], self.lastRow, df.iloc[index.row():]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addUpperLine

    def addLowerLineForConnection(self, index):
        def _addLowerLine():
            df = self.hydrogram.data
            self.hydrogram.data = pd.concat([df.iloc[:index.row()+1], self.lastRow, df.iloc[index.row()+1:]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addLowerLine

    def deleteLineForConnection(self, index):
        def _deleteLine():
            if self.hydrogram.data.shape[0] <= 1:
                return
            self.hydrogram.data = self.hydrogram.data.drop(self.hydrogram.data.index[index.row()])
            self.layoutChanged.emit()
            self.tab.plotData()
        return _deleteLine

    def changeEditionMode(self):
        self.editing = not(self.editing)
        self.backup = self.hydrogram.data.copy()

    def restore(self):
        self.hydrogram.data = self.backup
        self.tab.plotData()


    