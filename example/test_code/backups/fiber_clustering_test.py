# !/usr/bin/python
# -*- coding: utf-8 -*-

from dipy.segment.quickbundles import QuickBundles
import nibabel as nib
from mayavi import mlab
import numpy as np
from surfer import Brain
from mayavi import mlab
from pyfat.algorithm.fiber_maths import clusters_terminus2surface_pm, clusters_terminus2surface_mpm
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fasc_mapping import terminus2surface_nearest_pts, terminus2volume_nearest_vox, terminus2volume_density_map
from pyfat.algorithm.fasc_mapping import terminus2surface_map, terminus2surface_density_map
from pyfat.algorithm.fiber_clustering import FibClustering
from pyfat.algorithm.fiber_extract import FibSelection
# from pyfat.io.load import load_tck
from pyfat.io.save import save_nifti
from pyfat.viz.fiber_simple_viz import fiber_simple_3d_show
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced
from pyfat.viz.surfaceview import surface_streamlines_roi, surface_streamlines_map

# lh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/100408/surf/lh.white'
# rh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/100408/surf/rh.white'
#
lh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.L.white.native.surf.gii'
rh_white = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Native/100408.R.white.native.surf.gii'

geo_path = [lh_white, rh_white]

tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/cc_20fib_1.5lr_new_hierarchical_single_cc_splenium.tck'
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/result/result20vs45/cc_20fib_only_node.tck'
# tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_sample5000.tck'
# load data
data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100408/Structure/T1w_acpc_dc_restore_brain.nii.gz'
img = nib.load(data_path)

fasciculus = Fasciculus(tck_path)
fibcluster = FibClustering(fasciculus)
# length_clusters = fibcluster.length_seg()
# streamlines = fasciculus.sort_streamlines()
# fasciculus.set_data(streamlines)
streamlines = fasciculus.get_data()
print len(streamlines)

# d = fibcluster.bundle_seg(streamlines, dist_thre=15)
# print len(d[1])
index_streams = fibcluster.bundle_thre_seg(streamlines)
print len(index_streams[1])
centroids = fibcluster.bundle_centroids(streamlines, cluster_thre=10, dist_thre=10)
subject_id = "100408"
subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408"
hemi = 'both'
surf = 'inflated'
alpha = 1
# vertex = clusters_terminus2surface_mpm(index_streams[1], geo_path)
# vertex = terminus2surface_map(index_streams[1], geo_path)
# vertex = clusters_terminus2surface_pm(index_streams[1], geo_path)
# vertex = terminus2surface_density_map(index_streams[1][0], geo_path)
# surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, vertex)
# data_out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/100408/Structure/terminus2surface_density_map.nii.gz'
# count = terminus2volume_density_map(streamlines, data_path)
# save_nifti(count, img.affine, data_out_path)

# vertex = terminus2surface_nearest_pts(index_streams[1][0], geo_path)
# surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, vertex)

# print len(centroids)
#
# fibselection = FibSelection(fasciculus)
# ce_sy = fibcluster.terminus_symmetry(centroids, dist_thre=5.0)
# print len(ce_sy)
#
# centroids = fasciculus.sort_streamlines(centroids)
# stream_out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/result/463_clusters/clusters_%s.tck'
# for s in index_streams[0]:
#     fasciculus.set_data(index_streams[1][s])
#     fasciculus.save2tck(stream_out_path % s)

#     nt = terminus2surface_map(index_streams[1][s], geo_path)
#     print nt[0][nt[0] > 0].max()
#     subject_id = "100408"
#     subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408"
#     hemi = 'both'
#     surf = 'white'
#     alpha = 1
#     surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, nt)


fiber_simple_3d_show_advanced(img, centroids, 1)
# bundle = fibcluster.bundle_thre_seg(streamlines)
# # fasciculus.set_labels(bundle[0])
# # print len(set(bundle[0]))
# fib = FibSelection(fasciculus)
# # fiber = fib.labels2fasc(0)
# for i in range(len(bundle)):
#     # fiber_simple_3d_show(img, bundle[1][i])
#     fiber_simple_3d_show_advanced(img, bundle[i], i)


