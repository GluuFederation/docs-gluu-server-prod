# The Kubernetes recipes

## Getting Started with Kubernetes

The Kubernetes deployment of the Gluu Server, also called Cloud Native (CN) Edition, requires some special considerations compared to other deployments. This page details the installation and initial configuration of a CN deployment. More advanced configuration details are available on the appropriate pages throughout the Gluu documentation. For convenience, links to those documents follow:

- [Architectural general diagram](#architectural-diagram-of-all-gluu-services)
- [Certificate Management](../admin-guide/certificate.md)  
- [Key Reference Guide](../reference/container-configs.md)  
- [Image Reference Guide](../reference/container-image-refs.md)  
- [Backup Strategy](../operation/backup.md/)  
- [Upgrade](../upgrade/index.md)
- [Migrating from CE](../operation/ce_to_cn_migration.md)  
- [Casa interactions diagram](#architectural-diagram-of-casa)
- [SCIM interactions diagram](#architectural-diagram-of-scim)
- [Passport interactions diagram](#architectural-diagram-of-oxpassport)
- [Jackrabbit interactions diagram](#working-with-jackrabbit)

## System Requirements for cloud deployments

!!!note
    For local deployments like `minikube` and `microk8s`  or cloud installations for demoing Gluu may set the resources to the minimum and hence can have `8GB RAM`, `4 CPU`, and `50GB disk` in total to run all services.
  
Please calculate the minimum required resources as per services deployed. The following table contains default recommended resources to start with. Depending on the use of each service the resources may be increased or decreased. 

|Service           | CPU Unit   |    RAM      |   Disk Space     | Processor Type | Required                                    |
|------------------|------------|-------------|------------------|----------------|---------------------------------------------|
|oxAuth            | 2.5        |    2.5GB    |   N/A            |  64 Bit        | Yes                                         |
|LDAP              | 1.5        |    2GB      |   10GB           |  64 Bit        | if using hybrid or ldap for persistence     |
|[Couchbase](#minimum-couchbase-system-requirements-for-cloud-deployments)         |    -       |      -      |      -           |     -          | If using hybrid or couchbase for persistence|
|fido2             | 0.5        |    0.5GB    |   N/A            |  64 Bit        | No                                          |
|scim              | 1.0        |    1.0GB    |   N/A            |  64 Bit        | No                                          |
|config - job      | 0.5        |    0.5GB    |   N/A            |  64 Bit        | Yes on fresh installs                       |
|jackrabbit        | 1.5        |    1GB      |   10GB           |  64 Bit        | Yes                                         |
|persistence - job | 0.5        |    0.5GB    |   N/A            |  64 Bit        | Yes on fresh installs                       |
|oxTrust           | 1.0        |    1.0GB    |   N/A            |  64 Bit        | No                                          |
|oxShibboleth      | 1.0        |    1.0GB    |   N/A            |  64 Bit        | No                                          |  
|oxPassport        | 0.7        |    0.9GB    |   N/A            |  64 Bit        | No                                          |
|oxd-server        | 1          |    0.4GB    |   N/A            |  64 Bit        | No                                          |
|nginx             | 1          |    1GB      |   N/A            |  64 Bit        | Yes if not ALB                              |
|key-rotation      | 0.3        |    0.3GB    |   N/A            |  64 Bit        | No                                          |
|cr-rotate         | 0.2        |    0.2GB    |   N/A            |  64 Bit        | No                                          |
|casa              | 0.5        |    0.5GB    |   N/A            |  64 Bit        | No                                          |


1. Configure cloud or local kubernetes cluster:

=== "EKS"
    ## Amazon Web Services (AWS) - EKS
      
    ### Setup Cluster
    
    -  Follow this [guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
     to install a cluster with worker nodes. Please make sure that you have all the `IAM` policies for the AWS user that will be creating the cluster and volumes.
    
    ### Requirements
    
    -   The above guide should also walk you through installing `kubectl` , `aws-iam-authenticator` and `aws cli` on the VM you will be managing your cluster and nodes from. Check to make sure.
    
            aws-iam-authenticator help
            aws-cli
            kubectl version
    
    - **Optional[alpha]:** If using Istio please [install](https://istio.io/latest/docs/setup/install/standalone-operator/) it prior to installing Gluu. You may choose to use any installation method Istio supports. If you have insalled istio ingress , a loadbalancer will have been created. Please save the address of loadblancer for use later during installation.

    !!!note
        Default  AWS deployment will install a classic load balancer with an `IP` that is not static. Don't worry about the `IP` changing. All pods will be updated automatically with our script when a change in the `IP` of the load balancer occurs. However, when deploying in production, **DO NOT** use our script. Instead, assign a CNAME record for the LoadBalancer DNS name, or use Amazon Route 53 to create a hosted zone. More details in this [AWS guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html?icmpid=docs_elb_console).
      

=== "GKE"
    ## GCE (Google Cloud Engine) - GKE
    
    ### Setup Cluster

    1.  Install [gcloud](https://cloud.google.com/sdk/docs/quickstarts)
    
    1.  Install kubectl using `gcloud components install kubectl` command
    
    1.  Create cluster using a command such as the following example:
    
            gcloud container clusters create exploringgluu --num-nodes 2 --machine-type e2-highcpu-8 --zone us-west1-a
    
        where `CLUSTER_NAME` is the name you choose for the cluster and `ZONE_NAME` is the name of [zone](https://cloud.google.com/compute/docs/regions-zones/) where the cluster resources live in.
    
    1.  Configure `kubectl` to use the cluster:
    
            gcloud container clusters get-credentials CLUSTER_NAME --zone ZONE_NAME
    
        where `CLUSTER_NAME` is the name you choose for the cluster and `ZONE_NAME` is the name of [zone](https://cloud.google.com/compute/docs/regions-zones/) where the cluster resources live in.
    
        Afterwards run `kubectl cluster-info` to check whether `kubectl` is ready to interact with the cluster.
        
    1.  If a connection is not made to google consul using google account the call to the api will fail. Either connect to google consul using an associated google account and run any `kubectl` command like `kubectl get pod` or create a service account using a json key [file](https://cloud.google.com/docs/authentication/getting-started).
    
    - **Optional[alpha]:** If using Istio please [install](https://istio.io/latest/docs/setup/install/standalone-operator/) it prior to installing Gluu. You may choose to use any installation method Istio supports. If you have insalled istio ingress , a loadbalancer will have been created. Please save the ip of loadblancer for use later during installation.

    
=== "DOKS"
    ## DigitalOcean Kubernetes (DOKS)
    
    ### Setup Cluster
    
    -  Follow this [guide](https://www.digitalocean.com/docs/kubernetes/how-to/create-clusters/) to create digital ocean kubernetes service cluster and connect to it.

    - **Optional[alpha]:** If using Istio please [install](https://istio.io/latest/docs/setup/install/standalone-operator/) it prior to installing Gluu. You may choose to use any installation method Istio supports. If you have insalled istio ingress , a loadbalancer will have been created. Please save the ip of loadblancer for use later during installation.

=== "AKS"
    ## Azure - AKS
    
    !!!warning
        Pending
        
    ### Requirements
    
    -  Follow this [guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) to install Azure CLI on the VM that will be managing the cluster and nodes. Check to make sure.
    
    -  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#create-a-resource-group) to create the resource group for the AKS setup.
    
    -  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#create-aks-cluster) to create the AKS cluster
    
    -  Follow this [section](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster) to connect to the AKS cluster
    
    - **Optional[alpha]:** If using Istio please [install](https://istio.io/latest/docs/setup/install/standalone-operator/) it prior to installing Gluu. You may choose to use any installation method Istio supports. If you have insalled istio ingress , a loadbalancer will have been created. Please save the ip of loadblancer for use later during installation.

      
=== "Minikube"
    ## Minikube
    
    ### Requirements
    
    1. Install [minikube](https://github.com/kubernetes/minikube/releases).
    
    1. Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
    
    1. Create cluster:
    
        ```bash
        minikube start
        ```
            
    1. Configure `kubectl` to use the cluster:
    
            kubectl config use-context minikube
            
    1. Enable ingress on minikube
    
        ```bash
        minikube addons enable ingress
        ```
        
    1. **Optional[alpha]:** If using Istio please [install](https://istio.io/latest/docs/setup/install/standalone-operator/) it prior to installing Gluu. You may choose to use any installation method Istio supports.Please note that at the moment Istio ingress is not supported with Minikube. 
    
=== "MicroK8s"
    ## MicroK8s
    
    ### Requirements
    
    1. Install [MicroK8s](https://microk8s.io/)
    
    1. Make sure all ports are open for [microk8s](https://microk8s.io/docs/)
    
    1. Enable `helm3`, `storage`, `ingress` and `dns`.
    
        ```bash
        sudo microk8s.enable helm3 storage ingress dns
        ```
        
    1. **Optional[alpha]:** If using Istio please enable it.  Please note that at the moment Istio ingress is not supported with Microk8s.
    
        ```bash
        sudo microk8s.enable istio
        ```   
      
2. Install using one of the following :

=== "Helm"
    ## Install Gluu using Helm
    
    ### Prerequisites
    
    - Kubernetes >=1.19x
    - Persistent volume provisioner support in the underlying infrastructure
    - Install [Helm3](https://helm.sh/docs/using_helm/)
    
    ### Quickstart
    
    1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](#build-pygluu-kubernetespyz-manually).
    
    1. **Optional:** If using couchbase as the persistence backend. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`
    
    1. Run :
    
      ```bash
      ./pygluu-kubernetes.pyz helm-install
      ```
      
    #### Installing Gluu using Helm manually
    
    1. **Optional if not using istio ingress:** Install [nginx-ingress](https://github.com/kubernetes/ingress-nginx) Helm [Chart](https://github.com/helm/charts/tree/master/stable/nginx-ingress).
    
       ```bash
       helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
       helm repo add stable https://charts.helm.sh/stable
       helm repo update
       helm install <nginx-release-name> ingress-nginx/ingress-nginx --namespace=<nginx-namespace>
       ```
    
    1.  - If the FQDN for gluu i.e `demoexample.gluu.org` is registered and globally resolvable, forward it to the loadbalancers address created in the previous step by nginx-ingress. A record can be added on most cloud providers to forward the domain to the loadbalancer. Forexample, on AWS assign a CNAME record for the LoadBalancer DNS name, or use Amazon Route 53 to create a hosted zone. More details in this [AWS guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/using-domain-names-with-elb.html?icmpid=docs_elb_console). Another example on [GCE](https://medium.com/@kungusamuel90/custom-domain-name-mapping-for-k8s-on-gcp-4dc263b2dabe).
    
        - If the FQDN is not registered acquire the loadbalancers ip if on **GCE**, or **Azure** using `kubectl get svc <release-name>-nginx-ingress-controller --output jsonpath='{.status.loadBalancer.ingress[0].ip}'` and if on **AWS** get the loadbalancers addresss using `kubectl -n ingress-nginx get svc ingress-nginx \--output jsonpath='{.status.loadBalancer.ingress[0].hostname}'`.
    
    1.  - If deploying on the cloud make sure to take a look at the helm cloud specific notes before continuing.
    
          * [EKS](#eks-helm-notes)
          * [GKE](#gke-helm-notes)
    
        - If deploying locally make sure to take a look at the helm specific notes bellow before continuing.
    
          * [Minikube](#minikube-helm-notes)
          * [MicroK8s](#microk8s-helm-notes)
    
    1.  **Optional:** If using couchbase as the persistence backend.
        
        1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](#build-pygluu-kubernetespyz-manually).
        
        1. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`
    
        1.  Run:
        
           ```bash
           ./pygluu-kubernetes.pyz couchbase-install
           ```
           
        1. Open `settings.json` file generated from the previous step and copy over the values of `COUCHBASE_URL` and `COUCHBASE_USER`   to `global.gluuCouchbaseUrl` and `global.gluuCouchbaseUser` in `values.yaml` respectively. 
    
    1.  Make sure you are in the same directory as the `values.yaml` file and run:
    
       ```bash
       helm install <release-name> -f values.yaml -n <namespace> .
       ```
    
    ### EKS helm notes
    
    #### Required changes to the `values.yaml`
    
      Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appropriate values :
    
      ```yaml
      #global values to be used across charts
      global:
        provisioner: kubernetes.io/aws-ebs #CHANGE-THIS
        lbAddr: "" #CHANGE-THIS to the address received in the previous step axx-109xx52.us-west-2.elb.amazonaws.com
        domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
        isDomainRegistered: "false" # CHANGE-THIS  "true" or "false" to specify if the domain above is registered or not.
    
      nginx:
        ingress:
          enabled: true
          path: /
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
          tls:
            - secretName: tls-certificate
              hosts:
                - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      ```    
    
      Tweak the optional [parameters](#configuration) in `values.yaml` to fit the setup needed.
    
    ### GKE helm notes
    
    #### Required changes to the `values.yaml`
    
      Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :
    
      ```yaml
      #global values to be used across charts
      global:
        provisioner: kubernetes.io/gce-pd #CHANGE-THIS
        lbAddr: ""
        domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
        # Networking configs
        lbIp: "" #CHANGE-THIS  to the IP received from the previous step
        isDomainRegistered: "false" # CHANGE-THIS  "true" or "false" to specify if the domain above is registered or not.
      nginx:
        ingress:
          enabled: true
          path: /
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
          tls:
            - secretName: tls-certificate
              hosts:
                - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      ```
    
      Tweak the optional [parameters](#configuration) in `values.yaml` to fit the setup needed.
    
    ### Minikube helm notes
    
    #### Required changes to the `values.yaml`
    
      Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :
    
      ```yaml
      #global values to be used across charts
      global:
        provisioner: k8s.io/minikube-hostpath #CHANGE-THIS
        lbAddr: ""
        domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
        lbIp: "" #CHANGE-THIS  to the IP of minikube <minikube ip>
    
      nginx:
        ingress:
          enabled: true
          path: /
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
          tls:
            - secretName: tls-certificate
              hosts:
                - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      ```
    
      Tweak the optional [parameters](#configuration) in `values.yaml` to fit the setup needed.
    
    - Map gluus FQDN at `/etc/hosts` file  to the minikube IP as shown below.
    
        ```bash
        ##
        # Host Database
        #
        # localhost is used to configure the loopback interface
        # when the system is booting.  Do not change this entry.
        ##
        192.168.99.100	demoexample.gluu.org #minikube IP and example domain
        127.0.0.1	localhost
        255.255.255.255	broadcasthost
        ::1             localhost
        ```
    
    ### Microk8s helm notes
      
    #### Required changes to the `values.yaml`
    
      Inside the global `values.yaml` change the marked keys with `CHANGE-THIS`  to the appopriate values :
    
      ```yaml
      #global values to be used across charts
      global:
        provisioner: microk8s.io/hostpath #CHANGE-THIS
        lbAddr: ""
        domain: demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
        lbIp: "" #CHANGE-THIS  to the IP of the microk8s vm
    
      nginx:
        ingress:
          enabled: true
          path: /
          hosts:
            - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
          tls:
            - secretName: tls-certificate
              hosts:
                - demoexample.gluu.org #CHANGE-THIS to the FQDN used for Gluu
      ```
    
      Tweak the optional [parameteres](#configuration) in `values.yaml` to fit the setup needed.
    
    - Map gluus FQDN at `/etc/hosts` file  to the microk8s vm IP as shown below.
    
      ```bash
      ##
      # Host Database
      #
      # localhost is used to configure the loopback interface
      # when the system is booting.  Do not change this entry.
      ##
      192.168.99.100	demoexample.gluu.org #microk8s IP and example domain
      127.0.0.1	localhost
      255.255.255.255	broadcasthost
      ::1             localhost
      ```
      
    ### Uninstalling the Chart
    
    To uninstall/delete `my-release` deployment:
    
    `helm delete <my-release>`
    
    If during installation the release was not defined, release name is checked by running `$ helm ls` then deleted using the previous command and the default release name.
    
    ### Configuration
    
    === "global"

        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | global | object | `{"alb":{"ingress":false},"azureStorageAccountType":"Standard_LRS","azureStorageKind":"Managed","cloud":{"testEnviroment":false},"cnGoogleApplicationCredentials":"/etc/gluu/conf/google-credentials.json","config":{"enabled":true},"configAdapterName":"kubernetes","configSecretAdapter":"kubernetes","cr-rotate":{"enabled":false},"domain":"demoexample.gluu.org","fido2":{"enabled":false},"gcePdStorageType":"pd-standard","gluuJackrabbitCluster":"true","gluuPersistenceType":"couchbase","isDomainRegistered":"false","istio":{"enabled":false,"ingress":false,"namespace":"istio-system"},"jackrabbit":{"enabled":true},"lbIp":"","ldapServiceName":"opendj","nginx-ingress":{"enabled":true},"opendj":{"enabled":true},"oxauth":{"enabled":true},"oxauth-key-rotation":{"enabled":false},"oxd-server":{"enabled":false},"oxshibboleth":{"enabled":false},"oxtrust":{"enabled":true},"persistence":{"enabled":true},"scim":{"enabled":false},"storageClass":{"allowVolumeExpansion":true,"allowedTopologies":[],"mountOptions":["debug"],"parameters":{},"provisioner":"microk8s.io/hostpath","reclaimPolicy":"Retain","volumeBindingMode":"WaitForFirstConsumer"},"upgrade":{"enabled":false},"usrEnvs":{"normal":{},"secret":{}}}` | Parameters used globally across all services helm charts. |
        | global.alb.ingress | bool | `false` | Activates ALB ingress |
        | global.azureStorageAccountType | string | `"Standard_LRS"` | Volume storage type if using Azure disks. |
        | global.azureStorageKind | string | `"Managed"` | Azure storage kind if using Azure disks |
        | global.cloud.testEnviroment | bool | `false` | Boolean flag if enabled will strip resources requests and limits from all services. |
        | global.cnGoogleApplicationCredentials | string | `"/etc/gluu/conf/google-credentials.json"` | Base64 encoded service account. The sa must have roles/secretmanager.admin to use Google secrets and roles/spanner.databaseUser to use Spanner. |
        | global.config.enabled | bool | `true` | Boolean flag to enable/disable the configuration chart. This normally should never be false |
        | global.configAdapterName | string | `"kubernetes"` | The config backend adapter that will hold Gluu configuration layer. google|kubernetes |
        | global.configSecretAdapter | string | `"kubernetes"` | The config backend adapter that will hold Gluu secret layer. google|kubernetes |
        | global.cr-rotate.enabled | bool | `false` | Boolean flag to enable/disable the cr-rotate chart. |
        | global.domain | string | `"demoexample.gluu.org"` | Fully qualified domain name to be used for Gluu installation. This address will be used to reach Gluu services. |
        | global.fido2.enabled | bool | `false` | Boolean flag to enable/disable the fido2 chart. |
        | global.gcePdStorageType | string | `"pd-standard"` | GCE storage kind if using Google disks |
        | global.gluuJackrabbitCluster | string | `"true"` | Boolean flag if enabled will enable jackrabbit in cluster mode with Postgres. |
        | global.gluuPersistenceType | string | `"couchbase"` | Persistence backend to run Gluu with ldap|couchbase|hybrid|sql|spanner. |
        | global.isDomainRegistered | string | `"false"` | Boolean flag to enable mapping global.lbIp  to global.fqdn inside pods on clouds that provide static ip for loadbalancers. On cloud that provide only addresses to the LB this flag will enable a script to actively scan config.configmap.lbAddr and update the hosts file inside the pods automatically. |
        | global.istio.enabled | bool | `false` | Boolean flag that enables using istio gateway for Gluu. This assumes istio ingress is installed and hence the LB is available. |
        | global.istio.ingress | bool | `false` | Boolean flag that enables using istio side cars with Gluu services. |
        | global.istio.namespace | string | `"istio-system"` | The namespace istio is deployed in. The is normally istio-system. |
        | global.jackrabbit.enabled | bool | `true` | Boolean flag to enable/disable the jackrabbit chart. For more information on how it is used inside Gluu https://gluu.org/docs/gluu-server/4.2/installation-guide/install-kubernetes/#working-with-jackrabbit. If disabled oxShibboleth cannot be run. |
        | global.lbIp | string | `""` | The Loadbalancer IP created by nginx or istio on clouds that provide static IPs. This is not needed if `global.domain` is globally resolvable. |
        | global.ldapServiceName | string | `"opendj"` | Name of the OpenDJ service. Please keep it as default. |
        | global.nginx-ingress.enabled | bool | `true` | Boolean flag to enable/disable the nginx-ingress definitions chart. |
        | global.opendj.enabled | bool | `true` | Boolean flag to enable/disable the OpenDJ  chart. |
        | global.oxauth-key-rotation.enabled | bool | `false` | Boolean flag to enable/disable the oxauth-server-key rotation cronjob chart. |
        | global.oxauth.enabled | bool | `true` | Boolean flag to enable/disable oxauth chart. You should never set this to false. |
        | global.oxd-server.enabled | bool | `false` | Boolean flag to enable/disable the oxd-server chart. |
        | global.oxshibboleth.enabled | bool | `false` | Boolean flag to enable/disable the oxShibbboleth chart. |
        | global.oxtrust.enabled | bool | `true` | Boolean flag to enable/disable the oxtrust chart. |
        | global.persistence.enabled | bool | `true` | Boolean flag to enable/disable the persistence chart. |
        | global.scim.enabled | bool | `false` | Boolean flag to enable/disable the SCIM chart. |
        | global.storageClass | object | `{"allowVolumeExpansion":true,"allowedTopologies":[],"mountOptions":["debug"],"parameters":{},"provisioner":"microk8s.io/hostpath","reclaimPolicy":"Retain","volumeBindingMode":"WaitForFirstConsumer"}` | StorageClass section for Jackrabbit and OpenDJ charts. This is not currently used by the openbanking distribution. You may specify custom parameters as needed. |
        | global.storageClass.parameters | object | `{}` | parameters: |
        | global.upgrade.enabled | bool | `false` | Boolean flag used when running helm upgrade command. This allows upgrading the chart without immutable objects errors. |
        | global.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service. Envs defined in global.userEnvs will be globally available to all services |
        | global.usrEnvs.normal | object | `{}` | Add custom normal envs to the service. variable1: value1 |
        | global.usrEnvs.secret | object | `{}` | Add custom secret envs to the service. variable1: value1 |

    === "config"   
 
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | config | object | `{"adminPass":"P@ssw0rd","city":"Austin","configmap":{"cnConfigGoogleSecretNamePrefix":"gluu","cnConfigGoogleSecretVersionId":"latest","cnGoogleProjectId":"google-project-to-save-config-and-secrets-to","cnGoogleSecretManagerPassPhrase":"Test1234#","cnGoogleServiceAccount":"SWFtTm90YVNlcnZpY2VBY2NvdW50Q2hhbmdlTWV0b09uZQo=","cnGoogleSpannerDatabaseId":"","cnGoogleSpannerInstanceId":"","cnSecretGoogleSecretNamePrefix":"gluu","cnSecretGoogleSecretVersionId":"latest","cnSqlDbDialect":"mysql","cnSqlDbHost":"my-release-mysql.default.svc.cluster.local","cnSqlDbName":"gluu","cnSqlDbPort":3306,"cnSqlDbTimezone":"UTC","cnSqlDbUser":"gluu","cnSqlPasswordFile":"/etc/gluu/conf/sql_password","cnSqldbUserPassword":"Test1234#","containerMetadataName":"kubernetes","gluuCacheType":"NATIVE_PERSISTENCE","gluuCasaEnabled":false,"gluuCouchbaseBucketPrefix":"gluu","gluuCouchbaseCertFile":"/etc/certs/couchbase.crt","gluuCouchbaseCrt":"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURlakNDQW1LZ0F3SUJBZ0lKQUwyem5UWlREUHFNTUEwR0NTcUdTSWIzRFFFQkN3VUFNQzB4S3pBcEJnTlYKQkFNTUlpb3VZMkpuYkhWMUxtUmxabUYxYkhRdWMzWmpMbU5zZFhOMFpYSXViRzlqWVd3d0hoY05NakF3TWpBMQpNRGt4T1RVeFdoY05NekF3TWpBeU1Ea3hPVFV4V2pBdE1Tc3dLUVlEVlFRRERDSXFMbU5pWjJ4MWRTNWtaV1poCmRXeDBMbk4yWXk1amJIVnpkR1Z5TG14dlkyRnNNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUIKQ2dLQ0FRRUFycmQ5T3lvSnRsVzhnNW5nWlJtL2FKWjJ2eUtubGU3dVFIUEw4Q2RJa1RNdjB0eHZhR1B5UkNQQgo3RE00RTFkLzhMaU5takdZZk41QjZjWjlRUmNCaG1VNmFyUDRKZUZ3c0x0cTFGT3MxaDlmWGo3d3NzcTYrYmlkCjV6Umw3UEE0YmdvOXVkUVRzU1UrWDJUUVRDc0dxVVVPWExrZ3NCMjI0RDNsdkFCbmZOeHcvYnFQa2ZCQTFxVzYKVXpxellMdHN6WE5GY0dQMFhtU3c4WjJuaFhhUGlva2pPT2dyMkMrbVFZK0htQ2xGUWRpd2g2ZjBYR0V0STMrKwoyMStTejdXRkF6RlFBVUp2MHIvZnk4TDRXZzh1YysvalgwTGQrc2NoQTlNQjh3YmJORUp2ZjNMOGZ5QjZ0cTd2CjF4b0FnL0g0S1dJaHdqSEN0dFVnWU1oU0xWV3UrUUlEQVFBQm80R2NNSUdaTUIwR0ExVWREZ1FXQkJTWmQxWU0KVGNIRVZjSENNUmp6ejczZitEVmxxREJkQmdOVkhTTUVWakJVZ0JTWmQxWU1UY0hFVmNIQ01Sanp6NzNmK0RWbApxS0V4cEM4d0xURXJNQ2tHQTFVRUF3d2lLaTVqWW1kc2RYVXVaR1ZtWVhWc2RDNXpkbU11WTJ4MWMzUmxjaTVzCmIyTmhiSUlKQUwyem5UWlREUHFNTUF3R0ExVWRFd1FGTUFNQkFmOHdDd1lEVlIwUEJBUURBZ0VHTUEwR0NTcUcKU0liM0RRRUJDd1VBQTRJQkFRQk9meTVWSHlKZCtWUTBXaUQ1aSs2cmhidGNpSmtFN0YwWVVVZnJ6UFN2YWVFWQp2NElVWStWOC9UNnE4Mk9vVWU1eCtvS2dzbFBsL01nZEg2SW9CRnVtaUFqek14RTdUYUhHcXJ5dk13Qk5IKzB5CnhadG9mSnFXQzhGeUlwTVFHTEs0RVBGd3VHRlJnazZMRGR2ZEN5NVdxWW1MQWdBZVh5VWNaNnlHYkdMTjRPUDUKZTFiaEFiLzRXWXRxRHVydFJrWjNEejlZcis4VWNCVTRLT005OHBZN05aaXFmKzlCZVkvOEhZaVQ2Q0RRWWgyTgoyK0VWRFBHcFE4UkVsRThhN1ZLL29MemlOaXFyRjllNDV1OU1KdjM1ZktmNUJjK2FKdWduTGcwaUZUYmNaT1prCkpuYkUvUENIUDZFWmxLaEFiZUdnendtS1dDbTZTL3g0TklRK2JtMmoKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=","gluuCouchbaseIndexNumReplica":0,"gluuCouchbasePass":"P@ssw0rd","gluuCouchbasePassFile":"/etc/gluu/conf/couchbase_password","gluuCouchbaseSuperUser":"admin","gluuCouchbaseSuperUserPass":"P@ssw0rd","gluuCouchbaseSuperUserPassFile":"/etc/gluu/conf/couchbase_superuser_password","gluuCouchbaseUrl":"cbgluu.default.svc.cluster.local","gluuCouchbaseUser":"gluu","gluuDocumentStoreType":"JCA","gluuJackrabbitAdminId":"admin","gluuJackrabbitAdminIdFile":"/etc/gluu/conf/jackrabbit_admin_id","gluuJackrabbitAdminPassFile":"/etc/gluu/conf/jackrabbit_admin_password","gluuJackrabbitPostgresDatabaseName":"jackrabbit","gluuJackrabbitPostgresHost":"postgresql.postgres.svc.cluster.local","gluuJackrabbitPostgresPasswordFile":"/etc/gluu/conf/postgres_password","gluuJackrabbitPostgresPort":5432,"gluuJackrabbitPostgresUser":"jackrabbit","gluuJackrabbitSyncInterval":300,"gluuJackrabbitUrl":"http://jackrabbit:8080","gluuLdapUrl":"opendj:1636","gluuMaxRamPercent":"75.0","gluuOxauthBackend":"oxauth:8080","gluuOxdAdminCertCn":"oxd-server","gluuOxdApplicationCertCn":"oxd-server","gluuOxdBindIpAddresses":"*","gluuOxdServerUrl":"oxd-server:8443","gluuOxtrustApiEnabled":false,"gluuOxtrustApiTestMode":false,"gluuOxtrustBackend":"oxtrust:8080","gluuOxtrustConfigGeneration":true,"gluuPassportEnabled":false,"gluuPassportFailureRedirectUrl":"","gluuPersistenceLdapMapping":"default","gluuRedisSentinelGroup":"","gluuRedisSslTruststore":"","gluuRedisType":"STANDALONE","gluuRedisUrl":"redis:6379","gluuRedisUseSsl":"false","gluuSamlEnabled":false,"gluuSyncCasaManifests":false,"gluuSyncShibManifests":false,"lbAddr":""},"countryCode":"US","dnsConfig":{},"dnsPolicy":"","email":"support@gluu.com","image":{"repository":"gluufederation/config-init","tag":"4.3.0_b1"},"ldapPass":"P@ssw0rd","migration":{"enabled":false,"migrationDataFormat":"ldif","migrationDir":"/ce-migration"},"orgName":"Gluu","redisPass":"P@assw0rd","resources":{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}},"state":"TX","usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Configuration parameters for setup and initial configuration secret and config layers used by Gluu services. |
        | config.adminPass | string | `"P@ssw0rd"` | Admin password to log in to the UI. |
        | config.city | string | `"Austin"` | City. Used for certificate creation. |
        | config.configmap.cnConfigGoogleSecretNamePrefix | string | `"gluu"` | Prefix for Gluu configuration secret in Google Secret Manager. Defaults to gluu. If left intact gluu-configuration secret will be created. Used only when global.configAdapterName and global.configSecretAdapter is set to google. |
        | config.configmap.cnConfigGoogleSecretVersionId | string | `"latest"` | Secret version to be used for configuration. Defaults to latest and should normally always stay that way. Used only when global.configAdapterName and global.configSecretAdapter is set to google. Used only when global.configAdapterName and global.configSecretAdapter is set to google. |
        | config.configmap.cnGoogleProjectId | string | `"google-project-to-save-config-and-secrets-to"` | Project id of the google project the secret manager belongs to. Used only when global.configAdapterName and global.configSecretAdapter is set to google. |
        | config.configmap.cnGoogleSecretManagerPassPhrase | string | `"Test1234#"` | Passphrase for Gluu secret in Google Secret Manager. This is used for encrypting and decrypting data from the Google Secret Manager. Used only when global.configAdapterName and global.configSecretAdapter is set to google. |
        | config.configmap.cnGoogleSpannerDatabaseId | string | `""` | Google Spanner Database ID. Used only when global.gluuPersistenceType is spanner. |
        | config.configmap.cnGoogleSpannerInstanceId | string | `""` | Google Spanner ID. Used only when global.gluuPersistenceType is spanner. |
        | config.configmap.cnSecretGoogleSecretNamePrefix | string | `"gluu"` | Prefix for Gluu secret in Google Secret Manager. Defaults to gluu. If left gluu-secret secret will be created. Used only when global.configAdapterName and global.configSecretAdapter is set to google. |
        | config.configmap.cnSqlDbDialect | string | `"mysql"` | SQL database dialect. `mysql` or `pgsql` |
        | config.configmap.cnSqlDbHost | string | `"my-release-mysql.default.svc.cluster.local"` | SQL database host uri. |
        | config.configmap.cnSqlDbName | string | `"gluu"` | SQL database username. |
        | config.configmap.cnSqlDbPort | int | `3306` | SQL database port. |
        | config.configmap.cnSqlDbTimezone | string | `"UTC"` | SQL database timezone. |
        | config.configmap.cnSqlDbUser | string | `"gluu"` | SQL database username. |
        | config.configmap.cnSqlPasswordFile | string | `"/etc/gluu/conf/sql_password"` | SQL password file holding password from config.configmap.cnSqldbUserPassword . |
        | config.configmap.cnSqldbUserPassword | string | `"Test1234#"` | SQL password  injected as config.configmap.cnSqlPasswordFile . |
        | config.configmap.gluuCacheType | string | `"NATIVE_PERSISTENCE"` | Cache type. `NATIVE_PERSISTENCE`, `REDIS`. or `IN_MEMORY`. Defaults to `NATIVE_PERSISTENCE` . |
        | config.configmap.gluuCasaEnabled | bool | `false` | Enable Casa flag . |
        | config.configmap.gluuCouchbaseBucketPrefix | string | `"gluu"` | The prefix of couchbase buckets. This helps with separation in between different environments and allows for the same couchbase cluster to be used by different setups of Gluu. |
        | config.configmap.gluuCouchbaseCertFile | string | `"/etc/certs/couchbase.crt"` | Location of `couchbase.crt` used by Couchbase SDK for tls termination. The file path must end with couchbase.crt. In mTLS setups this is not required. |
        | config.configmap.gluuCouchbaseCrt | string | `"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURlakNDQW1LZ0F3SUJBZ0lKQUwyem5UWlREUHFNTUEwR0NTcUdTSWIzRFFFQkN3VUFNQzB4S3pBcEJnTlYKQkFNTUlpb3VZMkpuYkhWMUxtUmxabUYxYkhRdWMzWmpMbU5zZFhOMFpYSXViRzlqWVd3d0hoY05NakF3TWpBMQpNRGt4T1RVeFdoY05NekF3TWpBeU1Ea3hPVFV4V2pBdE1Tc3dLUVlEVlFRRERDSXFMbU5pWjJ4MWRTNWtaV1poCmRXeDBMbk4yWXk1amJIVnpkR1Z5TG14dlkyRnNNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUIKQ2dLQ0FRRUFycmQ5T3lvSnRsVzhnNW5nWlJtL2FKWjJ2eUtubGU3dVFIUEw4Q2RJa1RNdjB0eHZhR1B5UkNQQgo3RE00RTFkLzhMaU5takdZZk41QjZjWjlRUmNCaG1VNmFyUDRKZUZ3c0x0cTFGT3MxaDlmWGo3d3NzcTYrYmlkCjV6Umw3UEE0YmdvOXVkUVRzU1UrWDJUUVRDc0dxVVVPWExrZ3NCMjI0RDNsdkFCbmZOeHcvYnFQa2ZCQTFxVzYKVXpxellMdHN6WE5GY0dQMFhtU3c4WjJuaFhhUGlva2pPT2dyMkMrbVFZK0htQ2xGUWRpd2g2ZjBYR0V0STMrKwoyMStTejdXRkF6RlFBVUp2MHIvZnk4TDRXZzh1YysvalgwTGQrc2NoQTlNQjh3YmJORUp2ZjNMOGZ5QjZ0cTd2CjF4b0FnL0g0S1dJaHdqSEN0dFVnWU1oU0xWV3UrUUlEQVFBQm80R2NNSUdaTUIwR0ExVWREZ1FXQkJTWmQxWU0KVGNIRVZjSENNUmp6ejczZitEVmxxREJkQmdOVkhTTUVWakJVZ0JTWmQxWU1UY0hFVmNIQ01Sanp6NzNmK0RWbApxS0V4cEM4d0xURXJNQ2tHQTFVRUF3d2lLaTVqWW1kc2RYVXVaR1ZtWVhWc2RDNXpkbU11WTJ4MWMzUmxjaTVzCmIyTmhiSUlKQUwyem5UWlREUHFNTUF3R0ExVWRFd1FGTUFNQkFmOHdDd1lEVlIwUEJBUURBZ0VHTUEwR0NTcUcKU0liM0RRRUJDd1VBQTRJQkFRQk9meTVWSHlKZCtWUTBXaUQ1aSs2cmhidGNpSmtFN0YwWVVVZnJ6UFN2YWVFWQp2NElVWStWOC9UNnE4Mk9vVWU1eCtvS2dzbFBsL01nZEg2SW9CRnVtaUFqek14RTdUYUhHcXJ5dk13Qk5IKzB5CnhadG9mSnFXQzhGeUlwTVFHTEs0RVBGd3VHRlJnazZMRGR2ZEN5NVdxWW1MQWdBZVh5VWNaNnlHYkdMTjRPUDUKZTFiaEFiLzRXWXRxRHVydFJrWjNEejlZcis4VWNCVTRLT005OHBZN05aaXFmKzlCZVkvOEhZaVQ2Q0RRWWgyTgoyK0VWRFBHcFE4UkVsRThhN1ZLL29MemlOaXFyRjllNDV1OU1KdjM1ZktmNUJjK2FKdWduTGcwaUZUYmNaT1prCkpuYkUvUENIUDZFWmxLaEFiZUdnendtS1dDbTZTL3g0TklRK2JtMmoKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo="` | Couchbase certificate authority string. This must be encoded using base64. This can also be found in your couchbase UI Security > Root Certificate. In mTLS setups this is not required. |
        | config.configmap.gluuCouchbaseIndexNumReplica | int | `0` | The number of replicas per index created. Please note that the number of index nodes must be one greater than the number of index replicas. That means if your couchbase cluster only has 2 index nodes you cannot place the number of replicas to be higher than 1. |
        | config.configmap.gluuCouchbasePass | string | `"P@ssw0rd"` | Couchbase password for the restricted user config.configmap.gluuCouchbaseUser  that is often used inside the services. The password must contain one digit, one uppercase letter, one lower case letter and one symbol . |
        | config.configmap.gluuCouchbasePassFile | string | `"/etc/gluu/conf/couchbase_password"` | The location of the Couchbase restricted user config.configmap.gluuCouchbaseUser password. The file path must end with couchbase_password |
        | config.configmap.gluuCouchbaseSuperUser | string | `"admin"` | The Couchbase super user (admin) user name. This user is used during initialization only. |
        | config.configmap.gluuCouchbaseSuperUserPass | string | `"P@ssw0rd"` | Couchbase password for the super user config.configmap.gluuCouchbaseSuperUser  that is used during the initialization process. The password must contain one digit, one uppercase letter, one lower case letter and one symbol |
        | config.configmap.gluuCouchbaseSuperUserPassFile | string | `"/etc/gluu/conf/couchbase_superuser_password"` | The location of the Couchbase restricted user config.configmap.gluuCouchbaseSuperUser password. The file path must end with couchbase_superuser_password. |
        | config.configmap.gluuCouchbaseUrl | string | `"cbgluu.default.svc.cluster.local"` | Couchbase URL. Used only when global.gluuPersistenceType is hybrid or couchbase. This should be in FQDN format for either remote or local Couchbase clusters. The address can be an internal address inside the kubernetes cluster |
        | config.configmap.gluuCouchbaseUser | string | `"gluu"` | Couchbase restricted user. Used only when global.gluuPersistenceType is hybrid or couchbase. |
        | config.configmap.gluuDocumentStoreType | string | `"JCA"` | Document store type to use for shibboleth files JCA or LOCAL. Note that if JCA is selected Apache Jackrabbit will be used. Jackrabbit also enables loading custom files across all services easily. |
        | config.configmap.gluuJackrabbitAdminId | string | `"admin"` | Jackrabbit admin uid. |
        | config.configmap.gluuJackrabbitAdminIdFile | string | `"/etc/gluu/conf/jackrabbit_admin_id"` | The location of the Jackrabbit admin uid config.gluuJackrabbitAdminId. The file path must end with jackrabbit_admin_id. |
        | config.configmap.gluuJackrabbitAdminPassFile | string | `"/etc/gluu/conf/jackrabbit_admin_password"` | The location of the Jackrabbit admin password jackrabbit.secrets.gluuJackrabbitAdminPassword. The file path must end with jackrabbit_admin_password. |
        | config.configmap.gluuJackrabbitPostgresDatabaseName | string | `"jackrabbit"` | Jackrabbit postgres database name. |
        | config.configmap.gluuJackrabbitPostgresHost | string | `"postgresql.postgres.svc.cluster.local"` | Postgres url |
        | config.configmap.gluuJackrabbitPostgresPasswordFile | string | `"/etc/gluu/conf/postgres_password"` | The location of the Jackrabbit postgres password file jackrabbit.secrets.gluuJackrabbitPostgresPassword. The file path must end with postgres_password. |
        | config.configmap.gluuJackrabbitPostgresPort | int | `5432` | Jackrabbit Postgres port |
        | config.configmap.gluuJackrabbitPostgresUser | string | `"jackrabbit"` | Jackrabbit Postgres uid |
        | config.configmap.gluuJackrabbitSyncInterval | int | `300` | Interval between files sync (default to 300 seconds). |
        | config.configmap.gluuJackrabbitUrl | string | `"http://jackrabbit:8080"` | Jackrabbit internal url. Normally left as default. |
        | config.configmap.gluuLdapUrl | string | `"opendj:1636"` | OpenDJ internal address. Leave as default. Used when `global.gluuPersistenceType` is set to `ldap`. |
        | config.configmap.gluuMaxRamPercent | string | `"75.0"` | Value passed to Java option -XX:MaxRAMPercentage |
        | config.configmap.gluuOxauthBackend | string | `"oxauth:8080"` | oxAuth internal address. Leave as default. |
        | config.configmap.gluuOxdAdminCertCn | string | `"oxd-server"` | OXD serve OAuth client admin certificate common name. This should be left to the default value client-api . |
        | config.configmap.gluuOxdApplicationCertCn | string | `"oxd-server"` | OXD server OAuth client application certificate common name. This should be left to the default value client-api. |
        | config.configmap.gluuOxdBindIpAddresses | string | `"*"` | OXD server bind address. This limits what ip ranges can access the client-api. This should be left as * and controlled by a NetworkPolicy |
        | config.configmap.gluuOxdServerUrl | string | `"oxd-server:8443"` | OXD server Oauth client address. This should be left intact in kubernetes as it uses the internal address format. |
        | config.configmap.gluuOxtrustApiEnabled | bool | `false` | Enable oxTrust API |
        | config.configmap.gluuOxtrustApiTestMode | bool | `false` | Enable oxTrust API testmode |
        | config.configmap.gluuOxtrustBackend | string | `"oxtrust:8080"` | oxTrust internal address. Leave as default. |
        | config.configmap.gluuOxtrustConfigGeneration | bool | `true` | Whether to generate oxShibboleth configuration or not (default to true). |
        | config.configmap.gluuPassportEnabled | bool | `false` | Boolean flag to enable/disable passport chart |
        | config.configmap.gluuPassportFailureRedirectUrl | string | `""` | TEMP KEY TO BE REMOVED IN 4.3 which allows passport failure redirect url to be specified. |
        | config.configmap.gluuPersistenceLdapMapping | string | `"default"` | Specify data that should be saved in LDAP (one of default, user, cache, site, token, or session; default to default). Note this environment only takes effect when `global.gluuPersistenceType`  is set to `hybrid`. |
        | config.configmap.gluuRedisSentinelGroup | string | `""` | Redis Sentinel Group. Often set when `config.configmap.gluuRedisType` is set to `SENTINEL`. Can be used when  `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.configmap.gluuRedisSslTruststore | string | `""` | Redis SSL truststore. Optional. Can be used when  `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.configmap.gluuRedisType | string | `"STANDALONE"` | Redis service type. `STANDALONE` or `CLUSTER`. Can be used when  `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.configmap.gluuRedisUrl | string | `"redis:6379"` | Redis URL and port number <url>:<port>. Can be used when  `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.configmap.gluuRedisUseSsl | string | `"false"` | Boolean to use SSL in Redis. Can be used when  `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.configmap.gluuSamlEnabled | bool | `false` | Enable SAML-related features; UI menu, etc. |
        | config.configmap.gluuSyncCasaManifests | bool | `false` | Activate manual Casa files sync - depreciated |
        | config.configmap.gluuSyncShibManifests | bool | `false` | Activate manual Shib files sync - depreciated |
        | config.countryCode | string | `"US"` | Country code. Used for certificate creation. |
        | config.dnsConfig | object | `{}` | Add custom dns config |
        | config.dnsPolicy | string | `""` | Add custom dns policy |
        | config.email | string | `"support@gluu.com"` | Email address of the administrator usually. Used for certificate creation. |
        | config.image.repository | string | `"gluufederation/config-init"` | Image  to use for deploying. |
        | config.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | config.ldapPass | string | `"P@ssw0rd"` | LDAP admin password if OpennDJ is used for persistence. |
        | config.migration | object | `{"enabled":false,"migrationDataFormat":"ldif","migrationDir":"/ce-migration"}` | CE to CN Migration section |
        | config.migration.enabled | bool | `false` | Boolean flag to enable migration from CE |
        | config.migration.migrationDataFormat | string | `"ldif"` | migration data-format depending on persistence backend. Supported data formats are ldif, couchbase+json, spanner+avro, postgresql+json, and mysql+json. |
        | config.migration.migrationDir | string | `"/ce-migration"` | Directory holding all migration files |
        | config.orgName | string | `"Gluu"` | Organization name. Used for certificate creation. |
        | config.redisPass | string | `"P@assw0rd"` | Redis admin password if `config.configmap.gluuCacheType` is set to `REDIS`. |
        | config.resources | object | `{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}}` | Resource specs. |
        | config.resources.limits.cpu | string | `"300m"` | CPU limit. |
        | config.resources.limits.memory | string | `"300Mi"` | Memory limit. |
        | config.resources.requests.cpu | string | `"300m"` | CPU request. |
        | config.resources.requests.memory | string | `"300Mi"` | Memory request. |
        | config.state | string | `"TX"` | State code. Used for certificate creation. |
        | config.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service. |
        | config.usrEnvs.normal | object | `{}` | Add custom normal envs to the service. variable1: value1 |
        | config.usrEnvs.secret | object | `{}` | Add custom secret envs to the service. variable1: value1 |
        | config.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | config.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "nginx-ingress"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | nginx-ingress | object | `{"ingress":{"additionalAnnotations":{"kubernetes.io/ingress.class":"nginx"},"adminUiEnabled":true,"authServerEnabled":true,"casaEnabled":true,"enabled":true,"fido2ConfigEnabled":false,"hosts":["demoexample.gluu.org"],"openidConfigEnabled":true,"path":"/","scimConfigEnabled":false,"scimEnabled":false,"tls":[{"hosts":["demoexample.gluu.org"],"secretName":"tls-certificate"}],"u2fConfigEnabled":true,"uma2ConfigEnabled":true,"webdiscoveryEnabled":true,"webfingerEnabled":true}}` | Nginx ingress definitions chart |
        | nginx-ingress.ingress.additionalAnnotations | object | `{"kubernetes.io/ingress.class":"nginx"}` | Additional annotations that will be added across all ingress definitions in the format of {cert-manager.io/issuer: "letsencrypt-prod"} Enable client certificate authentication nginx.ingress.kubernetes.io/auth-tls-verify-client: "optional" Create the secret containing the trusted ca certificates nginx.ingress.kubernetes.io/auth-tls-secret: "gluu/tls-certificate" Specify the verification depth in the client certificates chain nginx.ingress.kubernetes.io/auth-tls-verify-depth: "1" Specify if certificates are passed to upstream server nginx.ingress.kubernetes.io/auth-tls-pass-certificate-to-upstream: "true" |
        | nginx-ingress.ingress.adminUiEnabled | bool | `true` | Enable Admin UI endpoints /identity |
        | nginx-ingress.ingress.authServerEnabled | bool | `true` | Enable Auth server endpoints /oxauth |
        | nginx-ingress.ingress.casaEnabled | bool | `true` | Enable casa endpoints /casa |
        | nginx-ingress.ingress.fido2ConfigEnabled | bool | `false` | Enable endpoint /.well-known/fido2-configuration |
        | nginx-ingress.ingress.openidConfigEnabled | bool | `true` | Enable endpoint /.well-known/openid-configuration |
        | nginx-ingress.ingress.scimConfigEnabled | bool | `false` | Enable endpoint /.well-known/scim-configuration |
        | nginx-ingress.ingress.scimEnabled | bool | `false` | Enable SCIM endpoints /scim |
        | nginx-ingress.ingress.u2fConfigEnabled | bool | `true` | Enable endpoint /.well-known/fido-configuration |
        | nginx-ingress.ingress.uma2ConfigEnabled | bool | `true` | Enable endpoint /.well-known/uma2-configuration |
        | nginx-ingress.ingress.webdiscoveryEnabled | bool | `true` | Enable endpoint /.well-known/simple-web-discovery |
        | nginx-ingress.ingress.webfingerEnabled | bool | `true` | Enable endpoint /.well-known/webfinger |

    === "jackrabbit"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | jackrabbit | object | `{"clusterId":"","dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/jackrabbit","tag":"4.3.0_b1"},"livenessProbe":{"initialDelaySeconds":25,"periodSeconds":25,"tcpSocket":{"port":"http-jackrabbit"},"timeoutSeconds":5},"readinessProbe":{"initialDelaySeconds":30,"periodSeconds":30,"tcpSocket":{"port":"http-jackrabbit"},"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"1500m","memory":"1000Mi"},"requests":{"cpu":"1500m","memory":"1000Mi"}},"secrets":{"gluuJackrabbitAdminPass":"Test1234#","gluuJackrabbitPostgresPass":"P@ssw0rd"},"service":{"jackRabbitServiceName":"jackrabbit","name":"http-jackrabbit","port":8080},"storage":{"size":"5Gi"},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Jackrabbit Oak is a complementary implementation of the JCR specification. It is an effort to implement a scalable and performant hierarchical content repository for use as the foundation of modern world-class web sites and other demanding content applications https://jackrabbit.apache.org/jcr/index.html |
        | jackrabbit.clusterId | string | `""` | This id needs to be unique to each kubernetes cluster in a multi cluster setup west, east, south, north, region ...etc If left empty it will be randomly generated. |
        | jackrabbit.dnsConfig | object | `{}` | Add custom dns config |
        | jackrabbit.dnsPolicy | string | `""` | Add custom dns policy |
        | jackrabbit.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | jackrabbit.hpa.behavior | object | `{}` | Scaling Policies |
        | jackrabbit.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | jackrabbit.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | jackrabbit.image.repository | string | `"gluufederation/jackrabbit"` | Image  to use for deploying. |
        | jackrabbit.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | jackrabbit.livenessProbe | object | `{"initialDelaySeconds":25,"periodSeconds":25,"tcpSocket":{"port":"http-jackrabbit"},"timeoutSeconds":5}` | Configure the liveness healthcheck for the Jackrabbit if needed. |
        | jackrabbit.livenessProbe.tcpSocket | object | `{"port":"http-jackrabbit"}` | Executes tcp healthcheck. |
        | jackrabbit.readinessProbe | object | `{"initialDelaySeconds":30,"periodSeconds":30,"tcpSocket":{"port":"http-jackrabbit"},"timeoutSeconds":5}` | Configure the readiness healthcheck for the Jackrabbit if needed. |
        | jackrabbit.readinessProbe.tcpSocket | object | `{"port":"http-jackrabbit"}` | Executes tcp healthcheck. |
        | jackrabbit.replicas | int | `1` | Service replica number. |
        | jackrabbit.resources | object | `{"limits":{"cpu":"1500m","memory":"1000Mi"},"requests":{"cpu":"1500m","memory":"1000Mi"}}` | Resource specs. |
        | jackrabbit.resources.limits.cpu | string | `"1500m"` | CPU limit. |
        | jackrabbit.resources.limits.memory | string | `"1000Mi"` | Memory limit. |
        | jackrabbit.resources.requests.cpu | string | `"1500m"` | CPU request. |
        | jackrabbit.resources.requests.memory | string | `"1000Mi"` | Memory request. |
        | jackrabbit.secrets.gluuJackrabbitAdminPass | string | `"Test1234#"` | Jackrabbit admin uid password |
        | jackrabbit.secrets.gluuJackrabbitPostgresPass | string | `"P@ssw0rd"` | Jackrabbit Postgres uid password |
        | jackrabbit.service.jackRabbitServiceName | string | `"jackrabbit"` | Name of the Jackrabbit service. Please keep it as default. |
        | jackrabbit.service.name | string | `"http-jackrabbit"` | The name of the jackrabbit port within the jackrabbit service. Please keep it as default. |
        | jackrabbit.service.port | int | `8080` | Port of the jackrabbit service. Please keep it as default. |
        | jackrabbit.storage.size | string | `"5Gi"` | Jackrabbit volume size |
        | jackrabbit.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | jackrabbit.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | jackrabbit.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | jackrabbit.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | jackrabbit.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "opendj"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | opendj | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/opendj","tag":"4.3.0_b1"},"livenessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"multiCluster":{"enabled":false,"serfAdvertiseAddr":"firstldap.gluu.org:30946","serfKey":"Z51b6PgKU1MZ75NCZOTGGoc0LP2OF3qvF6sjxHyQCYk=","serfPeers":["firstldap.gluu.org:30946","secondldap.gluu.org:31946"]},"persistence":{"size":"5Gi"},"ports":{"tcp-admin":{"nodePort":"","port":4444,"protocol":"TCP","targetPort":4444},"tcp-ldap":{"nodePort":"","port":1389,"protocol":"TCP","targetPort":1389},"tcp-ldaps":{"nodePort":"","port":1636,"protocol":"TCP","targetPort":1636},"tcp-repl":{"nodePort":"","port":8989,"protocol":"TCP","targetPort":8989},"tcp-serf":{"nodePort":"","port":7946,"protocol":"TCP","targetPort":7946},"udp-serf":{"nodePort":"","port":7946,"protocol":"UDP","targetPort":7946}},"readinessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"1500m","memory":"2000Mi"},"requests":{"cpu":"1500m","memory":"2000Mi"}},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | OpenDJ is a directory server which implements a wide range of Lightweight Directory Access Protocol and related standards, including full compliance with LDAPv3 but also support for Directory Service Markup Language (DSMLv2).Written in Java, OpenDJ offers multi-master replication, access control, and many extensions. |
        | opendj.dnsConfig | object | `{}` | Add custom dns config |
        | opendj.dnsPolicy | string | `""` | Add custom dns policy |
        | opendj.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | opendj.hpa.behavior | object | `{}` | Scaling Policies |
        | opendj.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | opendj.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | opendj.image.repository | string | `"gluufederation/opendj"` | Image  to use for deploying. |
        | opendj.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | opendj.livenessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for OpenDJ if needed. https://github.com/GluuFederation/docker-opendj/blob/4.3/scripts/healthcheck.py |
        | opendj.livenessProbe.exec | object | `{"command":["python3","/app/scripts/healthcheck.py"]}` | Executes the python3 healthcheck. |
        | opendj.multiCluster.enabled | bool | `false` | Enable OpenDJ multiCluster mode. This flag enables loading keys under `opendj.multiCluster` |
        | opendj.multiCluster.serfAdvertiseAddr | string | `"firstldap.gluu.org:30946"` | OpenDJ Serf advertise address for the cluster |
        | opendj.multiCluster.serfKey | string | `"Z51b6PgKU1MZ75NCZOTGGoc0LP2OF3qvF6sjxHyQCYk="` | Serf key. This key will automatically sync across clusters. |
        | opendj.multiCluster.serfPeers | list | `["firstldap.gluu.org:30946","secondldap.gluu.org:31946"]` | Serf peer addresses. One per cluster. |
        | opendj.persistence.size | string | `"5Gi"` | OpenDJ volume size |
        | opendj.ports | object | `{"tcp-admin":{"nodePort":"","port":4444,"protocol":"TCP","targetPort":4444},"tcp-ldap":{"nodePort":"","port":1389,"protocol":"TCP","targetPort":1389},"tcp-ldaps":{"nodePort":"","port":1636,"protocol":"TCP","targetPort":1636},"tcp-repl":{"nodePort":"","port":8989,"protocol":"TCP","targetPort":8989},"tcp-serf":{"nodePort":"","port":7946,"protocol":"TCP","targetPort":7946},"udp-serf":{"nodePort":"","port":7946,"protocol":"UDP","targetPort":7946}}` | servicePorts values used in StatefulSet container |
        | opendj.readinessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for OpenDJ if needed. https://github.com/GluuFederation/docker-opendj/blob/4.3/scripts/healthcheck.py |
        | opendj.replicas | int | `1` | Service replica number. |
        | opendj.resources | object | `{"limits":{"cpu":"1500m","memory":"2000Mi"},"requests":{"cpu":"1500m","memory":"2000Mi"}}` | Resource specs. |
        | opendj.resources.limits.cpu | string | `"1500m"` | CPU limit. |
        | opendj.resources.limits.memory | string | `"2000Mi"` | Memory limit. |
        | opendj.resources.requests.cpu | string | `"1500m"` | CPU request. |
        | opendj.resources.requests.memory | string | `"2000Mi"` | Memory request. |
        | opendj.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | opendj.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | opendj.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | opendj.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | opendj.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "persistence"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | persistence | object | `{"dnsConfig":{},"dnsPolicy":"","image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/persistence","tag":"4.3.0_b1"},"resources":{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Job to generate data and initial config for Gluu Server persistence layer. |
        | persistence.dnsConfig | object | `{}` | Add custom dns config |
        | persistence.dnsPolicy | string | `""` | Add custom dns policy |
        | persistence.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | persistence.image.repository | string | `"gluufederation/persistence"` | Image  to use for deploying. |
        | persistence.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | persistence.resources | object | `{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}}` | Resource specs. |
        | persistence.resources.limits.cpu | string | `"300m"` | CPU limit |
        | persistence.resources.limits.memory | string | `"300Mi"` | Memory limit. |
        | persistence.resources.requests.cpu | string | `"300m"` | CPU request. |
        | persistence.resources.requests.memory | string | `"300Mi"` | Memory request. |
        | persistence.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | persistence.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | persistence.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | persistence.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | persistence.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "oxauth"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxauth | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/oxauth","tag":"4.3.0_b1"},"livenessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"2500m","memory":"2500Mi"},"requests":{"cpu":"2500m","memory":"2500Mi"}},"service":{"name":"http-oxauth","oxAuthServiceName":"auth-server","port":8080},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | OAuth Authorization Server, the OpenID Connect Provider, the UMA Authorization Server--this is the main Internet facing component of Gluu. It's the service that returns tokens, JWT's and identity assertions. This service must be Internet facing. |
        | oxauth.dnsConfig | object | `{}` | Add custom dns config |
        | oxauth.dnsPolicy | string | `""` | Add custom dns policy |
        | oxauth.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | oxauth.hpa.behavior | object | `{}` | Scaling Policies |
        | oxauth.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | oxauth.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxauth.image.repository | string | `"gluufederation/oxauth"` | Image  to use for deploying. |
        | oxauth.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxauth.livenessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for the auth server if needed. |
        | oxauth.livenessProbe.exec | object | `{"command":["python3","/app/scripts/healthcheck.py"]}` | Executes the python3 healthcheck. https://github.com/GluuFederation/docker-oxauth/blob/4.3/scripts/healthcheck.py |
        | oxauth.readinessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the auth server if needed. https://github.com/GluuFederation/docker-oxauth/blob/4.3/scripts/healthcheck.py |
        | oxauth.replicas | int | `1` | Service replica number. |
        | oxauth.resources | object | `{"limits":{"cpu":"2500m","memory":"2500Mi"},"requests":{"cpu":"2500m","memory":"2500Mi"}}` | Resource specs. |
        | oxauth.resources.limits.cpu | string | `"2500m"` | CPU limit. |
        | oxauth.resources.limits.memory | string | `"2500Mi"` | Memory limit. |
        | oxauth.resources.requests.cpu | string | `"2500m"` | CPU request. |
        | oxauth.resources.requests.memory | string | `"2500Mi"` | Memory request. |
        | oxauth.service.name | string | `"http-oxauth"` | The name of the oxauth port within the oxauth service. Please keep it as default. |
        | oxauth.service.oxAuthServiceName | string | `"auth-server"` | Name of the auth-server service. Please keep it as default. |
        | oxauth.service.port | int | `8080` | Port of the oxauth service. Please keep it as default. |
        | oxauth.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxauth.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxauth.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxauth.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxauth.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |


    === "oxtrust"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxtrust | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/oxtrust","tag":"4.3.0_b1"},"livenessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"2500m","memory":"2500Mi"},"requests":{"cpu":"2500m","memory":"2500Mi"}},"service":{"clusterIp":"None","name":"http-oxtrust","oxTrustServiceName":"oxtrust","port":8080},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Gluu Admin UI. This shouldn't be internet facing. |
        | oxtrust.dnsConfig | object | `{}` | Add custom dns config |
        | oxtrust.dnsPolicy | string | `""` | Add custom dns policy |
        | oxtrust.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | oxtrust.hpa.behavior | object | `{}` | Scaling Policies |
        | oxtrust.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | oxtrust.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxtrust.image.repository | string | `"gluufederation/oxtrust"` | Image  to use for deploying. |
        | oxtrust.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxtrust.livenessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for the auth server if needed. |
        | oxtrust.livenessProbe.exec | object | `{"command":["python3","/app/scripts/healthcheck.py"]}` | Executes the python3 healthcheck. https://github.com/GluuFederation/docker-oxauth/blob/4.3/scripts/healthcheck.py |
        | oxtrust.readinessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the auth server if needed. https://github.com/GluuFederation/docker-oxauth/blob/4.3/scripts/healthcheck.py |
        | oxtrust.replicas | int | `1` | Service replica number. |
        | oxtrust.resources | object | `{"limits":{"cpu":"2500m","memory":"2500Mi"},"requests":{"cpu":"2500m","memory":"2500Mi"}}` | Resource specs. |
        | oxtrust.resources.limits.cpu | string | `"2500m"` | CPU limit. |
        | oxtrust.resources.limits.memory | string | `"2500Mi"` | Memory limit. |
        | oxtrust.resources.requests.cpu | string | `"2500m"` | CPU request. |
        | oxtrust.resources.requests.memory | string | `"2500Mi"` | Memory request. |
        | oxtrust.service.name | string | `"http-oxtrust"` | The name of the oxtrust port within the oxtrust service. Please keep it as default. |
        | oxtrust.service.oxTrustServiceName | string | `"oxtrust"` | Name of the auth-server service. Please keep it as default. |
        | oxtrust.service.port | int | `8080` | Port of the oxtrust service. Please keep it as default. |
        | oxtrust.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxtrust.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxtrust.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxtrust.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxtrust.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "fido2"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | fido2 | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/fido2","tag":"4.3.0_b1"},"livenessProbe":{"httpGet":{"path":"/fido2/restv1/fido2/configuration","port":"http-fido2"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"readinessProbe":{"httpGet":{"path":"/fido2/restv1/fido2/configuration","port":"http-fido2"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"500m","memory":"500Mi"},"requests":{"cpu":"500m","memory":"500Mi"}},"service":{"fido2ServiceName":"fido2","name":"http-fido2","port":8080},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | FIDO 2.0 (FIDO2) is an open authentication standard that enables leveraging common devices to authenticate to online services in both mobile and desktop environments. |
        | fido2.dnsConfig | object | `{}` | Add custom dns config |
        | fido2.dnsPolicy | string | `""` | Add custom dns policy |
        | fido2.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | fido2.hpa.behavior | object | `{}` | Scaling Policies |
        | fido2.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | fido2.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | fido2.image.repository | string | `"gluufederation/fido2"` | Image  to use for deploying. |
        | fido2.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | fido2.livenessProbe | object | `{"httpGet":{"path":"/fido2/restv1/fido2/configuration","port":"http-fido2"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the liveness healthcheck for the fido2 if needed. |
        | fido2.livenessProbe.httpGet | object | `{"path":"/fido2/restv1/fido2/configuration","port":"http-fido2"}` | http liveness probe endpoint |
        | fido2.readinessProbe | object | `{"httpGet":{"path":"/fido2/restv1/fido2/configuration","port":"http-fido2"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the readiness healthcheck for the fido2 if needed. |
        | fido2.replicas | int | `1` | Service replica number. |
        | fido2.resources | object | `{"limits":{"cpu":"500m","memory":"500Mi"},"requests":{"cpu":"500m","memory":"500Mi"}}` | Resource specs. |
        | fido2.resources.limits.cpu | string | `"500m"` | CPU limit. |
        | fido2.resources.limits.memory | string | `"500Mi"` | Memory limit. |
        | fido2.resources.requests.cpu | string | `"500m"` | CPU request. |
        | fido2.resources.requests.memory | string | `"500Mi"` | Memory request. |
        | fido2.service.fido2ServiceName | string | `"fido2"` | Name of the fido2 service. Please keep it as default. |
        | fido2.service.name | string | `"http-fido2"` | The name of the fido2 port within the fido2 service. Please keep it as default. |
        | fido2.service.port | int | `8080` | Port of the fido2 service. Please keep it as default. |
        | fido2.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | fido2.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | fido2.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | fido2.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | fido2.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |


    === "scim"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | scim | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/scim","tag":"4.3.0_b1"},"livenessProbe":{"httpGet":{"path":"/scim/restv1/scim/v2/ServiceProviderConfig","port":8080},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"httpGet":{"path":"/scim/restv1/scim/v2/ServiceProviderConfig","port":8080},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"1000m","memory":"1000Mi"},"requests":{"cpu":"1000m","memory":"1000Mi"}},"service":{"name":"http-scim","port":8080,"scimServiceName":"scim"},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | System for Cross-domain Identity Management (SCIM) version 2.0 |
        | scim.dnsConfig | object | `{}` | Add custom dns config |
        | scim.dnsPolicy | string | `""` | Add custom dns policy |
        | scim.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | scim.hpa.behavior | object | `{}` | Scaling Policies |
        | scim.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | scim.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | scim.image.repository | string | `"gluufederation/scim"` | Image  to use for deploying. |
        | scim.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | scim.livenessProbe | object | `{"httpGet":{"path":"/scim/restv1/scim/v2/ServiceProviderConfig","port":8080},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for SCIM if needed. |
        | scim.livenessProbe.httpGet.path | string | `"/scim/restv1/scim/v2/ServiceProviderConfig"` | http liveness probe endpoint |
        | scim.readinessProbe | object | `{"httpGet":{"path":"/scim/restv1/scim/v2/ServiceProviderConfig","port":8080},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the SCIM if needed. |
        | scim.readinessProbe.httpGet.path | string | `"/scim/restv1/scim/v2/ServiceProviderConfig"` | http readiness probe endpoint |
        | scim.replicas | int | `1` | Service replica number. |
        | scim.resources.limits.cpu | string | `"1000m"` | CPU limit. |
        | scim.resources.limits.memory | string | `"1000Mi"` | Memory limit. |
        | scim.resources.requests.cpu | string | `"1000m"` | CPU request. |
        | scim.resources.requests.memory | string | `"1000Mi"` | Memory request. |
        | scim.service.name | string | `"http-scim"` | The name of the scim port within the scim service. Please keep it as default. |
        | scim.service.port | int | `8080` | Port of the scim service. Please keep it as default. |
        | scim.service.scimServiceName | string | `"scim"` | Name of the auth-server service. Please keep it as default. |
        | scim.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | scim.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | scim.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | scim.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | scim.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "oxd-server"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxd-server | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/oxd-server","tag":"4.3.0_b1"},"livenessProbe":{"exec":{"command":["curl","-k","https://localhost:8443/health-check"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"exec":{"command":["curl","-k","https://localhost:8443/health-check"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"1000m","memory":"400Mi"},"requests":{"cpu":"1000m","memory":"400Mi"}},"service":{"oxdServerServiceName":"oxd-server"},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Middleware API to help application developers call an OAuth, OpenID or UMA server. You may wonder why this is necessary. It makes it easier for client developers to use OpenID signing and encryption features, without becoming crypto experts. This API provides some high level endpoints to do some of the heavy lifting. |
        | oxd-server.dnsConfig | object | `{}` | Add custom dns config |
        | oxd-server.dnsPolicy | string | `""` | Add custom dns policy |
        | oxd-server.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | oxd-server.hpa.behavior | object | `{}` | Scaling Policies |
        | oxd-server.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | oxd-server.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxd-server.image.repository | string | `"gluufederation/oxd-server"` | Image  to use for deploying. |
        | oxd-server.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxd-server.livenessProbe | object | `{"exec":{"command":["curl","-k","https://localhost:8443/health-check"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for the auth server if needed. |
        | oxd-server.livenessProbe.exec | object | `{"command":["curl","-k","https://localhost:8443/health-check"]}` | Executes the python3 healthcheck. |
        | oxd-server.readinessProbe | object | `{"exec":{"command":["curl","-k","https://localhost:8443/health-check"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the auth server if needed. |
        | oxd-server.replicas | int | `1` | Service replica number. |
        | oxd-server.resources | object | `{"limits":{"cpu":"1000m","memory":"400Mi"},"requests":{"cpu":"1000m","memory":"400Mi"}}` | Resource specs. |
        | oxd-server.resources.limits.cpu | string | `"1000m"` | CPU limit. |
        | oxd-server.resources.limits.memory | string | `"400Mi"` | Memory limit. |
        | oxd-server.resources.requests.cpu | string | `"1000m"` | CPU request. |
        | oxd-server.resources.requests.memory | string | `"400Mi"` | Memory request. |
        | oxd-server.service.oxdServerServiceName | string | `"oxd-server"` | Name of the OXD server service. This must match config.configMap.gluuOxdApplicationCertCn. Please keep it as default. |
        | oxd-server.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxd-server.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxd-server.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxd-server.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxd-server.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "casa"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | casa | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/casa","tag":"4.3.0_b1"},"livenessProbe":{"httpGet":{"path":"/casa/health-check","port":"http-casa"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"readinessProbe":{"httpGet":{"path":"/casa/health-check","port":"http-casa"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"500m","memory":"500Mi"},"requests":{"cpu":"500m","memory":"500Mi"}},"service":{"casaServiceName":"casa","name":"http-casa","port":8080},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Gluu Casa ("Casa") is a self-service web portal for end-users to manage authentication and authorization preferences for their account in a Gluu Server. |
        | casa.dnsConfig | object | `{}` | Add custom dns config |
        | casa.dnsPolicy | string | `""` | Add custom dns policy |
        | casa.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | casa.hpa.behavior | object | `{}` | Scaling Policies |
        | casa.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | casa.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | casa.image.repository | string | `"gluufederation/casa"` | Image  to use for deploying. |
        | casa.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | casa.livenessProbe | object | `{"httpGet":{"path":"/casa/health-check","port":"http-casa"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the liveness healthcheck for casa if needed. |
        | casa.livenessProbe.httpGet.path | string | `"/casa/health-check"` | http liveness probe endpoint |
        | casa.readinessProbe | object | `{"httpGet":{"path":"/casa/health-check","port":"http-casa"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the readiness healthcheck for the casa if needed. |
        | casa.readinessProbe.httpGet.path | string | `"/casa/health-check"` | http readiness probe endpoint |
        | casa.replicas | int | `1` | Service replica number. |
        | casa.resources | object | `{"limits":{"cpu":"500m","memory":"500Mi"},"requests":{"cpu":"500m","memory":"500Mi"}}` | Resource specs. |
        | casa.resources.limits.cpu | string | `"500m"` | CPU limit. |
        | casa.resources.limits.memory | string | `"500Mi"` | Memory limit. |
        | casa.resources.requests.cpu | string | `"500m"` | CPU request. |
        | casa.resources.requests.memory | string | `"500Mi"` | Memory request. |
        | casa.service.casaServiceName | string | `"casa"` | Name of the casa service. Please keep it as default. |
        | casa.service.name | string | `"http-casa"` | The name of the casa port within the casa service. Please keep it as default. |
        | casa.service.port | int | `8080` | Port of the casa service. Please keep it as default. |
        | casa.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | casa.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | casa.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | casa.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | casa.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |


    === "oxpassport"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxpassport | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/oxpassport","tag":"4.3.0_b1"},"livenessProbe":{"failureThreshold":20,"httpGet":{"path":"/passport/health-check","port":"http-passport"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"failureThreshold":20,"httpGet":{"path":"/passport/health-check","port":"http-passport"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"700m","memory":"900Mi"},"requests":{"cpu":"700m","memory":"900Mi"}},"service":{"name":"http-passport","oxPassportServiceName":"oxpassport","port":8090},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Gluu interface to Passport.js to support social login and inbound identity. |
        | oxpassport.dnsConfig | object | `{}` | Add custom dns config |
        | oxpassport.dnsPolicy | string | `""` | Add custom dns policy |
        | oxpassport.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | oxpassport.hpa.behavior | object | `{}` | Scaling Policies |
        | oxpassport.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | oxpassport.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxpassport.image.repository | string | `"gluufederation/oxpassport"` | Image  to use for deploying. |
        | oxpassport.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxpassport.livenessProbe | object | `{"failureThreshold":20,"httpGet":{"path":"/passport/health-check","port":"http-passport"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for oxPassport if needed. |
        | oxpassport.livenessProbe.httpGet.path | string | `"/passport/health-check"` | http liveness probe endpoint |
        | oxpassport.readinessProbe | object | `{"failureThreshold":20,"httpGet":{"path":"/passport/health-check","port":"http-passport"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the oxPassport if needed. |
        | oxpassport.readinessProbe.httpGet.path | string | `"/passport/health-check"` | http readiness probe endpoint |
        | oxpassport.replicas | int | `1` | Service replica number |
        | oxpassport.resources | object | `{"limits":{"cpu":"700m","memory":"900Mi"},"requests":{"cpu":"700m","memory":"900Mi"}}` | Resource specs. |
        | oxpassport.resources.limits.cpu | string | `"700m"` | CPU limit. |
        | oxpassport.resources.limits.memory | string | `"900Mi"` | Memory limit. |
        | oxpassport.resources.requests.cpu | string | `"700m"` | CPU request. |
        | oxpassport.resources.requests.memory | string | `"900Mi"` | Memory request. |
        | oxpassport.service.name | string | `"http-passport"` | The name of the oxPassport port within the oxPassport service. Please keep it as default. |
        | oxpassport.service.oxPassportServiceName | string | `"oxpassport"` | Name of the oxPassport service. Please keep it as default. |
        | oxpassport.service.port | int | `8090` | Port of the oxPassport service. Please keep it as default. |
        | oxpassport.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxpassport.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxpassport.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxpassport.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxpassport.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "oxshibboleth"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxshibboleth | object | `{"dnsConfig":{},"dnsPolicy":"","hpa":{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50},"image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/oxshibboleth","tag":"4.3.0_b1"},"livenessProbe":{"httpGet":{"path":"/idp","port":"http-oxshib"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5},"readinessProbe":{"httpGet":{"path":"/idp","port":"http-oxshib"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5},"replicas":1,"resources":{"limits":{"cpu":"1000m","memory":"1000Mi"},"requests":{"cpu":"1000m","memory":"1000Mi"}},"service":{"name":"http-oxshib","oxShibbolethServiceName":"oxshibboleth","port":8080},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Shibboleth project for the Gluu Server's SAML IDP functionality. |
        | oxshibboleth.dnsConfig | object | `{}` | Add custom dns config |
        | oxshibboleth.dnsPolicy | string | `""` | Add custom dns policy |
        | oxshibboleth.hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
        | oxshibboleth.hpa.behavior | object | `{}` | Scaling Policies |
        | oxshibboleth.hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
        | oxshibboleth.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxshibboleth.image.repository | string | `"gluufederation/oxshibboleth"` | Image  to use for deploying. |
        | oxshibboleth.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxshibboleth.livenessProbe | object | `{"httpGet":{"path":"/idp","port":"http-oxshib"},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for the oxShibboleth if needed. |
        | oxshibboleth.livenessProbe.httpGet.path | string | `"/idp"` | http liveness probe endpoint |
        | oxshibboleth.readinessProbe | object | `{"httpGet":{"path":"/idp","port":"http-oxshib"},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the casa if needed. |
        | oxshibboleth.readinessProbe.httpGet.path | string | `"/idp"` | http liveness probe endpoint |
        | oxshibboleth.replicas | int | `1` | Service replica number. |
        | oxshibboleth.resources | object | `{"limits":{"cpu":"1000m","memory":"1000Mi"},"requests":{"cpu":"1000m","memory":"1000Mi"}}` | Resource specs. |
        | oxshibboleth.resources.limits.cpu | string | `"1000m"` | CPU limit. |
        | oxshibboleth.resources.limits.memory | string | `"1000Mi"` | Memory limit. |
        | oxshibboleth.resources.requests.cpu | string | `"1000m"` | CPU request. |
        | oxshibboleth.resources.requests.memory | string | `"1000Mi"` | Memory request. |
        | oxshibboleth.service.name | string | `"http-oxshib"` | Port of the oxShibboleth service. Please keep it as default. |
        | oxshibboleth.service.oxShibbolethServiceName | string | `"oxshibboleth"` | Name of the oxShibboleth service. Please keep it as default. |
        | oxshibboleth.service.port | int | `8080` | The name of the oxPassport port within the oxPassport service. Please keep it as default. |
        | oxshibboleth.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxshibboleth.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxshibboleth.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxshibboleth.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxshibboleth.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "cr-rotate"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | cr-rotate | object | `{"dnsConfig":{},"dnsPolicy":"","image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/cr-rotate","tag":"4.3.0_b1"},"resources":{"limits":{"cpu":"200m","memory":"200Mi"},"requests":{"cpu":"200m","memory":"200Mi"}},"service":{"crRotateServiceName":"cr-rotate","name":"http-cr-rotate","port":8084},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | CacheRefreshRotation is a special container to monitor cache refresh on oxTrust containers. This may be depreciated. |
        | cr-rotate.dnsConfig | object | `{}` | Add custom dns config |
        | cr-rotate.dnsPolicy | string | `""` | Add custom dns policy |
        | cr-rotate.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | cr-rotate.image.repository | string | `"gluufederation/cr-rotate"` | Image  to use for deploying. |
        | cr-rotate.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | cr-rotate.resources | object | `{"limits":{"cpu":"200m","memory":"200Mi"},"requests":{"cpu":"200m","memory":"200Mi"}}` | Resource specs. |
        | cr-rotate.resources.limits.cpu | string | `"200m"` | CPU limit. |
        | cr-rotate.resources.limits.memory | string | `"200Mi"` | Memory limit. |
        | cr-rotate.resources.requests.cpu | string | `"200m"` | CPU request. |
        | cr-rotate.resources.requests.memory | string | `"200Mi"` | Memory request. |
        | cr-rotate.service.crRotateServiceName | string | `"cr-rotate"` | Name of the cr-rotate service. Please keep it as default. |
        | cr-rotate.service.name | string | `"http-cr-rotate"` | The name of the cr-rotate port within the cr-rotate service. Please keep it as default. |
        | cr-rotate.service.port | int | `8084` | Port of the casa service. Please keep it as default. |
        | cr-rotate.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | cr-rotate.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | cr-rotate.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | cr-rotate.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | cr-rotate.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    === "oxauth-key-rotation"
    
        | Key | Type | Default | Description |
        |-----|------|---------|-------------|
        | oxauth-key-rotation | object | `{"dnsConfig":{},"dnsPolicy":"","image":{"pullPolicy":"IfNotPresent","repository":"gluufederation/certmanager","tag":"4.3.0_b1"},"keysLife":48,"resources":{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}},"usrEnvs":{"normal":{},"secret":{}},"volumeMounts":[],"volumes":[]}` | Responsible for regenerating auth-keys per x hours |
        | oxauth-key-rotation.dnsConfig | object | `{}` | Add custom dns config |
        | oxauth-key-rotation.dnsPolicy | string | `""` | Add custom dns policy |
        | oxauth-key-rotation.image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
        | oxauth-key-rotation.image.repository | string | `"gluufederation/certmanager"` | Image  to use for deploying. |
        | oxauth-key-rotation.image.tag | string | `"4.3.0_b1"` | Image  tag to use for deploying. |
        | oxauth-key-rotation.keysLife | int | `48` | Auth server key rotation keys life in hours |
        | oxauth-key-rotation.resources | object | `{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}}` | Resource specs. |
        | oxauth-key-rotation.resources.limits.cpu | string | `"300m"` | CPU limit. |
        | oxauth-key-rotation.resources.limits.memory | string | `"300Mi"` | Memory limit. |
        | oxauth-key-rotation.resources.requests.cpu | string | `"300m"` | CPU request. |
        | oxauth-key-rotation.resources.requests.memory | string | `"300Mi"` | Memory request. |
        | oxauth-key-rotation.usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
        | oxauth-key-rotation.usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
        | oxauth-key-rotation.usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
        | oxauth-key-rotation.volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
        | oxauth-key-rotation.volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |

    
    ### Instructions on how to install different services
    
    Enabling the following services automatically install the corresponding associated chart. To enable/disable them set `true` or `false` in the persistence configs as shown below.  
    
    ```yaml
    config:
      configmap:
        # Auto install other services. If enabled the respective service chart will be installed
        gluuPassportEnabled: false
        gluuCasaEnabled: false
        gluuRadiusEnabled: false
        gluuSamlEnabled: false
    ```
    
    ### Casa
    
    - Casa is dependant on `oxd-server`. To install it `oxd-server` must be enabled.
    
    ### Other optional services
    
    Other optional services like `key-rotation`, and `cr-rotation`, are enabled by setting their corresponding values to `true` under the global block.
    
    For example, to enable `cr-rotate` set
    
    ```yaml
    global:
      cr-rotate:
        enabled: true
    ```
    
=== "GUI-alpha"
    ## Install Gluu using the gui installer
    
    !!!warning
        The GUI installer is currently alpha. Please report any bugs found by opening an [issue](https://github.com/GluuFederation/cloud-native-edition/issues/new/choose).
        
    1.  Create the GUI installer job
    
        ```bash
        cat <<EOF | kubectl apply -f -
        apiVersion: batch/v1
        kind: Job
        metadata:
          name: cloud-native-installer
          labels:
            APP_NAME: cloud-native-installer
        spec:
          template:
            metadata:
              labels:
                APP_NAME: cloud-native-installer
            spec:
              restartPolicy: Never
              containers:
                - name: cloud-native-installer
                  image: gluufederation/cloud-native:4.3.0_dev
        ---
        kind: Service
        apiVersion: v1
        metadata:
          name: cloud-native-installer
        spec:
          type: LoadBalancer
          selector:
            app: cloud-native-installer
          ports:
            - name: http
              port: 80
              targetPort: 5000           
        EOF
        ```
    
    1.  Grab the Loadbalancer address , ip or Nodeport and follow installation setup.
    
        === "AWS"
        
            ```bash
            kubectl -n default get svc cloud-native-installer --output jsonpath='{.status.loadBalancer.ingress[0].hostname}'
            ```
            
        === "GKE"
        
            ```bash
            kubectl -n default get svc cloud-native-installer --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
            ```
            
        === "Azure"
        
            ```bash
            kubectl -n default get svc cloud-native-installer --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
            ```
            
        === "DigitalOcean"
        
            ```bash
            kubectl -n default get svc cloud-native-installer --output jsonpath='{.status.loadBalancer.ingress[0].ip}'
            ```
            
        === "Microk8s"
        
            1. Get ip of microk8s vm
            
            1. Get `NodePort` of the GUI installer service
            
               ```bash
               kubectl -n default get svc cloud-native-installer
               ```
            
        === "Minikube"
        
            1. Get ip of minikube vm
            
               ```bash
               minikube ip
               ```
            
            1. Get `NodePort` of the GUI installer service
            
               ```bash
               kubectl -n default get svc cloud-native-installer
               ```
                
    1. Head to the address from previous step to start the installation.

=== "Kustomize-depreciated"
    ## Install Gluu using `pygluu-kubernetes`
    
    1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](#build-pygluu-kubernetespyz-manually).

    1. **Optional:** If using couchbase as the persistence backend. Download the couchbase [kubernetes](https://www.couchbase.com/downloads) operator package for linux and place it in the same directory as `pygluu-kubernetes.pyz`
    
    
    1. Run :
    
        ```bash
        ./pygluu-kubernetes.pyz install
        ```
        
    !!!note
        Prompts will ask for the rest of the information needed. You may generate the manifests (yaml files) and continue to deployment or just generate the  manifests (yaml files) during the execution of `pygluu-kubernetes.pyz`. `pygluu-kubernetes.pyz` will output a file called `settings.json` holding all the parameters. More information about this file and the vars it holds is [below](#settingsjson-parameters-file-contents) but  please don't manually create this file as the script can generate it using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/cloud-native-edition/releases). 
    
    ### Uninstall

    1. Run :
    
        ```bash
        ./pygluu-kubernetes.pyz uninstall
        ```    

### `settings.json` parameters file contents

This is the main parameter file used with the [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases) cloud native edition installer.

!!!note
    Please generate this file using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/cloud-native-edition/releases).

| Parameter                                       | Description                                                                      | Options                                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `ACCEPT_GLUU_LICENSE`                           | Accept the [License](https://www.gluu.org/license/cloud-native-edition/)         | `"Y"` or `"N"`                                                                              |
| `TEST_ENVIRONMENT`                              | Allows installation with no resources limits and requests defined.               | `"Y"` or `"N"`                                                                              |
| `ADMIN_PW`                                      | Password of oxTrust 6 chars min: 1 capital, 1 small, 1 digit and 1 special char  | `"P@ssw0rd"`                                                                                |
| `GLUU_VERSION`                                  | Gluu version to be installed                                                     | `"4.2"`                                                                                     |
| `GLUU_UPGRADE_TARGET_VERSION`                   | Gluu upgrade version                                                             | `"4.2"`                                                                                     |
| `GLUU_HELM_RELEASE_NAME`                        | Gluu Helm release name                                                           | `"<name>"`                                                                                  |
| `KONG_HELM_RELEASE_NAME`                        | Gluu Gateway (Kong) Helm release name                                            | `"<name>"`                                                                                  |
| `NGINX_INGRESS_NAMESPACE`                       | Nginx namespace                                                                  | `"<name>"`                                                                                  |
| `NGINX_INGRESS_RELEASE_NAME`                    | Nginx Helm release name                                                          | `"<name>"`                                                                                  |
| `GLUU_GATEWAY_UI_HELM_RELEASE_NAME`             |  Gluu Gateway UI release name                                                    | `"<name>"`                                                                                  |
| `INSTALL_GLUU_GATEWAY`                          | Install Gluu Gateway Database mode                                               | `"Y"` or `"N"`                                                                              |
| `USE_ISTIO`                                     | Enable use of Istio. This will inject sidecars in Gluu pods.[Alpha]              | `"Y"` or `"N"`                                                                              |
| `USE_ISTIO_INGRESS`                             | Enable Istio ingress.[Alpha]                                                     | `"Y"` or `"N"`                                                                              |
| `ISTIO_SYSTEM_NAMESPACE`                        | Postgres namespace - Gluu Gateway [Alpha]                                        | `"<name>"`                                                                                  |
| `POSTGRES_NAMESPACE`                            | Postgres namespace - Gluu Gateway                                                | `"<name>"`                                                                                  |
| `KONG_NAMESPACE`                                | Kong namespace - Gluu Gateway                                                    | `"<name>"`                                                                                  |
| `GLUU_GATEWAY_UI_NAMESPACE`                     | Gluu Gateway UI namespace - Gluu Gateway                                         | `"<name>"`                                                                                  |
| `KONG_PG_USER`                                  | Kong Postgres user - Gluu Gateway                                                | `"<name>"`                                                                                  |
| `KONG_PG_PASSWORD`                              | Kong Postgres password - Gluu Gateway                                            | `"<name>"`                                                                                  |
| `GLUU_GATEWAY_UI_PG_USER`                       | Gluu Gateway UI Postgres user - Gluu Gateway                                     | `"<name>"`                                                                                  |
| `GLUU_GATEWAY_UI_PG_PASSWORD`                   | Gluu Gateway UI Postgres password - Gluu Gateway                                 | `"<name>"`                                                                                  |
| `KONG_DATABASE`                                 | Kong Postgres Database name - Gluu Gateway                                       | `"<name>"`                                                                                  |
| `GLUU_GATEWAY_UI_DATABASE`                      | Gluu Gateway UI Postgres Database name - Gluu Gateway                            | `"<name>"`                                                                                  |
| `POSTGRES_REPLICAS`                             | Postgres number of replicas - Gluu Gateway                                       | `"<name>"`                                                                                  |
| `POSTGRES_URL`                                  | Postgres URL ( Can be local or remote) - Gluu Gateway                            |  i.e `"<servicename>.<namespace>.svc.cluster.local"`                                        |
| `NODES_IPS`                                     | List of kubernetes cluster node ips                                              | `["<ip>", "<ip2>", "<ip3>"]`                                                                |
| `NODES_ZONES`                                   | List of kubernetes cluster node zones                                            | `["<node1_zone>", "<node2_zone>", "<node3_zone>"]`                                          |
| `NODES_NAMES`                                   | List of kubernetes cluster node names                                            | `["<node1_name>", "<node2_name>", "<node3_name>"]`                                          |
| `NODE_SSH_KEY`                                  | nodes ssh key path location                                                      | `"<pathtosshkey>"`                                                                          |
| `HOST_EXT_IP`                                   | Minikube or Microk8s vm ip                                                       | `"<ip>"`                                                                                    |
| `VERIFY_EXT_IP`                                 | Verify the Minikube or Microk8s vm ip placed                                     | `"Y"` or `"N"`                                                                              |
| `AWS_LB_TYPE`                                   | AWS loadbalancer type                                                            | `""` , `"clb"` or `"nlb"`                                                                   |
| `USE_ARN`                                       | Use ssl provided from ACM AWS                                                    | `""`, `"Y"` or `"N"`                                                                        |
| `VPC_CIDR`                                      | VPC CIDR in use for the Kubernetes cluster                                       | `""`, i.e `192.168.1.116`                                                                   |
| `ARN_AWS_IAM`                                   | The arn string                                                                   | `""` or `"<arn:aws:acm:us-west-2:XXXXXXXX:certificate/XXXXXX-XXXXXXX-XXXXXXX-XXXXXXXX>"`    |
| `LB_ADD`                                        | AWS loadbalancer address                                                         | `"<loadbalancer_address>"`                                                                  |
| `DEPLOYMENT_ARCH`                               | Deployment architecture                                                          | `"microk8s"`, `"minikube"`, `"eks"`, `"gke"`, `"aks"`, `"do"` or `"local"`                  |
| `PERSISTENCE_BACKEND`                           | Backend persistence type                                                         | `"ldap"`, `"couchbase"` or `"hybrid"`                                                       |
| `REDIS_URL`                                     | Redis url with port. Used when Redis is deployed for Cache.                      | i.e `"redis:6379"`, `"clustercfg.testing-redis.icrbdv.euc1.cache.amazonaws.com:6379"`       |
| `REDIS_TYPE`                                    | Type of Redis deployed                                                           | `"SHARDED"`, `"STANDALONE"`, `"CLUSTER"`, or `"SENTINEL"`                                   |
| `REDIS_PW`                                      | Redis Password if used. This may be empty. If not choose a long password.        | i.e `""`, `"LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURUakNDQWphZ0F3SUJBZ0lVV2Y0TExEb"`     |
| `REDIS_USE_SSL`                                 | Redis SSL use                                                                    |  `"false"` or `"true"`                                                                      |
| `REDIS_SSL_TRUSTSTORE`                          | Redis SSL truststore. If using cloud provider services this is left empty.       | i.e `""`, `"/etc/myredis.pem"`                                                              |
| `REDIS_SENTINEL_GROUP`                          | Redis Sentinel group                                                             | i.e `""`                                                                                    |
| `REDIS_MASTER_NODES`                            | Number of Redis master node if Redis is to be installed                          | i.e `3`                                                                                     |
| `REDIS_NODES_PER_MASTER`                        | Number of nodes per Redis master node if Redis is to be installed                | i.e `2`                                                                                     |
| `REDIS_NAMESPACE`                               | Redis Namespace if Redis is to be installed                                      | i.e `"gluu-redis-cluster"`                                                                  |
| `INSTALL_REDIS`                                 | Install Redis                                                                    | `"Y"` or `"N"`                                                                              |
| `INSTALL_COUCHBASE`                             | Install couchbase                                                                | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_NAMESPACE`                           | Couchbase namespace                                                              | `"<name>"`                                                                                  |
| `COUCHBASE_VOLUME_TYPE`                         | Persistence Volume type                                                          | `"io1"`,`"ps-ssd"`, `"Premium_LRS"`                                                         |
| `COUCHBASE_CLUSTER_NAME`                        | Couchbase cluster name                                                           | `"<name>"`                                                                                  |
| `COUCHBASE_URL`                                 | Couchbase internal address to the cluster                                        | `""` or i.e `"<clustername>.<namespace>.svc.cluster.local"`                                 |
| `COUCHBASE_USER`                                | Couchbase username                                                               | `""` or i.e `"gluu"`                                                                        |
| `COUCHBASE_BUCKET_PREFIX`                       | Prefix for Couchbase buckets                                                     | `gluu`                                                                                      |
| `COUCHBASE_PASSWORD`                            | Password of CB 6 chars min: 1 capital, 1 small, 1 digit and 1 special char       | `"P@ssw0rd"`                                                                                |
| `COUCHBASE_SUPERUSER`                           | Couchbase superuser username                                                     | `""` or i.e `"admin"`                                                                       |
| `COUCHBASE_SUPERUSER_PASSWORD`                  | Password of CB 6 chars min: 1 capital, 1 small, 1 digit and 1 special char       | `"P@ssw0rd"`                                                                                |
| `COUCHBASE_CRT`                                 | Couchbase CA certification                                                       | `""` or i.e `<crt content not encoded>`                                                     |
| `COUCHBASE_CN`                                  | Couchbase certificate common name                                                | `""`                                                                                        |
| `COUCHBASE_INDEX_NUM_REPLICA`                   | Couchbase number of replicas per index                                           | `0`                                                                                         |
| `COUCHBASE_SUBJECT_ALT_NAME`                    | Couchbase SAN                                                                    | `""` or i.e `"cb.gluu.org"`                                                                 |
| `COUCHBASE_CLUSTER_FILE_OVERRIDE`               | Override `couchbase-cluster.yaml` with a custom `couchbase-cluster.yaml`         | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_USE_LOW_RESOURCES`                   | Use very low resources for Couchbase deployment. For demo purposes               | `"Y"` or `"N"`                                                                              |
| `COUCHBASE_DATA_NODES`                          | Number of Couchbase data nodes                                                   | `""` or i.e `"4"`                                                                           |
| `COUCHBASE_QUERY_NODES`                         | Number of Couchbase query nodes                                                  | `""` or i.e `"3"`                                                                           |
| `COUCHBASE_INDEX_NODES`                         | Number of Couchbase index nodes                                                  | `""` or i.e `"3"`                                                                           | 
| `COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES`     | Number of Couchbase search, eventing and analytics nodes                         | `""` or i.e `"2"`                                                                           |
| `COUCHBASE_GENERAL_STORAGE`                     | Couchbase general storage size                                                   | `""` or i.e `"2"`                                                                           |
| `COUCHBASE_DATA_STORAGE`                        | Couchbase data storage size                                                      | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_INDEX_STORAGE`                       | Couchbase index storage size                                                     | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_QUERY_STORAGE`                       | Couchbase query storage size                                                     | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_ANALYTICS_STORAGE`                   | Couchbase search, eventing and analytics storage size                            | `""` or i.e `"5Gi"`                                                                         |
| `COUCHBASE_INCR_BACKUP_SCHEDULE`                | Couchbase incremental backup schedule                                            |  i.e `"*/30 * * * *"`                                                                       |
| `COUCHBASE_FULL_BACKUP_SCHEDULE`                | Couchbase  full backup  schedule                                                 |  i.e `"0 2 * * 6"`                                                                          |
| `COUCHBASE_BACKUP_RETENTION_TIME`               | Couchbase time to retain backups in s,m or h                                     |  i.e `"168h`                                                                                |
| `COUCHBASE_BACKUP_STORAGE_SIZE`                 | Couchbase backup storage size                                                    | i.e `"20Gi"`                                                                                |
| `NUMBER_OF_EXPECTED_USERS`                      | Number of expected users [couchbase-resource-calc-alpha]                         | `""` or i.e `"1000000"`                                                                     |
| `EXPECTED_TRANSACTIONS_PER_SEC`                 | Expected transactions per second [couchbase-resource-calc-alpha]                 | `""` or i.e `"2000"`                                                                        |
| `USING_CODE_FLOW`                               | If using code flow [couchbase-resource-calc-alpha]                               | `""`, `"Y"` or `"N"`                                                                        |
| `USING_SCIM_FLOW`                               | If using SCIM flow [couchbase-resource-calc-alpha]                               | `""`, `"Y"` or `"N"`                                                                        |
| `USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW` | If using password flow [couchbase-resource-calc-alpha]                           | `""`, `"Y"` or `"N"`                                                                        |
| `DEPLOY_MULTI_CLUSTER`                          | Deploying a Multi-cluster [alpha]                                                | `"Y"` or `"N"`                                                                              |
| `HYBRID_LDAP_HELD_DATA`                         | Type of data to be held in LDAP with a hybrid installation of couchbase and LDAP | `""`, `"default"`, `"user"`, `"site"`, `"cache"` or `"token"`                               |
| `LDAP_JACKRABBIT_VOLUME`                        | LDAP/Jackrabbit Volume type                                                      | `""`, `"io1"`,`"ps-ssd"`, `"Premium_LRS"`                                                   |
| `APP_VOLUME_TYPE`                               | Volume type for LDAP persistence                                                 | [options](#app_volume_type-options)                                                         |
| `INSTALL_JACKRABBIT`                            | Install Jackrabbit                                                               | `"Y"` or `"N"`                                                                              |
| `JACKRABBIT_STORAGE_SIZE`                       | Jackrabbit volume storage size                                                   | `""` i.e `"4Gi"`                                                                            |
| `JACKRABBIT_URL`                                | http:// url for Jackrabbit                                                       | i.e `"http://jackrabbit:8080"`                                                              |
| `JACKRABBIT_ADMIN_ID`                           | Jackrabbit admin ID                                                              | i.e `"admin"`                                                                               |
| `JACKRABBIT_ADMIN_PASSWORD`                     | Jackrabbit admin password                                                        | i.e `"admin"`                                                                           |
| `JACKRABBIT_CLUSTER`                            | Jackrabbit Cluster mode                                                          | `"N"` or `"Y"`                                                                              |
| `JACKRABBIT_PG_USER`                            | Jackrabbit postgres username                                                     | i.e `"jackrabbit"`                                                                          |
| `JACKRABBIT_PG_PASSWORD`                        | Jackrabbit postgres password                                                     | i.e `"jackrabbbit"`                                                                         |
| `JACKRABBIT_DATABASE`                           | Jackrabbit postgres database name                                                | i.e `"jackrabbit"`                                                                          |
| `LDAP_STATIC_VOLUME_ID`                         | LDAP static volume id (AWS EKS)                                                  | `""` or `"<static-volume-id>"`                                                              |
| `LDAP_STATIC_DISK_URI`                          | LDAP static disk uri (GCE GKE or Azure)                                          | `""` or `"<disk-uri>"`                                                                      |
| `LDAP_BACKUP_SCHEDULE`                          | LDAP back up cron job frequency                                                  |  i.e `"*/30 * * * *"`                                                                       |
| `GLUU_CACHE_TYPE`                               | Cache type to be used                                                            | `"IN_MEMORY"`, `"REDIS"` or `"NATIVE_PERSISTENCE"`                                          |
| `GLUU_NAMESPACE`                                | Namespace to deploy Gluu in                                                      | `"<name>"`                                                                                  |
| `GLUU_FQDN`                                     | Gluu FQDN                                                                        | `"<FQDN>"` i.e `"demoexample.gluu.org"`                                                     |
| `COUNTRY_CODE`                                  | Gluu country code                                                                | `"<country code>"` i.e `"US"`                                                               |
| `STATE`                                         | Gluu state                                                                       | `"<state>"` i.e `"TX"`                                                                      |
| `EMAIL`                                         | Gluu email                                                                       | `"<email>"` i.e `"support@gluu.org"`                                                        |
| `CITY`                                          | Gluu city                                                                        | `"<city>"` i.e `"Austin"`                                                                   |
| `ORG_NAME`                                      | Gluu organization name                                                           | `"<org-name>"` i.e `"Gluu"`                                                                 |
| `LDAP_PW`                                       | Password of LDAP 6 chars min: 1 capital, 1 small, 1 digit and 1 special char     | `"P@ssw0rd"`                                                                                |
| `GMAIL_ACCOUNT`                                 | Gmail account for GKE installation                                               | `""` or`"<gmail>"` i.e                                                                      |
| `GOOGLE_NODE_HOME_DIR`                          | User node home directory, used if the hosts volume is used                       | `"Y"` or `"N"`                                                                              |
| `IS_GLUU_FQDN_REGISTERED`                       | Is Gluu FQDN globally resolvable                                                 | `"Y"` or `"N"`                                                                              |
| `OXD_APPLICATION_KEYSTORE_CN`                   | OXD application keystore common name                                             | `"<name>"` i.e `"oxd_server"`                                                               |
| `OXD_ADMIN_KEYSTORE_CN`                         | OXD admin keystore common name                                                   | `"<name>"` i.e `"oxd_server"`                                                               |
| `LDAP_STORAGE_SIZE`                             | LDAP volume storage size                                                         | `""` i.e `"4Gi"`                                                                            |
| `OXAUTH_KEYS_LIFE`                              | oxAuth Key life span in hours                                                    | `48`                                                               |
| `FIDO2_REPLICAS`                                | Number of FIDO2 replicas                                                         | min `"1"`                                                                                   |
| `SCIM_REPLICAS`                                 | Number of SCIM replicas                                                          | min `"1"`                                                                                   |
| `OXAUTH_REPLICAS`                               | Number of oxAuth replicas                                                        | min `"1"`                                                                                   |
| `OXTRUST_REPLICAS`                              | Number of oxTrust replicas                                                       | min `"1"`                                                                                   |
| `LDAP_REPLICAS`                                 | Number of LDAP replicas                                                          | min `"1"`                                                                                   |
| `OXSHIBBOLETH_REPLICAS`                         | Number of oxShibboleth replicas                                                  | min `"1"`                                                                                   |
| `OXPASSPORT_REPLICAS`                           | Number of oxPassport replicas                                                    | min `"1"`                                                                                   |
| `OXD_SERVER_REPLICAS`                           | Number of oxdServer replicas                                                     | min `"1"`                                                                                   |
| `CASA_REPLICAS`                                 | Number of Casa replicas                                                          | min `"1"`                                                                                   |
| `RADIUS_REPLICAS`                               | Number of Radius replica                                                         | min `"1"`                                                                                   |
| `ENABLE_OXTRUST_API`                            | Enable oxTrust-api                                                               | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXTRUST_TEST_MODE`                      | Enable oxTrust Test Mode                                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_CACHE_REFRESH`                          | Enable cache refresh rotate installation                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXD`                                    | Enable oxd server installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_RADIUS`                                 | Enable Radius installation                                                       | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXPASSPORT`                             | Enable oxPassport installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXSHIBBOLETH`                           | Enable oxShibboleth installation                                                 | `"Y"` or `"N"`                                                                              |
| `ENABLE_CASA`                                   | Enable Casa installation                                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_FIDO2`                                  | Enable Fido2 installation                                                        | `"Y"` or `"N"`                                                                              |
| `ENABLE_SCIM`                                   | Enable SCIM installation                                                         | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXAUTH_KEY_ROTATE`                      | Enable key rotate installation                                                   | `"Y"` or `"N"`                                                                              |
| `ENABLE_OXTRUST_API_BOOLEAN`                    | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_OXTRUST_TEST_MODE_BOOLEAN`              | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_RADIUS_BOOLEAN`                         | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_OXPASSPORT_BOOLEAN`                     | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_CASA_BOOLEAN`                           | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLE_SAML_BOOLEAN`                           | Used by `pygluu-kubernetes`                                                      | `"false"`                                                                                   |
| `ENABLED_SERVICES_LIST`                         | Used by `pygluu-kubernetes`. List of all enabled services                        | `"[]"`                                                                                   |
| `EDIT_IMAGE_NAMES_TAGS`                         | Manually place the image source and tag                                          | `"Y"` or `"N"`                                                                              |
| `JACKRABBIT_IMAGE_NAME`                         | Jackrabbit image repository name                                                 | i.e `"gluufederation/jackrabbit"`                                                           |
| `JACKRABBIT_IMAGE_TAG`                          | Jackrabbit image tag                                                             | i.e `"4.3.0_02"`                                                                            |
| `CASA_IMAGE_NAME`                               | Casa image repository name                                                       | i.e `"gluufederation/casa"`                                                                 |
| `CASA_IMAGE_TAG`                                | Casa image tag                                                                   | i.e `"4.3.0_02"`                                                                            |
| `CONFIG_IMAGE_NAME`                             | Config image repository name                                                     | i.e `"gluufederation/config-init"`                                                          |
| `CONFIG_IMAGE_TAG`                              | Config image tag                                                                 | i.e `"4.3.0_02"`                                                                            |
| `CACHE_REFRESH_ROTATE_IMAGE_NAME`               | Cache refresh image repository name                                              | i.e `"gluufederation/cr-rotate"`                                                            |
| `CACHE_REFRESH_ROTATE_IMAGE_TAG`                | Cache refresh  image tag                                                         | i.e `"4.3.0_02"`                                                                            |
| `CERT_MANAGER_IMAGE_NAME`                       | Gluus Certificate management image repository name                               | i.e `"gluufederation/certmanager"`                                                          |
| `CERT_MANAGER_IMAGE_TAG`                        | Gluus Certificate management image tag                                           | i.e `"4.3.0_02"`                                                                            |
| `LDAP_IMAGE_NAME`                               | LDAP image repository name                                                       | i.e `"gluufederation/opendj"`                                                               |
| `LDAP_IMAGE_TAG`                                | LDAP image tag                                                                   | i.e `"4.3.0_02"`                                                                            |
| `OXAUTH_IMAGE_NAME`                             | oxAuth image repository name                                                     | i.e `"gluufederation/oxauth"`                                                               |
| `OXAUTH_IMAGE_TAG`                              | oxAuth image tag                                                                 | i.e `"4.3.0_03"`                                                                            |
| `OXD_IMAGE_NAME`                                | oxd image repository name                                                        | i.e `"gluufederation/oxd-server"`                                                           |
| `OXD_IMAGE_TAG`                                 | oxd image tag                                                                    | i.e `"4.3.0_02"`                                                                            |
| `OXPASSPORT_IMAGE_NAME`                         | oxPassport image repository name                                                 | i.e `"gluufederation/oxpassport"`                                                           |
| `OXPASSPORT_IMAGE_TAG`                          | oxPassport image tag                                                             | i.e `"4.3.0_02"`                                                                            |
| `FIDO2_IMAGE_NAME`                              | FIDO2 image repository name                                                      | i.e `"gluufederation/oxpassport"`                                                           |
| `FIDO2_IMAGE_TAG`                               | FIDO2 image tag                                                                  | i.e `"4.3.0_02"`                                                                            |
| `SCIM_IMAGE_NAME`                               | SCIM image repository name                                                       | i.e `"gluufederation/oxpassport"`                                                           |
| `SCIM_IMAGE_TAG`                                | SCIM image tag                                                                   | i.e `"4.3.0_02"`                                                                            |
| `OXSHIBBOLETH_IMAGE_NAME`                       | oxShibboleth image repository name                                               | i.e `"gluufederation/oxshibboleth"`                                                         |
| `OXSHIBBOLETH_IMAGE_TAG`                        | oxShibboleth image tag                                                           | i.e `"4.3.0_02"`                                                                            |
| `OXTRUST_IMAGE_NAME`                            | oxTrust image repository name                                                    | i.e `"gluufederation/oxtrust"`                                                              |
| `OXTRUST_IMAGE_TAG`                             | oxTrust image tag                                                                | i.e `"4.3.0_02"`                                                                            |
| `PERSISTENCE_IMAGE_NAME`                        | Persistence image repository name                                                | i.e `"gluufederation/persistence"`                                                          |
| `PERSISTENCE_IMAGE_TAG`                         | Persistence image tag                                                            | i.e `"4.3.0_02"`                                                                            |
| `GLUU_GATEWAY_IMAGE_NAME`                       | Gluu Gateway image repository name                                               | i.e `"gluufederation/gluu-gateway"`                                                         |
| `GLUU_GATEWAY_IMAGE_TAG`                        | Gluu Gateway image tag                                                           | i.e `"4.3.0_01"`                                                                            |
| `GLUU_GATEWAY_UI_IMAGE_NAME`                    | Gluu Gateway UI image repository name                                            | i.e `"gluufederation/gluu-gateway-ui"`                                                      |
| `GLUU_GATEWAY_UI_IMAGE_TAG`                     | Gluu Gateway UI image tag                                                        | i.e `"4.3.0_01"`                                                                            |
| `UPGRADE_IMAGE_NAME`                            | Gluu upgrade image repository name                                               | i.e `"gluufederation/upgrade"`                                                              |
| `UPGRADE_IMAGE_TAG`                             | Gluu upgrade image tag                                                           | i.e `"4.3.0_02"`                                                                            |
| `CONFIRM_PARAMS`                                | Confirm using above options                                                      | `"Y"` or `"N"`                                                                              |
| `GLUU_LDAP_MULTI_CLUSTER`                       | HELM-ALPHA-FEATURE: Enable LDAP multi cluster environment                        |`"Y"` or `"N"`                                                                               |
| `GLUU_LDAP_SERF_PORT`                           | HELM-ALPHA-FEATURE: Serf UDP and TCP port                                        | i.e `30946`                                                                                 |
| `GLUU_LDAP_ADVERTISE_ADDRESS`                   | HELM-ALPHA-FEATURE: LDAP pod advertise address                                   | i.e `demoexample.gluu.org:30946"`                                                           |
| `GLUU_LDAP_ADVERTISE_ADMIN_PORT`                | HELM-ALPHA-FEATURE: LDAP serf advertise admin port                               | i.e `30444`                                                                                 |
| `GLUU_LDAP_ADVERTISE_LDAPS_PORT`                | HELM-ALPHA-FEATURE: LDAP serf advertise LDAPS port                               | i.e `30636`                                                                                 |
| `GLUU_LDAP_ADVERTISE_REPLICATION_PORT`          | HELM-ALPHA-FEATURE: LDAP serf advertise replication port                         | i.e `30989`                                                                                 |
| `GLUU_LDAP_SECONDARY_CLUSTER`                   | HELM-ALPHA-FEATURE: Is this the first kubernetes cluster or not                  | `"Y"` or `"N"`                                                                              |
| `GLUU_LDAP_SERF_PEERS`                          | HELM-ALPHA-FEATURE: All opendj serf advertised addresses. This must be resolvable | `["firstldap.gluu.org:30946", "secondldap.gluu.org:31946"]` |

### `APP_VOLUME_TYPE`-options

`APP_VOLUME_TYPE=""` but if `PERSISTENCE_BACKEND` is `OpenDJ` options are :

| Options  | Deployemnt Architecture  | Volume Type                                   |
| -------- | ------------------------ | --------------------------------------------- |
| `1`      | Microk8s                 | volumes on host                          |
| `2`      | Minikube                 | volumes on host                          |
| `6`      | EKS                      | volumes on host                          |
| `7`      | EKS                      | EBS volumes dynamically provisioned      |
| `8`      | EKS                      | EBS volumes statically provisioned       |
| `11`     | GKE                      | volumes on host                          |
| `12`     | GKE                      | Persistent Disk  dynamically provisioned |
| `13`     | GKE                      | Persistent Disk  statically provisioned  |
| `16`     | Azure                    | volumes on host                          |
| `17`     | Azure                    | Persistent Disk  dynamically provisioned |
| `18`     | Azure                    | Persistent Disk  statically provisioned  |
| `21`     | Digital Ocean            | volumes on host                          |
| `22`     | Digital Ocean            | Persistent Disk  dynamically provisioned |
| `23`     | Digital Ocean            | Persistent Disk  statically provisioned  |
    

## Use Couchbase solely as the persistence layer

### Requirements
  - If you are installing on microk8s or minikube please ignore the below notes as a low resource `couchbase-cluster.yaml` will be applied automatically, however the VM being used must at least have 8GB RAM and 2 cpu available .
  
  - An `m5.xlarge` EKS cluster with 3 nodes at the minimum or `n2-standard-4` GKE cluster with 3 nodes. We advice contacting Gluu regarding production setups.

- [Install couchbase Operator](https://www.couchbase.com/downloads) linux version `2.1.0` is recommended but version `2.0.3` is also supported. Place the tar.gz file inside the same directory as the `pygluu-kubernetes.pyz`.

- A modified `couchbase/couchbase-cluster.yaml` will be generated but in production it is likely that this file will be modified.
  * To override the `couchbase-cluster.yaml` place the file inside `/couchbase` folder after running `./pygluu-kubernetes.pyz`. More information on the properties [couchbase-cluster.yaml](https://docs.couchbase.com/operator/1.2/couchbase-cluster-config.html).

!!!note
    Please note the `couchbase/couchbase-cluster.yaml` file must include at least three defined `spec.servers` with the labels `couchbase_services: index`, `couchbase_services: data` and `couchbase_services: analytics`

**If you wish to get started fast just change the values of `spec.servers.name` and `spec.servers.serverGroups` inside `couchbase/couchbase-cluster.yaml` to the zones of your EKS nodes and continue.**

- Run `./pygluu-kubernetes.pyz install-couchbase` and follow the prompts to install couchbase solely with Gluu.


## Use remote Couchbase as the persistence layer

- [Install couchbase](https://docs.couchbase.com/server/current/install/install-intro.html)

- Obtain the Public DNS or FQDN of the couchbase node.

- Head to the FQDN of the couchbase node to [setup](https://docs.couchbase.com/server/current/manage/manage-nodes/create-cluster.html) your couchbase cluster. When setting up please use the FQDN as the hostname of the new cluster.

- Couchbase URL base , user, and password will be needed for installation when running `pygluu-kubernetes.pyz`


### How to expand EBS volumes

1. Make sure the `StorageClass` used in your deployment has the `allowVolumeExpansion` set to true. If you have used our EBS volume deployment strategy then you will find that this property has already been set for you.

1. Edit your persistent volume claim using `kubectl edit pvc <claim-name> -n <namespace> ` and increase the value found for `storage:` to the value needed. Make sure the volumes expand by checking the `kubectl get pvc <claim-name> -n <namespace> `.

1. Restart the associated services


### Scaling pods

!!!note
    When using Mircok8s substitute  `kubectl` with `microk8s.kubectl` in the below commands.

To scale pods, run the following command:

```
kubectl scale --replicas=<number> <resource> <name>
```

In this case, `<resource>` could be Deployment or Statefulset and `<name>` is the resource name.

Examples:

-   Scaling oxAuth:

    ```
    kubectl scale --replicas=2 deployment oxauth
    ```

-   Scaling oxTrust:

    ```
    kubectl scale --replicas=2 statefulset oxtrust
    ```
    
### Working with Jackrabbit

| Services         | Folder  / File                      |  Jackrabbit Repository                                  | Method                 |
| ---------------- | ----------------------------------- | ------------------------------------------------------- | ---------------------- |
| `oxAuth`         | `/opt/gluu/jetty/oxauth/custom`     | `/repository/default/opt/gluu/jetty/oxauth/custom`      | `PULL` from Jackrabbit |
| `oxTrust`        | `/opt/gluu/jetty/identity/custom`   |  `/repository/default/opt/gluu/jetty/identity/custom`   | `PULL` from Jackrabbit |
| `Casa`           | `/opt/gluu/jetty/casa`              | `/repository/default/opt/gluu/jetty/casa`               | `PULL` from Jackrabbit |

The above means that Jackrabbit will maintain the source folder on all replicas of a service. If one pushed a custom file to `/opt/gluu/jetty/oxauth/custom` at one replica all other replicas would have this file.

#### oxTrust --> Jackrabbit --> oxShibboleth

| Services         | Folder  / File                      |  Jackrabbit Repository                                  | Method                 |
| ---------------- | ----------------------------------- | ------------------------------------------------------- | ---------------------- |
| `oxTrust`        | `/opt/shibboleth-idp`               |  `/repository/default/opt/shibboleth-idp`               | `PUSH` to Jackrabbit   |
| `oxShibboleth`   | `/opt/shibboleth-idp`               | `/repository/default/opt/shibboleth-idp`                | `PULL` from Jackrabbit |

#### oxAuth --> Jackrabbit --> Casa

| Services         | Folder  / File                      |  Jackrabbit Repository                                  | Method                 |
| ---------------- | ----------------------------------- | ------------------------------------------------------- | ---------------------- |
| `oxAuth `        | `/etc/certs/otp_configuration.json` |  `/repository/etc/certs/otp_configuration.json`         | `PUSH` to Jackrabbit   |
| `oxAuth `        | `/etc/certs/super_gluu_creds.json`  |  `/repository/default/etc/certs/super_gluu_creds.json`  | `PUSH` to Jackrabbit   |
| `Casa`           | `/etc/certs/otp_configuration.json` | `/repository/etc/certs/otp_configuration.json`          | `PULL` from Jackrabbit |
| `Casa`           | `/etc/certs/super_gluu_creds.json`  | `/repository/default/etc/certs/super_gluu_creds.json`   | `PULL` from Jackrabbit |

![svg](../img/kubernetes/cn-jackrabbit.svg)

=== "File managers"

    !!!note
        You can use any client to connect to Jackrabbit. We assume Gluu is installed in `gluu` namespace

    1. Port forward Jackrabbit at `localhost` on port `8080`
    
        ```bash
            kubectl port-forward jackrabbit-0 --namespace gluu 8080:8080
        ```
    
    
    1. Optional: If your managing VM is in the cloud you must forward the connection to the mac, linux or windows computer you are working from.
    
        ```bash
            ssh -i <key.pem> -L 8080:localhost:8080 user-of-managing-vm@ip-of-managing-vm
        ```
        
    1. Use any filemanager to connect to Jackrabbit. Here are some examples:
    
        === "Linux"
        
            Open file manager which maybe `Nautilus` and find `Connect to Server` place the address which should be `http://localhost:8080`. By default the username and password are `admin` if not changed in `etc/gluu/conf/jca_password`.
        
        === "Windows"
        
            Open  `My PC` and inside the address that might read your `C` drive place the address which should be `http://localhost:8080`. By default the username and password are `admin` if not changed in `etc/gluu/conf/jca_password`.
            
        === "Mac"
        
            Open `Finder` , `Go` then `Connect to Server` and place the address which should be `http://localhost:8080`. By default the username and password are `admin` if not changed in `etc/gluu/conf/jca_password`. 
        
=== "Script"

    !!!warning
        Used for quick testing with Jackrabbit and should be avoided. 

    1. Copy files to Jackrabbit container at `/opt/webdav`
    
    1. Run `python3 /app/scripts/jca_sync.py` .


## Build pygluu-kubernetes installer

### Overview
[`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases) is periodically released and does not need to be built manually. However, the process of building the installer package is listed [below](#build-pygluu-kubernetespyz-manually).

### Build `pygluu-kubernetes.pyz` manually

### Prerequisites

1.  Python 3.6+.
1.  Python `pip3` package.

### Installation

#### Standard Python package

1.  Create virtual environment and activate:

    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

1.  Install the package:

    ```
    make install
    ```

    This command will install executable called `pygluu-kubernetes` available in virtual environment `PATH`.

#### Python zipapp

1.  Install [shiv](https://shiv.readthedocs.io/) using `pip3`:

    ```sh
    pip3 install shiv
    ```

1.  Install the package:

    ```sh
    make zipapp
    ```

    This command will generate executable called `pygluu-kubernetes.pyz` under the same directory.

## Architectural diagram of all Gluu services

![svg](../img/kubernetes/cn-general-arch-diagram.svg)

## Architectural diagram of oxPassport

![svg](../img/kubernetes/cn-oxpassport.svg)

## Architectural diagram of Casa

![svg](../img/kubernetes/cn-casa.svg)

## Architectural diagram of SCIM

![svg](../img/kubernetes/cn-scim.svg)


## Minimum Couchbase System Requirements for cloud deployments

!!!note
    Couchbase needs optimization in a production environment and must be tested to suit the organizational needs. 
 
| NAME                                     | # of nodes  | RAM(GiB) | Disk Space | CPU | Total RAM(GiB)                           | Total CPU |
| ---------------------------------------- | ----------- | -------  | ---------- | --- | ---------------------------------------- | --------- |
| Couchbase Index                          | 1           |  3       | 5Gi        | 1  | 3                                         | 1         |
| Couchbase Query                          | 1           |  -       | 5Gi        | 1  | -                                         | 1         |
| Couchbase Data                           | 1           |  3       | 5Gi        | 1  | 3                                         | 1         |
| Couchbase Search, Eventing and Analytics | 1           |  2       | 5Gi        | 1  | 2                                         | 1         |
| Grand Total                              |             | 7-8 GB (if query pod is allocated 1 GB)  | 20Gi | 4         |
