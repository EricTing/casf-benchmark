#!/usr/bin/env bash

complex=$1

readonly bin=~/local/bin/dock
# readonly bin=~/Workspace/Bitbucket/geauxdock/src/dock

readonly PDB_DIR=/work/jaydy/dat/website-core-set/input/protein-pdb

readonly SDF_DIR=/work/jaydy/dat/website-core-set/input/ligand-sdf

readonly FF_DIR=/work/jaydy/dat/website-core-set/input/params_ff

readonly paras=/home/jaydy/Workspace/Bitbucket/geauxdock/data/parameters/paras

readonly OUT_DIR=/work/jaydy/dat/website-core-set/output

readonly out_dir=$OUT_DIR/${complex}
mkdir -p $out_dir

readonly pdb_file=$PDB_DIR/${complex}.pdb
readonly sdf_file=$SDF_DIR/$(echo ${complex:0:4})_ligand.sdf

pred_pkt_dock() {
    mycomplex=$1
    ff_file=$FF_DIR/${mycomplex}.ff
    csv_file=$out_dir/$mycomplex.csv

    cmd="\
${bin} \
--id ${mycomplex} \
-p ${pdb_file} \
-l ${sdf_file} \
-s ${ff_file} \
\
--para ${paras} \
\
--csv $csv_file \
 --nc 10 \
--floor_temp 0.01 \
--ceiling_temp 0.036 \
--nt 1 \
-t 0.02 \
-r 0.08 \
"

    echo ${cmd}
    ${cmd}
}

native_pkt_dock() {
    ff_file=$FF_DIR/${mycomplex}_native_pkt.ff
    csv_file=$out_dir/${mycomplex}_native_pkt.csv

    cmd="\
${bin} \
--id ${mycomplex} \
-p ${pdb_file} \
-l ${sdf_file} \
-s ${ff_file} \
\
--para ${paras} \
\
--csv $csv_file \
 --nc 10 \
--floor_temp 0.01 \
--ceiling_temp 0.036 \
--nt 1 \
-t 0.02 \
-r 0.08 \
"
    echo ${cmd}
    ${cmd}
}

pred_pkt_dock $complex
native_pkt_dock $complex
