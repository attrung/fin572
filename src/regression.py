"""Small helpers for OLS regressions and paper-style regression tables."""
import pandas as pd
import statsmodels.api as sm


def ols(y, X):
    """OLS with a constant; rows with missing values are dropped."""
    return sm.OLS(y, sm.add_constant(X, has_constant="add"), missing="drop").fit()


def regression_table(fits, variables, scale=None):
    """One column per regression: 'coef [t-stat]', then R2 and N.
    scale multiplies a coefficient, e.g. {"const": 1200} turns monthly into %/year."""
    scale = scale or {}
    columns = {}
    for name, fit in fits.items():
        col = {v: f"{fit.params[v] * scale.get(v, 1):.3f} [{fit.tvalues[v]:.2f}]"
               if v in fit.params else "" for v in variables}
        col["R2 (%)"] = f"{fit.rsquared * 100:.1f}"
        col["N"] = str(int(fit.nobs))
        columns[name] = col
    return pd.DataFrame(columns)
