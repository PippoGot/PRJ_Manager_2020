# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\archive_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiArchivePage(object):
    def setupUi(self, uiArchivePage):
        uiArchivePage.setObjectName("uiArchivePage")
        uiArchivePage.resize(337, 815)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(uiArchivePage)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.gridWidget = QtWidgets.QWidget(uiArchivePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gridWidget.sizePolicy().hasHeightForWidth())
        self.gridWidget.setSizePolicy(sizePolicy)
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.uiType = QtWidgets.QLineEdit(self.gridWidget)
        self.uiType.setReadOnly(True)
        self.uiType.setObjectName("uiType")
        self.gridLayout.addWidget(self.uiType, 6, 1, 1, 3)
        self.uiQuantity = QtWidgets.QSpinBox(self.gridWidget)
        self.uiQuantity.setObjectName("uiQuantity")
        self.gridLayout.addWidget(self.uiQuantity, 9, 1, 1, 1)
        self.uiNumberID = QtWidgets.QLineEdit(self.gridWidget)
        self.uiNumberID.setReadOnly(True)
        self.uiNumberID.setObjectName("uiNumberID")
        self.gridLayout.addWidget(self.uiNumberID, 0, 0, 1, 4)
        self.label_10 = QtWidgets.QLabel(self.gridWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 4, 0, 1, 4)
        self.uiStatus = QtWidgets.QComboBox(self.gridWidget)
        self.uiStatus.setObjectName("uiStatus")
        self.gridLayout.addWidget(self.uiStatus, 8, 1, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.gridWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 10, 0, 1, 1)
        self.uiPrice = QtWidgets.QLineEdit(self.gridWidget)
        self.uiPrice.setObjectName("uiPrice")
        self.gridLayout.addWidget(self.uiPrice, 10, 1, 1, 3)
        self.uiDescription = QtWidgets.QPlainTextEdit(self.gridWidget)
        self.uiDescription.setObjectName("uiDescription")
        self.gridLayout.addWidget(self.uiDescription, 3, 0, 1, 4)
        self.uiQuantityPackage = QtWidgets.QSpinBox(self.gridWidget)
        self.uiQuantityPackage.setObjectName("uiQuantityPackage")
        self.gridLayout.addWidget(self.uiQuantityPackage, 9, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 12, 0, 1, 4)
        self.uiManufacture = QtWidgets.QStackedWidget(self.gridWidget)
        self.uiManufacture.setEnabled(True)
        self.uiManufacture.setMaximumSize(QtCore.QSize(16777215, 20))
        self.uiManufacture.setAutoFillBackground(False)
        self.uiManufacture.setObjectName("uiManufacture")
        self.uiManufacturePage1_2 = QtWidgets.QWidget()
        self.uiManufacturePage1_2.setObjectName("uiManufacturePage1_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.uiManufacturePage1_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.noneditable = QtWidgets.QLineEdit(self.uiManufacturePage1_2)
        self.noneditable.setReadOnly(True)
        self.noneditable.setObjectName("noneditable")
        self.horizontalLayout_3.addWidget(self.noneditable)
        self.uiManufacture.addWidget(self.uiManufacturePage1_2)
        self.uiManufacturePage2_2 = QtWidgets.QWidget()
        self.uiManufacturePage2_2.setObjectName("uiManufacturePage2_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.uiManufacturePage2_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.editable = QtWidgets.QComboBox(self.uiManufacturePage2_2)
        self.editable.setObjectName("editable")
        self.horizontalLayout_4.addWidget(self.editable)
        self.uiManufacture.addWidget(self.uiManufacturePage2_2)
        self.gridLayout.addWidget(self.uiManufacture, 7, 1, 1, 3)
        self.label_3 = QtWidgets.QLabel(self.gridWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 9, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 9, 2, 1, 1)
        self.uiName = QtWidgets.QLineEdit(self.gridWidget)
        self.uiName.setObjectName("uiName")
        self.gridLayout.addWidget(self.uiName, 1, 1, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.gridWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.uiLink = QtWidgets.QTextEdit(self.gridWidget)
        self.uiLink.setObjectName("uiLink")
        self.gridLayout.addWidget(self.uiLink, 13, 0, 1, 4)
        self.label_7 = QtWidgets.QLabel(self.gridWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.uiComment = QtWidgets.QPlainTextEdit(self.gridWidget)
        self.uiComment.setObjectName("uiComment")
        self.gridLayout.addWidget(self.uiComment, 5, 0, 1, 4)
        self.uiSeller = QtWidgets.QLineEdit(self.gridWidget)
        self.uiSeller.setObjectName("uiSeller")
        self.gridLayout.addWidget(self.uiSeller, 11, 1, 1, 3)
        self.label_8 = QtWidgets.QLabel(self.gridWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 11, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 4)
        self.label_6 = QtWidgets.QLabel(self.gridWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.uiAddBtn = QtWidgets.QPushButton(self.gridWidget)
        self.uiAddBtn.setObjectName("uiAddBtn")
        self.gridLayout.addWidget(self.uiAddBtn, 0, 4, 1, 1)
        self.uiDelBtn = QtWidgets.QPushButton(self.gridWidget)
        self.uiDelBtn.setObjectName("uiDelBtn")
        self.gridLayout.addWidget(self.uiDelBtn, 1, 4, 1, 1)
        self.horizontalLayout_5.addWidget(self.gridWidget)

        self.retranslateUi(uiArchivePage)
        self.uiManufacture.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(uiArchivePage)

    def retranslateUi(self, uiArchivePage):
        _translate = QtCore.QCoreApplication.translate
        uiArchivePage.setWindowTitle(_translate("uiArchivePage", "Form"))
        self.label_10.setText(_translate("uiArchivePage", "Comment:"))
        self.label_11.setText(_translate("uiArchivePage", "Price:"))
        self.label_9.setText(_translate("uiArchivePage", "Link:"))
        self.label_3.setText(_translate("uiArchivePage", "Quantity:"))
        self.label_4.setText(_translate("uiArchivePage", "Per Unit:"))
        self.label_5.setText(_translate("uiArchivePage", "Type:"))
        self.label_7.setText(_translate("uiArchivePage", "Status:"))
        self.label.setText(_translate("uiArchivePage", "Name:"))
        self.label_8.setText(_translate("uiArchivePage", "Seller:"))
        self.label_2.setText(_translate("uiArchivePage", "Description:"))
        self.label_6.setText(_translate("uiArchivePage", "Manufacture:"))
        self.uiAddBtn.setText(_translate("uiArchivePage", "Add"))
        self.uiDelBtn.setText(_translate("uiArchivePage", "Delete"))
