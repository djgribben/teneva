"""Package teneva, module core.stat: helper functions for processing statistics.

This module contains the helper functions for processing statistics, including
computation of the CDF function and its confidence bounds, as well as sampling
from the TT-tensor.

"""
import numpy as np
import teneva


def cdf_confidence(x, alpha=0.05):
    """Construct a Dvoretzky-Kiefer-Wolfowitz confidence band for the CDF.

    Args:
        x (np.ndarray): the empirical distribution in the form of 1D np.ndarray
            of length "m".
        alpha (float): "alpha" for the "(1 - alpha)" confidence band.

    Returns:
        [np.ndarray, np.ndarray]: CDF lower and upper bounds in the form of 1D
        np.ndarray of the length "m".

    """
    eps = np.sqrt(np.log(2. / alpha) / (2 * len(x)))
    return np.clip(x - eps, 0, 1), np.clip(x + eps, 0, 1)


def cdf_getter(x):
    """Build the getter for CDF.

    Args:
        x (list or np.ndarray): one-dimensional points.

    Returns:
        function: the function that computes CDF values. Its input may be one
        point (float) or a set of points (1D np.ndarray). The output
        (corresponding CDF value/values) will have the same type.

    """
    x = np.array(x, copy=True)
    x.sort()
    y = np.linspace(1./len(x), 1, len(x))

    x = np.r_[-np.inf, x]
    y = np.r_[0, y]

    def cdf(z):
        return y[np.searchsorted(x, z, 'right') - 1]

    return cdf



def _extend_core(G, n):
    r1, nold, r2 = G.shape
    Gn = np.empty([r1, n, r2])
    for i1 in range(r1):
        for i2 in range(r2):
            Gn[i1, :, i2] = np.interp(np.arange(n)*(nold - 1)/(n - 1), range(nold), G[i1, :, i2])

    return Gn



def sample_ind_rand(Y, m, unique=True, m_fact=5, max_rep=100):
    """Sample random multi-indices according to given probability TT-tensor.

    Args:
        Y (list): TT-tensor, which represents the discrete probability
            distribution.
        m (int, float): number of samples.
        unique (bool): if True, then unique multi-indices will be generated.

    Returns:
        np.ndarray: generated multi-indices for the tensor in the form
        of array of the shape [m, d], where "d" is the dimension of the tensor.

    Note:
        In the case "unique = True", the number of returned multi-indices may
        be less than requested.

    """
    d = len(Y)
    Z, p = teneva.orthogonalize(Y, 0, use_stab=True)

    G = Z[0]
    r1, n, r2 = G.shape

    if float_cf is not None:
        n, nold = n*float_cf, n
        G = _extend_core(G, n)


    Q = G.reshape(n, r2)

    Q, I1 = _sample_core_first(Q, teneva._range(n), m_fact*m if unique else m)
    I = np.empty([I1.shape[0], d])
    I[:, 0] = I1[:, 0]

    for di, G in enumerate(Z[1:], start=1):
        r1, n, r2 = G.shape
        if float_cf is not None:
            n, nold = n*float_cf, n
            G = _extend_core(G, n)

        Qtens = np.einsum('kr,riq->kiq', Q, G, optimize='optimal')
        Q = np.empty([Q.shape[0], r2])

        for im, qm, qnew in zip(I, Qtens, Q):
            norms = np.sum(qm**2, axis=1)
            norms /= norms.sum()

            i_cur = im[di] = np.random.choice(n, size=1, p=norms)
            qnew[:] = qm[i_cur]


    if unique:

        I = np.unique(I, axis=0)
        if I.shape[0] < m:
            # print(f"need more!!! m={m}, shape={I.shape[0]}, {m_fact=}, {max_rep=}")
            if max_rep < 0 or m_fact > 1000000:
                raise ValueError('Can not generate the required number of samples')
            return sample_ind_rand(Y, m, True, 2*m_fact, max_rep - 1, float_cf=float_cf)


        else:
            np.random.shuffle(I)

    I = I[:m]

    if I.shape[0] != m:
        raise ValueError('Can not generate the required number of samples')

    if float_cf is not None:
        I = I / float_cf

    return I


def _sample_core_first(Q, I, m, thr_n=10):
    n = Q.shape[0]

    norms = np.sum(Q**2, axis=1)
    norms /= norms.sum()

    ind = np.random.choice(n, size=m, p=norms, replace=True)

    return Q[ind, :], I[ind, :]

