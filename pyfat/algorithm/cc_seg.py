# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.core.dataobject import Fasciculus


def cc_seg_region(vol_path, roi_fib_paths_suffix):
    """
    Segment cc according to roi fibs
    """
    img = nib.load(vol_path)
    counts = np.zeros(img.shape)
    roi_name_list = os.listdir(roi_fib_paths_suffix)
    for roi_i in range(len(roi_name_list)):
        roi_fib_path = os.path.join(roi_fib_paths_suffix, roi_name_list[roi_i])
        fibs = apply_affine(npl.inv(img.affine), Fasciculus(roi_fib_path).xmin_nodes())
        for n in fibs:
            counts[int(n[0]), int(n[1]), int(n[2])] = roi_i + 1

    return counts


def cc_seg_regions(vol_path, roi_fib_paths_suffix):
    """
    Segment cc according to roi fibs
    """
    img = nib.load(vol_path)
    counts = np.zeros(img.shape)
    roi_name_list = os.listdir(roi_fib_paths_suffix)
    for roi_i in range(len(roi_name_list)):
        files = os.listdir(os.path.join(roi_fib_paths_suffix, roi_name_list[roi_i]))
        for f in files:
            roi_fib_path = os.path.join(roi_fib_paths_suffix, roi_name_list[roi_i], f)
            fibs = apply_affine(npl.inv(img.affine), Fasciculus(roi_fib_path).xmin_nodes())
            for n in fibs:
                counts[int(n[0]), int(n[1]), int(n[2])] = roi_i + 1

    return counts


def cc_seg_same_regions(vol_path, lr_region_path_suffix):
    """
     Segment cc according to lr same regions.
    """
    img = nib.load(vol_path)
    counts = np.zeros(img.shape)
    roi_name_list = os.listdir(lr_region_path_suffix)
    roi_fib_path = os.path.join(lr_region_path_suffix, roi_name_list[0])
    fibs_points = apply_affine(npl.inv(img.affine), Fasciculus(roi_fib_path).xmin_nodes())
    for n in fibs_points:
        counts[int(n[0]), int(n[1]), int(n[2])] += 1

    if len(roi_name_list) == 2:
        roi_fib_path = os.path.join(lr_region_path_suffix, roi_name_list[1])
        fibs_points = apply_affine(npl.inv(img.affine), Fasciculus(roi_fib_path).xmin_nodes())
        for m in fibs_points:
            if counts[int(m[0]), int(m[1]), int(m[2])] != 0:
                counts[int(m[0]), int(m[1]), int(m[2])] += 1

    return counts


def endpoints_axis2cc(vol_path, streamlines_path, axis='y', mode='max'):
    """
    Endpoints of streamlines mapping to cc.
    axis: 'x', 'y', 'z'
    mode: 'max', 'min', 'mean'
    """
    img = nib.load(vol_path)
    counts_l = np.zeros(img.shape)
    counts_r = np.zeros(img.shape)
    fibs_points = apply_affine(npl.inv(img.affine), Fasciculus(streamlines_path).xmin_nodes()).astype(int)
    streamlines = Fasciculus(streamlines_path).sort_streamlines()
    if axis == 'x':
        endpoints_l = np.array([fib[0][0] for fib in streamlines])
        endpoints_r = np.array([fib[-1][0] for fib in streamlines])
    elif axis == 'y':
        endpoints_l = np.array([fib[0][1] for fib in streamlines])
        endpoints_r = np.array([fib[-1][1] for fib in streamlines])
    else:
        endpoints_l = np.array([fib[0][2] for fib in streamlines])
        endpoints_r = np.array([fib[-1][2] for fib in streamlines])
    for i in range(len(streamlines)):
        index_i = fibs_points == np.array([fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]])
        index_i = index_i.sum(axis=1)
        inddex = index_i == 3
        if mode == 'max':
            counts_l[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_l[inddex].max()
            counts_r[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_r[inddex].max()
        elif mode == 'min':
            counts_l[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_l[inddex].min()
            counts_r[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_r[inddex].min()
        else:
            counts_l[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_l[inddex].mean()
            counts_r[fibs_points[i][0], fibs_points[i][1], fibs_points[i][2]] = endpoints_r[inddex].mean()

    return counts_l, counts_r
