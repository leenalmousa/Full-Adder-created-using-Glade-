################################################################################
# FreePDK15 Extraction deck.
# Peardrop Design Systems Ltd 2017
################################################################################
# Initialise DRC package. 
from ui import *
cv = ui().getEditCellView()
geomBegin(cv)

print "# Getting raw layers"
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

print "# Generating derived layers"
psub      = geomNot(nwell)
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

# Derived layers for devices
ngthinox  = geomAndNot(ngate, thkox)
ngate1    = geomAndNot(ngthinox, vtl)
ngate2    = geomAndNot(ngthinox, vth)
ngate3    = geomAnd(ngate, thkox)
pgate3    = geomAnd(pgate, thkox)
ngate4    = geomAndNot(ngate3, vtl)
pgate4    = geomAndNot(ngate3, vtl)

pgthinox  = geomAndNot(pgate, thkox)
pgate1    = geomAndNot(pgthinox, vtl)
pgate2    = geomAndNot(pgthinox, vth)

# Normal VT devices
ngnorm    = geomAndNot(ngate1, vth)
pgnorm    = geomAndNot(pgate1, vth)

# High VT devices
ngvth     = geomAnd(ngate1, vth)
pgvth     = geomAnd(pgate1, vth)

# Low VT devices
ngvtl     = geomAnd(ngate2, vtl)
pgvtl     = geomAnd(pgate2, vtl)

# thick ox devices
ngthkox   = geomAndNot(ngate4, vth)
pgthkox   = geomAndNot(pgate4, vth)

print "# Label nodes"
#geomLabel(m1, "M1", "drawing")
#geomLabel(mint1, "MINT1", "drawing")
# etc


print "Extracting connectivity"
geomConnect( [
              	[ntap, ndiff, nwell],
				[gil, allgate],
				[ail2, ail1, gil],
				[ail1, ndiff, pdiff],
              	[v0, ail2, gil, m1, m1a, m1b],
              	[v1, m1, m1a, m1b, mint1, mint1a, mint1b],
              	[vint1, mint1, mint1a, mint1b, mint2, mint2a, mint2b],
              	[vint2, mint2, mint2a, mint2b, mint3, mint3a, mint3b],
              	[vint3, mint3, mint3a, mint3b, mint4, mint4a, mint4b],
              	[vint4, mint4, mint4a, mint4b, mint5, mint5a, mint5b],
              	[vint5, mint5, mint5a, mint5b, msmg1],
              	[vsmg1, msmg1, msmg2],
              	[vsmg2, msmg2, msmg3],
              	[vsmg3, msmg3, msmg4],
              	[vsmg4, msmg4, msmg5],
              	[vsmg5, msmg5, mg1],
              	[vg1, mg1, mg2]
	     ] )

print "# Save interconnect"
saveInterconnect([
                 [psub, "PSUB"],
				 nwell,
				 [ntap, "ACT"],
				 [ptap, "ACT"],
				 [ndiff, "ACT"],
				 [pdiff, "ACT"],
				 [allgate, "GATEAB"],
				 v0,
				 ail1,
				 ail2,
				 gil,
				 m1,
				 [m1a, "M1"],
				 [m1b, "M1"],
				 mint1,
				 [mint1a, "MINT1"],
				 [mint1b, "MINT1"],
				 vint1,
				 mint2,
				 [mint2a, "MINT2"],
				 [mint2b, "MINT2"],
				 vint2,
				 mint3,
				 [mint3a, "MINT3"],
				 [mint3b, "MINT3"],
				 vint3,
				 mint4,
				 [mint4a, "MINT4"],
				 [mint4b, "MINT4"],
				 vint4,
				 mint5,
				 [mint5a, "MINT5"],
				 [mint5b, "MINT5"],
				 vint5,
				 msmg1,
				 vsmg1,
				 msmg2,
				 vsmg2,
				 msmg3,
				 vsmg3,
				 msmg4,
				 vsmg4,
				 msmg5,
				 vsmg5,
				 mg1,
				 vg1,
				 mg2
				 ])


print "# MOS device extraction"
extractMOS("nmos_ex", ngnorm, gate, ndiff, psub) 
extractMOS("pmos_ex", pgnorm, gate, pdiff, nwell) 

extractMOS("nmos_vtl_ex", ngvtl, gate, ndiff, psub) 
extractMOS("pmos_vtl_ex", ngvtl, gate, pdiff, nwell) 

extractMOS("nmos_vth_ex", ngvth, gate, ndiff, psub) 
extractMOS("pmos_vth_ex", ngvth, gate, pdiff, nwell) 

extractMOS("nmos_thk_ex", ngthkox, gate, ndiff, psub) 
extractMOS("pmos_thk_ex", pgthkox, gate, pdiff, nwell) 

# Exit DRC package, freeing memory
geomEnd()
ui().winFit()
