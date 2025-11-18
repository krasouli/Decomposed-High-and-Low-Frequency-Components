import matplotlib.pyplot as plt
import numpy as np

# Data setup
stations = ['Tehran', 'Semnan', 'Mashhad', 'Arak', 'B Anzali', 'Rasht']
models = ['SVR', 'Regression Tree']
metrics = ['RRMSE', 'NRMSE', 'RPD', 'VAF', 'AMAPE', 'P', 'S']

# Data dictionary with all metrics
data = {
    'RRMSE': {
        'Tehran': [0.82, 0.942],
        'Semnan': [0.941, 1.045],
        'Mashhad': [0.863, 0.8],
        'Arak': [0.9, 0.98],
        'B Anzali': [0.52, 0.54],
        'Rasht': [0.56, 0.54]
    },
    'NRMSE': {
        'Tehran': [0.26, 0.297],
        'Semnan': [0.251, 0.279],
        'Mashhad': [0.278, 0.26],
        'Arak': [0.224, 0.24],
        'B Anzali': [0.22, 0.23],
        'Rasht': [0.29, 0.27]
    },
    'RPD': {
        'Tehran': [1.25, 1.09],
        'Semnan': [1.26, 1.13],
        'Mashhad': [1.15, 1.24],
        'Arak': [1.34, 1.23],
        'B Anzali': [1.22, 1.18],
        'Rasht': [1.05, 1.1]
    },
    'VAF': {
        'Tehran': [0.36, 0.21],
        'Semnan': [0.67, 0.27],
        'Mashhad': [0.39, 0.39],
        'Arak': [0.5, 0.45],
        'B Anzali': [0.38, 0.32],
        'Rasht': [0.057, 0.14]
    },
    'AMAPE': {
        'Tehran': [0.66, 0.81],
        'Semnan': [0.73, 0.86],
        'Mashhad': [0.72, 0.67],
        'Arak': [0.69, 0.8],
        'B Anzali': [0.43, 0.44],
        'Rasht': [0.47, 0.43]
    },
    'P': {
        'Tehran': [0.79, 0.7],
        'Semnan': [0.7, 0.7],
        'Mashhad': [0.7, 0.79],
        'Arak': [0.75, 0.66],
        'B Anzali': [0.7, 0.7],
        'Rasht': [0.5, 0.58]
    },
    'S': {
        'Tehran': [0.65, 0.6],
        'Semnan': [0.84, 0.63],
        'Mashhad': [0.74, 0.81],
        'Arak': [0.7, 0.7],
        'B Anzali': [0.8, 0.8],
        'Rasht': [0.55, 0.8]
    }
}

# Create figure with subplots (3 rows, 3 columns, with one empty subplot)
fig, axes = plt.subplots(4, 2, figsize=(12, 10))
axes = axes.flatten()

# Colors for models
colors = ['red','black']  # Blue for SVR, Orange for Tree
bar_width = 0.35
x = np.arange(len(stations))

# Labels for subplots
subplot_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)']

# Plot each metric
for i, metric in enumerate(metrics):
    ax = axes[i]
    
    # Extract data for current metric
    svr_values = [data[metric][station][0] for station in stations]
    tree_values = [data[metric][station][1] for station in stations]
    
    # Create grouped bar chart
    if i==0:
        ax.bar(x - bar_width/2, svr_values, bar_width, label='SVR', color=colors[0], alpha=0.8)
        ax.bar(x + bar_width/2, tree_values, bar_width, label='Regression Tree', color=colors[1], alpha=0.8)
    else:
        ax.bar(x - bar_width/2, svr_values, bar_width, color=colors[0], alpha=0.8)
        ax.bar(x + bar_width/2, tree_values, bar_width, color=colors[1], alpha=0.8)
    
    # Customize subplot
    #ax.set_title(f'{metric}', fontsize=14, fontweight='bold')
    #ax.set_xlabel('Stations', fontsize=12)
    ax.set_ylabel(metric, fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(stations, rotation=0, ha='center')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add subplot label (a), (b), (c), etc.
    ax.text(-0.1, 1.02, subplot_labels[i], transform=ax.transAxes,
            fontsize=14, fontweight='bold')
    
    # Add values on top of bars
    for j, (svr_val, tree_val) in enumerate(zip(svr_values, tree_values)):
        ax.text(j - bar_width/2, svr_val + max(svr_values + tree_values) * 0.01, 
                f'{svr_val:.2f}', ha='center', va='bottom', fontsize=8)
        ax.text(j + bar_width/2, tree_val + max(svr_values + tree_values) * 0.01, 
                f'{tree_val:.2f}', ha='center', va='bottom', fontsize=8)

# Remove the empty subplot (8th position)
fig.delaxes(axes[7])

# Add overall title
#fig.suptitle('SVR vs Tree Model Performance Comparison Across Multiple Metrics', 
#             fontsize=16, fontweight='bold', y=0.98)

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(top=0.93)

# Save and show
plt.savefig('svr_vs_tree_comparison.tiff', dpi=300, bbox_inches='tight')
plt.show()

print("SVR vs Tree comparison chart saved as 'svr_vs_tree_comparison.png'")

