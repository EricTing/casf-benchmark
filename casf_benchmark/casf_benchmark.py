#!/usr/bin/env python

import os
import glob
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


class SelectDomainChain(luigi.Task):
    def find(self, tname):
        myid = tname[:4]
        lig_sdf = paths.Path(myid).ligand_sdf
        domain = paths.Domain(tname)
        pdbs = glob.glob(os.path.join(domain.dat_dir, "*.pdb"))

        mx_cnts = -1
        mx_pdb = ""
        for pdb in pdbs:
            lpc_job = LPC.LPC(lig_sdf, pdb)
            result = lpc_job.runLPC()
            parser = LPC.LPCParser(result)
            num_contacts = len(parser.readContacts())
            if num_contacts > mx_cnts:
                mx_cnts = num_contacts
                mx_pdb = pdb

        return mx_pdb

    def run(self):
        for tname in [_.rstrip() for _ in file("../dat/domains.txt")]:
            mx_pdb = self.find(tname)
            print(mx_pdb)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tname = sys.argv[1]
        luigi.build([SelectChain(tname), ], local_scheduler=True)
    else:
        luigi.build([SelectDomainChain()], local_scheduler=True)
