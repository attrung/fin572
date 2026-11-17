# Momentum by cutoff: top / bottom X% (nyse breakpoints)

## Highlights

- **The dynamic strategy beats basic WML at every cutoff, in both periods.** dyn (OOS) Sharpe ratio, 5% / 10% (baseline) / 20% / 30% / 40%: 1.09 / 1.00 / 0.78 / 0.69 / 0.62 (1972–2025), against 0.67 / 0.56 / 0.45 / 0.36 / 0.32 for basic WML.
- **Since 2006, the dynamic strategy is what keeps momentum alive.** dyn (OOS) Sharpe ratio is 0.76 / 0.60 / 0.47 / 0.41 / 0.36, while basic WML is 0.19 / 0.11 / 0.08 / −0.01 / −0.03. Its FF3 alpha is significant at 5%, 10% and 20% (t = 3.35, 2.58, 2.13) but not at 30–40%. Basic WML has no significant alpha at any cutoff.
- **Most of the crash risk goes away at every cutoff.** The dynamic (OOS) strategy's worst month is −20% to −27% and its max drawdown −30% to −39%, against −25% to −52% and −47% to −90% for basic WML.
- **dyn beats the constant-volatility benchmark in the last 20 years.** Over 2006–2025 dyn (OOS) beats cvol at every cutoff (Sharpe ratio 0.76 vs 0.56 at 5%, 0.60 vs 0.44 at 10%, 0.36 vs 0.28 at 40%). Over the full period they roughly tie (1.00 vs 0.98 at 10%, 1.09 vs 1.13 at 5%).
- **Basic WML: the same ranking as allfirm, at lower levels.** Sharpe ratio 0.67 at 5% vs 0.56 at 10% vs 0.32 at 40% over 1960–2025, with worst months from −25.5% (40%) to −51.9% (5%, Nov 2020). The 5% legs hold about 390 stocks (allfirm: about 200), because small Nasdaq stocks pile up in the tails relative to NYSE cut-offs.

## Tables

Long the top X% of stocks on past return (t-12 to t-2), short the bottom X%. Same stocks, signal, value weights and monthly rebalancing as the replication; only the cutoff changes. 10% is the paper's D10 − D1 (the baseline in results/tables_nyse.md).

- **Basic WML**: the plain long-short portfolio (paper Tables 1, 3, 5). Means, sd and alphas in %/year; [t-stats] in brackets. Skewness is of log returns. Max drawdown compounds monthly returns. T3 (2) = Table 3 column (2), the change in WML's market beta in bear markets; T5 (4) = Table 5 column (4), WML on bear flag x market variance.
- **Dynamic strategy**: the paper's Section 4 strategy built on each cutoff's WML: weight = forecast mean / forecast variance (GJR-GARCH). dyn (IS) fits the forecasts on the full sample, as in the paper; dyn (OOS) only uses past data (GARCH re-fits from 1970, first weight in 1972, so its "full" period is 1972–2025). cvol (constant volatility, weight = 1 / past vol) is the paper's benchmark. All are scaled to 19%/year volatility over 1960–2025 (Figure 5), so sd is exactly 19 only in the full period. Skewness is of simple monthly returns (as in Figure 5); alpha is the Fama-French 3-factor alpha.

