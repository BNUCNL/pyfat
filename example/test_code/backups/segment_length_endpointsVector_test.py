# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from pyfat.io.load import load_tck
from dipy.io.pickles import save_pickle
from dipy.segment.clustering import QuickBundles
from dipy.segment.metric import SumPointwiseEuclideanMetric
from pyfat.algorithm.segment_length_endpointsVector import ArcLengthFeature, show, CosineMetric


# load fiber data
data_path = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/101006/result/CC_fib.tck'
imgtck = load_tck(data_path)

world_coords = True
if not world_coords:
    from dipy.tracking.streamline import transform_streamlines
    streamlines = transform_streamlines(imgtck.streamlines, np.linalg.inv(imgtck.affine))

metric = SumPointwiseEuclideanMetric(feature=ArcLengthFeature())
qb = QuickBundles(threshold=2., metric=metric)
clusters = qb.cluster(streamlines)

# extract > 100
# print len(clusters) # 89
for c in clusters:
    if len(c) < 100:
        clusters.remove_cluster(c)

out_path = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/101006/result/CC_fib_length1_2.png'
show(imgtck, clusters, out_path)

metric = CosineMetric()
qb = QuickBundles(threshold=0.1, metric=metric)
clusters = qb.cluster(streamlines)

# extract > 100
# print len(clusters)  # 41
for c in clusters:
    if len(c) < 100:
        clusters.remove_cluster(c)

out_path = '/home/brain/workingdir/data/dwi/hcp/' \
            'preprocessed/response_dhollander/101006/result/CC_fib_length2_2.png'
show(imgtck, clusters, out_path)

# save the complete ClusterMap object with picking
save_pickle('/home/brain/workingdir/data/dwi/hcp/preprocessed/'
            'response_dhollander/101006/result/CC_fib_length_2.pk2', clusters)
