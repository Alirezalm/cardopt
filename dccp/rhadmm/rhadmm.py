from numpy import zeros
from scipy.linalg import norm

from dccp.rhadmm.rhadmm_steps import update_primary_vars


def create_prime_obj(main_obj, z, y, rho, ):
    def prime_obj(x):
        x = x.reshape(x.shape[0], 1)
        f = main_obj(x) + y.T @ (x - z) + rho / 2 * norm(x - z, 2) ** 2
        return f[0][0]

    return prime_obj


def rhadmm(obj, obj_grad, obj_hess, bin_var, comm, nvars, nzeros, nnodes, mpi_class, consts=None):
    rho = 1
    max_iter = 100
    n = nvars
    y = zeros((n, 1))
    z = zeros((n, 1))
    sum_reduce = zeros((n, 1))  # size must match the reduce op -- used for MPI reduction
    rank = comm.Get_rank()
    for k in range(max_iter):
        obj_func_inner = create_prime_obj(obj, z, y, rho)
        x = update_primary_vars(obj_func_inner, nvars)  # compute x update locally by each node
        sum_local = x + 1 / rho * y
        # reduction
        comm.Reduce([sum_local, mpi_class.DOUBLE], [sum_reduce, mpi_class.DOUBLE], op=mpi_class.SUM, root=0)
        if rank == 0:
            z = 1 / nnodes * sum_reduce
        comm.Bcast(z, root=0)  # broadcasting the z step .. all nodes have updates z

        y += rho * (x - z)  # y update

        if rank == 0:
            print('error', norm(x - z))
    return 1
