# !/usr/bin/python
# -*- coding: utf-8 -*-


from dipy.tracking.utils import length
import matplotlib.pyplot as plt

# count fiber lengths
def fib_lengths_count(stream):
    lengths = length(stream)
    return lengths

# show
def show(lengths):
    plt.figure('Fiber statistics')
    plt.subplot(111)
    plt.title('Length histogram')
    plt.hist(lengths, color='burlywood')
    plt.xlabel('Length')
    plt.ylabel('Count')

    # save length histogram
    # plt.legend()
    # plt.savefig('lr250_sift12_hcp_FFA_projabs-2_length_histogram.png')

    plt.show()


if __name__ == '__main__':
    from pyfat.io.load import load_tck, load_trk
    # tck
    fname_tck = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/lr250_sift12_hcp_FFA_projabs-2.tck'
    imgtck = load_tck(fname_tck)
    stream = imgtck.streamlines
    lengths = list(fib_lengths_count(stream))
    show(lengths)
    # trk
    fname_trk = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                'response_dhollander/lr250_sift12_hcp_FFA_projabs-2.trk'
    imgtrk, hdr = load_trk(fname_trk)
    stream = [s[0] for s in imgtrk]
    lengths = list(fib_lengths_count(stream))
    show(lengths)
