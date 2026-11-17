# Momentum by cutoff: top / bottom 5, 10, 20, 30, 40%

The replication (`results/`) builds WML as **D10 − D1**: long the top 10% of stocks on past
return, short the bottom 10%. Here we change **only that cutoff** and rerun everything.

| Cutoff | Long | Short |
|---|---|---|
| 5% | top 5% | bottom 5% |
| **10% (baseline)** | top 10% (= D10) | bottom 10% (= D1) |
| 20% | top 20% | bottom 20% |
| 30% | top 30% | bottom 30% |
| 40% | top 40% | bottom 40% |

Everything else is the same as the replication: same CRSP and Fama-French data (from the shared Drive folder),
same stocks and filters, same signal (log return from t-12 to t-2), value weights at t-1,
monthly rebalancing, buy-and-hold daily weights, same GARCH and dynamic strategy. Both
breakpoint versions are built: `allfirm` (X% of all stocks, the paper's main version) and `nyse`
(cut-offs from NYSE stocks only).

## Check: the 10% cutoff is the baseline

| Check | Result |
|---|---|
| Stocks in the 10% legs vs D1 / D10 | 0 of 3.2 million stock-months differ |
| Monthly and daily WML vs `data/processed/*_deciles_*` | largest difference 1e-16 (rounding) |
| Table 1 (all periods) vs `results/table1_*.csv` | largest difference 2e-14 |
| Figure 5 numbers vs `results/tables_*.md` | identical |
| GARCH forecasts / dynamic weights | differ by ~1e-6 (optimizer noise; a different `arch` version) |

So any difference between cutoffs comes from the cutoff alone.

## Headline numbers

WML Sharpe ratio (plain), and the out-of-sample dynamic strategy's Sharpe ratio (Figure 5; GARCH
re-fits from 1970, first weight in 1972, so its "1960–2025" row covers 1972–2025):

| | | 5% | 10% (baseline) | 20% | 30% | 40% |
|---|---|---|---|---|---|---|
| **allfirm, 1960–2025** | WML | **0.86** | 0.71 | 0.50 | 0.48 | 0.38 |
| | dyn (OOS) | **1.30** | 1.08 | 0.93 | 0.83 | 0.68 |
| **allfirm, 2006–2025** | WML | **0.51** | 0.33 | 0.11 | 0.16 | 0.06 |
| | dyn (OOS) | **0.92** | 0.67 | 0.56 | 0.48 | 0.39 |
| **nyse, 1960–2025** | WML | **0.67** | 0.56 | 0.45 | 0.36 | 0.32 |
| | dyn (OOS) | **1.09** | 1.00 | 0.78 | 0.69 | 0.62 |
| **nyse, 2006–2025** | WML | **0.19** | 0.11 | 0.08 | −0.01 | −0.03 |
| | dyn (OOS) | **0.76** | 0.60 | 0.47 | 0.41 | 0.36 |

Crash risk, allfirm, 1960–2025:

| | 5% | 10% (baseline) | 20% | 30% | 40% |
|---|---|---|---|---|---|
| WML mean (%/yr) | 30.0 | 21.1 | 11.5 | 8.8 | 5.6 |
| WML volatility (%/yr) | 35.1 | 29.7 | 23.1 | 18.3 | 14.6 |
| Worst month (%) | −67.8 | −47.4 | −45.9 | −37.6 | −28.4 |
| Max drawdown (%) | −86.9 | −83.6 | −72.9 | −56.5 | −47.5 |
| Skewness (monthly) | −2.87 | −2.10 | −2.24 | −1.81 | −1.42 |

The full set (alpha, beta, skewness, Table 3 and 5 coefficients, worst months of cvol and dyn) is in
`summary_allfirm.md` and `summary_nyse.md`, for four periods: 1960–2025, 2006–2025, 1960–2013 and 2013–2025.

## What we find

1. **Narrower legs earn more, even per unit of risk.** Mean, CAPM alpha and Sharpe ratio go up
   steadily from 40% to 5%. This holds for both breakpoint versions and both periods; the only exception
   is allfirm 20% vs 30% in the last 20 years (0.11 vs 0.16). Most of the extra comes from
   the **short leg**: the bottom 5% loses 12.4%/yr over the risk-free rate, while the bottom 40% earns +3.9%/yr.
