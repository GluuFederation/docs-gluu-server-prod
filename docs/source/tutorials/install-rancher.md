# Rancher Kubernetes Engine

## Overview

This is a tutorial to walk you through installing Gluu cloud native edition on RKE on a ubuntu 20.04.

## Instructions

!!!note
    Please use a registered FQDN. If you don't, follow instructions here.


1. Create instances to cover at minimum 8 cpu and 16 GB ram.

1. Follow instructions [here](https://rancher.com/docs/rke/latest/en/installation/) to install RKE. Please do not run `./rke up` until next step is executed.

1. You should have generated a `cluster.yml` following instructions above. Please open that file and add the following under the `services` --> `kubelet` --> `extra_binds`, as we use OpenEBS for volumes on RKE.

    ```yaml
    services:
      kubelet:
        extra_binds:
         - /var/openebs/local:/var/openebs/local
         - /etc/iscsi:/etc/iscsi
         - /bin/iscsiadm:/bin/iscsiadm
         - /var/lib/iscsi:/var/lib/iscsi
         - /lib/modules
         - /var/openebs/sparse:/var/openebs/sparse
         - /var/openebs/local:/var/openebs/local
         - /mnt/openebs/local:/mnt/openebs/local
         - /opt/openebs/local:/opt/openebs/local
    ```
    
1. Now you can bring your cluster up `./rke up`.

1. You should have a running Kubernetes cluster now. You may add or remove nodes as necessary.

1. Follow instructions [here](https://docs.openebs.io/docs/next/installation.html) to install openEBS.

1. Make sure that the instances has permissions as required by RKE to fully communicate with the intended cloud. 

1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](#build-pygluu-kubernetespyz-manually).

1. **Optional:** If using couchbase as the persistence backend. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`


1. Run :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```

!!!note
    Use local deployment on a manually created kubernetes cluster when prompted.


## Exposing the UI:

Exposing the UI is not necessary but you may do so by following these steps:

1. Create a single point of entry ( Load balancer) for your cluster. Please note that if you have given the instances permissions to act on the cloud the load balancer should have already been created and hence the following steps are not needed, otherwise a `NodePort` would have been created and you would need to follow with the next steps..

1. Get the port number nginx is using for forwarding `4.4` connections, here that would be `31822`

   ```bash
   kubectl get svc -n ingress-nginx
    NAME                                          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
    default-http-backend                          ClusterIP      10.43.60.162   <none>        80/TCP                       131m
    ningress-ingress-nginx-controller             LoadBalancer   10.43.55.137   <pending>     80:30925/TCP,4.4:31822/TCP   18m
    ningress-ingress-nginx-controller-admission   ClusterIP      10.43.8.231    <none>        4.4/TCP                      18m
   ```

   Forexample, Using AWS UI create an LB with `TCP` port `4.4` pointing to your nodeport i.e `TCP` `31822`. If this is a FQDN create an `https` listener rule instead and attach your arn certificate. If you used `TCP`, add to your local computer ip of your loadbalancer and map it to your FQDN, then head to your browser at `https://<gluu-FQDN>` i.e `https://demoexample.gluu.org`

1. You must add a record to point your FQDN to the loadbalancer / ip used as a the single point of entry.

## Non-FQDN setup:

oxTrust will likely fail as it calls to check the ssl certificate. You will have to make sure to add to oxtrust statefulset a hostAlias entry to point your FQDN to the ip of the loadbalancer.


## Using Rancher

1. Follow instructions [here](https://rancher.com/docs/rancher/v2.x/en/installation/) to install Rancher in the environment of your choice

1. In the Rancher UI ,create your cluster by going to `Global` --> `Add Cluster` and choosing from any of the providers, `AKS`, `EKS`, `GKE`, `EC2`, `Azure`, `Linode`, and `vSphere`

1. After the cluster has been created, copy  `kubeconfig` to a vm or laptop with `kubectl` , `helm` and `python3` installed.

1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](#build-pygluu-kubernetespyz-manually).

1. **Optional:** If using couchbase as the persistence backend. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`

1. Run :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```
    
!!!note
    If using EC2 or EKS please use the AWS deployment path.    