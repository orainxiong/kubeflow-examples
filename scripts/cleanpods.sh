#!/usr/bin/env bash

# release compute resource
kubectl get pods -n kubeflow | grep Error | awk '{print $1}' | xargs kubectl delete pod -n kubeflow



# release pvc/pv resource
kubectl get pvc -n kubeflow | grep tfx-taxi-cab-classification-pipeline-example | grep -v tfx-taxi-cab-classification-pipeline-example-d5lqz-pipeline-pvc | awk '{print $1}' | xargs kubectl delete pvc -n kubeflow