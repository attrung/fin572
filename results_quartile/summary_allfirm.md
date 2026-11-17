# Momentum by cutoff: top / bottom X% (allfirm breakpoints)

## Highlights

- **The dynamic strategy beats basic WML at every cutoff, in both periods.** dyn (OOS) Sharpe ratio, 5% / 10% (baseline) / 20% / 30% / 40%: 1.30 / 1.08 / 0.93 / 0.83 / 0.68 (1972–2025), against 0.86 / 0.71 / 0.50 / 0.48 / 0.38 for basic WML. That is 1.5–1.9× better, and the gain is largest for the wide cutoffs. Over 2006–2025: 0.92 / 0.67 / 0.56 / 0.48 / 0.39, against 0.51 / 0.33 / 0.11 / 0.16 / 0.06.
- **Narrower cutoffs are still the best base for the dynamic strategy.** dyn (OOS) FF3 alpha is 25.3%/yr (t = 9.7) at 5%, 21.4% (t = 8.2) at 10% and 13.4% (t = 5.1) at 40%. Over 2006–2025 it is 10.4% (t = 3.9), 7.4% (t = 3.0) and 3.5% (t = 1.75, not significant).
- **Most of the crash risk goes away at every cutoff.** The dynamic strategy's worst month is −17.5% to −29% and its max drawdown −27% to −44%, against −28% to −68% and −48% to −87% for basic WML. Skewness turns positive (0.3 to 0.7). The 5% cutoff gains the most: its max drawdown goes from −86.9% to −31.1% (OOS).
- **dyn beats the constant-volatility benchmark mainly in the last 20 years.** Over 2006–2025 dyn (OOS) beats cvol at every cutoff (Sharpe ratio 0.92 vs 0.84 at 5%, 0.67 vs 0.59 at 10%, 0.39 vs 0.33 at 40%). Over the full period they roughly tie (1.08 vs 1.09 at 10%). The in-sample version beats cvol everywhere.
- **Basic WML: narrower legs pay more and crash harder.** Sharpe ratio 0.86 at 5% vs 0.71 at 10% vs 0.38 at 40% (0.51 / 0.33 / 0.06 over 2006–2025), mostly from the short leg (bottom 5%: −12.4%/yr). The worst month goes from −28.4% (40%) to −67.8% (5%, Jan 2001). The paper's bear-market beta drop holds at every cutoff (t from −6.4 to −7.4).

## Tables

Long the top X% of stocks on past return (t-12 to t-2), short the bottom X%. Same stocks, signal, value weights and monthly rebalancing as the replication; only the cutoff changes. 10% is the paper's D10 − D1 (the baseline in results/tables_allfirm.md).

- **Basic WML**: the plain long-short portfolio (paper Tables 1, 3, 5). Means, sd and alphas in %/year; [t-stats] in brackets. Skewness is of log returns. Max drawdown compounds monthly returns. T3 (2) = Table 3 column (2), the change in WML's market beta in bear markets; T5 (4) = Table 5 column (4), WML on bear flag x market variance.
- **Dynamic strategy**: the paper's Section 4 strategy built on each cutoff's WML: weight = forecast mean / forecast variance (GJR-GARCH). dyn (IS) fits the forecasts on the full sample, as in the paper; dyn (OOS) only uses past data (GARCH re-fits from 1970, first weight in 1972, so its "full" period is 1972–2025). cvol (constant volatility, weight = 1 / past vol) is the paper's benchmark. All are scaled to 19%/year volatility over 1960–2025 (Figure 5), so sd is exactly 19 only in the full period. Skewness is of simple monthly returns (as in Figure 5); alpha is the Fama-French 3-factor alpha.

