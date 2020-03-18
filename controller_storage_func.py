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
print curve_shape
#if we select curveshape directly that gives an error, kindly fix that in the function
get_curve_points = cmds.getAttr( '%s.cv[*]'%curve_shape[0])
get_curve_degree = cmds.getAttr( '%s.degree'%curve_shape[0])
#get_curve_spans = cmds.getAttr( '%s.spans'%curve_shape[0])
curve_info_node = cmds.createNode( 'curveInfo', name="%s_controller_storage"%curve_shape[0])
cmds.connectAttr( '%s.worldSpace'%curve_shape[0], '%s_controller_storage.inputCurve'%curve_shape[0] )
get_curve_knots = cmds.getAttr( '%s_controller_storage.knots[*]'%curve_shape[0] )
cmds.delete(curve_info_node)



cmds.curve(degree=get_curve_degree, point=get_curve_points, knot=get_curve_knots)

#just to duplicate curve
cmds.duplicate()