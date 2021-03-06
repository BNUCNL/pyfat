# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

from __future__ import division
import os
from nibabel.spatialimages import ImageFileError
import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
import nibabel.streamlines.array_sequence as nibas
from scipy.spatial.distance import pdist, squareform
from dipy.tracking.streamline import set_number_of_points
from dipy.align.streamlinear import StreamlineLinearRegistration

from pyfat.core.dataobject import Fasciculus


def coordinate_dist(coordinate, metric='euclidean'):
    """
    Compute coordinate distance
    Parameters
    ----------
    coordinate: ndarray
        An m by n array of m original observations in an
        n-dimensional space.
    metric: string or function
        The distance metric to use. The distance function can
        be 'braycurtis', 'canberra', 'chebyshev', 'cityblock',
        'correlation', 'cosine', 'dice', 'euclidean', 'hamming',
        'jaccard', 'kulsinski', 'mahalanobis', 'matching',
        'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
        'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.

    Return
    ------
    matrix of distance
    """
    dist_temp = pdist(coordinate, metric)
    sdist = squareform(dist_temp)
    return sdist


def bundle_registration(cb_subj1, cb_subj2, pts=12):
    """
    Register two bundle from two subjects
    directly in the space of streamlines
    Parameters
    ----------
    cb_subj1: first subject's bundle
    cb_subj2: second subject's bundle
    pts: each streamline is divided into sections

    Return
    ------
    registration bundle
    """
    cb_subj1 = set_number_of_points(cb_subj1, pts)
    cb_subj2 = set_number_of_points(cb_subj2, pts)

    srr = StreamlineLinearRegistration()
    srm = srr.optimize(static=cb_subj1, moving=cb_subj2)
    cb_subj2_aligned = srm.transform(cb_subj2)

    return cb_subj2_aligned


def _sort_streamlines(fasciculus_data):
    """Store order of streamline is from left to right."""
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
    Parameters
    ----------
    cluters: clusters data
    geo_path: surface path

    Return
    ------
    left and right hemisphere pm matrix: vertex x clusters
    """
    data0 = _sort_streamlines(cluters[0])
    stream_terminus_lh0 = np.array([s[0] for s in data0])
    stream_terminus_rh0 = np.array([s[-1] for s in data0])

    suffix = os.path.split(geo_path[0])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[0]).darrays
        coords_lh, faces_lh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_lh0 = cdist(coords_lh, stream_terminus_lh0)
    vert_lh_label = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    # vert_lh_label[vert_lh_label > 0] = 1

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_rh0 = cdist(coords_rh, stream_terminus_rh0)
    vert_rh_label = np.array([float(np.array(dist_rh0[n] < 5).sum(axis=0)) for n in range(len(dist_rh0[:]))])
    # vert_rh_label[vert_rh_label > 0] = 1

    for i in range(len(cluters)):
        data = _sort_streamlines(cluters[i])
        stream_terminus_lh = np.array([s[0] for s in data])
        stream_terminus_rh = np.array([s[-1] for s in data])

        dist_lh = cdist(coords_lh, stream_terminus_lh)
        vert_lh_value = np.array([np.array(dist_lh[j] < 5).sum(axis=0) for j in range(len(dist_lh[:]))])

        dist_rh = cdist(coords_rh, stream_terminus_rh)
        vert_rh_value = np.array([np.array(dist_rh[k] < 5).sum(axis=0) for k in range(len(dist_rh[:]))])

        if i != 0:
            vert_lh_label = np.vstack((vert_lh_label, vert_lh_value))
            vert_rh_label = np.vstack((vert_rh_label, vert_rh_value))

    vert_lh_label /= vert_lh_label.sum(axis=0)
    vert_rh_label /= vert_rh_label.sum(axis=0)

    return vert_lh_label, vert_rh_label


def clusters_terminus2surface_mpm(cluters, geo_path):
    """
    Clusters mapping to surface
    Maximum probabilistic map
    Parameters
    ----------
    cluters: clusters data
    geo_path: surface path

    Return
    ------
    left and right hemisphere mpm : vertex x 1
    """
    data0 = _sort_streamlines(cluters[0])
    stream_terminus_lh0 = np.array([s[0] for s in data0])
    stream_terminus_rh0 = np.array([s[-1] for s in data0])

    suffix = os.path.split(geo_path[0])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[0]).darrays
        coords_lh, faces_lh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_lh0 = cdist(coords_lh, stream_terminus_lh0)
    vert_lh_label = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    vert_lh_label[vert_lh_label > 0] = 1
    vert_lh_label_array = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])
    vert_lh_label_array.shape = (1, vert_lh_label_array.shape[0])

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
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


def clusters_terminus2surface_mpm_short(pm_matrix):
    """
    Clusters mapping to surface
    Maximum probabilistic map
    Parameters
    ----------
    pm_matrix: result of clusters_terminus2surface_pm

    Return
    ------
    mpm matrix: vertex x 1
    """
    mpm = pm_matrix.argmax(axis=0)+1

    return mpm


def create_registration_paths(prepath, pospath):
    """
    Create muti-bundle registration path.
    Parameters
    ----------
    prepath: the first half of the path, which includes many subjects
    pospath: the final part of the path, which is a particular file path of subject

    Return
    ------
    paths_file: list
    eg: ['prepath/subject1/pospath', 'prepath/subject2/pospath', ...]
    """
    files = os.listdir(prepath)
    subjects = []
    for name in files:
        try:
            int(name)
            subjects.append(name)
        except ValueError:
            pass
    # print subjects

    paths_file = []
    for subject in subjects:
        paths_file.append(os.path.join(prepath, subject, pospath))

    return paths_file


def muti_bundle_registration(paths_file, pts=12):
    """
    muti-bundle registration and consolidation
    Parameters
    ----------
    paths_file: list; muti_bundle file path
    pts: each streamline is divided into sections

    Return
    ------
    new header: include id of each streamline that comes from different subjects
    registration and consolidation bundle
    """
    fas = Fasciculus(paths_file[0])
    # print fas.get_header()
    bundle_header = {'fasciculus_id': None}
    sub1 = fas.get_data()
    bundle_header['fasciculus_id'] = len(sub1) * [int(paths_file[0].split('/')[9])]
    sub2 = Fasciculus(paths_file[1]).get_data()
    subj2_aligned = bundle_registration(sub1, sub2, pts=pts)
    bundle = fas.fib_merge(sub1, subj2_aligned)
    bundle_header['fasciculus_id'] += (len(bundle) - len(sub1)) * [int(paths_file[1].split('/')[9])]
    # print bundle_header
    # print len(bundle)
    for index in range(len(paths_file))[2:]:
        # print paths_file[index]
        sub = Fasciculus(paths_file[index]).get_data()
        sub_aligned = bundle_registration(sub1, sub, pts=pts)
        lenth = len(bundle)
        bundle = fas.fib_merge(bundle, sub_aligned)
        bundle_header['fasciculus_id'] += (len(bundle) - lenth) * [int(paths_file[index].split('/')[9])]

    fas.update_header(bundle_header)
    fas.set_data(nibas.ArraySequence(bundle))

    return fas
