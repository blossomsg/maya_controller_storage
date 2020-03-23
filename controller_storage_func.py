import maya.cmds as cmds


# to preserve the shape of the curve
def query_curve():
	curve_sel_list_shape = cmds.listRelatives()
	if curve_sel_list_shape:
		if cmds.nodeType(curve_sel_list_shape[0], apiType=True) == "kNurbsCurve":
			print "It is a kNurbsCurve"
			return curve_sel_list_shape
		else:
			return "Kindly pick a 'kNurbsCurve'"
	else:
		return "Kindly select something in the scene"


curve_shape = query_curve()
if type(curve_shape) == list:
	# if we select curveshape directly that gives an error, kindly fix that in the function
	get_curve_points = cmds.getAttr('%s.cv[*]' % curve_shape[0])
	get_curve_degree = cmds.getAttr('%s.degree' % curve_shape[0])
	# get_curve_spans = cmds.getAttr( '%s.spans'%curve_shape[0])
	curve_info_node = cmds.createNode('curveInfo', name="%s_controller_storage" % curve_shape[0])
	cmds.connectAttr('%s.worldSpace' % curve_shape[0], '%s_controller_storage.inputCurve' % curve_shape[0])
	get_curve_knots = cmds.getAttr('%s_controller_storage.knots[*]' % curve_shape[0])
	cmds.delete(curve_info_node)
# cmds.curve(degree=get_curve_degree, point=get_curve_points, knot=get_curve_knots)
else:
	print curve_shape

# save the script in the json file "curve_dict" first need to create a dict
curve_dict = {
	"{}".format(curve_shape[0]): "cmds.curve(degree={}, point={}, knot={})".format(get_curve_degree, get_curve_points,
																				   get_curve_knots)}
# exec(curve_dict["trial_t_shirtShape"])
# then to append the another key values for more values
curve_dict["{}".format(curve_shape[0])] = "cmds.curve(degree={}, point={}, knot={})".format(get_curve_degree,
																							get_curve_points,
																							get_curve_knots)

import json

with open("D:\\All_Projs\\Maya_Projs\\controller_storage\\testing_data.json", "w") as write_file:
	json.dump(curve_dict, write_file, indent=4)
	write_file.close()

with open("D:\\All_Projs\\Maya_Projs\\controller_storage\\testing_data.json", "r") as read_file:
	testing = json.load(read_file)
	exec testing["type_curve_0Shape5"]
	print testing.keys()

# try to print json file contents
# try to update the json file with multiple values
# then try to fetch multiple values like first 1st, then second , thrid, after second point
#


#just to duplicate curve
cmds.duplicate()