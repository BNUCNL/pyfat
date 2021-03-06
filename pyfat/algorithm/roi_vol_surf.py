# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine
from nibabel.spatialimages import ImageFileError


def roi_vol2surf(roi_vol_path, geo_path):
    """
    Transform rois from volume to surface.
    Parameters
    ----------
    roi_vol_path: volume roi path
    geo_path: left and right surface geometry path

    Return
    ------
    left and right surface rois
    """
    # load volume roi file
    roi_img = nib.load(roi_vol_path)
    img_data = roi_img.get_data()

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

    lh_labels = np.array(len(coords_lh) * [None])
    coords_lh_affine = apply_affine(npl.inv(roi_img.affine), coords_lh)
    for index in range(len(coords_lh_affine)):
        lh_labels[index] = img_data[int(coords_lh_affine[index][0]),
                                    int(coords_lh_affine[index][1]), int(coords_lh_affine[index][2])]

    rh_labels = np.array(len(coords_rh) * [None])
    coords_rh_affine = apply_affine(npl.inv(roi_img.affine), coords_rh)
    for index in range(len(coords_rh_affine)):
        rh_labels[index] = img_data[int(coords_rh_affine[index][0]),
                                    int(coords_rh_affine[index][1]), int(coords_rh_affine[index][2])]

    return lh_labels, rh_labels


def label2surf_roi(label, geo_path):
    """
    From .label to surface vertex value.
    Parameters
    ----------
    label: .label file path
    geo_path: surface geometry path

    Return
    ------
    left and right surface roi
    """
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

    # load .label
    l_label_index = nib.freesurfer.read_label(label[0])
    r_label_index = nib.freesurfer.read_label(label[1])

    # initialize surface vertex value
    l_label_value = np.array(len(coords_lh) * [0])
    r_label_value = np.array(len(coords_rh) * [0])

    # generate surface value
    l_label_value[l_label_index] = 1
    r_label_value[r_label_index] = 1

    return l_label_value, r_label_value


def roi_surf2vol(roi_surf_path, geo_path, vol_path):
    """
    Transform rois from surface to volume.
    Parameters
    ----------
    roi_surf_path: surface roi path
    geo_path: surface geometry path
    vol_path: target volume

    Return
    ------
    volume rois
    """
    # load parcelltion data
    vertices, colortable, label = nib.freesurfer.read_annot(roi_surf_path)

    # load surf geometry
    suffix = os.path.split(geo_path)[1].split('.')[-1]
    if suffix in ('white', 'inflated', 'pial'):
        coords, faces = nib.freesurfer.read_geometry(geo_path[0])
    elif suffix == 'gii':
        gii_data = nib.load(geo_path).darrays
        coords, faces = gii_data[0].data, gii_data[1].data
    else:
        raise ImageFileError('This file format-{} is not supported at present.'.format(suffix))

    # load volume data
    img = nib.load(vol_path)
    data_temp = np.zeros(img.shape)

    coords_affine = apply_affine(npl.inv(img.affine), coords)

    # parcellation of surf to volume
    for value in set(vertices):
        for c in coords_affine[vertices == value]:
            data_temp[int(c[0]), int(c[1]), int(c[2])] = value

    return data_temp
