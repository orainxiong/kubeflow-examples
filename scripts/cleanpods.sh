#!/usr/bin/env bash

# release compute resource
kubectl get pods -n kubeflow | grep -E "Evicted|Error|Completed" | awk '{print $1}' | xargs kubectl delete pod -n kubeflow

kubectl get deployment -n kubeflow | grep -e 'viewer-' | grep -e '-deployment' | awk '{print $1}' | xargs kubectl delete deployment -n kubeflow


# release pvc/pv resource
kubectl get pvc -n kubeflow | grep tfx-taxi-cab-classification-pipeline-example | grep -v tfx-taxi-cab-classification-pipeline-example-d5lqz-pipeline-pvc | awk '{print $1}' | xargs kubectl delete pvc -n kubeflow