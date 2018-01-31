# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.io.load import load_tck
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection


source_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_rh_occipital8.tck'

fasciculus = Fasciculus(source_path)
fibs = FibSelection(fasciculus)
fib = fibs.lr_rat(5)
fasciculus.set_data(fib)
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_rh_occipital8_lr5.tck'
fasciculus.save2tck(out_path)


