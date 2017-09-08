# !/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import division
import nipype.interfaces.mrtrix as mrt

def tck2trk(tckfile, volumefile, trkfile):
    tck2trk = mrt.MRTrix2TrackVis()
    tck2trk.inputs.in_file = tckfile
    tck2trk.inputs.image_file = volumefile
    tck2trk.inputs.out_filename = trkfile
    tck2trk.run()

if __name__ == '__mian__':
    in_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/100206/Diffusion/l250_hcp_FFA_projabs-0-abs-2-1.tck'
    image_file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                 'response_dhollander/100206/Diffusion/data.nii.gz'
    out_filename = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                   'response_dhollander/100206/Diffusion/l250_hcp_FFA_projabs-0-abs-2-1.trk'
    tck2trk(in_file, image_file, out_filename)
