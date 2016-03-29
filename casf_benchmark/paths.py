from os import path, makedirs

DAT = "/work/jaydy/dat/website-core-set/"
DOMAIN_DAT = "/work/jaydy/dat/dom"


class Path:
    def __init__(self, id):
        self.id = id
        self.dat_dir = path.join(DAT, self.id)
        self.complex_pdb = path.join(self.dat_dir, self.id + "_complex.pdb")
        self.protein_pdb = path.join(self.dat_dir, self.id + "_protein.pdb")
        self.ligand_sdf = path.join(self.dat_dir, self.id + "_ligand.sdf")
        self.work_dir = path.join("/work/jaydy/working/casf_benchmark",
                                  self.id)

        try:
            makedirs(self.work_dir)
        except:
            pass


class Domain:
    def __init__(self, id):
        self.id = id
        self.dat_dir = path.join(DOMAIN_DAT, self.id)
