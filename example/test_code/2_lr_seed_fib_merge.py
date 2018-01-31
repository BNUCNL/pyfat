# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus

lh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
         'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lh_occipital5.tck'
rh_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
         'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rh_occipital5.tck'
out_fib = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
         'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_occipital5.tck'


fasciculus = Fasciculus(lh_fib)
fasciculus_t = Fasciculus(rh_fib)
fib = fasciculus.hemi_fib_merge(fasciculus.get_data(), fasciculus_t.get_data())
fasciculus.set_data(fib)
fasciculus.save2tck(out_fib)
