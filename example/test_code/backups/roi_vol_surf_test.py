# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from pyfat.algorithm.roi_vol_surf import roi_vol2surf, label2surf_roi
from pyfat.viz.surfaceview import surface_streamlines_map, surface_roi_contour
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_selection import select_by_surf_rois
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


lh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.L.white.native.surf.gii'
rh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.R.white.native.surf.gii'
# roi_vol_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                'response_dhollander/100408/Structure/MNI152_cytoMPM_thr25_2mm.nii.gz'
roi_vol_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/100408/Structure/Wangliang_Atlas/native_mpm_lrh_thr10.nii.gz'

tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_lr1.5_new_SD_Stream_hierarchical_single_cc_splenium.tck'

data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)

fasciculus = Fasciculus(tck_path)
streamlines = fasciculus.get_data()

subject_id = "100408"
subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408"
hemi = 'both'
surf = 'inflated'
alpha = 1
geo_path = [lh_white, rh_white]

# lr_labels = roi_vol2surf(roi_vol_path, geo_path)
# lr_labels[0][lr_labels[0] != 6] = 0
# # lr_labels[0][lr_labels[0] > 93] = 0
# # lr_labels[1][lr_labels[1] < 84] = 0
# lr_labels[1][lr_labels[1] != 6] = 0

# lr_labels[0][lr_labels[0] > 0] = 1
# lr_labels[1][lr_labels[1] > 0] = 1
# surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, lr_labels)
# hemi = 'rh'
surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, lr_labels)

#
l_labels = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/my_labels/native/native_lh_VMV3.label'
r_labels = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/my_labels/native/native_rh_VMV3.label'

lr_labels_vir_name = 'native_lrh_VMV3'
lr_labels_path = [l_labels, r_labels]
labels_values = label2surf_roi(lr_labels_path, geo_path)

# surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, labels_values)


#
# surface_roi_contour(subjects_dir, subject_id, hemi, surf, alpha, lr_label, lr_label)
streams = select_by_surf_rois(streamlines, labels_values, geo_path)
suffix = []
for i in range(len(lr_labels_path)):
    suffix.append(os.path.split(lr_labels_path[i])[1].split('.')[-2])
if len(streams) == 3:
    suffix.append(lr_labels_vir_name)
#
# print suffix
#
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/ROIs_fibs/hcp_VanEssen_Atlas/VMV3/%s_fib_SD_stream.tck'
for j in range(len(streams)):
    fasciculus.set_data(streams[j])
    fasciculus.save2tck(out_path % suffix[j])

# for i in range(len(streams)):
#     fiber_simple_3d_show_advanced(img, streams[i], 1)

