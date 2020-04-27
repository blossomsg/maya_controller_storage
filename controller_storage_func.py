# func_module_for_ui
import maya.cmds as cmds
import controller_storage_ui
import os
import json


class ControllerStorageFunc(controller_storage_ui.ControllerStorageUI):
	"""This Class is Func for UI to preserve nurbs curve

	"""

	def __init__(self):
		super(ControllerStorageFunc, self).__init__()

		self.cs_duplicate_curve_qpushbutton.clicked.connect(self.cs_duplicate_button_func)
		self.cs_filename()
		self.cs_filepath()
		self.cs_preserve_curve_qpushbutton.setEnabled(False)
		self.cs_locate_create_curve_json_qpushbutton.clicked.connect(self.cs_locate_create_button)
		self.cs_preserve_curve_qpushbutton.clicked.connect(self.query_curve)

	# CAVEAT : This Duplicate curve func helps to duplicate the curve
	@staticmethod
	def cs_duplicate_button_func():
		cmds.duplicate()

	# CAVEAT : This Controller storage function stores the readonly file name
	def cs_filename(self):
		self.cs_json_file_name_qlineedit.setText("controller_storage.json")
		self.cs_json_file_name_qlineedit.setReadOnly(True)

	# CAVEAT : Controller storage directory path tooltip
	def cs_filepath(self):
		self.cs_locate_json_path_qlineedit.setToolTip("Provide an appropriate directory path")

	# CAVEAT : Locate/Create button func helps to create the .json file in the mentioned directory
	def cs_locate_create_button(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		if file_dir:
			filepath = os.path.join(file_dir, file_name)  # filepath of the dir
			if os.path.isfile(filepath):
				print "controller_storage.json File already exists"
				self.cs_preserve_curve_qpushbutton.setEnabled(True)
			else:
				with open(filepath, "w") as _controller_storage:
					pass  # this creates the .json file
				print "controller_storage.json File created"
				self.cs_preserve_curve_qpushbutton.setEnabled(True)
		else:
			print "Kindly provide directory path"

	# CAVEAT : Preserve curve button func will preserve the curve in a .json file
	def query_curve(self):
		file_dir = self.cs_locate_json_path_qlineedit.text()
		file_name = self.cs_json_file_name_qlineedit.text()
		curve_sel_list_shape = cmds.listRelatives()  # Result: [u'curveShape2'] #
		if curve_sel_list_shape:
			if cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve":
				print "It is a kNurbsCurve"
				# return curve_sel_list_shape
				# print curve_sel_list_shape
				if type(curve_sel_list_shape) == list:  # list so that the we can extract single value from it
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
						print "no keys at all"
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
						curve_dict["{}".format(curve_sel_list_shape[0])] = "cmds.curve(degree={}, point={}, knot={})".format(get_curve_degree,
																													get_curve_points,
																													get_curve_knots)
						# write the values in the json with new and the old ones
						with open(os.path.join(file_dir, file_name), "w") as write_file:
							json.dump(curve_dict, write_file, indent=4)
							write_file.close()
				else:
					print curve_sel_list_shape
			else:
				print "Kindly pick a 'kNurbsCurve'"
		else:
			print "Kindly select something in the scene"

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
