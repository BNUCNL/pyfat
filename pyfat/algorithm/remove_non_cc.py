# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel.streamlines.array_sequence as nibas


def extract_up_z(img_cc, z_value=-10):
    """
    extract z > z_value fiber
    :param img_cc: input fiber
    :param z_value: z thresh
    :return: z > z_value fiber
    """
    L_temp = nibas.ArraySequence()
    for i in range(len(img_cc.streamlines)):
        l_x = []
        for j in range(len(img_cc.streamlines[i])):
            l_x.append(np.abs(img_cc.streamlines[i][j][0]))
        x_min_index = np.argmin(l_x)
        if img_cc.streamlines[i][x_min_index][2] > z_value:  # -2<x<2 & z>-10
            L_temp.append(img_cc.streamlines[i])
    return L_temp
