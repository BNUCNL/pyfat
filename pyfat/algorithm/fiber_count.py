# !/usr/bin/python
# -*- coding: utf-8 -*-


from dipy.tracking.utils import length
import matplotlib.pyplot as plt

# count fiber lengths
def fib_lengths_count(stream):
    """
    compute fiber lengths
    :param stream: input streamsline
    :return: fiber length
    """
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
