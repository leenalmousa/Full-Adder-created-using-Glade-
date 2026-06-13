#------------------------------------------------------------------------------
#
# NMOS FreePDK15 pcell. 
#	Create a Pcell with parameters:
#       fins (discretised width)
#       fingers (number of gate fingers)
#	start (leftmost gate colour, 'A' or 'B')
#
# Note: The first argument is always the cellView of the subMaster.
#       All subsequent arguments should have default values and will
#       be passed by name. Each argument should be seperated by a comma
#	and whitespace. 
#
#------------------------------------------------------------------------------

# Import the db wrappers
from ui import *

# The entry point. The function name *must* match the filename.
def nmos_vtl(cv, fins=1, fingers=1, start='A') :
	lib = cv.lib()
	dbu = float(lib.dbuPerUU())
	
	# Error checking
	if (start != 'A') & (start != 'B') :
		print 'Start colour must be A or B'
		return
	startA = 0
	if start == 'A' :
		startA = 1
	if fins < 1 :
		print 'Error: Number of fins must be >= 1'
		return
	if fingers < 1 :
		print 'Error: Number of fingers must be >= 1'
		return
	
	# Some predefined rules for FreePDK15
	# 'width' is in the Y direction, 'length' is in the X direction.
	ail1_length = int(0.028 * dbu)
        gate_length = int(0.020 * dbu)
	gate_ext_act = int(0.076 * dbu)
	ail1_gate_spc = int(0.008 * dbu)
	act_minwidth = int(0.048 * dbu)
	act_incwidth = int(0.040 * dbu)
	ail1_ext_act = int(0.005 * dbu)
	act_ext_ail1 = int(0.002 * dbu)
	act_gate_spc = int(0.006 * dbu)
	nim_ovlp_act_x = int(0.030 * dbu)
	nim_ovlp_act_y = int(0.040 * dbu)
	vtl_ovlp_act_x = int(0.030 * dbu)
	vtl_ovlp_act_y = int(0.064 * dbu)

	# Create active. 
	tech = lib.tech()
	act_lyr = tech.getLayerNum("ACT", "drawing")
	width = act_minwidth + (fins-1) * act_incwidth
	length = fingers * (gate_length + ail1_length + ail1_gate_spc * 2) + 2 * act_ext_ail1 + ail1_length
	act_rect = Rect(-length/2, -width/2, length/2, width/2)
	active = cv.dbCreateRect(act_rect, act_lyr);

	# Create nim
	nim_lyr = tech.getLayerNum("NIM", "drawing")
	nim_rect = Rect(-length/2-nim_ovlp_act_x, -width/2-nim_ovlp_act_y, length/2+nim_ovlp_act_x, width/2+nim_ovlp_act_y)
	nim = cv.dbCreateRect(nim_rect, nim_lyr);

	# Create vtl
	vtl_lyr = tech.getLayerNum("VTL", "drawing")
	vtl_rect = Rect(-length/2-vtl_ovlp_act_x, -width/2-vtl_ovlp_act_y, length/2+vtl_ovlp_act_x, width/2+vtl_ovlp_act_y)
	vtl = cv.dbCreateRect(vtl_rect, vtl_lyr);
	
	# Create poly fingers
	polyA_lyr = tech.getLayerNum("GATEA", "drawing")
	polyB_lyr = tech.getLayerNum("GATEB", "drawing")
	ail1_lyr = tech.getLayerNum("AIL1", "drawing")
	
	# Create left dummy poly
	gate_rect = Rect(act_rect.left()-gate_length-act_gate_spc, act_rect.bottom()-gate_ext_act, act_rect.left()-act_gate_spc, act_rect.top()+gate_ext_act)
	if (startA) :
		cv.dbCreateRect(gate_rect, polyA_lyr);
	else :
		cv.dbCreateRect(gate_rect, polyB_lyr);
		
	x = act_rect.left() + 	act_ext_ail1
	for i in range(fingers) :
		
		# Create AIL1 shape
		ail1_rect = Rect(x , act_rect.bottom()-ail1_ext_act, x + ail1_length, act_rect.top()+ail1_ext_act)
		ail1_shape = cv.dbCreateRect(ail1_rect, ail1_lyr);
		if (i+1) % 2 :
			net = cv.dbCreateNet("S")
			pin = cv.dbCreatePin("S", net, DB_PIN_INOUT)
		else :
			net = cv.dbCreateNet("D")
			pin = cv.dbCreatePin("D", net, DB_PIN_INOUT)
		cv.dbCreatePort(pin, ail1_shape)
		
		# Move to gate x coord
		x = x + ail1_length + ail1_gate_spc
		
		# Create gate shape		
		gate_rect = Rect(x , act_rect.bottom()-gate_ext_act, x + gate_length, act_rect.top()+gate_ext_act)
		if (i+startA+1) % 2 :
			gate_shape = cv.dbCreateRect(gate_rect, polyA_lyr);
		else :
			gate_shape = cv.dbCreateRect(gate_rect, polyB_lyr);	
		net = cv.dbCreateNet("G")
		pin = cv.dbCreatePin("G", net, DB_PIN_INPUT)
		cv.dbCreatePort(pin, gate_shape)
		
		# add to x coord
		x = x + gate_rect.width() + ail1_gate_spc
		
	# Create 'last' AIL1 cut and gate
	ail1_rect = Rect(x , act_rect.bottom()-ail1_ext_act, x + ail1_length, act_rect.top()+ail1_ext_act)
	ail1_shape = cv.dbCreateRect(ail1_rect, ail1_lyr);
	if (fingers+1) % 2 :
		net = cv.dbCreateNet("S")
		pin = cv.dbCreatePin("S", net, DB_PIN_INOUT)
	else :
		net = cv.dbCreateNet("D")
		pin = cv.dbCreatePin("D", net, DB_PIN_INOUT)
	cv.dbCreatePort(pin, ail1_shape)
	
	x = x + ail1_length + ail1_gate_spc
	
	# Create right dummy poly
	gate_rect = Rect(x , act_rect.bottom()-gate_ext_act, x + gate_length, act_rect.top()+gate_ext_act)
	if (fingers+startA+1) % 2 :
		gate_shape = cv.dbCreateRect(gate_rect, polyA_lyr);
	else :
		gate_shape = cv.dbCreateRect(gate_rect, polyB_lyr);	

	
	# Device type
	cv.dbAddProp("type", "mos")

	# Update the bounding box
	cv.update()
