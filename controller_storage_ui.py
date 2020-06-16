# module_for_ui
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import controller_storage_rcc

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

		# CAVEAT : Complete UI setup
		self.cs_image_pixmap = QtGui.QPixmap(":/testing/controller_storage_label.jpg")
		self.cs_qlabel_pixmap = QtWidgets.QLabel()
		self.cs_qlabel_pixmap.setPixmap(self.cs_image_pixmap)
		self.cs_duplicate_curve_qpushbutton = QtWidgets.QPushButton("Duplicate_Curve")
		self.cs_frame = QtWidgets.QFrame()
		self.cs_frame.setFrameShape(QtWidgets.QFrame.HLine)
		self.cs_frame.setLineWidth(5.0)
		self.cs_locate_create_curve_json_qpushbutton = QtWidgets.QPushButton("Locate/Create_CurveJSON")
		self.cs_locate_json_path_qlineedit = QtWidgets.QLineEdit()
		self.cs_json_file_name_qlineedit = QtWidgets.QLineEdit()
		self.cs_preserve_curve_qpushbutton = QtWidgets.QPushButton("Preserve_Curve")
		self.cs_read_json_file_qpushbutton = QtWidgets.QPushButton("Read_JSON_File")
		self.cs_curve_delete_qpushbutton = QtWidgets.QPushButton("Delete_Curve")
		self.cs_curve_dict_listwid = QtWidgets.QListWidget()
		self.cs_create_selected_curve_qpushbutton = QtWidgets.QPushButton("Create_Selected_Curve")

		# CAVEAT : Layouts
		self.cs_vlayout = QtWidgets.QVBoxLayout()  # vertical layout
		self.cs_locate_json_hlayout = QtWidgets.QHBoxLayout()  # horizontal layout to locate json

		# CAVEAT : Adding widgets to layouts
		self.cs_vlayout.addWidget(self.cs_qlabel_pixmap)
		self.cs_vlayout.addWidget(self.cs_duplicate_curve_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_frame)
		self.cs_locate_json_hlayout.addWidget(self.cs_locate_create_curve_json_qpushbutton)
		self.cs_locate_json_hlayout.addWidget(self.cs_locate_json_path_qlineedit)
		self.cs_locate_json_hlayout.addWidget(self.cs_json_file_name_qlineedit)
		self.cs_vlayout.addLayout(self.cs_locate_json_hlayout)
		self.cs_vlayout.addWidget(self.cs_preserve_curve_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_read_json_file_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_curve_delete_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_curve_dict_listwid)
		self.cs_vlayout.addWidget(self.cs_create_selected_curve_qpushbutton)

		# CAVEAT : UI additional details
		self.setLayout(self.cs_vlayout)
		self.setWindowTitle("CS v0.0.2")


if __name__ == "__main__":
	print "This is Main ControllerStorageUI"
else:
	print "This is ControllerStorageUI"
