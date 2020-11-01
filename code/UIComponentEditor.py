from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

from BaseNode import BaseNode


class ComponentEditor(qtw.QWidget):
    """
    This class is a popup window for components editing. Emits a signal when a new component
    needs to be added. The emitted signal contains a dictionary with the values of the new component.
    """

    submit = qtc.pyqtSignal(BaseNode)

    def __init__(self, manufacture_model, node):
        """
        Loads the UI window, connects the buttons to the proper functions and initialises
        the fields of the window's widgets.

        Custom functions:
            self.initFields()

        Args:
            manufacture_model (QAbstractItemModel): the model of the manufacture combobox.
            node (BaseNode): the node to fill. Used to initialise the fields.
        """

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
        The passed node is used as a reference for the data to set in the widgets.

        Custom functions:
            self.changeManufacture()
            BaseNode.getFeature()
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
        Editable nodes will have a combobox, non-editable nodes will have a line edit.

        Custom functions:
            BaseNode.getFeature()
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
        Used when submitting the dictionary.

        Custom functions:
            BaseNode.getFeature()
        """

        if self.currentNode.getFeature('type') == 'Assembly' or self.currentNode.getFeature('type') == 'Placeholder':
            return None
        else:
            return self.uiManufacture.currentText()

    def onSubmit(self):
        """Emits the dictionary with the current data."""

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
            'link': self.uiLink.toPlainText()
        }

        toRemove = []
        for key, value in data.items():
            if not value:
                toRemove.append(key)

        for key in toRemove:
            del data[key]

        self.currentNode.addFeatures(**data)

        self.submit.emit(self.currentNode)
        self.close()
