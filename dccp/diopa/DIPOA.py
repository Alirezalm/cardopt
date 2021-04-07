"""
Main loop of the DIPOA Algorithm
"""
from numpy import zeros, ones

from dccp.diopa.cut_store_gen import CutStoreGen
from dccp.masters.master_problem import solve_master
from dccp.rhadmm.rhadmm import rhadmm


def dipoa(problem_instance, comm, mpi_class):
    rank = comm.Get_rank()
    size = comm.Get_size()
    max_iter = 2
    n = problem_instance.nVars
    binvar = ones((problem_instance.nVars, 1))  # initial binary

    cut_manager = CutStoreGen()

    rcv_x = None  # related to MPI gather
    rcv_gx = None

    upper_bound = 1e8
    lower_bound = -upper_bound
    for k in range(max_iter):
        x, fx, gx = rhadmm(problem_instance, bin_var = binvar, comm = comm,
                           mpi_class = mpi_class)  # solves primal problem
        upper_bound = comm.reduce(fx, op = mpi_class.SUM, root = 0)
        if rank == 0:
            rcv_x = zeros((size, n))
            rcv_gx = zeros((size, n))

        rcv_fx = comm.gather(fx, root = 0)
        comm.Gather([x, mpi_class.DOUBLE], rcv_x, root = 0)
        comm.Gather([gx, mpi_class.DOUBLE], rcv_gx, root = 0)

        if rank == 0:
            for node in range(size):
                cut_manager.store_cut(k, node, rcv_x[node, :].reshape(n, 1), rcv_fx[node],
                                      rcv_gx[node, :].reshape(n, 1))

            lower_bound, binvar = solve_master(problem_instance, cut_manager)
        print(f"lb: {lower_bound}, ub:{upper_bound}")
    return x
