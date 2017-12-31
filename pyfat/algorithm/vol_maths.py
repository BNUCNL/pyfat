# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib


def voll_volr_merge(vol_suffix):
    """Merge all vol files directory"""
    files_list = os.listdir(vol_suffix)
    img = nib.load(os.path.join(vol_suffix, files_list[0]))
    data = np.zeros(img.shape)
    for img_file in files_list:
        img_data = nib.load(os.path.join(vol_suffix, img_file)).get_data()
        data += img_data

    return data


def vold_volv_merge(d_files_path, v_files_path):
    d_files = os.listdir(d_files_path)
    v_files = os.listdir(v_files_path)
    img_d = nib.load(os.path.join(d_files_path, d_files[0]))
    img_v = nib.load(os.path.join(v_files_path, v_files[0]))
    data_d = np.zeros(img_d.shape)
    data_v = np.zeros(img_v.shape)
    for d in d_files:
        img_d = nib.load(os.path.join(d_files_path, d))
        data_d += img_d.get_data()
    for v in v_files:
        img_v = nib.load(os.path.join(v_files_path, v))
        data_v += img_v.get_data()

    return data_d, data_v


def make_mpm(pm, threshold):
    """
    Make maximum probabilistic map (mpm)
    ---------------------------------------
    Parameters:
        pm: probabilistic map
        threshold: threholds to mask probabilistic maps
    Return:
        mpm: maximum probabilisic map
    """
    pm_temp = np.empty((pm.shape[0], pm.shape[1], pm.shape[2], pm.shape[3]+1))
    pm_temp[..., range(1, pm.shape[3]+1)] = pm
    pm_temp[pm_temp < threshold] = 0
    mpm = np.argmax(pm_temp, axis=3)
    return mpm


def vold_volv_mpm(d_vol, v_vol):
    data_d = nib.load(d_vol).get_data()
    data_v = nib.load(v_vol).get_data()
    data_d[data_d < data_v] = 0
    data_v[data_v < data_d] = 0
    return data_d, data_v


def vol_mask_vol(vol, mask):
    """volume + mask"""
    vol_data = nib.load(vol).get_data()
    mask_data = nib.load(mask).get_data()

    vol_mask_data = vol_data * mask_data

    return vol_mask_data
