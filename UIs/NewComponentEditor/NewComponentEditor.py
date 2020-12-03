from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from .new_component_editor import  Ui_uiNewComponentEditor as ui

class NewComponentEditor(qtw.QWidget, ui):

    submit = qtc.pyqtSignal(object)

    def __init__(self, node):
        """
        Loads the UI window.
        """

        super(NewComponentEditor, self).__init__()
        self.setupUi(self)

        self.manufactureModel = None
        self.statusModel = None
        self.node = node

        self.uiCancelBtn.clicked.connect(self.close)
        self.uiAddBtn.clicked.connect(self.submitNode)

        self._initFiedlds()
        self.show()

    def setManufactureModel(self, manufactureModel):
        self.manufactureModel = manufactureModel
        self.editable.setModel(self.manufactureModel)

    def setStatusModel(self, statusModel):
        self.statusModel = statusModel
        self.uiStatus.setModel(self.statusModel)

    def submitNode(self):
        self.node.addFeatures(**self._gatherData())
        self.submit.emit(self.node)
        self.close()

    def _initFiedlds(self):
        self.uiNumberID.setText(self.node.getFeature('numberID'))
        self.uiName.setText(self.node.getFeature('name'))
        self.uiDescription.setPlainText(self.node.getFeature('description'))
        self.uiType.setText(self.node.getFeature('type'))
        self.editable.setCurrentIndex(0)
        self.noneditable.setText(self.node.getFeature('manufacture'))
        self.uiComment.setPlainText(self.node.getFeature('comment'))
        self.uiPrice.setText(str(self.node.getFeature('price')))
        self.uiSeller.setText(self.node.getFeature('seller'))
        self.uiLink.setPlainText(self.node.getFeature('link'))

        self._changeManufacture()

    def _changeManufacture(self):
        """
        Changes dinamically the manufacture widget. The editable nodes will have a combo box,
        while non-editable nodes will have a read-only line edit.
        """

        editable = self.node.isEditable()

        if editable:
            self.uiManufacture.setCurrentIndex(0)
        else:
            self.uiManufacture.setCurrentIndex(1)

    def _disableWidgets(self):
        pass

    def _gatherData(self):
        data = {
            'name': self.uiName.text(),
            'description': self.uiDescription.toPlainText(),
            'status': self.uiStatus.currentText(),
            'comment': self.uiComment.toPlainText(),
            'price': self.uiPrice.text(),
            'quantity': self.uiQuantity.text(),
            'package': self.uiQuantityPackage.text(),
            'seller': self.uiSeller.text(),
            'link': self.uiLink.toPlainText()
        }

        if self.node.isEditable():
            data['manufacture'] = self.editable.currentText()

        return data
