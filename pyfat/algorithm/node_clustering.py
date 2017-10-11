# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans

def hierarchical_clust(Ls_temp, n_clusters=2, affinity='euclidean', memory=None,
                       connectivity=None, compute_full_tree='auto', linkage='ward', pooling_func=np.mean):
    clusters = AgglomerativeClustering(n_clusters, affinity, memory,
                                       connectivity, compute_full_tree, linkage, pooling_func)
    labels = clusters.fit_predict(Ls_temp)
    return labels

def k_means(Ls_temp, n_clusters=5000, init='k-means++', n_init=10, max_iter=300, tol=0.0001,
            precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1, algorithm='auto'):
    clusters = KMeans(n_clusters, init, n_init, max_iter, tol, precompute_distances,
                      verbose, random_state, copy_x, n_jobs, algorithm)
    means = clusters.fit(Ls_temp)
    clusters_labels = means.labels_
    clusters_centers = means.cluster_centers_
    return clusters_labels, clusters_centers