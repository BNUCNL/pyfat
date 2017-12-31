# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine
from math import sqrt, pow
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas

from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.node_clustering import NodeClustering
from pyfat.viz.visualization import show


class FibClustering(object):
    """Fiber clustering"""
    def __init__(self, fasciculus):
        """
        Fiber clustering

        Parameters
        ----------
        fasciculus :
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
        """
        Length-based segmentation

        Return
        ------
        labels: label of each streamline
        length_clusters: cluster data
        """
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

    def bundle_seg(self, streamlines=None, dist_thre=10.0, pts=12):
        """
        QuickBundles-based segmentation
        Parameters
        ----------
        streamlines: streamline data
        dist_thre: clustering threshold (distance mm)
        pts: each streamlines are divided into sections

        Return
        ------
        labels: label of each streamline
        data_cluster: cluster data
        N_list: size of each cluster
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines
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

    def bundle_thre_seg(self, streamlines=None, cluster_thre=10, dist_thre=10.0, pts=12):
        """
        QuickBundles-based segmentation
        Parameters
        ----------
        streamlines: streamline data
        cluster_thre: remove small cluster
        dist_thre: clustering threshold (distance mm)
        pts: each streamlines are divided into sections

        Return
        ------
        sort_index: sort of clusters according to y mean of cluster's centroids
        data_cluster: cluster data corresponding to sort_index
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines
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

    def bundle_centroids(self, streamlines=None, cluster_thre=10, dist_thre=10.0, pts=12):
        """
        QuickBundles-based segmentation
        Parameters
        ----------
        streamlines: streamline data
        cluster_thre: remove small cluster
        dist_thre: clustering threshold (distance mm)
        pts: each streamlines are divided into sections

        Return
        ------
        centroids: cluster's centroids
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines
        bundles = QuickBundles(streamlines, dist_thre, pts)
        bundles.remove_small_clusters(cluster_thre)
        centroids = bundles.centroids

        return nibas.ArraySequence(centroids)

    def terminus_symmetry(self, streamlines=None, dist_thre=5.0):
        """
        Extract streamlines that have symmetrical terminus/endpoints
        Parameters
        ----------
        streamlines: streamline data
        dist_thre: symmetry distance threshold

        Return
        ------
        term_sym_streamlines: endpoints meet the symmetry of the streamlines
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines
        dist = np.array([sqrt(pow(abs(s[0][0])-abs(s[-1][0]), 2) +
                              pow(s[0][1]-s[-1][1], 2) + pow(s[0][2]-s[-1][2], 2))
                         for s in streamlines])
        index = dist < dist_thre
        term_sym_streamlines = streamlines[index]

        return term_sym_streamlines

    def endpoints_seg(self, streamlines=None, temp_clusters=None, thre=2.0, mode='lh'):
        """
        Endpoints-based clustering fibers
        Parameters
        ----------
        streamlines: streamline data
        temp_clusters: the number of k-means iterations (the first step to use k-means when data set is too big)
        thre: hierarchical/agglomerative clustering threshold (distance mm)
        mode:'lh','rh','lh-rh'(left endpoints, right endpoints or left right endpoints)

        Return
        ------
        labels: label of each streamline
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines

        if temp_clusters is None:
            temp_clusters = len(streamlines)

        streamlines = self._fasciculus.sort_streamlines(streamlines)
        endpoints_l = nibas.ArraySequence([fib[0] for fib in streamlines])
        endpoints_r = nibas.ArraySequence([fib[-1] for fib in streamlines])

        if mode == 'lh':
            nc = NodeClustering(endpoints_l)
            labels = nc.hiera_single_clust(temp_clusters=temp_clusters, t=thre)
        elif mode == 'rh':
            nc = NodeClustering(endpoints_r)
            labels = nc.hiera_single_clust(temp_clusters=temp_clusters, t=thre)
        elif mode == 'lh-rh':
            endpoints_l_r = nibas.ArraySequence(np.hstack((endpoints_l, endpoints_r)))
            nc = NodeClustering(endpoints_l_r)
            labels = nc.hiera_single_clust(temp_clusters=temp_clusters, t=thre)
        else:
            raise ValueError("Without this mode!")

        return labels

    def hemisphere_cc(self, streamlines=None, hemi='lh'):
        """
        Select a particular hemisphere streamlines to display
        Parameters
        ----------
        streamlines: streamline data
        hemi:'lh','rh','both'

        Return
        ------
        hemi_fib: particular hemisphere streamlines
        """
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines

        streamlines = self._fasciculus.sort_streamlines(streamlines)
        hemi_fib = nibas.ArraySequence()
        for i in range(len(streamlines)):
            l = streamlines[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            index0 = np.argwhere(x_stemp_index <= 0)
            index_term = np.argmin((abs(streamlines[i][index0[0][0]][0]),
                                    abs(streamlines[i][index0[0][0] + 1][0])))
            index = index0[0][0] + index_term
            if hemi == 'lh':
                hemi_fib.append(streamlines[i][:index + 1])
            elif hemi == 'rh':
                hemi_fib.append(streamlines[i][index:])
            elif hemi == 'both':
                hemi_fib.append(streamlines[i])
            else:
                raise ValueError("Without this mode!")

        return hemi_fib

    def cluster_by_vol_rois(self, rois_path, streamlines=None):
        """
        Clustering fibers by vol_rois, according to the number of streamline through rois
        Parameters
        ----------
        rois_path: volume rois path
        streamlines: streamline data

        Return
        ------
        labels: label each streamline
        """
        img = nib.load(rois_path)
        rois = img.get_data()
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines

        streamlines = self._fasciculus.sort_streamlines(streamlines)

        labels = np.array(len(streamlines) * [None])

        for i in range(len(streamlines)):
            coords = apply_affine(npl.inv(img.affine), streamlines[i]).astype(int)
            count = np.array(int(rois.max()) * [0])
            for j in range(len(coords)):
                if rois[coords[j][0], coords[j][1], coords[j][2]] != 0:
                    count[int(rois[coords[j][0], coords[j][1], coords[j][2]]) - 1] += 1

            labels[i] = count.argmax() + 1

        return labels

    def cluster_endpoints_by_vol_rois(self, rois_path, streamlines=None, mode='lh'):
        """
        Clustering fiber endpoints by vol_rois, according to the endpoints of streamline through rois
        Parameters
        ----------
        rois_path: volume rois path
        streamlines: streamline data
        mode: 'lh', 'rh'

        Return
        ------
        labels: label each streamline
        """
        img = nib.load(rois_path)
        rois = img.get_data()
        if streamlines is None:
            streamlines = self._fasciculus.get_data()
        else:
            streamlines = streamlines

        streamlines = self._fasciculus.sort_streamlines(streamlines)

        labels = np.array(len(streamlines) * [None])

        if mode == 'lh':
            endpoints = [apply_affine(npl.inv(img.affine), fib[0]).astype(int) for fib in streamlines]
        elif mode == 'rh':
            endpoints = [apply_affine(npl.inv(img.affine), fib[-1]).astype(int) for fib in streamlines]

        for i in range(len(endpoints)):
            if rois[endpoints[i][0], endpoints[i][1], endpoints[i][2]] != 0:
                labels[i] = int(rois[endpoints[i][0], endpoints[i][1], endpoints[i][2]])

        return labels
