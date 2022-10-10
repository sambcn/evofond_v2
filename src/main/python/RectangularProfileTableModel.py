from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class RectangularProfileTableModel(QAbstractTableModel):

    def __init__(self, tab):
        super(RectangularProfileTableModel, self).__init__()
        self.data = pd.DataFrame({"x [m] \n(abscisse)":[], "z [m] \n(altitude)":[], "z_min [m] \n(altitude minimale)":[], 'b [m] \n(largeur)':[]})
        self.lastRow = pd.DataFrame({"x [m] \n(abscisse)":[None], "z [m] \n(altitude)":[None], "z_min [m] \n(altitude minimale)":[None], 'b [m] \n(largeur)':[None]})
        self.data = pd.concat([self.data, self.lastRow], ignore_index=True)
        self.tab = tab

    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            try:
                self.data.iloc[index.row(),index.column()] = float(value)
                self.tab.plotProfileData()
            except (TypeError, ValueError):
                self.data.iloc[index.row(),index.column()] = None
            if index.row() == self.rowCount(index)-1:
                self.data = pd.concat([self.data, self.lastRow], ignore_index=True)
                self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self.data.iloc[index.row(), index.column()]
            return "" if value==None else f"{value:.3f}"

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