from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from constants import TYPES_FROM_EDITOR


class ComponentEditor(qtw.QWidget):
    """
    This class is a popup window for components editing. Emits a signal when a new component
    needs to be added.
    """

    submit = qtc.pyqtSignal(dict)

    def __init__(self, manufacture_model, node):
        super(ComponentEditor, self).__init__()

        self.uiManufacture = None

        uic.loadUi('code/resources/UIs/ui_component_editor.ui', self)

        self.manufactures = manufacture_model
        self.currentNode = node

        self.uiCancelButton.clicked.connect(self.close)
        self.uiSubmitButton.clicked.connect(self.onSubmit)

        self.initFields()

    def initFields(self):
        """
        Initializes the fields when a new popup is opened.
        """

        self.uiNumberID.setText(self.currentNode.getFeature('number'))
        self.uiName.setText(self.currentNode.getFeature('title'))
        self.uiDescription.setPlainText(self.currentNode.getFeature('description'))
        self.uiType.setText(self.currentNode.getFeature('type'))
        self.uiComment.setPlainText(self.currentNode.getFeature('comment'))
        self.uiPriceUnit.setText(str(self.currentNode.getFeature('price')))
        self.uiSeller.setText(self.currentNode.getFeature('seller'))
        self.uiLink.setPlainText(self.currentNode.getFeature('link'))

        self.changeManufacture()

        if self.currentNode.getFeature('type') == 'Assembly':
            self.uiQnPContainer.setDisabled(True)

    def changeManufacture(self):
        """
        Changes dinamically the manufacture widget and initializes it's text in every context.
        """

        layout = self.uiManufacture.parentWidget().layout()

        layout.removeWidget(self.uiManufacture)
        self.uiManufacture.close()
        layout.removeRow(2)

        if not self.currentNode.getFeature('manufactureEditable'):
            self.uiManufacture = qtw.QLineEdit()
            self.uiManufacture.setReadOnly(True)
            self.uiManufacture.setText(self.currentNode.getFeature('manufacture'))
        else:
            self.uiManufacture = qtw.QComboBox()
            self.uiManufacture.setModel(self.manufactures)
            self.uiManufacture.setCurrentIndex(0)

        layout.insertRow(2, 'Manufacture', self.uiManufacture)
        layout.update()

    def calcManufacture(self):
        """
        Calculates the corresponding value for the manufacture field.
        """

        if self.currentNode.getFeature('type') == 'Assembly' or self.currentNode.getFeature('type') == 'Placeholder':
            return None
        else:
            return self.uiManufacture.currentText()

    def onSubmit(self):
        """Emits the ComponentTree object with the current data."""

        data = {
            'title': self.uiName.text(),
            'description': self.uiDescription.toPlainText(),
            'type': self.uiType.text(),
            'manufacture': self.calcManufacture(),
            'status': self.uiStatus.currentText(),
            'comment': self.uiComment.toPlainText(),
            'price': self.uiPriceUnit.text(),
            'quantity': self.uiQuantityNeeded.text(),
            'package': self.uiQuantityUnit.text(),
            'seller': self.uiSeller.text(),
            'kit': self.uiKit.currentText(),
            'link': self.uiLink.toPlainText()
        }

        toRemove = []
        for key, value in data.items():
            if not value:
                toRemove.append(key)

        for key in toRemove:
            del data[key]

        self.submit.emit(data)
        self.close()
