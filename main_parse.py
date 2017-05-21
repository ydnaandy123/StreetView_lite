#!/usr/bin/python3
# ==============================================================
# demo for parsing
# ==============================================================
import google_parse


fileID = 'NTHUDEMO'
"""
# 2. parse raw depth
"""
if True:
    sv3DRegion = google_parse.StreetView3DRegion(fileID)
    sv3DRegion.init_region(anchor=None)
    sv3DRegion.create_topoloy()
    sv3DRegion.create_region()
    for key in sv3DRegion.sv3D_Dict:
        sv = sv3DRegion.sv3D_Dict[key]
        sv.show_pano()
        #sv.visualize()
        break
