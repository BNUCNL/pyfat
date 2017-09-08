# !/usr/bin/python
# -*- coding: utf-8 -*-


import nibabel.streamlines.tck as nibtck
from nibabel import trackvis


def load_tck(file):
    '''
    load the streamlines data (.tck)
    :param file: data path
    :return:streamlines
    '''
    imgtck = nibtck.TckFile.load(file)
    return imgtck

def load_trk(file):
    '''
    load the streamlines data (.trk)
    :param file: data path
    :return:streamlines
    '''
    streams, hdr = trackvis.read(file, points_space="rasmm")
    # streamlines = [s[0] for s in streams]
    return streams, hdr


if __name__ == '__main__':
    file = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/100206/result/CC_fib.tck'
    img_cc = load_tck(file)
    print img_cc.streamlines
