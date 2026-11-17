"""Step 1: download CRSP and Fama-French data from the WRDS web API.

    python src/download.py monthly   # crsp.msf_v2, one file per year
    python src/download.py daily     # crsp.dsf_v2, one file per month
    python src/download.py ff        # Fama-French factors, monthly and daily

Files are saved in data/raw/<table>/. Files that already exist are skipped,
so you can re-run the script to resume. Your WRDS API token must be in
~/.wrds_api_token.

Two things to know about the WRDS API:
  * Only date filters work, so we download all securities and pick stocks later.
  * The "count" it reports is too high, so we keep paging until a page comes back short.
"""
import argparse
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests

from config import RAW

API = "https://wrds-api.wharton.upenn.edu/data"
PAGE_SIZE = 50_000
FIRST_MONTH, LAST_MONTH = "1958-01", "2025-12"

# Columns we use later to pick common stocks on NYSE/AMEX/Nasdaq
STOCK_FILTER_COLUMNS = ["primaryexch", "sharetype", "securitytype", "securitysubtype",
                        "usincflg", "issuertype", "conditionaltype", "tradingstatusflg"]

TABLES = {
    "monthly": {
        "table": "crsp.msf_v2", "date": "mthcaldt", "chunk": "year",
        "columns": ["permno", "mthcaldt", "mthret", "mthretx", "mthprc", "shrout",
                    "mthcap", "mthprevcap", "mthdelflg", "siccd"] + STOCK_FILTER_COLUMNS,
    },
    "daily": {
        "table": "crsp.dsf_v2", "date": "dlycaldt", "chunk": "month",
        "columns": ["permno", "dlycaldt", "dlyret", "dlyprc", "shrout", "dlycap",
                    "dlyprevcap", "dlydelflg"] + STOCK_FILTER_COLUMNS,
    },
}

session = requests.Session()


def api_get(url, params, tries=8):
    """GET one page, retrying with back-off on network or server errors."""
    for attempt in range(tries):
        try:
            r = session.get(url, params=params, timeout=600)
            if r.status_code == 200:
                return r.json()
            problem = f"HTTP {r.status_code}"
        except (requests.RequestException, ValueError) as e:
            problem = repr(e)
        wait = min(2 ** attempt, 120)
        print(f"  retry {attempt + 1}/{tries} in {wait}s ({problem})", file=sys.stderr, flush=True)
        time.sleep(wait)
    raise RuntimeError(f"failed: {url} {params}")


def download_range(table, date_col, start, end, order):
    """All rows with start <= date <= end, one page at a time."""
    url = f"{API}/{table}/"
    params = {f"{date_col}__gte": start, f"{date_col}__lte": end,
              "ordering": order, "limit": PAGE_SIZE}
    rows, offset = [], 0
    while True:
        page = api_get(url, {**params, "offset": offset})["results"]
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            return pd.DataFrame(rows)
        offset += PAGE_SIZE


def chunks(spec):
    """(file name, first day, last day) for each file we save."""
    months = pd.period_range(FIRST_MONTH, LAST_MONTH, freq="M")
    if spec["chunk"] == "year":
        return [(f"{y}", f"{y}-01-01", f"{y}-12-31") for y in sorted({m.year for m in months})]
    return [(m.strftime("%Y%m"), m.start_time.date().isoformat(), m.end_time.date().isoformat())
            for m in months]


def save_chunk(spec, name, start, end):
    path = RAW / spec["table"] / f"{name}.parquet"
    if path.exists():
        return None
    df = download_range(spec["table"], spec["date"], start, end, f"permno,{spec['date']}")
    if len(df):
        df = df[spec["columns"]]
        if df.duplicated(["permno", spec["date"]]).any():
            raise RuntimeError(f"duplicate rows in {spec['table']} {name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)   # only complete files get the .parquet name
    return len(df)


def download_crsp(kind, workers):
    spec = TABLES[kind]
    todo = chunks(spec)
    start = time.time()
    with ThreadPoolExecutor(workers) as pool:
        jobs = {pool.submit(save_chunk, spec, *c): c[0] for c in todo}
        for i, job in enumerate(as_completed(jobs), 1):
            n = job.result()
            print(f"{kind} {jobs[job]} rows={'cached' if n is None else n} "
                  f"[{i}/{len(todo)}, {time.time() - start:.0f}s]", flush=True)


def download_ff():
    (RAW / "ff").mkdir(parents=True, exist_ok=True)
    for table in ["ff.factors_monthly", "ff.factors_daily"]:
        df = download_range(table, "date", "1926-01-01", "2030-12-31", "date")
        df.to_parquet(RAW / "ff" / f"{table.split('.')[1]}.parquet", index=False)
        print(table, len(df), df["date"].min(), df["date"].max(), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("what", choices=["monthly", "daily", "ff"])
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    with open(os.path.expanduser("~/.wrds_api_token")) as f:
        token = f.read().strip()
    session.headers.update({"Authorization": f"Token {token}",
                            "Accept": "application/json"})
    if args.what == "ff":
        download_ff()
    else:
        download_crsp(args.what, args.workers)
