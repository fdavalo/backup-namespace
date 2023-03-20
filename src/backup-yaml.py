import sys
import json
import yaml

def transformed(data, kind):
    if kind == "secrets":
        if "metadata" in data and "annotations" in data["metadata"] and "kubernetes.io/service-account.name" in data["metadata"]["annotations"]: return None

    if kind == "configmaps":
        if data["metadata"]["name"] in ["config-service-cabundle", "config-trusted-cabundle", "kube-root-ca.crt", "openshift-service-ca.crt"]: return None

    if kind == "serviceaccounts":
        if data["metadata"]["name"] in ["default", "builder", "deployer"]: return None

    if "metadata" in data and "ownerReferences" in data["metadata"]: return None

    if kind in ["rolebindings.rbac.authorization.k8s.io","rolebindings.authorization.openshift.io"]:
        if data["metadata"]["name"] in ["system:deployers", "system:image-builders", "system:image-pullers"]: return None
        if "subjects" in data and len(data["subjects"]) == 1 and "name" in data["subjects"][0] and data["subjects"][0]["name"] == "kube:admin": return None

    if kind == "endpoints": return None

    if "metadata" in data:
        if "creationTimestamp" in data["metadata"]: del data["metadata"]["creationTimestamp"]
        if "managedFields" in data["metadata"]: del data["metadata"]["managedFields"]
        if "resourceVersion" in data["metadata"]: del data["metadata"]["resourceVersion"]
        if "uid" in data["metadata"]: del data["metadata"]["uid"]
    
    if "status" in data: del data["status"]

    return data

if __name__ == "__main__":
    name = sys.argv[1]
    kind = sys.argv[2]
    path = sys.argv[3]
    f = open(path+name+".json")
    data = json.load(f)
    f.close()
    transformed = transformed(data, kind)
    if transformed is not None:
        file = open(path+name+".yaml", 'w')
        yaml.dump(transformed, file, default_flow_style=False)
        file.close()
