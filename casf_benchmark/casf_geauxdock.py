#!/usr/bin/env python

from paths import VinaPath, GEAUX_OUTPUT
from dockedpose import rmsd_between  # https://gist.github.com/EricTing/4a540c8e13321954d2f3
import pandas as pd
import json
import pybel
import luigi
import os
import add_lig_atom_types


class AddTypes(luigi.Task):
    tname = luigi.Parameter()

    def run(self):
        vina_path = VinaPath(self.tname)
        lig_sdf = vina_path.lig_sdf
        add_lig_atom_types.main(lig_sdf)


def test():
    luigi.build([AddTypes("1h23A01")], local_scheduler=True)


def trace():
    """generate input for trace function
    """

    def foo(tname):
        try:
            csv_ifn = os.path.join(GEAUX_OUTPUT, tname,
                                   tname + '_native_pkt.csv')
            df = pd.read_csv(csv_ifn, sep=' ')
            cols = ["lig", "prt", "mv1", "mv2", "mv3", "mv4", "mv5", "mv6"]
            trace_ifn = os.path.join(GEAUX_OUTPUT, tname, tname + '_trace.csv')
            df[cols][:1].to_csv(trace_ifn, sep=' ', index=False)
        except Exception as e:
            print(e)

    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        foo(tname)


def eval_rmsd():
    """evaluate the geauxdock prediction using RMSD
    """

    def foo(tname):
        try:
            geaux_sdf = os.path.join(GEAUX_OUTPUT, tname, tname + '_new_0.sdf')
            native_sdf = VinaPath(tname).lig_sdf

            geaux_lig = pybel.readfile("sdf", geaux_sdf).next()
            native_lig = pybel.readfile("sdf", native_sdf).next()
            result_rmsd = rmsd_between(native_lig, geaux_lig)
            return result_rmsd
        except Exception as e:
            print(e)
            return None

    data = {}
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        data[tname] = foo(tname)

    with open("../dat/geaux_pred_rmsd.json", 'w') as ofs:
        ofs.write(json.dumps(data, indent=4, separators=(',', ': ')))


def main():
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        luigi.build([AddTypes(tname)], local_scheduler=True)


if __name__ == '__main__':
    # main()
    # test()
    # trace()
    eval_rmsd()
