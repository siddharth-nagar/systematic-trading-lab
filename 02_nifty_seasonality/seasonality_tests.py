"""NIFTY neutral omnibus month-effect test. Not a trading system.

No online fetch; reads the committed monthly file. Requires pandas, numpy.
Usage: python 02_nifty_seasonality/seasonality_tests.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "data/nifty50_monthly_2000_2026_partial.csv")
df["month"] = pd.to_datetime(df["month"])
df = df.sort_values("month")
month_code = df["month"].dt.year * 12 + df["month"].dt.month
month_gap = month_code.diff()
assert df.loc[month_gap.ne(1), "return_pct"].isna().all(), "Returns span missing calendar month"
df = df.loc[(df["month"] < "2026-01-01") & df["return_pct"].notna()].copy()
df["year"] = df["month"].dt.year
df["calendar_month"] = df["month"].dt.month

def f_stat(data):
    mean_all = data["return_pct"].mean()
    groups = [grp["return_pct"].to_numpy() for _, grp in data.groupby("calendar_month")]
    n = sum(len(g) for g in groups)
    between = sum(len(g)*(g.mean()-mean_all)**2 for g in groups)
    within = sum(((g-g.mean())**2).sum() for g in groups)
    return (between/(len(groups)-1))/(within/(n-len(groups)))

observed = f_stat(df)
rng = np.random.default_rng(7273)
n_perm = 5000
# Permute VALUES within each year, leaving the calendar-month labels and missingness fixed.
by_year = [np.flatnonzero(df["year"].to_numpy()==yr) for yr in sorted(df["year"].unique())]
returns = df["return_pct"].to_numpy()
calendar = df["calendar_month"].to_numpy()
unique_months = range(1, 13)
grand = returns.mean()
def fast_f(arr):
    between = 0.
    within = 0.
    for m in unique_months:
        g = arr[calendar==m]
        gm = g.mean()
        between += len(g)*(gm-grand)**2
        within += ((g-gm)**2).sum()
    return (between/11)/(within/(len(arr)-12))
assert np.isclose(observed, fast_f(returns))
at_least_as_large = 0
for _ in range(n_perm):
    new = returns.copy()
    for ix in by_year:
        new[ix] = rng.permutation(new[ix])
    if fast_f(new) >= observed:
        at_least_as_large += 1
p = (at_least_as_large + 1)/(n_perm + 1)

summary = pd.DataFrame([{
    "n_monthly_observations": len(df),
    "unconditional_mean_pct": returns.mean(),
    "observed_f": observed,
    "permutations": n_perm,
    "random_seed": 7273,
    "permutation_p": p
}])
summary.to_csv(HERE/"results"/"omnibus_test.csv", index=False)

df["period"] = np.where(df["year"]<=2012,"2000-2012","2013-2025")
subperiod = df.groupby(["period","calendar_month"])["return_pct"].agg(["count","mean","median","std"]).reset_index()
subperiod.to_csv(HERE/"results"/"subperiod_means.csv", index=False)

print(summary.to_string(index=False))
print("Exploratory only; not official-source validated or a trading signal.")
