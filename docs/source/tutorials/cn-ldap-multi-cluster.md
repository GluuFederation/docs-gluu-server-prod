# ALPHA-How to setup multi kubernetes clusters with Gluu Server cloud native edition and LDAP as a persistence

## Overview

This will walk you through a multi cluster setup of Gluu using LDAP as the backend persistence.

![svg](../img/kubernetes/cn-multi-cluster-ldap.svg)

## Installation

### Set up the cluster

#### Resources

Setup two kubernetes cluster. We will be using two microk8s clusters sized at t2.xlarge with one node each as an example.
 
#### Requirements

- You must make sure that the nodeports are open for ldap  communications. The node ports depend on the number of clusters and take a format of `309(namespaceintID)(n-1)`, `307(namespaceintID)(n-1)`, `304(namespaceintID)(n-1)`, and `306(namespaceintID)(n-1)`, where `n` is the replica number.
- All serf addresses will be in the format of `RELEASE-NAME-opendj-CLUSTERID-regional-STATEFULSET#-SERFADDRESSSUFFIX` and hence these addresses must be resolvable. The below table depicts the relationship , assuming the release name to be `gluu` , cluster id to be `east`, namespace int id to be `0`, and serf address suffix to be `regional.gluu.org`.

    |NodePort   |Serf advertise port  | Serf admin port | Serf LDAPS port	|Serf LDAP replication port| Serf Advertise address                          |
    |-----------|---------------------|-----------------|-------------------|--------------------------|-------------------------------------------------|
    |Replica 1  |`30700`              |`30400`	        |`30600`        	| `30900`                  | `gluu-opendj-east-regional-0-regional.gluu.org` |
    |Replica 2  |`30701`              |`30401`	        |`30601`	        | `30901`                  | `gluu-opendj-east-regional-1-regional.gluu.org` | 
    |Replica n  |`3070(n-1)`          |`3040(n-1)`	    |`3060(n-1)`	    | `3090(n-1)`              | `gluu-opendj-east-regional-(n-1)-regional.gluu.org` |


- All clusters must use the same helm release name

- All clusters will use the same nodeports

!!!note
    This is an alpha feature only offered with helm installation of Gluu >4.2.
        
!!!note
     It is recommended to start with one replica in cluster one and then scale through a helm upgrade command after the setup has finished. Forexample, you can edit the value of `opendj.multiCluster.replicaCount` inside your `values.yaml`  and run `helm upgrade <release-name> /helm -f /helm/gluu/values.yaml -n <namespace>`

!!!note
     All serf addresses will be in the format of `RELEASE-NAME-opendj-CLUSTERID-regional-STATEFULSET#-SERFADDRESSSUFFIX`

#### On the first cluster run:

1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).

1.  Run :

    ```bash
    ./pygluu-kubernetes.pyz helm-install
    ```

1.  Keep an eye out for the following prompts: 

    ```bash
    ALPHA-FEATURE-Are you setting up a multi kubernetes cluster [N] [y/N]: Y
    Please enter Serf advertise address suffix. You must be able to resolve this address in your DNS [regional.gluu.org]: regional.gluu.org
    ALPHA-FEATURE-Enter the number of opendj statefulsets to create. Each will have an advertise address of RELEASE-NAME-opendj-regional-{{statefulset number}}-{Serf address suffix }}  (1, 2, 3, 4, 5, 6, 7, 8, 9) [1]: 1
    ALPHA-FEATURE-Is this a subsequent kubernetes cluster (2nd and above) [N] [y/N]: N
    ALPHA-FEATURE-Please enter a cluster ID that distinguishes this cluster from any subsequent clusters. i.e west, east, north, south, test.. [test]: east
    ALPHA-FEATURE-Please enter the cluster IDs for all other subsequent clusters i.e west, east, north, south, test..seperated by a comma with no quotes , or brackets Forexample, if there was three other clusters ( not including this one) that Gluu will be installed three cluster IDs will be needed. This is to help generate the serf addresses automatically. [dev,stage,prod]: west
    ```
    
    All the above NodePorts must be reachable by the second cluster. Please note also that the Serf advertise address must be resolvable by both clusters. In the event that this is a test environment you may map the addresses via `hostAliases` key inside ldap StatefulSets in both cluster after deployment as in the example below:
   
    ```yaml
      hostAliases:
      - hostnames:
        - gluu-opendj-east-regional-0-regional.gluu.org
        ip: 11.11.11.11
      - hostnames:
        - gluu-opendj-west-regional-0-regional.gluu.org
        ip: 12.12.12.12
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
      volumes:
      - name: serfkey
        secret:
          secretName: gluu-serf-key
      - configMap:
          name: gluu-serf-peers
        name: serfpeers
    ```

