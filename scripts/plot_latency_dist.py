import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv('docs/wrk_results.csv')
summary = df.groupby('Environment')[['P50 Latency (ms)', 'P90 Latency (ms)', 'P99 Latency (ms)']].mean().reset_index()

# Setup plot
fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(len(summary['Environment']))
width = 0.25

# Plot bars
bars1 = ax.bar(x - width, summary['P50 Latency (ms)'], width, label='P50 (Median)', color='#2ca02c')
bars2 = ax.bar(x, summary['P90 Latency (ms)'], width, label='P90', color='#ff7f0e')
bars3 = ax.bar(x + width, summary['P99 Latency (ms)'], width, label='P99 (Tail)', color='#d62728')

# Formatting
ax.set_ylabel('Latency (ms)', fontweight='bold')
ax.set_title('Latency Distribution (QoS): Cloud vs Edge', fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(summary['Environment'], fontweight='bold')
ax.legend()

# Add values on top
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('docs/latency_distribution_chart.png', dpi=300)
print("Saved Latency Distribution chart to docs/latency_distribution_chart.png")