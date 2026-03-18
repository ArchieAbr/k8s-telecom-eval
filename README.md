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