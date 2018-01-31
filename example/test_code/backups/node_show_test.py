# !/usr/bin/python
# -*- coding: utf-8 -*-


import nibabel as nib
from pyfat.io.load import load_tck
from pyfat.algorithm.CC_extract_tck import extract_cc, extract_multi_node, extract_cc_step
from pyfat.algorithm.node_extract import xmin_extract
from pyfat.algorithm.node_show import show_slice_density

# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100206/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)
img_data = img.get_data()
# print img.shape
# print img_data
tck_path = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/100206/result/CC_fib_new.tck'

imgtck = load_tck(tck_path)
streamstck = imgtck.streamlines
# print len(streamstck)

# extract cc fib
imgtck_fib = extract_cc(imgtck)
# remove multi-node fib
imgtck_fib = extract_multi_node(imgtck_fib)[0]
# step > 20
imgtck_fib = extract_cc_step(imgtck_fib)[0]

# extract node according to x-value
Ls_temp = xmin_extract(imgtck_fib)
# print len(Ls_temp)
# show node density
show_slice_density(img, Ls_temp)
