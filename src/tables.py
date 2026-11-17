"""The paper's main tables (Tables 1-5). Each function takes the monthly table for one
sample period and returns a DataFrame laid out like the paper's table."""
import numpy as np
import pandas as pd

from regression import ols, regression_table

DECILES = [f"D{i}" for i in range(1, 11)]
PERCENT_PER_MONTH = 100     # paper reports intercepts "x100", i.e. in %/month


def portfolio_stats(m, daily=None):
    """Table 1: mean, volatility, CAPM alpha and beta, Sharpe ratio, skewness.
    Mean, sd and alpha are in %/year, in excess of the risk-free rate."""
    rows = {}
    for name in DECILES + ["WML", "Mkt"]:
        if name == "Mkt":
            excess, total = m.mktrf, m.mkt
        elif name == "WML":                  # long-short, already an excess return
            excess, total = m.WML, m.WML + m.rf
        else:
            excess, total = m[name] - m.rf, m[name]

        capm = ols(excess, m.mktrf)
        row = {
            "mean": excess.mean() * 1200,
            "sd": excess.std() * np.sqrt(12) * 100,
            "alpha": capm.params["const"] * 1200 if name != "Mkt" else np.nan,
            "t(alpha)": capm.tvalues["const"] if name != "Mkt" else np.nan,
            "beta": capm.params["mktrf"],
            "SR": excess.mean() / excess.std() * np.sqrt(12),
            "sk(m)": np.log1p(total).skew(),           # skewness of monthly log returns
        }
        if daily is not None:
            d = daily.loc[m.index[0].start_time:m.index[-1].end_time]
            d_total = {"Mkt": d.mkt, "WML": d.WML + d.rf}.get(name, d.get(name))
            row["sk(d)"] = np.log1p(d_total).skew()     # skewness of daily log returns
        rows[name] = row
    return pd.DataFrame(rows)


def worst_months(m, k=15):
    """Table 2: the k worst WML months, with the market before and during."""
    out = m.nsmallest(k, "WML")[["WML", "mkt24", "mkt"]] * 100
    out.columns = ["WML", "Mkt-2y", "Mkt (same month)"]
    out.index = out.index.astype(str)
    return out


def _timing_variables(m, state):
    """Right-hand side of eq. (3) for a market state (IB = bear, IL = bull = 1 - IB)."""
    s = m.IB if state == "IB" else 1 - m.IB
    return pd.DataFrame({state: s, "Rm": m.mktrf, f"{state}*Rm": s * m.mktrf,
                         f"{state}*IU*Rm": s * m.IU * m.mktrf})


def market_timing(m):
    """Table 3: WML on the market, letting beta change in bear markets (eqs. 1-3).
    alpha_0 and alpha_B are in %/month."""
    X = _timing_variables(m, "IB")
    specs = {"(1)": ["Rm"],
             "(2)": ["IB", "Rm", "IB*Rm"],
             "(3)": ["Rm", "IB*Rm", "IB*IU*Rm"],
             "(4)": ["IB", "Rm", "IB*Rm", "IB*IU*Rm"]}
    fits = {name: ols(m.WML, X[cols]) for name, cols in specs.items()}
    table = regression_table(fits, ["const", "IB", "Rm", "IB*Rm", "IB*IU*Rm"],
                             scale={"const": PERCENT_PER_MONTH, "IB": PERCENT_PER_MONTH})
    table.index = ["alpha_0", "alpha_B", "beta_0", "beta_B", "beta_BU", "R2 (%)", "N"]
    return table


def optionality(m, state="IB"):
    """Table 4: eq. (3) for every decile and WML.
    Panel A uses the bear-market flag IB, Panel B the bull-market flag IL = 1 - IB."""
    X = _timing_variables(m, state)
    fits = {}
    for name in DECILES + ["WML"]:
        y = m.WML if name == "WML" else m[name] - m.rf
        fits[name.replace("D", "")] = ols(y, X)
    table = regression_table(fits, ["const", state, "Rm", f"{state}*Rm", f"{state}*IU*Rm"],
                             scale={"const": PERCENT_PER_MONTH, state: PERCENT_PER_MONTH})
    s = state[1]   # "B" or "L"
    table.index = ["alpha_0", f"alpha_{s}", "beta_0", f"beta_{s}", f"beta_{s}U", "R2 (%)", "N"]
    return table


def market_states(m):
    """Extra: average WML return and beta in bull markets, bear markets, and rebounds."""
    states = {
        "Bull (IB=0)": m.IB == 0,
        "Bear (IB=1)": m.IB == 1,
        "Bear, market up": (m.IB == 1) & (m.IU == 1),
        "Bear, market down": (m.IB == 1) & (m.IU == 0),
    }
    rows = {}
    for name, mask in states.items():
        x = m[mask]
        rows[name] = {
            "months": len(x),
            "WML mean (%/mo)": x.WML.mean() * 100,
            "WML sd (%/mo)": x.WML.std() * 100,
            "Market mean (%/mo)": x.mktrf.mean() * 100,
            "WML beta": ols(x.WML, x.mktrf).params["mktrf"] if len(x) > 5 else np.nan,
        }
    return pd.DataFrame(rows).T


def forecasting(m):
    """Table 5: predict WML with the bear flag and past market variance (eq. 4).
    gamma_0 and gamma_B in %/month; var_m is annualized, as a decimal."""
    X = pd.DataFrame({"IB": m.IB, "var_m": m.var_m, "IB*var_m": m.IB * m.var_m})
    specs = {"(1)": ["IB"], "(2)": ["var_m"], "(3)": ["IB", "var_m"],
             "(4)": ["IB*var_m"], "(5)": ["IB", "var_m", "IB*var_m"]}
    fits = {name: ols(m.WML, X[cols]) for name, cols in specs.items()}
    table = regression_table(fits, ["const", "IB", "var_m", "IB*var_m"],
                             scale={"const": PERCENT_PER_MONTH, "IB": PERCENT_PER_MONTH})
    table.index = ["gamma_0", "gamma_B", "gamma_var", "gamma_int", "R2 (%)", "N"]
    return table
