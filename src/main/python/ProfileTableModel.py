from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class ProfileTableModel(QAbstractTableModel):

    def __init__(self, tab, profile):
        super(ProfileTableModel, self).__init__()
        self.editing = False
        self.tab = tab
        self.profile = profile
        lastRow = dict()
        for i in range(profile.data.shape[1]):
            lastRow[profile.data.columns[i]] = [None]
        self.lastRow = pd.DataFrame(lastRow)
        self.backup = self.profile.data.copy()

    def flags(self, index):
        if self.editing:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable
        else:
            return Qt.ItemIsSelectable|Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                self.profile.data.iloc[index.row(),index.column()] = float(value)
                self.tab.plotData()
            except (TypeError, ValueError):
                self.profile.data.iloc[index.row(),index.column()] = None
            if index.row() == self.rowCount(index)-1:
                self.profile.data = pd.concat([self.profile.data, self.lastRow], ignore_index=True)
                self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self.profile.data.iloc[index.row(), index.column()]
            return "" if value==None else f"{value:.3f}"

    def rowCount(self, index):
        # The length of the outer list.
        return self.profile.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.profile.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
         if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.profile.data.columns[section])

            if orientation == Qt.Vertical:
                return ""

    def addUpperLineForConnection(self, index):
        def _addUpperLine():
            df = self.profile.data
            self.profile.data = pd.concat([df.iloc[:index.row()], self.lastRow, df.iloc[index.row():]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addUpperLine

    def addLowerLineForConnection(self, index):
        def _addLowerLine():
            df = self.profile.data
            self.profile.data = pd.concat([df.iloc[:index.row()+1], self.lastRow, df.iloc[index.row()+1:]]).reset_index(drop=True)
            self.layoutChanged.emit()
        return _addLowerLine

    def deleteLineForConnection(self, index):
        def _deleteLine():
            if self.profile.data.shape[0] <= 1:
                return
            self.profile.data = self.profile.data.drop(self.profile.data.index[index.row()])
            self.layoutChanged.emit()
            self.tab.plotData()
        return _deleteLine

    def changeEditionMode(self):
        self.editing = not(self.editing)
        self.backup = self.profile.data.copy()

    def restore(self):
        self.profile.data = self.backup
        self.tab.plotData()