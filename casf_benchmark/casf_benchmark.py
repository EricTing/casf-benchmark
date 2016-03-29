#!/usr/bin/env python

import os
import luigi
import paths
import LPC
import protein


class SelectChain(luigi.Task):
    tname = luigi.Parameter()

    def run(self):
        protein_pdb = paths.Path(self.tname).protein_pdb
        ofn = self.output().path
        protein.selectChain(protein_pdb, ofn, self.chainID)

    def consensusChainID(self):
        protein_pdb = paths.Path(self.tname).protein_pdb
        ligand_sdf = paths.Path(self.tname).ligand_sdf
        lpc_job = LPC.LPC(ligand_sdf, protein_pdb)
        lpc_result = lpc_job.runLPC()
        chainID = LPC.LPCParser(lpc_result).consensusChainID()
        self.chainID = chainID

    def output(self):
        if self.tname == '3f3a':
            self.chainID = 'A'
        elif self.tname == '3f3e':
            self.chainID = 'A'
        elif self.tname == '3muz':
            self.chainID = '1'
        elif self.tname == '1a30':
            self.chainID = 'A'
        else:
            protein_pdb = paths.Path(self.tname).protein_pdb
            chain_id = protein.isSingleChain(protein_pdb)
            if chain_id is None:
                self.consensusChainID()
            else:
                self.chainID = chain_id

        path = os.path.join(
            paths.Path(self.tname).work_dir,
            "%s_%s.pdb" % (self.tname, self.chainID))
        return luigi.LocalTarget(path)


if __name__ == '__main__':
    import sys
    tname = sys.argv[1]
    luigi.build([SelectChain(tname)], local_scheduler=True)
