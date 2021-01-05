# How to setup a 2k authentications per second benchmark with the Gluu Server

## Overview

The Gluu Server has been optimized with several container strategies that allow scaling micro-services and orchestrating them using Kubernetes. This tutorial will walk through installation of Gluu on AWS EKS (Elastic Kuberentes service ).

With this procedure you can expect to get the following results with a `10` million user database:

#### Results

| Flow                                           | Authentications per second    | 
| ---------------------------------------------- | ----------------------------- | 
| Resource Owner Password Credential Grant Flow  |    8300-9000                  |
| Authorization code flow                        |    2000-3000                  |


## Installation

### Set up the cluster

#### Resources

Couchbase needs sufficient resources to run and under higher loads. This becomes critical as timeouts in connections can occur, resulting in failed authentications or cut offs.

-  Follow this [guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html) to install a cluster with worker nodes. We used the `c5a.8xlarge`(32 vCPU, 64 GB Memory) instance type. Please make sure that you have all the `IAM` policies for the AWS user that will be creating the cluster and volumes.
 
#### Requirements

-   The above guide should also walk you through installing `kubectl` , `aws-iam-authenticator` and `aws cli` on the VM you will be managing your cluster and nodes from. Check to make sure.

        aws-iam-authenticator help
        aws-cli
        kubectl version

#### Resources needed

| NAME                                     | # of nodes  | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
| ---------------------------------------- | ----------- | -------  | --- | -------------- | --------- |
| Couchbase Index                          | 2           |  24      |  6  | 48             | 12        |
| Couchbase Query                          | 3           |  -       |  4  | -              | 12        |
| Couchbase Data                           | 3           |  12      |  4  | 36             | 12        |
| Couchbase Search, Eventing and Analytics | 1           |  5       |  4  | 5              | 4         |
| oxAuth                                   | 25          |  2.5     | 2.5 | 62.5           | 62.5      |
| Grand Total                              |             |          |     | 151.5 GB       | 102.5     |

!!!note
    Instance type can be selected to best suit the deployment intended. Keep in mind when selecting the instance type to strive for a `10` or up to `10` network bandwidth (Gbps). Above details the exact resources needed for this tutorial. We will follow with using `c5a.8xlarge` instance type. 
        
!!!note
    The combination of flows in this case does mean the combination of grand total resources if the authentication is to each get the described [result](#results).

!!!note
    ROPC flow hits `/token` endpoint and authorization code flow  hits a total of 4 steps, 3 authorization steps `/token`, `/authorize`, `/oxauth/login` and 1 redirect.
    
1. Create the Kubernetes cluster. We will be using EKS but GKE is also fine to use.

    ```bash
    eksctl create cluster --name gluuropccluster --version 1.17 --nodegroup-name standard-workers --node-type c5a.8xlarge --zones eu-central-1a,eu-central-1b,eu-central-1c --nodes 4 --nodes-min 1 --nodes-max 5 --region eu-central-1 --node-ami auto --ssh-public-key "~/.ssh/id_rsa.pub"
    ```

1. Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).

