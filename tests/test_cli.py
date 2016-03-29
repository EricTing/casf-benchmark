from __future__ import print_function

from casf_benchmark import paths, LPC


def test_lpc():
    complex_id = "10gs"
    complex_path = paths.Path(complex_id).complex_pdb
    lpc_result = LPC.lpc(complex_path)
    assert lpc_result != " "
