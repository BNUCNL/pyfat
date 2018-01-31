# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from pyfat.io.load import load_tck, load_trk
from pyfat.viz.visualization import show
from pyfat.core.dataobject import Fasciculus

# tck
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_lh_occipital8.tck'
fas = Fasciculus(tck_path)
lengths = fas.get_lengths()
show(lengths)

R = fas.get_lr_ratio()
show(R, title='Rat histogram', xlabel='Rat')