### 1960:01-2025:12 (full)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 387             | 631              | 1023            | 1367            | 1691            |
|                      | Winners mean (%/yr)                 | 15.79           | 13.40            | 10.99           | 10.12           | 9.33            |
|                      | Losers mean (%/yr)                  | -3.81           | -0.32            | 2.47            | 4.48            | 5.23            |
|                      | WML mean (%/yr)                     | 19.60           | 13.72            | 8.52            | 5.64            | 4.10            |
|                      | WML sd (%/yr)                       | 29.32           | 24.55            | 19.00           | 15.71           | 12.95           |
|                      | WML Sharpe ratio                    | 0.67            | 0.56             | 0.45            | 0.36            | 0.32            |
|                      | CAPM alpha (%/yr) [t]               | 22.46 [6.31]    | 16.08 [5.39]     | 10.33 [4.47]    | 6.87 [3.57]     | 4.93 [3.09]     |
|                      | CAPM beta                           | -0.40           | -0.33            | -0.26           | -0.17           | -0.12           |
|                      | Skewness, monthly (log)             | -2.48           | -2.34            | -1.82           | -1.52           | -1.25           |
|                      | Skewness, daily (log)               | -1.20           | -1.69            | -1.37           | -1.37           | -1.34           |
|                      | Worst month (%)                     | -51.9 (2020-11) | -45.3 (2009-04)  | -37.3 (2009-04) | -32.7 (2009-04) | -25.5 (2009-04) |
|                      | Max drawdown (%)                    | -90.1           | -81.9            | -64.9           | -58.2           | -47.2           |
|                      | Bear-market beta change, T3 (2) [t] | -0.925 [-6.23]  | -0.822 [-6.65]   | -0.658 [-6.88]  | -0.541 [-6.77]  | -0.444 [-6.71]  |
|                      | Bear x variance, T5 (4) [t]         | -0.562 [-5.66]  | -0.591 [-7.19]   | -0.376 [-5.85]  | -0.299 [-5.62]  | -0.222 [-5.04]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 1.29            | 1.16             | 0.95            | 0.81            | 0.74            |
|                      | Sharpe ratio, dyn (OOS)             | 1.09            | 1.00             | 0.78            | 0.69            | 0.62            |
|                      | Sharpe ratio, cvol (benchmark)      | 1.13            | 0.98             | 0.81            | 0.68            | 0.61            |
|                      | Mean (%/yr), dyn (IS)               | 24.53           | 22.06            | 18.10           | 15.45           | 14.11           |
|                      | Mean (%/yr), dyn (OOS)              | 20.62           | 18.97            | 14.88           | 13.07           | 11.69           |
|                      | sd (%/yr), dyn (IS)                 | 19.00           | 19.00            | 19.00           | 19.00           | 19.00           |
|                      | sd (%/yr), dyn (OOS)                | 19.00           | 19.00            | 19.00           | 19.00           | 19.00           |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 25.39 [10.73]   | 22.65 [9.56]     | 18.66 [7.88]    | 15.64 [6.61]    | 14.08 [5.96]    |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 21.28 [8.12]    | 19.74 [7.53]     | 15.44 [5.88]    | 13.33 [5.09]    | 11.57 [4.42]    |
|                      | Skewness, monthly, dyn (IS)         | 0.69            | 0.70             | 0.48            | 0.28            | 0.28            |
|                      | Skewness, monthly, dyn (OOS)        | 0.86            | 0.66             | 0.54            | 0.28            | 0.54            |
|                      | Worst month (%), dyn (IS)           | -21.8 (1985-01) | -16.3 (1978-10)  | -18.2 (1978-10) | -19.4 (1972-11) | -18.3 (1978-10) |
|                      | Worst month (%), dyn (OOS)          | -20.6 (1985-01) | -20.7 (1973-07)  | -20.2 (1978-10) | -24.8 (1973-07) | -27.0 (1973-07) |
|                      | Worst month (%), cvol (benchmark)   | -17.7 (1973-07) | -19.4 (1973-07)  | -21.3 (1978-10) | -21.4 (1978-10) | -22.9 (1978-10) |
|                      | Max drawdown (%), dyn (IS)          | -31.5           | -31.0            | -28.4           | -35.8           | -35.2           |
|                      | Max drawdown (%), dyn (OOS)         | -31.6           | -29.7            | -35.9           | -38.0           | -38.7           |