2. **Narrower legs also crash harder.** The worst month goes from −28% (40%) to −68% (5%, Jan 2001),
   and skewness gets more negative. Higher Sharpe ratios come with deeper tail losses.
3. **Momentum has weakened in the last 20 years at every cutoff.** Wide cutoffs barely earn anything since 2006
   (allfirm 40%: Sharpe ratio 0.06; nyse 30–40%: slightly negative). Only the 5% and 10% allfirm portfolios keep an alpha
   with t > 2.5.
4. **The paper's crash mechanism holds at every cutoff.** In bear markets WML's market beta falls
   (Table 3 (2): t between −6.2 and −7.4, 1960–2025), and bear × market variance predicts low
   WML returns (Table 5 (4): t between −4.8 and −7.2). The coefficients are generally larger for narrower cutoffs.
5. **Volatility management helps at every cutoff.** cvol and dyn raise the Sharpe ratio for all five cutoffs
   and cut the worst month to about −20% (full period) or about −10% (last 20 years). The ranking across cutoffs
   doesn't change. In 2006–2025, the dynamic 40% strategy (0.39) beats the plain 10% baseline (0.33).

**Caveats.** All returns are gross: there are no trading costs. Narrow legs hold fewer stocks
(allfirm 5%: about 200 per leg, against 400 at 10% and 1,600 at 40%), turn over more, and lean toward small,
illiquid losers, so costs would hit them hardest. With NYSE breakpoints the extreme legs
hold *more* stocks (5%: about 390 per leg), because small Nasdaq stocks pile into the tails.

## Files

| File | Contents |
|---|---|
| `summary_<scheme>.md` | Highlights, then comparison across cutoffs, one table per period, with Basic WML and Dynamic strategy row groups (start here) |
| `comparison_<scheme>.csv` | The same numbers, unformatted (one row per period × cutoff) |
| `<scheme>/tables_<X>pct.md` | Full replication report for one cutoff: Tables 1–5, worst months, bull/bear, Figure 5 numbers, Table 7 |
| `<scheme>/table1_<X>pct_<start>_<end>.csv` | Table 1 for one cutoff and period |
| `<scheme>/strategies_<X>pct.csv` | Monthly returns of WML, cvol, dyn (IS), dyn (OOS) |
| `figs/<scheme>/wml_cumulative_1960-2025.png` | Running performance of WML, all cutoffs |
| `figs/<scheme>/wml_cumulative_1960-2025_19vol.png` | Same, each cutoff scaled to 19% volatility (compares risk-adjusted paths) |
| `figs/<scheme>/wml_cumulative_2006-2025*.png` | The same two plots for the last 20 years |
| `figs/<scheme>/wml_sharpe_by_cutoff.png` | WML Sharpe ratio by cutoff, full period vs last 20 years |
| `figs/<scheme>/dyn_is_cumulative_1960-2025.png`, `dyn_oos_cumulative_1972-2025.png` | Running performance of the dynamic strategy, all cutoffs (reds), with basic 10% WML (dashed grey); all at 19% vol |
| `figs/<scheme>/dyn_*_cumulative_2006-2025.png` | The same for the last 20 years |
| `figs/<scheme>/<X>pct/fig*.png` | The replication's Figures 1, 2, 3, 5 for one cutoff |

## How to rerun

```bash
cd src
python cutoff_portfolios.py monthly   # legs for all cutoffs (~1.5 min)
python cutoff_portfolios.py daily     # daily legs (~30 min)
python cutoff_portfolios.py check     # 10% legs vs D1/D10 (needs the decile files)
python cutoff_garch.py                # GARCH for 10 series (~10 min with 12 cores)
python cutoff_report.py               # all tables and figures (~2 min)
```

On Adroit: `sbatch slurm/cutoff_pipeline.sbatch`. The cutoffs and the last-20-years period are set in `src/config.py`.
