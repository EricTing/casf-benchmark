#!/usr/bin/env python

from paths import VinaPath, BOX_GYRA_BIN
import os
import subprocess32
import luigi
import shutil


def addCenter(ff_ifn, centers):
    # back up the ff file
    bk = ff_ifn + '.bk'
    shutil.copyfile(ff_ifn, bk)

    lines = file(ff_ifn).readlines()
    if "CENTER" in lines[0]:
        pass
    else:
        centers = map(str, centers)
        center_line = "CENTER " + ' '.join(centers) + "\n"
        lines.insert(0, center_line)

        with open(ff_ifn, 'w') as f:
            f.writelines(lines)


class AddNativeCenter(luigi.Task):
    tname = luigi.Parameter()

    def output(self):
        fn = os.path.splitext(ff_fn(self.tname))[0] + '_native_pkt.ff'
        return luigi.LocalTarget(fn)

    def run(self):
        vina_path = VinaPath(self.tname)
        lig_sdf = vina_path.lig_sdf

        cmds = ['perl', BOX_GYRA_BIN, lig_sdf]
        stdout = subprocess32.check_output(cmds)
        _, x, y, z = stdout.split()

        ff_ifn = ff_fn(self.tname)
        lines = file(ff_ifn).readlines()
        center_line = "CENTER {} {} {}\n".format(x, y, z)
        lines[0] = center_line

        with self.output().open('w') as ofs:
            ofs.writelines(lines)


def ff_fn(myid):
    return os.path.join("/work/jaydy/dat/website-core-set/input/params_ff",
                        myid + '.ff')


def main():
    pockets_ifn = "/work/jaydy/dat/website-core-set/input/pocket_center.out"
    for line in file(pockets_ifn):
        tokens = line.split()
        myid = tokens[0]
        ff_path = ff_fn(myid)
        addCenter(ff_path, tokens[1:])
        luigi.build([AddNativeCenter(myid)], local_scheduler=True)


def test():
    luigi.build([AddNativeCenter("3owjA00")], local_scheduler=True)


if __name__ == '__main__':
    main()
    # test()
