# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from dipy.viz import fvtk
from dipy.segment.clustering import QuickBundles
from dipy.io.pickles import save_pickle
import nibabel.streamlines.tck as nibtck

# load fiber data
imgtck = nibtck.TckFile.load('/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                             'response_dhollander/100206/result/CC_fib_remove_non_cc_z-10_x-min.tck')
streams = imgtck.streamlines
# print len(streams)
streamlines = [s for s in streams]

print len(streamlines)

world_coords = True
if not world_coords:
    from dipy.tracking.streamline import transform_streamlines
    streamlines = transform_streamlines(streamlines, np.linalg.inv(imgtck.affine))

# clustering
qb = QuickBundles(threshold=20.)  # maybe 10.
clusters = qb.cluster(streamlines)

# extract > 100
print len(clusters) # 294
for c in clusters:
    if len(c) < 100:
        clusters.remove_cluster(c)
print len(clusters)  # 161
# print clusters
# print "Nb. clusters:", len(clusters)
# print "Cluster size:", map(len, clusters)
# print "Small clusters:", clusters < 10
# print "Streamlines indices of the first cluster:\n", clusters[0].indices
# print "Centroid of the last cluster:\n", clusters[-1].centroid

# show rhe initial dataset
ren = fvtk.ren()
ren.SetBackground(1, 1, 1)
fvtk.add(ren, fvtk.streamtube(streamlines, fvtk.colors.white))
fvtk.record(ren, n_frames=1, out_path='/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                                      'response_dhollander/100206/result/CC_fib_remove_non_cc_z-10_x-min_10_jet.png', size=(600, 600))
# fvtk.show(ren)

# show the centroids of the CC
colormap = fvtk.create_colormap(np.arange(len(clusters)), name='jet')
fvtk.clear(ren)
ren.SetBackground(1, 1, 1)
fvtk.add(ren, fvtk.streamtube(streamlines, fvtk.colors.white, opacity=0.05))
fvtk.add(ren, fvtk.streamtube(clusters.centroids, colormap, linewidth=0.4))
fvtk.record(ren, n_frames=1, out_path='/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                                      'response_dhollander/100206/result/CC_fib1_remove_non_cc_z-10_x-min_10_jet.png', size=(600, 600))
# fvtk.show(ren)

# show the label CC (colors form centroids)
colormap_full = np.ones((len(streamlines)), np.float64(3))
for clusters, color in zip(clusters, colormap):
    colormap_full[clusters.indices] = color
fvtk.clear(ren)
ren.SetBackground(1, 1, 1)
fvtk.add(ren, fvtk.streamtube(streamlines, colormap_full))
fvtk.record(ren, n_frames=1, out_path='/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                                      'response_dhollander/100206/result/CC_fib2_remove_non_cc_z-10_x-min_10_jet.png', size=(600, 600))
# fvtk.show(ren)

# save the complete ClusterMap object with picking
save_pickle('/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
            '100206/result/CC_fib_remove_non_cc_z-10_x-min_10_jet.pk2', clusters)
