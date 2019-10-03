# Copyright 2019 The Kubeflow Authors
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

def use_minio_secret(secret_name='mlpipeline-minio-artifact', minio_access_key_id_name='accesskey', minio_secret_access_key_name='secretkey'):
    """An operator that configures the container to use minio credentials.
        AWS doesn't create secret along with kubeflow deployment and it requires users
        to manually create credential secret with proper permissions.
        ---
        apiVersion: v1
        kind: Secret
        metadata:
          name: mlpipeline-minio-artifact
        type: Opaque
        data:
          accesskey: BASE64_YOUR_AWS_ACCESS_KEY_ID
          secretkey: BASE64_YOUR_AWS_SECRET_ACCESS_KEY
    """

    def _use_minio_secret(task):
        from kubernetes import client as k8s_client
        return (
            task
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='AWS_ACCESS_KEY_ID',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key=minio_access_key_id_name
                            )
                        )
                    )
                )
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='AWS_SECRET_ACCESS_KEY',
                        value_from=k8s_client.V1EnvVarSource(
                            secret_key_ref=k8s_client.V1SecretKeySelector(
                                name=secret_name,
                                key=minio_secret_access_key_name
                            )
                        )
                    )
                )
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='S3_USE_HTTPS',
                        value='0'
                    )
                )
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='S3_VERIFY_SSL',
                        value='0'
                    )
                )
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='S3_ENDPOINT',
                        value='minio-service.kubeflow:9000'
                    )
                )
                .add_env_variable(
                    k8s_client.V1EnvVar(
                        name='S3_REQUEST_TIMEOUT_MSEC',
                        value='1200000'
                    )
                )
        )

    return _use_minio_secret