1. Configure [`couchbase-cluster.yaml`](#example-couchbase-clusteryaml), [`couchbase-ephemeral-buckets.yaml`](#example-couchbase-ephemeral-bucketsyaml) and [`couchbase-buckets.yaml`](#example-couchbase-bucketsyaml) . These files are used to create the couchbase cluster. Examples of these files are included below and may be used after editing the lines marked in each section to fit the setup intended.  These files must be placed in the same directory as `./pygluu-kubernetes.pyz` and the prompt `Override couchbase-cluster.yaml with a custom couchbase-cluster.yaml` must be answered `Y` after running the next step in order to use the custom files as in our examples.

1. Run :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```
    
1. Some tweaks and optimizations  which can be done in the UI at `Configuration` > `JSON Configuration` > `oxAuth Configuration` can be needed such as changing `idTokenLifetime` to `600`, and setting `sessionIdUnusedLifetime` to `14400`.

!!!note
    Prompts will ask for the rest of the information needed. You may generate the manifests (yaml files) and continue to deployment or just generate the  manifests (yaml files) during the execution of `pygluu-kubernetes.pyz`. `pygluu-kubernetes.pyz` will output a file called `settings.json` holding all the parameters. More information about this file and the vars it holds is [here](../installation-guide/install-kubernetes.md#settingsjson-parameters-file-contents) but  please don't manually create this file as the script can generate it using [`pygluu-kubernetes.pyz generate-settings`](https://github.com/GluuFederation/cloud-native-edition/releases). 

!!!note
    Keep an eye on the `gluu_token` and `gluu_session` buckets. If they get full you will begin to see oxAuth pods failing.

#### Example `settings.json` used.

```json
{
  "ACCEPT_GLUU_LICENSE": "Y",
  "GLUU_VERSION": "4.2",
  "TEST_ENVIRONMENT": "N",
  "GLUU_UPGRADE_TARGET_VERSION": "",
  "GLUU_HELM_RELEASE_NAME": "gluu",
  "NGINX_INGRESS_RELEASE_NAME": "ningress",
  "NGINX_INGRESS_NAMESPACE": "ingress-nginx",
  "INSTALL_GLUU_GATEWAY": "N",
  "POSTGRES_NAMESPACE": "",
  "KONG_NAMESPACE": "",
  "GLUU_GATEWAY_UI_NAMESPACE": "",
  "KONG_PG_USER": "",
  "KONG_PG_PASSWORD": "",
  "GLUU_GATEWAY_UI_PG_USER": "",
  "GLUU_GATEWAY_UI_PG_PASSWORD": "",
  "KONG_DATABASE": "",
  "GLUU_GATEWAY_UI_DATABASE": "",
  "POSTGRES_REPLICAS": "",
  "POSTGRES_URL": "",
  "KONG_HELM_RELEASE_NAME": "",
  "GLUU_GATEWAY_UI_HELM_RELEASE_NAME": "",
  "USE_ISTIO": "N",
  "USE_ISTIO_INGRESS": "N",
  "ISTIO_SYSTEM_NAMESPACE": "",
  "NODES_IPS": [
    "3.123.17.138",
    "3.126.207.249",
    "35.158.108.85",
    "18.156.199.103"
  ],
  "NODES_ZONES": [
    "eu-central-1a",
    "eu-central-1b",
    "eu-central-1c",
    "eu-central-1c"
  ],
  "NODES_NAMES": [
    "ip-192-168-19-56.eu-central-1.compute.internal",
    "ip-192-168-54-60.eu-central-1.compute.internal",
    "ip-192-168-77-16.eu-central-1.compute.internal",
    "ip-192-168-81-61.eu-central-1.compute.internal"
  ],
  "NODE_SSH_KEY": "~/.ssh/id_rsa",
  "HOST_EXT_IP": "22.22.22.22",
  "VERIFY_EXT_IP": "",
  "AWS_LB_TYPE": "clb",
  "USE_ARN": "Y",
  "ARN_AWS_IAM": "arn:aws:acm:eu-central-1:23423489237948:certificate/234asd234-7396-4dd5-b6c5-234asd21",
  "LB_ADD": "a55178c9c748c44b8a92e06d40e15bc0-639628331.eu-central-1.elb.amazonaws.com",
  "REDIS_URL": "",
  "REDIS_TYPE": "",
  "REDIS_PW": "",
  "REDIS_USE_SSL": "false",
  "REDIS_SSL_TRUSTSTORE": "",
  "REDIS_SENTINEL_GROUP": "",
  "REDIS_MASTER_NODES": "",
  "REDIS_NODES_PER_MASTER": "",
  "REDIS_NAMESPACE": "",
  "INSTALL_REDIS": "",
  "INSTALL_JACKRABBIT": "Y",
  "JACKRABBIT_STORAGE_SIZE": "4Gi",
  "JACKRABBIT_URL": "http://jackrabbit:8080",
  "JACKRABBIT_ADMIN_ID": "admin",
  "JACKRABBIT_ADMIN_PASSWORD": "izn%a.L>G6(=Z7)p{3|%~nIR",
  "JACKRABBIT_CLUSTER": "N",
  "JACKRABBIT_PG_USER": "",
  "JACKRABBIT_PG_PASSWORD": "",
  "JACKRABBIT_DATABASE": "",
  "DEPLOYMENT_ARCH": "eks",
  "PERSISTENCE_BACKEND": "couchbase",
  "INSTALL_COUCHBASE": "N",
  "COUCHBASE_NAMESPACE": "cbns",
  "COUCHBASE_VOLUME_TYPE": "",
  "COUCHBASE_CLUSTER_NAME": "cbgluu",
  "COUCHBASE_URL": "cbgluu.cbns.svc.cluster.local",
  "COUCHBASE_USER": "gluu",
  "COUCHBASE_SUPERUSER": "admin",
  "COUCHBASE_PASSWORD": "Couchit432#2",
  "COUCHBASE_SUPERUSER_PASSWORD": "SuperCouchit432#2",
  "COUCHBASE_CN": "Couchbase CA",
  "COUCHBASE_SUBJECT_ALT_NAME": [
    "*.cbgluu",
    "*.cbgluu.cbns",
    "*.cbgluu.cbns.svc",
    "cbgluu-srv",
    "cbgluu-srv.cbns",
    "cbgluu-srv.cbns.svc",
    "localhost"
  ],
  "COUCHBASE_CLUSTER_FILE_OVERRIDE": "Y",
  "COUCHBASE_USE_LOW_RESOURCES": "N",
  "COUCHBASE_DATA_NODES": "",
  "COUCHBASE_QUERY_NODES": "",
  "COUCHBASE_INDEX_NODES": "",
  "COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES": "",
  "COUCHBASE_GENERAL_STORAGE": "",
  "COUCHBASE_DATA_STORAGE": "",
  "COUCHBASE_INDEX_STORAGE": "",
  "COUCHBASE_QUERY_STORAGE": "",
  "COUCHBASE_ANALYTICS_STORAGE": "",
  "COUCHBASE_INCR_BACKUP_SCHEDULE": "*/30 * * * *",
  "COUCHBASE_FULL_BACKUP_SCHEDULE": "0 2 * * 6",
  "COUCHBASE_BACKUP_RETENTION_TIME": "168h",
  "COUCHBASE_BACKUP_STORAGE_SIZE": "20Gi",
  "LDAP_BACKUP_SCHEDULE": "",
  "NUMBER_OF_EXPECTED_USERS": "",
  "EXPECTED_TRANSACTIONS_PER_SEC": "",
  "USING_CODE_FLOW": "",
  "USING_SCIM_FLOW": "",
  "USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW": "",
  "DEPLOY_MULTI_CLUSTER": "N",
  "HYBRID_LDAP_HELD_DATA": "",
  "LDAP_JACKRABBIT_VOLUME": "io1",
  "APP_VOLUME_TYPE": 7,
  "LDAP_STATIC_VOLUME_ID": "",
  "LDAP_STATIC_DISK_URI": "",
  "GLUU_CACHE_TYPE": "NATIVE_PERSISTENCE",
  "GLUU_NAMESPACE": "gluu",
  "GLUU_FQDN": "cbgluu.testingluuk8.org",
  "COUNTRY_CODE": "US",
  "STATE": "TX",
  "EMAIL": "support@gluu.org",
  "CITY": "Austin",
  "ORG_NAME": "Gluu",
  "GMAIL_ACCOUNT": "",
  "GOOGLE_NODE_HOME_DIR": "",
  "IS_GLUU_FQDN_REGISTERED": "Y",
  "LDAP_PW": "Gluuit43#22",
  "ADMIN_PW": "Gluuit43#22",
  "OXD_APPLICATION_KEYSTORE_CN": "",
  "OXD_ADMIN_KEYSTORE_CN": "",
  "LDAP_STORAGE_SIZE": "",
  "OXAUTH_REPLICAS": 1,
  "OXTRUST_REPLICAS": 1,
  "LDAP_REPLICAS": "",
  "OXSHIBBOLETH_REPLICAS": "",
  "OXPASSPORT_REPLICAS": "",
  "OXD_SERVER_REPLICAS": "",
  "CASA_REPLICAS": "",
  "RADIUS_REPLICAS": "",
  "FIDO2_REPLICAS": "",
  "SCIM_REPLICAS": "",
  "ENABLE_OXTRUST_API": "N",
  "ENABLE_OXTRUST_TEST_MODE": "N",
  "ENABLE_CACHE_REFRESH": "N",
  "ENABLE_OXD": "N",
  "ENABLE_FIDO2": "N",
  "ENABLE_SCIM": "N",
  "ENABLE_RADIUS": "N",
  "ENABLE_OXPASSPORT": "N",
  "ENABLE_OXSHIBBOLETH": "N",
  "ENABLE_CASA": "N",
  "ENABLE_OXAUTH_KEY_ROTATE": "N",
  "ENABLE_OXTRUST_API_BOOLEAN": "true",
  "ENABLE_OXTRUST_TEST_MODE_BOOLEAN": "false",
  "ENABLE_RADIUS_BOOLEAN": "false",
  "ENABLE_OXPASSPORT_BOOLEAN": "false",
  "ENABLE_CASA_BOOLEAN": "false",
  "ENABLE_SAML_BOOLEAN": "false",
  "ENABLED_SERVICES_LIST": [
    "config",
    "oxauth",
    "persistence",
    "oxtrust",
    "jackrabbit"
  ],
  "OXAUTH_KEYS_LIFE": "",
  "EDIT_IMAGE_NAMES_TAGS": "N",
  "CASA_IMAGE_NAME": "gluufederation/casa",
  "CASA_IMAGE_TAG": "4.2.2_02",
  "CONFIG_IMAGE_NAME": "gluufederation/config-init",
  "CONFIG_IMAGE_TAG": "4.2.2_02",
  "CACHE_REFRESH_ROTATE_IMAGE_NAME": "gluufederation/cr-rotate",
  "CACHE_REFRESH_ROTATE_IMAGE_TAG": "4.2.2_02",
  "CERT_MANAGER_IMAGE_NAME": "gluufederation/certmanager",
  "CERT_MANAGER_IMAGE_TAG": "4.2.2_02",
  "LDAP_IMAGE_NAME": "gluufederation/opendj",
  "LDAP_IMAGE_TAG": "4.2.2_02",
  "JACKRABBIT_IMAGE_NAME": "gluufederation/jackrabbit",
  "JACKRABBIT_IMAGE_TAG": "4.2.2_02",
  "OXAUTH_IMAGE_NAME": "gluufederation/oxauth",
  "OXAUTH_IMAGE_TAG": "4.2.2_04",
  "FIDO2_IMAGE_NAME": "gluufederation/fido2",
  "FIDO2_IMAGE_TAG": "4.2.2_02",
  "SCIM_IMAGE_NAME": "gluufederation/scim",
  "SCIM_IMAGE_TAG": "4.2.2_02",
  "OXD_IMAGE_NAME": "gluufederation/oxd-server",
  "OXD_IMAGE_TAG": "4.2.2_02",
  "OXPASSPORT_IMAGE_NAME": "gluufederation/oxpassport",
  "OXPASSPORT_IMAGE_TAG": "4.2.2_03",
  "OXSHIBBOLETH_IMAGE_NAME": "gluufederation/oxshibboleth",
  "OXSHIBBOLETH_IMAGE_TAG": "4.2.2_02",
  "OXTRUST_IMAGE_NAME": "gluufederation/oxtrust",
  "OXTRUST_IMAGE_TAG": "4.2.2_03",
  "PERSISTENCE_IMAGE_NAME": "gluufederation/persistence",
  "PERSISTENCE_IMAGE_TAG": "4.2.2_02",
  "RADIUS_IMAGE_NAME": "gluufederation/radius",
  "RADIUS_IMAGE_TAG": "4.2.2_02",
  "GLUU_GATEWAY_IMAGE_NAME": "gluufederation/gluu-gateway",
  "GLUU_GATEWAY_IMAGE_TAG": "4.2.2_02",
  "GLUU_GATEWAY_UI_IMAGE_NAME": "gluufederation/gluu-gateway-ui",
  "GLUU_GATEWAY_UI_IMAGE_TAG": "4.2.2_02",
  "UPGRADE_IMAGE_NAME": "gluufederation/upgrade",
  "UPGRADE_IMAGE_TAG": "4.2.2_02",
  "CONFIRM_PARAMS": "Y"
}
```
##### Example `couchbase-buckets.yaml`

```yaml
apiVersion: couchbase.com/v2
kind: CouchbaseBucket
metadata:
  name: gluu
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu #DO NOT CHANGE THIS LINE
  memoryQuota: 200Mi
  replicas: 1
  ioPriority: low
  evictionPolicy: valueOnly
  conflictResolution: seqno
  enableFlush: true
  enableIndexReplica: false
  compressionMode: passive
---
apiVersion: couchbase.com/v2
kind: CouchbaseBucket
metadata:
  name: gluu-site
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu_site  #DO NOT CHANGE THIS LINE
  memoryQuota: 200Mi
  replicas: 1
  ioPriority: low
  evictionPolicy: valueOnly
  conflictResolution: seqno
  enableFlush: true
  enableIndexReplica: false
  compressionMode: passive
---
apiVersion: couchbase.com/v2
kind: CouchbaseBucket
metadata:
  name: gluu-user
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu_user  #DO NOT CHANGE THIS LINE
  memoryQuota: 4000Mi
  replicas: 1
  ioPriority: high
  evictionPolicy: valueOnly
  conflictResolution: seqno
  enableFlush: true
  enableIndexReplica: false
  compressionMode: passive
```

##### Example `couchbase-ephemeral-buckets.yaml`

```yaml
apiVersion: couchbase.com/v2
kind: CouchbaseEphemeralBucket
metadata:
  name: gluu-cache
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu_cache
  memoryQuota: 3000Mi
  replicas: 1
  ioPriority: high
  evictionPolicy: nruEviction
  conflictResolution: seqno
  enableFlush: true
  compressionMode: passive
---
apiVersion: couchbase.com/v2
kind: CouchbaseEphemeralBucket
metadata:
  name: gluu-token
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu_token
  memoryQuota: 6000Mi
  replicas: 1
  ioPriority: high
  evictionPolicy: nruEviction
  conflictResolution: seqno
  enableFlush: true
  compressionMode: passive
---
apiVersion: couchbase.com/v2
kind: CouchbaseEphemeralBucket
metadata:
  name: gluu-session
  labels:
    cluster: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  name: gluu_session
  memoryQuota: 8500Mi
  replicas: 1
  ioPriority: high
  evictionPolicy: nruEviction
  conflictResolution: seqno
  enableFlush: true
  compressionMode: passive

``` 
 
##### Example `couchbase-cluster.yaml`

```yaml
apiVersion: couchbase.com/v2
kind: CouchbaseCluster
metadata:
  name: cbgluu #CHANGE THIS LINE TO YOUR CLUSTER NAME
spec:
  image: couchbase/server:6.6.0
  antiAffinity: false
  networking:
    tls:
      static:
        serverSecret: couchbase-server-tls
        operatorSecret: couchbase-operator-tls
  security:
    adminSecret: cb-auth
    rbac:
      managed: true
      selector:
        matchLabels:
          cluster: cbgluu
  exposeAdminConsole: true
  adminConsoleServices:
  - data
  exposedFeatures:
  - xdcr
  - client
  exposedFeatureServiceType: NodePort
  cluster:
    autoCompaction:
      databaseFragmentationThreshold:
        percent: 30
        size: 1Gi
      viewFragmentationThreshold:
        percent: 30
        size: 1Gi
      parallelCompaction: false
      timeWindow:
        start: 02:00
        end: 06:00
        abortCompactionOutsideWindow: true
      tombstonePurgeInterval: 72h
    dataServiceMemoryQuota: 23000Mi
    indexServiceMemoryQuota: 11000Mi
    searchServiceMemoryQuota: 3200Mi
    eventingServiceMemoryQuota: 3200Mi
    analyticsServiceMemoryQuota: 3200Mi
    indexStorageSetting: memory_optimized
    autoFailoverTimeout: 10s
    autoFailoverMaxCount: 3
    autoFailoverOnDataDiskIssues: true
    autoFailoverOnDataDiskIssuesTimePeriod: 120s
    autoFailoverServerGroup: false
  buckets:
    managed: true
    selector:
      matchLabels:
        cluster: cbgluu
  servers:
  - name: data-eu-central-1a # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 6000m
        memory: 24Gi              
      requests:
        memory: 24Gi
        cpu: 6000m
    services:
    - data
    serverGroups:
    - eu-central-1a  # change to your zone
    volumeMounts:
      default: pvc-general
      data: pvc-data
  - name: data-eu-central-1c # change name to fit your zone
    size: 2
    resources:
      limits:
        cpu: 6000m
        memory: 24Gi              
      requests:
        memory: 24Gi
        cpu: 6000m
    services:
    - data
    serverGroups:
    - eu-central-1c  # change to your zone
    volumeMounts:
      default: pvc-general
      data: pvc-data
  - name: index-eu-central-1a # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 12Gi              
      requests:
        memory: 12Gi
        cpu: 4000m
    services:
    - index
    serverGroups:
    - eu-central-1a  # change to your zone
    volumeMounts:
      default: pvc-general
      index: pvc-index
  - name: index-eu-central-1b # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 12Gi              
      requests:
        memory: 12Gi
        cpu: 4000m
    services:
    - index
    serverGroups:
    - eu-central-1b  # change to your zone
    volumeMounts:
      default: pvc-general
      index: pvc-index
  - name: analytics-eu-central-1c # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 16Gi              
      requests:
        memory: 16Gi
        cpu: 4000m
    services:
    - query
    - search
    - eventing
    - analytics
    serverGroups:
    - eu-central-1c  # change to your zone
    volumeMounts:
      default: pvc-general
      analytics:
      - pvc-analytics
  - name: query-eu-central-1a # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 4Gi
      requests:
        cpu: 4000m
        memory: 4Gi
    services:
    - query
    serverGroups:
    - eu-central-1a  # change to your zone
    volumeMounts:
      default: pvc-general
  - name: query-eu-central-1b # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 4Gi
      requests:
        cpu: 4000m
        memory: 4Gi
    services:
    - query
    serverGroups:
    - eu-central-1b  # change to your zone
    volumeMounts:
      default: pvc-general
  - name: query-eu-central-1c # change name to fit your zone
    size: 1
    resources:
      limits:
        cpu: 4000m
        memory: 4Gi
      requests:
        cpu: 4000m
        memory: 4Gi
    services:
    - query
    serverGroups:
    - eu-central-1c  # change to your zone
    volumeMounts:
      default: pvc-general

  securityContext:
    fsGroup: 1000
  volumeClaimTemplates:
  - metadata:
      name: pvc-general
    spec:
      storageClassName: couchbase-sc
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: pvc-data
    spec:
      storageClassName: couchbase-sc
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: pvc-index
    spec:
      storageClassName: couchbase-sc
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: pvc-query
    spec:
      storageClassName: couchbase-sc
      resources:
        requests:
          storage: 10Gi
  - metadata:
      name: pvc-analytics
    spec:
      storageClassName: couchbase-sc
      resources:
        requests:
          storage: 10Gi
  serverGroups:
  - eu-central-1a # change to your zone
  - eu-central-1b # change to your zone
  - eu-central-1c # change to your zone

```      

### Load-test

Our tests used 10 million users that were loaded to our `gluu_user` bucket. We have created a docker image to load users rapidly using the couchbase client. That same image is also used to load test Gluu using jmeter tests for both `ROPC` and `Authorization code` flows. This image will load users and use a unique password for each user.

#### Loading users

1. Create a folder called `add_users`.

    ```bash
    mkdir add_users && cd add_users
    ```
1. Copy the following yaml into the folder under the name `load_users.yaml`.

    !!!note
        This job uses parallel jobs and needs at minimum of `18000m` CPU to function at the level needed. 

    ```yaml
    apiVersion: v1
    data:
      COUCHBASE_PW: Test1234#
      COUCHBASE_URL: cbgluu.cbns.svc.cluster.local
      LOAD_USERS_TO_COUCHBASE: "true"
      USER_NUMBER_ENDING_POINT: "10000000"
    kind: ConfigMap
    metadata:
      labels:
        app: load-users
      name: load-users-cm
    ---
    apiVersion: batch/v1
    kind: Job
    metadata:
      labels:
        app: load-users
      name: load-users
    spec:
      backoffLimit: 1
      template:
        metadata:
          labels:
            app: load-users
        spec:
          containers:
          - envFrom:
            - configMapRef:
                name: load-users-cm
            image: abudayyehwork/loadtesting:4.2.0_dev
            name: load-users
          restartPolicy: Never
    ```

1. Create a namespace for load-testing.

    ```bash
    kubectl create ns load
    ```
   
1. Create `load_users.yaml`

    ```bash
    kubectl create -f load_users.yaml -n load
    ```
   
#### Load testing

=== "ROPC client registration"

    ##### ROPC client registration
    
    ###### Resources needed for ROPC client  jmeter test
    
    | NAME                                     | # of pods   | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
    | ---------------------------------------- | ----------- | -------  | --- | -------------  | --------- |
    | ROPC jmeter test                         | 200         |  1.2     | .9  | 240            | 180       |
    | Grand Total                              |             |          |     | 240 GiB        | 180       |
    
    ###### Setup Client
    
    1. Open Gluu GUI , `OpenId Connect -> Clients --> Add New Client`
    
    1.  Create client with the following details:
    
        ```
        Client Secret: test_ro_client_password
        Client Name: test_ro
        Authentication method for the Token Endpoint:: client_secret_post
        Client Expiration Date: +few years from now
        Grant Types: password
        Response: id_token
        ```
    
    1. Save `Client ID` and `Client Secret` if changed from above.

=== "Authorization code client"

    ##### Authorization code client
    
    ###### Resources needed for Authorization code client jmeter test
    
    | NAME                                     | # of pods   | RAM(GiB) | CPU | Total RAM(GiB) | Total CPU |
    | ---------------------------------------- | ----------- | -------  | --- | -------------  | --------- |
    | Authorization code flow jmeter test      | 60          |  2.5     | 2.5 | 180            | 180       |
    | Grand Total                              |             |          |     | 180 GiB       | 180       |
    
    ###### Setup Client
    
    1. Open Gluu GUI , `OpenId Connect -> Clients -> oxTrust client`
    
    1. Save `Client ID` and `Client Secret`
    
    !!!note
        A seperate client can be created for this test similar to oxTrust client

##### Initiate load test

1. Create a folder called `load_test`.

    ```bash
    mkdir load_test && cd load_test
    ```

1. Copy the following yaml into the folder under the name `load.yaml`.
    
    ```yaml
    apiVersion: v1
    data:
      AUTHZ_CLIENT_ID: 1001.fa28ef9b-639d-4691-81bd-84ce469d8091
      AUTHZ_CLIENT_SECRET: Fa9ErhVLxqN0
      # First batch is the users from min - max that login 10% every time
      FIRST_BATCH_MAX: "1000000"
      FIRST_BATCH_MIN: "0"
      # Second batch is the users from min - max that login 90% every time
      SECOND_BATCH_MAX: "10000000"
      SECOND_BATCH_MIN: "1000001"
      # Regex of Gluu URL gluu.testingluuk8.org
      GLUU_REGEX_PART1: cbgluu
      GLUU_REGEX_PART2: testingluuk8
      GLUU_REGEX_PART3: org
      GLUU_URL: cbgluu.testingluuk8.org
      ROPC_CLIENT_ID: 4c1f46eb-6c6a-4b92-aa98-5b232b7b0530
      ROPC_CLIENT_SECRET: test_ro_client_password
      RUN_AUTHZ_TEST: "true" # or "false"
      RUN_ROPC_TEST: "false" # or "false"
    kind: ConfigMap
    metadata:
      labels:
        app: load-testing
      name: load-testing-cm
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      labels:
        app: load-testing
      name: load-testing
    spec:
      replicas: 120
      selector:
        matchLabels:
          app: load-testing
      template:
        metadata:
          labels:
            app: load-testing
        spec:
          containers:
          - envFrom:
            - configMapRef:
                name: load-testing-cm
            image: abudayyehwork/loadtesting:4.2.0_dev
            imagePullPolicy: Always
            name: load-testing
            resources:
              requests:
                memory: "2500Mi"
                cpu: "2500m"
              limits:
                memory: "2500Mi"
                cpu: "2500m"
    ```
    
1. Create a namespace for load-testing if it hasn't been created yet.

    ```bash
    kubectl create ns load
    ```
   
1. Create `load.yaml`

    ```bash
    kubectl create -f load.yaml -n load
    ```
   
1. Scale oxAuth to the number of pods according to flow. A mix and match if the total number of authentication per day is the same.

    ```bash
    # ROPC Flow
    kubectl scale deploy oxauth -n gluu --replicas=30
    # OR Authorization code Flow
    kubectl scale deploy oxauth -n gluu --replicas=30
    # OR if both flows and both need to reach the results separately. Note the resource tables in the beginning of this tutorial.
    kubectl scale deploy oxauth -n gluu --replicas=60
    ```

1. Scale load test according to flow.

    ```bash
    # ROPC Flow
    kubectl scale deploy load-testing -n load --replicas=180
    # OR Authorization code Flow
    kubectl scale deploy load-testing -n load --replicas=60
    # OR if both flows and both need to reach results separately. Note the resource tables in the beginning of this tutorial.
    kubectl scale deploy load-testing -n load --replicas=240
    ```

### Install Monitoring tools

!!!note
    This section is used for testing purposes and setup of these tools in production should consult official docs for each tool. 

1. Create a folder called `monitor`.

    ```bash
    mkdir minitor && cd monitor
    ```

1. Copy the following bash script into the folder under the name `setup_helm_prometheus_grafana.sh`. Change the password for user `admin` below as needed. This will install helm v3 , Prometheus and Grafana.

    ```bash
    #!/bin/bash
    echo "Installing Helm V3"
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    echo "Installing Prometheus"
    kubectl create namespace prometheus
    helm install prometheus stable/prometheus \
        --namespace prometheus \
        --set alertmanager.persistentVolume.storageClass="gp2" \
        --set server.persistentVolume.storageClass="gp2"
    sleep 60
    echo "Installing Grafana"
    kubectl create namespace grafana
    helm install grafana stable/grafana \
        --namespace grafana \
        --set persistence.storageClassName="gp2" \
        --set adminPassword='myPasswOrd#' \
        --set datasources."datasources\.yaml".apiVersion=1 \
        --set datasources."datasources\.yaml".datasources[0].name=Prometheus \
        --set datasources."datasources\.yaml".datasources[0].type=prometheus \
        --set datasources."datasources\.yaml".datasources[0].url=http://prometheus-server.prometheus.svc.cluster.local \
        --set datasources."datasources\.yaml".datasources[0].access=proxy \
        --set datasources."datasources\.yaml".datasources[0].isDefault=true \
        --set service.type=LoadBalancer
    sleep 60
    ELB=$(kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    echo "Grafana URL:"
    echo "http://$ELB"
    ```
   
1. Login into the URL of Grafana or the ip of the loadbalancer created as `admin` and `myPasswOrd` in our example. Several dashboards can be added but the most important one here is pod monitoring. After login, press `+` on the left panel, select `Import`, and enter `6417` for the dashboard id , `Prometheus` as the data source endpoint then press `Import`.

1. Create a dashbord to track requests to pods using the `nginx` metrics in the query section. The metrics are tuned as needed.
