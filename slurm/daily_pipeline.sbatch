#!/bin/bash
# Daily part (after the daily download): daily deciles, check vs Daniel, GARCH forecasts,
# then all tables and figures for both breakpoint versions.
#   sbatch slurm/daily_pipeline.sbatch
#SBATCH --job-name=dm-daily
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

$PY build_portfolios.py daily
$PY validate.py
for scheme in allfirm nyse dm; do
    $PY garch.py $scheme 1970-01
    $PY report.py $scheme
done
