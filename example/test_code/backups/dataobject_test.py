# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection

# lh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#          'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_lh_occipital5.tck'
# rh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#          'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_rh_occipital5.tck'
out_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
         'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital3.tck'

# fasciculus = Fasciculus(lh_fib)
# fasciculus_t = Fasciculus(rh_fib)
# fib = fasciculus.hemi_fib_merge(fasciculus_t.get_data())
# fasciculus.set_data(fib)
# fasciculus.save2tck(out_fib)

out_hemi_lh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital3.tck'
out_hemi_rh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital3.tck'
fasciculus = Fasciculus(out_fib)
fib = fasciculus.separation_fib_to_hemi()
fasciculus.set_data(fib[0])
fasciculus.save2tck(out_hemi_lh_fib)
fasciculus.set_data(fib[1])
fasciculus.save2tck(out_hemi_rh_fib)
