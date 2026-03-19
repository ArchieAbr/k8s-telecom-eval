import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('docs/wrk_results.csv')
summary = df.groupby('Environment')['Socket Read Errors'].mean().reset_index()

# Setup plot
fig, ax = plt.subplots(figsize=(7, 5))
colors = ['#1f77b4', '#d62728'] # Blue for Cloud, Red for Edge

# Plot bars
bars = ax.bar(summary['Environment'], summary['Socket Read Errors'], color=colors, width=0.5)

# Formatting
ax.set_ylabel('Average Socket Read Errors (Per 60s Test)', fontweight='bold')
ax.set_title('System Failure Mode: Dropped Packets under Saturation', fontweight='bold', pad=15)

# Add values on top with comma formatting
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{int(height):,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Use logarithmic scale if the difference is too massive to read normally
ax.set_yscale('log')
ax.set_ylabel('Average Socket Read Errors (Log Scale)', fontweight='bold')

plt.tight_layout()
plt.savefig('docs/socket_errors_chart.png', dpi=300)
print("Saved Socket Errors chart to docs/socket_errors_chart.png")