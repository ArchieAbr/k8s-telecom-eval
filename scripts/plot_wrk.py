import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
df = pd.read_csv('docs/wrk_results.csv')

# Calculate the averages for Cloud vs Edge
summary = df.groupby('Environment')[['Throughput (req/s)', 'Avg Latency (ms)']].mean().reset_index()

fig, ax1 = plt.subplots(figsize=(8, 6))

# Define bar positions
x = np.arange(len(summary['Environment']))
width = 0.35

# Plot Throughput on primary Y axis
bars1 = ax1.bar(x - width/2, summary['Throughput (req/s)'], width, label='Throughput (req/s)', color='#1f77b4')
ax1.set_ylabel('Throughput (Requests / Second)', color='#1f77b4', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1f77b4')

# Create secondary Y axis for Latency
ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, summary['Avg Latency (ms)'], width, label='Avg Latency (ms)', color='#ff7f0e')
ax2.set_ylabel('Average Latency (ms)', color='#ff7f0e', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#ff7f0e')

# Labels and Title
ax1.set_xticks(x)
ax1.set_xticklabels(summary['Environment'])
plt.title('VNF Saturation Test: Cloud vs Edge Performance', fontweight='bold', pad=15)

# Add values on top of bars
for bar in bars1:
    ax1.annotate(f'{bar.get_height():.0f}',
                 xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
for bar in bars2:
    ax2.annotate(f'{bar.get_height():.0f}',
                 xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

plt.tight_layout()
plt.savefig('docs/wrk_comparison_chart.png', dpi=300)
print("Saved wrk comparison chart to docs/wrk_comparison_chart.png")