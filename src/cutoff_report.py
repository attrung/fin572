"""Cutoff study, step 5: the replication's tables and figures for every cutoff, and a
comparison across cutoffs.

    python src/cutoff_report.py              both breakpoint versions
    python src/cutoff_report.py allfirm      one version

For each cutoff X (top / bottom X%) we rerun what report.py does for the deciles:
Tables 1-5, worst months, bull / bear states, the dynamic strategy (Figure 5 numbers and
Table 7), and Figures 1, 2, 3, 5, using the same functions. Only the portfolios change:
Table 1 / Table 4 show Losers, Winners and WML instead of D1 ... D10.

Output (results_quartile/):
  summary_<scheme>.md                      comparison across cutoffs, one table per period
  comparison_<scheme>.csv                  the same numbers in long format
  figs/<scheme>/*.png                      comparison figures (cumulative WML, Sharpe ratios)
  <scheme>/tables_<X>pct.md                full replication report for one cutoff
  <scheme>/table1_<X>pct_<start>_<end>.csv Table 1 for one cutoff and period
  <scheme>/strategies_<X>pct.csv           monthly WML / cvol / dyn returns for one cutoff
  figs/<scheme>/<X>pct/*.png               per-cutoff figures (as in results/figs/<scheme>)
"""
import sys
from functools import lru_cache

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import dynamic
import figures
import tables
from config import BASELINE_CUTOFF, CUTOFF_RESULTS, CUTOFFS, FULL, LAST_20, SAMPLES_CUTOFF, in_sample
from cutoff_portfolios import OUT, SCHEMES
from load_data import ff_daily, ff_monthly, past_126day_variance
from regression import ols
from report import NOTES, Markdown

PORTFOLIOS = ["Losers", "Winners"]
# periods in the comparison, in this order (the first two are the headline)
SUMMARY_SAMPLES = [FULL, LAST_20, "1960:01-2013:03 (paper overlap)", "2013:04-2025:12 (after the paper)"]

