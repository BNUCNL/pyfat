# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib


def gii2geo(geo_gii, geo_path):
    """
    Save geometry information.
    """
    gii_data = nib.load(geo_gii).darrays
    coords, faces = gii_data[0].data, gii_data[1].data
    nib.freesurfer.write_geometry(geo_path, coords, faces)
