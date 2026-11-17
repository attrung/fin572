#!/bin/bash
# Cutoff study (results_quartile/): top / bottom 5, 10, 20, 30, 40% instead of deciles.
# Needs data/raw (CRSP monthly + daily, Fama-French). Run the decile pipelines first if you
# also want the check that the 10% cutoff equals D10 - D1.
#   sbatch slurm/cutoff_pipeline.sbatch
#SBATCH --job-name=dm-cutoffs
#SBATCH --partition=class
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=06:00:00
#SBATCH --output=/home/an8303/fin572/logs/%x-%j.out

set -e
module purge
module load anaconda3/2024.10
cd /home/an8303/fin572/src
PY=../.venv/bin/python

$PY cutoff_portfolios.py monthly
$PY cutoff_portfolios.py daily
$PY cutoff_portfolios.py check
$PY cutoff_garch.py
$PY cutoff_report.py
