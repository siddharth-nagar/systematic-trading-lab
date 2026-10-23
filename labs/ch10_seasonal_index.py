"""Kaufman Chapter 10 — ratio-to-moving-average seasonal index on NIFTY monthly closes.

Descriptive replication of the book's method, not a test and not a trading signal.
Reads the committed NIFTY monthly file; never fills missing months.
Run: python labs/ch10_seasonal_index.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "nifty50_monthly_2000_2026_partial.csv"

df = pd.read_csv(DATA, parse_dates=["month"]).set_index("month").sort_index()
df = df[df.index < "2026-01-01"]
# Reindex to every calendar month so missing months stay NaN and break the moving average.
close = df["close"].reindex(pd.date_range(df.index.min(), df.index.max(), freq="MS"))

# Centred 2x12 moving average: the 12-month average sits between two months,
# so a further 2-month average re-centres it on a month. Needs 13 contiguous closes.
ma12 = close.rolling(12, min_periods=12).mean()
centred_ma = ma12.rolling(2, min_periods=2).mean().shift(-6)

# Step 1: remove the trend -> ratio of price to its centred trend.
ratio = 100 * close / centred_ma
ratios = pd.DataFrame({"ratio": ratio, "calendar_month": ratio.index.month}).dropna()

# Step 2: average the ratios for each calendar month.
# Step 3: normalise so the 12 indices average exactly 100.
raw = ratios.groupby("calendar_month")["ratio"].agg(["count", "mean", "median", "std"])
raw["seasonal_index"] = 100 * raw["mean"] / raw["mean"].mean()
raw.index.name = "month"

assert len(raw) == 12, "Every calendar month needs at least one ratio"
assert abs(raw["seasonal_index"].mean() - 100) < 1e-9

out = HERE / "results"
out.mkdir(exist_ok=True)
raw.to_csv(out / "ch10_seasonal_index.csv", float_format="%.6f")

# Step 4 (deseasonalise): divide price by its month's index. Shown for learning only.
deseasonalised = close / close.index.month.map(raw["seasonal_index"]).to_numpy() * 100

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8))
ax1.bar(raw.index.astype(str), raw["seasonal_index"] - 100)
ax1.axhline(0, color="black", linewidth=0.8)
ax1.set(title="NIFTY 50 ratio-to-moving-average seasonal index (2000–2025), deviation from 100",
        xlabel="Calendar month", ylabel="Index − 100")
ax2.plot(close.index, close, label="Close", linewidth=0.9)
ax2.plot(centred_ma.index, centred_ma, label="Centred 2x12 MA (trend)")
ax2.plot(deseasonalised.index, deseasonalised, label="Deseasonalised close", alpha=0.7)
ax2.set(yscale="log", title="Trend and deseasonalised series", ylabel="Index level (log)")
ax2.legend()
fig.tight_layout()
fig.savefig(out / "ch10_seasonal_index.png", dpi=160)
plt.close(fig)

print(raw.round(3).to_string())
print("\nDescriptive only. Compare with research/001-nifty-seasonality, which found no significant month effect.")
