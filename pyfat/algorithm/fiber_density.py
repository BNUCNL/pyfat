# !/usr/bin/python
# -*- coding: utf-8 -*-


import nibabel as nib
import dipy.tracking.utils as ditu

# fiber density of volume
def fib_density_map(volume, fiber, output):
    '''
    fiber density map
    :param volume: structure image T1w
    :param fiber: tck file
    :param output: density map file
    :return:
    '''
    shape = volume.shape
    affine = volume.affine
    streamstck = fiber.streamlines
    image_volume = ditu.density_map(streamstck, vol_dims=shape, voxel_size=0.625, affine=affine)

    dm_img = nib.Nifti1Image(image_volume.astype("int16"), affine)
    dm_img.to_filename(output)