### 2006:01-2025:12 (last 20 years)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 326             | 543              | 907             | 1234            | 1549            |
|                      | Winners mean (%/yr)                 | 14.58           | 11.51            | 9.42            | 9.85            | 10.11           |
|                      | Losers mean (%/yr)                  | 7.50            | 8.09             | 7.75            | 10.05           | 10.45           |
|                      | WML mean (%/yr)                     | 7.08            | 3.42             | 1.67            | -0.20           | -0.34           |
|                      | WML sd (%/yr)                       | 36.79           | 30.16            | 21.55           | 17.13           | 13.64           |
|                      | WML Sharpe ratio                    | 0.19            | 0.11             | 0.08            | -0.01           | -0.03           |
|                      | CAPM alpha (%/yr) [t]               | 15.09 [1.91]    | 10.76 [1.69]     | 7.38 [1.64]     | 3.78 [1.04]     | 2.55 [0.87]     |
|                      | CAPM beta                           | -0.79           | -0.72            | -0.56           | -0.39           | -0.28           |
|                      | Skewness, monthly (log)             | -2.42           | -2.37            | -2.02           | -2.21           | -1.83           |
|                      | Skewness, daily (log)               | -1.07           | -1.49            | -1.12           | -1.20           | -1.14           |
|                      | Worst month (%)                     | -51.9 (2020-11) | -45.3 (2009-04)  | -37.3 (2009-04) | -32.7 (2009-04) | -25.5 (2009-04) |
|                      | Max drawdown (%)                    | -90.1           | -81.9            | -64.9           | -58.2           | -47.2           |
|                      | Bear-market beta change, T3 (2) [t] | -0.582 [-1.91]  | -0.650 [-2.69]   | -0.382 [-2.23]  | -0.268 [-1.90]  | -0.208 [-1.83]  |
|                      | Bear x variance, T5 (4) [t]         | -0.533 [-3.86]  | -0.600 [-5.45]   | -0.385 [-4.84]  | -0.297 [-4.67]  | -0.212 [-4.16]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 0.81            | 0.64             | 0.53            | 0.48            | 0.42            |
|                      | Sharpe ratio, dyn (OOS)             | 0.76            | 0.60             | 0.47            | 0.41            | 0.36            |
|                      | Sharpe ratio, cvol (benchmark)      | 0.56            | 0.44             | 0.40            | 0.30            | 0.28            |
|                      | Mean (%/yr), dyn (IS)               | 9.91            | 8.45             | 5.95            | 5.96            | 5.46            |
|                      | Mean (%/yr), dyn (OOS)              | 7.31            | 5.91             | 3.80            | 3.77            | 2.93            |
|                      | sd (%/yr), dyn (IS)                 | 12.25           | 13.15            | 11.18           | 12.33           | 12.97           |
|                      | sd (%/yr), dyn (OOS)                | 9.64            | 9.92             | 8.12            | 9.09            | 8.22            |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 9.17 [3.34]     | 7.33 [2.48]      | 5.42 [2.17]     | 5.24 [1.92]     | 4.51 [1.56]     |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 7.13 [3.35]     | 5.64 [2.58]      | 3.76 [2.13]     | 3.56 [1.81]     | 2.65 [1.48]     |
|                      | Skewness, monthly, dyn (IS)         | 1.07            | 1.91             | 0.81            | 1.33            | 1.12            |
|                      | Skewness, monthly, dyn (OOS)        | 1.12            | 0.58             | 0.71            | 1.20            | 0.77            |
|                      | Worst month (%), dyn (IS)           | -12.7 (2010-12) | -11.0 (2010-12)  | -8.4 (2015-04)  | -11.7 (2016-11) | -10.5 (2016-11) |
|                      | Worst month (%), dyn (OOS)          | -11.3 (2010-12) | -10.4 (2010-12)  | -6.8 (2015-04)  | -9.5 (2016-11)  | -7.3 (2016-11)  |
|                      | Worst month (%), cvol (benchmark)   | -12.8 (2010-12) | -13.6 (2020-04)  | -9.3 (2008-01)  | -9.8 (2009-04)  | -10.0 (2009-04) |
|                      | Max drawdown (%), dyn (IS)          | -13.5           | -16.4            | -18.6           | -21.0           | -25.5           |
|                      | Max drawdown (%), dyn (OOS)         | -12.0           | -14.8            | -14.6           | -17.3           | -18.5           |

