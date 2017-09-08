# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
from scipy import rand
from scipy.sparse import csc_matrix, spdiags
from scipy.sparse.linalg import eigsh
from scipy.linalg import norm, svd, LinAlgError


# exception hander for singular value decomposition
class SVDError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# (eigen_val, eigen_vec) = ncut(W, nbEigenValues)
# The first step of normalized cut spectral clustering
def ncut(W, nbEigenValues):
    # parameters
    offset = .5
    maxiterations = 100
    eigsErrorTolerence = 1e-6
    eps = 2.2204e-16

    m = W.shape[1]

    # make sure that W is symmetric
    if (W-W.transpose()).sum() != 0:
       print "W should be symmetric!"
       exit(0)

    # degrees and regularization
    d = np.abs(W).sum(0)
    dr = 0.5*(d-W.sum(0))
    d = d + offset * 2
    dr = dr + offset

    # calculation of the normalized LaPlacian
    W = W + spdiags(dr, [0], m, m, "csc")
    Dinvsqrt = spdiags((1.0/np.sqrt(d+eps)), [0], m, m, "csc")
    P = Dinvsqrt * (W*Dinvsqrt)

    # perform the eigen decomposition
    eigen_val, eigen_vec = eigsh(P, nbEigenValues)
    # eigen_val, eigen_vec = eigsh(P, nbEigenValues, maxiter=maxiterations, tol=eigsErrorTolerence, which='LA')

    # sort the eigen_vals so that the first is the largest
    i = np.argsort(-eigen_val)
    eigen_val = eigen_val[i]
    eigen_vec = eigen_vec[:, i]

    # normalize the returned eigenvectors
    eigen_vec = Dinvsqrt*np.matrix(eigen_vec)
    norm_ones = norm(np.ones((m, 1)))
    for i in range(0, eigen_vec.shape[1]):
        eigen_vec[:, i] = (eigen_vec[:, i] / norm(eigen_vec[:, i]))*norm_ones
        if eigen_vec[0, i] != 0:
            eigen_vec[:, i] = -1 * eigen_vec[:, i] * np.sign(eigen_vec[0, i])

    return eigen_val, eigen_vec

# eigenvec_discrete=discretisation(eigen_vec)
# The second step of normalized cut clustering
def discretisation(eigen_vec):
    eps = 2.2204e-16

    # normalize the eigenvectors
    [n, k] = eigen_vec.shape
    vm = np.kron(np.ones((1, k)), np.sqrt(np.multiply(eigen_vec, eigen_vec).sum(1)))
    eigen_vec = np.divide(eigen_vec, vm)

    svd_restarts = 0
    exitLoop = 0

    # if there is an exception we try to randomize and rerun SVD again do this 30 times
    while (svd_restarts < 30) and (exitLoop == 0):

        # initialize algorithm with a random ordering of eigenvectors
        c = np.zeros((n, 1))
        R = np.matrix(np.zeros((k, k)))
        R[:, 0] = eigen_vec[int(rand(1)*(n-1)), :].transpose()

        for j in range(1, k):
            c = c+np.abs(eigen_vec*R[:, j-1])
            R[:, j] = eigen_vec[c.argmin(), :].transpose()


        lastObjectiveValue = 0
        nbIterationsDiscretisation = 0
        nbIterationsDiscretisationMax = 20

        # iteratively rotate the discretised eigenvectors until they
        # are maximally similar to the input eignevectors, this
        # converges when the differences between the current solution
        # and the previous solution differs by less than eps or we
        # we have reached the maximum number of itarations
        while exitLoop == 0:
            nbIterationsDiscretisation = nbIterationsDiscretisation + 1

            # rotate the original eigen_vectors
            tDiscrete = eigen_vec * R

            # discretise the result by setting the max of each row=1 and
            # other values to 0
            j = np.reshape(np.asarray(tDiscrete.argmax(1)), n)
            eigenvec_discrete = csc_matrix((np.ones(len(j)), (range(0, n),
                                                              np.array(j))), shape=(n, k))

            # calculate a rotation to bring the discrete eigenvectors cluster to
            # the original eigenvectors
            tSVD=eigenvec_discrete.transpose()*eigen_vec
            # catch a SVD convergence error and restart
            try:
                U, S, Vh = svd(tSVD)
            except LinAlgError:
                # catch exception and go back to the beginning of the loop
                print >> sys.stderr, \
                    "SVD did not converge, randomizing and trying again"
                break

            # test for convergence
            NcutValue = 2*(n-S.sum())
            if((np.abs(NcutValue-lastObjectiveValue) < eps) or
                   (nbIterationsDiscretisation >
                        nbIterationsDiscretisationMax)):
                exitLoop = 1
            else:
                # otherwise calculate rotation and continue
                lastObjectiveValue = NcutValue
                R = np.matrix(Vh).transpose()*np.matrix(U).transpose()

    if exitLoop == 0:
        raise SVDError("SVD did not converge after 30 retries")
    else:
        return eigenvec_discrete

def get_labels(eigenvec_discrete):
    '''
    get the label numbers--author:Taicheng Huang
    :param eigenvec_discrete:discrete eigenvec
    :return:labels
    '''
    eigenvec_discrete = eigenvec_discrete.todense()
    eigenvec_discrete = np.array(eigenvec_discrete)
    labels = np.argmax(eigenvec_discrete, axis=1)
    return labels
