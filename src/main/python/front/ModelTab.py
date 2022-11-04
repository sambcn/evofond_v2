from ast import If
from ctypes import alignment
from PyQt5.QtWidgets import (
    QListWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QComboBox, QWidget, QListWidgetItem, QCheckBox, QDoubleSpinBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from front.Tab import Tab
from front.DialogDelete import DialogDelete
from front.DialogNewModel import DialogNewModel
from utils import AVAILABLE_HYDRAULIC_MODEL, AVAILABLE_FRICTION_LAW, AVAILABLE_LIMITS, SEDIMENT_TRANSPORT_LAW_DICT

class ModelTab(Tab):
    
    def __init__(self, tabBar):
        super().__init__(tabBar, "Modèle", tabBar.getResource("images\\form.jpg"))
        
        self.listLayout = QVBoxLayout()
        self.modelList = QListWidget()
        self.modelList.currentTextChanged.connect(self.modelChoiceChanged)
        self.setModelList()
        
        self.binWidget = QPushButton(" DELETE")
        self.binWidget.setIcon(QIcon(self.getResource("images\\trash.png")))
        self.binWidget.released.connect(self.deleteButtonReleased)
        self.copyWidget = QPushButton(" COPY")
        self.copyWidget.setIcon(QIcon(self.getResource("images\\copy.png")))
        self.copyWidget.released.connect(self.copyButtonReleased)
        self.addWidget = QPushButton(" NEW")
        self.addWidget.setIcon(QIcon(self.getResource("images\\add.png")))
        self.addWidget.released.connect(self.newButtonReleased)

        self.listLayout.addWidget(QLabel("Liste des modèles : "))
        self.listLayout.addWidget(self.modelList)
        self.listLayout.addWidget(self.addWidget)
        self.listLayout.addWidget(self.copyWidget)
        self.listLayout.addWidget(self.binWidget)

        self.modelLayout = QGridLayout()

        # Refresh button
        self.refreshWidget = QPushButton(" Rafraîchir les listes")
        self.refreshWidget.setIcon(QIcon(self.getResource("images\\refresh.png")))
        self.refreshWidget.released.connect(self.refresh)
        self.modelLayout.addWidget(self.refreshWidget, 0, 0, alignment=Qt.AlignHCenter)

        # Hydrogram
        self.modelLayout.addWidget(QLabel("Hydrogramme : "), 1, 0, alignment=Qt.AlignRight)
        self.hydrogramComboBox = QComboBox()
        self.hydrogramComboBox.currentTextChanged.connect(self.hydrogramChanged)
        self.modelLayout.addWidget(self.hydrogramComboBox, 1, 1)

        # Sedimento
        self.modelLayout.addWidget(QLabel("Sédimentogramme : "), 2, 0, alignment=Qt.AlignRight)
        self.sedimentogramComboBox = QComboBox()
        self.sedimentogramComboBox.currentTextChanged.connect(self.sedimentogramChanged)
        self.modelLayout.addWidget(self.sedimentogramComboBox, 2, 1)

        # Profil
        self.modelLayout.addWidget(QLabel("Profil : "), 3, 0, alignment=Qt.AlignRight)
        self.profileComboBox = QComboBox()
        self.profileComboBox.currentTextChanged.connect(self.profileChanged)
        self.modelLayout.addWidget(self.profileComboBox, 3, 1)

        # Sediment transport law
        self.modelLayout.addWidget(QLabel("Loi de transport solide : "), 4, 0, alignment=Qt.AlignRight)
        self.sedimentTransportLawComboBox = QComboBox()
        self.sedimentTransportLawComboBox.currentTextChanged.connect(self.sedimentTransportLawChanged)
        self.modelLayout.addWidget(self.sedimentTransportLawComboBox, 4, 1)

        # Interpolation
        self.modelLayout.addWidget(QLabel("Interpolation "), 5, 0, alignment=Qt.AlignRight)
        self.interpolationCheckBox = QCheckBox()
        self.interpolationCheckBox.stateChanged.connect(self.interpolationChanged)
        self.modelLayout.addWidget(self.interpolationCheckBox, 5, 1)
        self.interpolationStepLabel = QLabel("Pas d'interpolation : ")
        self.interpolationStepLabel.setVisible(self.interpolationCheckBox.isChecked())
        self.interpolationStepDoubleSpinBox = QDoubleSpinBox()
        self.interpolationStepDoubleSpinBox.setSuffix(" m")
        self.interpolationStepDoubleSpinBox.valueChanged.connect(self.interpolationStepChanged)
        self.interpolationStepDoubleSpinBox.setVisible(self.interpolationCheckBox.isChecked())
        self.modelLayout.addWidget(self.interpolationStepLabel, 6, 0, alignment=Qt.AlignRight)
        self.modelLayout.addWidget(self.interpolationStepDoubleSpinBox, 6, 1)

        # Hydraulic model
        self.modelLayout.addWidget(QLabel("Modèle hydraulique :"), 7, 0, alignment=Qt.AlignRight)
        self.hydraulicModelComboBox = QComboBox()
        for m in AVAILABLE_HYDRAULIC_MODEL:
            self.hydraulicModelComboBox.addItem(m)
        self.hydraulicModelComboBox.currentTextChanged.connect(self.hydraulicModelChanged)
        self.modelLayout.addWidget(self.hydraulicModelComboBox, 7, 1)
        self.frictionLawLabel = QLabel("Loi de frottement :")
        self.frictionLawComboBox = QComboBox()
        for f in AVAILABLE_FRICTION_LAW:
            self.frictionLawComboBox.addItem(f)
        self.frictionLawLabel.setVisible(False)
        self.frictionLawComboBox.setVisible(False)
        self.frictionLawComboBox.currentTextChanged.connect(self.frictionLawChanged)
        self.modelLayout.addWidget(self.frictionLawLabel, 8, 0, alignment=Qt.AlignRight)
        self.modelLayout.addWidget(self.frictionLawComboBox, 8, 1)

        # Boundary conditions
        self.upstreamConditionLabel = QLabel("Condition amont :")
        self.modelLayout.addWidget(self.upstreamConditionLabel, 9, 0)
        self.upstreamConditionLabel.setVisible(False)
        self.downstreamConditionLabel = QLabel("Condition avale :")
        self.modelLayout.addWidget(self.downstreamConditionLabel, 11, 0)
        self.downstreamConditionLabel.setVisible(False)
        self.upstreamConditionComboBox = QComboBox()
        self.upstreamConditionComboBox.currentIndexChanged.connect(self.upstreamConditionChanged)
        self.upstreamConditionComboBox.setVisible(False)
        self.downstreamConditionComboBox = QComboBox()
        self.downstreamConditionComboBox.currentIndexChanged.connect(self.downstreamConditionChanged)
        self.downstreamConditionComboBox.setVisible(False)
        self.upstreamLabel = QLabel("hauteur d'eau amont : ")
        self.upstreamDoubleSpinBox = QDoubleSpinBox()
        self.upstreamDoubleSpinBox.valueChanged.connect(self.upstreamValueChanged)
        self.upstreamDoubleSpinBox.setSuffix(" m")
        self.downstreamLabel = QLabel("hauteur d'eau avale : ")
        self.downstreamDoubleSpinBox = QDoubleSpinBox()
        self.downstreamDoubleSpinBox.valueChanged.connect(self.downstreamValueChanged)       
        self.downstreamDoubleSpinBox.setSuffix(" m")
        for l in AVAILABLE_LIMITS:
            self.upstreamConditionComboBox.addItem(l)
            self.downstreamConditionComboBox.addItem(l)
        self.modelLayout.addWidget(self.upstreamConditionComboBox, 9, 1)
        self.modelLayout.addWidget(self.upstreamLabel, 10, 0)
        self.modelLayout.addWidget(self.upstreamDoubleSpinBox, 10, 1)
        self.modelLayout.addWidget(self.downstreamConditionComboBox, 11, 1)
        self.modelLayout.addWidget(self.downstreamLabel, 12, 0)
        self.modelLayout.addWidget(self.downstreamDoubleSpinBox, 12, 1)


        # State
        self.stateLabel = QLabel()
        self.stateLabel.setStyleSheet('color: red; font-style: Arial font; font-size: 12pt ')        
        self.modelLayout.addWidget(self.stateLabel, 100, 0)

        self.modelWidget = QWidget()
        self.modelWidget.setLayout(self.modelLayout)
        self.setModelLayout(self.getProject().modelSelected)

        self.layout.addLayout(self.listLayout)
        self.layout.addWidget(self.modelWidget, stretch=100)

    def deleteButtonReleased(self):
        m = self.getProject().modelSelected
        if m == None:
            return
        dlg = DialogDelete(m.name, parent=self)
        if dlg.exec():
            self.getProject().deleteModel(m)
            self.modelList.takeItem(self.modelList.currentRow())
            self.setModelLayout(self.getProject().modelSelected)
        return

    def copyButtonReleased(self):
        m = self.getProject().modelSelected
        if m == None:
            return
        newName = m.name + " (1)"
        i = 1
        while newName in self.getProject().getModelNameList():
            i += 1
            newName = m.name + f" ({i})"
        mCopy = m.copy(newName)
        self.getProject().addModel(mCopy)
        item = QListWidgetItem(mCopy.name)
        self.modelList.addItem(item)
        return

    def newButtonReleased(self):
        dlg = DialogNewModel(parent=self)
        if dlg.exec():
            p = self.getProject()
            p.addModel(dlg.model)
            p.setModelSelected(dlg.model.name)
            item = QListWidgetItem(dlg.model.name)
            self.modelList.addItem(item)
            self.modelList.setCurrentItem(item)
            self.setModelLayout(self.getProject().modelSelected)

    def hydrogramChanged(self, s):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.hydrogram = s
            self.updateText()

    def sedimentogramChanged(self, s):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.sedimentogram = s
            self.updateText()

    def profileChanged(self, s):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.profile = s
            self.updateText()

    def sedimentTransportLawChanged(self, s):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.sedimentTransportLaw = s
            self.updateText()

    def interpolationChanged(self):
        self.interpolationStepLabel.setVisible(self.interpolationCheckBox.isChecked())
        self.interpolationStepDoubleSpinBox.setVisible(self.interpolationCheckBox.isChecked())
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.interpolation = self.interpolationCheckBox.isChecked()
            self.getProject().modelSelected.dx = self.interpolationStepDoubleSpinBox.value()
            self.updateText()
            
    def interpolationStepChanged(self, v):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.dx = v
            self.updateText()

    def hydraulicModelChanged(self, s):
        self.frictionLawLabel.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        self.frictionLawComboBox.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        self.upstreamConditionLabel.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        self.downstreamConditionLabel.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        self.upstreamConditionComboBox.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        self.downstreamConditionComboBox.setVisible(s==AVAILABLE_HYDRAULIC_MODEL[1])
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.hydroModel = s
    
    def frictionLawChanged(self, s):
        if self.getProject().modelSelected != None:
            self.getProject().modelSelected.frictionLaw = s

    def upstreamConditionChanged(self, i):
        if i == 0:
            self.upstreamLabel.setVisible(True)
            self.upstreamDoubleSpinBox.setVisible(True)
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.upstreamCondition = self.upstreamDoubleSpinBox.value()
                self.updateText()
        else:
            self.upstreamLabel.setVisible(False)
            self.upstreamDoubleSpinBox.setVisible(False)
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.upstreamCondition = AVAILABLE_LIMITS[i]

    def downstreamConditionChanged(self, i):
        if i == 0:
            self.downstreamLabel.setVisible(True)
            self.downstreamDoubleSpinBox.setVisible(True)
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.downstreamCondition = self.downstreamDoubleSpinBox.value()
                self.updateText()
        else:
            self.downstreamLabel.setVisible(False)
            self.downstreamDoubleSpinBox.setVisible(False)
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.downstreamCondition = AVAILABLE_LIMITS[i]

    def upstreamValueChanged(self, v):
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.upstreamCondition = self.upstreamDoubleSpinBox.value()

    def downstreamValueChanged(self, v):
            if self.getProject().modelSelected != None:
                self.getProject().modelSelected.downstreamCondition = self.downstreamDoubleSpinBox.value()

    def modelChoiceChanged(self, s):
        self.setModelLayout(self.getProject().getModel(s))
        
    def setModelList(self):
        self.modelList.clear()
        for i, m in enumerate(self.getProject().modelList):
            item = QListWidgetItem(m.name)
            self.modelList.addItem(item)
            if i == self.getProject().modelSelectedIndex:
                self.modelList.setCurrentItem(item)
        return

    def refresh(self):
        self.setModelList()
        return

    def makeModelLayoutBlank(self):
        self.hydrogramComboBox.clear()
        self.sedimentogramComboBox.clear()
        self.profileComboBox.clear()
        self.sedimentTransportLawComboBox.clear()
        self.interpolationCheckBox.setChecked(False)
        self.interpolationStepDoubleSpinBox.setValue(10)
        self.frictionLawComboBox.setCurrentIndex(0)
        self.upstreamConditionComboBox.setCurrentIndex(1)
        self.upstreamDoubleSpinBox.setValue(1)
        self.downstreamConditionComboBox.setCurrentIndex(1)
        self.downstreamDoubleSpinBox.setValue(1)

    def updateText(self):
        p = self.getProject()
        if p.modelSelected != None:
            self.stateLabel.setText(p.modelSelected.getStringState(p))

    def setModelLayout(self, model):
        if self.getProject() == None:
            return
        if model == None:
            self.modelWidget.setVisible(False)
            return
        self.getProject().setNoModelSelected() # VERY IMPORTANT TO ALLOW MODIFICATION WITHOUT CHANGING THE PREVIOUS MODEL WITH WIDGETS CONNECTIONS
        self.modelWidget.setVisible(True)
        self.makeModelLayoutBlank()
        p = self.getProject()
        model

        nameList = p.getHydrogramNameList()
        index = p.hydrogramSelectedIndex
        self.hydrogramComboBox.addItems(nameList)
        if model.hydrogram in nameList:
            self.hydrogramComboBox.setCurrentText(model.hydrogram)
        else:
            self.hydrogramComboBox.setCurrentText(nameList[index] if index!=None else (nameList[0] if nameList != [] else None))
            model.hydrogram = self.hydrogramComboBox.currentText()

        nameList = p.getSedimentogramNameList()
        index = p.sedimentogramSelectedIndex
        self.sedimentogramComboBox.addItems(nameList)
        if model.sedimentogram in p.getSedimentogramNameList():
            self.sedimentogramComboBox.setCurrentText(model.sedimentogram)
        else:
            self.sedimentogramComboBox.setCurrentText(nameList[index] if index!=None else (nameList[0] if nameList != [] else None))
            model.sedimentogram = self.sedimentogramComboBox.currentText()

        nameList = p.getProfileNameList()
        index = p.profileSelectedIndex
        self.profileComboBox.addItems(nameList)
        if model.profile in p.getProfileNameList():
            self.profileComboBox.setCurrentText(model.profile)
        else:
            self.profileComboBox.setCurrentText(nameList[index] if index!=None else (nameList[0] if nameList != [] else None))
            model.profile = self.profileComboBox.currentText()

        self.sedimentTransportLawComboBox.addItems(SEDIMENT_TRANSPORT_LAW_DICT.keys())
        if model.sedimentTransportLaw != None:
            self.sedimentTransportLawComboBox.setCurrentText(model.sedimentTransportLaw)
        else:
            model.sedimentTransportLaw = self.sedimentTransportLawComboBox.currentText()

        self.interpolationCheckBox.setChecked(model.interpolation)
        if model.dx != None:
            self.interpolationStepDoubleSpinBox.setValue(model.dx)
        
        if model.hydroModel in AVAILABLE_HYDRAULIC_MODEL:
            self.hydraulicModelComboBox.setCurrentText(model.hydroModel)
        else:
            self.hydraulicModelComboBox.setCurrentText(AVAILABLE_HYDRAULIC_MODEL[0])
            model.hydroModel = AVAILABLE_HYDRAULIC_MODEL[0]

        if model.frictionLaw != None:
            self.frictionLawComboBox.setCurrentText(model.frictionLaw)
        else:
            model.frictionLaw = self.frictionLawComboBox.currentText()

        if model.upstreamCondition != None:
            if type(model.upstreamCondition) == str:
                self.upstreamConditionComboBox.setCurrentText(model.upstreamCondition)
            else:
                self.upstreamConditionComboBox.setCurrentIndex(0)
                self.upstreamDoubleSpinBox.setValue(model.upstreamCondition)
        else:
            model.upstreamCondition = self.upstreamConditionComboBox.currentText()

        if model.downstreamCondition != None:
            if type(model.downstreamCondition) == str:
                self.downstreamConditionComboBox.setCurrentText(model.downstreamCondition)
            else:
                self.downstreamConditionComboBox.setCurrentIndex(0)
                self.downstreamDoubleSpinBox.setValue(model.downstreamCondition)
        else:
            model.downstreamCondition = self.downstreamConditionComboBox.currentText()

        p.setModelSelected(model.name)
        self.updateText()
        return


       
