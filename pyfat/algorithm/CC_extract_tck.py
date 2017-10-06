# !/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import nibabel.streamlines.tck as nibtck
import nibabel.streamlines.array_sequence as nibAS


def extract_cc(imgtck):
    '''
    extract cc fiber
    :param streamlines:input wholeBrain fiber
    :return: ArraySequence: extract cc fiber
    '''
    L_temp = nibAS.ArraySequence()

    if isinstance(imgtck, nibtck.TckFile):
        for i in range(len(imgtck.streamlines)):
            if imgtck.streamlines[i][0][0] * imgtck.streamlines[i][-1][0] < 0:
                L_temp.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            if imgtck[i][0][0] * imgtck[i][-1][0] < 0:
                L_temp.append(imgtck[i])
    return L_temp


def extract_multi_node(imgtck):
    '''
    extract multi-nodes fiber
    :param imgtck: wholeBrain fiber
    :return: only node fiber and multi-nodes fiber
    '''
    L_temp_noly_node = nibAS.ArraySequence()
    L_temp_multi_node = nibAS.ArraySequence()

    if isinstance(imgtck, nibtck.TckFile):
        for i in range(len(imgtck.streamlines)):
            count = 0
            for j in range(len(imgtck.streamlines[i]) - 1):
                if imgtck.streamlines[i][j][0] * imgtck.streamlines[i][j + 1][0] < 0:
                    count += 1
                elif imgtck.streamlines[i][j][0] == 0:
                    count += 1
            if count == 1:
                L_temp_noly_node.append(imgtck.streamlines[i])
            else:
                L_temp_multi_node.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            count = 0
            for j in range(len(imgtck[i]) - 1):
                if imgtck[i][j][0] * imgtck[i][j + 1][0] < 0:
                    count += 1
                elif imgtck[i][j][0] == 0:
                    count += 1
            if count == 1:
                L_temp_noly_node.append(imgtck[i])
            else:
                L_temp_multi_node.append(imgtck[i])
    return L_temp_noly_node, L_temp_multi_node


def extract_cc_step(imgtck):
    '''
    extract cc fiber
    :param streamlines:input wholeBrain fiber
    :return: ArraySequence: extract cc fiber
    '''
    L_temp_need = nibAS.ArraySequence()
    L_temp_n = nibAS.ArraySequence()

    if isinstance(imgtck, nibtck.TckFile):
        for i in range(len(imgtck.streamlines)):
            index = np.argmin(abs(imgtck.streamlines[i][:, 0]))
            if (index - 20) in range(len(imgtck.streamlines[i])) \
                    and (index + 20) in range(len(imgtck.streamlines[i])):
                L_temp_need.append(imgtck.streamlines[i])
            else:
                L_temp_n.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            index = np.argmin(abs(imgtck[i][:, 0]))
            if (index - 20) in range(len(imgtck[i])) \
                    and (index + 20) in range(len(imgtck[i])):
                L_temp_need.append(imgtck[i])
            else:
                L_temp_n.append(imgtck[i])

    return L_temp_need, L_temp_n

def lr_number_cc(imgtck):
    '''
    extract fiber
    :param streamlines:input wholeBrain fiber
    :return: ArraySequence: extract fiber:the percentage of left and right hemispheres fiber points in [0.4, 2.5]
    '''
    L_temp_need = nibAS.ArraySequence()
    L_temp_n = nibAS.ArraySequence()

    if isinstance(imgtck, nibtck.TckFile):
        for i in range(len(imgtck.streamlines)):
            rat = len(imgtck.streamlines[i][:, 0][imgtck.streamlines[i][:, 0] <= 0]) / \
                  len(imgtck.streamlines[i][:, 0][imgtck.streamlines[i][:, 0] >= 0])
            if rat < 1:
                rat = 1 / rat
            if rat < 2.5:
                L_temp_need.append(imgtck.streamlines[i])
            else:
                L_temp_n.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            rat = len(imgtck[i][:, 0][imgtck[i][:, 0] <= 0]) / \
                  len(imgtck[i][:, 0][imgtck[i][:, 0] >= 0])
            if rat < 1:
                rat = 1 / rat
            if rat < 2.5:
                L_temp_need.append(imgtck[i])
            else:
                L_temp_n.append(imgtck[i])

    return L_temp_need, L_temp_n

def xyz_gradient(imgtck, n=None):
    '''
    extract fiber
    :param imgtck:input wholeBrain fiber
    :param n:lr numbers
    :return: ALS: extract AP LR SI orientation fiber
    '''
    AP = nibAS.ArraySequence()
    LR = nibAS.ArraySequence()
    SI = nibAS.ArraySequence()
    ALS = [AP, LR, SI]

    if n is None:
        if isinstance(imgtck, nibtck.TckFile):
            for i in range(len(imgtck.streamlines)):
                grad = np.gradient(imgtck.streamlines[i])
                x_grad = grad[0][:, 0].sum()
                y_grad = grad[0][:, 1].sum()
                z_grad = grad[0][:, 2].sum()

                index = np.array([y_grad, x_grad, z_grad]).argmax()
                ALS[index].append(imgtck.streamlines[i])

        if isinstance(imgtck, nibAS.ArraySequence):
            for i in range(len(imgtck)):
                grad = np.gradient(imgtck[i])
                x_grad = grad[0][:, 0].sum()
                y_grad = grad[0][:, 1].sum()
                z_grad = grad[0][:, 2].sum()

                index = np.array([y_grad, x_grad, z_grad]).argmax()
                ALS[index].append(imgtck[i])
    else:
        if isinstance(imgtck, nibtck.TckFile):
            for i in range(len(imgtck.streamlines)):
                index = np.argmin(abs(imgtck.streamlines[i][:, 0]))
                if (index - n) in range(len(imgtck.streamlines)) \
                        and (index + n) in range(len(imgtck.streamlines)):
                    grad = np.gradient(imgtck.streamlines[i][index - n:index + n, :])
                    x_grad = grad[0][:, 0].sum()
                    y_grad = grad[0][:, 1].sum()
                    z_grad = grad[0][:, 2].sum()

                    index = np.array([y_grad, x_grad, z_grad]).argmax()
                    ALS[index].append(imgtck.streamlines[i])

        if isinstance(imgtck, nibAS.ArraySequence):
            for i in range(len(imgtck)):
                index = np.argmin(abs(imgtck[i][:, 0]))
                if (index - n) in range(len(imgtck)) \
                        and (index + n) in range(len(imgtck)):
                    grad = np.gradient(imgtck[i])
                    x_grad = grad[0][:, 0].sum()
                    y_grad = grad[0][:, 1].sum()
                    z_grad = grad[0][:, 2].sum()

                    index = np.array([y_grad, x_grad, z_grad]).argmax()
                    ALS[index].append(imgtck[i])

    return ALS
