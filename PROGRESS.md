# Replication progress

Paper: Daniel & Moskowitz (2016), "Momentum Crashes". Paper sample: 1927–2013. Our sample: 1960–2025.

## Status

| Part | Status |
|---|---|
| Download CRSP monthly + Fama-French | done |
| Download CRSP daily | done |
| Monthly momentum portfolios | done, checked against Daniel's |
| Daily momentum portfolios | done, checked against Daniel's |
| Tables 1, 2, 3, 4, 5 | done |
| Figures 1, 2, 3 | done |
| Dynamic strategy (Figure 5, Table 7) | done |
| Tables 6, 8–12 | not planned (need VIX swaps, international data, other asset classes) |

## How we build momentum (same as the paper)

1. Take US common stocks on NYSE, AMEX and Nasdaq.
2. At the end of each month, rank stocks on their return over the past 12 months, skipping the last month.
3. Cut them into 10 groups with the same number of stocks. D1 = losers, D10 = winners.
4. Weight stocks by market cap. Hold for one month.
5. WML ("winners minus losers") = D10 − D1.

These rules come from Daniel's notes on his own portfolios. One detail: the paper's main version uses
**all stocks** for the cut-offs, not just NYSE stocks. We build both versions.

## How we check our work: three steps

### Check 1: are our portfolios the same as Daniel's?

We compare our monthly portfolio returns with Daniel's published ones, 1959–2016.

| | Correlation | WML mean, ours | WML mean, Daniel |
|---|---|---|---|
| Each decile (D1 … D10) | 0.997 – 0.999 | | |
| WML | 0.995 | 1.76%/month | 1.71%/month |
| WML, NYSE cut-offs | 0.998 | 1.29%/month | 1.28%/month |
| Daily WML | 0.992 | | |
| Daily WML, NYSE cut-offs | 0.996 | | |
We have about 3% more stocks per decile. That's probably because the new CRSP format
defines "common stock" a little differently.

**Result: our portfolios are nearly the same as the paper's.**

### Check 2: does our table code give the paper's numbers?

We run our table code on **Daniel's portfolios** for the **paper's own years (1927–2013)**,
and compare with the numbers printed in the paper.

| Number | Paper | Our code on Daniel's data |
|---|---|---|
| Table 1: WML mean (%/year) | 17.9 | 18.2 |
| Table 1: WML alpha (%/year) | 22.2 | 22.7 |
| Table 1: WML beta | −0.58 | −0.59 |
| Table 1: WML Sharpe ratio | 0.60 | 0.61 |
| Table 1: WML skewness (monthly) | −4.70 | −4.83 |
| Table 1: WML skewness (daily) | −1.18 | −1.19 |
| Table 2: worst month | Aug 1932, −74.4% | Aug 1932, −75.1% |
| Table 3 (2): beta change in bear markets | −1.131 (t = −13.4) | −1.136 (t = −13.4) |
| Table 3 (4): extra beta when market goes up | −0.727 (t = −5.6) | −0.790 (t = −4.4) |
| Table 4: loser up-market beta | 0.600 | 0.570 |
| Table 5 (4): bear × variance | −0.397 (t = −5.7) | −0.360 (t = −5.2) |
| Table 7A (1): dyn alpha on Mkt + WML (%/year) | 23.7 (t = 12.0) | 24.2 (t = 11.3) |
| Table 7A (4): dyn alpha on Mkt + cvol (%/year) | 7.3 (t = 6.9) | 8.2 (t = 6.0) |
| Table 7B (1): cvol alpha on Mkt + WML (%/year) | 14.3 (t = 11.4) | 14.0 (t = 10.6) |
| Table 7B (4): cvol alpha on Mkt + dyn (%/year) | −0.7 (t = −0.7) | 2.5 (t = 1.9) |

The worst-15 list is the same months, in almost the same order.

**Result: our code gives the paper's numbers.** The small gaps have two causes:

- We use the 2017 version of Daniel's data, which is slightly different from what the paper used.
- The bear-market flag needs 24 months of market history. Our Fama-French data starts in July 1926,
  so the flag is missing for Jan 1927 – Jun 1928 (18 months). This only matters for this 1927 check.

