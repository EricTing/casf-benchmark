import os
import pybel
import tempfile
import shlex
import subprocess32
import shutil


def lpc(complex_pdb, lpc_bin="/home/jaydy/local/LPC/lpcEx"):
    try:
        tmp_dir = tempfile.mkdtemp()
        merged_pdb_path = complex_pdb
        cmds = "{} 1 {}".format(lpc_bin, merged_pdb_path)
        print(cmds)
        cmds = shlex.split(cmds)
        os.chdir(tmp_dir)
        subprocess32.call(cmds)
        with open(os.path.join(tmp_dir, 'RES1')) as ifs:
            result = ifs.read()
        return result
    finally:
        shutil.rmtree(tmp_dir)


class LPC:
    def __init__(self, lig_path, prt_path):
        self._lig_path = lig_path
        self._prt_path = prt_path
        self._lig_format = os.path.splitext(self._lig_path)[-1][1:]
        self._prt_format = os.path.splitext(self._prt_path)[-1][1:]

    @staticmethod
    def merge(prt, lig):
        prt_pdb_lines = filter(lambda s: 'ATOM' in s,
                               prt.write('pdb').splitlines(True))
        lig_pdb_lines = filter(lambda s: ('ATOM' in s) or ('HETATM' in s),
                               lig.write('pdb').splitlines(True))
        to_write = []
        to_write.append("MODEL 1\n")
        to_write.extend(prt_pdb_lines)
        to_write.append("TER\n")
        to_write.extend(lig_pdb_lines)
        to_write.append("END\n")
        return "".join(to_write)

    def runLPC(self, lpc_bin="/home/jaydy/local/LPC/lpcEx"):
        prt = pybel.readfile(self._prt_format, self._prt_path).next()
        lig = pybel.readfile(self._lig_format, self._lig_path).next()
        merged = self.merge(prt, lig)

        try:
            tmp_dir = tempfile.mkdtemp()
            merged_pdb_path = os.path.join(tmp_dir, 'merged.pdb')
            with open(merged_pdb_path, 'w') as ofs:
                ofs.write(merged)
            cmds = "{} 1 {}".format(lpc_bin, merged_pdb_path)
            print(cmds)
            cmds = shlex.split(cmds)
            os.chdir(tmp_dir)
            subprocess32.call(cmds)
            with open(os.path.join(tmp_dir, 'RES1')) as ifs:
                result = ifs.read()
            return result
        finally:
            shutil.rmtree(tmp_dir)
