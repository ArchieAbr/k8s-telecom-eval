#!/bin/bash
# setup_edge.sh - Installs K3s (Edge Environment)

echo "Installing K3s"
curl -sfL https://get.k3s.io | sh -

echo "Configuring permissions"
sudo chmod 644 /etc/rancher/k3s/k3s.yaml

echo "Done"