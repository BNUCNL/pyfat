# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
==========================================================
Enhancing QuickBundles with different metrics and features
==========================================================
"""

import numpy as np
from dipy.segment.clustering import QuickBundles

from dipy.segment.metric import IdentityFeature
from dipy.segment.metric import ResampleFeature
from dipy.segment.metric import AveragePointwiseEuclideanMetric

from dipy.segment.metric import CenterOfMassFeature
from dipy.segment.metric import MidpointFeature
from dipy.segment.metric import ArcLengthFeature
from dipy.segment.metric import EuclideanMetric

from dipy.segment.metric import VectorOfEndpointsFeature
from dipy.segment.metric import CosineMetric


def qb_metrics_features(streamlines, threshold=10.0,
                        metric=None, max_nb_clusters=np.iinfo('i4').max):
    """
    Enhancing QuickBundles with different metrics and features
    metric: 'IF', 'RF', 'CoMF', 'MF', 'AF', 'VBEF', None
    """
    if metric == 'IF':
        feature = IdentityFeature()
        metric = AveragePointwiseEuclideanMetric(feature=feature)
    elif metric == 'RF':
        feature = ResampleFeature(nb_point=24)
        metric = AveragePointwiseEuclideanMetric(feature=feature)
    elif metric == 'CoMF':
        feature = CenterOfMassFeature()
        metric = EuclideanMetric(feature)
    elif metric == 'MF':
        feature = MidpointFeature()
        metric = EuclideanMetric(feature)
    elif metric == 'AF':
        feature = ArcLengthFeature()
        metric = EuclideanMetric(feature)
    elif metric == 'VBEF':
        feature = VectorOfEndpointsFeature()
        metric = CosineMetric(feature)
    else:
        metric = "MDF_12points"

    qb = QuickBundles(threshold=threshold, metric=metric, max_nb_clusters=max_nb_clusters)
    clusters = qb.cluster(streamlines)

    labels = np.array(len(streamlines) * [None])
    N_list = []
    for i in range(len(clusters)):
        N_list.append(clusters[i]['N'])
    data_clusters = []
    for i in range(len(clusters)):
        labels[clusters[i]['indices']] = i + 1
        data_clusters.append(streamlines[clusters[i]['indices']])

    return labels, data_clusters, N_list
