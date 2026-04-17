import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyEMD import EMD

# -----------------------------
# 1) Load data
# -----------------------------
# CSV must have columns: Year, Month, Rasht
file_path = "pr_rasht_month.csv"
df = pd.read_csv(file_path)

# Clean column names in case of extra spaces
df.columns = [c.strip() for c in df.columns]

# -----------------------------
# 2) Build a monthly datetime index
# -----------------------------
df["Date"] = pd.to_datetime(
    dict(year=df["Year"], month=df["Month"], day=1)
)
df = df.sort_values("Date").reset_index(drop=True)

# Keep only the precipitation series
ts = df["Rasht"].astype(float).values

# Optional: handle missing values
if np.isnan(ts).any():
    ts = pd.Series(ts).interpolate(limit_direction="both").values

# -----------------------------
# 3) Empirical Mode Decomposition
# -----------------------------
emd = EMD()
imfs = emd.emd(ts)

# Keep only the first 4 IMFs
n_imfs = min(4, imfs.shape[0])
imfs_4 = imfs[:n_imfs]

# If fewer than 4 IMFs are returned, pad with NaNs
if n_imfs < 4:
    pad = np.full((4 - n_imfs, len(ts)), np.nan)
    imfs_4 = np.vstack([imfs_4, pad])

# Residual (trend) if available
residual = ts - np.nansum(imfs_4, axis=0)

# -----------------------------
# 4) Save results
# -----------------------------
out = pd.DataFrame({
    "Date": df["Date"],
    "Original": ts,
    "IMF1": imfs_4[0],
    "IMF2": imfs_4[1],
    "IMF3": imfs_4[2],
    "IMF4": imfs_4[3],
    "Residual": residual
})

out.to_csv("precipitation_imf_decomposition.csv", index=False)

# -----------------------------
# 5) Plot
# -----------------------------
fig, axes = plt.subplots(6, 1, figsize=(10, 8), sharex=True)

axes[0].plot(df["Date"], ts, color="black")
axes[0].set_title("Original Monthly Precipitation in Rasht")
axes[0].set_ylabel("Precipitation [mm]")

for i in range(4):
    axes[i + 1].plot(df["Date"], imfs_4[i], color="tab:blue")
    axes[i + 1].set_title(f"IMF {i+1}")
    axes[i + 1].set_ylabel("Value [-]")

axes[5].plot(df["Date"], residual, color="tab:red")
axes[5].set_title("Residual / Trend [-]")
axes[5].set_ylabel("Value [-]")

plt.tight_layout()
plt.savefig("precipitation_imfs.tiff", dpi=300, bbox_inches="tight")
plt.show()
