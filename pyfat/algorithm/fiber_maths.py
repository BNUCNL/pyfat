# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

from __future__ import division
import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
import nibabel.streamlines.array_sequence as nibas
from scipy.spatial.distance import pdist, squareform
from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import StreamlineLinearRegistration


def coordinate_dist(coordinate, metric='euclidean'):
    """
    coordinate distance
    :param coordinate: ndarray
        An m by n array of m original observations in an
        n-dimensional space.
    :param metric: string or function
        The distance metric to use. The distance function can
        be 'braycurtis', 'canberra', 'chebyshev', 'cityblock',
        'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
        'jaccard', 'kulsinski', 'mahalanobis', 'matching',
        'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
        'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
    :return: matrix of distance
    """
    dist_temp = pdist(coordinate, metric)
    sdist = squareform(dist_temp)
    return sdist


def bundle_registration(cb_subj1, cb_subj2, pts=12):
    """
    Register two bundle from two subjects
    directly in the space of streamlines
    """
    cb_subj1 = set_number_of_points(cb_subj1, pts)
    cb_subj2 = set_number_of_points(cb_subj2, pts)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    cb_subj2_aligned = srm.transform(cb_subj2)

    return cb_subj2_aligned


def _sort_streamlines(fasciculus_data):
    fasciculus_data_sort = nibas.ArraySequence()
    for i in range(len(fasciculus_data)):
        if fasciculus_data[i][0][0] < 0:
            fasciculus_data_sort.append(fasciculus_data[i])
        else:
            fasciculus_data_sort.append(fasciculus_data[i][::-1])
    return fasciculus_data_sort


def clusters_terminus2surface_pm(cluters, geo_path):
    """
    Clusters mapping to surface
    Probabilistic map
    """
    data0 = _sort_streamlines(cluters[0])
    stream_terminus_lh0 = np.array([s[0] for s in data0])
    stream_terminus_rh0 = np.array([s[-1] for s in data0])

    coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    dist_lh0 = cdist(coords_lh, stream_terminus_lh0)
    vert_lh_label = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    vert_lh_label[vert_lh_label > 0] = 1

    coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    dist_rh0 = cdist(coords_rh, stream_terminus_rh0)
    vert_rh_label = np.array([float(np.array(dist_rh0[n] < 5).sum(axis=0)) for n in range(len(dist_rh0[:]))])
    vert_rh_label[vert_rh_label > 0] = 1

    for i in range(len(cluters)):
        data = _sort_streamlines(cluters[i])
        stream_terminus_lh = np.array([s[0] for s in data])
        stream_terminus_rh = np.array([s[-1] for s in data])

        dist_lh = cdist(coords_lh, stream_terminus_lh)
        vert_lh_value = np.array([np.array(dist_lh[j] < 5).sum(axis=0) for j in range(len(dist_lh[:]))])

        dist_rh = cdist(coords_rh, stream_terminus_rh)
        vert_rh_value = np.array([np.array(dist_rh[k] < 5).sum(axis=0) for k in range(len(dist_rh[:]))])

        if i != 0:
            vert_lh_value[vert_lh_value > 0] = 1
            vert_lh_label += vert_lh_value

            vert_rh_value[vert_rh_value > 0] = 1
            vert_rh_label += vert_rh_value

    vert_lh_label /= len(cluters)
    vert_rh_label /= len(cluters)

    return vert_lh_label, vert_rh_label


def clusters_terminus2surface_mpm(cluters, geo_path):
    """
    Clusters mapping to surface
    Maximum probabilistic map
    """
    data0 = _sort_streamlines(cluters[0])
    stream_terminus_lh0 = np.array([s[0] for s in data0])
    stream_terminus_rh0 = np.array([s[-1] for s in data0])

    coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    dist_lh0 = cdist(coords_lh, stream_terminus_lh0)
    vert_lh_label = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    vert_lh_label[vert_lh_label > 0] = 1
    vert_lh_label_array = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    vert_lh_label_array.shape = (1, vert_lh_label_array.shape[0])

    coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    dist_rh0 = cdist(coords_rh, stream_terminus_rh0)
    vert_rh_label = np.array([float(np.array(dist_rh0[n] < 5).sum(axis=0)) for n in range(len(dist_rh0[:]))])
    vert_rh_label[vert_rh_label > 0] = 1
    vert_rh_label_array = np.array([float(np.array(dist_rh0[n] < 5).sum(axis=0)) for n in range(len(dist_rh0[:]))])
    vert_rh_label_array.shape = (1, vert_rh_label_array.shape[0])

    for i in range(len(cluters)):
        data = _sort_streamlines(cluters[i])
        stream_terminus_lh = np.array([s[0] for s in data])
        stream_terminus_rh = np.array([s[-1] for s in data])

        dist_lh = cdist(coords_lh, stream_terminus_lh)
        vert_lh_value = np.array([np.array(dist_lh[j] < 5).sum(axis=0) for j in range(len(dist_lh[:]))])
        vert_lh_label_max = np.array([vert_lh_label_array[:, com_index].max()
                                      for com_index in range(vert_lh_label_array.shape[1])])
        vert_lh_label[vert_lh_value > vert_lh_label_max] = i + 1
        vert_lh_label_array = np.vstack((vert_lh_label_array, vert_lh_value))

        dist_rh = cdist(coords_rh, stream_terminus_rh)
        vert_rh_value = np.array([np.array(dist_rh[k] < 5).sum(axis=0) for k in range(len(dist_rh[:]))])
        vert_rh_label_max = np.array([vert_rh_label_array[:, com_id].max()
                                      for com_id in range(vert_rh_label_array.shape[1])])
        vert_rh_label[vert_rh_value > vert_rh_label_max] = i + 1
        vert_rh_label_array = np.vstack((vert_rh_label_array, vert_rh_value))

    return vert_lh_label, vert_rh_label
