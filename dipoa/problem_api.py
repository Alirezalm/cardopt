import json

from dccp.problem.problem import Problem


class ProblemAPI(object):

    def __init__(self, problem_data):
        self.problem_data = problem_data
        self.problem_instance = None

    def create_instance_run(self):
        problem = Problem(self.problem_data).create_random_problem_instance()
        problem.solve()


if __name__ == '__main__':
    with open('config.json') as jsonfile:
        problem_data = json.load(jsonfile)
    print(problem_data)
    problem_handler = ProblemAPI(problem_data)
    problem_handler.create_instance_run()


