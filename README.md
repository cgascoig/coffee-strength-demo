# Coffee strength demo

## Deployment

1. If using GKE, enable cluster-admin for you user account so that RBAC changes can be made:
```
kubectl create clusterrolebinding cluster-admin-binding --clusterrole cluster-admin --user <your GCP account>
```
2. Create namespace:
```
kubectl create ns coffee-prod
```
3. Setup RBAC policies so that load balancer URL can be discovered automatically:
```
kubectl create clusterrole get-coffee-svc --verb=get --resource=services --resource-name=coffee-strength-bot-service
kubectl create clusterrolebinding get-coffee-svc --clusterrole get-coffee-svc --serviceaccount coffee-prod:default
```
4. Deploy secrets in Kubernets (see `k8s-prod-secrets.sample.yml` for example):
```
kubectl apply -n coffee-prod -f k8s-prod-secrets.yml
```
5. Deploy application components:
```
kubectl apply -n coffee-prod -f k8s-deploy.yml