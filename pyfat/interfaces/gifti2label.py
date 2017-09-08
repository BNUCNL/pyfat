# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np

def gifti2label(label_gifti, white, label_number, label_label):
    label = nib.load(label_gifti)
    label_data = label.darrays
    labels = label_data[0].data

    geo = nib.freesurfer.read_geometry(white)
    geo_coords, geo_faces = geo

    FFA_label = []
    FFA_coords = []
    for i in range(len(labels)):
        if labels[i] == label_number:
            FFA_label.append(i)
            FFA_coords.append(list(geo_coords[i]))

    for j in range(len(FFA_label)):
        FFA_coords[j].insert(0, FFA_label[j])
        FFA_coords[j].append(float(0))

    FFA_list = FFA_coords
    FFA_array = np.asarray(FFA_list)

    np.savetxt(label_label, FFA_list, fmt=['%d', '%f', '%f', '%f', '%f'],
               header=str(FFA_array.shape[0]), comments='#!ascii label  , from subject  vox2ras=TkReg\n')

if __name__ == '__main__':
    label_gifti = '/home/brain/workingdir/HCP_label/brain_label/fsaverage.label.L.164k_fsavg_L.label.gii'
    white = '/home/brain/workingdir/HCP_label/brain_label/lh.white'
    label_label = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100206/label/lh_OFA.label'

    gifti2label(label_gifti, white, 202, label_label)
