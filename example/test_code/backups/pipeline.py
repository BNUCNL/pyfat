# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from dipy.segment.quickbundles import QuickBundles
from pyfat.core.dataobject import Fasciculus
from dipy.tracking.utils import length
from pyfat.algorithm.fiber_clustering import FibClustering
from pyfat.viz.colormap import create_random_colormap
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
      'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'
# fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital8_lr5.tck'
img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

img = nib.load(img_path)
fa = Fasciculus(fib)
streamlines = fa.get_data()
length_t = fa.get_lengths()
ind = length_t > 10
streamlines = streamlines[ind]
fa.set_data(streamlines)
fibcluster = FibClustering(fa)
print len(streamlines)

# 1
qb = QuickBundles(streamlines, 2)
clusters = qb.clusters()
print qb.clusters_sizes()
indexs = []
for i in range(len(clusters)):
    if clusters[i]['N'] >= 400:
        indexs += clusters[i]['indices']

# 2
streamlines = streamlines[indexs]
qb = QuickBundles(streamlines, 2)
clusters = qb.clusters()

centroids = qb.centroids
centroids_lengths = np.array(list(length(centroids)))
print centroids_lengths

indexs_c = []
for j in range(len(centroids)):
    if centroids_lengths[j] >= 50.:
        indexs_c += clusters[j]['indices']

streamlines = streamlines[indexs_c]
qb = QuickBundles(streamlines, 2)
clusters = qb.clusters()
print len(streamlines)
print qb.clusters_sizes()

# Color each streamline according to the cluster they belong to.
colormap = create_random_colormap(len(set(clusters)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for cluster, color in zip(clusters, colormap):
    colormap_full[clusters[cluster]['indices']] = color
# print colormap_full
fiber_simple_3d_show_advanced(img, streamlines, colormap_full)

# 3
fa.set_data(streamlines)
label_endpoints = fibcluster.endpoints_seg(mode='rh', thre=2)
print set(label_endpoints)

colormap = create_random_colormap(len(set(label_endpoints)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(label_endpoints), colormap):
    colormap_full[label_endpoints == label] = color
fiber_simple_3d_show_advanced(img, streamlines, colormap_full)

#
# for lab in set(label_endpoints):
#     index = label_endpoints == lab
#     fiber_simple_3d_show_advanced(img, streamlines[index], colormap_full[index])
