# Setting up Gluu server with Openshift (OCP-4.7)

## Overview

This will walk you through an installation of Gluu with Openshift (OCP 4.xx versions) manually. There are multiple managed services that may ease the operation and deployment listed below :

Using Red Hat OpenShift Dedicated:

  - Red Hat OpenShift Dedicated fully managed service is provided currently on Google Cloud and AWS as a SAAS.
  - The initial steps of configuring ocp4 are automated with this service, so no need for preparing any environment.
  - the service is fully managed, has maximum availability and offers a wide range of optimized clusters to choose from. .
  - [Click here](https://www.openshift.com/try) then Managed services to try it out for 60 days or navigate [here](https://marketplace.redhat.com/en-us/products/red-hat-openshift-dedicated) to buy it. 
  - For more about getting started with OpenShift dedicated, [follow this link](https://access.redhat.com/documentation/en-us/openshift_dedicated/4/html-single/getting_started/index). 

Red Hat OpenShift Service on AWS (ROSA):

  - This is a managed OpenShift offered as a service. 
  - The cluster lifecycle management is left to AWS.
  - Billing is supported for both pay-as-you-go hourly and annual. .
  - For more about getting started with ROSA, [follow this link](https://aws.amazon.com/rosa/)


## Installation on Google Cloud Platform

1.  Head to [https://www.openshift.com/try](https://www.openshift.com/try) and login with your credentials or create a new account. 

    1.  Select `Clusters`, and scroll down to the `Run it yourself` section. 

    2.  Go to `Google Cloud` and select `User provisioned infrastructure`. 

    3.  Create a directory, and prepare the listed items below in it: 

        ```bash
        # We will be using `./ocp4` in this tutorial 
        mkdir ./oc
        ```

        - Download `Openshift installer` for your OS. Currently, only Linux and MacOS are supported. 

        - Download and copy the `pull secret`. You'll be prompted for this during installation.

        - Download the `command line tools`. This will include an `oc cli kubeconfig` file downloaded for you.

2.  Download and install the [`gcloud-cli`](https://cloud.google.com/sdk/docs). 

    1.  Initialise login and authorise gcloud for your account in the browser.

        ```bash
        gcloud init 
        ```

    2.  Head to the [google cloud console](https://console.cloud.google.com) and login to access the cloud console. Ensure you have a `billing account` associated with it. 

    3.  Create a GCP `project` if not already present.

        ```bash
        gcloud projects create ${gcp_project}
        ```

    4.  Set the region, zone, and project.

        ```bash
       gcloud config set project ${gcp_project}
       ```
   
    5.  Verify your configuration values.

        ```bash
        gcloud config list
        ```

    6.  Head to the `google cloud console > navigation menu > API & Services`, and enable the below google api's:

        ```
        Compute Engine API -->  (compute.googleapis.com)
    
        Google Cloud APIs -->  (cloudapis.googleapis.com)     
    
        Cloud Resource Manager API --> (cloudresourcemanager.googleapis.com)         
    
        Google DNS API -->   (dns.googleapis.com)
    
        Identity and Access Management (IAM) API --> (iam.googleapis.com)
    
        IAM ServiceAccount Credentials --> (iamcredentials.googleapis.com) 
    
        Identity and Access Management (IAM) API --> (iam.googleapis.com)
    
        Service Management API --> (servicemanagement.googleapis.com)
    
        Service Usage API --> (serviceusage.googleapis.com)                      
    
        Google Cloud Storage JSON API → (storage-api.googleapis.com)           
    
        Cloud Storage --> (storage-component.googleapis.com)
        ```

    7.  Create a `service account` that grants authentication and authorization to access data through the Google APIs. Note that this and the two following steps can also be done on the `console.`

        ```bash
        gcloud iam service-accounts create ${gcp_sa}
        ```

    8.  Grant the above service account appropriate permissions. The following required GCP permissions will be needed for the installation.
 
        ```
        Compute Admin
        Security Admin
        Service Account Admin
        Service Account User
        Storage Admin
        DNS Administrator
        Service Account Key Admin
        ```

    9.  Create and store a `service account key` locally to be used for the installation in `json` format, this is needed to create the cluster. Google cloud requires identity establishment of the service account if it's to be used on other platforms.

        ```bash
        gcloud iam service-accounts keys create ./ocp4/sa-private-key.json --iam-account=${gcp_sa}@${gcp_project}.iam.gserviceaccount.com
        ```
      
        !!! Warning
            After you download the key, you can't download it again. Store your key securely as it can be used to authenticate as your service

    10.  Set the service key in your path

         ```bash
         export GOOGLE_APPLICATION_CREDENTIALS=csa-private-key.json
         ```
   
3.  Set up `DNS`. This tutorial assumes we already have a domain bought through GoDaddy. You can use an existing root domain and registrar or obtain a new one through GCP or another source. 

    1.  Create a new `managed zone` that cloud DNS supports. Command for the format is;

        ```bash
        gcloud dns managed-zones create NAME_FOR_YOUR_ZONE \
          --description=DESCRIPTION_FOR_YOUR_ZONE \
          --dns-name=DNS_SUFFIX_FOR_YOUR_ZONE \
          --labels=LABELS_OPTIONAL_K-V_PAIR \
          --visibility=public
        ```

        This tutorial assumes we use the domain `demoexample.gluu.org` 
    
        ```bash
        gcloud dns managed-zones create gluu-server-openshift --description="Gluu Openshift 4 Domain" --dns-name=demoexample.gluu.org --visibility=public
        ```

    2.  Get the `dns servers` for the domain by running the describe command. Register them with your DNS provider. They’ll be nameservers starting with `ns-`

        ```bash
        gcloud dns managed-zones describe gluu-server-openshift
        ```

    3.  Add the `dns servers` to your DNS provider portal. Select name server as type, gcp as host pointing to the name server. Do it for all nameservers.

        !!! Note
            If you would like to have a domain purchased through google, follow [this link](https://domains.google/) for more information about purchasing and configuring the domain.
   
    4.  Before creating the cluster, we need to verify that the dns delegation has been properly propagated. This assumes the `TTL` on your configuration is `60` seconds for faster propagation

        ```bash
        dig @8.8.8.8 demoexample.gluu.org NS +short
        ```

    5.  The default `quotas` aren't sufficient to install `ocp4`. The following only need to be increased in the `region` where you’ll do the installation:

        ```
        Compute Engine API (CPUs)
        Compute Engine API (Persistent Disk SSD (GB)
        ```
      
        Head to the `Navigation menu` in the console, > `IAM & admin` > `Quotas`. Choose the above quotas > `Edit Quotas`. Edit the CPU quotas to about `32`  and Persistent Disk SSD to `950 GB`. Fill in the contact Information and submit the request.
        
        It can take about `2-3 days` but usually the changes should be almost immediately.

4.  Install the cluster.

    1.  cd to the `ocp4` directory we created and install the cluster. The install-config will be used to customize our cluster.

        ```bash
        # Current working folder ./ocp4
        ./openshift-install create install-config --dir=./ocp4
        ```
      
        Prompt inputs for `ssh-key` (Optional), `cloud platform`, `service account key`, `project-id`, `region`, `base-domain`, `cluster-name`, `pull secret` saved from the first step will be required.

    2.  Open the content of the file with your favorite text editor.
   
        ```bash
        vi ./install-config.yaml
        ```

        ```yaml
        apiVersion: v1
        baseDomain: demoexample.gluu.org  #  this will be the basedomain that was prompted
        controlPlane:  
          architecture: amd64
          hyperthreading: Enabled 
          name: master
          Platform: {}
          replicas: 3
        compute:   
        - architecture: amd64
          hyperthreading: Enabled 
          name: worker
          Platform: {}
          replicas: 3
        metadata:
          name: gluu-ocp4-test-cluster #  this will be the cluster name that was prompted
        networking:
          clusterNetwork:
          - cidr: 10.128.0.0/14
            hostPrefix: 23
          machineNetwork:
          - cidr: 10.0.0.0/16
          networkType: OpenShiftSDN
          serviceNetwork:
          - 172.30.0.0/16
        platform:
          gcp:
            projectID:  # this will be the project-id that was prompted
            region:  # this will be the region that was prompted
        pullSecret: '{"auths": ...}'   # this will be the pull-secret that was prompted
        fips: false 
        publish: External
        sshKey: ssh-ed25519 AAAA…  # this will be the ssh-key that was prompted
        ```

        `ssh keys` are optional. you could add them in the script as shown above to the agent for debugging and installation troubleshooting purposes.

    3.  The `install-config.yaml` is consumed during the installation process. Create a copy and move it. 

    4.  Run the command below to create the cluster. The creation will take about 30 minutes. 

        ```bash
        ./openshift-install create cluster --dir=./ocp4 --log-level=info
        ```

        !!! Note
            Keep the installation program or the files that the installation program creates. They are required to delete the cluster.
    
    5.  Login to the cluster in the browser using the `url` provided along with the `kube-admin username / password`.  The credentials can also be accessed in the log file located in the ocp4 folder. 

        ```bash
        vi ./ocp4/.openshift_install.log
        ```

    6.  To interact with the ocp cluster from the host, first set the `kube admin credentials` with the following commands. 

        ```bash
        mkdir -p $HOME/.kube
        sudo cp -i ./ocp4/auth/kubeconfig $HOME/.kube/config
        sudo chown $(id -u):$(id -g) $HOME/.kube/config
        ```

    7.  Verify it works on the command line by trying to run any of these commands.

        ```bash
        oc whoami
        oc get nodes
        oc get sc.    (this will return storage class)
        oc get clusterversion    (openshift cluster version) 
        ```

    8.  Create a user and assign them an admin role.

        ```bash
        oc create user <user_name>
    
        kubectl create clusterrolebinding permissive-binding --clusterrole=cluster-admin --user=<user_name> --group=system:serviceaccounts
        ```

    9.  To obtain the list of users

        ```bash
        oc get users 
        ```
   
   
5.  Configuring an HTPasswd identity provider

    By default, only a kubeadmin user exists on your cluster. Refer to the [official documentation](https://docs.openshift.com/container-platform/4.7/authentication/identity_providers/configuring-htpasswd-identity-provider.html) for more information about the identity provider

    1.  Create an htpasswd file to store the user and password information

        ```bash
        sudo apt install apache2-utils
        htpasswd -c -B -b </path/to/users.htpasswd> <user_name> <password>
        ```

    2.  Create a hashed version of the password.

        ```bash
        htpasswd -c -B -b users.htpasswd user1 MyPassword! 
        ```

    3.  Create an OpenShift Container Platform secret to represent the htpasswd file.

        ```bash
        oc create secret generic htpass-secret --from-file=htpasswd=</path/to/users.htpasswd> -n openshift-config
        ```

    4.  Define the HTPasswd identity provider resource.
   
        ```bash
        vi HTPasswd.yaml
        ```

        ```yaml
        apiVersion: config.openshift.io/v1
        kind: OAuth
        metadata:
          name: cluster
        spec:
          identityProviders:
          - name: my_htpasswd_provider 
            mappingMethod: claim 
            type: HTPasswd
            htpasswd:
              fileData:
                name: htpass-secret 
        ```

    5.  Apply the resource to the default OAuth configuration.

        ```bash
        oc apply -f </path/to/CR>
        ```

        Alternatively, you could use [Google Identity Provider](https://docs.openshift.com/container-platform/4.7/authentication/identity_providers/configuring-google-identity-provider.html), [LDAP Identity Provider](https://docs.openshift.com/container-platform/4.7/authentication/identity_providers/configuring-ldap-identity-provider.html)  or [OpenID Identity Provider](https://docs.openshift.com/container-platform/4.7/authentication/identity_providers/configuring-oidc-identity-provider.html)

    6.  Log in to the cluster as a user from your identity provider, entering the password when prompted.

        ```bash
        oc login -u <username>
        ```

    7.  Confirm that the user logged in successfully, and display the username.

        ```bash
        oc whoami
        ```
      
6.  Configure helm since it’ll be used to deploy Gluu and any other services. Ensure you have helm installed on your computer

    1.  Installation. 

        === "Linux"
    
            ```bash
            curl -L https://mirror.openshift.com/pub/openshift-v4/clients/helm/latest/helm-linux-amd64 -o /usr/local/bin/helm
            chmod +x /usr/local/bin/helm
            ```

        === "Mac"
    
            ```bash
            curl -L https://mirror.openshift.com/pub/openshift-v4/clients/helm/latest/helm-darwin-amd64 -o /usr/local/bin/helm
            chmod +x /usr/local/bin/helm
            ```
   
    2.  Try running the following to confirm it works. 

        ```bash
        helm version
        helm repo update
        ```

    3.  In the next section we’ll be installing OpenEBS. It’s important to first create a new service account with root privilege that will be used for most of the following steps. You also have to configure `SCC`

        ```bash
        oc create serviceaccount useroot
        oc adm policy add-scc-to-user anyuid -z useroot
        ```

7.  Install OpenEBS.  It can be installed using both the terminal with helm or the `UI` from the `Operators > OperatorHub` section. 

    1.  Using helm  run the following to install openebs

        ```bash
        helm repo add openebs https://openebs.github.io/charts
        helm repo update
        helm install openebs --namespace openebs openebs/openebs --create-namespace
        ```

    2.  To view the chart, run `

        ```bash
        helm ls -n openebs
        ```

    3.  To view the pods in `<openebs> namespace`, run:

        ```bash
        kubectl get pods -n openebs
        ```

        The successful operation should have `(3)` `openebs-ndm` daemon set running on all `3 nodes`. The control plane pods `openebs-provisioner`, `maya-apiserver` and `openebs-snapshot-operator` should be running. 

    4.  To check if OpenEBS has installed with `default StorageClasses`, 4 storage classes should be created.

        ```bash
        kubectl get sc
        ```

    5.  For provisioning OpenEBS volumes, you have to edit SCC to allow HostPath volumes and Privileged containers.

        ```bash
        #oc adm policy add-scc-to-user privileged system:serviceaccount:<project>:<serviceaccountname>
        oc adm policy add-scc-to-user privileged system:serviceaccount:openebs:useroot 
        ```

    6.  Enable Container Images that Require Root

        ```bash
        oc adm policy add-scc-to-user anyuid system:serviceaccount:openebs:useroot
        ```

    7.  In this tutorial, you can alternatively use `GCE Persistent Disk volumes (gcePD)` that’s supported by openshift manually. `Openshift ui > storage > storage classes.` Create a storage class. Select `reclaim policy` and `kubernetes.io/gce-pd` from the dropdown list. Create it.

    8.  `Openshift ui > storage > PVC > Create PVC`. Choose the `storage class` created above. Select `access mode` and define `storage claims`.

8.  Manually configure Nginx Ingress.

    1.  `Operator > OperatorHub`
   
    2.  Search for `Nginx Ingress Operator` and install it.

    3.  Verify the operator is running

        ```bash
        oc get pods -n nginx-ingress
        ```

    4.  Create a `manifest` that would provision the deployment of the `nginx controller`. Click on the `installed operators`, choose `nginx ingress controller`, under `provided APIs`, click `NginxIngressXontroller`. 

    5.  Paste in a manifest file for the nginx controller and save the changes.

    6.  Verify setup
   
        ```bash
        oc get pods -n nginx-ingress to verify the controller has been deployed
        oc get svc -o wide -n nginx-ingress to see a service of type loadbalancer
        ```

9.  Install gluu. 

    === "Pygluu-helm"
            
        This option is more user friendly as it walks you through an installation pathway and executes a helm install.

        1.  Change permissions to the directory that contains [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases/download/v1.6.6/pygluu-kubernetes-linux-amd64.pyz)

            ```bash
            sudo chgrp -R 0 /path/to/dir/ && chmod -R g=u /path/to/dir/
            ```

        2.  Install the gluu server

            ```bash
            cd /path/to/dir/ && ./pygluu-kubernetes.pyz helm-install
            ```

    === "Helm"
        
        Follow this [section](https://gluu.org/docs/gluu-server/4.4/installation-guide/install-kubernetes/#installing-gluu-using-helm-manually) to install using helm manually.

    If the `nginx-ingress` didn't work correctly - modifying the `deployment configuration` for nginx-ingress and adding the serviceaccount to the `anyuid SCC` as the application defined needs to run as user root in the container.

    ```bash
    oc patch deployment.apps/ningress-nginx-ingress-controller --patch '{"spec":{"template":{"spec":{"serviceAccountName": "useroot"}}}}'
    oc patch deployment.apps/ningress-nginx-ingress-default-backend --patch '{"spec":{"template":{"spec":{"serviceAccountName": "useroot"}}}}'
    ```
    
## Uninstallation

  Uninstalling the cluster. `cd` to the folder that contains the installation program.

1.  First remove the gluu server helm deployment and all its workloads running in the cluster. Run the following command. 

    ```bash
    ./pygluu-kubernetes.pyz uninstall
    # if using helm purely
    helm delete <my-release>
    ```

2.  Uninistall OCP4. Run the following command to delete the cluster.

    ```bash
    ./openshift-install destroy cluster --dir=<installation_directory> --log-level=info
    ```        