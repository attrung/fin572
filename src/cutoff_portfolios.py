"""Cutoff study, step 2: long the top X%, short the bottom X% (X = 5, 10, 20, 30, 40).

    python src/cutoff_portfolios.py monthly
    python src/cutoff_portfolios.py daily      (run monthly first)

Everything except the cutoff is the same as build_portfolios.py: same stocks, same signal
(log return t-12 .. t-2), same eligibility filters, value weights at t-1, one-month hold,
buy-and-hold daily weights. We reuse its functions so the rules cannot drift apart.

The only change: instead of 10 deciles, each month the stocks are split into
  Losers  = bottom X% of the signal
  Winners = top X% of the signal
(the middle 100 - 2X% is not held). Two breakpoint versions, as in build_portfolios.py:
  allfirm - X% of all eligible stocks in each leg
  nyse    - cut-offs at the Xth and (100-X)th percentiles of NYSE stocks
X = 10 gives exactly D1 and D10 of build_portfolios.py (checked by `check` below).

Output (data/processed/cutoffs):
  members.parquet                  one row per stock and month: me and its leg for each cutoff
  monthly_legs_<scheme>.parquet    month, cutoff, leg (L/W), ret, n, me
  daily_legs_<scheme>.parquet      date, cutoff, leg (L/W), ret, n
"""
import sys

import numpy as np
import pandas as pd

from build_portfolios import assign_deciles, load_crsp_monthly
from config import CUTOFFS, PROCESSED, RAW

OUT = PROCESSED / "cutoffs"
SCHEMES = ["allfirm", "nyse"]
LOSER, MIDDLE, WINNER = -1, 0, 1
LEG_NAME = {LOSER: "L", WINNER: "W"}


def leg_column(scheme, pct):
    return f"{scheme}_{pct}"


# --------------------------------------------------------------------------- legs

def all_firm_legs(rank, pct):
    """Bottom / top pct% of all stocks (same quantile rule as pd.qcut in all_firm_deciles)."""
    p = pct / 100
    return pd.qcut(rank.rank(method="first"), [0, p, 1 - p, 1], labels=False) - 1


def nyse_legs(rank, is_nyse, pct):
    """Cut-offs at the pct-th and (100-pct)-th percentiles of NYSE stocks (as in nyse_deciles)."""
    p = pct / 100
    low, high = np.quantile(rank[is_nyse], [p, 1 - p])
    leg = np.where(rank <= low, LOSER, np.where(rank > high, WINNER, MIDDLE))
    return pd.Series(leg, index=rank.index)


def assign_legs(panel):
    by_month = panel.groupby("month", group_keys=False)
    for pct in CUTOFFS:
        panel[leg_column("allfirm", pct)] = by_month["rank"].transform(
            lambda r: all_firm_legs(r, pct)).astype("int8")
        panel[leg_column("nyse", pct)] = by_month[["rank", "nyse"]].apply(
            lambda g: nyse_legs(g["rank"], g["nyse"], pct)).astype("int8")
    return panel


# --------------------------------------------------------------------------- returns

def value_weighted_legs(df, time_col, weight_col, scheme):
    """Value-weighted return of each leg, for every cutoff. Stocks with no return are left out
    (same as value_weighted in build_portfolios.py)."""
    df = df[df.ret.notna()].assign(w_ret=lambda x: x[weight_col] * x.ret)
    pieces = []
    for pct in CUTOFFS:
        col = leg_column(scheme, pct)
        held = df[df[col] != MIDDLE]
        g = held.groupby([time_col, col]).agg(w_ret=("w_ret", "sum"), w=(weight_col, "sum"),
                                              n=("permno", "size"), me=(weight_col, "mean"))
        g["ret"] = g.w_ret / g.w
        g = g.reset_index().rename(columns={col: "leg"})
        g["leg"] = g.leg.map(LEG_NAME)
        pieces.append(g.assign(cutoff=pct))
    return pd.concat(pieces, ignore_index=True)


