from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ComponentTree import ComponentTree
from constants import TYPES_FROM_EDITOR as types

class ComponentEditor(qtw.QWidget):
    """
    This class is a popup window for components editing. Emits a signal when a new component
    needs to be added.
    """

    submit = qtc.pyqtSignal(ComponentTree)                                                  # signal for the submit button
    
    def __init__(self, parent, manufacture_model, level = None):
        """Loads the .ui file, and connects the buttons to their respective functions.

        INPUT:
            ComponentTree - parent: item to calculate the number from
            optional int - level: value for level overwriting
        """
        super(ComponentEditor, self).__init__()                                             # superclass constructor

        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_component_editor.ui', self)   # loads the UI from the .ui file

        self.mapper = qtw.QDataWidgetMapper()                                               # creates the mapper object
        self.manufactures = manufacture_model

        self.uiCancelButton.clicked.connect(self.close)                                     # connects the buttons to their respective functions
        self.uiSubmitButton.clicked.connect(self.onSubmit)

        self.initFields(parent, level)

    def onSubmit(self):
        """Emits the ComponentTree object with the current data."""

        data = {                                                                            # gathers the component data
            'number': self.uiNumberID.text(),
            'title': self.uiName.text(), 
            'description': self.uiDescription.toPlainText(),
            'type': self.uiType.text(),
            'manufacture': self.calc_manufacture(self.uiType.text()),
            'status': self.uiStatus.currentText(),
            'comment': self.uiComment.toPlainText(),
            'priceUnit': self.uiPriceUnit.text(),
            'quantity': self.uiQuantityNeeded.text(),
            'quantityPackage': self.uiQuantityUnit.text(),
            'seller': self.uiSeller.text(),
            'kit': self.uiKit.currentText(),
            'link': self.uiLink.toPlainText()
        }

        newComponent = ComponentTree(self.uiNumberID, data)

        self.submit.emit(newComponent)                                                      # the signal is emitted
        self.close()                                                                        # the window is closed

    def initFields(self, parent, level):
        """Initializes the fields when a new popup is opened.

        INPUT:
            ComponentTree - parent: item to calculate the number from
            int - level: value for level overwriting
        """
        
        number = parent.calc_number(parent, level)
        self.uiNumberID.setText(number)

        self.uiName.setText('-')
        self.uiDescription.setPlainText('-')

        level = parent.level + 1
        

        self.uiType.setText(types[level])
        self.uiComment.setPlainText('-')
        self.uiPriceUnit.setText('0')
        self.uiSeller.setText('-')
        self.uiLink.setPlainText('-')
        
        self.changeManufactureWidget(self.uiType.text(), self.uiManufacture, self.uiNumberID)

    def changeManufactureWidget(self, nodeType, widgetPtr, numberPtr):
        layout = widgetPtr.parentWidget().layout()

        def changeWidget(widget, widgetPointer, text = None):
            layout.removeWidget(widgetPointer)
            widgetPointer.close()
            layout.removeRow(2)

            if widget == 'LineEdit':
                widgetPointer = qtw.QLineEdit()
                widgetPointer.setReadOnly(True)
                widgetPointer.setText(text)
            elif widget == 'ComboBox':
                widgetPointer = qtw.QComboBox()
                widgetPointer.setModel(self.manufactures)
                widgetPointer.setCurrentIndex(0)

            layout.insertRow(2, 'Manufacture', widgetPointer)
            layout.update()
            self.uiManufacture = widgetPointer

        if nodeType == 'Project' or nodeType == 'Assembly':
            changeWidget('LineEdit', widgetPtr, 'Assembled')
        elif nodeType == 'Hardware' or nodeType == 'Consumables':
            if numberPtr.text()[1:4] == 'MMH':
                changeWidget('LineEdit', widgetPtr, 'Cut to Length')
            else:
                changeWidget('LineEdit', widgetPtr, 'Off the Shelf')
        elif nodeType == 'Placeholder':
            changeWidget('LineEdit', widgetPtr, 'None')
        else:
            changeWidget('ComboBox', widgetPtr)

    def calc_manufacture(self, nodeType):
        if nodeType == 'Project' or nodeType == 'Assembly':
            return 'Assembled'
        elif nodeType == 'Placeholder':
            return None
        else:
            return self.uiManufacture.currentText()
