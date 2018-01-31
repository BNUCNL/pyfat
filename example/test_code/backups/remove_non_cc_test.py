# !/usr/bin/python
# -*- coding: utf-8 -*-


from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.algorithm.remove_non_cc import extract_up_z

data_path = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/100206/result/CC_fib.tck'
# load tck data
img_cc = load_tck(data_path)
L_temp = extract_up_z(img_cc)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100206/result/CC_fib_remove_non_cc_z-10_x-min.tck'
save_tck(L_temp, img_cc.header, img_cc.tractogram.data_per_streamline, img_cc.tractogram.data_per_point,
         img_cc.tractogram.affine_to_rasmm, out_path)
