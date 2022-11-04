from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class ProfileGranuloTable(QAbstractTableModel):

    def __init__(self, tab):
        super(ProfileGranuloTable, self).__init__()
        self.tab = tab
        self.refreshData()

    def refreshData(self):
        p = self.tab.getProject().profileSelected
        if p == None:
            self.data = pd.DataFrame()
            return
        granuloData = p.granulo
        self.data = pd.DataFrame(granuloData)
        self.data.set_index("x début")
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            
            value = self.data.iloc[index.row(), index.column()]
            if value == None or type(value) == float or type(value) == int:
                return "" if value==None else f"{value:.3f}"
            else:
                return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return self.data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self.data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
         if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])

            if orientation == Qt.Vertical:
                return ""