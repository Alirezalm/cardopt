"""
Main loop of the DIPOA Algorithm
"""
from numpy import zeros, ones

from dccp.diopa.cut_store_gen import CutStoreGen
from dccp.rhadmm.rhadmm import rhadmm


def dipoa(problem_instance, comm, mpi_class):
    rank = comm.Get_rank()
    size = comm.Get_size()
    max_iter = 1
    n = problem_instance.nVars
    binvar = ones((problem_instance.nVars, 1))  # initial binary

    cut_manager = CutStoreGen()

    rcv_x = None  # related to MPI gather
    rcv_fx = None
    rcv_gx = None
    for k in range(max_iter):
        x, fx, gx = rhadmm(problem_instance, bin_var=binvar, comm=comm, mpi_class=mpi_class)  # solves primal problem
        if rank == 0:
            rcv_x = zeros((size, n))

        comm.Gatherv([x, mpi_class.DOUBLE], rcv_x, root=0)
        if rank == 0:
            rcv_x = rcv_x.T




    return x
