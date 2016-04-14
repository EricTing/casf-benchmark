#!/usr/bin/env bash

complex=$1

readonly bin=~/local/bin/dock

readonly PDB_DIR=/work/jaydy/dat/website-core-set/input/protein-pdb

readonly SDF_DIR=/work/jaydy/dat/website-core-set/input/ligand-sdf

readonly FF_DIR=/work/jaydy/dat/website-core-set/input/params_ff

readonly paras=/home/jaydy/Workspace/Bitbucket/geauxdock/data/parameters/paras

readonly OUT_DIR=/work/jaydy/dat/website-core-set/output

pdb_file=$PDB_DIR/${complex}.pdb
sdf_file=$SDF_DIR/$(echo ${complex:0:4})_ligand.sdf
ff_file=$FF_DIR/${complex}.ff

out_dir=$OUT_DIR/${complex}
mkdir -p $out_dir

csv_file=$out_dir/$complex.csv


cmd="\
${bin} \
--id ${complex} \
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
