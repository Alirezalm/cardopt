class CutStoreGen(object):

    def __init__(self):
        self.cut_storage = []

    def store_cut(self, cut_num, node_num, local_sol, local_obj, local_grad):
        cut_info = {
            'cut_id': cut_num,
            'node_id': node_num,
            'x': local_sol,
            'fx': local_obj,
            'gx': local_grad
        }
        self.cut_storage.append(cut_info)
