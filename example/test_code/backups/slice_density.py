# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.io.load import load_tck
from pyfat.core.dataobject import Fasciculus
from pyfat.viz.visualization import show_slice_density

data_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/100408/Structure/T1w_short.nii.gz'
img = nib.load(data_path)

tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/Diffusion/1M_20_002_dynamic250.tck'
fas = Fasciculus(tck_path)
Ls_temp = fas.xmin_nodes()
show_slice_density(img, Ls_temp)


