import gurobipy as gp
from gurobipy import GRB
from numpy import ones


def solve_master(problem_instance, cut_manager):
    model = gp.Model('master')

    n = problem_instance.nVars
    N = problem_instance.nNodes
    M = problem_instance.bound
    kappa = problem_instance.nZeros
    total_cuts = len(cut_manager.cut_storage)

    # defining variables
    alpha = model.addMVar(shape = N)
    x = model.addMVar(shape = n)
    delta = model.addMVar(shape = n, vtype = GRB.BINARY)

    obj = ones((problem_instance.nNodes, 1)).T @ alpha
    model.setObjective(obj, GRB.MINIMIZE)

    # introducing linear cuts
    i = 0
    for cut in cut_manager.cut_storage:
        if i == N - 1:
            i = 0
        else:
            i += 1
        model.addConstr(alpha[i] >= cut['fx'] + cut['gx'].T @ x - cut['gx'].T @ cut['x'], name = f"cut['cut_id']")

    for i in range(n):
        model.addConstr(x[i] <= M * delta[i], name = f'b1{i}')
        model.addConstr(-M * delta[i] <= x[i], name = f'b2{i}')

    model.addConstr(delta.sum() <= kappa, name = 'd')
    model.setParam('OutputFlag', 0)
    model.optimize()

    return model.objval, delta.x.reshape(n,1),