def build_monthly():
    panel = assign_legs(assign_deciles(load_crsp_monthly()))
    OUT.mkdir(parents=True, exist_ok=True)
    leg_cols = [leg_column(s, p) for s in SCHEMES for p in CUTOFFS]
    panel[["month", "permno", "rank", "me", "d_all", "d_nyse"] + leg_cols].to_parquet(
        OUT / "members.parquet", index=False)

    for scheme in SCHEMES:
        out = value_weighted_legs(panel, "month", "me", scheme)
        out = out[["month", "cutoff", "leg", "ret", "n", "me"]].sort_values(["cutoff", "month", "leg"])
        out.to_parquet(OUT / f"monthly_legs_{scheme}.parquet", index=False)
        print(scheme, out.month.min(), out.month.max(), len(out), flush=True)


def build_daily():
    leg_cols = [leg_column(s, p) for s in SCHEMES for p in CUTOFFS]
    members = pd.read_parquet(OUT / "members.parquet", columns=["month", "permno", "me"] + leg_cols)
    members = members[(members[leg_cols] != MIDDLE).any(axis=1)]     # held in at least one leg
    pieces = {scheme: [] for scheme in SCHEMES}

    for path in sorted((RAW / "crsp.dsf_v2").glob("*.parquet")):
        d = pd.read_parquet(path, columns=["permno", "dlycaldt", "dlyret"])
        d["date"] = pd.to_datetime(d.dlycaldt)
        d["month"] = d.date.dt.to_period("M")
        d["dlyret"] = pd.to_numeric(d.dlyret, errors="coerce")
        d = d.merge(members, on=["month", "permno"])
        if d.empty:
            continue

        # buy-and-hold weight: cap at t-1 grown by the stock's return up to yesterday
        # (identical to build_portfolios.build_daily)
        d = d.sort_values(["permno", "date"])
        stock_month = [d.permno, d.month]
        growth = (1 + d.dlyret.fillna(0)).groupby(stock_month).cumprod()
        d["w"] = d.me * growth.groupby(stock_month).shift(1).fillna(1.0)
        d = d.rename(columns={"dlyret": "ret"})

        for scheme in SCHEMES:
            pieces[scheme].append(value_weighted_legs(d, "date", "w", scheme)
                                  [["date", "cutoff", "leg", "ret", "n"]])
        print(path.name, flush=True)

    for scheme, parts in pieces.items():
        out = pd.concat(parts).sort_values(["cutoff", "date", "leg"])
        out.to_parquet(OUT / f"daily_legs_{scheme}.parquet", index=False)
        print(scheme, out.date.min(), out.date.max(), len(out), flush=True)


# --------------------------------------------------------------------------- check

def check():
    """The 10% cutoff must give the same portfolios as D1 / D10 of build_portfolios.py."""
    members = pd.read_parquet(OUT / "members.parquet")
    for scheme, decile_col in [("allfirm", "d_all"), ("nyse", "d_nyse")]:
        expected = members[decile_col].map({1: LOSER, 10: WINNER}).fillna(MIDDLE)
        mismatched = (members[leg_column(scheme, 10)] != expected).sum()
        print(f"{scheme}: stocks whose 10% leg differs from D1/D10: {mismatched} of {len(members)}")

    for freq, time_col in [("monthly", "month"), ("daily", "date")]:
        for scheme in SCHEMES:
            ours_path = OUT / f"{freq}_legs_{scheme}.parquet"
            base_path = PROCESSED / f"{freq}_deciles_{scheme}.parquet"
            if not (ours_path.exists() and base_path.exists()):
                continue
            ours = pd.read_parquet(ours_path).query("cutoff == 10").pivot(
                index=time_col, columns="leg", values="ret")
            base = pd.read_parquet(base_path).pivot(index=time_col, columns="decile", values="ret")
            diff = (ours.W - ours.L) - (base[10] - base[1])
            print(f"{freq} {scheme}: max |WML(10%) - WML(D10-D1)| = {diff.abs().max():.2e} "
                  f"over {diff.notna().sum()} periods")


if __name__ == "__main__":
    {"monthly": build_monthly, "daily": build_daily, "check": check}[sys.argv[1]]()
