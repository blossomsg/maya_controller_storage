# module_for_ui
from PySide2 import QtCore
from PySide2 import QtWidgets
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
		self.cs_frame = QtWidgets.QFrame()
		self.cs_frame.setFrameShape(QtWidgets.QFrame.HLine)
		self.cs_frame.setLineWidth(5.0)
		self.cs_locate_create_curve_json_qpushbutton = QtWidgets.QPushButton("Locate/Create_CurveJSON")
		self.cs_locate_json_path_qlineedit = QtWidgets.QLineEdit()
		self.cs_json_file_name_qlineedit = QtWidgets.QLineEdit()
		self.cs_preserve_curve_qpushbutton = QtWidgets.QPushButton("Preserve_Curve")
		self.cs_read_json_file_qpushbutton = QtWidgets.QPushButton("Read_JSON_File")
		# self.cs_json_create_checkbox = QtWidgets.QCheckBox("Create_JSON")
		# self.cs_create_curve_json_qpushbutton = QtWidgets.QPushButton("Create_CurveJSON")
		# self.cs_create_newjson_path_qlineedit = QtWidgets.QLineEdit()
		self.cs_curve_dict_listwid = QtWidgets.QListWidget()
		self.cs_create_selected_curve_qpushbutton = QtWidgets.QPushButton("Create_Selected_Curve")

		# CAVEAT : Layouts
		self.cs_vlayout = QtWidgets.QVBoxLayout()  # vertical layout
		self.cs_locate_json_hlayout = QtWidgets.QHBoxLayout()  # horizontal layout to locate json
		# self.cs_create_json_hlayout = QtWidgets.QHBoxLayout()  # horizontal layout to create json
		# self.cs_create_json_set_vlayout = QtWidgets.QVBoxLayout() # vertically organize "create json"

		# CAVEAT : Adding widgets to layouts
		self.cs_vlayout.addWidget(self.cs_duplicate_curve_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_frame)
		self.cs_locate_json_hlayout.addWidget(self.cs_locate_create_curve_json_qpushbutton)
		self.cs_locate_json_hlayout.addWidget(self.cs_locate_json_path_qlineedit)
		self.cs_locate_json_hlayout.addWidget(self.cs_json_file_name_qlineedit)
		self.cs_vlayout.addLayout(self.cs_locate_json_hlayout)
		self.cs_vlayout.addWidget(self.cs_preserve_curve_qpushbutton)
		self.cs_vlayout.addWidget(self.cs_read_json_file_qpushbutton)
		# self.cs_create_json_hlayout.addWidget(self.cs_create_curve_json_qpushbutton)
		# self.cs_create_json_hlayout.addWidget(self.cs_create_newjson_path_qlineedit)
		# self.cs_create_json_set_vlayout.addWidget(self.cs_json_create_checkbox)
		# self.cs_create_json_set_vlayout.addLayout(self.cs_create_json_hlayout)
		# self.cs_vlayout.addLayout(self.cs_create_json_set_vlayout)
		self.cs_vlayout.addWidget(self.cs_curve_dict_listwid)
		self.cs_vlayout.addWidget(self.cs_create_selected_curve_qpushbutton)

		# CAVEAT : UI additional details
		self.setLayout(self.cs_vlayout)
		self.setWindowTitle("CS v1.0")
		# self.setWindowIcon(provide file path)
		# self.windowIcon(provide file path)
		# self.setFixedSize(300, 100)


if __name__ == "__main__":
	print "This is Main ControllerStorageUI"
else:
	print "This is ControllerStorageUI"
