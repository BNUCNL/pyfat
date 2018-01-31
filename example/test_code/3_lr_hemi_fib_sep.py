# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus

tck_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
          'response_dhollander/subjects_all/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital5_all_subjects.tck'

out_hemi_lh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/subjects_all/Diffusion/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_all_subjects.tck'
out_hemi_rh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/subjects_all/Diffusion/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5_all_subjects.tck'

fasciculus = Fasciculus(tck_fib)
fib = fasciculus.separation_fib_to_hemi()
fasciculus.set_data(fib[0])
fasciculus.save2tck(out_hemi_lh_fib)
fasciculus.set_data(fib[1])
fasciculus.save2tck(out_hemi_rh_fib)