1.  Wait for all pods to be ina ready state.

1.  Prepare `gluu` Secret for second cluster
    
    ```bash
    kubectl get  secret gluu -n gluu -o yaml > gluu-secret.yaml
    ```

1.  Prepare `gluu` ConfigMap for second cluster

    ```bash
    kubectl get cm gluu -n gluu -o yaml > gluu-cm.yaml
    ```
    
#### On the second cluster:

1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).

1.  Move the following from the first cluster:
    - `settings.json`
    - `gluu-secret.yaml`
    -  `gluu-cm.yaml`

1.  Place `settings.json` adjacent to `pygluu-kubernetes.pyz`.

1.  Create the namespace for gluu. It must match the one created in the first cluster

    ```bash
    kubectl create ns gluu
    ```
   
1.  Create both `gluu-secret.yaml` and `gluu-cm.yaml`

    ```bash
    kubectl create -f gluu-secret.yaml
    kubectl create -f gluu-cm.yaml
    ```
    
1.  Open `settings.json` at the second cluster and edit the following lines to match your setup:

    ```json
      "GLUU_LDAP_SECONDARY_CLUSTER": "Y",
      "GLUU_LDAP_MULTI_CLUSTER_CLUSTER_ID": "west",
    ```
    

1.  Run :

    ```bash
    ./pygluu-kubernetes.pyz helm-install
    ```
   
1.  Tail the logs and wait for replication to occur. Services should start turning on soon after replication finishes.

#### Test replication

You may run `dsreplication` command to check the replication status using the a command as in the example below:

```bash
kubectl exec -ti gluu-opendj-0 -n gluu -- /opt/opendj/bin/dsreplication status -X


>>>> Specify OpenDJ LDAP connection parameters

Directory server hostname or IP address [gluu-opendj-regional-0-0]: 
Directory server administration port number [30440]: 

Global Administrator User ID [admin]: 

Password for user 'admin': 
Suffix DN : Server                                              : Entries : Replication enabled : DS ID : RS ID : RS Port (1) : M.C. (2) : A.O.M.C. (3) : Security (4)
----------:-----------------------------------------------------:---------:---------------------:-------:-------:-------------:----------:--------------:-------------
o=gluu    : gluu-opendj-east-regional-0-regional.gluu.org:30400 : 210     : true                : 3405  : 24442 : 30980       : 0        :              : true
o=gluu    : gluu-opendj-east-regional-1-regional.gluu.org:30401 : 210     : true                : 10457 : 11635 : 30981       : 0        :              : true
o=gluu    : gluu-opendj-west-regional-1-regional.gluu.org:30401 : 210     : true                : 20953 : 28477 : 30981       : 0        :              : true
o=metric  : gluu-opendj-east-regional-0-regional.gluu.org:30400 : 25      : true                : 6048  : 24442 : 30980       : 24       :              : true
o=metric  : gluu-opendj-east-regional-1-regional.gluu.org:30401 : 28      : true                : 12646 : 11635 : 30981       : 14       :              : true
o=metric  : gluu-opendj-west-regional-1-regional.gluu.org:30401 : 7       : true                : 13210 : 28477 : 30981       : 52       :              : true
o=site    : gluu-opendj-east-regional-0-regional.gluu.org:30400 : 2       : true                : 2115  : 24442 : 30980       : 0        :              : true
o=site    : gluu-opendj-east-regional-1-regional.gluu.org:30401 : 2       : true                : 2672  : 11635 : 30981       : 0        :              : true
o=site    : gluu-opendj-west-regional-1-regional.gluu.org:30401 : 2       : true                : 3031  : 28477 : 30981       : 0        :              : true

[1] The port used to communicate between the servers whose contents are being
replicated.
[2] The number of changes that are still missing on this server (and that have
been applied to at least one of the other servers).
[3] Age of oldest missing change: the date on which the oldest change that has
not arrived on this server was generated.
[4] Whether the replication communication through the replication port is
encrypted or not.

```   

