# kube-elevate

_Work in progress!! documentation is pretty sparse..._

A self-service permissions elevation framework for Kubernetes.

## What is this project?
This project provides a Kubernetes-native method of allowing cluster users to self-elevate their permissions from ReadOnly to ReadWrite, to a given namespace for a given period of time.

The project is a python-based Kubernetes Operator (built with kopf) that allows a user to submit a CRD of an 'ElevatePermissions' object to the Kubernetes API, Kubernetes will validate this (check for an open ServiceNow ticket, for example), then then assign ReadWrite permissions for the user to a particular namespace for a given period of time (before removing them again). This is useful in situations where users may need breakglass access to Production when they typically only have Read permissions.

## How does it work?
##### CRD
##### Operator
##### CronJobs

## How do I deploy this to my cluster?
```
kubectl apply -f deploy.yaml
```

```
docker build . -t docker.io/jimmyjamesbaldwin/op-db:5
docker push docker.io/jimmyjamesbaldwin/op-db:5

```




