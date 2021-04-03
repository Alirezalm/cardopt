from numpy.random import randn
from scipy.optimize import minimize


def update_primary_vars(rhadmm_obj, n_vars):

    initial_condition = randn(n_vars, )
    x = minimize(rhadmm_obj, initial_condition)['x']
    return x.reshape(n_vars, 1)
