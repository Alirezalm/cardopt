from dccp.problem.problem import Problem


class ProblemAPI(object):

    def __init__(self, problem_data):
        self.problem_data = problem_data
        self.problem_instance = None

    def create_instance_run(self, comm, mpi_class, bound):
        problem = Problem(self.problem_data).create_random_problem_instance(bound)
        return problem.solve(comm, mpi_class)


