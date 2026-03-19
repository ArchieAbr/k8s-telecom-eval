# k8s-telecom-eval
## Performance Evaluation of Kubernetes for Cloud and Edge

**Phase 1:** Environment Setup. Provisioning two Virtual Machines and installing the Kubernetes distributions (e.g., Minikube for Cloud, K3s for Edge).

**Phase 2:** Writing Manifests. Creating the standard Kubernetes YAML files to deploy NGINX load balancer and backend pods. I will apply these to both environments.

# Task B: Environment Setup

## Operating System Selection
Both virtual machines were provisioned using Ubuntu Server 24.04 LTS. This was selected as it is a highly stable, industry-standard Linux distribution for Kubernetes deployments. The server edition was chosen specifically to eliminate the resource overhead of a desktop GUI, simulating headless server environments.

## VM Specifications & Kubernetes Instances

| Environment | Role | CPU | RAM | Storage | K8s Distribution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cloud-like** | Emulates a central data centre environment. | 2 Cores | 6 GB | 25 GB | Minikube (Full K8s) |
| **Edge-like** | Emulates a resource-constrained MEC node. | 1 Core | 2 GB | 15 GB | K3s (Lightweight K8s) |

# Task C: Deploy Network Function(s)

## Deployment Summary
The NGINX Layer 7 Load Balancer was successfully deployed alongside two ultra-lightweight dummy backend pods (`hashicorp/http-echo`). The deployment was executed using a unified declarative YAML manifest that provisioned the Deployments, internal routing Services, an NGINX ConfigMap, and an external NodePort Service (Port 30000).

## Validation
A "Hello World" test was conducted via the host machine using HTTP GET requests (`curl`) directed at the NodePort of both VMs. This successfully validated:
1.  **External Ingress:** The NodePort correctly accepted external traffic.
2.  **VNF Operation:** The NGINX container correctly processed the HTTP request using its injected ConfigMap.
3.  **Internal Routing:** NGINX successfully reverse-proxied the traffic to the internal `dummy-backend` service, which returned the expected "Hello World from the Telecom Backend!" string.

## Complexity Comparison (Cloud vs. Edge)
The declarative nature of Kubernetes meant that the exact same YAML manifest was used for both environments, ensuring high portability. However, there were differences in the command-line execution:
* **Cloud (Minikube):** Required invoking the kubectl binary through the Minikube wrapper (`minikube kubectl --`). The heavier Docker runtime also resulted in a slightly longer initial image pull and pod startup time.
* **Edge (K3s):** Exhibited lower complexity at the command line. K3s operates as a single systemd service with a seamlessly integrated kubectl (`k3s kubectl`). Container startup was noticeably faster due to the lightweight `containerd` runtime optimised for edge environments.

# Task D: Experimental Design and Performance Monitoring

## Traffic Scenarios and Parameters
To evaluate the performance of the NGINX VNF, a custom asynchronous Python workload generator was developed using the `aiohttp` library. This allowed for high-concurrency HTTP GET requests simulating realistic, sustained user traffic hitting the edge load balancer.

## Metric Collection Methodology
1.  **Latency and Throughput:** Collected directly by the Python script. The script recorded the precise start and end times of every successful HTTP 200 OK response, calculating the total throughput (requests per second), average latency, and the 95th percentile latency. Results were automatically appended to a CSV file.

## Resuming Work (Cold Boot Sequence)
If the host machine has been turned off or the VMs restarted, run these steps to restore the testing environments:

### 1. Cloud Environment
SSH into the Cloud VM and wake up the Minikube cluster:
```bash
minikube start
minikube kubectl -- get pods # Verify everything is Running
# Re-establish Grafana UI tunnel
minikube kubectl -- port-forward --address 0.0.0.0 svc/k8s-monitor-grafana 32000:80 &
```
### 2. Edge Environment
SSH into the Edge VM. K3s runs as a systemd service, so the cluster starts automatically on boot. Simply restore the tunnel:

```bash
sudo k3s kubectl get pods # Verify everything is Running
# Re-establish Grafana UI tunnel
sudo k3s kubectl port-forward --address 0.0.0.0 svc/k8s-monitor-grafana 32000:80 &
```
