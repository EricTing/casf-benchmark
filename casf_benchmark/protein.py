from Bio.PDB import PDBParser, PDBIO


def selectChain(ifn, ofn, chainID='A'):
    parser = PDBParser()
    structure = parser.get_structure('x', ifn)

    class ChainSelector():
        def __init__(self, chainID=chainID):
            self.chainID = chainID

        def accept_chain(self, chain):
            if chain.get_id() == self.chainID:
                return 1
            return 0

        def accept_model(self, model):
            return 1

        def accept_residue(self, residue):
            return 1

        def accept_atom(self, atom):
            return 1

    sel = ChainSelector(chainID)
    io = PDBIO()
    io.set_structure(structure)
    io.save(ofn, sel)
