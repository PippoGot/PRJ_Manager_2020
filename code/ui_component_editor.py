# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_component_editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiComponentsEditor(object):
    def setupUi(self, uiComponentsEditor):
        uiComponentsEditor.setObjectName("uiComponentsEditor")
        uiComponentsEditor.resize(521, 388)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(uiComponentsEditor)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uiNumberID = QtWidgets.QLineEdit(uiComponentsEditor)
        self.uiNumberID.setMinimumSize(QtCore.QSize(80, 0))
        self.uiNumberID.setAlignment(QtCore.Qt.AlignCenter)
        self.uiNumberID.setReadOnly(True)
        self.uiNumberID.setObjectName("uiNumberID")
        self.horizontalLayout_2.addWidget(self.uiNumberID)
        self.uiQuantityNeededLabel = QtWidgets.QLabel(uiComponentsEditor)
        self.uiQuantityNeededLabel.setObjectName("uiQuantityNeededLabel")
        self.horizontalLayout_2.addWidget(self.uiQuantityNeededLabel)
        self.uiQuantityNeeded = QtWidgets.QSpinBox(uiComponentsEditor)
        self.uiQuantityNeeded.setProperty("value", 1)
        self.uiQuantityNeeded.setObjectName("uiQuantityNeeded")
        self.horizontalLayout_2.addWidget(self.uiQuantityNeeded)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(uiComponentsEditor)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.manufactureContainer = QtWidgets.QWidget(self.widget)
        self.manufactureContainer.setObjectName("manufactureContainer")
        self.formLayout = QtWidgets.QFormLayout(self.manufactureContainer)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(5)
        self.formLayout.setObjectName("formLayout")
        self.uiNameLabel = QtWidgets.QLabel(self.manufactureContainer)
        self.uiNameLabel.setMinimumSize(QtCore.QSize(50, 20))
        self.uiNameLabel.setObjectName("uiNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.uiNameLabel)
        self.uiName = QtWidgets.QLineEdit(self.manufactureContainer)
        self.uiName.setMinimumSize(QtCore.QSize(170, 20))
        self.uiName.setObjectName("uiName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.uiName)
        self.uiTypeLabel = QtWidgets.QLabel(self.manufactureContainer)
        self.uiTypeLabel.setMinimumSize(QtCore.QSize(70, 20))
        self.uiTypeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.uiTypeLabel.setObjectName("uiTypeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.uiTypeLabel)
        self.uiManufactureLabel = QtWidgets.QLabel(self.manufactureContainer)
        self.uiManufactureLabel.setMinimumSize(QtCore.QSize(70, 20))
        self.uiManufactureLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.uiManufactureLabel.setObjectName("uiManufactureLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.uiManufactureLabel)
        self.uiManufacture = QtWidgets.QComboBox(self.manufactureContainer)
        self.uiManufacture.setEditable(False)
        self.uiManufacture.setObjectName("uiManufacture")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.uiManufacture)
        self.uiStatusLabel = QtWidgets.QLabel(self.manufactureContainer)
        self.uiStatusLabel.setMinimumSize(QtCore.QSize(70, 20))
        self.uiStatusLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.uiStatusLabel.setObjectName("uiStatusLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.uiStatusLabel)
        self.uiStatus = QtWidgets.QComboBox(self.manufactureContainer)
        self.uiStatus.setEditable(False)
        self.uiStatus.setObjectName("uiStatus")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uiStatus)
        self.uiType = QtWidgets.QLineEdit(self.manufactureContainer)
        self.uiType.setReadOnly(True)
        self.uiType.setObjectName("uiType")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uiType)
        self.verticalLayout.addWidget(self.manufactureContainer)
        self.uiDescriptionLabel = QtWidgets.QLabel(self.widget)
        self.uiDescriptionLabel.setObjectName("uiDescriptionLabel")
        self.verticalLayout.addWidget(self.uiDescriptionLabel)
        self.uiDescription = QtWidgets.QPlainTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiDescription.sizePolicy().hasHeightForWidth())
        self.uiDescription.setSizePolicy(sizePolicy)
        self.uiDescription.setMinimumSize(QtCore.QSize(0, 50))
        self.uiDescription.setObjectName("uiDescription")
        self.verticalLayout.addWidget(self.uiDescription)
        self.uiCommentLabel = QtWidgets.QLabel(self.widget)
        self.uiCommentLabel.setMinimumSize(QtCore.QSize(50, 20))
        self.uiCommentLabel.setObjectName("uiCommentLabel")
        self.verticalLayout.addWidget(self.uiCommentLabel)
        self.uiComment = QtWidgets.QPlainTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiComment.sizePolicy().hasHeightForWidth())
        self.uiComment.setSizePolicy(sizePolicy)
        self.uiComment.setMinimumSize(QtCore.QSize(0, 50))
        self.uiComment.setObjectName("uiComment")
        self.verticalLayout.addWidget(self.uiComment)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.uiQnPContainer = QtWidgets.QWidget(uiComponentsEditor)
        self.uiQnPContainer.setObjectName("uiQnPContainer")
        self.uiBuyingDetailsContainer = QtWidgets.QVBoxLayout(self.uiQnPContainer)
        self.uiBuyingDetailsContainer.setContentsMargins(0, 0, 0, 0)
        self.uiBuyingDetailsContainer.setObjectName("uiBuyingDetailsContainer")
        self.formLayout_2 = QtWidgets.QWidget(self.uiQnPContainer)
        self.formLayout_2.setObjectName("formLayout_2")
        self.uiQuantityAndPriceContainer = QtWidgets.QFormLayout(self.formLayout_2)
        self.uiQuantityAndPriceContainer.setObjectName("uiQuantityAndPriceContainer")
        self.uiQuantityUnitLabel = QtWidgets.QLabel(self.formLayout_2)
        self.uiQuantityUnitLabel.setObjectName("uiQuantityUnitLabel")
        self.uiQuantityAndPriceContainer.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.uiQuantityUnitLabel)
        self.uiQuantityUnit = QtWidgets.QSpinBox(self.formLayout_2)
        self.uiQuantityUnit.setProperty("value", 1)
        self.uiQuantityUnit.setObjectName("uiQuantityUnit")
        self.uiQuantityAndPriceContainer.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.uiQuantityUnit)
        self.uiPriceUnitLabel = QtWidgets.QLabel(self.formLayout_2)
        self.uiPriceUnitLabel.setObjectName("uiPriceUnitLabel")
        self.uiQuantityAndPriceContainer.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.uiPriceUnitLabel)
        self.uiPriceUnit = QtWidgets.QLineEdit(self.formLayout_2)
        self.uiPriceUnit.setObjectName("uiPriceUnit")
        self.uiQuantityAndPriceContainer.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.uiPriceUnit)
        self.uiSellerLabel = QtWidgets.QLabel(self.formLayout_2)
        self.uiSellerLabel.setMinimumSize(QtCore.QSize(50, 20))
        self.uiSellerLabel.setObjectName("uiSellerLabel")
        self.uiQuantityAndPriceContainer.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.uiSellerLabel)
        self.uiSeller = QtWidgets.QLineEdit(self.formLayout_2)
        self.uiSeller.setObjectName("uiSeller")
        self.uiQuantityAndPriceContainer.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.uiSeller)
        self.uiBuyingDetailsContainer.addWidget(self.formLayout_2)
        self.uiLinkLabel = QtWidgets.QLabel(self.uiQnPContainer)
        self.uiLinkLabel.setObjectName("uiLinkLabel")
        self.uiBuyingDetailsContainer.addWidget(self.uiLinkLabel)
        self.uiLink = QtWidgets.QPlainTextEdit(self.uiQnPContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiLink.sizePolicy().hasHeightForWidth())
        self.uiLink.setSizePolicy(sizePolicy)
        self.uiLink.setMinimumSize(QtCore.QSize(0, 50))
        self.uiLink.setObjectName("uiLink")
        self.uiBuyingDetailsContainer.addWidget(self.uiLink)
        self.verticalLayout_3.addWidget(self.uiQnPContainer)
        self.uiExitButtonsContainer = QtWidgets.QHBoxLayout()
        self.uiExitButtonsContainer.setObjectName("uiExitButtonsContainer")
        self.uiSubmitButton = QtWidgets.QPushButton(uiComponentsEditor)
        self.uiSubmitButton.setAutoDefault(False)
        self.uiSubmitButton.setDefault(True)
        self.uiSubmitButton.setObjectName("uiSubmitButton")
        self.uiExitButtonsContainer.addWidget(self.uiSubmitButton)
        self.uiCancelButton = QtWidgets.QPushButton(uiComponentsEditor)
        self.uiCancelButton.setObjectName("uiCancelButton")
        self.uiExitButtonsContainer.addWidget(self.uiCancelButton)
        self.verticalLayout_3.addLayout(self.uiExitButtonsContainer)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.retranslateUi(uiComponentsEditor)
        QtCore.QMetaObject.connectSlotsByName(uiComponentsEditor)

    def retranslateUi(self, uiComponentsEditor):
        _translate = QtCore.QCoreApplication.translate
        uiComponentsEditor.setWindowTitle(_translate("uiComponentsEditor", "Components Editor"))
        self.uiQuantityNeededLabel.setText(_translate("uiComponentsEditor", "Needed"))
        self.uiNameLabel.setText(_translate("uiComponentsEditor", "Name"))
        self.uiTypeLabel.setText(_translate("uiComponentsEditor", "Type"))
        self.uiManufactureLabel.setText(_translate("uiComponentsEditor", "Manufacture"))
        self.uiStatusLabel.setText(_translate("uiComponentsEditor", "Status"))
        self.uiDescriptionLabel.setText(_translate("uiComponentsEditor", "Description"))
        self.uiCommentLabel.setText(_translate("uiComponentsEditor", "Comment:"))
        self.uiQuantityUnitLabel.setText(_translate("uiComponentsEditor", "Per Unit"))
        self.uiPriceUnitLabel.setText(_translate("uiComponentsEditor", "Price"))
        self.uiSellerLabel.setText(_translate("uiComponentsEditor", "Seller"))
        self.uiLinkLabel.setText(_translate("uiComponentsEditor", "Link"))
        self.uiSubmitButton.setText(_translate("uiComponentsEditor", "Add"))
        self.uiSubmitButton.setShortcut(_translate("uiComponentsEditor", "Return"))
        self.uiCancelButton.setText(_translate("uiComponentsEditor", "Cancel"))
        self.uiCancelButton.setShortcut(_translate("uiComponentsEditor", "Esc"))
