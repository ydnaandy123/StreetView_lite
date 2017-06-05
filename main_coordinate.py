#!/usr/bin/python3
# ==============================================================
# demo for chane coordinate(lat, lon, h) <--> (x, y, z)
# ==============================================================
import google_parse
import base_process

fileID = 'viewDEMO'
"""
# 2. parse raw depth
"""
if True:
    sv3DRegion = google_parse.StreetView3DRegion(fileID)
    sv3DRegion.init_region(anchor=None)
    sv3DRegion.create_topoloy()
    # All single location
    topology_data = sv3DRegion.topologyData
    sv3DRegion.create_region()
    # Visual24.796195, 120.99238
    for key in sv3DRegion.sv3D_Dict:
        sv = sv3DRegion.sv3D_Dict[key]
        lat, lon = sv.lat, sv.lon
        lat, lon, h = base_process.ecef_2_geo(sv.ecef[0], sv.ecef[1], sv.ecef[2])
        x, y, z = base_process.geo_2_ecef(lat, lon, h)
        #sv.show_pano()
        #sv.visualize()
        break
