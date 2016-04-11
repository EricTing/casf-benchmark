from os import path, makedirs

DAT = "/work/jaydy/dat/website-core-set/"
DOMAIN_DAT = "/work/jaydy/dat/dom"
VINA_INPUT = "/work/jaydy/dat/website-core-set/input"


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


class VinaPath:
    def __init__(self, id):
        "Paths for the inputs and outputs benchmarking CASF using Vina"
        self.id = id
        self.lig_pdbqt = path.join(VINA_INPUT, 'ligand-pdbqt', self.id[:4] + "_ligand.pdbqt")
        self.lig_sdf = path.join(VINA_INPUT, 'ligand-sdf',
                                 self.id[:4] + "_ligand.sdf")
