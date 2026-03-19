import json
import csv

def json_to_csv(json_file, env_name):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Extract bits per second and convert to Gbps
    bps = data['end']['sum_received']['bits_per_second']
    gbps = bps / 1e9

    with open('docs/network_results.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # Header: Env, Throughput(Gbps)
        writer.writerow([env_name, round(gbps, 2)])

# Run it
json_to_csv('docs/iperf_cloud_tcp.json', 'Cloud')
json_to_csv('docs/iperf_edge_tcp.json', 'Edge')