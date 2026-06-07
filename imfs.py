import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data
stations = ['Tehran', 'Semnan', 'Mashhad', 'Arak', 'Bandar Anzali', 'Rasht']
annual_imfs = {
    'IMF1': [8, 8, 10, 11, 12, 10],
    'IMF2': [22, 19, 22, 24, 26, 19],
    'IMF3': [25, 24, 26, 27, 28, 24],
    'IMF4': [27, 28, 28, 28, 28, 26],
}
monthly_imfs = {
    'IMF1': [55, 46, 51, 65, 42, 39],
    'IMF2': [96, 90, 97, 95, 95, 93],
    'IMF3': [107, 107, 105, 109, 107, 108],
    'IMF4': [117, 116, 116, 117, 113, 116],
}

annual_df = pd.DataFrame(annual_imfs, index=stations)
monthly_df = pd.DataFrame(monthly_imfs, index=stations)
imf_labels = list(annual_imfs.keys())

# Plotting parameters
bar_width = 0.2
x = np.arange(len(stations))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Matplotlib default colors

fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True)

# --- Subplot a: Annual ---
for i, imf in enumerate(imf_labels):
    offset = (i - 1.5) * bar_width  # Center bars
    bars = axes[0].bar(x + offset, annual_df[imf], width=bar_width, label=imf, color=colors[i])
    axes[0].bar_label(bars, label_type='edge', fontsize=8)

axes[0].set_xticks(x)
axes[0].set_xticklabels(stations, rotation=0)
axes[0].set_ylabel('Number of Runs')
axes[0].set_title('a) Annual IMFs')
axes[0].legend(title='IMF')
axes[0].grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Subplot b: Monthly ---
for i, imf in enumerate(imf_labels):
    offset = (i - 1.5) * bar_width  # Center bars
    bars = axes[1].bar(x + offset, monthly_df[imf], width=bar_width, label=imf, color=colors[i])
    axes[1].bar_label(bars, label_type='edge', fontsize=8)

axes[1].set_xticks(x)
axes[1].set_xticklabels(stations, rotation=0)
axes[1].set_ylabel('Number of Runs')
axes[1].set_title('b) Monthly IMFs')
axes[1].grid(True, axis='y', linestyle='--', alpha=0.3)

fig.text(0.5, 0.04, 'Station', ha='center', fontsize=12)
fig.tight_layout(rect=(0,0.05,1,1))
plt.savefig('my_figure.tiff', bbox_inches='tight', dpi=300)
plt.show()

