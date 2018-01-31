# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import nibabel.streamlines.array_sequence as nibas

from pyfat.algorithm.metric import Metric
from pyfat.io.load import load_tck
from pyfat.io.save import save_tck
from pyfat.algorithm.fiber_count import show

# load data
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
       'response_dhollander/100408/result/result20vs45/cc_20fib_step20_new_sample5000.tck'
imgtck = load_tck(tck_path)
streamlines = imgtck.streamlines
print type(streamlines)
print len(streamlines)
img = Metric(streamlines)
# print img.lengths
lengths = img.length()
print lengths.min()
set_min_fib = img.set_length_min(30)
min_l = set_min_fib.lengths_min
print min_l
print len(set_min_fib.streamlines)

# print set_min_fib.streamlines
# for i in set_min_fib.streamlines:
#        streamlines.append(i)
# print len(streamlines)
merge = img.fib_merge(set_min_fib.streamlines)
print len(merge.streamlines)
