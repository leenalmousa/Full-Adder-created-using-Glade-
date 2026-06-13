################################################################################
# FreePDK15 DRC deck.
# Peardrop Design Systems Ltd 2017
# Note: You need an advanced DRC license to run this DRC deck.
# Contact support@peardrop.co.uk for details.
################################################################################
# Initialise DRC package. 
from ui import *
cv = ui().getEditCellView()
geomBegin(cv)

print "Getting raw layers"
nwell     = geomGetShapes("NW", "drawing")
active    = geomGetShapes("ACT", "drawing")
vtl       = geomGetShapes("VTL", "drawing")
vth       = geomGetShapes("VTH", "drawing")
thkox     = geomGetShapes("THKOX", "drawing")
nimp      = geomGetShapes("NIM", "drawing")
pimp      = geomGetShapes("PIM", "drawing")
gatea     = geomGetShapes("GATEA", "drawing")
gateb     = geomGetShapes("GATEB", "drawing")
gateab    = geomGetShapes("GATEAB", "drawing")
gatec     = geomGetShapes("GATEC", "drawing")
ail1      = geomGetShapes("AIL1", "drawing")
ail2      = geomGetShapes("AIL2", "drawing")
gil       = geomGetShapes("GIL", "drawing")
v0        = geomGetShapes("V0", "drawing")
m1        = geomGetShapes("M1", "drawing")
m1a       = geomGetShapes("M1A", "drawing")
m1b       = geomGetShapes("M1B", "drawing")
v1        = geomGetShapes("V1", "drawing")
mint1     = geomGetShapes("MINT1", "drawing")
mint1a    = geomGetShapes("MINT1A", "drawing")
mint1b    = geomGetShapes("MINT1B", "drawing")
vint1     = geomGetShapes("VINT1", "drawing")
mint2     = geomGetShapes("MINT2", "drawing")
mint2a    = geomGetShapes("MINT2A", "drawing")
mint2b    = geomGetShapes("MINT2B", "drawing")
vint2     = geomGetShapes("VINT2", "drawing")
mint3     = geomGetShapes("MINT3", "drawing")
mint3a    = geomGetShapes("MINT3A", "drawing")
mint3b    = geomGetShapes("MINT3B", "drawing")
vint3     = geomGetShapes("VINT3", "drawing")
mint4     = geomGetShapes("MINT4", "drawing")
mint4a    = geomGetShapes("MINT4A", "drawing")
mint4b    = geomGetShapes("MINT4B", "drawing")
vint4     = geomGetShapes("VINT4", "drawing")
mint5     = geomGetShapes("MINT5", "drawing")
mint5a    = geomGetShapes("MINT5A", "drawing")
mint5b    = geomGetShapes("MINT5B", "drawing")
vint5     = geomGetShapes("VINT5", "drawing")
msmg1     = geomGetShapes("MSMG1", "drawing")
vsmg1     = geomGetShapes("VSMG1", "drawing")
msmg2     = geomGetShapes("MSMG2", "drawing")
vsmg2     = geomGetShapes("VSMG2", "drawing")
msmg3     = geomGetShapes("MSMG3", "drawing")
vsmg3     = geomGetShapes("VSMG3", "drawing")
msmg4     = geomGetShapes("MSMG4", "drawing")
vsmg4     = geomGetShapes("VSMG4", "drawing")
msmg5     = geomGetShapes("MSMG5", "drawing")
vsmg5     = geomGetShapes("VSMG5", "drawing")
mg1       = geomGetShapes("MG1", "drawing")
vg1       = geomGetShapes("VG1", "drawing")
mg2       = geomGetShapes("MG2", "drawing")
rectv0    = geomGetShapes("RECTV0", "drawing")
rectv1    = geomGetShapes("RECTV1", "drawing")
ncont     = geomGetShapes("NCONT", "drawing")

print "Generating derived layers"
gateaOrb  = geomOr(gatea, gateb)
allgate   = geomOr(gateaOrb, gateab)
gate      = geomAnd(allgate, active)
ngate     = geomAnd(gate, nimp)
pgate     = geomAnd(gate, pimp)
diff      = geomAndNot(active, gate)
ndiff     = geomAnd(diff, nimp)
pdiff     = geomAnd(diff, pimp)
ntap      = geomAnd(ndiff, nwell)
ptap      = geomAndNot(pdiff, nwell)

print "Extracting connectivity"
geomConnect( [
	          	[ntap, ndiff, nwell],
		[gil, gate],
		[ail1, ail2],
		[ail1, ndiff, pdiff, ail2],
	          	[v0, ail2, gil, m1, m1a, m1b],
	          	[v1, m1, m1a, m1a, mint1a, mint1b],
	          	[vint1, mint1, mint1a, mint1b, mint2, mint2a, mint2b],
	          	[vint2, mint2, mint2a, mint2b, mint3, mint3a, mint3b],
	          	[vint3, mint3, mint3a, mint3b, mint4, mint4a, mint4b],
	          	[vint4, mint4a, mint4b, mint5a, mint5b],
	          	[vint5, mint5, mint5a, mint5b, msmg1],
	          	[vsmg1, msmg1, msmg2],
	          	[vsmg2, msmg2, msmg3],
	          	[vsmg3, msmg3, msmg4],
	          	[vsmg4, msmg4, msmg5],
	          	[vsmg5, msmg5, mg1],
	          	[vg1, mg1, mg2]
	     ] )

if geomNumShapes(nwell) > 0 :
	print "Check NW"
	geomSpace(nwell, 0.180, diffnet, "NW space (different net) < 180nm (NW.1)")
	geomSpace(nwell, 0.110, samenet, "NW space < 110nm (NW.2)")
	geomWidth(nwell, 0.160, "NW width < 160nm (NW.3)")
	geomArea(nwell, 0.140, 9e99, "NW area < 0.140um^2 (NW.4A)")
	nwholes = geomHoles(nwell)
	geomArea(nwholes, 0.140, 9e99, "NW enclosed area < 0.140um^2 (NW.4B)")
	badnw = geomGetNon90(nwell)
	saveDerived(badnw, "NW must be orthogonal (NW.5)")
	geomExtension(nwell, gate, 0.080, "NW extension on gate < 80nm (NW.6)")

if geomNumShapes(active) > 0 :
	print "Check ACT"
	geomWidth(active, 0.048, horizontal, "ACT vertical width < 48nm (ACT.1)")
	geomAllowedWidths(active, [0.048, 0.088, 0.128, 0.168,
				   0.208, 0.248, 0.288, 0.328,
				   0.368, 0.408, 0.448, 0.488,
				   0.528, 0.568, 0.608, 0.648,
				   0.688, 0.728, 0.768, 0.808,
				   0.848, 0.888, 0.928, 0.968,
				   1.008], horizontal,
			  "ACT allowed vertical width 48nm or increments of 40nm (ACT.2)")
	geomSpace(active, 0.062, horizontal, "ACT vertical space < 62nm (ACT.3)")
	geomWidth(active, 0.096, vertical, "ACT horizontal width < 96nm (ACT.4)")
	geomAllowedSpaces(active, [0.032, 0.096, 0.160], vertical | project,
			  "ACT horizontal edge allowed space 32nm, 96nm or >=160nm (ACT.5)")
	geomNotch(active, 0.112, "ACT notch < 112nm (ACT.6)")
	geomSpace(nwell, active, 0.031, "NW spacing to ACT < 31nm (ACT.7A)")
	geomEnclose(nwell, active, 0.031, "NW enclosure of ACT < 31nm (ACT.7B)")
	geomArea(active, 0.004608, 9e99, "ACT area < 0.004608um^2 (ACT.8A)")
	actholes = geomHoles(active)
	geomArea(actholes, 0.004608, 9e99, "ACT enclosed area < 0.004608um^2 (ACT.8B)")
	sized_ptap = geomSize(ptap, 30.000)
	sized_ntap = geomSize(ntap, 30.000)
	bad_ngate = geomAndNot(ngate, sized_ptap)
	# need to check if both in same well
	saveDerived(bad_ngate, "Max distance from ngate to ptap 30um (ACT.9)")
	bad_pgate = geomAndNot(pgate, sized_ntap)
	# need to check if both in same well
	saveDerived(bad_pgate, "Max distance from pgate to ntap 30um (ACT.9)")

if geomNumShapes(gatea) > 0 :
	print "Check GATEA"
	geomAllowedWidths(gatea, [0.014, 0.016, 0.020, 9.999],
			  vertical, "GATEA allowed widths 14nm, 16nm, 20nm (GATE.1)")
	geomPitch(gatea, 0.128, vertical, "GATEA horizontal pitch != 128nm (GATE.2)")
	geomSpace(gatea, 0.044, vertical, "GATEA horizontal space < 44nm (GATE.3)")
	badpo = geomGetNon90(gatea)
	saveDerived(badpo, "GATEA must be orthogonal (GATEAB.4)")
	geomExtension(active, gatea, 0.038, "ACT extension on GATEA < 38nm (GATE.5)")
	geomExtension(gatea, active, 0.062, "GATEA Extension on ACT < 62nm (GATE.6)")
	geomWidth(gatea, 0.200, horizontal, "GATEA vertical length < 200nm (GATE.7)")
	gateanotc = geomAndNot(gatea, gatec)
	x = geomSize(gateanotc, 0.237)
	badga = geomAndNot(gatea, x)
	saveDerived(badga, "GATEA not GATEC max space to neighbour > 236nm (GATE.8)")

if geomNumShapes(gateb) > 0 :
	print "Check GATEB"
	geomAllowedWidths(gateb, [0.014, 0.016, 0.020, 9.999],
			  vertical, "GATEB allowed widths 14nm, 16nm, 20nm (GATE.1)")
	geomPitch(gateb, 0.128, vertical, "GATEB horizontal pitch != 128nm (GATE.2)")
	geomSpace(gateb, 0.044, vertical, "GATEB horizontal space < 44nm (GATE.3)")
	badpo = geomGetNon90(gateb)
	saveDerived(badpo, "GATEB must be orthogonal (GATEAB.4)")
	geomExtension(active, gateb, 0.038, "ACT extension on GATEB < 38nm (GATE.5)")
	geomExtension(gateb, active, 0.062, "GATEB Extension on ACT < 62nm (GATE.6)")
	geomWidth(gateb, 0.200, horizontal, "GATEB vertical length < 200nm (GATE.7)")
	gateanotc = geomAndNot(gateb, gatec)
	x = geomSize(gateanotc, 0.237)
	badga = geomAndNot(gateb, x)
	saveDerived(badga, "GATEB not GATEC max space to neighbour > 236nm (GATE.8)")

if geomNumShapes(gateab) > 0 :
	print "Check GATEAB"
	geomAllowedWidths(gateab, [0.014, 0.016, 0.020, 9.999],
			  vertical, "GATEAB allowed widths 14nm, 16nm, 20nm (GATE.1AB)")
	geomPitch(gateab, 0.064, vertical, "GATEAB horizontal pitch != 64nm (GATE.2AB)")
	geomSpace(gateab, 0.044, vertical, "GATEAB horizontal space < 44nm (GATE.3AB)")
	badpo = geomGetNon90(gateab)
	saveDerived(badpo, "GATE must be orthogonal (GATEAB.4AB)")
	geomExtension(active, gateab, 0.038, "ACT extension on GATE < 38nm (GATEAB.5AB)")
	geomExtension(gateab, active, 0.062, "GATE extension on ACT < 62nm (GATEAB.6AB)")
	geomWidth(gateab, 0.200, horizontal, "GATE vertical length < 200nm (GATEAB.7AB)")
	gateanotc = geomAndNot(gateab, gatec)
	x = geomSize(gateanotc, 0.237)
	badga = geomAndNot(gateab, x)
	saveDerived(badga, "GATEAB not GATEC max space to neighbour > 236nm (GATE.8AB)")

