"""Step 2: build the momentum decile portfolios, following Daniel & Moskowitz (2016).

    python src/build_portfolios.py monthly
    python src/build_portfolios.py daily      (run monthly first)

Rules (from Kent Daniel's notes on the DM portfolios, data/benchmark/mom_data.pdf):
  * Stocks: common shares (CRSP share code 10/11) on NYSE, AMEX or Nasdaq.
  * Rank stocks at the end of month t-1 on their return from month t-12 to t-2
    (sum of log returns; skip the most recent month).
  * A stock needs: a price at t-13, a return at t-2, and a market cap at t-1.
  * Split into 10 deciles. Two versions:
      allfirm - same number of stocks in each decile (the paper's main version)
      nyse    - cut-offs from NYSE stocks only (like Ken French's portfolios)
  * Weight by market cap at t-1. Hold for one month.
  * Daily returns: same stocks all month, buy-and-hold weights.
  * Delisting returns are already inside CRSP CIZ returns (mthret / dlyret).

Output (data/processed):
  members.parquet                    one row per stock and month, with its deciles
  monthly_deciles_<scheme>.parquet   month, decile, ret, n (stocks), me (average cap)
  daily_deciles_<scheme>.parquet     date, decile, ret, n
"""
import sys

import numpy as np
import pandas as pd

from config import PROCESSED, RAW

FIRST_HOLDING_MONTH = pd.Period("1959-01", "M")
DECILE_COLUMN = {"allfirm": "d_all", "nyse": "d_nyse"}


# --------------------------------------------------------------------------- inputs

