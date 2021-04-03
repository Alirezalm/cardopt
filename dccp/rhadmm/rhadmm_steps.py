from scipy.optimize import minimize


def update_primary_vars(rhadmm_obj, initial_condition):
    return minimize(rhadmm_obj, initial_condition)