### 1960:01-2025:12 (full)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 198             | 398              | 800             | 1202            | 1605            |
|                      | Winners mean (%/yr)                 | 17.58           | 14.79            | 11.23           | 10.27           | 9.43            |
|                      | Losers mean (%/yr)                  | -12.44          | -6.27            | -0.31           | 1.48            | 3.86            |
|                      | WML mean (%/yr)                     | 30.02           | 21.06            | 11.54           | 8.79            | 5.57            |
|                      | WML sd (%/yr)                       | 35.11           | 29.67            | 23.05           | 18.30           | 14.57           |
|                      | WML Sharpe ratio                    | 0.86            | 0.71             | 0.50            | 0.48            | 0.38            |
|                      | CAPM alpha (%/yr) [t]               | 33.22 [7.77]    | 24.31 [6.79]     | 14.19 [5.12]    | 10.65 [4.80]    | 6.80 [3.82]     |
|                      | CAPM beta                           | -0.45           | -0.46            | -0.38           | -0.26           | -0.17           |
|                      | Skewness, monthly (log)             | -2.87           | -2.10            | -2.24           | -1.81           | -1.42           |
|                      | Skewness, daily (log)               | -1.08           | -1.20            | -1.34           | -1.29           | -1.25           |
|                      | Worst month (%)                     | -67.8 (2001-01) | -47.4 (2001-01)  | -45.9 (2001-01) | -37.6 (2001-01) | -28.4 (2009-04) |
|                      | Max drawdown (%)                    | -86.9           | -83.6            | -72.9           | -56.5           | -47.5           |
|                      | Bear-market beta change, T3 (2) [t] | -1.142 [-6.42]  | -0.978 [-6.58]   | -0.782 [-6.80]  | -0.641 [-6.97]  | -0.543 [-7.38]  |
|                      | Bear x variance, T5 (4) [t]         | -0.682 [-5.74]  | -0.649 [-6.50]   | -0.485 [-6.24]  | -0.305 [-4.89]  | -0.240 [-4.84]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 1.44            | 1.23             | 1.05            | 0.98            | 0.82            |
|                      | Sharpe ratio, dyn (OOS)             | 1.30            | 1.08             | 0.93            | 0.83            | 0.68            |
|                      | Sharpe ratio, cvol (benchmark)      | 1.25            | 1.09             | 0.91            | 0.85            | 0.69            |
|                      | Mean (%/yr), dyn (IS)               | 27.37           | 23.44            | 19.97           | 18.66           | 15.51           |
|                      | Mean (%/yr), dyn (OOS)              | 24.68           | 20.46            | 17.64           | 15.77           | 12.99           |
|                      | sd (%/yr), dyn (IS)                 | 19.00           | 19.00            | 19.00           | 19.00           | 19.00           |
|                      | sd (%/yr), dyn (OOS)                | 19.00           | 19.00            | 19.00           | 19.00           | 19.00           |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 28.42 [12.02]   | 24.44 [10.33]    | 21.04 [8.89]    | 19.67 [8.31]    | 15.90 [6.72]    |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 25.31 [9.67]    | 21.43 [8.18]     | 18.66 [7.13]    | 16.65 [6.35]    | 13.37 [5.10]    |
|                      | Skewness, monthly, dyn (IS)         | 0.44            | 0.65             | 0.40            | 0.34            | 0.37            |
|                      | Skewness, monthly, dyn (OOS)        | 0.27            | 0.54             | 0.63            | 0.54            | 0.40            |
|                      | Worst month (%), dyn (IS)           | -23.0 (1973-07) | -17.5 (1984-01)  | -19.7 (1972-11) | -20.2 (1972-11) | -19.3 (1972-11) |
|                      | Worst month (%), dyn (OOS)          | -29.0 (1973-07) | -19.3 (1974-04)  | -23.2 (1973-07) | -21.6 (1972-11) | -21.1 (1973-07) |
|                      | Worst month (%), cvol (benchmark)   | -22.1 (1973-07) | -18.2 (1973-07)  | -22.1 (1978-10) | -21.7 (2001-01) | -22.7 (1978-10) |
|                      | Max drawdown (%), dyn (IS)          | -27.3           | -32.6            | -29.4           | -29.7           | -43.6           |
|                      | Max drawdown (%), dyn (OOS)         | -31.1           | -33.3            | -35.7           | -37.7           | -41.5           |

