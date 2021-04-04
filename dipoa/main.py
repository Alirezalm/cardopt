import json

from django.http import JsonResponse
from mpi4py import MPI

from dipoa.problem_api import ProblemAPI

# entry point of the algorithm, runs in parallel
with open('config.json') as jsonfile:
    data = json.load(jsonfile)

comm = MPI.COMM_WORLD

rank = comm.Get_rank()

print(data, f"from node {rank}")

problem_handler = ProblemAPI(data)

x = problem_handler.create_instance_run(comm, MPI, 0.1)
x = [item[0] for item in x]
if rank == 0:
    ans = {
        'sol': x
    }

    with open('solution.json', 'w') as jsonfile:
        json.dump(ans, jsonfile)
