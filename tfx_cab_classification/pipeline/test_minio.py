#!/usr/bin/env python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import kfp
from kfp import dsl
from kubernetes.client import V1SecretKeySelector


@dsl.pipeline(
    name="custom_artifact_location_pipeline",
    description="""A pipeline to demonstrate how to configure the artifact
    location for all the ops in the pipeline.""",
)
def custom_artifact_location(
    tag: str, namespace: str = "kubeflow", bucket: str = "somebucket"
):

    # configures artifact location
    pipeline_artifact_location = dsl.ArtifactLocation.s3(
        bucket=bucket,
        endpoint="minio-service.%s:9000" % namespace,  # parameterize minio-service endpoint
        insecure=True,
        access_key_secret={"name": "mlpipeline-minio-artifact", "key": "accesskey"},
        secret_key_secret={"name": "mlpipeline-minio-artifact", "key": "accesssecret"})

    # artifacts in this op are stored to endpoint `minio-service.<namespace>:9000`
    op = dsl.ContainerOp(name="foo", image="busybox:%s" % tag, artifact_location=pipeline_artifact_location)

if __name__ == '__main__':
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = "minio"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "minio123"
    os.environ["S3_USE_HTTPS"] = "0"
    os.environ["S3_VERIFY_SSL"] = "0"
    os.environ["S3_ENDPOINT"] = "minio-service.kubeflow:9000"
    os.environ["S3_REQUEST_TIMEOUT_MSEC"] = "600000"


    from tensorflow.python.lib.io import file_io

    print(file_io.stat('s3://orain/'))
    output = '/home/jovyan/data-vol-1/mnist/pipeline-test-minio-fix9/7692858b-824f-4cf9-b286-0e50a34e4b1d/tfx-taxi-cab-classification-pipeline-example-tt6s6-902552594/data/'

    if  not os.path.exists(output):
      os.makedirs(output)

    kfp.compiler.Compiler().compile(custom_artifact_location, __file__ + '.zip')