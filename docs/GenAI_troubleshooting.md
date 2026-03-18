# GenAI Troubleshooting Log

| Problem | Proposed AI Solution | Did it work? |
| :--- | :--- | :--- |
| **Boot Error:** `VERR_INTNET_FLT_IF_NOT_FOUND` when starting `k8s-cloud-vm` due to Host-Only adapter failure. | 1. Verified Host-Only network exists in VirtualBox global Network Manager.<br>2. Opened Windows Network Connections (`ncpa.cpl`), verified `VirtualBox NDIS6` driver was ticked, and restarted the adapter. | Yes |


| **Script Execution Halt:** `setup_cloud.sh` stopped executing after installing Docker. | 1. Identified `newgrp docker` command spawns a new shell, abandoning the script.<br>2. Manually executed the remaining Minikube installation commands in the active terminal. | Yes |

| **Connectivity Failure:** `curl` command to Cloud VM NodePort failed with "Couldn't connect to server". | 1. Diagnosed issue as Minikube Docker driver network isolation (network within a network).<br>2. Applied `kubectl port-forward --address 0.0.0.0` to bridge the Ubuntu host network interface with the internal Minikube cluster network. | Yes |

| **Manifest Pull Error:** `kubectl apply -k` failed with `evalsymlink failure` when trying to pull Prometheus CRDs from GitHub. | 1. Diagnosed as a `kubectl` remote URL kustomize quirk.<br>2. Proceeded with the `helm install` command, as the `kube-prometheus-stack` chart natively bundles necessary CRDs as a fallback. Verified successful deployment via pod status. | Yes |