### 2006:01-2025:12 (last 20 years)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 184             | 369              | 741             | 1113            | 1486            |
|                      | Winners mean (%/yr)                 | 16.25           | 13.68            | 9.40            | 9.70            | 10.20           |
|                      | Losers mean (%/yr)                  | -4.50           | 2.28             | 6.51            | 6.57            | 9.30            |
|                      | WML mean (%/yr)                     | 20.74           | 11.40            | 2.89            | 3.13            | 0.90            |
|                      | WML sd (%/yr)                       | 40.59           | 34.81            | 25.36           | 19.43           | 15.21           |
|                      | WML Sharpe ratio                    | 0.51            | 0.33             | 0.11            | 0.16            | 0.06            |
|                      | CAPM alpha (%/yr) [t]               | 28.26 [3.18]    | 19.93 [2.71]     | 10.32 [2.00]    | 8.50 [2.12]     | 4.77 [1.49]     |
|                      | CAPM beta                           | -0.74           | -0.84            | -0.73           | -0.53           | -0.38           |
|                      | Skewness, monthly (log)             | -2.09           | -2.08            | -2.36           | -1.85           | -2.00           |
|                      | Skewness, daily (log)               | -1.08           | -1.19            | -1.22           | -1.05           | -1.05           |
|                      | Worst month (%)                     | -50.3 (2009-03) | -45.2 (2009-04)  | -43.9 (2009-04) | -33.9 (2009-04) | -28.4 (2009-04) |
|                      | Max drawdown (%)                    | -86.9           | -83.6            | -72.9           | -56.5           | -47.5           |
|                      | Bear-market beta change, T3 (2) [t] | -0.688 [-2.01]  | -0.602 [-2.15]   | -0.441 [-2.24]  | -0.321 [-2.08]  | -0.278 [-2.26]  |
|                      | Bear x variance, T5 (4) [t]         | -0.590 [-3.87]  | -0.660 [-5.17]   | -0.481 [-5.17]  | -0.297 [-4.08]  | -0.238 [-4.20]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 0.95            | 0.72             | 0.61            | 0.52            | 0.45            |
|                      | Sharpe ratio, dyn (OOS)             | 0.92            | 0.67             | 0.56            | 0.48            | 0.39            |
|                      | Sharpe ratio, cvol (benchmark)      | 0.84            | 0.59             | 0.44            | 0.44            | 0.33            |
|                      | Mean (%/yr), dyn (IS)               | 12.45           | 9.44             | 7.35            | 6.34            | 5.64            |
|                      | Mean (%/yr), dyn (OOS)              | 10.79           | 7.57             | 5.29            | 4.37            | 3.60            |
|                      | sd (%/yr), dyn (IS)                 | 13.11           | 13.12            | 11.97           | 12.19           | 12.61           |
|                      | sd (%/yr), dyn (OOS)                | 11.78           | 11.25            | 9.37            | 9.09            | 9.18            |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 11.63 [3.92]    | 8.62 [2.91]      | 7.03 [2.63]     | 6.03 [2.25]     | 5.01 [1.80]     |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 10.43 [3.94]    | 7.39 [2.95]      | 5.47 [2.68]     | 4.40 [2.24]     | 3.46 [1.75]     |
|                      | Skewness, monthly, dyn (IS)         | 0.67            | 1.12             | 0.77            | 1.13            | 1.13            |
|                      | Skewness, monthly, dyn (OOS)        | 0.59            | 0.42             | 0.44            | 1.15            | 0.81            |
|                      | Worst month (%), dyn (IS)           | -12.4 (2010-12) | -13.8 (2010-12)  | -9.4 (2014-03)  | -10.6 (2019-01) | -10.3 (2016-11) |
|                      | Worst month (%), dyn (OOS)          | -12.0 (2010-12) | -13.8 (2010-12)  | -8.2 (2014-03)  | -8.0 (2019-01)  | -8.0 (2016-11)  |
|                      | Worst month (%), cvol (benchmark)   | -11.2 (2010-12) | -13.5 (2010-12)  | -9.7 (2020-04)  | -9.5 (2019-01)  | -9.5 (2023-01)  |
|                      | Max drawdown (%), dyn (IS)          | -14.6           | -17.7            | -18.7           | -20.1           | -25.1           |
|                      | Max drawdown (%), dyn (OOS)         | -14.4           | -16.9            | -16.0           | -15.8           | -20.1           |

