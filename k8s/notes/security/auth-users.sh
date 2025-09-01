#!/bin/sh

# Usage: ./auth-users.sh

# Apply the CSR files
kubectl apply -f ./csr.yml

# Approve the certificate requests
kubectl certificate approve alice
kubectl certificate approve bob

# Extract the approved certificates
kubectl get csr alice -o jsonpath='{.status.certificate}' | base64 -d > alice.crt
kubectl get csr bob -o jsonpath='{.status.certificate}' | base64 -d > bob.crt

# Add the users to your kubeconfig
kubectl config set-credentials alice --client-certificate=alice.crt --client-key=alice.key
kubectl config set-credentials bob --client-certificate=bob.crt --client-key=bob.key
