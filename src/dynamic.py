"""The paper's dynamic momentum strategy (Section 4, Figure 5, Table 7).

Each month t we hold w units of WML, set at the end of month t-1 (eq. 5):
    w  ∝  expected WML return / expected WML variance
  * expected return: fitted value from Table 5, column (4): WML on IB*var_m
  * expected volatility: fitted value from regressing realized WML volatility on the
    GJR-GARCH forecast and the past 126-day volatility (Appendix D)
We compare it with:
  * WML     the plain strategy (w = 1)
  * cvol    constant volatility (Barroso & Santa-Clara): w = 1 / past 126-day volatility

In-sample (IS): forecasting regressions use the full sample, as in the paper.
Out-of-sample (OOS): our extra check. Regressions and GARCH only use data before month t.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import FULL, in_sample
from regression import ols, regression_table

PERFORMANCE_VOL = 0.19   # Figure 5: scale to 19%/year (the market's volatility)


# --------------------------------------------------------------------------- weights

def fitted(fit, X):
    return fit.predict(sm.add_constant(X, has_constant="add"))


def out_of_sample_forecasts(df):
    """Expanding-window forecasts of WML mean and volatility, using data before month t only."""
    mean = pd.Series(np.nan, index=df.index)
    vol = pd.Series(np.nan, index=df.index)
    for t in df.index[df.garch_oos.notna()]:
        past = df.loc[:t - 1]
        a = ols(past.WML, past[["IB*var_m"]]).params
        mean[t] = a["const"] + a["IB*var_m"] * df.at[t, "IB*var_m"]

        past = past.dropna(subset=["garch_oos", "rv126", "rv_next"])
        if len(past) >= 24:
            b = ols(past.rv_next, past[["garch_oos", "rv126"]]).params
            vol[t] = b["const"] + b["garch_oos"] * df.at[t, "garch_oos"] + b["rv126"] * df.at[t, "rv126"]
    return mean, vol


def weights(monthly, vol):
    """Monthly WML weights for cvol, dyn (IS) and dyn (OOS), plus the IS regressions."""
    df = in_sample(monthly.join(vol, how="inner"), FULL).copy()
    df["IB*var_m"] = df.IB * df.var_m

    mean_fit = ols(df.WML, df[["IB*var_m"]])
    vol_fit = ols(df.rv_next, df[["garch_is", "rv126"]])
    mean_oos, vol_oos = out_of_sample_forecasts(df)

    w = pd.DataFrame({
        "WML": 1.0,
        "cvol": 1 / df.rv126,
        "dyn (IS)": fitted(mean_fit, df[["IB*var_m"]]) / fitted(vol_fit, df[["garch_is", "rv126"]]) ** 2,
        "dyn (OOS)": mean_oos / vol_oos ** 2,
    }, index=df.index)
    return w, mean_fit, vol_fit


# --------------------------------------------------------------------------- returns

def scale_to_vol(returns, target, periods_per_year):
    """Multiply each column by a constant so its volatility equals target."""
    return returns * target / (returns.std() * np.sqrt(periods_per_year))


def monthly_returns(w, monthly):
    """Strategy returns; cvol and dyn scaled to 19%/year, plain WML left as is."""
    r = w.mul(monthly.WML.loc[w.index], axis=0)
    scaled = r.columns != "WML"
    r.loc[:, scaled] = scale_to_vol(r.loc[:, scaled], PERFORMANCE_VOL, 12)
    return r


def daily_returns(w, daily):
    """The month's weight times each day's WML return. Scaled to WML's own volatility (Table 7)."""
    d = daily.loc[w.index[0].start_time:w.index[-1].end_time]
    w_daily = w.reindex(d.index.to_period("M")).set_axis(d.index)
    r = w_daily.mul(d.WML, axis=0)
    return scale_to_vol(r, d.WML.std() * np.sqrt(252), 252)


# --------------------------------------------------------------------------- tables

def performance(strategies, monthly, sample):
    """Figure 5 numbers: mean, volatility, Sharpe ratio, skewness, worst month, FF3 alpha."""
    rows = {}
    for name, r in in_sample(strategies, sample).items():
        r = r.dropna()
        if len(r) < 12:
            continue
        ff3 = ols(r, monthly.loc[r.index, ["mktrf", "smb", "hml"]])
        rows[name] = {
            "months": len(r),
            "mean (%/yr)": r.mean() * 1200,
            "sd (%/yr)": r.std() * np.sqrt(12) * 100,
            "Sharpe ratio": r.mean() / r.std() * np.sqrt(12),
            "skew (monthly)": r.skew(),
            "worst month (%)": r.min() * 100,
            "FF3 alpha (%/yr)": ff3.params["const"] * 1200,
            "t(alpha)": ff3.tvalues["const"],
        }
    return pd.DataFrame(rows)


def spanning(daily_strategies, daily, dyn):
    """Table 7 (unconditional columns 1, 3, 4, 6): daily regressions, alpha in %/year.
    Panel A: is dyn explained by WML or cvol (plus market or FF3)?
    Panel B: is cvol explained by WML or dyn?"""
    ff = ["mktrf", "smb", "hml"]
    x = daily_strategies[["WML", "cvol", dyn]].join(daily[ff]).dropna()

    def alphas(y, models):
        fits = {name: ols(x[y], x[cols]) for name, cols in models.items()}
        t = regression_table(fits, ["const"], scale={"const": 252 * 100})
        t.index = ["alpha (%/yr)", "R2 (%)", "N"]
        return t

    panel_a = alphas(dyn, {"Mkt+WML": ["mktrf", "WML"], "FF+WML": ff + ["WML"],
                           "Mkt+cvol": ["mktrf", "cvol"], "FF+cvol": ff + ["cvol"]})
    panel_b = alphas("cvol", {"Mkt+WML": ["mktrf", "WML"], "FF+WML": ff + ["WML"],
                              "Mkt+dyn": ["mktrf", dyn], "FF+dyn": ff + [dyn]})
    return panel_a, panel_b


def forecast_regressions(mean_fit, vol_fit):
    """The two in-sample regressions behind the dynamic weights."""
    mean_table = regression_table({"WML": mean_fit}, ["const", "IB*var_m"], scale={"const": 100})
    vol_table = regression_table({"realized vol": vol_fit}, ["const", "garch_is", "rv126"])
    return mean_table, vol_table
