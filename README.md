# kube-elevate
A self-service permissions elevation framework for Kubernetes.

## What is this project?
This project is a python-based Kubernetes Operator (built with kopf) that allows a user to submit a CRD of an 'ElevatePermissions' object to the Kubernetes API, Kubernetes will validate this (check for an open ServiceNow ticket, for example), then then assign ReadWrite permissions for the user to a particular namespace for a given period of time (before removing them again). This is useful in situations where users may need breakglass access to Production when they typically only have Read permissions.

## How does it work?
##### CRD
##### Operator
##### CronJobs

## How do I deploy this to my cluster?









