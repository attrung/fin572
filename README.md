# Momentum Crashes: replication

We replicate Daniel & Moskowitz (2016), "Momentum Crashes", *Journal of Financial Economics* 122, 221–247.
The paper uses US stocks from 1927 to 2013. We use **1960 to 2025**.

How it's going, and how our numbers compare to the paper: see [PROGRESS.md](PROGRESS.md).

## Where the data is

| Place | Path |
|---|---|
| Adroit | `/scratch/network/an8303/fin572/data` |
| Project folder | `data/` (a link to the Adroit folder above) |
| Google Drive | folder **FIN572 Data** (shared with us, so it's under "Shared with me") |

The data is too big for the Adroit home folder, so it lives on scratch. The Drive folder is a copy.

```
data/
  raw/crsp.msf_v2/      CRSP monthly stock file, 1958-2025 (one file per year)
  raw/crsp.dsf_v2/      CRSP daily stock file, 1958-2025 (one file per month)
  raw/ff/               Fama-French factors (market, rf, SMB, HML), monthly and daily
  processed/            our momentum portfolios (made by the code below)
  benchmark/            Kent Daniel's published momentum portfolios + the paper (NBER version)
```

**Where it comes from.**
- **CRSP** (the new CIZ format) and **Fama-French**: the WRDS web API. You need a WRDS API token in `~/.wrds_api_token`.
- **Daniel's portfolios**: [kentdaniel.net](https://www.kentdaniel.net/data.php), file `DM_data_2017_03.tar.gz`.

**Copy data to or from Google Drive.** rclone can only read a "Shared with me" folder by name, so use the folder ID:

```bash
# upload (only sends new or changed files)
rclone copy -L data/ gdrive: --drive-root-folder-id 1A0-5aHZBF8evcBcanZUtAmVWnBmoDhHU
# download
rclone copy gdrive: data/ --drive-root-folder-id 1A0-5aHZBF8evcBcanZUtAmVWnBmoDhHU
```

## How to run it

Run the download on the login node. It only waits on the network. Everything else is a Slurm job.

```bash
module load anaconda3/2024.10
python -m venv --system-site-packages .venv && .venv/bin/pip install wrds arch pyarrow

cd src
../.venv/bin/python download.py ff         # 1. download (about 3 hours for daily)
../.venv/bin/python download.py monthly
../.venv/bin/python download.py daily
cd ..
sbatch slurm/monthly_pipeline.sbatch       # 2-3, 5: monthly portfolios, checks, tables (~2 min)
sbatch slurm/daily_pipeline.sbatch         # 2-5: daily portfolios, GARCH, all tables (~15 min)
```

## The code

Each step is one file in `src/`. Run them in this order:

| Step | File | What it does |
|---|---|---|
| 1 | `download.py` | Downloads CRSP and Fama-French from WRDS. |
| 2 | `build_portfolios.py` | Ranks stocks on past returns and makes the 10 momentum portfolios (monthly and daily). |
| 3 | `validate.py` | Compares our portfolios with Daniel's published ones. |
| 4 | `garch.py` | Forecasts momentum volatility; the dynamic strategy needs it. |
| 5 | `report.py` | Makes all tables and figures. |

Helper files:
- `config.py`: folders and sample periods
- `load_data.py`: puts portfolios and market data into one table
- `regression.py`: OLS and table formatting
- `tables.py`: paper Tables 1–5
- `dynamic.py`: the dynamic strategy and Table 7
- `figures.py`: the figures

We make every table three times:
- `allfirm`: our portfolios, built the paper's way (each decile has the same number of stocks)
- `nyse`: our portfolios with NYSE cut-offs (like Ken French's portfolios)
- `dm`: Daniel's own portfolios. This lets us check our code against the paper.

### Cutoff study (`results_quartile/`)

The same strategy, but long the top X% and short the bottom X% for X = 5, 10, 20, 30, 40
(10% is the baseline D10 − D1, and matches it exactly). See [results_quartile/README.md](results_quartile/README.md).

| Step | File | What it does |
|---|---|---|
| 2 | `cutoff_portfolios.py` | Builds the top / bottom X% legs (monthly and daily); `check` compares 10% with D1/D10. |
| 4 | `cutoff_garch.py` | GARCH volatility forecasts for each cutoff's WML. |
| 5 | `cutoff_report.py` | All replication tables and figures per cutoff, plus the comparison across cutoffs. |

Run: `sbatch slurm/cutoff_pipeline.sbatch`, or the five commands in `results_quartile/README.md`.

## Output

- `results/tables_allfirm.md`, `tables_nyse.md`, `tables_dm.md`: all tables
- `results/validation_vs_dm.csv`: how close our portfolios are to Daniel's
- `results/figs/<version>/`: figures
- `results_quartile/`: the cutoff study (summary tables, per-cutoff reports, figures)
- `logs/`: download and Slurm logs
