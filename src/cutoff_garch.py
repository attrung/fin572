"""Cutoff study, step 4: volatility forecasts of each cutoff's daily WML (for the dynamic strategy).

    python src/cutoff_garch.py                 all schemes and cutoffs
    python src/cutoff_garch.py allfirm 20      one scheme / cutoff

Same model as garch.py (GJR-GARCH(1,1), in-sample and out-of-sample from 1970-01),
applied to WML = Winners - Losers of each cutoff.

Output: data/processed/cutoffs/wml_vol_<scheme>_<cutoff>.parquet
"""
import os
import sys

import pandas as pd

from config import CUTOFFS
from cutoff_portfolios import OUT, SCHEMES
from garch import volatility_table

OOS_START = "1970-01"


def daily_wml(scheme, pct):
    d = pd.read_parquet(OUT / f"daily_legs_{scheme}.parquet").query("cutoff == @pct")
    d = d.pivot(index="date", columns="leg", values="ret")
    return (d.W - d.L).dropna()


def main(schemes=SCHEMES, cutoffs=CUTOFFS):
    workers = int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count() or 4))
    for scheme in schemes:
        for pct in cutoffs:
            out = volatility_table(daily_wml(scheme, pct), OOS_START, verbose=False, workers=workers)
            out.reset_index().to_parquet(OUT / f"wml_vol_{scheme}_{pct}.parquet", index=False)
            print(scheme, pct, "done;", out.dropna().mean().round(4).to_dict(), flush=True)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main([sys.argv[1]], [int(sys.argv[2])])
    else:
        main()