#### Example `settings.json` used in the first cluster.

```json
{
  "ACCEPT_GLUU_LICENSE": "Y",
  "GLUU_VERSION": "4.2",
  "TEST_ENVIRONMENT": "",
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
  "USE_ISTIO_INGRESS": "",
  "ISTIO_SYSTEM_NAMESPACE": "",
  "NODES_ZONES": [],
  "NODES_NAMES": [],
  "NODE_SSH_KEY": "",
  "VERIFY_EXT_IP": "",
  "AWS_LB_TYPE": "",
  "USE_ARN": "",
  "VPC_CIDR": "",
  "ARN_AWS_IAM": "",
  "LB_ADD": "",
  "REDIS_URL": "",
  "REDIS_TYPE": "",
  "REDIS_PW": "",
  "REDIS_USE_SSL": "false",
  "REDIS_SSL_TRUSTSTORE": "",
  "REDIS_SENTINEL_GROUP": "",
  "REDIS_NAMESPACE": "",
  "INSTALL_REDIS": "",
  "INSTALL_JACKRABBIT": "Y",
  "JACKRABBIT_STORAGE_SIZE": "4Gi",
  "JACKRABBIT_URL": "http://jackrabbit:8080",
  "JACKRABBIT_ADMIN_ID": "admin",
  "JACKRABBIT_ADMIN_PASSWORD": ":bC-g@<_|Db{+@*|<Su1p|{o",
  "JACKRABBIT_CLUSTER": "N",
  "JACKRABBIT_PG_USER": "",
  "JACKRABBIT_PG_PASSWORD": "",
  "JACKRABBIT_DATABASE": "",
  "DEPLOYMENT_ARCH": "microk8s",
  "PERSISTENCE_BACKEND": "ldap",
  "INSTALL_COUCHBASE": "",
  "COUCHBASE_NAMESPACE": "",
  "COUCHBASE_VOLUME_TYPE": "",
  "COUCHBASE_CLUSTER_NAME": "",
  "COUCHBASE_URL": "",
  "COUCHBASE_USER": "",
  "COUCHBASE_BUCKET_PREFIX": "",
  "COUCHBASE_SUPERUSER": "",
  "COUCHBASE_PASSWORD": "",
  "COUCHBASE_SUPERUSER_PASSWORD": "",
  "COUCHBASE_CRT": "",
  "COUCHBASE_CN": "",
  "COUCHBASE_INDEX_NUM_REPLICA": "",
  "COUCHBASE_SUBJECT_ALT_NAME": "",
  "COUCHBASE_CLUSTER_FILE_OVERRIDE": "",
  "COUCHBASE_USE_LOW_RESOURCES": "",
  "COUCHBASE_DATA_NODES": "",
  "COUCHBASE_QUERY_NODES": "",
  "COUCHBASE_INDEX_NODES": "",
  "COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES": "",
  "COUCHBASE_GENERAL_STORAGE": "",
  "COUCHBASE_DATA_STORAGE": "",
  "COUCHBASE_INDEX_STORAGE": "",
  "COUCHBASE_QUERY_STORAGE": "",
  "COUCHBASE_ANALYTICS_STORAGE": "",
  "COUCHBASE_INCR_BACKUP_SCHEDULE": "",
  "COUCHBASE_FULL_BACKUP_SCHEDULE": "",
  "COUCHBASE_BACKUP_RETENTION_TIME": "",
  "COUCHBASE_BACKUP_STORAGE_SIZE": "",
  "LDAP_BACKUP_SCHEDULE": "",
  "NUMBER_OF_EXPECTED_USERS": "",
  "EXPECTED_TRANSACTIONS_PER_SEC": "",
  "USING_CODE_FLOW": "",
  "USING_SCIM_FLOW": "",
  "USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW": "",
  "DEPLOY_MULTI_CLUSTER": "",
  "HYBRID_LDAP_HELD_DATA": "",
  "LDAP_JACKRABBIT_VOLUME": "",
  "APP_VOLUME_TYPE": 1,
  "LDAP_STATIC_VOLUME_ID": "",
  "LDAP_STATIC_DISK_URI": "",
  "GLUU_CACHE_TYPE": "NATIVE_PERSISTENCE",
  "GLUU_NAMESPACE": "gluu",
  "GLUU_FQDN": "demoexample.gluu.org",
  "COUNTRY_CODE": "US",
  "STATE": "TX",
  "EMAIL": "support@gluu.org",
  "CITY": "Austin",
  "ORG_NAME": "Gluu",
  "GMAIL_ACCOUNT": "",
  "GOOGLE_NODE_HOME_DIR": "",
  "IS_GLUU_FQDN_REGISTERED": "N",
  "LDAP_PW": "Test65Me$",
  "ADMIN_PW": "Test1234#",
  "OXD_APPLICATION_KEYSTORE_CN": "",
  "OXD_ADMIN_KEYSTORE_CN": "",
  "LDAP_STORAGE_SIZE": "4Gi",
  "OXAUTH_REPLICAS": 1,
  "OXTRUST_REPLICAS": 1,
  "LDAP_REPLICAS": 1,
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
    "ldap",
    "update-lb-ip",
    "oxauth",
    "persistence",
    "jackrabbit",
    "oxtrust",
    "config"
  ],
  "OXAUTH_KEYS_LIFE": "",
  "EDIT_IMAGE_NAMES_TAGS": "N",
  "CASA_IMAGE_NAME": "gluufederation/casa",
  "CASA_IMAGE_TAG": "4.2.3_02",
  "CONFIG_IMAGE_NAME": "gluufederation/config-init",
  "CONFIG_IMAGE_TAG": "4.2.3_03",
  "CACHE_REFRESH_ROTATE_IMAGE_NAME": "gluufederation/cr-rotate",
  "CACHE_REFRESH_ROTATE_IMAGE_TAG": "4.2.3_03",
  "CERT_MANAGER_IMAGE_NAME": "gluufederation/certmanager",
  "CERT_MANAGER_IMAGE_TAG": "4.2.3_07",
  "LDAP_IMAGE_NAME": "gluufederation/opendj",
  "LDAP_IMAGE_TAG": "4.2.3_02",
  "JACKRABBIT_IMAGE_NAME": "gluufederation/jackrabbit",
  "JACKRABBIT_IMAGE_TAG": "4.2.3_02",
  "OXAUTH_IMAGE_NAME": "gluufederation/oxauth",
  "OXAUTH_IMAGE_TAG": "4.2.3_06",
  "FIDO2_IMAGE_NAME": "gluufederation/fido2",
  "FIDO2_IMAGE_TAG": "4.2.3_02",
  "SCIM_IMAGE_NAME": "gluufederation/scim",
  "SCIM_IMAGE_TAG": "4.2.3_02",
  "OXD_IMAGE_NAME": "gluufederation/oxd-server",
  "OXD_IMAGE_TAG": "4.2.3_02",
  "OXPASSPORT_IMAGE_NAME": "gluufederation/oxpassport",
  "OXPASSPORT_IMAGE_TAG": "4.2.3_04",
  "OXSHIBBOLETH_IMAGE_NAME": "gluufederation/oxshibboleth",
  "OXSHIBBOLETH_IMAGE_TAG": "4.2.3_04",
  "OXTRUST_IMAGE_NAME": "gluufederation/oxtrust",
  "OXTRUST_IMAGE_TAG": "4.2.3_02",
  "PERSISTENCE_IMAGE_NAME": "gluufederation/persistence",
  "PERSISTENCE_IMAGE_TAG": "4.2.3_03",
  "RADIUS_IMAGE_NAME": "gluufederation/radius",
  "RADIUS_IMAGE_TAG": "4.2.3_02",
  "GLUU_GATEWAY_IMAGE_NAME": "gluufederation/gluu-gateway",
  "GLUU_GATEWAY_IMAGE_TAG": "4.2.2_01",
  "GLUU_GATEWAY_UI_IMAGE_NAME": "gluufederation/gluu-gateway-ui",
  "GLUU_GATEWAY_UI_IMAGE_TAG": "4.2.2_01",
  "UPGRADE_IMAGE_NAME": "gluufederation/upgrade",
  "UPGRADE_IMAGE_TAG": "4.2.3_03",
  "CONFIRM_PARAMS": "Y",
  "GLUU_LDAP_MULTI_CLUSTER": "Y",
  "GLUU_LDAP_SERF_PORT": "30946",
  "GLUU_LDAP_ADVERTISE_ADDRESS": "firstldap.gluu.org:30946",
  "GLUU_LDAP_ADVERTISE_ADMIN_PORT": "30444",
  "GLUU_LDAP_ADVERTISE_LDAPS_PORT": "30636",
  "GLUU_LDAP_ADVERTISE_REPLICATION_PORT": "30989",
  "GLUU_LDAP_SECONDARY_CLUSTER": "N",
  "GLUU_LDAP_SERF_PEERS": [
    "gluu-opendj-west-regional-0-regional.gluu.org:30940",
    "gluu-opendj-east-regional-0-regional.gluu.org:30940",
    "gluu-opendj-west-regional-1-regional.gluu.org:30941",
    "gluu-opendj-east-regional-1-regional.gluu.org:30941"
  ],
  "GLUU_LDAP_MULTI_CLUSTER_REPLICAS": 1,
  "GLUU_LDAP_MULTI_CLUSTER_CLUSTER_ID": "east",
  "GLUU_LDAP_MUTLI_CLUSTERS_IDS": [
    "west",
    "east"
  ]
}
``` 
  
