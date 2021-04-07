import gurobipy as gp
from gurobipy import GRB


def solve_master(problem_instance, cut_storage):
    model = gp.Model('master')

    # defining variables
    alpha = model.addMVar((problem_instance.nNodes, 1))
    x = model.addMVar((problem_instance.nVars, 1))
    z = model.addMVar((problem_instance.nVars, 1))
    delta = model.addMVar((problem_instance.nVars, 1))

