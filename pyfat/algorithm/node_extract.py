# !/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
import nibabel.streamlines.tck as nibtck
import nibabel.streamlines.array_sequence as nibAS

def xmin_extract(streams):
    '''
    extract node according to x_min
    :param streams: streamlines img
    :return: extracted node
    '''
    Ls_temp = []

    if isinstance(streams, nibtck.TckFile):
        for i in range(len(streams.streamlines)):
            # l = []
            # for j in range(len(streams.streamlines[i])):
            #     l.append(streams.streamlines[i][j][0])
            l = streams.streamlines[i][:, 0]
            for k in range(len(l) - 1):
                if l[k] * l[k + 1] < 0:
                    if np.abs(l[k]) < np.abs(l[k + 1]):
                        Ls_temp.append(streams.streamlines[i][k])
                    else:
                        Ls_temp.append(streams.streamlines[i][k + 1])

                elif l[k] == 0:
                    Ls_temp.append(streams.streamlines[i][k])

    if isinstance(streams, nibAS.ArraySequence):
        for i in range(len(streams)):
            # l = []
            # for j in range(len(streams[i])):
            #     l.append(streams[i][j][0])
            l = streams[i][:, 0]
            for k in range(len(l) - 1):
                if l[k] * l[k + 1] < 0:
                    if np.abs(l[k]) < np.abs(l[k + 1]):
                        Ls_temp.append(streams[i][k])
                    else:
                        Ls_temp.append(streams[i][k + 1])

                elif l[k] == 0:
                    Ls_temp.append(streams[i][k])

    return Ls_temp
