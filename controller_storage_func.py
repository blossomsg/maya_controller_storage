# func_module_for_ui
from PySide2 import QtCore
from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import maya.cmds as cmds
import controller_storage_ui
import os


class ControllerStorageFunc(controller_storage_ui.ControllerStorageUI):
	"""This Class is Func for UI to preserve nurbs curve

	"""
	def __init__(self):
		super(ControllerStorageFunc, self).__init__()

		self.cs_duplicate_curve_qpushbutton.clicked.connect(self.cs_duplicate_button_func)
		# self.cs_locate_create_curve_json_qpushbutton.clicked.connect()
		self.cs_filename()
		self.cs_filepath()
		self.cs_preserve_curve_qpushbutton.setEnabled(False)
		self.cs_locate_create_curve_json_qpushbutton.clicked.connect(self.cs_locate_create_button)

	# CAVEAT : Duplicate curve func
	def cs_duplicate_button_func(self):
		cmds.duplicate()

	# CAVEAT : Controller storage file name
	def cs_filename(self):
		self.cs_json_file_name_qlineedit.setText("controller_storage.json")
		self.cs_json_file_name_qlineedit.setReadOnly(True)

	# CAVEAT : Controller storage directory path
	def cs_filepath(self):
		self.cs_locate_json_path_qlineedit.setToolTip("Provide an appropriate directory path")
		# if self.cs_locate_json_path_qlineedit(filepath):
		# 	self.cs_preserve_curve_qpushbutton.setEnabled(True)
		# else:
		# 	self.cs_preserve_curve_qpushbutton.setEnabled(False)

	# CAVEAT : Locate/Create button func
	def cs_locate_create_button(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		if file_dir:
			filepath = os.path.join(self.cs_locate_json_path_qlineedit.text(), self.cs_json_file_name_qlineedit.text())
			if os.path.isfile(filepath):
				print "controller_storage.json File already exists"
			else:
				with open(filepath, "w") as testing:
					pass
				print "controller_storage.json File created"
		else:
			print "Kindly provide directory path"

			print filepath

# to preserve the shape of the curve
# def query_curve():
# 	curve_sel_list_shape = cmds.listRelatives()
# 	if curve_sel_list_shape:
# 		if cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve":
# 			print "It is a kNurbsCurve"
# 			return curve_sel_list_shape
# 		else:
# 			return "Kindly pick a 'kNurbsCurve'"
# 	else:
# 		return "Kindly select something in the scene"
#

# curve_shape = query_curve()
# if type(curve_shape) == list:
# 	# if we select curveshape directly that gives an error, kindly fix that in the function
# 	get_curve_points = cmds.getAttr('%s.cv[*]' % curve_shape[0])
# 	get_curve_degree = cmds.getAttr('%s.degree' % curve_shape[0])
# 	# get_curve_spans = cmds.getAttr( '%s.spans'%curve_shape[0])
# 	curve_info_node = cmds.createNode('curveInfo', name="%s_controller_storage" % curve_shape[0])
# 	cmds.connectAttr('%s.worldSpace' % curve_shape[0], '%s_controller_storage.inputCurve' % curve_shape[0])
# 	get_curve_knots = cmds.getAttr('%s_controller_storage.knots[*]' % curve_shape[0])
# 	cmds.delete(curve_info_node)
# # cmds.curve(degree=get_curve_degree, point=get_curve_points, knot=get_curve_knots)
# else:
# 	print curve_shape
#
# # save the script in the json file "curve_dict" first need to create a dict
# curve_dict = {
# 	"{}".format(curve_shape[0]): "cmds.curve(degree={}, point={}, knot={})".format(get_curve_degree, get_curve_points,
# 																				   get_curve_knots)}
# # exec(curve_dict["trial_t_shirtShape"])
# # then to append the another key values for more values
# curve_dict["{}".format(curve_shape[0])] = "cmds.curve(degree={}, point={}, knot={})".format(get_curve_degree,
# 																							get_curve_points,
# 																							get_curve_knots)
#
# import json
#
# with open("D:\\All_Projs\\Maya_Projs\\controller_storage\\testing_data.json", "w") as write_file:
# 	json.dump(curve_dict, write_file, indent=4)
# 	write_file.close()
#
# with open("D:\\All_Projs\\Maya_Projs\\controller_storage\\testing_data.json", "r") as read_file:
# 	testing = json.load(read_file)
# 	exec testing["type_curve_0Shape5"]
# 	print testing.keys()
#
# # try to print json file contents
# # try to update the json file with multiple values
# # then try to fetch multiple values like first 1st, then second , thrid, after second point
# #