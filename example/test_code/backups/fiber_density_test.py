# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
from pyfat.io.load import load_tck
from pyfat.algorithm.fasc_mapping import fib_density_map

img = nib.load("/home/brain/workingdir/data/dwi/hcp/preprocessed/"
                "response_dhollander/100206/Structure/T1w_short.nii.gz")
img_cc = load_tck('/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                'response_dhollander/100206/result/CC_fib.tck')
output = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
            'response_dhollander/100206/result/CC_fib_density_map.nii.gz'
fib_density_map(img, img_cc, output)
