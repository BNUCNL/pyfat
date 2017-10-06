# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.cluster import AgglomerativeClustering

def hierarchical_clust(Ls_temp, n_clusters=2, affinity='euclidean', memory=None,
                       connectivity=None, compute_full_tree='auto', linkage='ward', pooling_func=np.mean):
    clusters = AgglomerativeClustering(n_clusters, affinity, memory,
                                       connectivity, compute_full_tree, linkage, pooling_func)
    labels = clusters.fit_predict(Ls_temp)
    return labels
