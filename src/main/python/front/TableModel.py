from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex

import pandas as pd

class TableModel(QAbstractTableModel):

    def __init__(self, tab, _object):
        """
        
        """
        super(TableModel, self).__init__()
        self.tab = tab
        self.editing = False
        self._object = _object
        lastRow = dict()
        for i in range(_object.data.shape[1]):
            lastRow[_object.data.columns[i]] = [None]
        self.lastRow = pd.DataFrame(lastRow)
        self.backup = self._object.data.copy()

    def flags(self, index):
        if self.editing:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole: 
            try:
                self._object.data.iloc[index.row(),index.column()] = float(value)
                self.tab.plotData()
            except (TypeError, ValueError):
                self._object.data.iloc[index.row(),index.column()] = None
            if index.row() == self.rowCount(index)-1:
                self._object.data = pd.concat([self._object.data, self.lastRow], ignore_index=True)
                self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self._object.data.iloc[index.row(), index.column()]
            return "" if value==None else f"{value:.3f}"

    def rowCount(self, index):
        # The length of the outer list.
        return self._object.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._object.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
         if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._object.data.columns[section])

            if orientation == Qt.Vertical:
                return ""

    def copy(self):
        self._object.data.to_clipboard(index=False)

    def paste(self, index):
        def _paste():
            row = index.row()
            column = index.column()
            clipboard = QApplication.clipboard()
            rows = clipboard.text().split("\n")
            for i, r in enumerate(rows):
                values = r.split("\t")
                for j, val in enumerate(values):
                    self.setData(self.index(row+i, column+j), val, Qt.EditRole)
        return _paste

    def addUpperLineForConnection(self, index):
        def _addUpperLine():
            df = self._object.data
            self._object.data = pd.concat([df.iloc[:index.row()], self.lastRow, df.iloc[index.row():]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addUpperLine

    def addLowerLineForConnection(self, index):
        def _addLowerLine():
            df = self._object.data
            self._object.data = pd.concat([df.iloc[:index.row()+1], self.lastRow, df.iloc[index.row()+1:]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addLowerLine

    def deleteLineForConnection(self, index):
        def _deleteLine():
            if self._object.data.shape[0] <= 1:
                return
            self._object.data = self._object.data.drop(self._object.data.index[index.row()])
            self.layoutChanged.emit()
            self.tab.plotData()
        return _deleteLine

    def changeEditionMode(self):
        self.editing = not(self.editing)
        self._object.data = self._object.data.sort_values(by=[self._object.data.columns[0]])
        self.backup = self._object.data.copy()
        self.tab.plotData()

    def restore(self):
        self._object.data = self.backup
        self.layoutChanged.emit()
        self.tab.updateVarLists()
        self.tab.plotData()
