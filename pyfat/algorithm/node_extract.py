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
    Ls_temp = []

    if isinstance(streams, nibtck.TckFile):
        for i in range(len(streams.streamlines)):
            index = np.argmin(abs(streams.streamlines[i][:, 0]))
            Ls_temp.append(streams.streamlines[i][index])

            # l = streams.streamlines[i][:, 0]
            # for k in range(len(l) - 1):
            #     if l[k] * l[k + 1] < 0:
            #         if np.abs(l[k]) < np.abs(l[k + 1]):
            #             Ls_temp.append(streams.streamlines[i][k])
            #         else:
            #             Ls_temp.append(streams.streamlines[i][k + 1])
            #
            #     elif l[k] == 0:
            #         Ls_temp.append(streams.streamlines[i][k])

    if isinstance(streams, nibas.ArraySequence):
        for i in range(len(streams)):
            index = np.argmin(abs(streams[i][:, 0]))
            Ls_temp.append(streams[i][index])

            # l = streams[i][:, 0]
            # for k in range(len(l) - 1):
            #     if l[k] * l[k + 1] < 0:
            #         if np.abs(l[k]) < np.abs(l[k + 1]):
            #             Ls_temp.append(streams[i][k])
            #         else:
            #             Ls_temp.append(streams[i][k + 1])
            #
            #     elif l[k] == 0:
            #         Ls_temp.append(streams[i][k])

    return Ls_temp
