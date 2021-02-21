import base64
from datetime import datetime
from kubernetes import client, config

def main():
    """Method which will update secret and update annotation through k8s client lib
    """

    secret = "secret_2"

    # Generate base64 needed for secret update
    secret_bytes = secret.encode('ascii')
    base64_bytes = base64.b64encode(secret_bytes)
    secret_encoded = base64_bytes.decode('ascii')

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()
    client_v1 = client.CoreV1Api()
    
    # Update secret
    ret = client_v1.patch_namespaced_secret(
        "test-secret",
        "default",
        {
            "data": {
                "username": secret_encoded
            }
        }
    )
    # Update annotation on specific pod
    # it's also possible to implement update on all namespaced pods
    ret = client_v1.patch_namespaced_pod(
        "k8s-python-pod",
        "default",
        {
            "metadata": {
                "annotations": {
                    "secret_updated_at": datetime.now()
                }
            }
        }
    )

    # ret = client_v1.list_namespaced_secret("default")


if __name__ == "__main__":
    main()
