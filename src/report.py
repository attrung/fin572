"""Step 5: make all tables and figures.

    python src/report.py allfirm      (the paper's version)
    python src/report.py nyse
    python src/report.py dm           (Daniel's published portfolios, ends 2016-12)

Output: results/tables_<scheme>.md, results/*.csv, results/figs/<scheme>/*.png
"""
import sys

import pandas as pd

import dynamic
import figures
import tables
from config import FIGURES, FULL, PAPER, RESULTS, SAMPLES, SAMPLES_FOR_DM, in_sample
from load_data import load

NOTES = """Numbers in [brackets] are t-stats. "x100" coefficients are in % per month.
IB = 1 if the market fell over the past 24 months (bear market). IU = 1 if the market is up this month.
Rm = market excess return. var_m = variance of daily market returns over the past 126 days (annualized)."""


class Markdown:
    def __init__(self):
        self.lines = []

    def text(self, s=""):
        print(s)
        self.lines.append(s)

    def table(self, df, title, note=None, floatfmt=".2f"):
        self.text(f"\n### {title}\n")
        self.text(df.to_markdown(floatfmt=floatfmt))
        if note:
            self.text(f"\n_{note}_")

    def save(self, path):
        path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def paper_tables(md, monthly, daily, scheme):
    samples = SAMPLES_FOR_DM if scheme == "dm" else SAMPLES
    for sample, (start, end) in samples.items():
        m = in_sample(monthly, sample)
        md.text(f"\n## {sample}")

        stats = tables.portfolio_stats(m, daily)
        stats.to_csv(RESULTS / f"table1_{scheme}_{start}_{end}.csv")
        md.table(stats, "Table 1: momentum portfolios",
                 "mean, sd, alpha in %/year over the risk-free rate. sk = skewness of log returns.")
        md.table(tables.worst_months(m), "Table 2: worst 15 WML months (%)", floatfmt=".1f")
        md.table(tables.market_timing(m), "Table 3: market timing regressions")
        md.table(tables.optionality(m, "IB"), "Table 4A: optionality in bear markets")
        md.table(tables.optionality(m, "IL"), "Table 4B: optionality in bull markets")
        md.table(tables.forecasting(m), "Table 5: WML returns and market variance")
        md.table(tables.market_states(m), "Extra: WML in bull and bear markets")


def dynamic_tables(md, monthly, daily, vol, scheme, folder):
    w, mean_fit, vol_fit = dynamic.weights(monthly, vol, PAPER if scheme == "dm" else FULL)
    strategies = dynamic.monthly_returns(w, monthly)
    strategies.to_csv(RESULTS / f"strategies_{scheme}.csv")

    md.text("\n## Dynamic strategy (Section 4)")
    mean_table, vol_table = dynamic.forecast_regressions(mean_fit, vol_fit)
    md.table(mean_table, "Expected return: WML on IB*var_m (const x100)")
    md.table(vol_table, "Expected volatility: realized WML vol on GARCH and 126-day vol (Appendix D)")
    for sample in SAMPLES_FOR_DM if scheme == "dm" else SAMPLES:
        md.table(dynamic.performance(strategies, monthly, sample), f"Figure 5 numbers, {sample}",
                 "cvol and dyn scaled to 19%/year volatility. OOS starts in 1970 and only uses past data.")

    daily_strategies = dynamic.daily_returns(w, daily)
    for dyn in ["dyn (IS)", "dyn (OOS)"]:
        panel_a, panel_b = dynamic.spanning(daily_strategies, daily, dyn)
        md.table(panel_a, f"Table 7A: alpha of {dyn} (daily regressions)")
        md.table(panel_b, f"Table 7B: alpha of cvol (daily regressions, using {dyn})")
    figures.strategies_over_time(strategies, folder)


def main(scheme="allfirm"):
    folder = FIGURES / scheme
    folder.mkdir(parents=True, exist_ok=True)
    monthly, daily, vol = load(scheme)

    md = Markdown()
    md.text(f"# Momentum Crashes replication: all tables ({scheme} breakpoints)\n")
    md.text(NOTES)
    paper_tables(md, monthly, daily, scheme)

    figures.deciles_over_time(monthly, folder)
    if daily is not None:
        figures.crash_window(daily, "2009-03-01", "2009-05-31", folder / "fig2a_crash_2009.png",
                             "The 2009 momentum crash (daily, Mar–May 2009)")
        if daily.index[-1] >= pd.Timestamp("2021-03-31"):
            figures.crash_window(daily, "2020-10-15", "2021-03-31", folder / "fig2b_crash_2020.png",
                                 "The 2020 vaccine rally (daily, after the paper)")
        figures.rolling_betas(daily, folder)
        if vol is not None:
            dynamic_tables(md, monthly, daily, vol, scheme, folder)

    md.save(RESULTS / f"tables_{scheme}.md")


if __name__ == "__main__":
    main(*sys.argv[1:])
