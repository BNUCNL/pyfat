# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection
# load data
file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream.tck'
fasciculus = Fasciculus(file)


# extract CC
fibselection = FibSelection(fasciculus)
L_temp_need0 = fibselection.endpoint_dissimilarity()
fasciculus.set_data(L_temp_need0)
L_temp_need1 = fibselection.single_point_mid_sag()
fasciculus.set_data(L_temp_need1)

out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/996782/Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_single.tck'
fasciculus.save2tck(out_path)
