import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_graphs(csv_path="docs/performance_results.csv", output_dir="docs/graphs"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: {csv_path} not found. Run tests first!")
        return

    # Clean up column names for easier reference
    df.columns = df.columns.str.strip()

    # Set visual style
    sns.set_theme(style="whitegrid")

    # 1. Throughput Comparison Chart
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x="Concurrency", y="Throughput (req/s)", hue="Environment", palette=["#3498db", "#e74c3c"])
    plt.title("VNF Throughput: Cloud vs Edge", fontsize=14, fontweight="bold")
    plt.ylabel("Throughput (Requests / Second)")
    plt.xlabel("Concurrent Connections")
    plt.savefig(f"{output_dir}/throughput_comparison.png", dpi=300)
    plt.close()

    # 2. P95 Latency Comparison Chart
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=df, x="Concurrency", y="P95 Latency (ms)", hue="Environment", palette=["#3498db", "#e74c3c"])
    plt.title("VNF 95th Percentile Latency: Cloud vs Edge", fontsize=14, fontweight="bold")
    plt.ylabel("P95 Latency (Milliseconds) - Lower is Better")
    plt.xlabel("Concurrent Connections")
    plt.savefig(f"{output_dir}/latency_comparison.png", dpi=300)
    plt.close()

    print(f"Graphs successfully generated in {output_dir}/")

if __name__ == "__main__":
    generate_graphs()