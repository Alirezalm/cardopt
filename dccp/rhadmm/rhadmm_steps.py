from numpy import zeros
from numpy.random import randn
from scipy.optimize import minimize


def update_primary_vars(rhadmm_obj, rhadmm_grad, n_vars):
    initial_condition = zeros((n_vars,))
    x = minimize(rhadmm_obj, jac=rhadmm_grad, x0=initial_condition, method='cg', options={'gtol': 1e-3})['x']
    return x.reshape(n_vars, 1)