#### Example `settings.json` used in the second cluster.

```json
{
  "ACCEPT_GLUU_LICENSE": "Y",
  "GLUU_VERSION": "4.2",
  "TEST_ENVIRONMENT": "",
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
  "USE_ISTIO_INGRESS": "",
  "ISTIO_SYSTEM_NAMESPACE": "",
  "NODES_ZONES": [],
  "NODES_NAMES": [],
  "NODE_SSH_KEY": "",
  "VERIFY_EXT_IP": "",
  "AWS_LB_TYPE": "",
  "USE_ARN": "",
  "VPC_CIDR": "",
  "ARN_AWS_IAM": "",
  "LB_ADD": "",
  "REDIS_URL": "",
  "REDIS_TYPE": "",
  "REDIS_PW": "",
  "REDIS_USE_SSL": "false",
  "REDIS_SSL_TRUSTSTORE": "",
  "REDIS_SENTINEL_GROUP": "",
  "REDIS_NAMESPACE": "",
  "INSTALL_REDIS": "",
  "INSTALL_JACKRABBIT": "Y",
  "JACKRABBIT_STORAGE_SIZE": "4Gi",
  "JACKRABBIT_URL": "http://jackrabbit:8080",
  "JACKRABBIT_ADMIN_ID": "admin",
  "JACKRABBIT_ADMIN_PASSWORD": ":bC-g@<_|Db{+@*|<Su1p|{o",
  "JACKRABBIT_CLUSTER": "N",
  "JACKRABBIT_PG_USER": "",
  "JACKRABBIT_PG_PASSWORD": "",
  "JACKRABBIT_DATABASE": "",
  "DEPLOYMENT_ARCH": "microk8s",
  "PERSISTENCE_BACKEND": "ldap",
  "INSTALL_COUCHBASE": "",
  "COUCHBASE_NAMESPACE": "",
  "COUCHBASE_VOLUME_TYPE": "",
  "COUCHBASE_CLUSTER_NAME": "",
  "COUCHBASE_URL": "",
  "COUCHBASE_USER": "",
  "COUCHBASE_BUCKET_PREFIX": "",
  "COUCHBASE_SUPERUSER": "",
  "COUCHBASE_PASSWORD": "",
  "COUCHBASE_SUPERUSER_PASSWORD": "",
  "COUCHBASE_CRT": "",
  "COUCHBASE_CN": "",
  "COUCHBASE_INDEX_NUM_REPLICA": "",
  "COUCHBASE_SUBJECT_ALT_NAME": "",
  "COUCHBASE_CLUSTER_FILE_OVERRIDE": "",
  "COUCHBASE_USE_LOW_RESOURCES": "",
  "COUCHBASE_DATA_NODES": "",
  "COUCHBASE_QUERY_NODES": "",
  "COUCHBASE_INDEX_NODES": "",
  "COUCHBASE_SEARCH_EVENTING_ANALYTICS_NODES": "",
  "COUCHBASE_GENERAL_STORAGE": "",
  "COUCHBASE_DATA_STORAGE": "",
  "COUCHBASE_INDEX_STORAGE": "",
  "COUCHBASE_QUERY_STORAGE": "",
  "COUCHBASE_ANALYTICS_STORAGE": "",
  "COUCHBASE_INCR_BACKUP_SCHEDULE": "",
  "COUCHBASE_FULL_BACKUP_SCHEDULE": "",
  "COUCHBASE_BACKUP_RETENTION_TIME": "",
  "COUCHBASE_BACKUP_STORAGE_SIZE": "",
  "LDAP_BACKUP_SCHEDULE": "",
  "NUMBER_OF_EXPECTED_USERS": "",
  "EXPECTED_TRANSACTIONS_PER_SEC": "",
  "USING_CODE_FLOW": "",
  "USING_SCIM_FLOW": "",
  "USING_RESOURCE_OWNER_PASSWORD_CRED_GRANT_FLOW": "",
  "DEPLOY_MULTI_CLUSTER": "",
  "HYBRID_LDAP_HELD_DATA": "",
  "LDAP_JACKRABBIT_VOLUME": "",
  "APP_VOLUME_TYPE": 1,
  "LDAP_STATIC_VOLUME_ID": "",
  "LDAP_STATIC_DISK_URI": "",
  "GLUU_CACHE_TYPE": "NATIVE_PERSISTENCE",
  "GLUU_NAMESPACE": "gluu",
  "GLUU_FQDN": "demoexample.gluu.org",
  "COUNTRY_CODE": "US",
  "STATE": "TX",
  "EMAIL": "support@gluu.org",
  "CITY": "Austin",
  "ORG_NAME": "Gluu",
  "GMAIL_ACCOUNT": "",
  "GOOGLE_NODE_HOME_DIR": "",
  "IS_GLUU_FQDN_REGISTERED": "N",
  "LDAP_PW": "Test65Me$",
  "ADMIN_PW": "Test1234#",
  "OXD_APPLICATION_KEYSTORE_CN": "",
  "OXD_ADMIN_KEYSTORE_CN": "",
  "LDAP_STORAGE_SIZE": "4Gi",
  "OXAUTH_REPLICAS": 1,
  "OXTRUST_REPLICAS": 1,
  "LDAP_REPLICAS": 1,
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
    "persistence",
    "jackrabbit",
    "oxtrust",
    "update-lb-ip",
    "ldap",
    "oxauth",
    "config"
  ],
  "OXAUTH_KEYS_LIFE": "",
  "EDIT_IMAGE_NAMES_TAGS": "N",
  "CASA_IMAGE_NAME": "gluufederation/casa",
  "CASA_IMAGE_TAG": "4.2.3_02",
  "CONFIG_IMAGE_NAME": "gluufederation/config-init",
  "CONFIG_IMAGE_TAG": "4.2.3_03",
  "CACHE_REFRESH_ROTATE_IMAGE_NAME": "gluufederation/cr-rotate",
  "CACHE_REFRESH_ROTATE_IMAGE_TAG": "4.2.3_03",
  "CERT_MANAGER_IMAGE_NAME": "gluufederation/certmanager",
  "CERT_MANAGER_IMAGE_TAG": "4.2.3_07",
  "LDAP_IMAGE_NAME": "gluufederation/opendj",
  "LDAP_IMAGE_TAG": "4.2.3_02",
  "JACKRABBIT_IMAGE_NAME": "gluufederation/jackrabbit",
  "JACKRABBIT_IMAGE_TAG": "4.2.3_02",
  "OXAUTH_IMAGE_NAME": "gluufederation/oxauth",
  "OXAUTH_IMAGE_TAG": "4.2.3_06",
  "FIDO2_IMAGE_NAME": "gluufederation/fido2",
  "FIDO2_IMAGE_TAG": "4.2.3_02",
  "SCIM_IMAGE_NAME": "gluufederation/scim",
  "SCIM_IMAGE_TAG": "4.2.3_02",
  "OXD_IMAGE_NAME": "gluufederation/oxd-server",
  "OXD_IMAGE_TAG": "4.2.3_02",
  "OXPASSPORT_IMAGE_NAME": "gluufederation/oxpassport",
  "OXPASSPORT_IMAGE_TAG": "4.2.3_04",
  "OXSHIBBOLETH_IMAGE_NAME": "gluufederation/oxshibboleth",
  "OXSHIBBOLETH_IMAGE_TAG": "4.2.3_04",
  "OXTRUST_IMAGE_NAME": "gluufederation/oxtrust",
  "OXTRUST_IMAGE_TAG": "4.2.3_02",
  "PERSISTENCE_IMAGE_NAME": "gluufederation/persistence",
  "PERSISTENCE_IMAGE_TAG": "4.2.3_03",
  "RADIUS_IMAGE_NAME": "gluufederation/radius",
  "RADIUS_IMAGE_TAG": "4.2.3_02",
  "GLUU_GATEWAY_IMAGE_NAME": "gluufederation/gluu-gateway",
  "GLUU_GATEWAY_IMAGE_TAG": "4.2.2_01",
  "GLUU_GATEWAY_UI_IMAGE_NAME": "gluufederation/gluu-gateway-ui",
  "GLUU_GATEWAY_UI_IMAGE_TAG": "4.2.2_01",
  "UPGRADE_IMAGE_NAME": "gluufederation/upgrade",
  "UPGRADE_IMAGE_TAG": "4.2.3_02",
  "CONFIRM_PARAMS": "Y",
  "GLUU_LDAP_MULTI_CLUSTER": "Y",
  "GLUU_LDAP_ADVERTISE_ADDRESS": "regional.gluu.org",
  "GLUU_LDAP_SECONDARY_CLUSTER": "Y",
  "GLUU_LDAP_SERF_PEERS": [
    "gluu-opendj-west-regional-0-regional.gluu.org:30940",
    "gluu-opendj-east-regional-0-regional.gluu.org:30940",
    "gluu-opendj-west-regional-1-regional.gluu.org:30941",
    "gluu-opendj-east-regional-1-regional.gluu.org:30941"
  ],
  "GLUU_LDAP_MULTI_CLUSTER_REPLICAS": 1,
  "GLUU_LDAP_MULTI_CLUSTER_CLUSTER_ID": "west",
  "GLUU_LDAP_MULTI_CLUSTERS_IDS": [
    "west",
    "east"
  ]
}
```
