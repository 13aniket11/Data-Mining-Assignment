# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dm(object):
    def setupUi(self, dm):
        dm.setObjectName("dm")
        dm.setWindowModality(QtCore.Qt.WindowModal)
        dm.resize(747, 389)
        dm.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        dm.setLayoutDirection(QtCore.Qt.LeftToRight)
        dm.setAutoFillBackground(True)
        self.comboBox = QtWidgets.QComboBox(dm)
        self.comboBox.setGeometry(QtCore.QRect(0, 0, 111, 61))
        self.comboBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.comboBox.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setInputMethodHints(QtCore.Qt.ImhNoTextHandles)
        self.comboBox.setEditable(False)
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(dm)
        self.comboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(dm)

    def retranslateUi(self, dm):
        _translate = QtCore.QCoreApplication.translate
        dm.setWindowTitle(_translate("dm", "Data Analysis Tool"))
        self.comboBox.setAccessibleName(_translate("dm", "Select Tool"))
        self.comboBox.setAccessibleDescription(_translate("dm", "Select Tool"))
        self.comboBox.setItemText(0, _translate("dm", "Assignmen 1"))
        self.comboBox.setItemText(1, _translate("dm", "Assignment 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dm = QtWidgets.QWidget()
    ui = Ui_dm()
    ui.setupUi(dm)
    dm.show()
    sys.exit(app.exec_())
