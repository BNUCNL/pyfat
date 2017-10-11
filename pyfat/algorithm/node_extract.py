# !/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import nibabel.streamlines.tck as nibtck
import nibabel.streamlines.array_sequence as nibas

def xmin_extract(streams):
    """
    extract node according to x_min
    :param streams: streamlines img
    :return: extracted node
    """
    Ls_temp = nibas.ArraySequence()

    if isinstance(streams, nibtck.TckFile):

        for i in range(len(streams.streamlines)):
            l = streams.streamlines[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            index0 = np.argwhere(x_stemp_index <= 0)
            index_term = np.argmin((abs(streams.streamlines[i][index0[0]][0]),
                                    abs(streams.streamlines[i][index0[0]+1][0])))
            index = index0[0] + index_term
            Ls_temp.append(streams.streamlines[i][index][0])

    if isinstance(streams, nibas.ArraySequence):
        for i in range(len(streams)):
            l = streams[i][:, 0]
            l_ahead = list(l[:])
            a = l_ahead.pop(0)
            l_ahead.append(a)
            x_stemp = np.array([l, l_ahead])
            x_stemp_index = x_stemp.prod(axis=0)
            index0 = np.argwhere(x_stemp_index <= 0)
            index_term = np.argmin((abs(streams[i][index0[0]][0]),
                                    abs(streams[i][index0[0] + 1][0])))
            index = index0[0] + index_term
            Ls_temp.append(streams[i][index][0])

    return Ls_temp
