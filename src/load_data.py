"""Load our portfolios and the market data into one table per frequency.

Monthly table (index = month) columns:
  D1..D10, WML        decile returns, WML = D10 - D1
  mktrf, rf, mkt      Fama-French market excess return, risk-free rate, market return
  smb, hml            Fama-French size and value factors
  mkt24               market return over the past 24 months (t-24 .. t-1)
  IB                  bear market: 1 if mkt24 < 0
  IU                  up market: 1 if mktrf > 0 in month t
  var_m               variance of daily market returns, 126 days before month t (annualized)

Daily table (index = date): D1..D10, WML, mktrf, smb, hml, rf, mkt.
"""
import numpy as np
import pandas as pd

from config import PROCESSED, RAW


def _numeric(df, cols):
    return df[cols].apply(pd.to_numeric)


def ff_monthly():
    ff = pd.read_parquet(RAW / "ff" / "factors_monthly.parquet")
    ff.index = pd.PeriodIndex(pd.to_datetime(ff.date), freq="M", name="month")
    ff = _numeric(ff, ["mktrf", "smb", "hml", "rf"])
    ff["mkt"] = ff.mktrf + ff.rf
    # bear-market flag uses the full history so it exists from the first month
    ff["mkt24"] = np.exp(np.log1p(ff.mkt).rolling(24).sum().shift(1)) - 1
    ff["IB"] = (ff.mkt24 < 0).astype(float).where(ff.mkt24.notna())
    ff["IU"] = (ff.mktrf > 0).astype(float)
    return ff


def ff_daily():
    ff = pd.read_parquet(RAW / "ff" / "factors_daily.parquet")
    ff.index = pd.DatetimeIndex(pd.to_datetime(ff.date), name="date")
    ff = _numeric(ff, ["mktrf", "smb", "hml", "rf"])
    ff["mkt"] = ff.mktrf + ff.rf
    return ff


def past_126day_variance(daily_returns):
    """For each month t: annualized variance over the 126 trading days before month t."""
    var = daily_returns.rolling(126).var() * 252
    return var.groupby(var.index.to_period("M")).last().shift(1)


def decile_returns(freq, scheme):
    path = PROCESSED / f"{freq}_deciles_{scheme}.parquet"
    if not path.exists():
        return None
    df = pd.read_parquet(path).pivot(index="month" if freq == "monthly" else "date",
                                     columns="decile", values="ret")
    df.columns = [f"D{c}" for c in df.columns]
    df["WML"] = df.D10 - df.D1
    return df


def load(scheme):
    """Returns (monthly, daily, vol). daily / vol are None if not built yet."""
    market_daily = ff_daily()
    monthly = decile_returns("monthly", scheme).join(ff_monthly(), how="inner")
    monthly["var_m"] = past_126day_variance(market_daily.mkt).reindex(monthly.index)

    daily = decile_returns("daily", scheme)
    if daily is not None:
        daily = daily.join(market_daily, how="inner")

    vol_path = PROCESSED / f"wml_vol_{scheme}.parquet"
    vol = pd.read_parquet(vol_path).set_index("month") if vol_path.exists() else None
    return monthly, daily, vol
