"""Paths and settings shared by all scripts."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"                  # symlink to /scratch/network/an8303/fin572/data
RAW = DATA / "raw"                    # downloaded from WRDS
PROCESSED = DATA / "processed"        # our momentum portfolios
BENCHMARK = DATA / "benchmark"        # Kent Daniel's published portfolios
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figs"

# Periods we report results for
SAMPLES = {
    "1960:01-2025:12 (full)": ("1960-01", "2025-12"),
    "1960:01-2013:03 (paper overlap)": ("1960-01", "2013-03"),
    "2013:04-2025:12 (after the paper)": ("2013-04", "2025-12"),
}
FULL = "1960:01-2025:12 (full)"

# The paper's own sample. Only Daniel's data (scheme "dm") goes back this far.
PAPER = "1927:01-2013:03 (paper's sample)"
SAMPLES_FOR_DM = {PAPER: ("1927-01", "2013-03"),
                  "1960:01-2013:03 (paper overlap)": ("1960-01", "2013-03")}


def in_sample(df, sample):
    """Rows of a month-indexed frame that fall inside a sample period."""
    start, end = {**SAMPLES, **SAMPLES_FOR_DM}[sample]
    return df.loc[pd.Period(start, "M"):pd.Period(end, "M")]
