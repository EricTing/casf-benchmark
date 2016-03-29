from os import path

DAT = "/work/jaydy/dat/website-core-set/"


class Path:
    def __init__(self, id):
        self.id = id
        self.dat_dir = path.join(DAT, self.id)
        self.complex_pdb = path.join(self.dat_dir, self.id + "_complex.pdb")
        self.protein_pdb = path.join(self.dat_dir, self.id + "_protein.pdb")
