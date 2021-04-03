import json

from mpi4py import MPI

from dipoa.problem_api import ProblemAPI

# entry point of the algorithm, runs in parallel
with open('config.json') as jsonfile:
    data = json.load(jsonfile)

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

print(data, f"from node {rank}")

problem_handler = ProblemAPI(data)
problem_handler.create_instance_run(comm, mpi_class=MPI)
