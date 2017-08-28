#!/usr/bin/python3
# ==============================================================
# demo for parsing
# ==============================================================
import google_parse


fileID = 'NovelView_small'
"""
# 2. parse raw depth
"""
sv3DRegion = google_parse.StreetView3DRegion(fileID)
sv3DRegion.init_region(anchor=None)
sv3DRegion.create_topology()
sv3DRegion.create_region()

"""
" 3. openGl visual
"""
import numpy as np
import glumpy_setting
import base_process
import scipy.misc

needMatchInfo3d = True
needVisual = True
addPlane = False
needGround = True
needPerspective = False
randomDeg = 0

pano_length = len(sv3DRegion.sv3D_Dict)
anchor_inv = np.linalg.inv(sv3DRegion.anchorMatrix)
zero_vec, pano_ori_set, dis_len_set = [0, 0, 0, 1], np.zeros((pano_length, 3)), np.zeros(pano_length)
# Initialize the pano according to location(lat, lon)
for i, sv3D_key in enumerate(sv3DRegion.sv3D_Dict):
    sv3D = sv3DRegion.sv3D_Dict[sv3D_key]
    sv3D.apply_global_adjustment()  # Absolute position on earth (lat, lon, yaw)
    sv3D.apply_local_adjustment()  # Relative position according to anchor (anchor's lat,lon)
    if needMatchInfo3d:
        # This rotate the SV3D for matching x-y plane
        # Actually we build the point cloud on x-y plane
        # So we just multiply the inverse matrix of anchor
        sv3D.apply_anchor_adjustment(anchor_matrix=sv3DRegion.anchorMatrix)
    # Record all pano location(relative)
    # And find the nearest panorama
isFirst = True
for key in sv3DRegion.sv3D_Dict:
    sv3D = sv3DRegion.sv3D_Dict[key]
    if addPlane:
        sv3D.auto_plane()
    if isFirst:
        data = sv3D.ptCLoudData[np.nonzero(sv3D.non_con)]
        dataGnd = sv3D.ptCLoudData[np.nonzero(sv3D.gnd_con)]
        isFirst = False
    else:
        data = np.concatenate((data, sv3D.ptCLoudData[np.nonzero(sv3D.non_con)]), axis=0)
        dataGnd = np.concatenate((dataGnd, sv3D.ptCLoudData[np.nonzero(sv3D.gnd_con)]), axis=0)

    if needPerspective:
        ori_pano = sv3D.panorama / 255.0
        pano_height, pano_width = ori_pano.shape[0], ori_pano.shape[1]  # Actually, this must be 1:2
        perspective_height, perspective_width = int(pano_height / 2), int(pano_width / 2)
        perspective_90_set = []
        # randomDeg = - sv3D.yaw
        for degree in range(0, 360, 90):
            perspective_90 = np.zeros((perspective_height, perspective_width, 3))
            for p_y in range(0, perspective_height):
                for p_x in range(0, perspective_width):
                    x = p_x - perspective_width / 2
                    z = -p_y + perspective_height / 2
                    y = perspective_height
                    lng, lat = base_process.pos_2_deg(x, y, z)

                    lng = (lng + degree + randomDeg) % 360
                    img_x = lng / 360.0 * pano_width
                    img_y = -(lat - 90) / 180.0 * pano_height

                    img_pos0_x = np.floor(img_x)
                    img_pos0_y = np.floor(img_y)

                    img_pos_diff_x = img_x - img_pos0_x
                    img_pos_diff_y = img_y - img_pos0_y

                    img_pos1_x = img_pos0_x + 1
                    img_pos1_y = img_pos0_y

                    img_pos2_x = img_pos0_x
                    img_pos2_y = img_pos0_y + 1

                    img_pos3_x = img_pos0_x + 1
                    img_pos3_y = img_pos0_y + 1

                    if img_pos1_x == pano_width:
                        img_pos1_x = pano_width - 1
                    if img_pos3_x == pano_width:
                        img_pos3_x = pano_width - 1
                    if img_pos2_y == pano_height:
                        img_pos2_y = pano_height - 1
                    if img_pos3_y == pano_height:
                        img_pos3_y = pano_height - 1

                    img_ratio0 = (1 - img_pos_diff_x) * (1 - img_pos_diff_y)
                    img_ratio1 = img_pos_diff_x * (1 - img_pos_diff_y)
                    img_ratio2 = (1 - img_pos_diff_x) * img_pos_diff_y
                    img_ratio3 = img_pos_diff_x * img_pos_diff_y

                    img_color0 = ori_pano[img_pos0_y, img_pos0_x, :]
                    img_color1 = ori_pano[img_pos1_y, img_pos1_x, :]
                    img_color2 = ori_pano[img_pos2_y, img_pos2_x, :]
                    img_color3 = ori_pano[img_pos3_y, img_pos3_x, :]

                    img_color = img_ratio0 * img_color0 + img_ratio1 * img_color1 + \
                                img_ratio2 * img_color2 + img_ratio3 * img_color3

                    perspective_90[p_y, p_x, :] = img_color

            scipy.misc.imsave(str(degree) + '.png', perspective_90)
            scipy.misc.imshow(perspective_90)
            perspective_90_set.append(perspective_90)

if needVisual:
    programSV3DRegion = glumpy_setting.ProgramSV3DRegion(
        data=data, name='ProgramSV3DRegion', point_size=1,
        anchor_matrix=sv3DRegion.anchorMatrix, anchor_yaw=sv3DRegion.anchorYaw, is_inverse=needMatchInfo3d)
    programSV3DRegionGnd = glumpy_setting.ProgramSV3DRegion(
        data=dataGnd, name='ProgramSV3DRegionGnd', point_size=1,
        anchor_matrix=sv3DRegion.anchorMatrix, anchor_yaw=sv3DRegion.anchorYaw, is_inverse=needMatchInfo3d)
    programSV3DTopology = glumpy_setting.ProgramSV3DTopology(
        data=sv3DRegion.topologyData, name='programSV3DTopology',
        anchor_matrix=sv3DRegion.anchorMatrix, anchor_yaw=sv3DRegion.anchorYaw, is_inverse=needMatchInfo3d)

"""
For Visualize
"""
if needVisual:
    gpyWindow = glumpy_setting.GpyWindow()
    if addPlane:
        for j in range(0, pano_length):
            sv3D = sv3DRegion.sv3D_Time[j]
            for i in range(0, len(sv3D.all_plane)):
                programGround = glumpy_setting.ProgramPlane(data=sv3D.all_plane[i]['data'], name='test',
                                                            face=sv3D.all_plane[i]['tri'])
                gpyWindow.add_program(programGround)
    else:
        gpyWindow.add_program(programSV3DRegion)
        gpyWindow.add_program(programSV3DTopology)
        if needGround:
            gpyWindow.add_program(programSV3DRegionGnd)

    programAxis = glumpy_setting.ProgramAxis(line_length=5)
    gpyWindow.add_program(programAxis)

    gpyWindow.run()