### 1960:01-2013:03 (paper overlap)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 204             | 409              | 822             | 1235            | 1649            |
|                      | Winners mean (%/yr)                 | 16.47           | 14.11            | 10.94           | 9.84            | 8.67            |
|                      | Losers mean (%/yr)                  | -15.41          | -7.95            | -2.70           | -0.50           | 2.02            |
|                      | WML mean (%/yr)                     | 31.88           | 22.07            | 13.65           | 10.34           | 6.64            |
|                      | WML sd (%/yr)                       | 34.45           | 28.73            | 22.87           | 18.34           | 14.75           |
|                      | WML Sharpe ratio                    | 0.93            | 0.77             | 0.60            | 0.56            | 0.45            |
|                      | CAPM alpha (%/yr) [t]               | 34.26 [7.34]    | 24.24 [6.25]     | 15.41 [5.00]    | 11.60 [4.66]    | 7.46 [3.71]     |
|                      | CAPM beta                           | -0.42           | -0.38            | -0.31           | -0.22           | -0.14           |
|                      | Skewness, monthly (log)             | -3.30           | -2.37            | -2.57           | -2.08           | -1.56           |
|                      | Skewness, daily (log)               | -0.98           | -1.44            | -1.42           | -1.33           | -1.22           |
|                      | Worst month (%)                     | -67.8 (2001-01) | -47.4 (2001-01)  | -45.9 (2001-01) | -37.6 (2001-01) | -28.4 (2009-04) |
|                      | Max drawdown (%)                    | -86.9           | -83.6            | -72.9           | -56.5           | -47.5           |
|                      | Bear-market beta change, T3 (2) [t] | -1.239 [-6.70]  | -1.046 [-6.79]   | -0.844 [-6.89]  | -0.712 [-7.23]  | -0.603 [-7.59]  |
|                      | Bear x variance, T5 (4) [t]         | -0.656 [-5.49]  | -0.581 [-5.85]   | -0.448 [-5.66]  | -0.293 [-4.57]  | -0.228 [-4.41]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 1.56            | 1.34             | 1.15            | 1.09            | 0.89            |
|                      | Sharpe ratio, dyn (OOS)             | 1.43            | 1.19             | 1.04            | 0.93            | 0.75            |
|                      | Sharpe ratio, cvol (benchmark)      | 1.35            | 1.19             | 1.02            | 0.95            | 0.77            |
|                      | Mean (%/yr), dyn (IS)               | 31.68           | 27.28            | 23.47           | 21.98           | 18.00           |
|                      | Mean (%/yr), dyn (OOS)              | 29.73           | 24.82            | 21.79           | 19.58           | 15.86           |
|                      | sd (%/yr), dyn (IS)                 | 20.27           | 20.32            | 20.36           | 20.22           | 20.26           |
|                      | sd (%/yr), dyn (OOS)                | 20.79           | 20.88            | 21.03           | 21.03           | 21.05           |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 32.98 [11.67]   | 28.40 [10.00]    | 24.45 [8.58]    | 22.70 [8.01]    | 17.85 [6.30]    |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 30.60 [9.27]    | 25.89 [7.79]     | 22.84 [6.82]    | 20.34 [6.07]    | 15.94 [4.76]    |
|                      | Skewness, monthly, dyn (IS)         | 0.29            | 0.52             | 0.27            | 0.19            | 0.26            |
|                      | Skewness, monthly, dyn (OOS)        | 0.08            | 0.37             | 0.45            | 0.35            | 0.26            |
|                      | Worst month (%), dyn (IS)           | -23.0 (1973-07) | -17.5 (1984-01)  | -19.7 (1972-11) | -20.2 (1972-11) | -19.3 (1972-11) |
|                      | Worst month (%), dyn (OOS)          | -29.0 (1973-07) | -19.3 (1974-04)  | -23.2 (1973-07) | -21.6 (1972-11) | -21.1 (1973-07) |
|                      | Worst month (%), cvol (benchmark)   | -22.1 (1973-07) | -18.2 (1973-07)  | -22.1 (1978-10) | -21.7 (2001-01) | -22.7 (1978-10) |
|                      | Max drawdown (%), dyn (IS)          | -27.3           | -32.6            | -29.4           | -29.7           | -43.6           |
|                      | Max drawdown (%), dyn (OOS)         | -31.1           | -33.3            | -35.7           | -37.7           | -41.5           |

### 2013:04-2025:12 (after the paper)

