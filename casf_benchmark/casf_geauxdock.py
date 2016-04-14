#!/usr/bin/env python

from paths import VinaPath
import luigi
import add_lig_atom_types


class AddTypes(luigi.Task):
    tname = luigi.Parameter()

    def run(self):
        vina_path = VinaPath(self.tname)
        lig_sdf = vina_path.lig_sdf
        add_lig_atom_types.main(lig_sdf)


def test():
    luigi.build([AddTypes("1h23A01")], local_scheduler=True)


def main():
    for tname in [_.rstrip() for _ in file("../dat/casf_names.txt")]:
        luigi.build([AddTypes(tname)], local_scheduler=True)


if __name__ == '__main__':
    main()
    # test()