### 1960:01-2013:03 (paper overlap)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 403             | 656              | 1060            | 1413            | 1743            |
|                      | Winners mean (%/yr)                 | 14.93           | 13.05            | 10.66           | 9.61            | 8.61            |
|                      | Losers mean (%/yr)                  | -7.46           | -2.79            | 0.56            | 2.63            | 3.42            |
|                      | WML mean (%/yr)                     | 22.40           | 15.84            | 10.09           | 6.98            | 5.18            |
|                      | WML sd (%/yr)                       | 27.71           | 23.69            | 18.73           | 15.77           | 13.12           |
|                      | WML Sharpe ratio                    | 0.81            | 0.67             | 0.54            | 0.44            | 0.40            |
|                      | CAPM alpha (%/yr) [t]               | 24.28 [6.46]    | 17.36 [5.40]     | 11.23 [4.41]    | 7.75 [3.59]     | 5.72 [3.18]     |
|                      | CAPM beta                           | -0.33           | -0.26            | -0.20           | -0.13           | -0.09           |
|                      | Skewness, monthly (log)             | -2.34           | -2.70            | -2.11           | -1.70           | -1.42           |
|                      | Skewness, daily (log)               | -1.13           | -1.98            | -1.40           | -1.28           | -1.22           |
|                      | Worst month (%)                     | -46.2 (2001-01) | -45.3 (2009-04)  | -37.3 (2009-04) | -32.7 (2009-04) | -25.5 (2009-04) |
|                      | Max drawdown (%)                    | -82.6           | -81.9            | -64.9           | -53.9           | -44.5           |
|                      | Bear-market beta change, T3 (2) [t] | -0.940 [-6.27]  | -0.861 [-6.75]   | -0.733 [-7.27]  | -0.617 [-7.24]  | -0.516 [-7.25]  |
|                      | Bear x variance, T5 (4) [t]         | -0.507 [-5.27]  | -0.540 [-6.64]   | -0.346 [-5.32]  | -0.291 [-5.32]  | -0.219 [-4.78]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 1.41            | 1.27             | 1.03            | 0.88            | 0.80            |
|                      | Sharpe ratio, dyn (OOS)             | 1.20            | 1.11             | 0.86            | 0.76            | 0.68            |
|                      | Sharpe ratio, cvol (benchmark)      | 1.26            | 1.10             | 0.89            | 0.75            | 0.68            |
|                      | Mean (%/yr), dyn (IS)               | 28.66           | 25.77            | 21.13           | 17.97           | 16.35           |
|                      | Mean (%/yr), dyn (OOS)              | 25.31           | 23.25            | 18.31           | 16.01           | 14.36           |
|                      | sd (%/yr), dyn (IS)                 | 20.34           | 20.25            | 20.43           | 20.30           | 20.31           |
|                      | sd (%/yr), dyn (OOS)                | 21.07           | 20.93            | 21.19           | 21.06           | 21.22           |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 29.72 [10.46]   | 26.37 [9.31]     | 21.51 [7.53]    | 17.61 [6.21]    | 15.71 [5.55]    |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 26.22 [7.83]    | 24.08 [7.22]     | 18.81 [5.57]    | 15.91 [4.75]    | 13.81 [4.10]    |
|                      | Skewness, monthly, dyn (IS)         | 0.52            | 0.55             | 0.35            | 0.15            | 0.17            |
|                      | Skewness, monthly, dyn (OOS)        | 0.63            | 0.48             | 0.37            | 0.13            | 0.40            |
|                      | Worst month (%), dyn (IS)           | -21.8 (1985-01) | -16.3 (1978-10)  | -18.2 (1978-10) | -19.4 (1972-11) | -18.3 (1978-10) |
|                      | Worst month (%), dyn (OOS)          | -20.6 (1985-01) | -20.7 (1973-07)  | -20.2 (1978-10) | -24.8 (1973-07) | -27.0 (1973-07) |
|                      | Worst month (%), cvol (benchmark)   | -17.7 (1973-07) | -19.4 (1973-07)  | -21.3 (1978-10) | -21.4 (1978-10) | -22.9 (1978-10) |
|                      | Max drawdown (%), dyn (IS)          | -31.5           | -31.0            | -28.4           | -35.8           | -35.2           |
|                      | Max drawdown (%), dyn (OOS)         | -31.6           | -29.7            | -35.9           | -38.0           | -38.7           |

