from PyQt5.QtCore import QAbstractTableModel, Qt

import pandas as pd

class GranuloTableModel(QAbstractTableModel):

    def __init__(self, tab):
        super(GranuloTableModel, self).__init__()
        self.tab = tab
        self.refreshData()

    def refreshData(self):
        granuloList = self.tab.getProject().granulometryList
        name = []
        dm = []
        d30 = []
        d50 = []
        d90 = []
        d84tb = []
        d84bs = []
        Gr = []
        for g in granuloList:
            name.append(g.name)
            dm.append(g.dm)
            d30.append(g.d30)
            d50.append(g.d50)
            d90.append(g.d90)
            d84tb.append(g.d84tb)
            d84bs.append(g.d84bs)
            Gr.append(g.Gr)
        self.data = pd.DataFrame({"name":name, "dm":dm, "d30":d30, "d50":d50, "d90":d90, "d84tb":d84tb, "d84bs":d84bs, "Gr":Gr})
        self.data.set_index("name")
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