# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from surfer import Brain
from mayavi import mlab
from line_profiler import LineProfiler
from memory_profiler import memory_usage

from dipy.segment.quickbundles import QuickBundles
from pyfat.core.dataobject import Fasciculus
from dipy.tracking.utils import length
from pyfat.algorithm.fiber_clustering import FibClustering
from pyfat.algorithm.fasc_mapping import terminus2surface_map
from pyfat.viz.surfaceview import surface_streamlines_map
from pyfat.viz.colormap import create_random_colormap
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
      'response_dhollander/subjects_all/Diffusion/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_all_subjects.tck'
img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100610/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

# load volume data to show fib
img = nib.load(img_path)

# load fib
fa = Fasciculus(fib)
streamlines = fa.get_data()

# remove unmeaning fib
length_t = fa.get_lengths()
ind = length_t > 10
streamlines = streamlines[ind]
fa.set_data(streamlines)
print len(streamlines)

# step1 the first Quickbundle clustering
# remove strange fib: number of the cluster < thre
qb = QuickBundles(streamlines, 2)
clusters = qb.clusters()
print qb.clusters_sizes()
indexs = []
for i in range(len(clusters)):
    if clusters[i]['N'] >= 400:
        indexs += clusters[i]['indices']

streamlines = streamlines[indexs]

# step2 the second Quickbundle clustering
# remove short fib: length of the cluster < thre
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

########
# lp = LineProfiler()
# lp_wrapper = lp(create_random_colormap)
# lp_wrapper(len(set(clusters)))
# lp.print_stats()
# print "----------------------"
# print memory_usage((create_random_colormap, (len(set(clusters)),)))


colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for cluster, color in zip(clusters, colormap):
    colormap_full[clusters[cluster]['indices']] = color
# print colormap_full
# fiber_simple_3d_show_advanced(img, streamlines, colormap_full)

# step3 endpoints clustering
fa.set_data(streamlines)
fibcluster = FibClustering(fa)
label_endpoints = fibcluster.endpoints_seg(temp_clusters=10000, mode='lh', thre=5)

#################
# lp = LineProfiler()
# lp_wrapper = lp(fibcluster.endpoints_seg)
# lp_wrapper(mode='lh', thre=1.6)
# lp.print_stats()

print set(label_endpoints)

colormap = create_random_colormap(len(set(label_endpoints)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(label_endpoints), colormap):
    colormap_full[label_endpoints == label] = color
fiber_simple_3d_show_advanced(img, streamlines, colormap_full)


# # terminus2surface_map
# # load left and right hemisphere geometry data
# geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/100206/Native/100206.L.white.native.surf.gii'
# geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/100206/Native/100206.R.white.native.surf.gii'
# geo_path = [geo_path_l, geo_path_r]
# inde = label_endpoints == 1
# lh_map, rh_map = terminus2surface_map(streamlines[inde], geo_path)
# for lab in set(label_endpoints):
#     if lab == 1:
#         continue
#     index = label_endpoints == lab
#     lh_map_t, rh_map_t = terminus2surface_map(streamlines[index], geo_path)
#     lh_map = np.vstack((lh_map, lh_map_t))
#     rh_map = np.vstack((rh_map, rh_map_t))
#
# lh_value = lh_map.argmax(axis=0)
# rh_value = rh_map.argmax(axis=0)
# print set(lh_value), set(rh_value)
# coords = [lh_value, rh_value]
# subject_id = "100206"
# subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206"
# hemi = 'lh'
# surf = 'inflated'
# alpha = 1
# # brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)
# # brain.add_data(coords[0], thresh=0, vertices=coords[0], colormap='rocket', alpha=0.8)
# # mlab.show()
# surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, coords)