# Hand-written highlights at the top of summary_<scheme>.md.
# The numbers are typed in from the tables below them: update them if the results change.
HIGHLIGHTS = {
    "allfirm": [
        "**The dynamic strategy beats basic WML at every cutoff, in both periods.** dyn (OOS) Sharpe ratio, "
        "5% / 10% (baseline) / 20% / 30% / 40%: 1.30 / 1.08 / 0.93 / 0.83 / 0.68 (1972–2025), against 0.86 / 0.71 / "
        "0.50 / 0.48 / 0.38 for basic WML. That is 1.5–1.9× better, and the gain is largest for the wide cutoffs. "
        "Over 2006–2025: 0.92 / 0.67 / 0.56 / 0.48 / 0.39, against 0.51 / 0.33 / 0.11 / 0.16 / 0.06.",
        "**Narrower cutoffs are still the best base for the dynamic strategy.** dyn (OOS) FF3 alpha is 25.3%/yr "
        "(t = 9.7) at 5%, 21.4% (t = 8.2) at 10% and 13.4% (t = 5.1) at 40%. Over 2006–2025 it is 10.4% (t = 3.9), "
        "7.4% (t = 3.0) and 3.5% (t = 1.75, not significant).",
        "**Most of the crash risk goes away at every cutoff.** The dynamic strategy's worst month is −17.5% to −29% "
        "and its max drawdown −27% to −44%, against −28% to −68% and −48% to −87% for basic WML. Skewness turns "
        "positive (0.3 to 0.7). The 5% cutoff gains the most: its max drawdown goes from −86.9% to −31.1% (OOS).",
        "**dyn beats the constant-volatility benchmark mainly in the last 20 years.** Over 2006–2025 dyn (OOS) beats "
        "cvol at every cutoff (Sharpe ratio 0.92 vs 0.84 at 5%, 0.67 vs 0.59 at 10%, 0.39 vs 0.33 at 40%). Over the full "
        "period they roughly tie (1.08 vs 1.09 at 10%). The in-sample version beats cvol everywhere.",
        "**Basic WML: narrower legs pay more and crash harder.** Sharpe ratio 0.86 at 5% vs 0.71 at 10% vs 0.38 "
        "at 40% (0.51 / 0.33 / 0.06 over 2006–2025), mostly from the short leg (bottom 5%: −12.4%/yr). The worst month "
        "goes from −28.4% (40%) to −67.8% (5%, Jan 2001). The paper's bear-market beta drop holds at every cutoff "
        "(t from −6.4 to −7.4).",
    ],
    "nyse": [
        "**The dynamic strategy beats basic WML at every cutoff, in both periods.** dyn (OOS) Sharpe ratio, "
        "5% / 10% (baseline) / 20% / 30% / 40%: 1.09 / 1.00 / 0.78 / 0.69 / 0.62 (1972–2025), against 0.67 / 0.56 / "
        "0.45 / 0.36 / 0.32 for basic WML.",
        "**Since 2006, the dynamic strategy is what keeps momentum alive.** dyn (OOS) Sharpe ratio is 0.76 / 0.60 / "
        "0.47 / 0.41 / 0.36, while basic WML is 0.19 / 0.11 / 0.08 / −0.01 / −0.03. Its FF3 alpha is significant at "
        "5%, 10% and 20% (t = 3.35, 2.58, 2.13) but not at 30–40%. Basic WML has no significant alpha at any cutoff.",
        "**Most of the crash risk goes away at every cutoff.** The dynamic (OOS) strategy's worst month is −20% to "
        "−27% and its max drawdown −30% to −39%, against −25% to −52% and −47% to −90% for basic WML.",
        "**dyn beats the constant-volatility benchmark in the last 20 years.** Over 2006–2025 dyn (OOS) beats cvol "
        "at every cutoff (Sharpe ratio 0.76 vs 0.56 at 5%, 0.60 vs 0.44 at 10%, 0.36 vs 0.28 at 40%). Over the full "
        "period they roughly tie (1.00 vs 0.98 at 10%, 1.09 vs 1.13 at 5%).",
        "**Basic WML: the same ranking as allfirm, at lower levels.** Sharpe ratio 0.67 at 5% vs 0.56 at 10% vs 0.32 at "
        "40% over 1960–2025, with worst months from −25.5% (40%) to −51.9% (5%, Nov 2020). The 5% legs hold about "
        "390 stocks (allfirm: about 200), because small Nasdaq stocks pile up in the tails relative to NYSE cut-offs.",
    ],
}

# one blue ramp, darker = narrower (more extreme) legs; steps from the dataviz reference palette
SHADE = {5: "#0d366b", 10: "#1c5cab", 20: "#3987e5", 30: "#6da7ec", 40: "#86b6ef"}
FULL_COLOR, RECENT_COLOR = "#2a78d6", "#eb6834"


def name(pct):
    return f"{pct}% (baseline)" if pct == BASELINE_CUTOFF else f"{pct}%"


class QuietMarkdown(Markdown):
    """Same Markdown builder as report.py, without echoing every table to the console."""
    def text(self, s=""):
        self.lines.append(s)


# --------------------------------------------------------------------------- data

@lru_cache
def market():
    daily = ff_daily()
    monthly = ff_monthly()
    monthly["var_m"] = past_126day_variance(daily.mkt).reindex(monthly.index)
    return monthly, daily


def legs(freq, scheme, pct):
    """Losers, Winners, WML and the number of stocks in each leg (n_L, n_W)."""
    path = OUT / f"{freq}_legs_{scheme}.parquet"
    if not path.exists():
        return None
    time_col = "month" if freq == "monthly" else "date"
    df = pd.read_parquet(path).query("cutoff == @pct")
    wide = df.pivot(index=time_col, columns="leg", values="ret").rename(
        columns={"L": "Losers", "W": "Winners"})
    wide["WML"] = wide.Winners - wide.Losers
    n = df.pivot(index=time_col, columns="leg", values="n")
    wide["n_L"], wide["n_W"] = n.L, n.W
    return wide


