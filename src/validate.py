"""Step 3: check our portfolios against Kent Daniel's published DM portfolios.

    python src/validate.py

Daniel's files (data/benchmark, March 2017 release, 1927-2016). Columns: date, decile,
return, average market cap, number of firms.
  m_m_pt_tot.txt / d_m_pt_tot.txt            monthly / daily, all-firm breakpoints
  m_m_pt_nyse_tot.txt / d_m_pt_nyse_tot.txt  monthly / daily, NYSE breakpoints

Also saves Daniel's portfolios in our own format (scheme "dm"), so every table can be
run on his data too: data/processed/{monthly,daily}_deciles_dm.parquet

Output: results/validation_vs_dm.csv and a printed summary.
"""
import numpy as np
import pandas as pd

from config import BENCHMARK, PROCESSED, RESULTS

DM_FILES = {
    ("monthly", "allfirm"): "m_m_pt_tot.txt",
    ("monthly", "nyse"): "m_m_pt_nyse_tot.txt",
    ("daily", "allfirm"): "d_m_pt_tot.txt",
    ("daily", "nyse"): "d_m_pt_nyse_tot.txt",
}
PERIODS_PER_YEAR = {"monthly": 12, "daily": 252}


def read_dm(freq, scheme):
    df = pd.read_csv(BENCHMARK / DM_FILES[freq, scheme], sep=r"\s+", header=None,
                     names=["date", "decile", "ret", "me", "n"])
    df = df[df.decile.astype(str) != "."].astype({"decile": int})   # "." = firms with no decile
    df["date"] = pd.to_datetime(df.date.astype(str))
    if freq == "monthly":
        df["date"] = df.date.dt.to_period("M")
    return df.pivot(index="date", columns="decile", values=["ret", "n"])


def read_ours(freq, scheme):
    path = PROCESSED / f"{freq}_deciles_{scheme}.parquet"
    if not path.exists():
        return None
    df = pd.read_parquet(path).rename(columns={"month": "date"})
    return df.pivot(index="date", columns="decile", values=["ret", "n"])


def compare(ours, dm, freq):
    dates = ours.index.intersection(dm.index)
    ours, dm = ours.loc[dates], dm.loc[dates]
    ours_ret = ours["ret"].assign(WML=ours["ret"][10] - ours["ret"][1])
    dm_ret = dm["ret"].assign(WML=dm["ret"][10] - dm["ret"][1])

    rows = []
    for col in ours_ret:
        a, b = ours_ret[col], dm_ret[col]
        rows.append({
            "portfolio": col,
            "correlation": a.corr(b),
            "mean ours": a.mean(),
            "mean DM": b.mean(),
            "tracking error (ann.)": (a - b).std() * np.sqrt(PERIODS_PER_YEAR[freq]),
            "firms ours": ours["n"][col].mean() if col != "WML" else np.nan,
            "firms DM": dm["n"][col].mean() if col != "WML" else np.nan,
        })
    return pd.DataFrame(rows), dates


def save_dm_in_our_format():
    """Daniel's all-firm portfolios (the paper's data), saved like ours."""
    for freq, date_col in [("monthly", "month"), ("daily", "date")]:
        dm = read_dm(freq, "allfirm").stack(future_stack=True).reset_index()
        dm.columns = [date_col, "decile", "ret", "n"]
        dm.to_parquet(PROCESSED / f"{freq}_deciles_dm.parquet", index=False)


def main():
    RESULTS.mkdir(exist_ok=True)
    save_dm_in_our_format()
    tables = []
    for freq, scheme in DM_FILES:
        ours = read_ours(freq, scheme)
        if ours is None:
            continue
        table, dates = compare(ours, read_dm(freq, scheme), freq)
        print(f"\n== {freq}, {scheme} breakpoints: {dates.min()} to {dates.max()} ({len(dates)} periods)")
        print(table.round(4).to_string(index=False))
        tables.append(table.assign(frequency=freq, breakpoints=scheme))
    pd.concat(tables).to_csv(RESULTS / "validation_vs_dm.csv", index=False)


if __name__ == "__main__":
    main()
