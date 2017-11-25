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
    for path_i in range(len(roi_name_list)):
        roi_fib_path = os.path.join(lr_region_path_suffix, roi_name_list[path_i])
        fibs_points = apply_affine(npl.inv(img.affine), Fasciculus(roi_fib_path).xmin_nodes())
        for n in fibs_points:
            counts[int(n[0]), int(n[1]), int(n[2])] += 1
    counts[counts != 2] = 0

    return counts