if geomNumShapes(gatec) > 0 :
	print "Check GATEC"
	geomWidth(gatec, 0.032, vertical | not_equal, "GATEC vertical width != 32nm (GATEC.1a)")
	geomWidth(gatec, 0.064, horizontal | not_equal, "GATEC horizontal width != 64nm (GATEC.1b)")
	geomLength(gatec, 0.128, horizontal, "GATEC horizontal length < 128nm (GATEC.2a)")
	geomLength(gatec, 0.064, vertical | not_equal, "GATEC vertical length != 64nm (GATEC.2b)")
	geomSpace(gatec, 0.128, 0, "GATEC space < 128nm (GATEC.3)")
	geomExtension(gatec, gate, 0.022, "GATEC extension on GATE < 22nm (GATEC.4)")
	geomSpace(gatec, active, 0.015, "GATEC space to ACT < 15nm (GATEC.5)")
	badgc = geomGetNon90(gate)
	saveDerived(badgc, "GATEC must be orthogonal (GATEC.6)")
	gatec_spc = geomSpace(gatec, 0.192, vertical | output_only)
	bad_gatec = geomGetNon90(gatec_spc)
	saveDerived(bad_gatec, "GATEC space < 192nm top/bottom misaligned (GATEC.7)")

if geomNumShapes(vtl) > 0 :
	print "Check VTL"
	geomWidth(vtl, 0.144, "VTL width < 114nm (VT.1)")
	geomSpace(vtl, 0.144, 0, "VTL space < 114nm (VT.2)")
	geomEnclose(gate, vtl, 0.064, "VTL enclose GATE < 64nm (VT.3)")
	geomSpace(gate, vtl, 0.044, "VTL space to GATE < 44nm (VT.4)")
	
if geomNumShapes(vth) > 0 :
	print "Check VTH"
	geomWidth(vth, 0.144, "VTH width < 114nm (VT.1)")
	geomSpace(vth, 0.144, 0, "VTH space < 114nm (VT.2)")
	geomEnclose(gate, vth, 0.064, "VTH enclose GATE < 64nm (VT.3)")
	geomSpace(gate, vth, 0.044, "VTH space to GATE < 44nm (VT.4)")

if geomNumShapes(nimp) > 0 :
	print "Check NIM"
	geomWidth(nimp, 0.128, "NIM width < 128nm (NIM.1)")
	geomSpace(nimp, 0.128, 0, "NIM space < 128nm (NIM.1)")
	geomNotch(nimp, 0.128, "NIM notch < 128nm (NIM.1)")
	geomSpace(nimp, gate, 0.032, 0, "NIM space to channel < 32nm (NIM.2)")
	geomExtension(nimp, gate, 0.032, horizontal, "NIM horizontal extension on ACT < 32nm (NIM.3)")
	geomExtension(nimp, gate, 0.030, vertical, "NIM vertical extension on ACT < 30nm (NIM.4)")
	geomSpace(nimp, active, 0.030, 0, "NIM space to ACT < 30nm (NIM.5)")
	geomEnclose(nimp, active, 0.030, "NIM enclosure ACT < 30nm (NIM.6)")
	geomArea(nimp, 0.049, 9e99, "NIM area < 0.049um (NIM.7)")

if geomNumShapes(pimp) > 0 :
	print "Check PIM"
	geomWidth(pimp, 0.128, "PIM width < 128nm (PIM.1)")
	geomSpace(pimp, 0.128, 0, "PIM space < 128nm (PIM.1)")
	geomNotch(pimp, 0.128, "PIM notch < 128nm (PIM.1)")
	geomSpace(pimp, gate, 0.032, 0, "PIM space to channel < 32nm (PIM.2)")
	geomExtension(pimp, gate, 0.032, horizontal, "PIM horizontal extension on ACT < 32nm (PIM.3)")
	geomExtension(pimp, gate, 0.030, vertical, "PIM vertical extension on ACT < 30nm (PIM.4)")
	geomSpace(pimp, active, 0.030, 0, "PIM space to ACT < 30nm (PIM.5)")
	geomEnclose(pimp, active, 0.030, "PIM enclosure ACT < 30nm (PIM.6)")
	geomArea(pimp, 0.049, 9e99, "PIM area < 0.049um (PIM.7)")

if geomNumShapes(ail1) > 0 :
	print "Check AIL1"
	geomWidth(ail1, 0.028, vertical, "AIL1 horizontal width < 28nm (AIL1.1)")
	geomSpace(ail1, 0.036, vertical, "AIL1 horizontal space < 36nm (AIL1.2)")
	geomSpace(ail1, gate, 0.008, "AIL1 space to GATE < 8nm (AIL1.3)")
	geomExtension(active, ail1, 0.002, horizontal, "ACT horizontal extension on AIL1 < 2nm (AIL1.4)")
	geomWidth(ail1, 0.058, horizontal, "AIL1 vertical length < 58nm (AIL1.5)")
	geomSpace(ail1, 0.062, horizontal, "AIL1 vertical spacing < 62nm (AIL1.6)")
	geomExtension(ail1, active, 0.000, horizontal, "AIL1 horizontal extension on ACT < 0nm (AIL1.7)")
	badail1 = geomGetNon90(ail1)
	saveDerived(badail1, "AIL1 must be orthogonal (AIL1.8)")

if geomNumShapes(ail2) > 0 :
	print "Check AIL2"
	geomWidth(ail2, 0.024, vertical, "AIL2 horizontal width < 24nm (AIL2.1)")
	geomSpace(ail2, 0.040, vertical, "AIL2 horizontal space < 40nm (AIL2.2)")
	geomSpace(ail2, gate, 0.002, "AIL2 space to GATE < 2nm (AIL2.3)")
	geomExtension(active, ail1, 0.002, horizontal, "ACT horizontal extension on AIL2 < 2nm (AIL1.4)")
	ail12 = geomAnd(ail1, ail2)
	geomWidth(ail12, 0.006, horizontal, "AIL1 & Ail2 minimum vertical overlap < 6 (AIL2.5)")
	geomWidth(ail2, 0.068, horizontal, "AIL2 vertical length < 68nm (AIL2.6)")
	geomSpace(ail2, 0.062, horizontal, "AIL2 vertical spacing < 62nm (AIL2.7)")
	badail2 = geomGetNon90(ail2)
	saveDerived(badail2, "AIL2 must be orthogonal (AIL2.8)")
	geomSpace(ail2, ail1, 0.016, diffnet | horizontal, "Diffnet horizontal spacing AIL1 to AIL2 < 16nm (AIL2.9)")
	geomSpace(ail2, ail1, 0.016, diffnet | vertical, "Diffnet vertical spacing AIL1 to AIL2 < 16nm (AIL2.10)")

if geomNumShapes(gil) > 0 :
	print "Check GIL"
	geomWidth(gil, 0.044, horizontal, "GIL vertical width < 44nm (GIL.1)")
	geomWidth(gil, 0.056, vertical, "GIL horizontal length < 56nm (GIL.2)")
	geomSpace(gil, 0.032, horizontal, "GIL vertical space < 32nm (GIL.3)")
	geomSpace(gil, 0.040, vertical, "GIL horizontal space < 40nm (GIL.4)")
	geomSpace(gil, active, 0.006, horizontal, "GIL vertical space to ACT < 6nm (GIL.5)")
	geomExtension(gil, gate, 0.002, "GIL horizontal extension on GATE < 2nm (GIL.6)")
	geomSpace(gil, ail2, 0.008, diffnet | horizontal, "Diffnet horizontal spacing GIL to AIL2 < 8nm (GIL.7)")
	geomSpace(gil, ail2, 0.005, horizontal, "Vertical spacing GIL to AIL2 < 5nm (GIL.8)")
	geomSpace(gil, gate, 0.010, vertical, "GIL horizontal space to GATE < 10nm (GIL.9)")
	geomOverlap(ail2, gil, 0.002, vertical, "AIL2 overlap GIL < 2nm (GIL.10)")
	geomExtension(ail2, gil, 0.004, "AIL2 extension GIL < 4nm (GIL.11)")
	badgil = geomGetNon90(gil)
	saveDerived(badgil, "GIL must be orthogonal (GIL.12)")

if geomNumShapes(v0) > 0 :
	print "Check V0"
	geomWidth(v0, 0.028, "V0 minimum edge length 28nm (V0.1a)")#
	geomAllowedSize(v0, [[0.028, 0.028],[0.028,0.056]], "V0 is rectangular 28x56nm (V0.1b)")
	geomSpace(v0, 0.036, "V0 minimum space < 36nm (V0.2)")
	# V0 space for projecting length < 28nm is 50nm (V0.3)
	gilm1 = geomAnd(gil, m1)
	v0gilm1 = geomAnd(gil, gilm1)
	geomSpace(v0, v0gilm1, 0.050, vertical | project, "V0 space for projecting length < 28nm is 50nm (V0.3)")
	ail2m1 = geomAnd(ail2, m1)
	v0ail2m1 = geomAnd(v0, ail2m1)
	geomSpace(v0, v0ail2m1, 0.050, vertical | project, "V0 space for projecting length < 28nm is 50nm (V0.3)")
	#
	ail2Orgil = geomOr(ail2,gil)
	m1aorm1b = geomOr(m1a, m1b)
	v0surround = geomAnd(ail2Orgil, m1aorm1b)
	badv0 = geomOutside(v0, v0surround)
	saveDerived(badv0, "V0 must be inside AIL2|GIL & METAL1 (V0.4)")
	geomEnclose(v0, ail2, 0.002, vertical, "V0 horizontal enclosure by AIL2 < -2nm (V0.5a)")
	geomEnclose(ail2, v0, 0.020, horizontal, "V0 vertical enclosure by AIL2 < 20nm (V0.5b)")
	gilAndail2 = geomAnd(ail2, gil)
	geomEnclose(v0, gilAndail2, 0.002, vertical, "V0 horizontal enclosure by AIL2&GIL < -2nm (V0.6a)")
	geomEnclose(gilAndail2, v0, 0.020, horizontal, "V0 vertical enclosure by AIL2&GIL < 20nm (V0.6b)")
	gilAndNotail2 = geomAndNot(gil, ail2)	    
	geomEnclose(gilAndNotail2, v0, 0.014, vertical, "V0 horizontal enclosure by AIL2^GIL < 14nm (V0.7a)")
	geomEnclose(gilAndNotail2, v0, 0.008, horizontal, "V0 vertical enclosure by AIL2^GIL < 8nm (V0.7b)")
	geomSpace(v0, ail2, 0.038, diffnet, "Diffnet spacing V0 to AIL2 < 38nm (V0.8)")
	geomSpace(v0, gil, 0.006, diffnet, "Diffnet spacing V0 to GIL < 6nm (V0.9)")
	v0andgil = geomAnd(v0, gil)
	badv0 = geomOverlap(v0andgil, gate, 0)
	saveDerived(badv0, "V0 enclosed by GIL may not overlap GATEAB over ACT (V0.10)")

