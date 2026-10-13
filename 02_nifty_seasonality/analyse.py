"""Reproduce monthly seasonality statistics from repository's recorded monthly data.
Run: python 02_nifty_seasonality/analyse.py
Requires pandas and matplotlib. Does not download or modify price data.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
df = pd.read_csv(HERE / "data" / "nifty50_monthly_2000_2026_partial.csv",
                 parse_dates=["month"], dtype={"year_complete": bool})
df = df.sort_values("month")
assert df["month"].is_unique, "Duplicate months"
study = df[(df["month"] < pd.Timestamp("2026-01-01")) & df["return_pct"].notna()].copy()
study["calendar_month"] = study["month"].dt.month

def metrics(s):
    return pd.Series({
        "n": int(s.count()), "mean_pct": s.mean(), "median_pct": s.median(),
        "positive_count": int(s.gt(0).sum()),
        "positive_frequency_pct": 100*s.gt(0).sum()/s.count(),
        "std_pct": s.std(ddof=1), "min_pct": s.min(), "max_pct": s.max()
    })
monthly = study.groupby("calendar_month")["return_pct"].apply(metrics).unstack()
monthly.index.name = "month"
monthly.to_csv(HERE / "results" / "monthly_seasonality.csv")

study["year"] = study["month"].dt.year
study["sample"] = study["year"].map(lambda x: "2000-2012" if x<=2012 else "2013-2025")
sub = study.groupby(["sample", "calendar_month"])["return_pct"].apply(metrics).unstack()
sub.to_csv(HERE / "results" / "subperiods.csv")

annual = study.pivot(index="year", columns="calendar_month", values="return_pct")
annual.to_csv(HERE / "results" / "year_month_matrix.csv")

fig, ax = plt.subplots(figsize=(11,5))
ax.bar(monthly.index.astype(str), monthly["mean_pct"])
ax.axhline(0, color="black", linewidth=0.8)
ax.set(title="NIFTY 50: mean monthly price-index returns (2000–2025)",
       xlabel="Calendar month", ylabel="Mean return (%)")
fig.tight_layout()
fig.savefig(HERE / "results" / "mean_monthly_returns.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(11,5))
ax.plot(monthly.index, monthly["positive_frequency_pct"], marker="o")
ax.set(xticks=range(1,13), ylim=(0,100),
       title="NIFTY 50: frequency of positive monthly returns", ylabel="Frequency (%)", xlabel="Month")
fig.tight_layout()
fig.savefig(HERE / "results" / "positive_frequency.png", dpi=160)
plt.close(fig)

print(monthly.round(2).to_string())
print("\nResults written into results/. No optimisation or trading P&L performed.")
