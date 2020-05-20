#! /bin/bash
for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/1agw_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/1fgi_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/1fgi_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/2fgi_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/2fgi_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/3c4f_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/3c4f_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/3gql_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/3gql_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/3js2_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/3js2_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/3tt0_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/3tt0_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/4wun_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/4wun_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/5a46_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/5a46_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/6mzw_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/6mzw_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done

cd /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/actives/6nvl_A;

for f in /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/actives/*pdbqt; do
    b=`basename $f .pdbqt`
    echo Processing ligand $b
    mkdir -p $b
    vina --config /home/john/docking_results_calculations/DUDE/vina/active_decoy_merged_results/fgfr1/completed_assays/config_files/6nvl_A.conf --ligand $f --out ${b}/out.pdbqt --log ${b}/log.txt
done




