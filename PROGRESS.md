# Replication progress

Paper: Daniel & Moskowitz (2016), "Momentum Crashes". Paper sample: 1927–2013. Our sample: 1960–2025.

## Status

| Part | Status |
|---|---|
| Download CRSP monthly + Fama-French | done |
| Download CRSP daily | running (about 70% done) |
| Monthly momentum portfolios | done, checked against Daniel's |
| Tables 1, 2, 3, 4, 5 (monthly) | done |
| Figure 1 | done |
| Daily portfolios, Figures 2 and 3, daily skewness | waiting for the daily download |
| Dynamic strategy (Figure 5, Table 7) | waiting for the daily download |
| Tables 6, 8–12 | not planned (need VIX swaps, international data, other asset classes) |

The daily part runs on its own as a Slurm job when the download finishes.

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

A test on daily data (1959–1968) also matched: WML correlation 0.997.
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
| Table 1: WML skewness | −4.70 | −4.83 |
| Table 2: worst month | Aug 1932, −74.4% | Aug 1932, −75.1% |
| Table 3 (2): beta change in bear markets | −1.131 (t = −13.4) | −1.136 (t = −13.4) |
| Table 3 (4): extra beta when market goes up | −0.727 (t = −5.6) | −0.790 (t = −4.4) |
| Table 4: loser up-market beta | 0.600 | 0.570 |
| Table 5 (4): bear × variance | −0.397 (t = −5.7) | −0.360 (t = −5.2) |

The worst-15 list is the same months, in almost the same order.

**Result: our code gives the paper's numbers.** The small gaps have two causes:

- We use the 2017 version of Daniel's data, which is slightly different from what the paper used.
- The bear-market flag needs 24 months of market history. Our Fama-French data starts in July 1926,
  so the flag is missing for Jan 1927 – Jun 1928 (18 months). This only matters for this 1927 check.

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

### After the paper (2013–2025)

This is new data the paper never saw.

- WML still earns 17% a year, but with a lower Sharpe ratio (0.50).
- New crashes: Jan 2023 (−36%), Apr 2020 (−29%), Nov 2020 vaccine rally (−27%).
- Bear × variance still predicts crashes (t = −4.4). But there are only 8 bear-market months, so this is a hint, not proof.

## Not the same as the paper

- **Years:** 1960–2025, not 1927–2013. No 1930s, so fewer giant crashes.
- **Data:** CRSP's new CIZ format. Delisting returns are already included in it.
- **Market and risk-free rate:** from the Fama-French data on WRDS. The paper uses the CRSP index for the bear flag. Fama-French's market is built from CRSP, so it's nearly the same.
- **Dynamic strategy:** we also run an out-of-sample version that only uses past data (from 1970). The paper's main version uses the full sample.
- **Table 7:** we run the plain columns (1, 3, 4, 6). We skip the "conditional" columns (2, 5).

## Next

1. Daily download finishes → daily pipeline runs by itself.
2. Fill in the dynamic strategy results here (Figure 5 Sharpe ratios, Table 7).
3. Upload the final data and results to Google Drive.
