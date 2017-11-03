# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, fcluster


def hiera_clust(Ls_temp, n_clusters=2, affinity='euclidean', memory=None,
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

def hiera_single_clust(Ls_temp, temp_clusters=5000, t=2):
    Ls_temp_labels, Ls_temp_centers = k_means(Ls_temp, n_clusters=temp_clusters)
    sdist = pdist(Ls_temp_centers)
    knn_graph = linkage(sdist, method='single', metric='euclidean')
    label_img = fcluster(knn_graph, t=t, criterion='distance')

    labels = np.array(len(Ls_temp)*[None])
    for i in set(label_img):
        l = np.argwhere(label_img == i)
        stream = Ls_temp_labels == l
        stream_sum = stream.sum(axis=0)
        stream_temp = stream_sum > 0
        labels[stream_temp] = i
    return labels