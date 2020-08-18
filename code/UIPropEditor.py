from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from ComponentTree import ComponentTree

class PropEditor(qtw.QWidget):
    """
    This class is a popup/widget for components editing. Emits a signal when a new component
    needs to be added.
    """

    submit = qtc.pyqtSignal(ComponentTree)                            # signal for the submit button
    
    def __init__(self, parent, level = None):
        """Loads the .ui file, and connects the buttons to their respective functions.

        INPUT:
            str - mode: changes the mode of the widget, choose between popup and widget. Defaults to 'widget'.
        """
        super(PropEditor, self).__init__()                                              # superclass constructor

        uic.loadUi('D:/Data/_PROGETTI/Apps/PRJ_Manager/UIs/ui_component_editor.ui', self)        # loads the UI from the .ui file

        self.mapper = qtw.QDataWidgetMapper()                                           # creates the mapper object

        self.uiCancelButton.clicked.connect(self.close)                                 # connects the buttons to their respective functions
        self.uiSubmitButton.clicked.connect(self.onSubmit)

        self.initFields(parent, level)

    def onSubmit(self):
        """
        Emits the current selected item data. Can be connected to the model insertRows() function
        if an index and a row are provided beforehand.
        """

        data = {                                                                        # gathers the component data
            'number': self.uiNumberID.text(),
            'title': self.uiName.text(), 
            'description': self.uiDescription.toPlainText(),
            'type': self.uiType.text(),
            'manufacture': self.uiManufacture.currentText(),
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

        self.submit.emit(newComponent)                                 # the signal is emitted
        self.close()                                                                    # the window is closed

    def initFields(self, parent, level):
        number = parent.calc_number(parent, level)
        self.uiNumberID.setText(number)

        self.uiName.setText('-')
        self.uiDescription.setPlainText('-')

        types = {
            1: 'Project',
            2: 'Assembly',
            3: 'Assembly',
            4: 'Assembly',
            5: 'Part'
        }

        self.uiType.setText(types[parent.level + 1])
        # self.uiManufacture.currentText(),
        # self.uiStatus.currentText(),
        self.uiComment.setPlainText('-')
        self.uiPriceUnit.setText('0')
        self.uiSeller.setText('-')
        # self.uiKit.currentText()
        self.uiLink.setPlainText('-')