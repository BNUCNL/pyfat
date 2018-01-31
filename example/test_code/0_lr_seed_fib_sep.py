# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus

# load origin fib
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_single.tck'

fasciculus = Fasciculus(tck_path)
streamlines = fasciculus.get_data()
fib = fasciculus.hemi_fib_separation()

# save left hemisphere seed fib
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lh.tck'
fasciculus.set_data(fib[0])
fasciculus.save2tck(out_path)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rh.tck'
fasciculus.set_data(fib[1])
fasciculus.save2tck(out_path)