def load(scheme, pct):
    """Like load_data.load: (monthly, daily, vol) for one cutoff."""
    market_monthly, market_daily = market()
    monthly = legs("monthly", scheme, pct).join(market_monthly, how="inner")
    daily = legs("daily", scheme, pct)
    if daily is not None:
        daily = daily.join(market_daily, how="inner")
    vol_path = OUT / f"wml_vol_{scheme}_{pct}.parquet"
    vol = pd.read_parquet(vol_path).set_index("month") if vol_path.exists() else None
    return monthly, daily, vol


# --------------------------------------------------------------------------- one cutoff

def cutoff_report(scheme, pct, monthly, daily, vol):
    """The replication report (report.py) for one cutoff. Returns the dynamic strategies."""
    folder = CUTOFF_RESULTS / scheme
    fig_folder = CUTOFF_RESULTS / "figs" / scheme / f"{pct}pct"
    fig_folder.mkdir(parents=True, exist_ok=True)
    leg_labels = ((f"Winners (top {pct}%)", "Winners"), (f"Losers (bottom {pct}%)", "Losers"))

    md = QuietMarkdown()
    md.text(f"# Momentum, top / bottom {pct}% ({scheme} breakpoints)"
            + (" — the baseline, identical to D10 − D1" if pct == BASELINE_CUTOFF else "") + "\n")
    md.text(f"Winners = top {pct}% of stocks on past return (t-12 to t-2), Losers = bottom {pct}%, "
            "WML = Winners − Losers. Everything else as in results/tables_<scheme>.md.\n")
    md.text(NOTES)

    for sample, (start, end) in SAMPLES_CUTOFF.items():
        m = in_sample(monthly, sample)
        md.text(f"\n## {sample}")
        stats = tables.portfolio_stats(m, daily, PORTFOLIOS)
        stats.to_csv(folder / f"table1_{pct}pct_{start}_{end}.csv")
        md.table(stats, "Table 1: momentum portfolios",
                 "mean, sd, alpha in %/year over the risk-free rate. sk = skewness of log returns.")
        md.table(m[["n_L", "n_W"]].mean().rename({"n_L": "Losers", "n_W": "Winners"}).to_frame("stocks").T,
                 "Average number of stocks per leg", floatfmt=".0f")
        md.table(tables.worst_months(m), "Table 2: worst 15 WML months (%)", floatfmt=".1f")
        md.table(tables.market_timing(m), "Table 3: market timing regressions")
        md.table(tables.optionality(m, "IB", PORTFOLIOS), "Table 4A: optionality in bear markets")
        md.table(tables.optionality(m, "IL", PORTFOLIOS), "Table 4B: optionality in bull markets")
        md.table(tables.forecasting(m), "Table 5: WML returns and market variance")
        md.table(tables.market_states(m), "Extra: WML in bull and bear markets")

    figures.deciles_over_time(monthly, fig_folder, legs=leg_labels)
    strategies = None
    if daily is not None:
        figures.crash_window(daily, "2009-03-01", "2009-05-31", fig_folder / "fig2a_crash_2009.png",
                             f"The 2009 momentum crash, top / bottom {pct}% (daily, Mar–May 2009)",
                             legs=leg_labels)
        figures.crash_window(daily, "2020-10-15", "2021-03-31", fig_folder / "fig2b_crash_2020.png",
                             f"The 2020 vaccine rally, top / bottom {pct}% (daily)", legs=leg_labels)
        figures.rolling_betas(daily, fig_folder, legs=leg_labels)

    if daily is not None and vol is not None:
        w, mean_fit, vol_fit = dynamic.weights(monthly, vol, FULL)
        strategies = dynamic.monthly_returns(w, monthly)
        strategies.to_csv(folder / f"strategies_{pct}pct.csv")

        md.text("\n## Dynamic strategy (Section 4)")
        mean_table, vol_table = dynamic.forecast_regressions(mean_fit, vol_fit)
        md.table(mean_table, "Expected return: WML on IB*var_m (const x100)")
        md.table(vol_table, "Expected volatility: realized WML vol on GARCH and 126-day vol (Appendix D)")
        for sample in SAMPLES_CUTOFF:
            md.table(dynamic.performance(strategies, monthly, sample), f"Figure 5 numbers, {sample}",
                     "cvol and dyn scaled to 19%/year volatility. OOS starts in 1970 and only uses past data.")
        daily_strategies = dynamic.daily_returns(w, daily)
        for dyn in ["dyn (IS)", "dyn (OOS)"]:
            panel_a, panel_b = dynamic.spanning(daily_strategies, daily, dyn)
            md.table(panel_a, f"Table 7A: alpha of {dyn} (daily regressions)")
            md.table(panel_b, f"Table 7B: alpha of cvol (daily regressions, using {dyn})")
        figures.strategies_over_time(strategies, fig_folder)

    md.save(folder / f"tables_{pct}pct.md")
    return strategies