### 2013:04-2025:12 (after the paper)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 321             | 527              | 869             | 1177            | 1477            |
|                      | Winners mean (%/yr)                 | 19.39           | 14.88            | 12.40           | 12.28           | 12.34           |
|                      | Losers mean (%/yr)                  | 11.46           | 10.03            | 10.43           | 12.21           | 12.79           |
|                      | WML mean (%/yr)                     | 7.92            | 4.85             | 1.97            | 0.08            | -0.45           |
|                      | WML sd (%/yr)                       | 35.13           | 27.79            | 20.01           | 15.44           | 12.17           |
|                      | WML Sharpe ratio                    | 0.23            | 0.17             | 0.10            | 0.00            | -0.04           |
|                      | CAPM alpha (%/yr) [t]               | 17.11 [1.77]    | 12.97 [1.71]     | 8.31 [1.54]     | 4.36 [1.03]     | 2.36 [0.70]     |
|                      | CAPM beta                           | -0.72           | -0.64            | -0.50           | -0.34           | -0.22           |
|                      | Skewness, monthly (log)             | -2.48           | -1.26            | -0.78           | -0.77           | -0.44           |
|                      | Skewness, daily (log)               | -1.02           | -1.09            | -1.13           | -1.33           | -1.34           |
|                      | Worst month (%)                     | -51.9 (2020-11) | -28.9 (2020-04)  | -22.6 (2023-01) | -18.0 (2023-01) | -12.7 (2023-01) |
|                      | Max drawdown (%)                    | -82.3           | -63.0            | -51.8           | -44.4           | -36.5           |
|                      | Bear-market beta change, T3 (2) [t] | -1.470 [-2.45]  | -0.977 [-2.09]   | -0.237 [-0.71]  | -0.140 [-0.52]  | -0.020 [-0.09]  |
|                      | Bear x variance, T5 (4) [t]         | -2.066 [-3.81]  | -1.947 [-4.63]   | -1.215 [-3.94]  | -0.652 [-2.67]  | -0.435 [-2.25]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 0.69            | 0.57             | 0.52            | 0.42            | 0.41            |
|                      | Sharpe ratio, dyn (OOS)             | 0.65            | 0.54             | 0.47            | 0.38            | 0.38            |
|                      | Sharpe ratio, cvol (benchmark)      | 0.45            | 0.36             | 0.36            | 0.25            | 0.21            |
|                      | Mean (%/yr), dyn (IS)               | 7.27            | 6.54             | 5.44            | 4.93            | 4.77            |
|                      | Mean (%/yr), dyn (OOS)              | 5.44            | 5.12             | 3.78            | 3.55            | 3.06            |
|                      | sd (%/yr), dyn (IS)                 | 10.54           | 11.51            | 10.45           | 11.69           | 11.74           |
|                      | sd (%/yr), dyn (OOS)                | 8.31            | 9.55             | 8.00            | 9.27            | 8.09            |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 7.04 [2.44]     | 5.83 [1.86]      | 5.61 [2.03]     | 5.07 [1.68]     | 4.81 [1.59]     |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 5.41 [2.37]     | 4.73 [1.82]      | 4.01 [1.89]     | 3.73 [1.55]     | 3.15 [1.50]     |
|                      | Skewness, monthly, dyn (IS)         | 1.48            | 1.60             | 1.12            | 1.32            | 1.00            |
|                      | Skewness, monthly, dyn (OOS)        | 1.69            | 1.20             | 1.26            | 1.56            | 1.13            |
|                      | Worst month (%), dyn (IS)           | -6.9 (2014-03)  | -9.6 (2017-11)   | -8.4 (2015-04)  | -11.7 (2016-11) | -10.5 (2016-11) |
|                      | Worst month (%), dyn (OOS)          | -5.9 (2014-03)  | -8.4 (2017-11)   | -6.8 (2015-04)  | -9.5 (2016-11)  | -7.3 (2016-11)  |
|                      | Worst month (%), cvol (benchmark)   | -12.3 (2020-04) | -13.6 (2020-04)  | -8.8 (2023-01)  | -9.3 (2023-01)  | -8.4 (2023-01)  |
|                      | Max drawdown (%), dyn (IS)          | -10.5           | -11.9            | -18.6           | -21.0           | -25.5           |
|                      | Max drawdown (%), dyn (OOS)         | -8.1            | -10.7            | -14.6           | -17.3           | -18.5           |
