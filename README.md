# Kubernetes Secrets Research
The purpose of this repo is to give details regarding the research for secrets update mapped as a volume inside a pod

## Research Topic
Once the secrets are available within the pods we want to make sure that any change on secret values will be visible by the applications inside the pods without a need to restart the pods every time a secret value changes.

This can be accomplished by mapping secrets to volumes within the pods (and inner containers).

Providing secrets within the pods:
- https://kubernetes.io/docs/concepts/configuration/secret/

### Important Note
- Have in mind that the secret update will not propagate instantly by default, the sync time for the secrets is determined by several k8s config parameters:
    - kubelet sync period + cache propagation delay, where the cache propagation delay depends on the chosen cache type (it equals to watch propagation delay, ttl of cache, or zero correspondingly). [More info](https://kubernetes.io/docs/concepts/configuration/secret/)
- One way to get around the sync period wait is to update annotations on the pod which will result in secrets value sync. [More info](https://github.com/kubernetes/kubernetes/issues/30189)

## Research Steps (CLI)
- Make sure k8s cluster is up and running. For this research I've used local Docker for desktop single node cluster
- Build docker image with `docker build --tag k8s-python .`
- Create secrets with `kubectl apply -f kubernetes/secret.yaml`
- Create pod with `kubectl apply -f kubernetes/pod.yaml`
    - Pod runs a simple docker container with python app which writes log of secrets value from mapped volume every 5s
- In another terminal window follow logs for created pod with `kubectl logs k8s-python-pod --follow`
- Update secret value within the secrets.yaml
    - have in mind that the value should be base64, for example: `echo -n 'my-app' | base64`
- Update secret with `kubectl apply -f kubernetes/secret.yaml`
- Observe that secrets are not instantly updated within the pod logs, but only after certain period expires (sync)
- Again update secret value within the secrets.yaml
- Update secret with `kubectl apply -f kubernetes/secret.yaml`
- Update all pod annotations with `kubectl annotate --overwrite pods --all datetime="$(date)"`
    - This will add datetime annotation with current datetime to all running pods
- Observe that the secret is updated instantly within the running pod

## Research Steps (CLI and K8S Python Client)
- Make sure k8s cluster is up and running. For this research I've used local Docker for desktop single node cluster
- Build docker image with `docker build --tag k8s-python .`
- Create secrets with `kubectl apply -f kubernetes/secret.yaml`
- Create pod with `kubectl apply -f kubernetes/pod.yaml`
    - Pod runs a simple docker container with python app which writes log of secrets value from mapped volume every 5s
- In another terminal window follow logs for created pod with `kubectl logs k8s-python-pod --follow`
- Update secret value running the secrets_update.py script
    - Update the secret var to change the secret value
    - This will also add secret_updated_at annotation with current datetime to the running pod
- Observe that the secret is updated instantly within the running pod

<span style="color:yellow">
    TODO: Check are there any negative effects of updating annotations on all pods
</span>

## Additional useful commands:
- `kubectl get pods`
- `kubectl get secrets`
- `kubectl delete pod {pod_name}`
- `kubectl delete secret {secret_name}`
