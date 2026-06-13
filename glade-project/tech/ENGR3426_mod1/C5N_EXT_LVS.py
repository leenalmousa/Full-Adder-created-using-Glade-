#------------------------------------------------------------------------------
#
# C5N extraction script
#
#------------------------------------------------------------------------------

from ui import *
ui = cvar.uiptr
cv = ui.getEditCellView()
geomBegin(cv)
lib = cv.lib()

print 'Loading pcells for extraction...'
ui.loadPCell(lib.libName(), 'C5NNMOS')
ui.loadPCell(lib.libName(), 'C5NPMOS')
#ui.loadPCell(lib.libName(), 'C5NP1RES')
#ui.loadPCell(lib.libName(), 'C5NP2RES')
#ui.loadPCell(lib.libName(), 'C5NHIRES')
#ui.loadPCell(lib.libName(), 'C5NP1P2CAP')
#ui.loadPCell(lib.libName(), 'C5NPADCAP')

print 'Getting raw layers...'
nwell = geomGetShapes('NWELL', 'drawing')
active = geomGetShapes('DIFF', 'drawing')
poly = geomGetShapes('POLY', 'drawing')
nplus = geomGetShapes('NPLUS', 'drawing')
pplus = geomGetShapes('PPLUS', 'drawing')
hires = geomGetShapes('hires', 'drawing')
contact = geomGetShapes('CONT', 'drawing')
metal1 = geomGetShapes('M1', 'drawing')
via = geomGetShapes('VIA12', 'drawing')
metal2 = geomGetShapes('M2', 'drawing')
via2 = geomGetShapes('VIA23', 'drawing')
metal3 = geomGetShapes('M3', 'drawing')
glass = geomGetShapes('glass', 'drawing')
pads = geomGetShapes('pads', 'drawing')
cap_id = geomGetShapes('cap_id', 'drawing')
res_id = geomGetShapes('res_id', 'drawing')
diode_id = geomGetShapes('diode_id', 'drawing')

print 'Forming derived layers...'
bkgnd = geomBkgnd()
psub = geomAndNot(bkgnd, nwell)
gate = geomAnd(poly, active)
ngate = geomAnd(gate, nplus)
pgate = geomAnd(gate, pplus)
diff = geomAndNot(active, gate)
ndiff = geomAnd(diff, nplus)
pdiff = geomAnd(diff, pplus)
nplug = geomAnd(ndiff, nwell)
pplug = geomAndNot(pdiff, nwell)
activecon = geomAnd(contact, active)
polycon = geomAnd(contact, poly)
poly_wire = geomAndNot(poly, res_id)
poly_res = geomAnd(poly, res_id)
pad_cap = geomAnd(metal1, pads)

print 'Labeling nodes...'
#geomLabel(poly_wire, 'POLY', 'pin', True)
geomLabel(metal1, 'M1', 'pin', True)
geomLabel(metal2, 'M2', 'pin', True)
geomLabel(metal3, 'M3', 'pin', True)
#geomLabel(poly_wire, 'POLY', 'lbl', False)
geomLabel(metal1, 'M1', 'lbl', False)
geomLabel(metal2, 'M2', 'lbl', False)
geomLabel(metal3, 'M3', 'lbl', False)

print 'Forming connectivity...'
geomConnect([[pplug, psub, pdiff], 
             [nplug, nwell, ndiff], 
             [activecon, ndiff, pdiff, metal1], 
             [polycon, poly_wire, metal1], 
             [via, metal1, metal2], 
             [via2, metal2, metal3]])

# Save connectivity to extracted view. Saved layers must be
# ones previously connected by geomConnect. Any derived
# layers must be saved to a named layer (e.g. psub below)
print 'Saving interconnect...'
saveInterconnect([[psub, 'psub'],
                  nwell,
                  [ndiff, 'DIFF'],
                  [pdiff, 'DIFF'],
                  [nplug, 'DIFF'],
                  [pplug, 'DIFF'],
                  [poly_wire, 'POLY'],
                  [activecon, 'CONT'],
                  [polycon, 'CONT'],
                  nplus,
                  pplus,
                  metal1,
                  via,
                  metal2,
                  via2,
                  metal3])

# Extract MOS devices. Device terminal layers *must* exist in
# the extracted view as a result of saveInterconnect.
# In this case we are using pcell devices which will be
# created according to the recognition region polygon.
print 'Extracting MOS devices...'
extractMOS('C5NNMOS', ngate, poly, active, psub)
extractMOS('C5NPMOS', pgate, poly, active, nwell)

# Extract resistors. Device terminal layers must exist in
# extracted view as a result of saveInterconnect.
#if geomNumShapes(poly_res)>0:
#    print 'Extracting poly resistors...'
#    extractRes('C5NP1RES', poly_res, poly_wire)

# Extract pad capacitors. Device terminal layers must exist in 
# extracted view as a result of saveInterconnect.
#if geomNumShapes(pad_cap)>0:
#    print 'Extracting pad capacitors...'
#    extractMosCap('C5NPADCAP', pad_cap, metal1, psub)

# Exit geometry package, freeing memory.
print 'Extraction completed.'
geomEnd()

# Open the extracted view.
ui.openCellView(lib.libName(), cv.cellName(), 'extracted')
