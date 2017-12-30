# !/usr/bin/python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:l

import os
import numpy as np
import nibabel as nib
from scipy.spatial.distance import cdist
from nibabel.spatialimages import ImageFileError
from dipy.tracking import streamline, utils
import nibabel.streamlines.array_sequence as nibas


def _sort_streamlines(fasciculus_data):
    """Store order of streamline is from left to right."""
    fasciculus_data_sort = nibas.ArraySequence()
    for i in range(len(fasciculus_data)):
        if fasciculus_data[i][0][0] < 0:
            fasciculus_data_sort.append(fasciculus_data[i])
        else:
            fasciculus_data_sort.append(fasciculus_data[i][::-1])
    return fasciculus_data_sort


def select_by_vol_roi(streamlines, target_mask, affine, include=True):
    """
    Include or exclude the streamlines according to a ROI
    Parameters
    ----------
    streamlines: streamline data
    target_mask: volume roi
    affine: project streamline to roi space
    include: True or False (include or exclude)

    Return
    ------
    roi_streamlines: extracted streamlines
    """
    roi_selection = utils.target(streamlines=streamlines, target_mask=target_mask,
                                 affine=affine, include=include)
    roi_streamlines = list(roi_selection)

    return roi_streamlines


def select_by_vol_rois(streamlines, rois, include, mode=None, affine=None, tol=None):
    """
    Include or exclude the streamlines according to some ROIs
    example
    >>>selection = select_by_vol_rois(streamlines, [mask1, mask2], [True, False], mode="both_end", tol=1.0)
    >>>selection = list(selection)
    """
    rois_selection = streamline.select_by_rois(streamline=streamline, rois=rois,
                                               include=include, mode=mode, affine=affine, tol=tol)
    rois_streamlines = list(rois_selection)

    return rois_streamlines


def select_by_surf_rois(streamlines_ori, surf_rois, geo_path, include=[True, True]):
    """
    Include or exclude the streamlines according to some surface ROIs
    Parameters
    ----------
    streamlines_ori: origin streamlines
    surf_rois: left and right surface rois
    geo_path: left and right surface geometry

    Return
    ------
    lh_rois_streamlines: extracted streamlines by left roi
    rh_rois_streamlines: extracted streamlines by right roi
    lrh_rois_streamlines: intersection of lh_rois_streamlines and rh_rois_streamlines
    """
    streamlines = _sort_streamlines(streamlines_ori)
    s0 = [s[0] for s in streamlines]
    s_t = [s[-1] for s in streamlines]
    # s = s0 + s_t
    # stream_terminus = np.array(s)
    stream_terminus_lh = np.array(s0)  # stream_terminus[stream_terminus[:, 0] < 0]
    stream_terminus_rh = np.array(s_t)  # stream_terminus[stream_terminus[:, 0] > 0]

    # load surf geometry
    suffix = os.path.split(geo_path[0])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_lh, faces_lh = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[0]).darrays
        coords_lh, faces_lh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))

    suffix = os.path.split(geo_path[1])[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords_rh, faces_rh = nib.freesurfer.read_geometry(geo_path[1])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path[1]).darrays
        coords_rh, faces_rh = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))

    dist_lh = cdist(coords_lh[surf_rois[0] > 0], stream_terminus_lh)
    lh_stream_index = np.array(len(streamlines) * [False])
    for i in range(len(dist_lh[:])):
        temp_index = np.array(dist_lh[i] < 5)
        lh_stream_index += temp_index

    dist_rh = cdist(coords_rh[surf_rois[1] > 0], stream_terminus_rh)
    rh_stream_index = np.array(len(streamlines) * [False])
    for j in range(len(dist_rh[:])):
        temp_index = np.array(dist_rh[j] < 5)
        rh_stream_index += temp_index

    lh_rois_streamlines = streamlines_ori[lh_stream_index]
    rh_rois_streamlines = streamlines_ori[rh_stream_index]
    lrh_rois_streamlines = streamlines_ori[np.array([lh_stream_index, rh_stream_index]).sum(axis=0) == 2]
    if len(lrh_rois_streamlines) == 0:
        print "ROI-1 to ROI-2 have no connection!"
        return lh_rois_streamlines, rh_rois_streamlines
    else:
        return lh_rois_streamlines, rh_rois_streamlines, lrh_rois_streamlines
