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


if __name__ == '__main__':
    from pyfat.io.load import load_tck
    img = nib.load("/home/brain/workingdir/data/dwi/hcp/preprocessed/"
                   "response_dhollander/100206/Structure/T1w_short.nii.gz")
    img_cc = load_tck('/home/brain/workingdir/data/dwi/hcp/preprocessed/'
                  'response_dhollander/100206/result/CC_fib.tck')
    output = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/100206/result/CC_fib_density_map.nii.gz'
    fib_density_map(img, img_cc, output)


