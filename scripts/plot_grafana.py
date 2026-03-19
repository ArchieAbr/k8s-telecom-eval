import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_averaged_grafana_data(file_prefix, metric_type):
    all_dfs = []
    
    # Loop through runs 1, 2, and 3
    for i in range(1, 4):
        filepath = f"docs/{file_prefix}_{i}.csv"
        try:
            df = pd.read_csv(filepath)
            metric_col = df.columns[1] # The actual metric values
            
            # Convert timestamp strings to actual datetime objects
            df['Time'] = pd.to_datetime(df['Time'])
            
            # Normalize time to "Seconds from start" so we can overlay the 3 runs perfectly
            start_time = df['Time'].min()
            df['Relative_Seconds'] = (df['Time'] - start_time).dt.total_seconds()
            
            # Clean up the metric values (remove "MiB", convert to float)
            if metric_type == 'memory':
                df['Value'] = df[metric_col].astype(str).str.extract(r'([\d\.]+)').astype(float)
            else:
                df['Value'] = df[metric_col].astype(float)
                
            all_dfs.append(df[['Relative_Seconds', 'Value']])
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Skipping.")
            continue
            
    if not all_dfs:
        print(f"No data found for {file_prefix}. Returning empty DataFrame.")
        return pd.DataFrame({'Relative_Seconds': [], 'Value': []})
        
    # Combine all 3 runs into one giant table
    combined_df = pd.concat(all_dfs)
    
    # Round the relative seconds to the nearest 5-second mark (to match Grafana's scrape interval)
    combined_df['Relative_Seconds_Rounded'] = (combined_df['Relative_Seconds'] / 5).round() * 5
    
    # Calculate the average (mean) value for each 5-second interval across all 3 runs
    averaged_df = combined_df.groupby('Relative_Seconds_Rounded')['Value'].mean().reset_index()
    averaged_df = averaged_df.rename(columns={'Relative_Seconds_Rounded': 'Relative_Seconds'})
    
    return averaged_df

# 1. Process and Average the Data
cloud_cpu = get_averaged_grafana_data('Cloud_Sat_Test_CPU', 'cpu')
edge_cpu = get_averaged_grafana_data('Edge_Sat_Test_CPU', 'cpu')
cloud_mem = get_averaged_grafana_data('Cloud_Sat_Test_Mem', 'memory')
edge_mem = get_averaged_grafana_data('Edge_Sat_Test_Mem', 'memory')

# 2. Plot the Averaged Data
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# --- CPU Plot ---
ax1.plot(cloud_cpu['Relative_Seconds'], cloud_cpu['Value'], label='Cloud (Minikube) - 3 Run Avg', color='blue', linewidth=2)
ax1.plot(edge_cpu['Relative_Seconds'], edge_cpu['Value'], label='Edge (K3s) - 3 Run Avg', color='red', linewidth=2)
ax1.set_title('Average CPU Usage During Saturation Test', fontweight='bold')
ax1.set_ylabel('CPU Usage (Cores)', fontweight='bold')
ax1.set_xlabel('Time Since Test Start (Seconds)', fontweight='bold')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.7)

# --- Memory Plot ---
ax2.plot(cloud_mem['Relative_Seconds'], cloud_mem['Value'], label='Cloud (Minikube) - 3 Run Avg', color='blue', linewidth=2)
ax2.plot(edge_mem['Relative_Seconds'], edge_mem['Value'], label='Edge (K3s) - 3 Run Avg', color='red', linewidth=2)
ax2.set_title('Average Memory Usage During Saturation Test', fontweight='bold')
ax2.set_ylabel('Working Set Memory (MiB)', fontweight='bold')
ax2.set_xlabel('Time Since Test Start (Seconds)', fontweight='bold')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

# Save the final chart
plt.tight_layout()
plt.savefig('docs/averaged_resource_usage_chart.png', dpi=300)
print("Saved averaged Grafana resource chart to docs/averaged_resource_usage_chart.png")