# --------------------------------------------------------------------------- comparison

STRATEGIES = ["dyn (IS)", "dyn (OOS)", "cvol"]


def max_drawdown(r):
    wealth = (1 + r).cumprod()
    return (wealth / wealth.cummax() - 1).min() * 100


def comparison_stats(monthly, daily, strategies, sample):
    """The headline numbers for one cutoff and period, unformatted.
    Basic WML: Table 1, Table 3 (2), Table 5 (4). Dynamic: Figure 5 numbers (dynamic.performance)."""
    m = in_sample(monthly, sample)
    capm = ols(m.WML, m.mktrf)
    timing = ols(m.WML, pd.DataFrame({"IB": m.IB, "Rm": m.mktrf, "IB*Rm": m.IB * m.mktrf}))
    forecast = ols(m.WML, (m.IB * m.var_m).rename("IB*var_m"))
    s = {
        "stocks_per_leg": (m.n_L.mean() + m.n_W.mean()) / 2,
        "winners_mean": (m.Winners - m.rf).mean() * 1200,
        "losers_mean": (m.Losers - m.rf).mean() * 1200,
        "wml_mean": m.WML.mean() * 1200,
        "wml_sd": m.WML.std() * np.sqrt(12) * 100,
        "wml_sharpe": m.WML.mean() / m.WML.std() * np.sqrt(12),
        "capm_alpha": capm.params["const"] * 1200, "capm_alpha_t": capm.tvalues["const"],
        "capm_beta": capm.params["mktrf"],
        "skew_monthly": np.log1p(m.WML + m.rf).skew(),
        "worst_month": m.WML.min() * 100, "worst_month_date": str(m.WML.idxmin()),
        "max_drawdown": max_drawdown(m.WML),
        "bear_beta_change": timing.params["IB*Rm"], "bear_beta_change_t": timing.tvalues["IB*Rm"],
        "bear_x_variance": forecast.params["IB*var_m"], "bear_x_variance_t": forecast.tvalues["IB*var_m"],
    }
    if daily is not None:
        d = daily.loc[m.index[0].start_time:m.index[-1].end_time]
        s["skew_daily"] = np.log1p(d.WML + d.rf).skew()
    if strategies is not None:
        perf = dynamic.performance(strategies, monthly, sample)
        for strat in STRATEGIES:
            r = in_sample(strategies[strat], sample).dropna()
            s.update({
                f"{strat}: months": perf.at["months", strat],
                f"{strat}: mean": perf.at["mean (%/yr)", strat],
                f"{strat}: sd": perf.at["sd (%/yr)", strat],
                f"{strat}: sharpe": perf.at["Sharpe ratio", strat],
                f"{strat}: skew": perf.at["skew (monthly)", strat],
                f"{strat}: worst_month": perf.at["worst month (%)", strat],
                f"{strat}: worst_month_date": str(r.idxmin()),
                f"{strat}: max_drawdown": max_drawdown(r),
                f"{strat}: ff3_alpha": perf.at["FF3 alpha (%/yr)", strat],
                f"{strat}: ff3_alpha_t": perf.at["t(alpha)", strat],
            })
    return s


def _num(key, digits=2):
    return lambda s: f"{s[key]:.{digits}f}"


