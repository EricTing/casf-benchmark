from __future__ import print_function
from casf_benchmark import paths, LPC, protein
import unittest
import os


class TestLPC(unittest.TestCase):
    def setUp(self):
        self.protein_pdb = paths.Path("1hfs").protein_pdb
        self.ligand_sdf = paths.Path("1hfs").ligand_sdf
        lpc_job = LPC.LPC(self.ligand_sdf, self.protein_pdb)
        self.lpc_result = lpc_job.runLPC()
        self.lpc_parser = LPC.LPCParser(self.lpc_result)

    def test_run(self):
        contacts = self.lpc_parser.readContacts()
        self.assertEqual(32, len(contacts))
        self.assertEqual('A', self.lpc_parser.consensusChainID())


class TestSelectChain(unittest.TestCase):
    def setUp(self):
        self.protein_path = paths.Path("1hfs").protein_pdb

    def test_select(self):
        os.chdir(os.path.dirname(__file__))
        ofn = "./1hfs_A.pdb"
        protein.selectChain(self.protein_path, ofn, chainID='A')


if __name__ == '__main__':
    unittest.main()
