# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\hardware_selector.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_uiHardwareSelector(object):
    def setupUi(self, uiHardwareSelector):
        uiHardwareSelector.setObjectName("uiHardwareSelector")
        uiHardwareSelector.setWindowModality(QtCore.Qt.ApplicationModal)
        uiHardwareSelector.resize(1005, 692)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(uiHardwareSelector)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(uiHardwareSelector)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.uiQuanity = QtWidgets.QSpinBox(uiHardwareSelector)
        self.uiQuanity.setObjectName("uiQuanity")
        self.horizontalLayout_2.addWidget(self.uiQuanity)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.uiArchiveView = ArchiveView(uiHardwareSelector)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiArchiveView.sizePolicy().hasHeightForWidth())
        self.uiArchiveView.setSizePolicy(sizePolicy)
        self.uiArchiveView.setObjectName("uiArchiveView")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.uiArchiveView)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addWidget(self.uiArchiveView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.uiOkBtn = QtWidgets.QPushButton(uiHardwareSelector)
        self.uiOkBtn.setObjectName("uiOkBtn")
        self.horizontalLayout.addWidget(self.uiOkBtn)
        self.uiCancelBtn = QtWidgets.QPushButton(uiHardwareSelector)
        self.uiCancelBtn.setObjectName("uiCancelBtn")
        self.horizontalLayout.addWidget(self.uiCancelBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(uiHardwareSelector)
        QtCore.QMetaObject.connectSlotsByName(uiHardwareSelector)

    def retranslateUi(self, uiHardwareSelector):
        _translate = QtCore.QCoreApplication.translate
        uiHardwareSelector.setWindowTitle(_translate("uiHardwareSelector", "uiHardwareSelector"))
        self.label.setText(_translate("uiHardwareSelector", "Quantity:"))
        self.uiOkBtn.setText(_translate("uiHardwareSelector", "Ok"))
        self.uiCancelBtn.setText(_translate("uiHardwareSelector", "Cancel"))