def _coef(key, digits=2):
    return lambda s: f"{s[key]:.{digits}f} [{s[key + '_t']:.2f}]"


def _worst(key):
    return lambda s: f"{s[key]:.1f} ({s[key + '_date']})"


BASIC_ROWS = [
    ("Stocks per leg (avg)", _num("stocks_per_leg", 0)),
    ("Winners mean (%/yr)", _num("winners_mean")),
    ("Losers mean (%/yr)", _num("losers_mean")),
    ("WML mean (%/yr)", _num("wml_mean")),
    ("WML sd (%/yr)", _num("wml_sd")),
    ("WML Sharpe ratio", _num("wml_sharpe")),
    ("CAPM alpha (%/yr) [t]", _coef("capm_alpha")),
    ("CAPM beta", _num("capm_beta")),
    ("Skewness, monthly (log)", _num("skew_monthly")),
    ("Skewness, daily (log)", _num("skew_daily")),
    ("Worst month (%)", _worst("worst_month")),
    ("Max drawdown (%)", _num("max_drawdown", 1)),
    ("Bear-market beta change, T3 (2) [t]", _coef("bear_beta_change", 3)),
    ("Bear x variance, T5 (4) [t]", _coef("bear_x_variance", 3)),
]
DYNAMIC_ROWS = [
    ("Sharpe ratio, dyn (IS)", _num("dyn (IS): sharpe")),
    ("Sharpe ratio, dyn (OOS)", _num("dyn (OOS): sharpe")),
    ("Sharpe ratio, cvol (benchmark)", _num("cvol: sharpe")),
    ("Mean (%/yr), dyn (IS)", _num("dyn (IS): mean")),
    ("Mean (%/yr), dyn (OOS)", _num("dyn (OOS): mean")),
    ("sd (%/yr), dyn (IS)", _num("dyn (IS): sd")),
    ("sd (%/yr), dyn (OOS)", _num("dyn (OOS): sd")),
    ("FF3 alpha (%/yr) [t], dyn (IS)", _coef("dyn (IS): ff3_alpha")),
    ("FF3 alpha (%/yr) [t], dyn (OOS)", _coef("dyn (OOS): ff3_alpha")),
    ("Skewness, monthly, dyn (IS)", _num("dyn (IS): skew")),
    ("Skewness, monthly, dyn (OOS)", _num("dyn (OOS): skew")),
    ("Worst month (%), dyn (IS)", _worst("dyn (IS): worst_month")),
    ("Worst month (%), dyn (OOS)", _worst("dyn (OOS): worst_month")),
    ("Worst month (%), cvol (benchmark)", _worst("cvol: worst_month")),
    ("Max drawdown (%), dyn (IS)", _num("dyn (IS): max_drawdown", 1)),
    ("Max drawdown (%), dyn (OOS)", _num("dyn (OOS): max_drawdown", 1)),
]


def comparison_table(stats_by_cutoff):
    """Strategy | Statistic | one column per cutoff. The strategy name is shown on its first row."""
    rows = []
    for group, specs in [("**Basic WML**", BASIC_ROWS), ("**Dynamic strategy**", DYNAMIC_ROWS)]:
        for i, (label, fmt) in enumerate(specs):
            row = {"Strategy": group if i == 0 else "", "Statistic": label}
            for col, s in stats_by_cutoff.items():
                try:
                    row[col] = fmt(s)
                except KeyError:          # no daily data / no dynamic strategy
                    row[col] = ""
            rows.append(row)
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- figures

# red ramp for the dynamic strategy, darker = narrower legs (built around the palette's red, #e34948)
RED = {5: "#7a1b1b", 10: "#b02a2a", 20: "#e34948", 30: "#ec7a79", 40: "#f09c9b"}


