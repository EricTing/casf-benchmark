#!/usr/bin/env python

from casf_vina import EvalVinaResult
import luigi
import json


class ReduceVinaRMSD(luigi.Task):
    def output(self):
        ofn = "../dat/vina_rmsd.json"
        return luigi.LocalTarget(ofn)

    def run(self):
        tnames = [_.rstrip() for _ in file("../dat/casf_names.txt")]
        datas = {}
        for tname in tnames:
            try:
                data = json.loads(EvalVinaResult(tname).output().open(
                    'r').read())
                datas.update({tname: data})
            except Exception as e:
                print(e, tname, 'fails')

        with open(self.output().path, 'w') as ofs:
            ofs.write(json.dumps(datas, indent=4, separators=(',', ': ')))


def main():
    luigi.build([ReduceVinaRMSD()], local_scheduler=True)


if __name__ == '__main__':
    main()
