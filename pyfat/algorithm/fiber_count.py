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
def show(lengths, x=180, y=10000, title='Length histogram', xlabel='Length', ylabel='Count'):
    plt.figure('Fiber statistics')
    plt.subplot(111)
    plt.title(title)
    plt.hist(lengths, color='burlywood')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.text(x, y, 'fiber_count=%d' % len(lengths), fontsize=10)

    # save length histogram
    # plt.legend()
    # plt.savefig('lr250_sift12_hcp_FFA_projabs-2_length_histogram.png')

    plt.show()
