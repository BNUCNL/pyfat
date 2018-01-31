# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from nibabel import gifti


l_label = gifti.read('fsaverage.label.R.164k_fsavg_R.label.gii')
data = np.array(l_label.darrays[0].data)
data.shape = (data.shape[0], 1, 1)
mgzl = nib.load('rh.orig.avg.area.mgh')
header = mgzl.header
mgz = nib.MGHImage(data, None, header)
nib.save(mgz, 'rh_label.mgz')
