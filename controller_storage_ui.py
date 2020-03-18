# module_for_ui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

ptr = omui.MQtUtil.mainWindow()
ptr_instance = wrapInstance(long(ptr), QtWidgets.QWidget)

class ControllerStorageUI(QtWidgets.QWidget):
	"""Preserve the controller in the json and that json will be displayed
	in the ui. That will help create the controllers

	"""

	def __init__(self):
		super(ControllerStorageUI, self).__init__()

		# CAVEAT : Parent the UI to the application Maya
		self.setParent(ptr_instance)
		self.setWindowFlags(QtCore.Qt.Window)

		# CAVEAT : Duplicate Curve button
		self.cs_duplicate_curve_qpushbutton = QtWidgets.QPushButton("Duplicate_Curve")

		# CAVEAT : Layouts
		self.cs_qpushbutton_hlayout = QtWidgets.QHBoxLayout()  # horizontal layout

		# CAVEAT : Adding widgets to layouts
		self.cs_qpushbutton_hlayout.addWidget(self.cs_duplicate_curve_qpushbutton)

		# CAVEAT : UI additional details
		self.setLayout(self.cs_qpushbutton_hlayout)
		self.setWindowTitle("CS v1.0")
		# self.setWindowIcon(provide file path)
		# self.windowIcon(provide file path)
		self.setFixedSize(300, 100)


if __name__ == "__main__":
	print "This is Main ControllerStorageUI"
else:
	print "This is ControllerStorageUI"