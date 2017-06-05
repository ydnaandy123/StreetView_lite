#!/usr/bin/python3
# ==============================================================
# demo for render new view
# ==============================================================
import google_parse
import glumpy_setting
import base_process

fileID = 'viewDEMO'
"""
# 3. parse raw depth
"""
if True:
    anchor = '5PhE8uGmkxJD2GhtcJaGQg'
    sv3DRegion = google_parse.StreetView3DRegion(fileID)
    sv3DRegion.init_region(anchor=None, only3=True)
    sv3DRegion.create_region()

    a, b = None, None
    # Visual
    for pano_idx, key in enumerate(sv3DRegion.sv3D_Dict):
        sv = sv3DRegion.sv3D_Dict[key]
        if pano_idx == 0:
            a = sv
        elif pano_idx == 1:
            b = sv
        else:
            break

    # DEMO b to a
    a.show_pano()
    b.show_pano()
    b2a = None
