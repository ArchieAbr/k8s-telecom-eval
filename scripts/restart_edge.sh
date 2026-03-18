#!/bin/bash
echo "--- Starting Edge Recovery (K3s) ---"

# 1. Restart K3s service to clear any 'TLS handshake' or 'soft lockup' hangs
sudo systemctl restart k3s

# 2. Wait for API server to respond
echo "Waiting for K3s API to wake up..."
sleep 15

# 3. Clean up old tunnels
sudo pkill -f "port-forward"

# 4. Open Grafana Tunnel (Port 32000)
echo "Opening Edge Grafana on http://192.168.56.105:32000"
sudo k3s kubectl port-forward --address 0.0.0.0 svc/k8s-monitor-grafana 32000:80 > /dev/null 2>&1 &

# 5. The Edge VNF is NodePort 30000, so it is natively open on the VM IP. 
# No tunnel needed for VNF traffic on Edge!

echo "--- Edge Recovery Complete ---"