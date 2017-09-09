# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel.streamlines.array_sequence as nibAS


def extract_up_z(img_cc):
    L_temp = nibAS.ArraySequence()
    for i in range(len(img_cc.streamlines)):
        l_x = []
        for j in range(len(img_cc.streamlines[i])):
            l_x.append(np.abs(img_cc.streamlines[i][j][0]))
        x_min_index = np.argmin(l_x)
        if img_cc.streamlines[i][x_min_index][2] > -10:  # -2<x<2 & z>-10
            L_temp.append(img_cc.streamlines[i])
    return L_temp

if __name__ == '__main__':
    from pyfat.io.load import load_tck
    from pyfat.io.save import save_tck
    data_path = '/home/brain/workingdir/data/dwi/hcp/' \
                'preprocessed/response_dhollander/100206/result/CC_fib.tck'
    # load tck data
    img_cc = load_tck(data_path)
    L_temp = extract_up_z(img_cc)
    out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/100206/result/CC_fib_remove_non_cc_z-10_x-min.tck'
    save_tck(L_temp, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
             img_cc.tractogram.affine_to_rasmm, out_path)
