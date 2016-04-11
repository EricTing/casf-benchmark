#!/usr/bin/env python

from paths import VinaPath
import luigi
import pybel


class LigSdf(luigi.Task):
    tname = luigi.Parameter()

    def run(self):
        vina_path = VinaPath(self.tname)
        lig_sdf = vina_path.lig_sdf
        lig = pybel.readfile("sdf", lig_sdf).next()
        lig.removeh()
        lig.write("pdbqt", self.output().path)

    def output(self):
        ofn = VinaPath(self.tname).lig_pdbqt
        return luigi.LocalTarget(ofn)


def main():
    tnames = [_.rstrip() for _ in file("../dat/casf_names.txt")]
    luigi.build([LigSdf(tname) for tname in tnames], local_scheduler=True)


if __name__ == '__main__':
    main()
