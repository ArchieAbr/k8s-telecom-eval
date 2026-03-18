#!/bin/bash
echo "--- Starting Cloud Recovery (Minikube) ---"

# 1. Start Minikube
minikube start

# 2. Re-export the IP variable so it's available for this session
export MINIKUBE_IP=$(minikube ip)
echo "Minikube IP found: $MINIKUBE_IP"

# 3. Clean up old tunnels
pkill -f "port-forward"

# 4. Open Grafana Tunnel
echo "Opening Grafana tunnel on http://192.168.56.104:32000"
minikube kubectl -- port-forward --address 0.0.0.0 svc/k8s-monitor-grafana 32000:80 > /dev/null 2>&1 &

# 5. Find the exact Pod name and Open VNF Tunnel
# This looks for the pod name starting with 'nginx-vnf'
VNF_POD=$(minikube kubectl -- get pods -l app=nginx-vnf -o jsonpath='{.items[0].metadata.name}')
echo "Opening VNF tunnel for Pod: $VNF_POD"
minikube kubectl -- port-forward --address 0.0.0.0 pod/$VNF_POD 30000:80 > /dev/null 2>&1 &

echo "--- Cloud Recovery Complete ---"
echo "You can now run: wrk -t12 -c400 -d60s http://\$MINIKUBE_IP:30000"