def load_crsp_monthly():
    files = sorted((RAW / "crsp.msf_v2").glob("*.parquet"))
    df = pd.concat([pd.read_parquet(f) for f in files])
    df["month"] = pd.to_datetime(df.mthcaldt).dt.to_period("M")
    for col in ["mthret", "mthprc", "mthcap"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # CIZ version of "share code 10/11" (US common stock)
    common_stock = ((df.sharetype == "NS") & (df.securitytype == "EQTY")
                    & (df.securitysubtype == "COM") & (df.usincflg == "Y")
                    & df.issuertype.isin(["ACOR", "CORP"]))
    # CIZ version of "exchange code 1/2/3" (NYSE, AMEX, Nasdaq), regular-way trading
    main_exchange = (df.primaryexch.isin(["N", "A", "Q"]) & (df.conditionaltype == "RW")
                     & (df.tradingstatusflg == "A"))
    df["eligible"] = (common_stock & main_exchange).astype(float)
    df["nyse"] = (df.primaryexch == "N").astype(float)
    return df


# --------------------------------------------------------------------------- deciles

def all_firm_deciles(rank):
    """Equal number of stocks in each decile."""
    return pd.qcut(rank.rank(method="first"), 10, labels=False) + 1


def nyse_deciles(rank, is_nyse):
    """Cut-offs at the 10th, 20th, ... percentiles of NYSE stocks."""
    cutoffs = np.quantile(rank[is_nyse], np.arange(0.1, 1.0, 0.1))
    return pd.Series(np.searchsorted(cutoffs, rank.values) + 1, index=rank.index)


def assign_deciles(df):
    """One row per (stock, holding month t) with ranking return, weight and deciles."""
    months = pd.period_range(df.month.min(), df.month.max(), freq="M", name="month")

    def wide(col):   # months x stocks
        return df.pivot(index="month", columns="permno", values=col).reindex(months)

    ret, price, cap = wide("mthret"), wide("mthprc"), wide("mthcap")
    eligible = wide("eligible").fillna(0).astype(bool)
    nyse = wide("nyse").fillna(0).astype(bool)

    # ranking return for holding month t = sum of log returns over t-12 .. t-2
    with np.errstate(divide="ignore"):   # a -100% return gives log(0) = -inf, ranked last
        log_ret = np.log1p(ret)
    rank = log_ret.shift(2).rolling(11, min_periods=1).sum()

    keep = (eligible.shift(1, fill_value=False)      # eligible at formation (t-1)
            & price.shift(13).notna()                 # price at t-13
            & ret.shift(2).notna()                    # return at t-2
            & (cap.shift(1) > 0)                      # market cap at t-1
            & rank.notna())

    panel = pd.DataFrame({
        "rank": rank.stack(), "keep": keep.stack(), "me": cap.shift(1).stack(),
        "nyse": nyse.shift(1, fill_value=False).stack(), "ret": ret.stack(),
    })
    panel = panel[panel.keep].drop(columns="keep").reset_index()
    panel = panel[panel.month >= FIRST_HOLDING_MONTH]

    by_month = panel.groupby("month", group_keys=False)
    panel["d_all"] = by_month["rank"].transform(all_firm_deciles)
    panel["d_nyse"] = by_month[["rank", "nyse"]].apply(lambda g: nyse_deciles(g["rank"], g["nyse"]))
    return panel


# --------------------------------------------------------------------------- returns

def value_weighted(group):
    group = group[group.ret.notna()]
    return pd.Series({"ret": np.average(group.ret, weights=group.me),
                      "n": len(group), "me": group.me.mean()})


def build_monthly():
    panel = assign_deciles(load_crsp_monthly())
    PROCESSED.mkdir(parents=True, exist_ok=True)
    panel[["month", "permno", "rank", "me", "nyse", "d_all", "d_nyse"]].to_parquet(
        PROCESSED / "members.parquet", index=False)

    for scheme, col in DECILE_COLUMN.items():
        out = (panel.groupby(["month", col]).apply(value_weighted, include_groups=False)
               .reset_index().rename(columns={col: "decile"})
               .astype({"decile": int, "n": int}))
        out.to_parquet(PROCESSED / f"monthly_deciles_{scheme}.parquet", index=False)
        print(scheme, out.month.min(), out.month.max(), len(out))


def build_daily():
    members = pd.read_parquet(PROCESSED / "members.parquet",
                              columns=["month", "permno", "me", "d_all", "d_nyse"])
    pieces = {scheme: [] for scheme in DECILE_COLUMN}

    for path in sorted((RAW / "crsp.dsf_v2").glob("*.parquet")):
        d = pd.read_parquet(path, columns=["permno", "dlycaldt", "dlyret"])
        d["date"] = pd.to_datetime(d.dlycaldt)
        d["month"] = d.date.dt.to_period("M")
        d["dlyret"] = pd.to_numeric(d.dlyret, errors="coerce")
        d = d.merge(members, on=["month", "permno"])     # only stocks in a portfolio
        if d.empty:
            continue

        # buy-and-hold weight: cap at t-1 grown by the stock's return up to yesterday
        d = d.sort_values(["permno", "date"])
        stock_month = [d.permno, d.month]
        growth = (1 + d.dlyret.fillna(0)).groupby(stock_month).cumprod()
        d["w"] = d.me * growth.groupby(stock_month).shift(1).fillna(1.0)
        d = d[d.dlyret.notna()]
        d["w_ret"] = d.w * d.dlyret

        for scheme, col in DECILE_COLUMN.items():
            g = d.groupby(["date", col]).agg(w_ret=("w_ret", "sum"), w=("w", "sum"),
                                             n=("permno", "size"))
            g["ret"] = g.w_ret / g.w
            pieces[scheme].append(g[["ret", "n"]].reset_index().rename(columns={col: "decile"}))
        print(path.name, flush=True)

    for scheme, parts in pieces.items():
        out = pd.concat(parts).astype({"decile": int}).sort_values(["date", "decile"])
        out.to_parquet(PROCESSED / f"daily_deciles_{scheme}.parquet", index=False)
        print(scheme, out.date.min(), out.date.max(), len(out))


if __name__ == "__main__":
    {"monthly": build_monthly, "daily": build_daily}[sys.argv[1]]()
