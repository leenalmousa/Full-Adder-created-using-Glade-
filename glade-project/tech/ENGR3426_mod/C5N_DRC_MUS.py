#------------------------------------------------------------------------------
#
# C5N SCMOS3ME_SUBM scalable design rules from MOSIS with lambda = 0.01um. 
#
#------------------------------------------------------------------------------
def printErrors(msg):
    n = geomGetCount()
    if n>0:
        print n, msg

num_errors = 0
def addErrors():
	global num_errors
	num_errors += geomGetCount()

#------------------------------------------------------------------------------
#
# Initialize the DRC package.
#
#------------------------------------------------------------------------------

from ui import *
cv = ui().getEditCellView()
lib = cv.lib()

geomBegin(cv)

LAMBDA = 0.01

#------------------------------------------------------------------------------
#
# Get raw layers.
#
#------------------------------------------------------------------------------

nwell = geomGetShapes('NWELL', 'drawing')
active = geomGetShapes('DIFF', 'drawing')
poly = geomGetShapes('POLY', 'drawing')
nplus = geomGetShapes('NPLUS', 'drawing')
pplus = geomGetShapes('PPLUS', 'drawing')
hires = geomGetShapes('hires', 'drawing')
contact = geomGetShapes('CONT', 'drawing')
metal1 = geomGetShapes('M1', 'drawing')
via12 = geomGetShapes('VIA12', 'drawing')
metal2 = geomGetShapes('M2', 'drawing')
via23 = geomGetShapes('VIA23', 'drawing')
metal3 = geomGetShapes('M3', 'drawing')
glass = geomGetShapes('glass', 'drawing')
pads = geomGetShapes('pads', 'drawing')
cap_id = geomGetShapes('cap_id', 'drawing')
res_id = geomGetShapes('res_id', 'drawing')
diode_id = geomGetShapes('diode_id', 'drawing')


#------------------------------------------------------------------------------
#
# Form derived layers.
#
#------------------------------------------------------------------------------

gate = geomAnd(poly, active)
ngate = geomAnd(gate, nplus)
pgate = geomAnd(gate, pplus)
diff = geomAndNot(active, gate)
ndiff = geomAnd(diff, nplus)
pdiff = geomAnd(diff, pplus)
nsrcdrain = geomAndNot(ndiff, nwell)
psrcdrain = geomAnd(pdiff, nwell)
nplug = geomAnd(ndiff, nwell)
pplug = geomAndNot(pdiff, nwell)
activecon = geomAnd(contact, active)
polycon = geomAnd(contact, poly)
bonding_passivation = geomAnd(glass, pads)
probe_passivation = geomAndNot(glass, pads)
pad_metal = geomAnd(metal3, pads)

#------------------------------------------------------------------------------
#
# Form connectivity.
#
#------------------------------------------------------------------------------

geomConnect([[nplug, nwell, ndiff],
             [activecon, ndiff, pdiff, metal1],
             [polycon, poly, metal1],
             [via12, metal1, metal2],
             [via23, metal2, metal3],
             [pads, metal3, pad_metal]])

#------------------------------------------------------------------------------
#
# Check design rules.
#
#------------------------------------------------------------------------------


