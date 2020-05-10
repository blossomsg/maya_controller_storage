# func_module_for_ui
from PySide2 import QtWidgets
import maya.cmds as cmds
import controller_storage_ui
import os
import json


class ControllerStorageFunc(controller_storage_ui.ControllerStorageUI):
	"""This Class is Func for UI to preserve nurbs curve

	"""

	def __init__(self):
		super(ControllerStorageFunc, self).__init__()

		self.cs_tooltips()
		self.cs_duplicate_curve_qpushbutton.clicked.connect(self.cs_duplicate_button_func)
		self.cs_filename()
		self.cs_preserve_curve_qpushbutton.setEnabled(False)
		self.cs_read_json_file_qpushbutton.setEnabled(False)
		self.cs_locate_create_curve_json_qpushbutton.clicked.connect(self.cs_locate_create_button)
		self.cs_preserve_curve_qpushbutton.clicked.connect(self.cs_query_curve)
		self.cs_read_json_file_qpushbutton.clicked.connect(self.cs_read_json)
		self.cs_create_selected_curve_qpushbutton.clicked.connect(self.cs_create_curve)

	# CAVEAT : Controller storage directory path tooltip
	def cs_tooltips(self):
		self.cs_duplicate_curve_qpushbutton.setToolTip("Creates duplicate of the curve on the spot")
		self.cs_locate_json_path_qlineedit.setToolTip("Provide an appropriate directory path")
		self.cs_preserve_curve_qpushbutton.setToolTip(
			"Enables once the jason file location is confirmed,"
			"Preserves nurbs curve in a json file(kindly provide a unique name, or it will override existing key)")
		self.cs_locate_create_curve_json_qpushbutton.setToolTip("Confirms if the json file exists in the "
																"mentioned path or not and enables the Preserve "
																"Curve and Read json button")
		self.cs_read_json_file_qpushbutton.setToolTip("Enables once the jason file location is confirmed,"
													  "fetches the keys from the json file")
		self.cs_curve_dict_listwid.setToolTip("Will list the names of the curves that were saved in the json file")
		self.cs_create_selected_curve_qpushbutton.setToolTip("Creates the curve acc. to the selection from the list")

	# CAVEAT : This Duplicate curve func helps to duplicate the curve
	@staticmethod
	def cs_duplicate_button_func():
		curve_sel_list_shape = cmds.listRelatives()
		print curve_sel_list_shape
		if curve_sel_list_shape:
			if cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve":
				print "It is a kNurbsCurve"
				cmds.duplicate()
			else:
				print "Kindly pick a 'kNurbsCurve'"
		else:
			print "Kindly select something in the scene"

	# CAVEAT : This Controller storage function stores the readonly file name
	def cs_filename(self):
		self.cs_json_file_name_qlineedit.setText("controller_storage.json")
		self.cs_json_file_name_qlineedit.setReadOnly(True)

	# CAVEAT : Locate/Create button func helps to create the .json file in the mentioned directory
	def cs_locate_create_button(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		if file_dir:
			filepath = os.path.join(file_dir, file_name)  # filepath of the dir
			if os.path.isfile(filepath):
				print "controller_storage.json File already exists"
				self.cs_preserve_curve_qpushbutton.setEnabled(True)
				self.cs_read_json_file_qpushbutton.setEnabled(True)
			else:
				with open(filepath, "w") as _controller_storage:
					pass  # this creates the .json file
				print "controller_storage.json File created"
				self.cs_preserve_curve_qpushbutton.setEnabled(True)
				self.cs_read_json_file_qpushbutton.setEnabled(True)
		else:
			print "Kindly provide directory path"

	# CAVEAT : Preserve curve button func will preserve the curve in a .json file
	def cs_query_curve(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		curve_sel_list_shape = cmds.listRelatives()  # Result: [u'curveShape2'] #
		if curve_sel_list_shape:
			if cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve":
				print "It is a kNurbsCurve"
				# return curve_sel_list_shape
				# print curve_sel_list_shape
				get_curve_points = cmds.getAttr('%s.cv[*]' % curve_sel_list_shape[0])
				get_curve_degree = cmds.getAttr('%s.degree' % curve_sel_list_shape[0])
				# get_curve_spans = cmds.getAttr( '%s.spans'%curve_sel_list_shape[0])
				curve_info_node = cmds.createNode('curveInfo',
												  name="%s_controller_storage" % curve_sel_list_shape[0])
				cmds.connectAttr('%s.worldSpace' % curve_sel_list_shape[0],
								 '%s_controller_storage.inputCurve' % curve_sel_list_shape[0])
				get_curve_knots = cmds.getAttr('%s_controller_storage.knots[*]' % curve_sel_list_shape[0])
				cmds.delete(curve_info_node)
				# cmds.curve(degree=get_curve_degree, point=get_curve_points, knot=get_curve_knots)
				# save the script in the json file "curve_dict" first need to create a dict
				if os.stat(os.path.join(file_dir, file_name)).st_size == 0:
					print "Empty json file, adding first key"
					curve_dict = {
						"{}".format(curve_sel_list_shape[0]): "cmds.curve(degree={}, point={}, knot={})".format(
							get_curve_degree, get_curve_points,
							get_curve_knots)}  # to save a single key in dict, outside of if did not make any sense
					with open(os.path.join(file_dir, file_name), "w") as write_file:
						json.dump(curve_dict, write_file, indent=4)
						write_file.close()
				else:
					print "there are some keys in the json"
					# reading keys to get existing values in the variable
					with open(os.path.join(file_dir, file_name), "r") as read_file:
						curve_dict = json.load(read_file)
					# dict to dump with existing keys
					curve_dict[
						"{}".format(curve_sel_list_shape[0])] = "cmds.curve(degree={}, point={}, knot={})".format(
						get_curve_degree,
						get_curve_points,
						get_curve_knots)
					# write the values in the json with new and the old ones
					with open(os.path.join(file_dir, file_name), "w") as write_file:
						json.dump(curve_dict, write_file, indent=4)
						write_file.close()
			else:
				print "Kindly pick a 'kNurbsCurve'"
		else:
			print "Kindly select something in the scene"

	# CAVEAT : Read json will read the file for the dict and display in the listwidget
	def cs_read_json(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		self.cs_curve_dict_listwid.clear()
		with open(os.path.join(file_dir, file_name), "r") as read_file:
			curve_dict = json.load(read_file)
		keys = curve_dict.keys()
		for x in keys:
			QtWidgets.QListWidgetItem(x,
									  self.cs_curve_dict_listwid)  # Add the values in the listwid through listwiditem
		self.cs_curve_dict_listwid.setCurrentRow(0)  # Select the value in the listwidget already

	# CAVEAT : Create curve will create the curve from the selection of listwidget
	def cs_create_curve(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		if file_dir:
			with open(os.path.join(file_dir, file_name), "r") as read_file:
				curve_dict = json.load(read_file)
				exec curve_dict[QtWidgets.QListWidgetItem.text(
					self.cs_curve_dict_listwid.selectedItems()[0])]  # Creation of the selected curve in the listwid
		else:
			print "Kindly provide the file path"



if __name__ == "__main__":
	print "This is Main ControllerStorageUIFunc"
else:
	print "This is ControllerStorageUIFunc"
