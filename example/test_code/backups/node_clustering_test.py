# !/usr/bin/python
# -*- coding: utf-8 -*-

from pyfat.io.load import load_tck
from pyfat.algorithm.node_extract import xmin_extract
from pyfat.algorithm.node_clustering import hiera_single_clust

source_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
              'response_dhollander/100408/result/result20vs45/cc_20fib_lr1.5_new_correct_sample1000.tck'

data = load_tck(source_path)
Ls_temp = xmin_extract(data)
c = hiera_single_clust(Ls_temp)
print c
