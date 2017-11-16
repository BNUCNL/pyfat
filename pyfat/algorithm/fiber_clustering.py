# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

import numpy as np
from math import sqrt, pow
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas

from pyfat.core.dataobject import Fasciculus
from pyfat.viz.visualization import show


class FibClustering(object):
    """Fiber clustering"""
    def __init__(self, fasciculus):
        """
        Fiber clustering

        Parameters
        ----------
        fasciculus : whole fasciculus
        An object of class Fasciculus

        Return
        ------
        FibClustering

        """
        if isinstance(fasciculus, Fasciculus):
            self._fasciculus = fasciculus
        else:
            raise ValueError("The fasciculus must be an object of class Fasciculus.")

    def _length_seg(self, min_length, max_length):
        """A segmentation of length-based segmentation"""
        fasciculus_data = self._fasciculus.get_data()
        lengths = self._fasciculus.get_lengths()
        index0 = lengths >= min_length
        index1 = lengths <= max_length
        index_term = np.vstack((np.array([index0]), np.array([index1]))).sum(axis=0)
        index = index_term > 1
        length_seg_data = fasciculus_data[index]

        return index, length_seg_data

    def length_seg(self):
        """Length-based segmentation"""
        length_clusters = nibas.ArraySequence()
        labels = np.array(len(self._fasciculus.get_data()) * [None])
        length_seg_temp = self._length_seg(20, 50)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 1

        length_seg_temp = self._length_seg(50, 65)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 2

        length_seg_temp = self._length_seg(65, 80)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 3

        length_seg_temp = self._length_seg(80, 95)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 4

        length_seg_temp = self._length_seg(95, 110)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 5

        length_seg_temp = self._length_seg(110, 130)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 6

        length_seg_temp = self._length_seg(130, 150)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 7

        length_seg_temp = self._length_seg(150, 175)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 8

        length_seg_temp = self._length_seg(175, 200)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 9

        length_seg_temp = self._length_seg(200, 250)
        length_clusters.append(length_seg_temp[1])
        labels[length_seg_temp[0]] = 10

        return labels, length_clusters

    def bundle_seg(self, streamlines, dist_thre=10.0, pts=12):
        """QuickBundles-based segmentation"""
        bundles = QuickBundles(streamlines, dist_thre, pts)
        clusters = bundles.clusters()
        labels = np.array(len(streamlines) * [None])
        N_list = []
        for i in range(len(clusters)):
            N_list.append(clusters[i]['N'])
        # show(N_list, title='N histogram', xlabel='N')
        data_clusters = []
        for i in range(len(clusters)):
            labels[clusters[i]['indices']] = i + 1
            data_clusters.append(streamlines[clusters[i]['indices']])

        return labels, data_clusters, N_list

    def bundle_thre_seg(self, streamlines, cluster_thre=10, dist_thre=10.0, pts=12):
        """QuickBundles-based segmentation"""
        bundles = QuickBundles(streamlines, dist_thre, pts)
        bundles.remove_small_clusters(cluster_thre)
        clusters = bundles.clusters()
        data_clusters = []
        for key in clusters.keys():
            data_clusters.append(streamlines[clusters[key]['indices']])
        centroids = bundles.centroids
        clusters_y_mean = [clu[:, 1].mean() for clu in centroids]
        sort_index = np.argsort(clusters_y_mean)

        return sort_index, data_clusters

    def bundle_centroids(self, streamlines, cluster_thre=10, dist_thre=10.0, pts=12):
        """QuickBundles-based segmentation"""
        bundles = QuickBundles(streamlines, dist_thre, pts)
        bundles.remove_small_clusters(cluster_thre)
        centroids = bundles.centroids

        return nibas.ArraySequence(centroids)

    def terminus_symmetry(self, streamlines, dist_thre=5.0):
        dist = np.array([sqrt(pow(abs(s[0][0])-abs(s[-1][0]), 2) +
                              pow(s[0][1]-s[-1][1], 2) + pow(s[0][2]-s[-1][2], 2))
                         for s in streamlines])
        index = dist < dist_thre
        term_sym_streamlines = streamlines[index]

        return term_sym_streamlines



    def voxel_seg(self):
        """Voxel-based clustering"""
        pass
