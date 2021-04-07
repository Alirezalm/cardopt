from numpy import zeros, minimum, maximum
from scipy.linalg import norm

from dccp.rhadmm.rhadmm_steps import update_primary_vars


def create_prime_obj(main_obj, z, y, rho, ):
    def prime_obj(x):
        x = x.reshape(x.shape[0], 1)
        f = main_obj(x) + y.T @ (x - z) + rho / 2 * norm(x - z, 2) ** 2
        return f[0][0]

    return prime_obj


def create_prime_grad(main_grad, z, y, rho):

    def prime_grad(x):
        n = x.shape[0]
        x = x.reshape(n, 1)
        return (main_grad(x) + y + rho * (x - z)).reshape(n, )

    return prime_grad


def rhadmm(problem, bin_var, comm, mpi_class):

    rho = 70
    max_iter = 500
    n = problem.nVars
    y = zeros((n, 1))
    z = zeros((n, 1))
    z_old = zeros((n, 1))
    eps = 1e-3
    sum_reduce = zeros((n, 1))  # size must match the reduce op -- used for MPI reduction
    rank = comm.Get_rank()
    for k in range(max_iter):
        obj_func_inner = create_prime_obj(problem.problem_instance.compute_obj_at, z, y, rho)
        grad_func_inner = create_prime_grad(problem.problem_instance.compute_grad_at, z, y, rho)
        x = update_primary_vars(obj_func_inner, grad_func_inner, n)  # compute x update locally by each node

        sum_local = x + 1 / rho * y
        # reduction
        comm.Reduce([sum_local, mpi_class.DOUBLE], [sum_reduce, mpi_class.DOUBLE], op=mpi_class.SUM, root=0)
        if rank == 0:
            z_old = z
            z = 1 / problem.nNodes * sum_reduce
            z = minimum(problem.bound * bin_var, maximum(-problem.bound * bin_var, z))

        comm.Bcast(z_old, root=0)
        comm.Bcast(z, root=0)  # broadcasting the z step .. all nodes have updates z

        # print(f" iter: {k} z: {norm(z)} z_old: {norm(z_old)} rank: {rank}")
        y += rho * (x - z)  # y update

        r = norm(x - z, 2)
        s = rho ** 2 * problem.nNodes * norm(z_old - z)
        t = comm.reduce(r, op=mpi_class.SUM, root=0)
        t = comm.bcast(t, root=0)
        # if rank == 0:
        #     print(f" k:{k} t: {t} s: {s} rank: {rank}")
        if (t <= eps) & (s <= eps / 2):
            # print(f'done: {rank}')
            return z, problem.problem_instance.compute_obj_at(z)[0][0], problem.problem_instance.compute_grad_at(z)

    return z,
