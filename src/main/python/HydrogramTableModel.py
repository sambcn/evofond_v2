from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class HydrogramTableModel(QAbstractTableModel):

    def __init__(self, hydrogram):
        super(HydrogramTableModel, self).__init__()
        self.hydrogram = hydrogram
        if hydrogram == None:
            self.data = pd.DataFrame({'t (s)':[], 'Q (m3/s)':[]})
        else:
            self.data = hydrogram.data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self.data.iloc[index.row(), index.column()]
            return f"{value:.3f}"

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