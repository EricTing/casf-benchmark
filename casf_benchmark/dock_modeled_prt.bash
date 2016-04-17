#!/usr/bin/env bash

complex=$1

bin=~/local/bin/dock
# bin=~/Workspace/Bitbucket/geauxdock/src/dock


version_0_7_dock() {
    mycomplex=$1

    PDB_DIR=/work/jaydy/dat/pred_pkt_casf/models-0.7

    SDF_DIR=/work/jaydy/dat/website-core-set/input/ligand-sdf

    FF_DIR=/work/jaydy/dat/pred_pkt_casf/params_ff-0.7

    paras=/home/jaydy/Workspace/Bitbucket/geauxdock/data/parameters/paras

    OUT_DIR=/work/jaydy/working/casf_model_0.7

    out_dir=$OUT_DIR/${mycomplex}
    mkdir -p $out_dir

    pdb_file=$PDB_DIR/${mycomplex}.pdb
    sdf_file=$SDF_DIR/$(echo ${mycomplex:0:4})_ligand.sdf

    ff_file=$FF_DIR/${mycomplex}_pkt_add.ff
    csv_file=$out_dir/${mycomplex}_0.7.csv

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


version_0_5_dock() {
    mycomplex=$1

    PDB_DIR=/work/jaydy/dat/pred_pkt_casf/models-0.5

    SDF_DIR=/work/jaydy/dat/website-core-set/input/ligand-sdf

    FF_DIR=/work/jaydy/dat/pred_pkt_casf/params_ff-0.5

    paras=/home/jaydy/Workspace/Bitbucket/geauxdock/data/parameters/paras

    OUT_DIR=/work/jaydy/working/casf_model_0.5

    out_dir=$OUT_DIR/${mycomplex}
    mkdir -p $out_dir

    pdb_file=$PDB_DIR/${mycomplex}.pdb
    sdf_file=$SDF_DIR/$(echo ${mycomplex:0:4})_ligand.sdf

    ff_file=$FF_DIR/${mycomplex}_pkt_add.ff
    csv_file=$out_dir/${mycomplex}_0.5.csv

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


version_0_7_dock $complex
version_0_5_dock $complex
