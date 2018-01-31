# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_clustering import FibClustering
from pyfat.viz.colormap import create_random_colormap
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital8_lr5.tck'
roi_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/lab_map/native1.25_wang_maxprob_vol_lh_mask_vis.nii.gz'
img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

img = nib.load(img_path)
fa = Fasciculus(fib)
streamlines = fa.get_data()
fibcluster = FibClustering(fa)

# 1
label_endpoints = fibcluster.endpoints_seg(temp_clusters=5000, mode='lh', thre=1)
# labels_rois = fibcluster.cluster_by_vol_rois(roi_path)
print set(label_endpoints)

colormap = create_random_colormap(len(set(label_endpoints)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(label_endpoints), colormap):
    colormap_full[label_endpoints == label] = color

hemi_fib = fibcluster.hemisphere_cc(hemi='lh')

fiber_simple_3d_show_advanced(img, hemi_fib, colormap_full)

# 2
labels_rois = fibcluster.cluster_endpoints_by_vol_rois(roi_path, mode='lh')
print set(labels_rois)

colormap = create_random_colormap(len(set(labels_rois)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(labels_rois), colormap):
    colormap_full[labels_rois == label] = color

hemi_fib = fibcluster.hemisphere_cc(hemi='lh')

fiber_simple_3d_show_advanced(img, hemi_fib, colormap_full)

# 3
for i in set(label_endpoints):
    cluster_value = len(set(labels_rois)) * [None]
    endpoints_flag = label_endpoints == i
    for j in range(len(set(labels_rois))):
        if np.array(list(set(labels_rois)))[j] is not None:
            rois_flag = labels_rois == np.array(list(set(labels_rois)))[j]
            flag = endpoints_flag * rois_flag
            cluster_value[j] = flag.sum(axis=0)
    index = np.array(cluster_value).argmax()
    label_endpoints[endpoints_flag] = np.array(list(set(labels_rois)))[index]

colormap = create_random_colormap(len(set(label_endpoints)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(label_endpoints), colormap):
    colormap_full[label_endpoints == label] = color

hemi_fib = fibcluster.hemisphere_cc(hemi='lh')

fiber_simple_3d_show_advanced(img, hemi_fib, colormap_full)

print len(set(label_endpoints))
print len(set(labels_rois))
