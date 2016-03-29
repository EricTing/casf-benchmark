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


def isSingleChain(ifn):
    """return the chain id if one pdb file contains only one chain,
    else return None
    """
    parser = PDBParser()
    structure = parser.get_structure('x', ifn)
    chains = []
    for chain in structure.get_chains():
        chains.append(chain.id)

    chains = [c for c in chains if c != ' ']
    print(chains)
    if len(chains) == 1:
        return chains[0]
    else:
        return None
