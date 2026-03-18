import asyncio
import aiohttp
import time
import csv
import statistics
import argparse
from datetime import datetime

async def fetch(session, url, latencies):
    start_time = time.perf_counter()
    try:
        async with session.get(url, timeout=5) as response:
            await response.read()
            if response.status == 200:
                end_time = time.perf_counter()
                latencies.append((end_time - start_time) * 1000) # Convert to milliseconds
                return True
    except Exception:
        return False
    return False

async def worker(session, url, duration, latencies, success_count):
    end_time = time.time() + duration
    while time.time() < end_time:
        success = await fetch(session, url, latencies)
        if success:
            success_count[0] += 1

async def main(target_url, environment, duration, concurrency):
    print(f"Starting test on {environment} environment: {target_url}")
    print(f"Parameters: {duration} seconds, {concurrency} concurrent connections.")
    
    latencies = []
    success_count = [0]
    
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _ in range(concurrency):
            task = asyncio.create_task(worker(session, target_url, duration, latencies, success_count))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

    # Calculate metrics
    total_requests = success_count[0]
    throughput = total_requests / duration
    
    if latencies:
        min_lat = min(latencies)
        max_lat = max(latencies)
        avg_lat = statistics.mean(latencies)
        p95_lat = statistics.quantiles(latencies, n=100)[94] if len(latencies) > 100 else max_lat
    else:
        min_lat = max_lat = avg_lat = p95_lat = 0

    print("\n--- Test Results ---")
    print(f"Total Successful Requests: {total_requests}")
    print(f"Throughput: {throughput:.2f} req/sec")
    print(f"Average Latency: {avg_lat:.2f} ms (95th Percentile: {p95_lat:.2f} ms)")

    # Save to CSV
    filename = "docs/performance_results.csv"
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Environment', 'Duration (s)', 'Concurrency', 'Total Requests', 'Throughput (req/s)', 'Avg Latency (ms)', 'P95 Latency (ms)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Environment': environment,
            'Duration (s)': duration,
            'Concurrency': concurrency,
            'Total Requests': total_requests,
            'Throughput (req/s)': round(throughput, 2),
            'Avg Latency (ms)': round(avg_lat, 2),
            'P95 Latency (ms)': round(p95_lat, 2)
        })
    print(f"\nResults appended to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTTP traffic for VNF evaluation.")
    parser.add_argument("--url", required=True, help="Target URL (e.g., http://192.168.56.102:30000)")
    parser.add_argument("--env", required=True, help="Environment name (e.g., Cloud, Edge)")
    parser.add_argument("--duration", type=int, default=30, help="Test duration in seconds")
    parser.add_argument("--concurrency", type=int, default=50, help="Number of concurrent connections")
    
    args = parser.parse_args()
    asyncio.run(main(args.url, args.env, args.duration, args.concurrency))