def cumulative_by_cutoff(wml, sample, path, title, target_vol=None):
    """Running performance of WML for every cutoff: cumulative log return."""
    fig, ax = figures._new_figure(title, "Cumulative log return")
    for pct, r in wml.items():
        r = in_sample(r, sample).dropna()
        if target_vol:
            r = dynamic.scale_to_vol(r, target_vol, 12)
        sharpe = r.mean() / r.std() * np.sqrt(12)
        ax.plot(r.index.to_timestamp(), figures.cumulative(r), color=SHADE[pct],
                lw=2.6 if pct == BASELINE_CUTOFF else 1.6, label=f"{name(pct)}  (SR {sharpe:.2f})",
                zorder=3 if pct == BASELINE_CUTOFF else 2)
    ax.axhline(0, color=figures.GREY, lw=0.8)
    figures._save(fig, ax, path)


def dynamic_by_cutoff(strategies, baseline_wml, which, sample, path, title):
    """Running performance of the dynamic strategy for every cutoff (reds), with the basic
    10% WML for reference. All scaled to 19% vol over 1960-2025, as in Figure 5."""
    fig, ax = figures._new_figure(title, "Cumulative log return")
    start = None
    for pct, strat in strategies.items():
        r = in_sample(strat[which], sample).dropna()
        start = r.index[0] if start is None else min(start, r.index[0])
        sharpe = r.mean() / r.std() * np.sqrt(12)
        ax.plot(r.index.to_timestamp(), figures.cumulative(r), color=RED[pct],
                lw=2.6 if pct == BASELINE_CUTOFF else 1.6,
                label=f"{which}, {name(pct)}  (SR {sharpe:.2f})",
                zorder=3 if pct == BASELINE_CUTOFF else 2)
    wml = dynamic.scale_to_vol(in_sample(baseline_wml, FULL), dynamic.PERFORMANCE_VOL, 12)
    wml = in_sample(wml, sample).loc[start:]        # same start as the dynamic lines
    sharpe = wml.mean() / wml.std() * np.sqrt(12)
    ax.plot(wml.index.to_timestamp(), figures.cumulative(wml), color=figures.GREY, lw=2, ls="--",
            label=f"Basic WML, {name(BASELINE_CUTOFF)}  (SR {sharpe:.2f})", zorder=4)
    ax.axhline(0, color=figures.GREY, lw=0.8)
    figures._save(fig, ax, path)


def sharpe_by_cutoff(wml, path, title):
    """WML Sharpe ratio by cutoff: full period vs the last 20 years."""
    fig, ax = figures._new_figure(title, "Sharpe ratio (annualized)")
    x = np.arange(len(wml))
    width = 0.36
    for i, (sample, color, label) in enumerate([(FULL, FULL_COLOR, "1960–2025"),
                                                (LAST_20, RECENT_COLOR, "2006–2025 (last 20 years)")]):
        sr = [in_sample(r, sample).mean() / in_sample(r, sample).std() * np.sqrt(12) for r in wml.values()]
        bars = ax.bar(x + (i - 0.5) * width, sr, width * 0.92, color=color, label=label)
        ax.bar_label(bars, fmt="%.2f", fontsize=8, color=figures.INK, padding=2)
    ax.set_xticks(x, [name(p) for p in wml])
    ax.axhline(0, color=figures.GREY, lw=0.8)
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, fontsize=9, loc="upper right")   # tallest bars are on the left
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def comparison_figures(scheme, wml, strategies):
    folder = CUTOFF_RESULTS / "figs" / scheme
    label = f"{scheme} breakpoints"
    cumulative_by_cutoff(wml, FULL, folder / "wml_cumulative_1960-2025.png",
                         f"WML by cutoff, 1960–2025 ({label})")
    cumulative_by_cutoff(wml, FULL, folder / "wml_cumulative_1960-2025_19vol.png",
                         f"WML by cutoff, each scaled to 19% vol, 1960–2025 ({label})", 0.19)
    cumulative_by_cutoff(wml, LAST_20, folder / "wml_cumulative_2006-2025.png",
                         f"WML by cutoff, last 20 years, 2006–2025 ({label})")
    cumulative_by_cutoff(wml, LAST_20, folder / "wml_cumulative_2006-2025_19vol.png",
                         f"WML by cutoff, each scaled to 19% vol, 2006–2025 ({label})", 0.19)
    sharpe_by_cutoff(wml, folder / "wml_sharpe_by_cutoff.png",
                     f"WML Sharpe ratio by cutoff ({label})")
    if len(strategies) == len(wml):          # dynamic strategy built for every cutoff
        baseline = wml[BASELINE_CUTOFF]
        for which, tag in [("dyn (IS)", "dyn_is"), ("dyn (OOS)", "dyn_oos")]:
            first = in_sample(strategies[BASELINE_CUTOFF][which], FULL).first_valid_index().year
            dynamic_by_cutoff(strategies, baseline, which, FULL,
                              folder / f"{tag}_cumulative_{first}-2025.png",
                              f"Dynamic strategy {which} by cutoff, {first}–2025 ({label}, 19% vol)")
            dynamic_by_cutoff(strategies, baseline, which, LAST_20,
                              folder / f"{tag}_cumulative_2006-2025.png",
                              f"Dynamic strategy {which} by cutoff, 2006–2025 ({label}, 19% vol)")


