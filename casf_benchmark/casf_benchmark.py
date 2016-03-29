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
        complex_path = paths.Path(self.tname).complex_pdb
        lpc_result = LPC.lpc(complex_path)
        chainID = LPC.LPCParser(lpc_result).consensusChainID()
        self.chainID = chainID

    def output(self):
        self.consensusChainID()
        path = os.path.join(
            paths.Path(self.tname).work_dir,
            "%s_%s.pdb" % (self.tname, self.chainID))
        return luigi.LocalTarget(path)


if __name__ == '__main__':
    import sys
    tname = sys.argv[1]
    luigi.build([SelectChain(tname)], local_scheduler=True)
