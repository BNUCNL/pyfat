# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l


"""
The module consits of functions which map fasciculus information to brain volume or cortical surface, including,
endpoint mapping,density mapping, midsag plane mapping. 
"""

import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
import dipy.tracking.utils as ditu
import nibabel.streamlines.array_sequence as nibas
from dipy.segment.quickbundles import QuickBundles


# fiber density of volume
def fib_density_map(volume, fiber, output_path):
    """
    fiber to volume density map
    Parameters
    ----------
    volume : nifti img
        nifti img
    fiber : ArraySequence streamlines
        streamlines
    output : output path
            output path nii.gz

    Return
    ------
    output file nii.gz
    """
    shape = volume.shape
    affine = volume.affine
    streamlines = fiber
    voxel_size = nib.affine.voxel_size(affine)
    image_volume = ditu.density_map(streamlines, vol_dims=shape, voxel_size=voxel_size, affine=affine)

    dm_img = nib.Nifti1Image(image_volume.astype("int16"), affine)
    dm_img.to_filename(output_path)


def _sort_streamlines(fasciculus_data):
    fasciculus_data_sort = nibas.ArraySequence()
    for i in range(len(fasciculus_data)):
        if fasciculus_data[i][0][0] < 0:
            fasciculus_data_sort.append(fasciculus_data[i])
        else:
            fasciculus_data_sort.append(fasciculus_data[i][::-1])
    return fasciculus_data_sort


def terminus2surface_nearest_pts(streamlines, geo_path):
    """Points project surface"""
    streamlines = _sort_streamlines(streamlines)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    # s = s0 + s_t
    # stream_terminus = np.array(s)

    stream_terminus_lh = np.array(s0)  # stream_terminus[stream_terminus[:, 0] < 0]
    coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    dist_lh = cdist(stream_terminus_lh, coords_lh)
    nearest_vert_lh = np.array([dist_lh[i].argmin() for i in range(len(dist_lh[:]))])

    stream_terminus_rh = np.array(s_t)  # stream_terminus[stream_terminus[:, 0] > 0]
    coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    dist_rh = cdist(stream_terminus_rh, coords_rh)
    nearest_vert_rh = np.array([dist_rh[i].argmin() for i in range(len(dist_rh[:]))])
    # print nearest_vert_lh, nearest_vert_rh

    return nearest_vert_lh, nearest_vert_rh


def terminus2surface_map(streamlines, geo_path):
    """Points mapping to surface"""
    streamlines = _sort_streamlines(streamlines)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    # s = s0 + s_t
    # stream_terminus = np.array(s)

    stream_terminus_lh = np.array(s0)  # stream_terminus[stream_terminus[:, 0] < 0]
    coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    dist_lh = cdist(coords_lh, stream_terminus_lh)
    vert_lh_value = np.array([float(np.array(dist_lh[i] < 5).sum(axis=0)) for i in range(len(dist_lh[:]))])

    stream_terminus_rh = np.array(s_t)  # stream_terminus[stream_terminus[:, 0] > 0]
    coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    dist_rh = cdist(coords_rh, stream_terminus_rh)
    vert_rh_value = np.array([float(np.array(dist_rh[i] < 5).sum(axis=0)) for i in range(len(dist_rh[:]))])

    return vert_lh_value, vert_rh_value


def terminus2surface_density_map(streamlines, geo_path):
    """
    Points mapping to surface
    streamlines > 1000
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

    coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    dist_lh0 = cdist(coords_lh, stream_terminus_lh0)
    vert_lh_value = np.array([float(np.array(dist_lh0[m] < 5).sum(axis=0)) for m in range(len(dist_lh0[:]))])

    coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
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
