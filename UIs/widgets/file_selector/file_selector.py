# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\file_selector.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_file_selector(object):
    def setupUi(self, file_selector):
        file_selector.setObjectName("file_selector")
        file_selector.resize(400, 23)
        self.horizontalLayout = QtWidgets.QHBoxLayout(file_selector)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiDetails = QtWidgets.QLabel(file_selector)
        self.uiDetails.setObjectName("uiDetails")
        self.horizontalLayout.addWidget(self.uiDetails)
        self.uiPath = QtWidgets.QLineEdit(file_selector)
        self.uiPath.setText("")
        self.uiPath.setObjectName("uiPath")
        self.horizontalLayout.addWidget(self.uiPath)
        self.uiBrowseBtn = QtWidgets.QPushButton(file_selector)
        self.uiBrowseBtn.setObjectName("uiBrowseBtn")
        self.horizontalLayout.addWidget(self.uiBrowseBtn)

        self.retranslateUi(file_selector)
        QtCore.QMetaObject.connectSlotsByName(file_selector)

    def retranslateUi(self, file_selector):
        _translate = QtCore.QCoreApplication.translate
        file_selector.setWindowTitle(_translate("file_selector", "Form"))
        self.uiDetails.setText(_translate("file_selector", "Details"))
        self.uiPath.setPlaceholderText(_translate("file_selector", "Path..."))
        self.uiBrowseBtn.setText(_translate("file_selector", "Browse"))
