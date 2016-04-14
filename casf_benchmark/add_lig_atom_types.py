#!/usr/bin/env python

from openbabel import OBAtomAtomIter, OBTypeTable
import pybel
import shutil


def test():
    sdf_ifn = "/home/jaydy/Workspace/Bitbucket/geauxdock/data/10gs/10gs_ligand.sdf"

    lig = pybel.readfile("sdf", sdf_ifn).next()

    typetable = OBTypeTable()
    typetable.SetFromType('INT')
    typetable.SetToType('SYB')

    types = [typetable.Translate(a.type) for a in lig.atoms]

    to_write = ' '.join(types)

    lig.data['OB_ATOM_TYPES'] = to_write

    lig.write("sdf", "10gs_ligand.sdf", overwrite=True)


def main(sdf_ifn):
    # back up
    bk = sdf_ifn + "_bk"
    shutil.copyfile(sdf_ifn, bk)

    lig = pybel.readfile("sdf", sdf_ifn).next()

    typetable = OBTypeTable()
    typetable.SetFromType('INT')
    typetable.SetToType('SYB')

    types = [typetable.Translate(a.type) for a in lig.atoms]
    to_write = ' '.join(types)
    lig.data['OB_ATOM_TYPES'] = to_write

    lig.write("sdf", sdf_ifn, overwrite=True)


if __name__ == '__main__':
    import sys
    ifn = sys.argv[1]
    main(ifn)
