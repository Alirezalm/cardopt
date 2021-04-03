from numpy.random import randn

from dccp.problem.problem_classes import LogRegProb
from dccp.rhadmm.rhadmm import rhadmm

PROBLEM_CLASS = {
    'dslr': 'distributed sparse logistic regression',
    'dspo': 'distributed sparse portfolio optimization',
}


class Problem(object):
    def __init__(self, problem_data: dict):
        self.name = problem_data['name']
        self.nVars = int(problem_data['nVars'])
        self.nSamples = int(problem_data['nSamples'])
        self.nZeros = int(problem_data['nZeros'])
        self.compareTo = problem_data['compareTo']
        self.nNodes = int(problem_data['nNodes'])
        self.problem_instance = None

    def create_random_problem_instance(self):
        if self.name == PROBLEM_CLASS['dslr']:
            dataset = randn(self.nSamples, self.nVars)
            response = randn(self.nSamples, 1)
            response[response >= 0.5] = 1
            response[response < 0.5] = 0
            self.problem_instance = LogRegProb(local_dataset=dataset, local_response=response)
            return self

    def solve(self, comm, mpi_class):
        binvar = randn(self.nVars, 1)
        x = rhadmm(self.problem_instance.compute_obj_at, None, None, binvar, comm, self.nVars, self.nZeros, self.nNodes,
                   mpi_class)
        return 1