#----------------------- Checking for off-grid geometry -----------------------#
print 'Checking for off-grid geometry...'
off_grid_msg = 'Design grid is {0!s}um x {1!s}um'.format(0.5*LAMBDA, 0.5*LAMBDA)
geomOffGrid(nwell, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(active, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(poly, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(nplus, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(pplus, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(hires, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(contact, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal1, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(via12, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal2, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(via23, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(metal3, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(glass, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(pads, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(cap_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(res_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)
geomOffGrid(diode_id, 0.5*LAMBDA, LAMBDA, off_grid_msg)

#----------------------- Checking for bad contacts -----------------------#
print 'Checking for bad contacts...'
saveDerived(geomAndNot(contact, geomOr(active, poly)), 'Contacts must be enclosed by diffusion or poly'); addErrors()
saveDerived(geomAndNot(geomOr(activecon, polycon), metal1), 'Contacts must be enclosed by M1'); addErrors()

#----------------------- Checking for bad vias -----------------------#
print 'Checking for bad vias...'
saveDerived(geomAndNot(via12, geomAnd(metal1, metal2)), 'VIA12 must be enclosed by M1 and M2'); addErrors()
saveDerived(geomAndNot(via23, geomAnd(metal2, metal3)), 'VIA23 must be enclosed by M2 and M3'); addErrors()

#----------------------- Checking for unselected diffusion -----------------------#
print 'Checking for unselected diffusion...'
saveDerived(geomAndNot(active, geomOr(nplus, pplus)), 'Diffusion must overlap pplus or nplus'); addErrors()

#----------------------- Checking well rules -----------------------#
print 'Checking well rules...'
geomWidth(nwell, 60*LAMBDA , '1.1 Well width >= 0.6u'); addErrors()
geomSpace(nwell, 60*LAMBDA , diffnet, '1.2 Spacing between wells at different potentials >= 0.6'); addErrors()
geomSpace(nwell, 30*LAMBDA , samenet, '1.3 Spacing between wells at same potential >= 0.3'); addErrors()
geomNotch(nwell, 30*LAMBDA , '1.3 Spacing between wells at same potential >= 0.3'); addErrors()

#----------------------- Checking diffusion rules -----------------------#
print 'Checking diffusion rules...'
geomWidth(active, 10*LAMBDA , '2.1 Diffusion width >= 0.1'); addErrors()
geomSpace(active, 5*LAMBDA , 0, '2.2 Diffusion spacing >= 0.05'); addErrors()
geomNotch(active, 5*LAMBDA , '2.2 Diffusion spacing >= 0.05'); addErrors()
geomEnclose(nwell, psrcdrain, 12*LAMBDA , '2.3 Source/drain diffusion to well edge >= 0.12'); addErrors()
geomSpace(nwell, nsrcdrain, 12*LAMBDA , 0, '2.3 Source/drain diffusion to well edge >= 0.12'); addErrors()
geomEnclose(nwell, nplug, 5*LAMBDA , '2.4 Substrate/well contact diffusion to well edge >= 0.05'); addErrors()
geomSpace(nwell, pplug, 5*LAMBDA , 0, '2.4 Substrate/well contact diffusion to well edge >= 0.05'); addErrors()
geomSpace(ndiff, geomAvoiding(ndiff, pdiff), 5*LAMBDA , 0, '2.5 Spacing between non-abutting diffusion of different implant >= 0.05'); addErrors()

#----------------------- Checking poly rules -----------------------#
print 'Checking poly rules...'
geomWidth(poly, 3*LAMBDA , '3.1 Poly width >= 0.03'); addErrors()
#geomAllowedWidths(poly, [0.028, 0.030, 0.04], horizontal, '3.1.5 allowed Poly width (0.028, 0.030, 0.04)'); addErrors()
geomSpace(poly, 8*LAMBDA , 0, '3.2 Poly spacing >= 0.08'); addErrors()
geomNotch(poly, 8*LAMBDA , '3.2 Poly spacing >= 0.08'); addErrors()
geomExtension(poly, active, 8*LAMBDA , '3.3 Poly extension of diffusion >= 0.08'); addErrors()
geomExtension(active, poly, 7.5*LAMBDA , '3.4 Diffusion extension of poly >= 0.075'); addErrors()
geomSpace(poly, active, 2.5*LAMBDA , 0, '3.5 Field poly to diffusion spacing >= 0.025'); addErrors()

#----------------------- Checking select rules -----------------------#
print 'Checking select rules...'
geomSpace(nplus, pgate, 4*LAMBDA , 0, '4.1 Select spacing to channel of tranistor to ensure adequate source/drain width >= 0.04'); addErrors()
geomSpace(pplus, ngate, 4*LAMBDA , 0, '4.1 Select spacing to channel of tranistor to ensure adequate source/drain width >= 0.04'); addErrors()
geomOverlap(nplus, active, 2*LAMBDA , '4.2 Select overlap of active >= 0.02'); addErrors()
geomOverlap(pplus, active, 2*LAMBDA , '4.2 Select overlap of active >= 0.02'); addErrors()
geomEnclose(nplus, activecon, LAMBDA , '4.3 Select overlap of contact >= 0.01'); addErrors()
geomEnclose(pplus, activecon, LAMBDA , '4.3 Select overlap of contact >= 0.01'); addErrors()
geomWidth(nplus, 10*LAMBDA , '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
geomWidth(pplus, 10*LAMBDA , '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
geomSpace(nplus, 10*LAMBDA , 0, '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
geomSpace(pplus, 10*LAMBDA , 0, '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
geomNotch(nplus, 10*LAMBDA , '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
geomNotch(pplus, 10*LAMBDA , '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()
saveDerived(geomAnd(nplus, pplus), '4.4 Select width and spacing >= 0.1 (Note: P-select and N-select may be coincident, but must not overlap)'); addErrors()

#----------------------- Checking poly contact rules -----------------------#
print 'Checking poly contact rules...'
geomArea(polycon, (4*LAMBDA )**2, (4*LAMBDA )**2, '5.1 Exact poly contact size = 0.04 x 0.04'); addErrors()
geomWidth(polycon, 4*LAMBDA , '5.1 Exact poly contact size = 0.04 x 0.04'); addErrors()
geomEnclose(poly, polycon, 1*LAMBDA , abut, '5.2 Poly overlap of poly contact all sides >= 0.01'); addErrors()
#############The below line needs the advanced rules feature to be enabled ############################################
###ADVANCED###geomAllowedEncs(metal1, polycon,[[0.05,0.3,2],[0.1,0.2,2]], '5.5 Metal1 overlap of poly contact 2 sides >= 0.3 with other 2 sides >=0.05'); addErrors()
#########################################################################################################################
#geomEnclose2(poly, polycon, 1*LAMBDA, 0.5*LAMBDA, 3*LAMBDA, 2, '5.2 Poly enclosed contact all sides >= 0.015, or >= -0.005 for parallel sides with other 2 sides >= 0.03'); addErrors()
#geomAllowedEncs(poly, polycon, [[LAMBDA, LAMBDA, 4], [0.5*LAMBDA, 1.5*LAMBDA, 4]], '5.2 Poly overlap of poly contact all sides >= 0.01'); addErrors() # needs the advanced rules feature to be enabled and I don't know how !!
geomSpace(polycon, 7*LAMBDA , 0, '5.3 Poly contact spacing >= 0.07'); addErrors()
geomSpace(polycon, active, 4*LAMBDA , 0, '5.4 Poly contact spacing to gate of transistor >= 0.04'); addErrors()
#geomSpace(polycon, gate, 4*LAMBDA , 0, '5.4 Poly contact spacing to gate of transistor >= 0.04'); addErrors()
geomEnclose2(metal1, polycon, 0.02, 0.005, 0.03, 2, '5.5 Metal1 overlap of Poly contact allsides >=0.02 , or 2 sides >= 0.03 with other 2 sides >=0.005'); addErrors()

#----------------------- Checking diffusion contact rules -----------------------#
print 'Checking diffusion contact rules...'
geomArea(activecon, (4*LAMBDA )**2, (4*LAMBDA )**2, '6.1 Exact diffusion contact size = 0.04 x 0.04'); addErrors()
geomWidth(activecon, 4*LAMBDA , '6.1 Exact diffusion contact size = 0.04 x 0.04'); addErrors()
geomEnclose2(active, activecon, 1.5*LAMBDA, 0.5*LAMBDA, 2*LAMBDA, 2, '6.2 Diffusion enclosed contact all sides >= 0.015, or >= 0.005 for one side with other 2 sides >= 0.02'); addErrors()
geomSpace(activecon, 7*LAMBDA , 0, '6.3 Diffusion contact spacing >= 0.07'); addErrors()
geomSpace(activecon, gate, 3.5*LAMBDA , 0, '6.4 Diffusion contact spacing to gate of transistor >= 0.035'); addErrors()
###ADVANCED###geomAllowedEncs(metal1, activecon,[[0.05,0.3,2],[0.1,0.2,2]], '6.5 Metal1 overlap of Diffusion contact 2 sides >= 0.3 with other 2 sides >=0.05'); addErrors()
geomEnclose2(metal1, activecon, 0.02, 0.005, 0.03, 2, '6.5 Metal1 overlap of Diffusion contact allsides >=0.02 , or 2 sides >= 0.03 with other 2 sides >=0.005'); addErrors()

#----------------------- Checking M1 rules -----------------------#
print 'Checking M1 rules...'
geomWidth(metal1, 0.05 , '7.1 M1 width >= 0.05'); addErrors()
geomSpace(metal1, 5*LAMBDA ,0 , '7.2 M1 spacing >= 0.05'); addErrors()
#############The below 3 lines needs some work by trying to give a range instead of value to the width###################
#geomSpace2(metal1, 8*LAMBDA ,7*LAMBDA,4*LAMBDA,0 ,  '7.22 M1 Line End to END spacing >= 0.08'); addErrors()
#geomSpace(metal1, 7*LAMBDA ,5*LAMBDA,0 ,0, '7.21 M1 Line End spacing >= 0.07'); addErrors()
#geomSpace(metal1, 5*LAMBDA ,7*LAMBDA,0,0 , '7.2 M1 spacing >= 0.05'); addErrors()
#########################################################################################################################
geomNotch(metal1, 5*LAMBDA , 0, '7.2 M1 spacing >= 0.05'); addErrors()
geomArea(metal1, (0.0057), 9e99, '7.10 M1 Area >=0.0057'); addErrors()
geomEnclose2(metal1, contact, 1.5*LAMBDA, 0.5*LAMBDA, 2*LAMBDA, 2, '7.3 M1 enclosed contact all sides >= 0.015, or >= 0.005 for parallel sides with other 2 sides >= 0.02'); addErrors()
#############The below 3 lines needs the advanced rules feature to be enabled ############################################
#layer = geomLineEnd(layer1, rule, num_ends, min_adj_edge_length=0.0, flags=0, const char *message=NULL)
###ADVANCED###geomLineEnd(metal1, 0.08, 2, 0, 0,'7.21 M1 Line End to END spacing >= 0.08'); addErrors()
###ADVANCED###geomLineEnd(metal1, 0.07, 1, 0, 0,'7.22 M1 Line End spacing >= 0.07'); addErrors()
#########################################################################################################################

#----------------------- Checking VIA12 rules -----------------------#
print 'Checking VIA12 rules...'
geomArea(via12, (5*LAMBDA )**2, (5*LAMBDA )**2, '8.1 Exact VIA12 size = 0.05 x 0.05'); addErrors()
geomWidth(via12, 4*LAMBDA , '8.1 Exact VIA12 size = 0.04 x 0.04'); addErrors()
geomSpace(via12, 7*LAMBDA , 0, '8.2 VIA12 spacing >= 0.07'); addErrors()
geomEnclose2(metal1, via12, 2.5*LAMBDA, 0.5*LAMBDA, 3.5*LAMBDA, 2, 'M1 enclosed contact all sides >= 0.025, or >= 0.005 for parallel sides with other 2 sides >= 0.035'); addErrors()
geomEnclose(metal2, via12, 3*LAMBDA , '14.3.1 M2 enclosed VIA12 two opisite sides >= 0.030'); addErrors()

#----------------------- Checking M2 rules -----------------------#
print 'Checking M2 rules...'
geomWidth(metal2, 5*LAMBDA , '9.1 M2 width >= 0.05'); addErrors()
geomSpace(metal2, 5*LAMBDA , 0, '9.2 M2 spacing >= 0.05'); addErrors()
geomNotch(metal2, 5*LAMBDA , 0, '9.2 M2 spacing >= 0.05'); addErrors()
geomEnclose2(metal1, via12, 2.5*LAMBDA, 0.5*LAMBDA, 3.5*LAMBDA, 2); addErrors()
wide_metal2 = geomSize(geomSize(metal2, -5.9*LAMBDA), 5.9*LAMBDA)
narrow_metal2 = geomAndNot(metal2, wide_metal2)
geomSpace(wide_metal2, narrow_metal2, 8*LAMBDA , '9.4 M2 spacing when either M2 line is wider than 0.12 >= 0.08'); addErrors()

#----------------------- Checking VIA23 rules -----------------------#
print 'Checking VIA23 rules...'
geomArea(via23, (4*LAMBDA )**2, (4*LAMBDA )**2, '14.1 Exact VIA23 size = 0.04 x 0.04'); addErrors()
geomWidth(via23, 4*LAMBDA , '14.1 Exact VIA23 size = 0.04 x 0.04'); addErrors()
geomSpace(via23, 7*LAMBDA , 0, '14.2 VIA23 spacing >= 0.07'); addErrors()
geomEnclose(metal2, via23, 0.5*LAMBDA , '14.3 M2 overlap of VIA23 >= 0.005'); addErrors()

#----------------------- Checking M3 rules -----------------------#
print 'Checking M3 rules...'
geomWidth(metal3, 6*LAMBDA , '15.1 M3 width >= 0.06'); addErrors()
geomSpace(metal3, 5*LAMBDA , 0, '15.2 M3 spacing >= 0.05'); addErrors()
geomNotch(metal3, 5*LAMBDA , 0, '15.2 M3 spacing >= 0.05'); addErrors()
geomEnclose(metal3, via23, LAMBDA , '15.3 M3 overlap of VIA23 >= 0.01'); addErrors()
wide_metal3 = geomSize(geomSize(metal3, -5.9*LAMBDA), 5.9*LAMBDA)
narrow_metal3 = geomAndNot(metal3, wide_metal3)
geomSpace(wide_metal3, narrow_metal3, 8*LAMBDA , '15.4 M3 spacing when either M3 line is wider than 0.12 >= 0.08'); addErrors()

#----------------------- Checking overglass rules -----------------------#
print 'Checking overglass rules...'
geomWidth(bonding_passivation, 60. , '10.1 Bonding passivation opening >= 60um'); addErrors()
geomWidth(probe_passivation, 20. , '10.2 Probe passivation opening >= 20um'); addErrors()
geomEnclose(metal3, glass, 6. , '10.3 Pad metal overlap of passivation >= 6um'); addErrors()
geomSpace(pad_metal, active, 15. , 0, '10.5 Pad spacing to active, poly, or poly2 >= 15um'); addErrors()
geomSpace(pad_metal, poly, 15. , 0, '10.5 Pad spacing to active, poly, or poly2 >= 15um'); addErrors()

if num_errors==0:
    print 'No DRC errors were found.'
else:
    print 'Found {0!s} DRC error{1}.'.format(num_errors, 's' if num_errors>1 else '')

# Exit DRC package, freeing memory.
geomEnd()

ui().winRedraw()
