# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection
# load data
# file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#        'response_dhollander/100206/Diffusion/100k_sift_1M45006_dynamic250.tck'
file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/100408/result/result20vs45/Prob01_plenium_fib_vis.tck'
fasciculus = Fasciculus(file)


# extract CC
fibselection = FibSelection(fasciculus)
L_temp_need0 = fibselection.endpoint_dissimilarity()
fasciculus.set_data(L_temp_need0)
L_temp_need1 = fibselection.single_point_mid_sag()
fasciculus.set_data(L_temp_need1)
L_temp_need2 = fibselection.lr_step()
fasciculus.set_data(L_temp_need2)

out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100408/result/result20vs45/Prob01_plenium_fib_vis_pure.tck'
fasciculus.save2tck(out_path)

# if __name__ == '__main__':
#     fib_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                'response_dhollander/100408/result/result20vs45/Prob01_plenium_fib.tck'
#     out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                'response_dhollander/100408/result/result20vs45/Prob01_plenium_fib_vis.tck'
#     fasciculus = Fasciculus(fib_path)
#     fib = FibSelection(fasciculus)
#     se = fib.fib_plenium(-78)
#     fasciculus.set_data(se)
#     fasciculus.save2tck(out_path)