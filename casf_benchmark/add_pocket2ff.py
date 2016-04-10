#!/usr/bin/env python

import os
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


if __name__ == '__main__':
    main()
