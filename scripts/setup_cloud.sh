#!/bin/bash
# setup_cloud.sh - Installs Docker and Minikube (Cloud Environment)

echo "Installing Docker"
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker $USER && newgrp docker

echo "Installing Minikube"
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

echo "Starting Minikube cluster"
minikube start --driver=docker --memory=4096 --cpus=2

echo "Done"sudo apt-get install -y wrk
