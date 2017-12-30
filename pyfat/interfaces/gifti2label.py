# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np


def gifti2label(label_gifti, white, label_number, label_label):
    """
    Extract roi-label from a gifti file
    Parameters
    ----------
    label_gifti: gifti file of labels (whole  brain)
    white: surface geometry .white file
    label_number: label number
    label_label: save roi to label_label file .label

    Return
    ------
    .label file
    """
    label = nib.load(label_gifti)
    label_data = label.darrays
    labels = label_data[0].data

    geo = nib.freesurfer.read_geometry(white)
    geo_coords, geo_faces = geo

    roi_label = []
    roi_coords = []
    for i in range(len(labels)):
        if labels[i] == label_number:
            roi_label.append(i)
            roi_coords.append(list(geo_coords[i]))

    for j in range(len(roi_label)):
        roi_coords[j].insert(0, roi_label[j])
        roi_coords[j].append(float(0))

    roi_list = roi_coords
    roi_array = np.asarray(roi_list)

    np.savetxt(label_label, roi_list, fmt=['%d', '%f', '%f', '%f', '%f'],
               header=str(roi_array.shape[0]), comments='#!ascii label  , from subject  vox2ras=TkReg\n')
