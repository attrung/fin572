"""Figures. Each function saves one PNG into the folder it is given (results/figs/<scheme>)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.regression.rolling import RollingOLS

from config import FULL, in_sample

# fixed colors, same meaning in every figure
WINNERS, LOSERS, MARKET, WML = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
GREY, INK, GRID = "#52514e", "#0b0b0b", "#e4e3df"


def _new_figure(title, ylabel):
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.set_title(title, loc="left", fontsize=12)
    ax.set_ylabel(ylabel, color=GREY)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.tick_params(colors=GREY, labelsize=9)
    return fig, ax


def _save(fig, ax, path):
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def cumulative(returns):
    return np.log1p(returns).cumsum()


# (label, column) of the long and short legs; the cutoff study passes its own
DECILE_LEGS = (("Winners (D10)", "D10"), ("Losers (D1)", "D1"))


def _legs(legs):
    (w_label, w_col), (l_label, l_col) = legs
    return [(w_label, w_col, WINNERS), (l_label, l_col, LOSERS)]


def deciles_over_time(monthly, folder, legs=DECILE_LEGS):
    """Figure 1: winners vs losers vs the market."""
    m = in_sample(monthly, FULL)
    dates = m.index.to_timestamp()
    fig, ax = _new_figure(f"Winners, losers and the market, {dates[0].year}–{dates[-1].year}",
                          "Cumulative log return")
    for label, col, color in _legs(legs) + [("Market", "mkt", MARKET), ("Risk-free", "rf", GREY)]:
        y = cumulative(m[col])
        ax.plot(dates, y, color=color, lw=2, label=label)
        ax.annotate(label, (dates[-1], y.iloc[-1]), xytext=(4, 0), textcoords="offset points",
                    fontsize=9, color=INK, va="center")
    ax.set_xlim(dates[0], dates[-1] + pd.Timedelta(days=365 * 7))
    _save(fig, ax, folder / "fig1_cumulative_deciles.png")


def crash_window(daily, start, end, path, title, legs=DECILE_LEGS):
    """Figure 2: daily returns through a momentum crash."""
    d = daily.loc[start:end]
    fig, ax = _new_figure(title, "Cumulative log return")
    for label, col, color in _legs(legs) + [("Market", "mkt", MARKET), ("WML", "WML", WML)]:
        ax.plot(d.index, cumulative(d[col]), color=color, lw=2, label=label)
    ax.axhline(0, color=GREY, lw=0.8)
    fig.autofmt_xdate()
    _save(fig, ax, path)


def market_beta_with_lags(excess, mktrf, window=126, lags=10):
    """Paper footnote 2: rolling regression on the market and 10 daily lags; beta = sum of slopes."""
    X = pd.concat({f"lag{k}": mktrf.shift(k) for k in range(lags + 1)}, axis=1)
    X.insert(0, "const", 1.0)
    fit = RollingOLS(excess, X, window=window, missing="drop").fit(params_only=True)
    return fit.params.drop(columns="const").sum(axis=1, min_count=1)


def rolling_betas(daily, folder, legs=DECILE_LEGS):
    """Figure 3: market betas of winners and losers over time (126-day window, 10 lags)."""
    d = daily.loc["1960":]
    fig, ax = _new_figure("Market betas of winners and losers (126 days, 10 daily lags)",
                          "Market beta")
    for label, col, color in _legs(legs):
        beta = market_beta_with_lags(d[col] - d.rf, d.mktrf)
        ax.plot(beta.index, beta, color=color, lw=1.2, label=label)
    ax.axhline(1, color=GREY, lw=0.8)
    _save(fig, ax, folder / "fig3_rolling_betas.png")


def strategies_over_time(strategies, folder):
    """Figure 5: plain vs constant-vol vs dynamic momentum, Sharpe ratios in the legend."""
    fig, ax = _new_figure("Plain, constant-volatility and dynamic momentum (19% vol)",
                          "Cumulative log return")
    for name, color in [("WML", GREY), ("cvol", MARKET), ("dyn (IS)", WINNERS), ("dyn (OOS)", LOSERS)]:
        r = strategies[name].dropna()
        sharpe = r.mean() / r.std() * np.sqrt(12)
        ax.plot(r.index.to_timestamp(), cumulative(r), color=color, lw=2,
                label=f"{name} (SR {sharpe:.2f})")
    _save(fig, ax, folder / "fig5_dynamic_strategies.png")
