from __future__ import print_function
import unittest
from casf_benchmark import paths, LPC, protein


class TestLPC(unittest.TestCase):
    def setUp(self):
        self.complex_path = paths.Path("10gs").complex_pdb
        self.lpc_result = LPC.lpc(self.complex_path)
        self.lpc_parser = LPC.LPCParser(self.lpc_result)

    def test_run(self):
        contacts = self.lpc_parser.readContacts()
        self.assertEqual(21, len(contacts))
        self.assertEqual('A', self.lpc_parser.consensusChainID())


class TestSelectChain(unittest.TestCase):
    def setUp(self):
        self.protein_path = paths.Path("10gs").protein_pdb

    def test_select(self):
        ofn = "./10gs_A.pdb"
        protein.selectChain(self.protein_path, ofn, chainID='A')


if __name__ == '__main__':
    unittest.main()