if geomNumShapes(m1) > 0 :
	print "Check M1"
	geomWidth(m1, 0.028, "M1 width < 28 (M1.1)")
	geomAdjLength(m1, 0.056, 0.056, 0, "M1 adjacent edge < 56nm (M1.2)")
	minm1 = geomWidth(m1, 0.028, equal | output_only | opposite)
	geomLength(minm1, 1.800, greater, "M1 length with width=28nm > 1.8um (M1.3)")
	geomLineEnd(m1, 0.068, 1, 0.032, 0, "M1 minimum end-of-line space < 68nm (M1.4)")
	geomSpace(m1, 0.054, "M1 minimum space < 54nm (M1.5)")
	geomNotch(m1, 0.054, "M1 minimum notch < 54nm (M1.5)")
	geom2DSpace(m1,  [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
                [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
                [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
                [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
                [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
                [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
                [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "M1 Minimum spacing (M1.8-21)")
	geomAllowedEncs(m1, v0, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ],
			"M1 allowed enclosure of V0 (M1.23)")
	m1gt60 = geomSize(m1, -0.060)
	widem1 = geomSize(m1gt60, 0.060)
	v0inm1 = geomAnd(v0, widem1)
	geomAllowedSize(v0inm1, [[0.028, 0.056]], "V0 must be rectangular if M1 width > 60nm (M1.26)")
	rectm1 = geomGetRectangles(m1)
	geomArea(rectm1, 0.0024, 9e99, "M1 minimum area for rectangular shape (M1.27)")
	polym1 = geomGetPolygons(m1)
	geomArea(polym1, 0.0036, 9e99, "M1 minimum area for non-rectangular shape (M1.28)")

if geomNumShapes(m1a) > 0 :
	print "Check M1A"
	geomWidth(m1a, 0.028, "M1A width < 28 (M1.1)")
	geomAdjLength(m1a, 0.056, 0.056, 0, "M1A adjacent edge < 56nm (M1.2)")
	minm1a = geomWidth(m1a, 0.028, equal | output_only | opposite)
	geomLength(minm1a, 1.800, greater, "M1A length with width=28nm > 1.8um (M1.3)")
	geomLineEnd(m1a, 0.068, 1, 0.032, 0, "M1A minimum end-of-line space < 68nm (M1.4)")
	geomSpace(m1a, 0.054, "M1A minimum space < 54nm (M1.5)")
	geomNotch(m1a, 0.054, "M1A minimum notch < 54nm (M1.5)")
	geomSpace(m1a, m1b, 0.036, "M1A space to M1B (M1.6)")
	geomLineEnd(m1a, m1b, 0.044, 1, 0.032, 0, "M1A to M1B minimum end-of-line space < 44nm (M1.7)")
	geom2DSpace(m1a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
                [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
                [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
                [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
                [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
                [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
                [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "M1A Minimum spacing (M1.8-21)")
	geomOverlap(m1a, m1b, 0.040, 0, "M1A overlap M1B < 40nm (M1.22)")
	geomAllowedEncs(m1a, v0, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ],
			"MaA allowed enclosure of V0(M1.23)")
	m1ab = geomAnd(m1a, m1b)
	geomAllowedEncs(m1ab, v0, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ],
			"M1A&M1B allowed enclosure of V0(M1.24)")
	m1agt60 = geomSize(m1a, -0.060)
	widem1 = geomSize(m1agt60, 0.060)
	v0inm1 = geomAnd(v0, widem1)
	geomAllowedSize(v0inm1, [[0.028, 0.056]], "V0 must be rectangular if M1 width > 60nm (M1.26)")
	rectm1a = geomGetRectangles(m1a)
	geomArea(rectm1a, 0.0024, 9e99, "M1A minimum area for rectangular shape (M1.27)")
	polym1a = geomGetPolygons(m1a)
	geomArea(polym1a, 0.0036, 9e99, "M1A minimum area for non-rectangular shape (M1.28)")

if geomNumShapes(m1b) > 0 :
	print "Check M1B"
	geomWidth(m1b, 0.028, "M1B width < 28 (M1.1)")
	geomAdjLength(m1b, 0.056, 0.056, 0, "M1B adjacent edge < 56nm (M1.2)")
	minm1b = geomWidth(m1b, 0.028, equal | output_only | opposite)
	geomLength(minm1b, 1.800, greater, "M1B length with width=28nm > 1.8um (M1.3)")
	geomLineEnd(m1b, 0.068, 1, 0.032, 0, "M1B minimum end-of-line space < 68nm (M1.4)")
	geomSpace(m1b, 0.054, "M1B minimum space < 54nm (M1.5)")
	geomNotch(m1b, 0.054, "M1B minimum notch < 54nm (M1.5)")
	geom2DSpace(m1b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
                [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
                [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
                [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
                [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
                [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
                [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "M1B Minimum spacing (M1.8-21)")
	geomAllowedEncs(m1b, v0, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ],
			"M1B allowed enclosure of V0(M1.23)")
	m1bgt60 = geomSize(m1a, -0.060)
	widem1 = geomSize(m1bgt60, 0.060)
	v0inm1 = geomAnd(v0, widem1)
	geomAllowedSize(v0inm1, [[0.028, 0.056]], "V0 must be rectangular if M1 width > 60nm (M1.26)")
	rectm1b = geomGetRectangles(m1b)
	geomArea(rectm1b, 0.0024, 9e99, "M1B minimum area for rectangular shape (M1.27)")
	polym1a = geomGetPolygons(m1b)
	geomArea(polym1a, 0.0036, 9e99, "M1B minimum area for non-rectangular shape (M1.28)")
	
if geomNumShapes(v1) > 0 :
	print "Check V1"
	geomWidth(v1, 0.028, "V1 minimum edge length 28nm (V1.1.a)")#
	geomAllowedSize(v1, [[0.028, 0.028],[0.028,0.056]], "V1 is rectangular 28x56nm (V1.1b)")
	geomSpace(v1, 0.036, "V1 minimum space < 36nm (V1.2)")
	# V1 space for projecting length < 28nm is 50nm (V1.3)
	m1mint1 = geomAnd(m1, mint1)
	v1m1mint1 = geomAnd(v1, m1mint1)
	geomSpace(v1, v1m1mint1, 0.050, vertical | project, "V1 space for projecting length < 28nm is 50nm (V1.3)")
	#
	m1amint1a = geomAnd(m1a, mint1a)
	m1bmint1b = geomAnd(m1b, mint1b)
	m1bmint1a = geomAnd(m1b, mint1a)
	m1amint1b = geomAnd(m1a, mint1b)
	#m1mint1 = geomAnd(m1, mint1)
	allmimint1 = geomOr(m1mint1, geomOr(m1amint1b, geomOr(m1bmint1a, geomOr(m1amint1a, m1bmint1b))))
	badv1 = geomOutside(v1, allmimint1)
	saveDerived(badv1, "V1 must be inside M1 & MINT1 (V1.4)")

if geomNumShapes(mint1) > 0 :
	print "Check MINT1"
	geomWidth(mint1, 0.028, "MINT1 width < 28 (MINT1.1)")
	geomAdjLength(mint1, 0.056, 0.056, 0, "MINT1 adjacent edge < 56nm (MINT1.2)")
	minmint1 = geomWidth(mint1, 0.028, equal | output_only | opposite)
	geomLength(minmint1, 1.800, greater, "MINT1 length with width=28nm > 1.8um (MINT1.3)")
	geomLineEnd(mint1, 0.068, 1, 0.032, 0, "MINT1 minimum end-of-line space < 68nm (MINT1.4)")
	geomSpace(mint1, 0.054, "MINT1 minimum space < 54nm (MINT1.5)")
	geomNotch(mint1, 0.054, "MINT1 minimum notch < 54nm (MINT1.5)")
	geom2DSpace(mint1, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
                [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
                [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT1 Minimum spacing (MINT1.8-21)")
	geomAllowedEncs(mint1, v1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT1 allowed enclosure of V1(MINT1.23)")
	mint1gt60 = geomSize(mint1, -0.060)
	widemint1 = geomSize(mint1gt60, 0.060)
	v1inmint1 = geomAnd(v1, widemint1)
	geomAllowedSize(v1inmint1, [[0.028, 0.056]], "V1 must be rectangular if MINT1 width > 60nm (MINT1.26)")
	rectmint1 = geomGetRectangles(mint1)
	geomArea(rectmint1, 0.0024, 9e99, "MINT1 minimum area for rectangular shape (MINT1.27)")
	polymint1 = geomGetPolygons(mint1)
	geomArea(polymint1, 0.0036, 9e99, "MINT1 minimum area for non-rectangular shape (MINT1.28)")

if geomNumShapes(mint1a) > 0 :
	print "Check MINT1A"
	geomWidth(mint1a, 0.028, "MINT1A width < 28 (MINT1.1)")
	geomAdjLength(mint1a, 0.056, 0.056, 0, "MINT1A adjacent edge < 56nm (MINT1.2)")
	minmint1a = geomWidth(mint1a, 0.028, equal | output_only | opposite)
	geomLength(minmint1a, 1.800, greater, "MINT1A length with width=28nm > 1.8um (MINT1.3)")
	geomLineEnd(mint1a, 0.068, 1, 0.032, 0, "MINT1A minimum end-of-line space < 68nm (MINT1.4)")
	geomSpace(mint1a, 0.054, "MINT1A minimum space < 54nm (MINT1.5)")
	geomNotch(mint1a, 0.054, "MINT1A minimum notch < 54nm (MINT1.5)")
	geomSpace(mint1a, mint1b, 0.036, "MINT1A space to MINT1B (MINT1.6)")
	geomLineEnd(mint1a, mint1b, 0.044, 1, 0.032, 0, "MINT1A to MINT1B minimum end-of-line space < 44nm (MINT1.7)")
	geom2DSpace(mint1a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT1A Minimum spacing (MINT1.8-21)")
	geomOverlap(mint1a, mint1b, 0.040, 0, "MINT1A overlap MINT1B < 40nm (MINT1.22)")
	geomAllowedEncs(mint1a, v1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT1A allowed enclosure of V1(MINT1.23)")
	mint1amint1b = geomAnd(mint1a, mint1b)
	geomAllowedEncs(mint1amint1b, v1, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ], "MINT1A allowed enclosure of V1 (MINT1.24)")
	mint1agt60 = geomSize(mint1a, -0.060)
	widemint1 = geomSize(mint1agt60, 0.060)
	v1inmint1 = geomAnd(v1, widemint1)
	geomAllowedSize(v1inmint1, [[0.028, 0.056]], "V1 must be rectangular if MINT1A width > 60nm (MINT1.26)")
	rectmint1a = geomGetRectangles(mint1a)
	geomArea(rectmint1a, 0.0024, 9e99, "MINT1A minimum area for rectangular shape (MINT1.27)")
	polymint1a = geomGetPolygons(mint1a)
	geomArea(polymint1a, 0.0036, 9e99, "MINT1A minimum area for non-rectangular shape (MINT1.28)")

if geomNumShapes(mint1b) > 0 :
	print "Check MINT1B"
	geomWidth(mint1b, 0.028, "MINT1B width < 28 (MINT1.1)")
	geomAdjLength(mint1b, 0.056, 0.056, 0, "MINT1B adjacent edge < 56nm (MINT1.2)")
	minmint1b = geomWidth(mint1b, 0.028, equal | output_only | opposite)
	geomLength(minmint1b, 1.800, greater, "MINT1B length with width=28nm > 1.8um (MINT1.3)")
	geomLineEnd(mint1b, 0.068, 1, 0.032, 0, "MINT1B minimum end-of-line space < 68nm (MINT1.4)")
	geomSpace(mint1b, 0.054, "MINT1B minimum space < 54nm (MINT1.5)")
	geomNotch(mint1b, 0.054, "MINT1B minimum notch < 54nm (MINT1.5)")
	geom2DSpace(mint1b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT1B Minimum spacing (MINT1.8-21)")
	geomAllowedEncs(mint1b, v1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT1B allowed enclosure of V1(MINT1.23)")
	mint1bgt60 = geomSize(mint1a, -0.060)
	widemint1 = geomSize(mint1bgt60, 0.060)
	v1inmint1 = geomAnd(v1, widemint1)
	geomAllowedSize(v1inmint1, [[0.028, 0.056]], "V1 must be rectangular if MINT1B width > 60nm (MINT1.26)")
	rectmint1b = geomGetRectangles(mint1b)
	geomArea(rectmint1b, 0.0024, 9e99, "MINT1B minimum area for rectangular shape (MINT1.27)")
	polymint1b = geomGetPolygons(mint1b)
	geomArea(polymint1b, 0.0036, 9e99, "MINT1B minimum area for non-rectangular shape (MINT1.28)")
	
if geomNumShapes(vint1) > 0 :
	print "Check VINT1"
	geomWidth(vint1, 0.028, "VINT1 minimum edge length 28nm (VINT1.1a)")#
	geomAllowedSize(vint1, [[0.028, 0.028],[0.028,0.056]], "VINT1 is rectangular 28x56nm (VINT1.1b)")
	geomSpace(vint1, 0.036, "VINT1 minimum space < 36nm (VINT1.2)")
	# VINT1 space for projecting length < 28nm is 50nm (VINT1.3)
	mint1mint2 = geomAnd(mint1, mint2)
	vint1mint1mint1 = geomAnd(vint1, mint1mint2)
	geomSpace(vint1, vint1mint1mint1, 0.050, vertical | project, "VINT1 space for projecting length < 28nm is 50nm (VINT1.3)")
	#
	mint1amint2a = geomAnd(mint1a, mint2a)
	mint1bmint2b = geomAnd(mint1b, mint2b)
	mint1bmint2a = geomAnd(mint1b, mint2a)
	mint1amint2b = geomAnd(mint1a, mint2b)
	#mint1mint2 = geomAnd(mint1, mint2)
	allmint1mint2 = geomOr(mint1mint2, geomOr(mint1amint2b, geomOr(mint1bmint2a, geomOr(mint1amint2a, mint1bmint2b))))
	badvint1 = geomOutside(vint1, allmint1mint2)
	saveDerived(badvint1, "VINT1 must be inside MINT1 & MINT2 (VINT1.4)")

if geomNumShapes(mint2) > 0 :
	print "Check MINT2"
	geomWidth(mint2, 0.028, "MINT2 width < 28 (MINT2.1)")
	geomAdjLength(mint2, 0.056, 0.056, 0, "MINT2 adjacent edge < 56nm (MINT2.2)")
	minmint2 = geomWidth(mint2, 0.028, equal | output_only | opposite)
	geomLength(minmint2, 1.800, greater, "MINT2 length with width=28nm > 1.8um (MINT2.3)")
	geomLineEnd(mint2, 0.068, 1, 0.032, 0, "MINT2 minimum end-of-line space < 68nm (MINT2.4)")
	geomSpace(mint2, 0.054, "MINT2 minimum space < 54nm (MINT2.5)")
	geomNotch(mint2, 0.054, "MINT2 minimum notch < 54nm (MINT2.5)")
	geom2DSpace(mint2, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT2 Minimum spacing (MINT2.8-21)")
	geomAllowedEncs(mint2, vint1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT2 allowed enclosure of VINT1 (MINT1.23)")
	mint2gt60 = geomSize(mint2, -0.060)
	widemint2 = geomSize(mint2gt60, 0.060)
	vint1inmint2 = geomAnd(vint1, widemint2)
	geomAllowedSize(vint1inmint2, [[0.028, 0.056]], "VINT1 must be rectangular if MINT2 width > 60nm (MINT2.26)")
	rectmint2 = geomGetRectangles(mint2)
	geomArea(rectmint2, 0.0024, 9e99, "MINT2 minimum area for rectangular shape (MINT2.27)")
	polymint2 = geomGetPolygons(mint1)
	geomArea(polymint2, 0.0036, 9e99, "MINT2 minimum area for non-rectangular shape (MINT2.28)")

if geomNumShapes(mint2a) > 0 :
	print "Check MINT2A"
	geomWidth(mint2a, 0.028, "MINT2A width < 28 (MINT2.1)")
	geomAdjLength(mint2a, 0.056, 0.056, 0, "MINT2A adjacent edge < 56nm (MINT2.2)")
	minmint2a = geomWidth(mint2a, 0.028, equal | output_only | opposite)
	geomLength(minmint2a, 1.800, greater, "MINT2A length with width=28nm > 1.8um (MINT2.3)")
	geomLineEnd(mint2a, 0.068, 1, 0.032, 0, "MINT2A minimum end-of-line space < 68nm (MINT2.4)")
	geomSpace(mint2a, 0.054, "MINT2A minimum space < 54nm (MINT2.5)")
	geomNotch(mint2a, 0.054, "MINT2A minimum notch < 54nm (MINT2.5)")
	geomSpace(mint2a, mint1b, 0.036, "MINT1A space to MINT1B (MINT2.6)")
	geomLineEnd(mint2a, mint2b, 0.044, 1, 0.032, 0, "MINT2A to MINT2B minimum end-of-line space < 44nm (MINT2.7)")
	geom2DSpace(mint2a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT1A Minimum spacing (MINT1.8-21)")
	geomOverlap(mint2a, mint2b, 0.040, 0, "MINT2A overlap MINT2B < 40nm (MINT2.22)")
	geomAllowedEncs(mint2a, vint1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT2A allowed enclosure of VINT1 (MINT2.23)")
	mint2amint2b = geomAnd(mint2a, mint2b)
	geomAllowedEncs(mint2amint2b, vint1, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ], "MINT2A allowed enclosure of VINT1 (MINT2.24)")
	mint2agt60 = geomSize(mint2a, -0.060)
	widemint2 = geomSize(mint2agt60, 0.060)
	vint1inmint2 = geomAnd(vint1, widemint2)
	geomAllowedSize(vint1inmint2, [[0.028, 0.056]], "VINT1 must be rectangular if MINT2A width > 60nm (MINT2.26)")
	rectmint2a = geomGetRectangles(mint1a)
	geomArea(rectmint2a, 0.0024, 9e99, "MINT2A minimum area for rectangular shape (MINT2.27)")
	polymint2a = geomGetPolygons(mint2a)
	geomArea(polymint2a, 0.0036, 9e99, "MINT2A minimum area for non-rectangular shape (MINT2.28)")

if geomNumShapes(mint2b) > 0 :
	print "Check MINT2B"
	geomWidth(mint2b, 0.028, "MINT2B width < 28 (MINT2.1)")
	geomAdjLength(mint2b, 0.056, 0.056, 0, "MINT2B adjacent edge < 56nm (MINT2.2)")
	minmint2b = geomWidth(mint2b, 0.028, equal | output_only | opposite)
	geomLength(minmint2b, 1.800, greater, "MINT2B length with width=28nm > 1.8um (MINT2.3)")
	geomLineEnd(mint2b, 0.068, 1, 0.032, 0, "MINT2B minimum end-of-line space < 68nm (MINT2.4)")
	geomSpace(mint2b, 0.054, "MINT2B minimum space < 54nm (MINT2.5)")
	geomNotch(mint2b, 0.054, "MINT2B minimum notch < 54nm (MINT2.5)")
	geom2DSpace(mint2b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT2A Minimum spacing (MINT2.8-21)")
	geomAllowedEncs(mint2b, vint1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT2B allowed enclosure of VINT1 (MINT2.23)")
	mint2bgt60 = geomSize(mint2b, -0.060)
	widemint2 = geomSize(mint2bgt60, 0.060)
	vint1inmint2 = geomAnd(vint1, widemint2)
	geomAllowedSize(vint1inmint2, [[0.028, 0.056]], "VINT1 must be rectangular if MINT2B width > 60nm (MINT2.26)")
	rectmint2b = geomGetRectangles(mint2b)
	geomArea(rectmint2b, 0.0024, 9e99, "MINT2B minimum area for rectangular shape (MINT2.27)")
	polymint2b = geomGetPolygons(mint2b)
	geomArea(polymint2b, 0.0036, 9e99, "MINT1B minimum area for non-rectangular shape (MINT2.28)")
	
if geomNumShapes(vint2) > 0 :
	print "Check VINT2"
	geomWidth(vint2, 0.028, "VINT2 minimum edge length 28nm (VINT2.1a)")#
	geomAllowedSize(vint2, [[0.028, 0.028],[0.028,0.056]], "VINT2 is rectangular 28x56nm (VINT2.1b)")
	geomSpace(vint2, 0.036, "VINT2 minimum space < 36nm (VINT2.2)")
	# VINT2 space for projecting length < 28nm is 50nm (VINT2.3)
	mint2mint3 = geomAnd(mint2, mint3)
	vint2mint2mint3 = geomAnd(vint2, mint2mint3)
	geomSpace(vint2, vint2mint2mint3, 0.050, vertical | project, "VINT2 space for projecting length < 28nm is 50nm (VINT2.3)")
	#
	mint2amint3a = geomAnd(mint2a, mint3a)
	mint2bmint3b = geomAnd(mint2b, mint3b)
	mint2bmint3a = geomAnd(mint2b, mint3a)
	mint2amint3b = geomAnd(mint2a, mint3b)
	#mint2mint3 = geomAnd(mint2, mint3)
	allmint2mint3 = geomOr(mint2mint3, geomOr(mint2amint3b, geomOr(mint2bmint3a, geomOr(mint2amint3a, mint2bmint3b))))
	badvint2 = geomOutside(vint2, allmint2mint3)
	saveDerived(badvint2, "VINT2 must be inside MINT2 & MINT3 (VINT2.4)")

if geomNumShapes(mint3) > 0 :
	print "Check MINT3"
	geomWidth(mint3, 0.028, "MINT3 width < 28 (MINT3.1)")
	geomAdjLength(mint3, 0.056, 0.056, 0, "MINT3 adjacent edge < 56nm (MINT3.2)")
	minmint3 = geomWidth(mint3, 0.028, equal | output_only | opposite)
	geomLength(minmint3, 1.800, greater, "MINT3 length with width=28nm > 1.8um (MINT3.3)")
	geomLineEnd(mint3, 0.068, 1, 0.032, 0, "MINT3 minimum end-of-line space < 68nm (MINT3.4)")
	geomSpace(mint3, 0.054, "MINT3 minimum space < 54nm (MINT3.5)")
	geomNotch(mint3, 0.054, "MINT3 minimum notch < 54nm (MINT3.5)")
	geom2DSpace(mint3, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT3 Minimum spacing (MINT3.8-21)")
	geomAllowedEncs(mint3, vint2, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT3 allowed enclosure of VINT2 (MINT3.23)")
	mint3gt60 = geomSize(mint3, -0.060)
	widemint3 = geomSize(mint3gt60, 0.060)
	vint2inmint3 = geomAnd(vint2, widemint3)
	geomAllowedSize(vint2inmint3, [[0.028, 0.056]], "VINT2 must be rectangular if MINT3 width > 60nm (MINT3.26)")
	rectmint3 = geomGetRectangles(mint3)
	geomArea(rectmint3, 0.0024, 9e99, "MINT3 minimum area for rectangular shape (MINT3.27)")
	polymint3 = geomGetPolygons(mint3)
	geomArea(polymint3, 0.0036, 9e99, "MINT3 minimum area for non-rectangular shape (MINT3.28)")

if geomNumShapes(mint3a) > 0 :
	print "Check MINT3A"
	geomWidth(mint3a, 0.028, "MINT3A width < 28 (MINT3.1)")
	geomAdjLength(mint3a, 0.056, 0.056, 0, "MINT3A adjacent edge < 56nm (MINT3.2)")
	minmint3a = geomWidth(mint3a, 0.028, equal | output_only | opposite)
	geomLength(minmint3a, 1.800, greater, "MINT3A length with width=28nm > 1.8um (MINT3.3)")
	geomLineEnd(mint3a, 0.068, 1, 0.032, 0, "MINT3A minimum end-of-line space < 68nm (MINT3.4)")
	geomSpace(mint3a, 0.054, "MINT3A minimum space < 54nm (MINT3.5)")
	geomNotch(mint3a, 0.054, "MINT3A minimum notch < 54nm (MINT3.5)")
	geomSpace(mint3a, mint3b, 0.036, "MINT3A space to MINT3B (MINT3.6)")
	geomLineEnd(mint3a, mint3b, 0.044, 1, 0.032, 0, "MINT3A to MINT3B minimum end-of-line space < 44nm (MINT3.7)")
	geom2DSpace(mint3a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT3A Minimum spacing (MINT3.8-21)")
	geomOverlap(mint3a, mint3b, 0.040, 0, "MINT3A overlap MINT3B < 40nm (MINT3.22)")
	geomAllowedEncs(mint3a, vint2, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT3A allowed enclosure of VINT2 (MINT3.23)")
	mint3amint3b = geomAnd(mint3a, mint3b)
	geomAllowedEncs(mint3amint3b, vint2, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ], "MINT3A allowed enclosure of VINT2 (MINT3.24)")
	mint3agt60 = geomSize(mint3a, -0.060)
	widemint3 = geomSize(mint3agt60, 0.060)
	vint2inmint3 = geomAnd(vint2, widemint3)
	geomAllowedSize(vint2inmint3, [[0.028, 0.056]], "VINT2 must be rectangular if MINT3A width > 60nm (MINT3.26)")
	rectmint3a = geomGetRectangles(mint3a)
	geomArea(rectmint3a, 0.0024, 9e99, "MINT3A minimum area for rectangular shape (MINT3.27)")
	polymint3a = geomGetPolygons(mint3a)
	geomArea(polymint3a, 0.0036, 9e99, "MINT3A minimum area for non-rectangular shape (MINT3.28)")

if geomNumShapes(mint3b) > 0 :
	print "Check MINT3B"
	geomWidth(mint3b, 0.028, "MINT3B width < 28 (MINT3.1)")
	geomAdjLength(mint3b, 0.056, 0.056, 0, "MINT3B adjacent edge < 56nm (MINT3.2)")
	minmint3b = geomWidth(mint3b, 0.028, equal | output_only | opposite)
	geomLength(minmint3b, 1.800, greater, "MINT3B length with width=28nm > 1.8um (MINT3.3)")
	geomLineEnd(mint3b, 0.068, 1, 0.032, 0, "MINT3B minimum end-of-line space < 68nm (MINT3.4)")
	geomSpace(mint3b, 0.054, "MINT3B minimum space < 54nm (MINT3.5)")
	geomNotch(mint3b, 0.054, "MINT3B minimum notch < 54nm (MINT3.5)")
	geom2DSpace(mint3b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT3B Minimum spacing (MINT3.8-21)")
	geomAllowedEncs(mint3b, vint2, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT3B allowed enclosure of VINT2 (MINT3.23)")
	mint3bgt60 = geomSize(mint3b, -0.060)
	widemint3 = geomSize(mint3bgt60, 0.060)
	vint2inmint3 = geomAnd(vint2, widemint3)
	geomAllowedSize(vint2inmint3, [[0.028, 0.056]], "VINT2 must be rectangular if MINT3B width > 60nm (MINT3.26)")
	rectmint3b = geomGetRectangles(mint3b)
	geomArea(rectmint3b, 0.0024, 9e99, "MINT3B minimum area for rectangular shape (MINT3.27)")
	polymint3b = geomGetPolygons(mint3b)
	geomArea(polymint3b, 0.0036, 9e99, "MINT3B minimum area for non-rectangular shape (MINT3.28)")
	
if geomNumShapes(vint3) > 0 :
	print "Check VINT3"
	geomWidth(vint3, 0.028, "VINT3 minimum edge length 28nm (VINT3.1a)")#
	geomAllowedSize(vint3, [[0.028, 0.028],[0.028,0.056]], "VINT3 is rectangular 28x56nm (VINT3.1b)")
	geomSpace(vint3, 0.036, "VINT3 minimum space < 36nm (VINT3.2)")
	# VINT3 space for projecting length < 28nm is 50nm (VINT3.3)
	mint3mint4 = geomAnd(mint3, mint4)
	vint3mint3mint4 = geomAnd(vint3, mint3mint4)
	geomSpace(vint3, vint3mint3mint4, 0.050, vertical | project, "VINT3 space for projecting length < 28nm is 50nm (VINT3.3)")
	#
	mint3amint4a = geomAnd(mint3a, mint4a)
	mint3bmint4b = geomAnd(mint3b, mint4b)
	mint3bmint4a = geomAnd(mint3b, mint4a)
	mint3amint4b = geomAnd(mint3a, mint4b)
	#mint3mint4 = geomAnd(mint3, mint4)
	allmint3mint4 = geomOr(mint3mint4, geomOr(mint3amint4b, geomOr(mint3bmint4a, geomOr(mint3amint4a, mint3bmint4b))))
	badvint3 = geomOutside(vint3, allmint3mint4)
	saveDerived(badvint3, "VINT3 must be inside MINT3 & MINT4 (VINT3.4)")
	    
if geomNumShapes(mint4) > 0 :
	print "Check MINT4"
	geomWidth(mint4, 0.028, "MINT4 width < 28 (MINT4.1)")
	geomAdjLength(mint4, 0.056, 0.056, 0, "MINT4 adjacent edge < 56nm (MINT4.2)")
	minmint4 = geomWidth(mint4, 0.028, equal | output_only | opposite)
	geomLength(minmint4, 1.800, greater, "MINT4 length with width=28nm > 1.8um (MINT4.3)")
	geomLineEnd(mint4, 0.068, 1, 0.032, 0, "MINT4 minimum end-of-line space < 68nm (MINT4.4)")
	geomSpace(mint4, 0.054, "MINT4 minimum space < 54nm (MINT4.5)")
	geomNotch(mint4, 0.054, "MINT4 minimum notch < 54nm (MINT4.5)")
	geom2DSpace(mint4, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT4 Minimum spacing (MINT4.8-21)")
	geomAllowedEncs(mint4, vint3, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT4 allowed enclosure of VINT3 (MINT4.23)")
	mint4gt60 = geomSize(mint4, -0.060)
	widemint4 = geomSize(mint4gt60, 0.060)
	vint3inmint4 = geomAnd(vint3, widemint4)
	geomAllowedSize(vint3inmint4, [[0.028, 0.056]], "VINT3 must be rectangular if MINT4 width > 60nm (MINT4.26)")
	rectmint4 = geomGetRectangles(mint4)
	geomArea(rectmint4, 0.0024, 9e99, "MINT4 minimum area for rectangular shape (MINT4.27)")
	polymint4 = geomGetPolygons(mint4)
	geomArea(polymint4, 0.0036, 9e99, "MINT4 minimum area for non-rectangular shape (MINT4.28)")

if geomNumShapes(mint4a) > 0 :
	print "Check MINT4A"
	geomWidth(mint4a, 0.028, "MINT4A width < 28 (MINT4.1)")
	geomAdjLength(mint4a, 0.056, 0.056, 0, "MINT4A adjacent edge < 56nm (MINT4.2)")
	minmint4a = geomWidth(mint4a, 0.028, equal | output_only | opposite)
	geomLength(minmint4a, 1.800, greater, "MINT4A length with width=28nm > 1.8um (MINT4.3)")
	geomLineEnd(mint4a, 0.068, 1, 0.032, 0, "MINT4A minimum end-of-line space < 68nm (MINT4.4)")
	geomSpace(mint4a, 0.054, "MINT4A minimum space < 54nm (MINT4.5)")
	geomNotch(mint4a, 0.054, "MINT4A minimum notch < 54nm (MINT4.5)")
	geomSpace(mint4a, mint4b, 0.036, "MINT4A space to MINT4B (MINT4.6)")
	geomLineEnd(mint4a, mint4b, 0.044, 1, 0.032, 0, "MINT4A to MINT4B minimum end-of-line space < 44nm (MINT4.7)")
	geom2DSpace(mint4a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT4A Minimum spacing (MINT4.8-21)")
	geomOverlap(mint4a, mint4b, 0.040, 0, "MINT4A overlap MINT4B < 40nm (MINT4.22)")
	geomAllowedEncs(mint4a, vint3, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT4A allowed enclosure of VINT3 (MINT4.23)")
	mint4amint4b = geomAnd(mint4a, mint4b)
	geomAllowedEncs(mint4amint4b, vint3, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ], "MINT4A allowed enclosure of VINT3 (MINT4.24)")
	mint4agt60 = geomSize(mint4a, -0.060)
	widemint4 = geomSize(mint4agt60, 0.060)
	vint3inmint4 = geomAnd(vint3, widemint4)
	geomAllowedSize(vint3inmint4, [[0.028, 0.056]], "VINT3 must be rectangular if MINT4A width > 60nm (MINT4.26)")
	rectmint4a = geomGetRectangles(mint4a)
	geomArea(rectmint4a, 0.0024, 9e99, "MINT4A minimum area for rectangular shape (MINT4.27)")
	polymint4a = geomGetPolygons(mint4a)
	geomArea(polymint4a, 0.0036, 9e99, "MINT4A minimum area for non-rectangular shape (MINT4.28)")

if geomNumShapes(mint4b) > 0 :
	print "Check MINT4B"
	geomWidth(mint4b, 0.028, "MINT4B width < 28 (MINT4.1)")
	geomAdjLength(mint4b, 0.056, 0.056, 0, "MINT4B adjacent edge < 56nm (MINT4.2)")
	minmint4b = geomWidth(mint4b, 0.028, equal | output_only | opposite)
	geomLength(minmint4b, 1.800, greater, "MINT4B length with width=28nm > 1.8um (MINT4.3)")
	geomLineEnd(mint4b, 0.068, 1, 0.032, 0, "MINT4B minimum end-of-line space < 68nm (MINT4.4)")
	geomSpace(mint4b, 0.054, "MINT4B minimum space < 54nm (MINT4.5)")
	geomNotch(mint4b, 0.054, "MINT4B minimum notch < 54nm (MINT4.5)")
	geom2DSpace(mint4b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT4B Minimum spacing (MINT4.8-21)")
	geomAllowedEncs(mint4b, vint3, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT4B allowed enclosure of VINT3 (MINT4.23)")
	mint4bgt60 = geomSize(mint4b, -0.060)
	widemint4 = geomSize(mint4bgt60, 0.060)
	vint3inmint4 = geomAnd(vint3, widemint4)
	geomAllowedSize(vint3inmint4, [[0.028, 0.056]], "VINT3 must be rectangular if MINT4B width > 60nm (MINT4.26)")
	rectmint4b = geomGetRectangles(mint4b)
	geomArea(rectmint4b, 0.0024, 9e99, "MINT4B minimum area for rectangular shape (MINT4.27)")
	polymint4b = geomGetPolygons(mint4b)
	geomArea(polymint4b, 0.0036, 9e99, "MINT4B minimum area for non-rectangular shape (MINT4.28)")
	
if geomNumShapes(vint4) > 0 :
	print "Check VINT4"
	geomWidth(vint4, 0.028, "VINT4 minimum edge length 28nm (VINT4.1a)")#
	geomAllowedSize(vint4, [[0.028, 0.028],[0.028,0.056]], "VINT4 is rectangular 28x56nm (VINT4.1b)")
	geomSpace(vint4, 0.036, "VINT4 minimum space < 36nm (VINT4.2)")
	# VINT4 space for projecting length < 28nm is 50nm (VINT4.3)
	mint4mint5 = geomAnd(mint4, mint5)
	vint4mint4mint5 = geomAnd(vint4, mint4mint5)
	geomSpace(vint4, vint4mint4mint5, 0.050, vertical | project, "VINT4 space for projecting length < 28nm is 50nm (VINT4.3)")
	#
	mint4amint5a = geomAnd(mint4a, mint5a)
	mint4bmint5b = geomAnd(mint4b, mint5b)
	mint4bmint5a = geomAnd(mint4b, mint5a)
	mint4amint5b = geomAnd(mint4a, mint5b)
	#mint4mint5 = geomAnd(mint4, mint5)
	allmint4mint5 = geomOr(mint4mint5, geomOr(mint4amint5b, geomOr(mint4bmint5a, geomOr(mint4amint5a, mint4bmint5b))))
	badvint4 = geomOutside(vint4, allmint4mint5)
	saveDerived(badvint4, "VINT4 must be inside MINT4 & MINT5 (VINT4.4)")
	    
if geomNumShapes(mint5) > 0 :
	print "Check MINT5"
	geomWidth(mint5, 0.028, "MINT5 width < 28 (MINT5.1)")
	geomAdjLength(mint5, 0.056, 0.056, 0, "MINT5 adjacent edge < 56nm (MINT5.2)")
	minmint5 = geomWidth(mint5, 0.028, equal | output_only | opposite)
	geomLength(minmint5, 1.800, greater, "MINT5 length with width=28nm > 1.8um (MINT5.3)")
	geomLineEnd(mint5, 0.068, 1, 0.032, 0, "MINT5 minimum end-of-line space < 68nm (MINT5.4)")
	geomSpace(mint5, 0.054, "MINT5 minimum space < 54nm (MINT5.5)")
	geomNotch(mint5, 0.054, "MINT5 minimum notch < 54nm (MINT5.5)")
	geom2DSpace(mint5, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT5 Minimum spacing (MINT5.8-21)")
	geomAllowedEncs(mint5, vint4, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT5 allowed enclosure of VINT4 (MINT5.23)")
	mint5gt60 = geomSize(mint5, -0.060)
	widemint5 = geomSize(mint5gt60, 0.060)
	vint4inmint5 = geomAnd(vint4, widemint5)
	geomAllowedSize(vint4inmint5, [[0.028, 0.056]], "VINT4 must be rectangular if MINT5 width > 60nm (MINT5.26)")
	rectmint5 = geomGetRectangles(mint5)
	geomArea(rectmint5, 0.0024, 9e99, "MINT5 minimum area for rectangular shape (MINT5.27)")
	polymint5 = geomGetPolygons(mint5)
	geomArea(polymint5, 0.0036, 9e99, "MINT5 minimum area for non-rectangular shape (MINT5.28)")

if geomNumShapes(mint5a) > 0 :
	print "Check MINT5A"
	geomWidth(mint5a, 0.028, "MINT5A width < 28 (MINT5.1)")
	geomAdjLength(mint5a, 0.056, 0.056, 0, "MINT5A adjacent edge < 56nm (MINT5.2)")
	minmint5a = geomWidth(mint5a, 0.028, equal | output_only | opposite)
	geomLength(minmint5a, 1.800, greater, "MINT5A length with width=28nm > 1.8um (MINT5.3)")
	geomLineEnd(mint5a, 0.068, 1, 0.032, 0, "MINT5A minimum end-of-line space < 68nm (MINT5.4)")
	geomSpace(mint5a, 0.054, "MINT5A minimum space < 54nm (MINT5.5)")
	geomNotch(mint5a, 0.054, "MINT5A minimum notch < 54nm (MINT5.5)")
	geomSpace(mint5a, mint5b, 0.036, "MINT5A space to MINT5B (MINT5.6)")
	geomLineEnd(mint5a, mint5b, 0.044, 1, 0.032, 0, "MINT5A to MINT5B minimum end-of-line space < 44nm (MINT5.7)")
	geom2DSpace(mint5a, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			], 0, "MINT5A Minimum spacing (MINT5.8-21)")
	geomOverlap(mint5a, mint5b, 0.040, 0, "MINT5A overlap MINT5B < 40nm (MINT5.22)")
	geomAllowedEncs(mint5a, vint4, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT5A allowed enclosure of VINT4 (MINT5.23)")
	mint5amint5b = geomAnd(mint5a, mint5b)
	geomAllowedEncs(mint5amint5b, vint4, [ [0.014, 0.014, 4], [0.0, 0.040, 2], [0.002, 0.032, 2] ], "MINT5A allowed enclosure of VINT4 (MINT5.24)")
	mint5agt60 = geomSize(mint5a, -0.060)
	widemint5 = geomSize(mint5agt60, 0.060)
	vint4inmint5 = geomAnd(vint4, widemint5)
	geomAllowedSize(vint4inmint5, [[0.028, 0.056]], "VINT4 must be rectangular if MINT5A width > 60nm (MINT5.26)")
	rectmint5a = geomGetRectangles(mint5a)
	geomArea(rectmint5a, 0.0024, 9e99, "MINT5A minimum area for rectangular shape (MINT5.27)")
	polymint5a = geomGetPolygons(mint5a)
	geomArea(polymint5a, 0.0036, 9e99, "MINT5A minimum area for non-rectangular shape (MINT5.28)")

if geomNumShapes(mint5b) > 0 :
	print "Check MINT5B"
	geomWidth(mint5b, 0.028, "MINT5B width < 28 (MINT5.1)")
	geomAdjLength(mint5b, 0.056, 0.056, 0, "MINT5B adjacent edge < 56nm (MINT5.2)")
	minmint5b = geomWidth(mint5b, 0.028, equal | output_only | opposite)
	geomLength(minmint5b, 1.800, greater, "MINT5B length with width=28nm > 1.8um (MINT5.3)")
	geomLineEnd(mint5b, 0.068, 1, 0.032, 0, "MINT5B minimum end-of-line space < 68nm (MINT5.4)")
	geomSpace(mint5b, 0.054, "MINT5B minimum space < 54nm (MINT5.5)")
	geomNotch(mint5b, 0.054, "MINT5B minimum notch < 54nm (MINT5.5)")
	geom2DSpace(mint5b, [ [0.000, 0.028, 0.032, 0.040, 0.064, 0.120, 0.240, 0.320, 0.600],
			    [0.028, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036, 0.036],
		        [0.240, 0.036, 0.068, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076],
			    [0.480, 0.036, 0.068, 0.076, 0.092, 0.092, 0.092, 0.092, 0.092],
			    [1.200, 0.036, 0.068, 0.076, 0.092, 0.120, 0.120, 0.120, 0.120],
			    [1.800, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.240, 0.240],
			    [2.400, 0.036, 0.068, 0.076, 0.092, 0.120, 0.240, 0.320, 0.600]
			    ], 0, "MINT5B Minimum spacing (MINT5.8-21)")
	geomAllowedEncs(mint5b, vint4, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MINT5B allowed enclosure of VINT4 (MINT5.23)")
	mint5bgt60 = geomSize(mint5b, -0.060)
	widemint5 = geomSize(mint5bgt60, 0.060)
	vint4inmint5 = geomAnd(vint4, widemint5)
	geomAllowedSize(vint4inmint5, [[0.028, 0.056]], "VINT4 must be rectangular if MINT5B width > 60nm (MINT5.26)")
	rectmint5b = geomGetRectangles(mint5b)
	geomArea(rectmint5b, 0.0024, 9e99, "MINT5B minimum area for rectangular shape (MINT5.27)")
	polymint5b = geomGetPolygons(mint5b)
	geomArea(polymint5b, 0.0036, 9e99, "MINT5B minimum area for non-rectangular shape (MINT5.28)")
	
if geomNumShapes(vint5) > 0 :
	print "Check VINT5"
	geomWidth(vint5, 0.028, "VINT5 minimum edge length 28nm (VINT5.1a)")#
	geomAllowedSize(vint5, [[0.028, 0.028],[0.028,0.056]], "VINT5 is rectangular 28x56nm (VINT5.1b)")
	geomSpace(vint5, 0.036, "VINT5 minimum space < 36nm (VINT5.2)")
	# VINT5 space for projecting length < 28nm is 50nm (VINT5.3)
	mint5msmg1 = geomAnd(mint5, msmg1)
	vint5mint5msmg1 = geomAnd(vint5, mint5msmg1)
	geomSpace(vint5, vint5mint5msmg1, 0.050, vertical | project, "VINT5 space for projecting length < 28nm is 50nm (VINT5.3)")
	#
	mint5amsmg1 = geomAnd(mint5a, msmg1)
	mint5bmsmg1 = geomAnd(mint5b, msmg1)
	mint5msmg1 = geomAnd(mint5, msmg1)
	allmint5msmg1 = geomOr(mint5amsmg1, geomOr(mint5bmsmg1, mint5msmg1))
	badvint5 = geomOutside(vint5, allmint5msmg1)
	saveDerived(badvint5, "VINT5 must be inside MINT5 & MSMG1 (VINT5.4)")
	        
if geomNumShapes(msmg1) > 0 :
	print "Check MSMG1"
	geomWidth(msmg1, 0.056, "MSMG1 width < 56 (MSMG1.1)")
	geomAdjLength(msmg1, 0.112, 0.112, 0, "MSMG1 adjacent edge < 112nm (MSMG1.2)")
	minmint5 = geomWidth(msmg1, 0.056, equal | output_only | opposite)
	geomLength(minmint5, 1.920, greater, "MSMG1 length with width=56nm > 1.92um (MSMG1.3)")
	geomLineEnd(msmg1, 0.136, 1, 0.064, 0, "MSMG1 minimum end-of-line space < 136nm (MSMG1.4)")
	geomSpace(msmg1, 0.056, "MSMG1 minimum space < 56nm (MSMG1.5)")
	geomNotch(msmg1, 0.056, "MSMG1 minimum notch < 56nm (MSMG1.5)")
	geom2DSpace(msmg1, [ [0.000, 0.056, 0.064, 0.120, 0.240, 0.320, 0.600],
			     [0.056, 0.056, 0.056, 0.056, 0.056, 0.056, 0.056],
			     [0.480, 0.056, 0.092, 0.092, 0.092, 0.092, 0.092],
			     [1.200, 0.056, 0.092, 0.120, 0.120, 0.120, 0.120],
			     [1.800, 0.056, 0.092, 0.120, 0.240, 0.320, 0.320],
			     [2.400, 0.056, 0.092, 0.120, 0.240, 0.320, 0.600]
		        ], 0, "MSMG1 Minimum spacing (MSMG1.6-10)")
	geomAllowedEncs(msmg1, vint5, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MSMG1 allowed enclosure of VINT5 (MSMG1.11)")
	# MSMG1.12
	msmg1gt120 = geomSize(msmg1, -0.120)
	widemsmg1 = geomSize(msmg1gt120, 0.120)
	vint5inmsmg1 = geomAnd(vint5, widemsmg1)
	geomAllowedSize(vint5inmsmg1, [[0.056, 0.112]], "VINT5 must be rectangular if MSMG1 width > 120nm (MSMG1.13)")
	rectmsmg1 = geomGetRectangles(msmg1)
	geomArea(rectmsmg1, 0.0024, 9e99, "MSMG1 minimum area for rectangular shape (MSMG1.14)")
	polymsmg1 = geomGetPolygons(msmg1)
	geomArea(polymsmg1, 0.0036, 9e99, "MSMG1 minimum area for non-rectangular shape (MSMG1.15)")
	    
if geomNumShapes(vsmg1) > 0 :
	print "Check VSMG1"
	geomWidth(vsmg1, 0.056, "VSMG1 minimum edge length 56nm (VSMG1.1a)")#
	geomAllowedSize(vsmg1, [[0.056, 0.056],[0.056,0.112]], "VSMG1 is rectangular 56x112nm (VSMG1.1b)")
	geomSpace(vsmg1, 0.072, "VSMG1 minimum space < 72nm (VSMG1.2)")
	# VSMG1 space for projecting length < 56nm is 100nm (VSMG1.3)
	msmg1msmg2 = geomAnd(msmg1, msmg2)
	vsmg1msmg1msmg2 = geomAnd(vsmg1, msmg1msmg2)
	geomSpace(vsmg1, vsmg1msmg1msmg2, 0.100, vertical | project, "VSMG1 space for projecting length < 56nm is 100nm (VSMG1.3)")
	#
	badvsmg1 = geomOutside(vsmg1, msmg1msmg2)
	saveDerived(badvsmg1, "VSMG1 must be inside MSMG1 & MSMG2 (VSMG1.4)")

if geomNumShapes(msmg2) > 0 :
	print "Check MSMG2"
	geomWidth(msmg2, 0.056, "MSMG2 width < 56 (MSMG2.1)")
	geomAdjLength(msmg2, 0.112, 0.112, 0, "MSMG2 adjacent edge < 112nm (MSMG2.2)")
	minmint5 = geomWidth(msmg2, 0.056, equal | output_only | opposite)
	geomLength(minmint5, 1.920, greater, "MSMG2 length with width=56nm > 1.92um (MSMG2.3)")
	geomLineEnd(msmg2, 0.136, 1, 0.064, 0, "MSMG2 minimum end-of-line space < 136nm (MSMG2.4)")
	geomSpace(msmg2, 0.056, "MSMG2 minimum space < 56nm (MSMG2.5)")
	geomNotch(msmg2, 0.056, "MSMG2 minimum notch < 56nm (MSMG2.5)")
	geom2DSpace(msmg2, [ [0.000, 0.056, 0.064, 0.120, 0.240, 0.320, 0.600],
			     [0.056, 0.056, 0.056, 0.056, 0.056, 0.056, 0.056],
			     [0.480, 0.056, 0.092, 0.092, 0.092, 0.092, 0.092],
			     [1.200, 0.056, 0.092, 0.120, 0.120, 0.120, 0.120],
			     [1.800, 0.056, 0.092, 0.120, 0.240, 0.320, 0.320],
			     [2.400, 0.056, 0.092, 0.120, 0.240, 0.320, 0.600]
		        ], 0, "MSMG2 Minimum spacing (MSMG2.6-10)")
	geomAllowedEncs(msmg2, vsmg1, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MSMG2 allowed enclosure of VSMG1 (MSMG2.11)")
	# MSMG2.12
	msmg2gt120 = geomSize(msmg2, -0.120)
	widemsmg2 = geomSize(msmg2gt120, 0.120)
	vsmg1inmsmg2 = geomAnd(vsmg1, widemsmg2)
	geomAllowedSize(vsmg1inmsmg2, [[0.056, 0.112]], "VSMG1 must be rectangular if MSMG2 width > 120nm (MSMG2.13)")
	rectmsmg2 = geomGetRectangles(msmg2)
	geomArea(rectmsmg2, 0.0024, 9e99, "MSMG2 minimum area for rectangular shape (MSMG2.14)")
	polymsmg2 = geomGetPolygons(msmg2)
	geomArea(polymsmg2, 0.0036, 9e99, "MSMG2 minimum area for non-rectangular shape (MSMG2.15)")
	    
if geomNumShapes(vsmg2) > 0 :
	print "Check VSMG2"
	geomWidth(vsmg2, 0.056, "VSMG2 minimum edge length 56nm (VSMG2.1a)")#
	geomAllowedSize(vsmg2, [[0.056, 0.056],[0.056,0.112]], "VSMG2 is rectangular 56x112nm (VSMG1.1b)")
	geomSpace(vsmg2, 0.072, "VSMG2 minimum space < 72nm (VSMG1.2)")
	# VSMG2 space for projecting length < 56nm is 100nm (VSMG2.3)
	msmg2msmg3 = geomAnd(msmg2, msmg3)
	vsmg2msmg2msmg3 = geomAnd(vsmg2, msmg2msmg3)
	geomSpace(vsmg2, vsmg2msmg2msmg3, 0.100, vertical | project, "VSMG2 space for projecting length < 56nm is 100nm (VSMG2.3)")
	#
	badvsmg2 = geomOutside(vsmg2, msmg2msmg3)
	saveDerived(badvsmg2, "VSMG2 must be inside MSMG2 & MSMG3 (VSMG2.4)")
	    
if geomNumShapes(msmg3) > 0 :
	print "Check MSMG3"
	geomWidth(msmg3, 0.056, "MSMG3 width < 56 (MSMG3.1)")
	geomAdjLength(msmg3, 0.112, 0.112, 0, "MSMG3 adjacent edge < 112nm (MSMG3.2)")
	minmint5 = geomWidth(msmg3, 0.056, equal | output_only | opposite)
	geomLength(minmint5, 1.920, greater, "MSMG3 length with width=56nm > 1.92um (MSMG3.3)")
	geomLineEnd(msmg3, 0.136, 1, 0.064, 0, "MSMG3 minimum end-of-line space < 136nm (MSMG3.4)")
	geomSpace(msmg3, 0.056, "MSMG3 minimum space < 56nm (MSMG3.5)")
	geomNotch(msmg3, 0.056, "MSMG3 minimum notch < 56nm (MSMG3.5)")
	geom2DSpace(msmg3, [ [0.000, 0.056, 0.064, 0.120, 0.240, 0.320, 0.600],
			     [0.056, 0.056, 0.056, 0.056, 0.056, 0.056, 0.056],
			     [0.480, 0.056, 0.092, 0.092, 0.092, 0.092, 0.092],
			     [1.200, 0.056, 0.092, 0.120, 0.120, 0.120, 0.120],
			     [1.800, 0.056, 0.092, 0.120, 0.240, 0.320, 0.320],
			     [2.400, 0.056, 0.092, 0.120, 0.240, 0.320, 0.600]
		        ], 0, "MSMG3 Minimum spacing (MSMG3.6-10)")
	geomAllowedEncs(msmg3, vsmg2, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MSMG3 allowed enclosure of VSMG2 (MSMG3.11)")
	# MSMG3.12
	msmg3gt120 = geomSize(msmg3, -0.120)
	widemsmg3 = geomSize(msmg3gt120, 0.120)
	vsmg2inmsmg3 = geomAnd(vsmg2, widemsmg3)
	geomAllowedSize(vsmg2inmsmg3, [[0.056, 0.112]], "VSMG2 must be rectangular if MSMG3 width > 120nm (MSMG3.13)")
	rectmsmg3 = geomGetRectangles(msmg3)
	geomArea(rectmsmg3, 0.0024, 9e99, "MSMG3 minimum area for rectangular shape (MSMG3.14)")
	polymsmg3 = geomGetPolygons(msmg3)
	geomArea(polymsmg3, 0.0036, 9e99, "MSMG3 minimum area for non-rectangular shape (MSMG3.15)")
	    
if geomNumShapes(vsmg3) > 0 :
	print "Check VSMG3"
	geomWidth(vsmg3, 0.056, "VSMG3 minimum edge length 56nm (VSMG3.1a)")#
	geomAllowedSize(vsmg3, [[0.056, 0.056],[0.056,0.112]], "VSMG3 is rectangular 56x112nm (VSMG1.1b)")
	geomSpace(vsmg3, 0.072, "VSMG3 minimum space < 72nm (VSMG3.2)")
	# VSMG3 space for projecting length < 56nm is 100nm (VSMG3.3)
	msmg3msmg4 = geomAnd(msmg3, msmg4)
	vsmg3msmg3msmg4 = geomAnd(vsmg3, msmg3msmg4)
	geomSpace(vsmg3, vsmg3msmg3msmg4, 0.100, vertical | project, "VSMG3 space for projecting length < 56nm is 100nm (VSMG3.3)")
	#
	badvsmg3 = geomOutside(vsmg3, msmg3msmg4)
	saveDerived(badvsmg3, "VSMG3 must be inside MSMG3 & MSMG4 (VSMG3.4)")
	    
if geomNumShapes(msmg4) > 0 :
	print "Check MSMG4"
	geomWidth(msmg4, 0.056, "MSMG4 width < 56 (MSMG4.1)")
	geomAdjLength(msmg4, 0.112, 0.112, 0, "MSMG4 adjacent edge < 112nm (MSMG4.2)")
	minmint5 = geomWidth(msmg4, 0.056, equal | output_only | opposite)
	geomLength(minmint5, 1.920, greater, "MSMG4 length with width=56nm > 1.92um (MSMG4.3)")
	geomLineEnd(msmg4, 0.136, 1, 0.064, 0, "MSMG4 minimum end-of-line space < 136nm (MSMG4.4)")
	geomSpace(msmg4, 0.056, "MSMG4 minimum space < 56nm (MSMG4.5)")
	geomNotch(msmg4, 0.056, "MSMG4 minimum notch < 56nm (MSMG4.5)")
	geom2DSpace(msmg4, [ [0.000, 0.056, 0.064, 0.120, 0.240, 0.320, 0.600],
			     [0.056, 0.056, 0.056, 0.056, 0.056, 0.056, 0.056],
			     [0.480, 0.056, 0.092, 0.092, 0.092, 0.092, 0.092],
			     [1.200, 0.056, 0.092, 0.120, 0.120, 0.120, 0.120],
			     [1.800, 0.056, 0.092, 0.120, 0.240, 0.320, 0.320],
			     [2.400, 0.056, 0.092, 0.120, 0.240, 0.320, 0.600]
		        ], 0, "MSMG4 Minimum spacing (MSMG4.6-10)")
	geomAllowedEncs(msmg4, vsmg3, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MSMG4 allowed enclosure of VSMG3 (MSMG4.11)")
	# MSMG4.12
	msmg4gt120 = geomSize(msmg4, -0.120)
	widemsmg4 = geomSize(msmg4gt120, 0.120)
	vsmg3inmsmg4 = geomAnd(vsmg3, widemsmg4)
	geomAllowedSize(vsmg3inmsmg4, [[0.056, 0.112]], "VSMG3 must be rectangular if MSMG4 width > 120nm (MSMG4.13)")
	rectmsmg4 = geomGetRectangles(msmg4)
	geomArea(rectmsmg4, 0.0024, 9e99, "MSMG4 minimum area for rectangular shape (MSMG4.14)")
	polymsmg4 = geomGetPolygons(msmg4)
	geomArea(polymsmg4, 0.0036, 9e99, "MSMG4 minimum area for non-rectangular shape (MSMG4.15)")
	    
if geomNumShapes(vsmg4) > 0 :
	print "Check VSMG4"
	geomWidth(vsmg4, 0.056, "VSMG4 minimum edge length 56nm (VSMG4.1a)")#
	geomAllowedSize(vsmg4, [[0.056, 0.056],[0.056,0.112]], "VSMG4 is rectangular 56x112nm (VSMG4.1b)")
	geomSpace(vsmg4, 0.072, "VSMG4 minimum space < 72nm (VSMG4.2)")
	# VSMG3 space for projecting length < 56nm is 100nm (VSMG3.3)
	msmg4msmg5 = geomAnd(msmg4, msmg5)
	vsmg4msmg4msmg5 = geomAnd(vsmg4, msmg4msmg5)
	geomSpace(vsmg4, vsmg4msmg4msmg5, 0.100, vertical | project, "VSMG4 space for projecting length < 56nm is 100nm (VSMG4.3)")
	#
	badvsmg4 = geomOutside(vsmg4, msmg4msmg5)
	saveDerived(badvsmg4, "VSMG4 must be inside MSMG4 & MSMG5 (VSMG4.4)")
	    
if geomNumShapes(msmg5) > 0 :
	print "Check MSMG5"
	geomWidth(msmg5, 0.056, "MSMG5 width < 56nm (MSMG5.1)")
	geomAdjLength(msmg5, 0.112, 0.112, 0, "MSMG5 adjacent edge < 112nm (MSMG5.2)")
	minmint5 = geomWidth(msmg5, 0.056, equal | output_only | opposite)
	geomLength(minmint5, 1.920, greater, "MSMG5 length with width=56nm > 1.92um (MSMG5.3)")
	geomLineEnd(msmg5, 0.136, 1, 0.064, 0, "MSMG5 minimum end-of-line space < 136nm (MSMG5.4)")
	geomSpace(msmg5, 0.056, "MSMG5 minimum space < 56nm (MSMG5.5)")
	geomNotch(msmg5, 0.056, "MSMG5 minimum notch < 56nm (MSMG5.5)")
	geom2DSpace(msmg5, [ [0.000, 0.056, 0.064, 0.120, 0.240, 0.320, 0.600],
			     [0.056, 0.056, 0.056, 0.056, 0.056, 0.056, 0.056],
			     [0.480, 0.056, 0.092, 0.092, 0.092, 0.092, 0.092],
			     [1.200, 0.056, 0.092, 0.120, 0.120, 0.120, 0.120],
			     [1.800, 0.056, 0.092, 0.120, 0.240, 0.320, 0.320],
			     [2.400, 0.056, 0.092, 0.120, 0.240, 0.320, 0.600]
		        ], 0, "MSMG5 Minimum spacing (MSMG5.6-10)")
	geomAllowedEncs(msmg5, vsmg4, [ [0.010, 0.010, 4], [0.0, 0.032, 2], [0.002, 0.028, 2] ], "MSMG5 allowed enclosure of VSMG4 (MSMG5.11)")
	# MSMG5.12
	msmg5gt120 = geomSize(msmg5, -0.120)
	widemsmg5 = geomSize(msmg5gt120, 0.120)
	vsmg4inmsmg5 = geomAnd(vsmg4, widemsmg5)
	geomAllowedSize(vsmg4inmsmg5, [[0.056, 0.112]], "VSMG4 must be rectangular if MSMG5 width > 120nm (MSMG5.13)")
	rectmsmg5 = geomGetRectangles(msmg5)
	geomArea(rectmsmg4, 0.0024, 9e99, "MSMG5 minimum area for rectangular shape (MSMG5.14)")
	polymsmg5 = geomGetPolygons(msmg5)
	geomArea(polymsmg5, 0.0036, 9e99, "MSMG5 minimum area for non-rectangular shape (MSMG5.15)")
	    
if geomNumShapes(vsmg5) > 0 :
	print "Check VSMG5"
	geomWidth(vsmg5, 0.056, "VSMG5 minimum edge length 56nm (VSMG5.1a)")#
	geomAllowedSize(vsmg5, [[0.056, 0.056],[0.056,0.112]], "VSMG5 is rectangular 56x112nm (VSMG5.1b)")
	geomSpace(vsmg5, 0.072, "VSMG5 minimum space < 72nm (VSMG5.2)")
	# VSMG5 space for projecting length < 56nm is 100nm (VSMG5.3)
	msmg5mg1 = geomAnd(msmg5, mg1)
	vsmg5msmg5mg1 = geomAnd(vsmg5, msmg5mg1)
	geomSpace(vsmg5, vsmg5msmg5mg1, 0.100, vertical | project, "VSMG5 space for projecting length < 56nm is 100nm (VSMG5.3)")
	#
	badvsmg5 = geomOutside(vsmg5, msmg5mg1)
	saveDerived(badvsmg5, "VSMG5 must be inside MSMG4 & MG1 (VSMG5.4)")

if geomNumShapes(mg1) > 0 :
	print "Check MG1"
	geomWidth(mg1, 0.112, "MG1 width < 112nm (MG1.1)")
	geomAdjLength(mg1, 0.224, 0.224, 0, "MG1 adjacent edge < 224nm (MG1.2)")
	minmint5 = geomWidth(mg1, 0.112, equal | output_only | opposite)
	geomLength(minmint5, 3.840, greater, "MG1 length with width=112nm > 3.84um (MG1.3)")
	geomLineEnd(mg1, 0.272, 1, 0.128, 0, "MG1 minimum end-of-line space < 272nm (MG1.4)")
	geomSpace(mg1, 0.112, "MG1 minimum space < 112nm (MG1.5)")
	geomNotch(mg1, 0.112, "MG1 minimum notch < 112nm (MG1.5)")
	geom2DSpace(mg1, [ [0.000, 0.112, 0.120, 0.240, 0.320, 0.600],
		           [0.112, 0.112, 0.112, 0.112, 0.112, 0.112],
		           [1.200, 0.112, 0.120, 0.120, 0.120, 0.120],
		           [1.800, 0.112, 0.120, 0.240, 0.320, 0.320],
		           [2.400, 0.112, 0.120, 0.240, 0.320, 0.600]
	            ], 0, "MG1 Minimum spacing (MG1.6-9)")
	geomAllowedEncs(mg1, vsmg4, [ [0.000, 0.000, 4] ], "MG1 allowed enclosure of VSMG5 (MG1.10)")
	# MG1.11
	mg1gt160 = geomSize(mg1, -0.160)
	widemg1 = geomSize(mg1gt160, 0.160)
	vsmg5inmg1 = geomAnd(vsmg5, widemg1)
	geomAllowedSize(vsmg5inmg1, [[0.112, 0.224]], "VSMG4 must be rectangular if MG1 width > 160nm (MG1.12)")
	rectmg1 = geomGetRectangles(mg1)
	geomArea(rectmg1, 0.0024, 9e99, "MG1 minimum area for rectangular shape (MG1.13)")
	polymg1 = geomGetPolygons(mg1)
	geomArea(polymg1, 0.0036, 9e99, "MG1 minimum area for non-rectangular shape (MG1.14)")
	    
if geomNumShapes(vg1) > 0 :
	print "Check VG1"
	geomWidth(vg1, 0.112, "VG1 minimum edge length 56nm (VG1.1a)")#
	geomAllowedSize(vg1, [[0.112, 0.112],[0.112,0.224]], "VG1 is rectangular 56x112nm (VG1.1b)")
	geomSpace(vg1, 0.144, "VG1 minimum space < 144nm (VG1.2)")
	# VSMG5 space for projecting length < 56nm is 100nm (VSMG5.3)
	mg1mg2 = geomAnd(mg1, mg2)
	vg1mg1mg2 = geomAnd(vg1, mg1mg2)
	geomSpace(vg1, vg1mg1mg2, 0.200, vertical | project, "VG1 space for projecting length < 112nm is 200nm (VG1.3)")
	#
	badvg1 = geomOutside(vg1, mg1mg2)
	saveDerived(badvg1, "VG1 must be inside MG1 & MG2 (VG1.4)")

if geomNumShapes(mg2) > 0 :
	print "Check MG2"
	geomWidth(mg2, 0.112, "MG2 width < 112nm (MG2.1)")
	geomAdjLength(mg2, 0.224, 0.224, 0, "MG2 adjacent edge < 224nm (MG2.2)")
	minmint5 = geomWidth(mg2, 0.112, equal | output_only | opposite)
	geomLength(minmint5, 3.840, greater, "MG2 length with width=112nm > 3.84um (MG2.3)")
	geomLineEnd(mg2, 0.272, 1, 0.128, 0, "MG2 minimum end-of-line space < 272nm (MG2.4)")
	geomSpace(mg2, 0.112, "MG2 minimum space < 112nm (MG2.5)")
	geomNotch(mg2, 0.112, "MG2 minimum notch < 112nm (MG2.5)")
	geom2DSpace(mg2, [ [0.000, 0.112, 0.120, 0.240, 0.320, 0.600],
		           [0.112, 0.112, 0.112, 0.112, 0.112, 0.112],
		           [1.200, 0.112, 0.120, 0.120, 0.120, 0.120],
		           [1.800, 0.112, 0.120, 0.240, 0.320, 0.320],
		           [2.400, 0.112, 0.120, 0.240, 0.320, 0.600]
	            ], 0, "MG2 Minimum spacing (MG2.6-9)")
	geomAllowedEncs(mg2, vsmg4, [ [0.000, 0.000, 4] ], "MG2 allowed enclosure of VG1 (MG2.10)")
	# MG2.11
	mg2gt160 = geomSize(mg2, -0.160)
	widemg2 = geomSize(mg2gt160, 0.160)
	vg1inmg2 = geomAnd(vg1, widemg2)
	geomAllowedSize(vg1inmg2, [[0.112, 0.224]], "VG1 must be rectangular if MG2 width > 160nm (MG2.12)") 
	rectmg2 = geomGetRectangles(mg2)
	geomArea(rectmg2, 0.0024, 9e99, "MG2 minimum area for rectangular shape (MG2.13)")
	polymg2 = geomGetPolygons(mg2)
	geomArea(polymg2, 0.0036, 9e99, "MG2 minimum area for non-rectangular shape (MG2.14)")

# Exit DRC package, freeing memory
geomEnd()
ui().winFit()
