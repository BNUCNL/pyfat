# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np


def gifti2label(label_gifti, white, label_number, label_label):
    """
    Extract ROI-label from a gifti file
    """
    label = nib.load(label_gifti)
    label_data = label.darrays
    labels = label_data[0].data

    geo = nib.freesurfer.read_geometry(white)
    geo_coords, geo_faces = geo

    ROI_label = []
    ROI_coords = []
    for i in range(len(labels)):
        if labels[i] == label_number:
            ROI_label.append(i)
            ROI_coords.append(list(geo_coords[i]))

    for j in range(len(ROI_label)):
        ROI_coords[j].insert(0, ROI_label[j])
        ROI_coords[j].append(float(0))

    ROI_list = ROI_coords
    ROI_array = np.asarray(ROI_list)

    np.savetxt(label_label, ROI_list, fmt=['%d', '%f', '%f', '%f', '%f'],
               header=str(ROI_array.shape[0]), comments='#!ascii label  , from subject  vox2ras=TkReg\n')
