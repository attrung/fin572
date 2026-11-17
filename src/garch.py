"""Step 4: forecast next month's WML volatility (needed for the dynamic strategy).

    python src/garch.py allfirm 1970-01

For each holding month t, using daily WML returns up to the end of month t-1:
  rv126      realized volatility over the last 126 trading days
  garch_is   GJR-GARCH(1,1) forecast, model fitted once on the full sample (in-sample)
  garch_oos  same, but the model is re-fitted each month on past data only (out-of-sample),
             starting at the month given on the command line
  rv_next    realized volatility inside month t (what we try to forecast)

All volatilities are monthly (square root of the sum of 22 daily variances).
The out-of-sample part fits ~670 models, so run this as a Slurm job.

Output: data/processed/wml_vol_<scheme>.parquet
"""
import os
import sys
from multiprocessing import Pool

import numpy as np
import pandas as pd
from arch import arch_model

from config import PROCESSED

DAYS_PER_MONTH = 22
PERCENT = 100.0   # GARCH is fitted on returns in percent (more stable numerically)


def daily_wml(scheme):
    d = pd.read_parquet(PROCESSED / f"daily_deciles_{scheme}.parquet")
    d = d.pivot(index="date", columns="decile", values="ret")
    return (d[10] - d[1]).dropna()


def fit_gjr_garch(returns):
    model = arch_model(returns * PERCENT, mean="Constant", vol="GARCH", p=1, o=1, q=1)
    return model.fit(disp="off")


def monthly_vol_forecast(fit, start=None):
    """Forecast of volatility over the next 22 trading days, from each date on."""
    f = fit.forecast(horizon=DAYS_PER_MONTH, start=start, reindex=False)
    return np.sqrt(f.variance.sum(axis=1)) / PERCENT


def forecast_with_data_up_to(args):
    returns, last_day = args
    fit = fit_gjr_garch(returns.loc[:last_day])
    return last_day, float(monthly_vol_forecast(fit).iloc[-1])


def main(scheme="allfirm", oos_start="1970-01"):
    wml = daily_wml(scheme)
    month = wml.index.to_period("M")
    month_end = wml.groupby(month).apply(lambda s: s.index[-1])   # last trading day per month

    out = pd.DataFrame(index=pd.PeriodIndex(month_end.index + 1, name="month"))
    out["rv126"] = (np.sqrt((wml ** 2).rolling(126).mean() * DAYS_PER_MONTH)
                    .reindex(month_end.values).values)
    out["rv_next"] = np.sqrt((wml ** 2).groupby(month).sum()).reindex(out.index).values

    full_fit = fit_gjr_garch(wml)
    print(full_fit.summary(), flush=True)
    out["garch_is"] = monthly_vol_forecast(full_fit, start=wml.index[0]).reindex(month_end.values).values

    oos_days = [day for m, day in month_end.items() if m + 1 >= pd.Period(oos_start, "M")]
    workers = int(os.environ.get("SLURM_CPUS_PER_TASK", 4))
    with Pool(workers) as pool:
        oos = dict(pool.map(forecast_with_data_up_to, [(wml, day) for day in oos_days], chunksize=4))
    out["garch_oos"] = [oos.get(day, np.nan) for day in month_end.values]

    out.reset_index().to_parquet(PROCESSED / f"wml_vol_{scheme}.parquet", index=False)
    print(out.dropna().describe(), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