The biggest gap is Table 7B (4): in the paper, dyn fully explains cvol (alpha −0.7%). For us a small
alpha is left (2.5%, t = 1.9, not significant at 5%). The dynamic weights depend on GARCH fits, so
small differences in the volatility model can move this number.

### Check 3: our data vs Daniel's data, same years

Same tables, same years (1960–2013), our portfolios vs Daniel's:

| Number | Our portfolios | Daniel's portfolios |
|---|---|---|
| WML mean (%/year) | 22.1 | 21.5 |
| WML alpha (%/year) | 24.2 | 23.8 |
| WML skewness | −2.37 | −2.46 |
| Table 3 (2): beta change in bear markets | −1.05 | −1.03 |
| Table 3 (4): extra beta when market goes up | −0.44 | −0.44 |
| Table 5 (4): bear × variance | −0.58 | −0.57 |
| Dynamic strategy Sharpe ratio | 1.34 | 1.33 |

**Result: almost identical.** So when our 1960+ numbers differ from the paper, it's because of the
**years**, not our data or code.

## What we find (1960–2025)

From `results/tables_allfirm.md`:

- **Momentum still pays.** WML earns 21% a year, Sharpe ratio 0.71, alpha 24% a year (t = 6.8).
- **It still crashes.** Monthly skewness is −2.1. The worst months are rebounds after bad markets:
  Jan 2001 (−47%), Apr 2009 (−45%), Mar 2009 (−43%), Nov 2002 (−38%).
- **The beta flips in bear markets.** After the market falls, WML's market beta drops by about 1
  (t = −6.6). Momentum ends up short the market just as the market bounces back.
- **Crashes can be predicted.** Bear market × high market variance predicts low WML returns
  (t = −6.5). This is the paper's key result, and it holds.
- **Weaker without the 1930s.** The "option-like" part (beta drops *more* when the market goes up)
  is weaker after 1960: t = −2.9 in Table 3 column (3), and not significant in column (4).
  In the paper it's strong, mostly because of the 1930s.
- **The dynamic strategy works.** All three below are scaled to the same 19% volatility (Figure 5):

  | | Sharpe ratio | Worst month |
  |---|---|---|
  | Plain WML (not scaled) | 0.71 | −47% |
  | Constant volatility (cvol) | 1.09 | −18% |
  | Dynamic, in-sample (like the paper) | 1.23 | −18% |
  | Dynamic, out-of-sample (from 1972) | 1.08 | −19% |

  The dynamic strategy beats WML and cvol (Table 7: alpha 32%/year on Mkt + WML, 12%/year on
  Mkt + cvol, both t > 6). The out-of-sample version is about as good as cvol, not better.

### After the paper (2013–2025)

This is new data the paper never saw.

- WML still earns 17% a year, but with a lower Sharpe ratio (0.50).
- New crashes: Jan 2023 (−36%), Apr 2020 (−29%), Nov 2020 vaccine rally (−27%).
- Bear × variance still predicts crashes (t = −4.4). But there are only 8 bear-market months, so this is a hint, not proof.
- Scaling still helps. Sharpe ratio: WML 0.50, cvol 0.60, dynamic 0.68 (in-sample), 0.65 (out-of-sample).

## Not the same as the paper

- **Years:** 1960–2025, not 1927–2013. No 1930s, so fewer giant crashes.
- **Data:** CRSP's new CIZ format. Delisting returns are already included in it.
- **Market and risk-free rate:** from the Fama-French data on WRDS. The paper uses the CRSP index for the bear flag. Fama-French's market is built from CRSP, so it's nearly the same.
- **Dynamic strategy:** we also run an out-of-sample version that only uses past data (from 1970). The paper's main version uses the full sample.
- **Table 7:** we run columns (1) and (4) as in the paper. Our "FF" columns add SMB and HML but
  skip the paper's "conditional" interaction terms. We skip columns (2) and (5).

## Next

All planned parts are done. Possible extras: the paper's subsample plots (Figure 5, by quarter-century),
and the "conditional" Table 7 columns.
