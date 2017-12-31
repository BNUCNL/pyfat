# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l


"""
The module consits of functions which map fasciculus information to brain volume or cortical surface, including,
endpoint mapping,density mapping, midsag plane mapping. 
"""

import os
import nibabel as nib
import numpy as np
from nibabel.spatialimages import ImageFileError
from scipy.spatial.distance import cdist
import dipy.tracking.utils as ditu
import nibabel.streamlines.array_sequence as nibas
from dipy.segment.quickbundles import QuickBundles

import numpy.linalg as npl
from nibabel.affines import apply_affine


# fiber density of volume
def fib_density_map(volume, fiber):
    """
    fiber to volume density map
    Parameters
    ----------
    volume : volume data
    fiber : streamlines data

    Return
    ------
    streamline density in each voxel
    """
    shape = volume.shape
    affine = volume.affine
    streamlines = fiber
    voxel_size = nib.affine.voxel_size(affine)
    image_volume = ditu.density_map(streamlines, vol_dims=shape, voxel_size=voxel_size, affine=affine)

    return image_volume


def _sort_streamlines(fasciculus_data):
    """
    Store order of streamline is from left to right.
    Parameters
    ----------
    fasciculus_data: streamlines data

    Return
    ------
    sorted streamlines
    """
    fasciculus_data_sort = nibas.ArraySequence()
    for i in range(len(fasciculus_data)):
        if fasciculus_data[i][0][0] < 0:
            fasciculus_data_sort.append(fasciculus_data[i])
        else:
            fasciculus_data_sort.append(fasciculus_data[i][::-1])
    return fasciculus_data_sort


def terminus2surface_nearest_pts(streamlines, geo_path):
    """
    Streamline endpoints mapping to surface
    Parameters
    ----------
    streamlines: streamline data
    geo_path: surface data path

    Return
    ------
    endpoints map on surface
    """
    streamlines = _sort_streamlines(streamlines)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    # s = s0 + s_t
    # stream_terminus = np.array(s)
    stream_terminus_lh = np.array(s0)  # stream_terminus[stream_terminus[:, 0] < 0]
    stream_terminus_rh = np.array(s_t)  # stream_terminus[stream_terminus[:, 0] > 0]

    suffix = os.path.split(geo_path[0])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[0]).darrays
        coords_lh, faces_lh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_lh = cdist(stream_terminus_lh, coords_lh)
    nearest_vert_lh = np.array([dist_lh[i].argmin() for i in range(len(dist_lh[:]))])

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_rh = cdist(stream_terminus_rh, coords_rh)
    nearest_vert_rh = np.array([dist_rh[i].argmin() for i in range(len(dist_rh[:]))])
    # print nearest_vert_lh, nearest_vert_rh

    return nearest_vert_lh, nearest_vert_rh


def terminus2surface_map(streamlines, geo_path):
    """
    Streamline endpoints areas mapping to surface
    Parameters
    ----------
    streamlines: streamline data
    geo_path: surface data path

    Return
    ------
    endpoints areas map on surface
    """
    streamlines = _sort_streamlines(streamlines)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    # s = s0 + s_t
    # stream_terminus = np.array(s)
    stream_terminus_lh = np.array(s0)  # stream_terminus[stream_terminus[:, 0] < 0]
    stream_terminus_rh = np.array(s_t)  # stream_terminus[stream_terminus[:, 0] > 0]

    suffix = os.path.split(geo_path[0])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[0]).darrays
        coords_lh, faces_lh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_lh = cdist(coords_lh, stream_terminus_lh)
    vert_lh_value = np.array([float(np.array(dist_lh[i] < 5).sum(axis=0)) for i in range(len(dist_lh[:]))])

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_rh = cdist(coords_rh, stream_terminus_rh)
    vert_rh_value = np.array([float(np.array(dist_rh[i] < 5).sum(axis=0)) for i in range(len(dist_rh[:]))])

    return vert_lh_value, vert_rh_value


