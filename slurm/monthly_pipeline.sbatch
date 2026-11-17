#!/bin/bash
# Monthly part: build monthly deciles, check them against Daniel's files, make the tables.
#   sbatch slurm/monthly_pipeline.sbatch
#SBATCH --job-name=dm-monthly
#SBATCH --partition=class
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=01:00:00
#SBATCH --output=/home/an8303/fin572/logs/%x-%j.out

set -e
module purge
module load anaconda3/2024.10
cd /home/an8303/fin572/src
PY=../.venv/bin/python

$PY build_portfolios.py monthly
$PY validate.py
$PY report.py allfirm
$PY report.py nyse
$PY report.py dm
