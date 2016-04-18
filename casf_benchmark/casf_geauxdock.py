#!/usr/bin/env python

from paths import VinaPath, GEAUX_OUTPUT, ModelPath
from casf_vina import EvalVinaModeledProtein
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

    def pred_foo(tname):
        try:
            csv_ifn = os.path.join(GEAUX_OUTPUT, tname, tname + '.csv')
            df = pd.read_csv(csv_ifn, sep=' ')
            cols = ["lig", "prt", "mv1", "mv2", "mv3", "mv4", "mv5", "mv6"]
            trace_ifn = os.path.join(GEAUX_OUTPUT, tname, tname + '_trace.csv')
            df[cols][:1].to_csv(trace_ifn, sep=' ', index=False)
        except Exception as e:
            print(e)

    def native_foo(tname):
        try:
            csv_ifn = os.path.join(GEAUX_OUTPUT, tname,
                                   tname + '_native_pkt.csv')
            df = pd.read_csv(csv_ifn, sep=' ')
            cols = ["lig", "prt", "mv1", "mv2", "mv3", "mv4", "mv5", "mv6"]
            trace_ifn = os.path.join(GEAUX_OUTPUT, tname,
                                     tname + '_native_trace.csv')
            df[cols][:1].to_csv(trace_ifn, sep=' ', index=False)
        except Exception as e:
            print(e)

    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        pred_foo(tname)
        native_foo(tname)


def eval_rmsd():
    """evaluate the geauxdock prediction using RMSD
    """

    def native_foo(tname):
        try:
            geaux_sdf = os.path.join(GEAUX_OUTPUT, tname,
                                     tname + '_native_0.sdf')
            native_sdf = VinaPath(tname).lig_sdf

            geaux_lig = pybel.readfile("sdf", geaux_sdf).next()
            native_lig = pybel.readfile("sdf", native_sdf).next()
            result_rmsd = rmsd_between(native_lig, geaux_lig)
            return result_rmsd
        except Exception as e:
            print(e)
            return None

    def pred_foo(tname):
        try:
            geaux_sdf = os.path.join(GEAUX_OUTPUT, tname,
                                     tname + '_pred_0.sdf')
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
        data[tname] = native_foo(tname)

    with open("../dat/geaux_native_rmsd.json", 'w') as ofs:
        ofs.write(json.dumps(data, indent=4, separators=(',', ': ')))

    data = {}
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        data[tname] = pred_foo(tname)

    with open("../dat/geaux_pred_rmsd.json", 'w') as ofs:
        ofs.write(json.dumps(data, indent=4, separators=(',', ': ')))


def eval_rmsd_modeled_prt():
    """evaluate the geauxdock prediction on modeled protein structures
    """

    def helper_vina(tname, version='0.7'):
        try:
            result = EvalVinaModeledProtein(tname, version=version)
            with result.output().open('r') as ifs:
                data = json.loads(ifs.read())
            return data.values()[0]
        except Exception as e:
            print(e)
            return None

    def helper_geauxdock(tname, version="0.7"):
        try:
            native_sdf = VinaPath(tname).lig_sdf
            geaux_sdf = os.path.join(
                ModelPath(tname,
                          version=version).work_dir,
                "{}_{}_0.sdf".format(tname, version))
            geaux_lig = pybel.readfile("sdf", geaux_sdf).next()
            native_lig = pybel.readfile("sdf", native_sdf).next()
            result_rmsd = rmsd_between(native_lig, geaux_lig)
            return result_rmsd
        except Exception as e:
            print(e)
            return None

    data = {}
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        geaux_r1 = helper_geauxdock(tname, version="0.7")
        geaux_r2 = helper_geauxdock(tname, version="0.5")

        vina_r1 = helper_vina(tname, version='0.7')
        vina_r2 = helper_vina(tname, version='0.5')

        data[tname] = {"geaux_0.7": geaux_r1,
                       "geaux_0.5": geaux_r2,
                       "vina_0.7": vina_r1,
                       "vina_0.5": vina_r2}

    with open("../dat/geaux_modeled_prt_rmsd.json", 'w') as ofs:
        ofs.write(json.dumps(data, indent=4, separators=(',', ': ')))


def main():
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        luigi.build([AddTypes(tname)], local_scheduler=True)


if __name__ == '__main__':
    # main()
    # test()
    # trace()
    # eval_rmsd()
    eval_rmsd_modeled_prt()