| Strategy             | Statistic                           | 5%              | 10% (baseline)   | 20%             | 30%             | 40%             |
|:---------------------|:------------------------------------|:----------------|:-----------------|:----------------|:----------------|:----------------|
| **Basic WML**        | Stocks per leg (avg)                | 176             | 353              | 709             | 1064            | 1420            |
|                      | Winners mean (%/yr)                 | 22.23           | 17.63            | 12.41           | 12.08           | 12.64           |
|                      | Losers mean (%/yr)                  | -0.05           | 0.79             | 9.69            | 9.78            | 11.56           |
|                      | WML mean (%/yr)                     | 22.28           | 16.84            | 2.72            | 2.30            | 1.08            |
|                      | WML sd (%/yr)                       | 37.80           | 33.38            | 23.69           | 18.05           | 13.78           |
|                      | WML Sharpe ratio                    | 0.59            | 0.50             | 0.11            | 0.13            | 0.08            |
|                      | CAPM alpha (%/yr) [t]               | 29.94 [2.82]    | 27.28 [3.03]     | 11.26 [1.81]    | 8.04 [1.66]     | 5.05 [1.35]     |
|                      | CAPM beta                           | -0.60           | -0.82            | -0.67           | -0.45           | -0.31           |
|                      | Skewness, monthly (log)             | -1.25           | -1.25            | -0.93           | -0.65           | -0.81           |
|                      | Skewness, daily (log)               | -0.98           | -0.75            | -1.05           | -1.07           | -1.19           |
|                      | Worst month (%)                     | -37.9 (2020-11) | -35.7 (2023-01)  | -25.0 (2023-01) | -19.2 (2023-01) | -18.2 (2023-01) |
|                      | Max drawdown (%)                    | -70.2           | -55.1            | -48.6           | -36.7           | -31.0           |
|                      | Bear-market beta change, T3 (2) [t] | -1.050 [-1.57]  | -0.841 [-1.51]   | -0.738 [-1.91]  | -0.314 [-1.03]  | -0.219 [-0.93]  |
|                      | Bear x variance, T5 (4) [t]         | -1.531 [-2.56]  | -2.248 [-4.42]   | -1.554 [-4.30]  | -0.757 [-2.65]  | -0.647 [-2.99]  |
| **Dynamic strategy** | Sharpe ratio, dyn (IS)              | 0.85            | 0.68             | 0.50            | 0.40            | 0.42            |
|                      | Sharpe ratio, dyn (OOS)             | 0.82            | 0.65             | 0.47            | 0.38            | 0.40            |
|                      | Sharpe ratio, cvol (benchmark)      | 0.74            | 0.60             | 0.30            | 0.31            | 0.29            |
|                      | Mean (%/yr), dyn (IS)               | 9.38            | 7.43             | 5.36            | 4.78            | 5.10            |
|                      | Mean (%/yr), dyn (OOS)              | 8.35            | 6.38             | 4.19            | 3.46            | 3.71            |
|                      | sd (%/yr), dyn (IS)                 | 10.98           | 10.89            | 10.77           | 11.94           | 12.04           |
|                      | sd (%/yr), dyn (OOS)                | 10.15           | 9.87             | 8.91            | 9.07            | 9.32            |
|                      | FF3 alpha (%/yr) [t], dyn (IS)      | 9.30 [3.02]     | 7.40 [2.48]      | 5.57 [1.97]     | 5.07 [1.64]     | 5.26 [1.71]     |
|                      | FF3 alpha (%/yr) [t], dyn (OOS)     | 8.35 [2.93]     | 6.42 [2.38]      | 4.49 [1.92]     | 3.74 [1.58]     | 3.89 [1.62]     |
|                      | Skewness, monthly, dyn (IS)         | 0.99            | 0.76             | 0.79            | 1.53            | 1.06            |
|                      | Skewness, monthly, dyn (OOS)        | 1.12            | 0.81             | 0.78            | 1.62            | 1.16            |
|                      | Worst month (%), dyn (IS)           | -6.7 (2019-09)  | -8.7 (2014-03)   | -9.4 (2014-03)  | -10.6 (2019-01) | -10.3 (2016-11) |
|                      | Worst month (%), dyn (OOS)          | -6.2 (2015-04)  | -8.1 (2014-03)   | -8.2 (2014-03)  | -8.0 (2019-01)  | -8.0 (2016-11)  |
|                      | Worst month (%), cvol (benchmark)   | -8.8 (2019-12)  | -10.7 (2020-04)  | -9.7 (2020-04)  | -9.5 (2019-01)  | -9.5 (2023-01)  |
|                      | Max drawdown (%), dyn (IS)          | -10.2           | -12.1            | -13.1           | -20.1           | -25.1           |
|                      | Max drawdown (%), dyn (OOS)         | -8.9            | -11.2            | -11.3           | -15.8           | -20.1           |