def terminus2surface_density_map(streamlines, geo_path):
    """
    Streamline endpoints areas mapping to surface
    streamlines > 1000
    Parameters
    ----------
    streamlines: streamline data
    geo_path: surface data path

    Return
    ------
    endpoints areas map on surface
    """
    streamlines = _sort_streamlines(streamlines)
    bundles = QuickBundles(streamlines, 10, 12)
    # bundles.remove_small_clusters(10)
    clusters = bundles.clusters()
    data_clusters = []
    for key in clusters.keys():
        data_clusters.append(streamlines[clusters[key]['indices']])

    data0 = data_clusters[0]
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
    vert_lh_value = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))
    dist_rh0 = cdist(coords_rh, stream_terminus_rh0)
    vert_rh_value = np.array([float(np.array(dist_rh0[n] < 5).sum(axis=0)) for n in range(len(dist_rh0[:]))])

    for i in range(len(data_clusters)):
        data = data_clusters[i]
        stream_terminus_lh = np.array([s[0] for s in data])
        stream_terminus_rh = np.array([s[-1] for s in data])

        dist_lh = cdist(coords_lh, stream_terminus_lh)
        vert_lh_value_i = np.array([np.array(dist_lh[j] < 5).sum(axis=0) for j in range(len(dist_lh[:]))])

        dist_rh = cdist(coords_rh, stream_terminus_rh)
        vert_rh_value_i = np.array([np.array(dist_rh[k] < 5).sum(axis=0) for k in range(len(dist_rh[:]))])

        if i != 0:
            vert_lh_value += vert_lh_value_i
            vert_rh_value += vert_rh_value_i

    return vert_lh_value, vert_rh_value


def terminus2volume_nearest_vox(streamlines, volume_path):
    """
    Points mapping to volume
    streamlines > 1000
    Parameters
    ----------
    streamlines: streamline data
    volume_path: volume data path

    Return
    ------
    endpoints map im volume
    """
    img = nib.load(volume_path)
    streamlines = _sort_streamlines(streamlines)
    stream_terminus_lh = apply_affine(npl.inv(img.affine), np.array([s[0] for s in streamlines]))
    stream_terminus_rh = apply_affine(npl.inv(img.affine), np.array([s[-1] for s in streamlines]))
    counts = np.zeros(img.shape)
    for st in stream_terminus_lh:
        i = st[0]
        j = st[1]
        k = st[2]
        counts[int(i), int(j), int(k)] += 1

    for st in stream_terminus_rh:
        i = st[0]
        j = st[1]
        k = st[2]
        counts[int(i), int(j), int(k)] += 1

    return counts


def terminus2volume_density_map(streamlines, volume_path):
    """
    Points mapping to volume
    streamlines > 1000
    Parameters
    ----------
    streamlines: streamline data
    volume_path: volume data path

    Return
    ------
    endpoints areas map(26 direct neighbor points) im volume
    """
    img = nib.load(volume_path)
    streamlines = _sort_streamlines(streamlines)
    stream_terminus_lh = apply_affine(npl.inv(img.affine), np.array([s[0] for s in streamlines]))
    stream_terminus_rh = apply_affine(npl.inv(img.affine), np.array([s[-1] for s in streamlines]))

    # 26 direct neighbor points
    neighbors = [[1, 0, 0],
                 [-1, 0, 0],
                 [0, 1, 0],
                 [0, -1, 0],
                 [0, 0, -1],
                 [0, 0, 1],
                 [1, 1, 0],
                 [1, 1, 1],
                 [1, 1, -1],
                 [0, 1, 1],
                 [-1, 1, 1],
                 [1, 0, 1],
                 [1, -1, 1],
                 [-1, -1, 0],
                 [-1, -1, -1],
                 [-1, -1, 1],
                 [0, -1, -1],
                 [1, -1, -1],
                 [-1, 0, -1],
                 [-1, 1, -1],
                 [0, 1, -1],
                 [0, -1, 1],
                 [1, 0, -1],
                 [1, -1, 0],
                 [-1, 0, 1],
                 [-1, 1, 0]]

    counts = np.zeros(img.shape)
    for st in stream_terminus_lh:
        i = st[0]
        j = st[1]
        k = st[2]
        counts[int(i), int(j), int(k)] += 1
        for n in range(26):
            i_n = int(i) + neighbors[n][0]
            j_n = int(j) + neighbors[n][1]
            k_n = int(k) + neighbors[n][2]
            inside = (i_n >= 0) and (i_n < img.shape[0]) and (j_n >= 0) and \
                     (j_n < img.shape[1]) and (k_n >= 0) and (k_n < img.shape[2])
            if inside:
                counts[i_n, j_n, k_n] += 1

    for st in stream_terminus_rh:
        i = st[0]
        j = st[1]
        k = st[2]
        counts[int(i), int(j), int(k)] += 1
        for n in range(26):
            i_n = int(i) + neighbors[n][0]
            j_n = int(j) + neighbors[n][1]
            k_n = int(k) + neighbors[n][2]
            inside = (i_n >= 0) and (i_n < img.shape[0]) and (j_n >= 0) and \
                     (j_n < img.shape[1]) and (k_n >= 0) and (k_n < img.shape[2])
            if inside:
                counts[i_n, j_n, k_n] += 1

    return counts
