# func_module_for_ui
from PySide2 import QtWidgets
from PySide2 import QtCore
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
		self.cs_curve_delete_qpushbutton.setEnabled(False)
		self.cs_locate_create_curve_json_qpushbutton.clicked.connect(self.cs_locate_create_button)
		self.settings = QtCore.QSettings()
		string_text = self.settings.value("path")
		self.cs_locate_json_path_qlineedit.setText(string_text)
		self.cs_preserve_curve_qpushbutton.clicked.connect(self.cs_query_curve)
		self.cs_read_json_file_qpushbutton.clicked.connect(self.cs_read_json)
		self.cs_curve_delete_qpushbutton.clicked.connect(self.cs_delete_json_keys)
		self.cs_create_selected_curve_qpushbutton.clicked.connect(self.cs_create_curve)

	# CAVEAT : Controller storage directory path tooltip
	def cs_tooltips(self):
		self.cs_duplicate_curve_qpushbutton.setToolTip("Creates duplicate of the curve on the spot")
		self.cs_locate_json_path_qlineedit.setToolTip("Provide an appropriate directory path")
		self.cs_preserve_curve_qpushbutton.setToolTip(
			"Enables once the json file location is confirmed,"
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
		self.settings.setValue("path", self.cs_locate_json_path_qlineedit.text())
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
			curve_type = cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve"
			print "It is a kNurbsCurve"
			if curve_type:
				curve_dict = {}
				curves = []
				curve_info_node_list = []
				# Saving multiple curveinfo in the above list
				for each_curve in curve_sel_list_shape:
					curve_info_node = cmds.createNode('curveInfo',
													  name="%s_controller_storage" % curve_sel_list_shape[0])
					curve_info_node_list.append(curve_info_node)
				# Below for loop helps to store multiple shape values in the list "curves"
				for x, y in zip(curve_sel_list_shape, curve_info_node_list):
					cmds.connectAttr('%s.worldSpace' % x,
									 '%s.inputCurve' % y)
					get_curve_knots = cmds.getAttr('%s.knots[*]' % y)
					get_curve_points = cmds.getAttr('%s.cv[*]' % x)
					get_curve_degree = cmds.getAttr('%s.degree' % x)
					# print get_curve_knots
					# print get_curve_points
					# print get_curve_degree
					curves.append("cmds.curve(degree={}, point={}, knot={})".format(
						get_curve_degree,
						get_curve_points,
						get_curve_knots))
					# print each_curve
				for x, y in zip(curve_sel_list_shape, curve_info_node_list):
					cmds.disconnectAttr('%s.worldSpace' % x, '%s.inputCurve' % y)
					cmds.delete(y)
				# print curves
				if os.stat(os.path.join(file_dir, file_name)).st_size == 0:  # checks the size of the json
					print "Empty json file, adding first key"
					curve_dict["{}".format(curve_sel_list_shape[0])] = curves
					# to save a single key in dict, outside of if statement did not make any sense
					with open(os.path.join(file_dir, file_name), "w") as write_file:
						json.dump(curve_dict, write_file, indent=4)
						write_file.close()
				else:
					print "there are some keys in the json"
					# reading keys to get existing values in the variable
					with open(os.path.join(file_dir, file_name), "r") as read_file:
						curve_dict = json.load(read_file)
					# dict to dump with existing keys
					# disabling below line does not dump the dict in .json, the above line overwrites the above variable
					curve_dict["{}".format(curve_sel_list_shape[0])] = curves
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
		self.cs_curve_delete_qpushbutton.setEnabled(True)
		self.cs_curve_dict_listwid.clear()
		with open(os.path.join(file_dir, file_name), "r") as read_file:
			curve_dict = json.load(read_file)
		keys = curve_dict.keys()
		for x in keys:
			QtWidgets.QListWidgetItem(x,
									  self.cs_curve_dict_listwid)  # Add the values in the listwid through listwiditem
		self.cs_curve_dict_listwid.setCurrentRow(0)  # Keep the first value selected in the listwidget

	def cs_delete_json_keys(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		with open(os.path.join(file_dir, file_name), "r") as read_file:  # read the json file
			curve_dict = json.load(read_file)
		# the selection from the list_wid is converted to text and deleted from the above variable(keys:values) dict
		del curve_dict[str(self.cs_curve_dict_listwid.currentItem().text())]  # delete the selected key from list_wid
		# print curve_dict.keys()
		with open(os.path.join(file_dir, file_name), "w") as write_file:  # dumping the updated key values in json
			json.dump(curve_dict, write_file, indent=4)
			write_file.close()
		self.cs_read_json()  # after deleting again read the updated json file

	# print self.cs_curve_dict_listwid.currentItem().text()

	# CAVEAT : Create curve will create the curve from the selection of listwidget
	def cs_create_curve(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		if file_dir:
			with open(os.path.join(file_dir, file_name), "r") as read_file:
				curve_dict = json.load(read_file)
			list_wid_sel = QtWidgets.QListWidgetItem.text(self.cs_curve_dict_listwid.selectedItems()[0])
			names_list = []
			# listwidget selection name to query in the curve_dict
			# for loop - to create multiple shapes if there are
			for create_curve in curve_dict.get(list_wid_sel):
				# print create_curve
				exec create_curve
				# maya curve command's own naming flags are buggy in maya 2020 so rename was best option
				# even works great with shape rename
				cmds.rename(list_wid_sel[:-5])
				# this part is mainly for multi shape, as it helps to get the len to proceed with next part of the code
				names_list.append(cmds.ls(sl=True))
			# if multi shape curve
			if len(names_list) > 1:
				names_flatten = [x for x in names_list for x in x]
				for x in names_flatten[1:]:
					for y in cmds.listRelatives(x):
						cmds.parent(y, names_flatten[0], relative=True, shape=True)
					cmds.delete(x)
		else:
			print "Kindly provide the file path"


if __name__ == "__main__":
	print "This is Main ControllerStorageUIFunc"
else:
	print "This is ControllerStorageUIFunc"
