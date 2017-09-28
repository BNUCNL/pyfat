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
            for j in range(len(imgtck.streamlines[i]) - 1):
                if imgtck.streamlines[i][j][0] * imgtck.streamlines[i][j + 1][0] < 0:
                    if (j - 20) in range(len(imgtck.streamlines[i])) \
                            and (j + 20) in range(len(imgtck.streamlines[i])) \
                            and imgtck.streamlines[i][j - 20][0] * imgtck.streamlines[i][j + 20][0] < 0:
                        L_temp_need.append(imgtck.streamlines[i])
                    else:
                        L_temp_n.append(imgtck.streamlines[i])
                elif imgtck.streamlines[i][j][0] == 0:
                    if (j - 20) in range(len(imgtck.streamlines[i])) \
                            and (j + 20) in range(len(imgtck.streamlines[i])) \
                            and imgtck.streamlines[i][j - 20][0] * imgtck.streamlines[i][j + 20][0] < 0:
                        L_temp_need.append(imgtck.streamlines[i])
                    else:
                        L_temp_n.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            for j in range(len(imgtck[i]) - 1):
                if imgtck[i][j][0] * imgtck[i][j + 1][0] < 0:
                    if (j - 20) in range(len(imgtck[i])) \
                            and (j + 20) in range(len(imgtck[i])) \
                            and imgtck[i][j - 20][0] * imgtck[i][j + 20][0] < 0:
                        L_temp_need.append(imgtck[i])
                    else:
                        L_temp_n.append(imgtck[i])
                elif imgtck[i][j][0] == 0:
                    if (j - 20) in range(len(imgtck[i])) \
                            and (j + 20) in range(len(imgtck[i])) \
                            and imgtck[i][j - 20][0] * imgtck[i][j + 20][0] < 0:
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
            if 0.4 < len(imgtck.streamlines[i][:, 0][imgtck.streamlines[i][:, 0] <= 0]) / \
                    len(imgtck.streamlines[i][:, 0][imgtck.streamlines[i][:, 0] >= 0]) < 2.5:
                L_temp_need.append(imgtck.streamlines[i])
            else:
                L_temp_n.append(imgtck.streamlines[i])

    if isinstance(imgtck, nibAS.ArraySequence):
        for i in range(len(imgtck)):
            if 0.4 < len(imgtck[i][:, 0][imgtck[i][:, 0] <= 0]) / \
                    len(imgtck[i][:, 0][imgtck[i][:, 0] >= 0]) < 2.5:
                L_temp_need.append(imgtck[i])
            else:
                L_temp_n.append(imgtck[i])

    return L_temp_need, L_temp_n

def xyz_gradient(imgtck):
    '''
    extract fiber
    :param streamlines:input wholeBrain fiber
    :return: ALS: extract AP LR SI orientation fiber
    '''
    AP = nibAS.ArraySequence()
    LR = nibAS.ArraySequence()
    SI = nibAS.ArraySequence()
    ALS = [AP, LR, SI]

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

    return ALS


if __name__ == '__main__':
    from pyfat.io.load import load_tck
    from pyfat.io.save import save_tck
    # load data
    file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/Diffusion/100k_sift_1M45006_dynamic250.tck'
    imgtck = load_tck(file)


    # extract CC
    L_temp_need0 = extract_cc(imgtck)
    L_temp_need1 = extract_multi_node(L_temp_need0)[0]
    L_temp_need2 = xyz_gradient(L_temp_need1)[0]
    # L_temp_need2 = lr_number_cc(L_temp_need1)[0]
    # L_temp_need2 = extract_cc_step(L_temp_need1)[0]
    # print L_temp

    # none cc
    L_temp_n1 = extract_multi_node(L_temp_need0)[1]
    L_temp_n2 = xyz_gradient(L_temp_need0)[1]
    L_temp_n3 = xyz_gradient(L_temp_need1)[1]
    # L_temp_n2 = lr_number_cc(L_temp_need0)[1]
    # L_temp_n3 = lr_number_cc(L_temp_need1)[1]
    # L_temp_n2 = extract_cc_step(L_temp_need0)[1]
    # L_temp_n3 = extract_cc_step(L_temp_need1)[1]

    # save data

    out_path = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_lr_term_step1.tck'
    save_tck(L_temp_need0, imgtck.header, imgtck.tractogram.data_per_streamline,
         imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path)
    out_path1 = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_only_node_step2.tck'
    save_tck(L_temp_need1, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path1)
    out_path2 = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_xyz_gradient_step3.tck'
    save_tck(L_temp_need2, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path2)
    out_path3 = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_multi_node_step1.tck'
    save_tck(L_temp_n1, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path3)
    out_path4 = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_xyz_gradient_not_step2.tck'
    save_tck(L_temp_n2, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path4)
    out_path5 = '/home/brain/workingdir/data/dwi/hcp/' \
               'preprocessed/response_dhollander/100206/result_pipeline/fib_only_node_xyz_gradient_not_step3.tck'
    save_tck(L_temp_n3, imgtck.header, imgtck.tractogram.data_per_streamline,
             imgtck.tractogram.data_per_point, imgtck.tractogram.affine_to_rasmm, out_path5)
