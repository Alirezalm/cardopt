class Problem(object):
    def __init__(self, problem_data: dict):

        self.name = problem_data['name']
        self.nVars = problem_data['nVars']
        self.nSamples = problem_data['nSamples']
        self.nZeros = problem_data['nZeros']
        self.compareTo = problem_data['compareTo']
        self.nNodes = problem_data['nNodes']

    # def _dslr_obj_create(self, local_dataset, local_response):