# --------------------------------------------------------------------------- main

INTRO = """Long the top X% of stocks on past return (t-12 to t-2), short the bottom X%. Same stocks, \
signal, value weights and monthly rebalancing as the replication; only the cutoff changes. 10% is the \
paper's D10 − D1 (the baseline in results/tables_{scheme}.md).

- **Basic WML**: the plain long-short portfolio (paper Tables 1, 3, 5). Means, sd and alphas in %/year; \
[t-stats] in brackets. Skewness is of log returns. Max drawdown compounds monthly returns. T3 (2) = Table 3 \
column (2), the change in WML's market beta in bear markets; T5 (4) = Table 5 column (4), WML on bear flag \
x market variance.
- **Dynamic strategy**: the paper's Section 4 strategy built on each cutoff's WML: weight = forecast mean / \
forecast variance (GJR-GARCH). dyn (IS) fits the forecasts on the full sample, as in the paper; dyn (OOS) \
only uses past data (GARCH re-fits from 1970, first weight in 1972, so its "full" period is 1972–2025). cvol (constant volatility, weight = 1 / past vol) is the paper's \
benchmark. All are scaled to 19%/year volatility over 1960–2025 (Figure 5), so sd is exactly 19 only in the \
full period. Skewness is of simple monthly returns (as in Figure 5); alpha is the Fama-French 3-factor alpha."""


def main(schemes=SCHEMES):
    for scheme in schemes:
        (CUTOFF_RESULTS / scheme).mkdir(parents=True, exist_ok=True)
        stats = {sample: {} for sample in SUMMARY_SAMPLES}
        rows, wml, strategies = [], {}, {}
        for pct in CUTOFFS:
            monthly, daily, vol = load(scheme, pct)
            strat = cutoff_report(scheme, pct, monthly, daily, vol)
            wml[pct] = monthly.WML
            if strat is not None:
                strategies[pct] = strat
            for sample in SUMMARY_SAMPLES:
                s = comparison_stats(monthly, daily, strat, sample)
                stats[sample][name(pct)] = s
                rows.append({"scheme": scheme, "sample": sample, "cutoff": pct, **s})
            print(scheme, pct, "done", flush=True)

        pd.DataFrame(rows).to_csv(CUTOFF_RESULTS / f"comparison_{scheme}.csv", index=False)
        comparison_figures(scheme, wml, strategies)

        md = Markdown()
        md.text(f"# Momentum by cutoff: top / bottom X% ({scheme} breakpoints)\n")
        md.text("## Highlights\n")
        for point in HIGHLIGHTS[scheme]:
            md.text(f"- {point}")
        md.text("\n## Tables\n")
        md.text(INTRO.format(scheme=scheme))
        for sample in SUMMARY_SAMPLES:
            md.text(f"\n### {sample}\n")
            md.text(comparison_table(stats[sample]).to_markdown(index=False))
        md.save(CUTOFF_RESULTS / f"summary_{scheme}.md")


if __name__ == "__main__":
    main(sys.argv[1:] or SCHEMES)
