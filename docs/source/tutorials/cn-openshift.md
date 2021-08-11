7. Install OpenEBS.  It can be installed using both the terminal with helm or the `UI` from the `Operators > OperatorHub` section. 

   1. Using helm  run the following to install openebs

      ```bash
      helm repo add openebs https://openebs.github.io/charts
      helm repo update
      helm install openebs --namespace openebs openebs/openebs --create-namespace
      ```

   2. To view the chart, run `

      ```bash
      helm ls -n openebs
      ```

   3. To view the pods in `<openebs> namespace`, run:

      ```bash
      kubectl get pods -n openebs
      ```

    The successful operation should have `(3)` `openebs-ndm` daemon set running on all `3 nodes`. The control plane pods `openebs-provisioner`, `maya-apiserver` and `openebs-snapshot-operator` should be running. 

   4. To check if OpenEBS has installed with `default StorageClasses`, 4 storage classes should be created.

      ```bash
      kubectl get sc
      ```

   5. For provisioning OpenEBS volumes, you have to edit SCC to allow HostPath volumes and Privileged containers.

      ```bash
      #oc adm policy add-scc-to-user privileged system:serviceaccount:<project>:<serviceaccountname>
      oc adm policy add-scc-to-user privileged system:serviceaccount:openebs:useroot 
      ```

   6. Enable Container Images that Require Root

      ```bash
      oc adm policy add-scc-to-user anyuid system:serviceaccount:openebs:useroot
      ```

   7. In this tutorial, you can alternatively use `GCE Persistent Disk volumes (gcePD)` that’s supported by openshift manually. `Openshift ui > storage > storage classes.` Create a storage class. Select `reclaim policy` and `kubernetes.io/gce-pd` from the dropdown list. Create it.

   8. `Openshift ui > storage > PVC > Create PVC`. Choose the `storage class` created above. Select `access mode` and define `storage claims`.

8. Manually configure Nginx Ingress.

   1. `Operator > OperatorHub`
   
   2. Search for `Nginx Ingress Operator` and install it.

   3. Verify the operator is running

      ```bash
      oc get pods -n nginx-ingress
      ```

   4. Create a `manifest` that would provision the deployment of the `nginx controller`. Click on the `installed operators`, choose `nginx ingress controller`, under `provided APIs`, click `NginxIngressXontroller`. 

   5. Paste in a manifest file for the nginx controller and save the changes.

   6. Verify setup
   
       ```bash
       oc get pods -n nginx-ingress to verify the controller has been deployed
       oc get svc -o wide -n nginx-ingress to see a service of type loadbalancer
       ```

9. Install gluu. 

   1. Change permissions to the directory that contains `pygluu-kubernetes.pyz`

      ```bash
      sudo chgrp -R 0 /path/to/dir/ && chmod -R g=u /path/to/dir/
      ```

   2. Install the gluu server

      ```bash
      cd /path/to/dir/ && ./pygluu-kubernetes.pyz helm-install
      ```

   3. If the `nginx-ingress` didn't work correctly - modifying the `deployment configuration` for nginx-ingress and adding the serviceaccount to the `anyuid SCC` as the application defined needs to run as user root in the container.

      ```bash
      oc patch deployment.apps/ningress-nginx-ingress-controller --patch '{"spec":{"template":{"spec":{"serviceAccountName": "useroot"}}}}'
      oc patch deployment.apps/ningress-nginx-ingress-default-backend --patch '{"spec":{"template":{"spec":{"serviceAccountName": "useroot"}}}}'
      ```

## Uninstallation

  Uninstalling the cluster. `cd` to the folder that contains the installation program.

1. First remove the gluu server helm deployment and all its workloads running in the cluster. Run the following command. 

   ```bash
   ./pygluu-kubernetes.pyz uninstall
   # if using helm purely
   helm delete <my-release>
   ```

2. Uninistall OCP4. Run the following command to delete the cluster.

   ```bash
   ./openshift-install destroy cluster --dir=<installation_directory> --log-level=info
   ```        