class CutStoreGen(object):

    def __init__(self):
        self.cut_storage = []

    def store_cut(self, local_sol, local_obj, local_grad):
        cut_info = {
            'x': local_sol,
            'fx': local_obj,
            'gx': local_grad
        }
        self.cut_storage.append(cut_info)
