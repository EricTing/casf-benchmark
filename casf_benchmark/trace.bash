#!/usr/bin/env bash

readonly bin=~/local/bin/dock
# readonly bin=~/Workspace/Bitbucket/geauxdock/src/dock

readonly PDB_DIR=/work/jaydy/dat/website-core-set/input/protein-pdb

readonly SDF_DIR=/work/jaydy/dat/website-core-set/input/ligand-sdf

readonly FF_DIR=/work/jaydy/dat/website-core-set/input/params_ff

readonly paras=/home/jaydy/Workspace/Bitbucket/geauxdock/data/parameters/paras

readonly OUT_DIR=/work/jaydy/dat/website-core-set/output

pred_trace() {
    complex=$1

    pdb_file=$PDB_DIR/${complex}.pdb
    sdf_file=$SDF_DIR/$(echo ${complex:0:4})_ligand.sdf
    ff_file=$FF_DIR/${complex}.ff

    out_dir=$OUT_DIR/${complex}
    mkdir -p $out_dir

    csv_file=$out_dir/${complex}_trace.csv
    conf_file=$out_dir/${complex}_pred


    cmd="\
${bin} \
--id ${complex} \
-p ${pdb_file} \
-l ${sdf_file} \
-s ${ff_file} \
\
--para ${paras} \
--trace \
--conf $conf_file \
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

native_trace() {
    complex=$1

    pdb_file=$PDB_DIR/${complex}.pdb
    sdf_file=$SDF_DIR/$(echo ${complex:0:4})_ligand.sdf
    ff_file=$FF_DIR/${complex}_native_pkt.ff

    out_dir=$OUT_DIR/${complex}
    mkdir -p $out_dir

    csv_file=$out_dir/${complex}_native_trace.csv
    conf_file=$out_dir/${complex}_native


    cmd="\
${bin} \
--id ${complex} \
-p ${pdb_file} \
-l ${sdf_file} \
-s ${ff_file} \
\
--para ${paras} \
--trace \
--conf $conf_file \
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

for complex in `cat ../dat/casf_names.txt `; do
    pred_trace $complex
    native_trace $complex
done
