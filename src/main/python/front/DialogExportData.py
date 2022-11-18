from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QVBoxLayout, QListWidget, QStackedLayout, QPushButton, QSlider,
    QHBoxLayout, QWidget, QGridLayout, QLabel, QFileDialog, QMessageBox, QCheckBox, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from utils import time_to_string

import pandas as pd

class DialogExportData(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Export data")
        self.setFont(QFont('Arial font', 12))

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.check)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        ###

        self.hlayout = QHBoxLayout()

        # Available exports list
        self.exportStringList = ["Personnalisé", "Profil maximum", "Profil minimum", "Profil au pic de crue"]
        self.exportList = QListWidget()
        self.exportList.addItems(self.exportStringList)
        self.exportList.currentRowChanged.connect(self.exportChoiceChanged)
        self.hlayout.addWidget(self.exportList)
        
        # One layout for each kind of export
        self.stackedLayout = QStackedLayout()

        # Random export
        self.randomExportDict = dict()
        currentResult = self.parent().currentResult
        qgrid = QGridLayout()
        qgrid.addWidget(QLabel("Export personnalisé\n"), 0, 0)

        self.xData = QComboBox()
        self.xData.addItems(["Abscisse x [m]", "Temps t [s]"])
        self.xData.currentIndexChanged.connect(self.xDataRowChanged)
        qgrid.addWidget(self.xData, 1, 0)
        self.slayout = QStackedLayout()
        
        # abscissa associated data
        vlayout = QVBoxLayout()
        checkBox = QCheckBox("Altitude du fond z [m]")
        checkBox.setChecked(True)
        self.randomExportDict["z"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Altitude du fond inafouillable z_min [m]")
        checkBox.setChecked(True)
        self.randomExportDict["z_min"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Altitude du fond initial z0 [m]")
        checkBox.setChecked(True)
        self.randomExportDict["z0"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Hauteur d'eau h [m]")
        checkBox.setChecked(True)
        self.randomExportDict["h"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Hauteur critique hc [m]")
        checkBox.setChecked(True)
        self.randomExportDict["hc"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Charge H [m]")
        checkBox.setChecked(True)
        self.randomExportDict["H"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Largeur b [m]")
        checkBox.setChecked(True)
        self.randomExportDict["b"] = checkBox
        vlayout.addWidget(checkBox)
        checkBox = QCheckBox("Débit Q [m]")
        checkBox.setChecked(True)
        self.randomExportDict["Q"] = checkBox
        vlayout.addWidget(checkBox)

        vlayout2 = QVBoxLayout()
        timeSliderLabel = QLabel("")
        timeSlider = QSlider(Qt.Horizontal)
        timeSlider.setMaximum(len(currentResult["time"])-1)
        timeSlider.valueChanged.connect(lambda v:timeSliderLabel.setText(f"temps = {time_to_string(currentResult['time'][v])}"))
        self.randomExportDict["timeSlider"] = timeSlider
        vlayout2.addWidget(timeSliderLabel, alignment=Qt.AlignBottom)
        vlayout2.addWidget(timeSlider)

        widget = QWidget()
        widget.setLayout(vlayout2)
        self.slayout.addWidget(widget)

        vlayout2 = QVBoxLayout()
        abscissaSliderLabel = QLabel("")
        abscissaSlider = QSlider(Qt.Horizontal)
        abscissaSlider.setMaximum(len(currentResult["abscissa"])-1)
        abscissaSlider.valueChanged.connect(lambda v:abscissaSliderLabel.setText(f"abscisse = {currentResult['abscissa'][v]}m"))
        self.randomExportDict["abscissaSlider"] = abscissaSlider
        vlayout2.addWidget(abscissaSliderLabel)
        vlayout2.addWidget(abscissaSlider)

        widget = QWidget()
        widget.setLayout(vlayout2)
        self.slayout.addWidget(widget)

        vlayout.addLayout(self.slayout)

        widget = QWidget()
        widget.setLayout(vlayout)
        qgrid.addWidget(widget, 2, 0)
        widget = QWidget()
        widget.setLayout(qgrid)
        self.stackedLayout.addWidget(widget)

        # Max profile
        self.maxProfileDict = dict()
        qgrid = QGridLayout()
        qgrid.addWidget(QLabel("Profil maximum"), 0, 0)

        checkBox = QCheckBox("x")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.maxProfileDict["x"] = checkBox
        qgrid.addWidget(checkBox, 1, 0)
        qgrid.addWidget(QLabel("Abscisse [m]"), 1, 1)
        checkBox = QCheckBox("z_maxi")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.maxProfileDict["z_maxi"] = checkBox
        qgrid.addWidget(checkBox, 2, 0)
        qgrid.addWidget(QLabel("Alitude maximale durant l'évènement [m]"), 2, 1)
        checkBox = QCheckBox("t_maxi")
        checkBox.setChecked(True)
        self.maxProfileDict["t_maxi"] = checkBox
        qgrid.addWidget(checkBox, 3, 0)
        qgrid.addWidget(QLabel("Instant auquel est atteint z_maxi [s]"), 3, 1)
        checkBox = QCheckBox("z_min")
        checkBox.setChecked(True)
        self.maxProfileDict["z_min"] = checkBox
        qgrid.addWidget(checkBox, 4, 0)
        qgrid.addWidget(QLabel("altitude du fond inafouillable [m]"), 4, 1)
        checkBox = QCheckBox("z_0")
        checkBox.setChecked(True)
        self.maxProfileDict["z_0"] = checkBox
        qgrid.addWidget(checkBox, 5, 0)
        qgrid.addWidget(QLabel("altitude du fond initial [m]"), 5, 1)
        checkBox = QCheckBox("b")
        checkBox.setChecked(True)
        self.maxProfileDict["b"] = checkBox
        qgrid.addWidget(checkBox, 6, 0)
        qgrid.addWidget(QLabel("largeur à t_maxi [m]"), 6, 1)

        widget = QWidget()
        widget.setLayout(qgrid)
        self.stackedLayout.addWidget(widget)

        # Min profile

        self.minProfileDict = dict()
        qgrid = QGridLayout()
        qgrid.addWidget(QLabel("Profil minimum"), 0, 0)

        checkBox = QCheckBox("x")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.minProfileDict["x"] = checkBox
        qgrid.addWidget(checkBox, 1, 0)
        qgrid.addWidget(QLabel("Abscisse [m]"), 1, 1)
        checkBox = QCheckBox("z_mini")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.minProfileDict["z_mini"] = checkBox
        qgrid.addWidget(checkBox, 2, 0)
        qgrid.addWidget(QLabel("Alitude minimale durant l'évènement [m]"), 2, 1)
        checkBox = QCheckBox("t_mini")
        checkBox.setChecked(True)
        self.minProfileDict["t_mini"] = checkBox
        qgrid.addWidget(checkBox, 3, 0)
        qgrid.addWidget(QLabel("Instant auquel est atteint z_mini [s]"), 3, 1)
        checkBox = QCheckBox("z_min")
        checkBox.setChecked(True)
        self.minProfileDict["z_min"] = checkBox
        qgrid.addWidget(checkBox, 4, 0)
        qgrid.addWidget(QLabel("altitude du fond inafouillable [m]"), 4, 1)
        checkBox = QCheckBox("z_0")
        checkBox.setChecked(True)
        self.minProfileDict["z_0"] = checkBox
        qgrid.addWidget(checkBox, 5, 0)
        qgrid.addWidget(QLabel("altitude du fond initial [m]"), 5, 1)
        checkBox = QCheckBox("b")
        checkBox.setChecked(True)
        self.minProfileDict["b"] = checkBox
        qgrid.addWidget(checkBox, 6, 0)
        qgrid.addWidget(QLabel("largeur à t_mini [m]"), 6, 1)

        widget = QWidget()
        widget.setLayout(qgrid)
        self.stackedLayout.addWidget(widget)


        # Profile at maximum water discharge 

        self.maxDischargeProfileDict = dict()
        qgrid = QGridLayout()
        qgrid.addWidget(QLabel("Profil au pic de crue"), 0, 0)

        checkBox = QCheckBox("x")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.maxDischargeProfileDict["x"] = checkBox
        qgrid.addWidget(checkBox, 1, 0)
        qgrid.addWidget(QLabel("Abscisse [m]"), 1, 1)
        checkBox = QCheckBox("z")
        checkBox.setChecked(True)
        checkBox.setEnabled(False)
        self.maxDischargeProfileDict["z_mini"] = checkBox
        qgrid.addWidget(checkBox, 2, 0)
        qgrid.addWidget(QLabel("Alitude du fond au pic de crue [m]"), 2, 1)
        checkBox = QCheckBox("z_min")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["z_min"] = checkBox
        qgrid.addWidget(checkBox, 3, 0)
        qgrid.addWidget(QLabel("altitude du fond inafouillable [m]"), 3, 1)
        checkBox = QCheckBox("z_0")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["z_0"] = checkBox
        qgrid.addWidget(checkBox, 4, 0)
        qgrid.addWidget(QLabel("altitude du fond initial [m]"), 4, 1)
        checkBox = QCheckBox("b")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["b"] = checkBox
        qgrid.addWidget(checkBox, 5, 0)
        qgrid.addWidget(QLabel("largeur au pic de crue [m]"), 5, 1)
        checkBox = QCheckBox("h")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["h"] = checkBox
        qgrid.addWidget(checkBox, 6, 0)
        qgrid.addWidget(QLabel("hauteur au pic de crue [m]"), 6, 1)
        checkBox = QCheckBox("hc")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["hc"] = checkBox
        qgrid.addWidget(checkBox, 7, 0)
        qgrid.addWidget(QLabel("hauteur critique au pic de crue [m]"), 7, 1)
        checkBox = QCheckBox("H")
        checkBox.setChecked(True)
        self.maxDischargeProfileDict["H"] = checkBox
        qgrid.addWidget(checkBox, 8, 0)
        qgrid.addWidget(QLabel("charge au pic de crue [m]"), 8, 1)

        widget = QWidget()
        widget.setLayout(qgrid)
        self.stackedLayout.addWidget(widget)

        self.hlayout.addLayout(self.stackedLayout)

        # Export location path
        
        self.path = None
        browseButton = QPushButton(" Parcourir ")
        browseButton.released.connect(self.browseButtonReleased)
        pathLayout = QGridLayout()
        pathLayout.addWidget(QLabel("Fichier d'export : "), 0, 0, alignment=Qt.AlignRight)
        self.pathLabel = QLabel("")
        self.pathLabel.setStyleSheet("border: 1px solid black;padding: 8px; font-family: 'Arial font'; font-size: 14px")
        pathLayout.addWidget(self.pathLabel, 0, 1, alignment=Qt.AlignVCenter)
        pathLayout.addWidget(browseButton, 0, 2, alignment=(Qt.AlignVCenter | Qt.AlignLeft))
        pathWidget = QWidget()
        pathWidget.setFont(QFont('Arial font', 12))
        pathWidget.setLayout(pathLayout)
        
        ###

        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(pathWidget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def exportChoiceChanged(self, i):
        self.stackedLayout.setCurrentIndex(i)

    def browseButtonReleased(self):
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setNameFilter("*.csv")
        dlg.setDefaultSuffix(".csv")
        if dlg.exec():
            self.path = dlg.selectedFiles()[-1]
            self.pathLabel.setText(self.path)

    def xDataRowChanged(self, i):
        self.slayout.setCurrentIndex(i)

    def getProfileDF(self):
        if self.exportList.currentRow() == 0: # maximum profile
            return self.getDF()
        if self.exportList.currentRow() == 1: # maximum profile
            return self.getExtremeProfileDF(maxi=True)
        if self.exportList.currentRow() == 2: # minimum profile
            return self.getExtremeProfileDF(maxi=False)
        if self.exportList.currentRow() == 3: # maximum discharge profile
            return self.getMaxDischargeProfileDF()
        return pd.DataFrame()

    def getDF(self):
        currentResult = self.parent().currentResult
        d = dict()
        isAbscissa = (self.xData.currentIndex() == 0)
        x = currentResult["abscissa"] if isAbscissa else currentResult["time"]
        key = "Abscisse x [m]" if isAbscissa else "Temps t [s]"
        key2 = "Temps t [s]" if isAbscissa else "Abscisse x [m]"
        slideIndex = self.randomExportDict["timeSlider"].value() if isAbscissa else  self.randomExportDict["abscissaSlider"].value()
        d = {key:x}
        if self.randomExportDict["z"].isChecked():
            z = currentResult["bottom_height"]
            data = z[slideIndex] if isAbscissa else [z[i][slideIndex] for i in range(len(x))]
            d["Altitude du fond z [m]"] = data
        if self.randomExportDict["z_min"].isChecked():
            z_min = currentResult["minimal_bottom_height"]
            data = z_min if isAbscissa else [z_min[slideIndex] for i in range(len(x))]
            d["Altitude du fond inafouillable z_min [m]"] = data
        if self.randomExportDict["z0"].isChecked():
            z0 = currentResult["bottom_height"][0]
            data = z0 if isAbscissa else [z0[slideIndex] for i in range(len(x))]
            d["Altitude du fond initial z0 [m]"] = data
        if self.randomExportDict["h"].isChecked():
            h = currentResult["water_depth"]
            data = h[slideIndex] if isAbscissa else [h[i][slideIndex] for i in range(len(x))]
            d["Hauteur d'eau h [m]"] = data
        if self.randomExportDict["hc"].isChecked():
            hc = currentResult["critical_depth"]
            data = hc[slideIndex] if isAbscissa else [hc[i][slideIndex] for i in range(len(x))]
            d["Hauteur critique hc [m]"] = data
        if self.randomExportDict["H"].isChecked():
            H = currentResult["energy"]
            data = H[slideIndex] if isAbscissa else [H[i][slideIndex] for i in range(len(x))]
            d["Charge H [m]"] = data
        if self.randomExportDict["Q"].isChecked():
            Q = currentResult["water_discharge"]
            data = Q[slideIndex] if isAbscissa else [Q[i][slideIndex] for i in range(len(x))]
            d["Débit liquide Q [m3/s]"] = data
        if self.randomExportDict["b"].isChecked():
            b = currentResult["width"]
            data = b[slideIndex] if isAbscissa else [b[i][slideIndex] for i in range(len(x))]
            d["Largeur b [m]"] = data
        d[key2] = currentResult["time"][slideIndex] if isAbscissa else currentResult["abscissa"][slideIndex]
        return pd.DataFrame(d)

    def getExtremeProfileDF(self, maxi):
        result = self.parent().currentResult
        t = result["time"]
        x = result["abscissa"]
        z = result["bottom_height"]
        z_min = result["minimal_bottom_height"]
        b = result["width"]
        z_bis = [[z[j][i] for j in range(len(t))] for i in range(len(x))]
        z_extreme = [max(zi) for zi in z_bis] if maxi else [min(zi) for zi in z_bis]
        index_extreme = [zi.index(ziextreme) for zi, ziextreme in zip(z_bis, z_extreme)]
        if maxi:
            d = {"Abscisse x [m]":x, "Altitude maximum z_maxi [m]":z_extreme}
        else:
            d = {"Abscisse x [m]":x, "Altitude minimum z_mini [m]":z_extreme}
        if self.maxProfileDict["t_maxi"].isChecked():
            d["t_max [s]"] = [t[i] for i in index_extreme]
        if self.maxProfileDict["z_min"].isChecked():
            d["Altitude du fond inafouillable z_min [m]"] = z_min
        if self.maxProfileDict["z_0"].isChecked():
            d["Altitude initiale z_0 [m]"] = z[0] if len(z) > 0 else None
        if self.maxProfileDict["b"].isChecked():
            d["Largeur b [m]"] = [b[index_extreme[i]][i] for i in range(len(x))]
        return pd.DataFrame(d)

    def getMaxDischargeProfileDF(self):
        result = self.parent().currentResult
        t = result["time"]
        x = result["abscissa"]
        z = result["bottom_height"]
        h = result["water_depth"]
        hc = result["critical_depth"]
        H = result["energy"]
        Q = result["water_discharge"]
        z_min = result["minimal_bottom_height"]
        b = result["width"]
        upstreamQ = [Qi[0] for Qi in Q]
        indexQmax = upstreamQ.index(max(upstreamQ))
        d = {"Abscisse x [m]":x, "Altitude du fond z [m]":z[indexQmax]}
        if self.maxDischargeProfileDict["z_min"].isChecked():
            d["Altitude du fond inafouillable z_min [m]"] = z_min
        if self.maxDischargeProfileDict["z_0"].isChecked():
            d["Altitude initiale z_0 [m]"] = z[0] if len(z) > 0 else None
        if self.maxDischargeProfileDict["b"].isChecked():
            d["Largeur b [m]"] = b[indexQmax]
        if self.maxDischargeProfileDict["h"].isChecked():
            d["Hauteur d'eau h [m]"] = h[indexQmax]
        if self.maxDischargeProfileDict["hc"].isChecked():
            d["Hauteur critique hc [m]"] = hc[indexQmax]
        if self.maxDischargeProfileDict["H"].isChecked():
            d["Charge H [m]"] = H[indexQmax]
        return pd.DataFrame(d)
            

    def check(self):
        if self.path == None:
            QMessageBox.critical(self, "Sélectionnez un fichier cible", "Aucun fichier sélectionné pour enregistrer le résultat.")
            return
        df = self.getProfileDF()
        df.to_csv(self.path)
        self.accept()
