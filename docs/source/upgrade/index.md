# Upgrade to Gluu Server 4.3

!!! Important
    The upgrade process for Gluu Server 4.3.0 will be made available once the initial beta testing has completed.

=== "Community Edition"
    
    ## Overview
    The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.3. 
    
    ### Pre-requisites
    
    - Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
    - Upgrades should always be thoroughly scoped and tested on a development environment *first*.
    - This upgrade process only upgrades versions 4.0.x through 4.1.x. To upgrade from a previous version, first [upgrade to 4.0](https://gluu.org/docs/gluu-server/4.0/upgrade/).
    
    #### Online Upgrade from 4.x to 4.3
    
    !!! Note
        Upgrade script runs on Python 3. You need to install Python 3 before running the script.
        * On CentoOS/RHEL: `yum install -y python3`
        * On Ubuntu/Debian: `apt-get update && apt-get install -y python3`
    
    The upgrade script downloads all needed software and applications from the internet. You can perform an online upgrade by following these steps:
    
    * Download the upgrade script
    
    ```
    wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.3.0/upg4xto430.py
    ```
    
    * Execute the script:
    
    ```
    python3 upg4xto430.py
    ```
    
    Your upgrade directory will be the current directory. The script will create these directories: `app`, and `ces_current`, and writes Gluu cacerts.
    

=== "Cloud Native Edition"

    !!!warning
        This section is under construction. 
    
    ## Overview
    
    This guide introduces how to upgrade cloud native edition from one version to another.

    ### Upgrade
    
    #### Helm

    === "LDAP"
    
        1.  Copy the following yaml into `upgrade.yaml` and adjust all entries marked below:
         
            ```yaml
            apiVersion: v1
            data:
              DOMAIN: FQDN #<-- Change this to your FQDN
              GLUU_CACHE_TYPE: NATIVE_PERSISTENCE #<-- Change this if necessary
              GLUU_CONFIG_ADAPTER: kubernetes
              GLUU_CONFIG_KUBERNETES_NAMESPACE: gluu  #<-- Change this to Gluus namespace
              GLUU_LDAP_URL: opendj:1636
              GLUU_PERSISTENCE_TYPE: ldap
              GLUU_SECRET_ADAPTER: kubernetes
              GLUU_SECRET_KUBERNETES_NAMESPACE: gluu #<-- Change this to Gluus namespace
            kind: ConfigMap
            metadata:
              labels:
                app: gluu-upgrade
              name: upgrade-cm
            ---
            apiVersion: batch/v1
            kind: Job
            metadata:
              labels:
                app: gluu-upgrade
              name: gluu-upgrade-job
            spec:
              template:
                metadata:
                  annotations:
                     sidecar.istio.io/inject: "false"                
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.2"
                    - --target
                    - "4.3"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.3.0_b1
                    name: gluu-upgrade-job
                  restartPolicy: Never
            ```
            
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.3 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. Also make sure your current `values.yaml` other options are moved correctly to the new values.yaml.
            Move old `settings.json` that was used in 4.2 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
            
            Go over your `values.yaml` and make sure it reflects all current information.
            
        1.  Inside `values.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
        
        1.  Create configmap for `101-ox.ldif` file.
        
            ```bash
            kubectl -n <gluu-namespace> create -f https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.3/pygluu/kubernetes/templates/ldap/base/101-ox.yaml
            ```
            
        1.  Delete `oxAuthExpiration` index
        
            ```bash
            kubectl exec -ti gluu-opendj-0 -n <gluu-namespace> -- /opt/opendj/bin/dsconfig delete-backend-index --backend-name userRoot --index-name oxAuthExpiration --hostName 0.0.0.0 --port 4444 --bindDN 'cn=Directory Manager' --trustAll -f
            ```
            
        1.  Mount 101-ox.ldif in opendj-pods. Open opendj yaml or edit the statefulset directly `kubectl edit statefulset gluu-opendj -n gluu`
        
            ```yaml
              volumes:
              - name: ox-ldif-cm
                configMap:
                  name: oxldif
              containers:
                image: gluufederation/opendj:4.3.0_b1
                ...
                ...
                volumeMounts:
                - name: ox-ldif-cm
                  mountPath: /opt/opendj/config/schema/101-ox.ldif
                  subPath: 101-ox.ldif
        
            ```
            
        1. Apply `upgrade.yaml`
        
            ```bash
            kubectl create -f upgrade.yaml -n <gluu-namespace>
            ```
           
            Wait until upgrade job is finished and tail the logs of the upgrade pod.
                   
        1.  Run upgrade `Helm`
        
            ```bash
            helm upgrade <release-name> . -f ./values.yaml -n <namespace>   
            ```
             
        
    === "Couchbase"
      
        1.  Copy the following yaml into `upgrade.yaml` and adjust all entries marked below:
         
            ```yaml
            apiVersion: v1
            data:
              DOMAIN: FQDN #<-- Change this to your FQDN
              GLUU_CACHE_TYPE: NATIVE_PERSISTENCE #<-- Change this if necessary
              GLUU_CONFIG_ADAPTER: kubernetes
              GLUU_CONFIG_KUBERNETES_NAMESPACE: gluu  #<-- Change this to Gluus namespace
              GLUU_COUCHBASE_CERT_FILE: /etc/certs/couchbase.crt
              GLUU_COUCHBASE_PASSWORD_FILE: /etc/gluu/conf/couchbase_password #<-- super user password
              GLUU_COUCHBASE_URL: cbgluu.cbns.svc.cluster.local #<-- Change this if necessary
              GLUU_COUCHBASE_USER: admin #<-- Change super user if necessary .
              GLUU_COUCHBASE_BUCKET_PREFIX: gluu #<-- Change if necessary .
              GLUU_PERSISTENCE_TYPE: couchbase
              GLUU_SECRET_ADAPTER: kubernetes
              GLUU_SECRET_KUBERNETES_NAMESPACE: gluu #<-- Change this to Gluus namespace
            kind: ConfigMap
            metadata:
              labels:
                app: gluu-upgrade
              name: upgrade-cm
            ---
            apiVersion: batch/v1
            kind: Job
            metadata:
              labels:
                app: gluu-upgrade
              name: gluu-upgrade-job
            spec:
              template:
                metadata:
                  annotations:
                     sidecar.istio.io/inject: "false"              
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.2"
                    - --target
                    - "4.3"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.3.0_b1
                    name: gluu-upgrade-job                 
                    volumeMounts:
                    - mountPath: /etc/gluu/conf/couchbase_password
                      name: cb-pass
                      subPath: couchbase_password
                    - mountPath: /etc/certs/couchbase.crt
                      name: cb-crt
                      subPath: couchbase.crt
                  restartPolicy: Never
                  volumes:
                  - name: cb-pass
                    secret:
                      secretName: cb-pass #<-- Change this to the secret name holding couchbase superuser pass
                  - name: cb-crt
                    secret:
                      secretName: cb-crt #<-- Change this to the secret name holding couchbase cert
            ```
            
        1. Add a new bucket  named `gluu_session`.
            
            === "Couchbase Operator v1"
            
                Add the following to `couchbase-cluster.yaml` under the buckets section:
                
                ```yaml
                  buckets:
                  - name: gluu_session   #DO NOT CHANGE THIS LINE
                    type: ephemeral
                    memoryQuota: 100 #<-- Change this if necessary
                    replicas: 1
                    ioPriority: high
                    evictionPolicy: nruEviction
                    conflictResolution: seqno
                    enableFlush: true
                    enableIndexReplica: false
                    compressionMode: passive
                ```
                
            === "Couchbase Operator v2"
            
                Apply the following yaml in the couchbase namespace:
                
                ```yaml
                cat <<EOF | kubectl apply -f -
                apiVersion: couchbase.com/v2
                kind: CouchbaseEphemeralBucket
                metadata:
                  name: gluu-session
                  labels:
                    cluster: gluu-couchbase
                spec:
                  name: gluu_session
                  memoryQuota: 100Mi #<-- Change this if necessary
                  replicas: 1
                  ioPriority: high
                  evictionPolicy: nruEviction
                  conflictResolution: seqno
                  enableFlush: true
                  compressionMode: passive
                EOF
                ```

        1. Add a new user in couchbase  named `gluu`.
            
            === "Couchbase Operator v1"
            
                1. Inside the Couchbase UI create a group by going to `Security` --> `ADD GROUP` and call that `gluu-group`  and add `query_select`, `query_insert`, `query_update` and `query_delete` to gluu buckets `gluu`, `gluu_session`, `gluu_token`, `gluu_cache` and `gluu_site`.

                1. Inside the Couchbase UI create a user by going to `Security` --> `ADD USER` and call that user `gluu` and choose a good password and remember that as you will need it later. Assign the group `gluu-group`  which was create in the previous step to that user.
                                
            === "Couchbase Operator v2"
                
                1.  Create a secret that will hold `gluu` password in the couchbase namespace:
                
                ```bash
                kubectl create secret generic gluu-couchbase-user-password --from-literal=password=P@ssw0rd --namespace cbns
                ```
                
                1.  Apply the following yaml in the couchbase namespace:
                
                ```yaml
                cat <<EOF | kubectl apply -f -
                apiVersion: couchbase.com/v2
                kind: CouchbaseGroup
                metadata:
                  name: gluu-group
                  labels:
                    cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                spec:
                  roles:
                  - name: query_select
                    bucket: gluu
                  - name: query_select
                    bucket: gluu_site
                  - name: query_select
                    bucket: gluu_user
                  - name: query_select
                    bucket: gluu_cache
                  - name: query_select
                    bucket: gluu_token
                  - name: query_select
                    bucket: gluu_session
                
                  - name: query_update
                    bucket: gluu
                  - name: query_update
                    bucket: gluu_site
                  - name: query_update
                    bucket: gluu_user
                  - name: query_update
                    bucket: gluu_cache
                  - name: query_update
                    bucket: gluu_token
                  - name: query_update
                    bucket: gluu_session
                
                  - name: query_insert
                    bucket: gluu
                  - name: query_insert
                    bucket: gluu_site
                  - name: query_insert
                    bucket: gluu_user
                  - name: query_insert
                    bucket: gluu_cache
                  - name: query_insert
                    bucket: gluu_token
                  - name: query_insert
                    bucket: gluu_session
                
                  - name: query_delete
                    bucket: gluu
                  - name: query_delete
                    bucket: gluu_site
                  - name: query_delete
                    bucket: gluu_user
                  - name: query_delete
                    bucket: gluu_cache
                  - name: query_delete
                    bucket: gluu_token
                  - name: query_delete
                    bucket: gluu_session
                ---
                apiVersion: couchbase.com/v2
                kind: CouchbaseRoleBinding
                metadata:
                  name: gluu-role-binding
                spec:
                  subjects:
                  - kind: CouchbaseUser
                    name: gluu
                  roleRef:
                    kind: CouchbaseGroup
                    name: gluu-group
                ---
                apiVersion: couchbase.com/v2
                kind: CouchbaseUser
                metadata:
                  name: gluu
                  labels:
                    cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                spec:
                  fullName: "Gluu Cloud Native"
                  authDomain: local
                  authSecret: gluu-couchbase-user-password
                EOF
                ```
                                
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.3 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.3/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.3/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.2 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
            
            Go over your `values.yaml` and make sure it reflects all current information. Forexample, make sure your couchbase url and crt are filled and correct. Also make sure that your couchbase user and password are the new ones which you created in a previous step,  and that the couchbase superuser and superuser password are filled correctly.
            
        1.  Inside `values.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
                        
        1.  Apply `upgrade.yaml`
        
            ```bash
            kubectl create -f upgrade.yaml -n <gluu-namespace>
            ```
           
            Wait until upgrade job is finished and tail the logs of the upgrade pod.
           
        1.  Run upgrade `Helm`
        
            ```bash
            helm upgrade <release-name> . -f ./values.yaml -n <namespace>   
            ```

    === "Hybrid"
      
        1.  Copy the following yaml into `upgrade.yaml` and adjust all entries marked below:
         
            ```yaml
            apiVersion: v1
            data:
              DOMAIN: FQDN #<-- Change this to your FQDN
              GLUU_CACHE_TYPE: NATIVE_PERSISTENCE #<-- Change this if necessary
              GLUU_CONFIG_ADAPTER: kubernetes
              GLUU_CONFIG_KUBERNETES_NAMESPACE: gluu  #<-- Change this to Gluus namespace
              GLUU_COUCHBASE_CERT_FILE: /etc/certs/couchbase.crt
              GLUU_COUCHBASE_PASSWORD_FILE: /etc/gluu/conf/couchbase_password #<-- super user password
              GLUU_COUCHBASE_URL: cbgluu.cbns.svc.cluster.local #<-- Change this if necessary
              GLUU_COUCHBASE_USER: admin #<-- Change this if necessary
              GLUU_COUCHBASE_BUCKET_PREFIX: gluu #<-- Change if necessary .
              GLUU_LDAP_URL: opendj:1636
              GLUU_PERSISTENCE_LDAP_MAPPING: "default" #<-- Change this if needed
              GLUU_PERSISTENCE_TYPE: couchbase
              GLUU_SECRET_ADAPTER: kubernetes
              GLUU_SECRET_KUBERNETES_NAMESPACE: gluu #<-- Change this to Gluus namespace
            kind: ConfigMap
            metadata:
              labels:
                app: gluu-upgrade
              name: upgrade-cm
            ---
            apiVersion: batch/v1
            kind: Job
            metadata:
              labels:
                app: gluu-upgrade
              name: gluu-upgrade-job
            spec:
              template:
                metadata:
                  annotations:
                     sidecar.istio.io/inject: "false"                      
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.2"
                    - --target
                    - "4.3"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.3.0_b1
                    name: gluu-upgrade-job                    
                    volumeMounts:
                    - mountPath: /etc/gluu/conf/couchbase_password
                      name: cb-pass
                      subPath: couchbase_password
                    - mountPath: /etc/certs/couchbase.crt
                      name: cb-crt
                      subPath: couchbase.crt
                  restartPolicy: Never
                  volumes:
                  - name: cb-pass
                    secret:
                      secretName: cb-pass #<-- Change this to the secret name holding couchbase pass
                  - name: cb-crt
                    secret:
                      secretName: cb-crt #<-- Change this to the secret name holding couchbase cert
            ```
            
        1. Add a new bucket  named `gluu_session`.
            
            === "Couchbase Operator v1"
            
                Add the following to `couchbase-cluster.yaml` under the buckets section:
                
                ```yaml
                  buckets:
                  - name: gluu_session   #DO NOT CHANGE THIS LINE
                    type: ephemeral
                    memoryQuota: 100 #<-- Change this if necessary
                    replicas: 1
                    ioPriority: high
                    evictionPolicy: nruEviction
                    conflictResolution: seqno
                    enableFlush: true
                    enableIndexReplica: false
                    compressionMode: passive
                ```
                
            === "Couchbase Operator v2"
            
                Apply the following yaml in the couchbase namespace:
                
                ```yaml
                cat <<EOF | kubectl apply -f -
                apiVersion: couchbase.com/v2
                kind: CouchbaseEphemeralBucket
                metadata:
                  name: gluu-session
                  labels:
                    cluster: gluu-couchbase
                spec:
                  name: gluu_session
                  memoryQuota: 100Mi <-- Change this if necessary
                  replicas: 1
                  ioPriority: high
                  evictionPolicy: nruEviction
                  conflictResolution: seqno
                  enableFlush: true
                  compressionMode: passive
                EOF
                ```
        1. Add a new user in couchbase  named `gluu`.
            
            === "Couchbase Operator v1"
            
                1. Inside the Couchbase UI create a group by going to `Security` --> `ADD GROUP` and call that `gluu-group`  and add `query_select`, `query_insert`, `query_update` and `query_delete` to gluu buckets `gluu`, `gluu_session`, `gluu_token`, `gluu_cache` and `gluu_site`.

                1. Inside the Couchbase UI create a user by going to `Security` --> `ADD USER` and call that user `gluu` and choose a good password and remember that as you will need it later. Assign the group `gluu-group`  which was create in the previous step to that user.
                           
            === "Couchbase Operator v2"
                
                1.  Create a secret that will hold `gluu` password in the couchbase namespace:
                
                ```bash
                kubectl create secret generic gluu-couchbase-user-password --from-literal=password=P@ssw0rd --namespace cbns
                ```
                
                1.  Apply the following yaml in the couchbase namespace:
                
                ```yaml
                cat <<EOF | kubectl apply -f -
                apiVersion: couchbase.com/v2
                kind: CouchbaseGroup
                metadata:
                  name: gluu-group
                  labels:
                    cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                spec:
                  roles:
                  - name: query_select
                    bucket: gluu
                  - name: query_select
                    bucket: gluu_site
                  - name: query_select
                    bucket: gluu_user
                  - name: query_select
                    bucket: gluu_cache
                  - name: query_select
                    bucket: gluu_token
                  - name: query_select
                    bucket: gluu_session
                
                  - name: query_update
                    bucket: gluu
                  - name: query_update
                    bucket: gluu_site
                  - name: query_update
                    bucket: gluu_user
                  - name: query_update
                    bucket: gluu_cache
                  - name: query_update
                    bucket: gluu_token
                  - name: query_update
                    bucket: gluu_session
                
                  - name: query_insert
                    bucket: gluu
                  - name: query_insert
                    bucket: gluu_site
                  - name: query_insert
                    bucket: gluu_user
                  - name: query_insert
                    bucket: gluu_cache
                  - name: query_insert
                    bucket: gluu_token
                  - name: query_insert
                    bucket: gluu_session
                
                  - name: query_delete
                    bucket: gluu
                  - name: query_delete
                    bucket: gluu_site
                  - name: query_delete
                    bucket: gluu_user
                  - name: query_delete
                    bucket: gluu_cache
                  - name: query_delete
                    bucket: gluu_token
                  - name: query_delete
                    bucket: gluu_session
                ---
                apiVersion: couchbase.com/v2
                kind: CouchbaseRoleBinding
                metadata:
                  name: gluu-role-binding
                spec:
                  subjects:
                  - kind: CouchbaseUser
                    name: gluu
                  roleRef:
                    kind: CouchbaseGroup
                    name: gluu-group
                ---
                apiVersion: couchbase.com/v2
                kind: CouchbaseUser
                metadata:
                  name: gluu
                  labels:
                    cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                spec:
                  fullName: "Gluu Cloud Native"
                  authDomain: local
                  authSecret: gluu-couchbase-user-password
                EOF
                ```
                                    
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.3 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.3/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.3/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.2 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
            
            Go over your `values.yaml` and make sure it reflects all current information. Forexample, make sure your couchbase url and crt are filled and correct. Also make sure that your couchbase user and password are the new ones which you created in a previous step,  and that the couchbase superuser and superuser password are filled correctly.
            
            Go over your `values.yaml` and make sure it reflects all current information. Forexample, make sure your couchbase url and crt are filled and correct. Also make sure that your couchbase user and password are the new ones which you created in a previous step,  and that the couchbase superuser and superuser password are filled correctly.

        1.  Inside `values.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
            
        1.  Create configmap for `101-ox.ldif` file.
        
            ```bash
            kubectl -n <gluu-namespace> create -f https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/v1.2.6/pygluu/kubernetes/templates/ldap/base/101-ox.yaml
            ```
            
        1.  Delete `oxAuthExpiration` index
        
            ```bash
            kubectl exec -ti gluu-opendj-0 -n <gluu-namespace> -- /opt/opendj/bin/dsconfig delete-backend-index --backend-name userRoot --index-name oxAuthExpiration --hostName 0.0.0.0 --port 4444 --bindDN 'cn=Directory Manager' --trustAll -f
            ```
            
        1.  Mount 101-ox.ldif in opendj-pods. Open opendj yaml or edit the statefulset directly `kubectl edit statefulset opendj -n gluu`
        
            ```yaml
              volumes:
              - name: ox-ldif-cm
                configMap:
                  name: oxldif
              containers:
                image: gluufederation/opendj:4.3.0_b1
                ...
                ...
                volumeMounts:
                - name: ox-ldif-cm
                  mountPath: /opt/opendj/config/schema/101-ox.ldif
                  subPath: 101-ox.ldif
        
            ```
                    
        1. Apply `upgrade.yaml`
        
            ```bash
            kubectl create -f upgrade.yaml -n <gluu-namespace>
            ```
           
            Wait until upgrade job is finished and tail the logs of the upgrade pod.
           
        1.  Run upgrade `Helm`
        
            ```bash
            helm upgrade <release-name> . -f ./values.yaml -n <namespace>   
            ``` 


    #### Kustomize - Depreciated
    
    - Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.3/README.md#build-pygluu-kubernetespyz-manually).
    
    - Move your  `settings.json` that was used in installing 4.2 next to `./pygluu-kubernetes.pyz`. 
    
        === "LDAP"
    
            -  Run :
            
                ```bash
                ./pygluu-kubernetes.pyz upgrade
                ```
     
        === "Couchbase | Hybrid"
        
            !!! Note
                The upgrade method has no means of installing couchbase. You may be prompted for couchbase related settings, but that is only to update your current or new settings.json.        
             
            1. Add a new bucket  named `gluu_session`.
            
                === "Couchbase Operator v1"
                
                    If you are using a custom `couchbase-cluster.yaml` that means that `COUCHBASE_CLUSTER_FILE_OVERRIDE` is set to `Y` inside settings.json. We advice you upgrade to the new couchbase operator and couchbase-server `6.6.0`. If you stick with the current operator please create two empty files `couchbase-buckets.yaml` and `couchbase-ephemeral-buckets.yaml` next to your custom `couchbase-cluster.yaml`.
    
                    Add the following to `couchbase-cluster.yaml` under the buckets section:
                    
                    ```yaml
                      buckets:
                      - name: gluu_session   #DO NOT CHANGE THIS LINE
                        type: ephemeral
                        memoryQuota: 100 #<-- Change this if necessary
                        replicas: 1
                        ioPriority: high
                        evictionPolicy: nruEviction
                        conflictResolution: seqno
                        enableFlush: true
                        enableIndexReplica: false
                        compressionMode: passive
                    ```
                    
                === "Couchbase Operator v2"
                
                    Apply the following yaml in the couchbase namespace:
                    
                    ```yaml
                    cat <<EOF | kubectl apply -f -
                    apiVersion: couchbase.com/v2
                    kind: CouchbaseEphemeralBucket
                    metadata:
                      name: gluu-session
                      labels:
                        cluster: gluu-couchbase
                    spec:
                      name: gluu_session
                      memoryQuota: 100Mi #<-- Change this if necessary
                      replicas: 1
                      ioPriority: high
                      evictionPolicy: nruEviction
                      conflictResolution: seqno
                      enableFlush: true
                      compressionMode: passive
                    EOF
                    ```
                    
            1. Add a new user in couchbase  named `gluu`.
                
                === "Couchbase Operator v1"
                
                    1. Inside the Couchbase UI create a group by going to `Security` --> `ADD GROUP` and call that `gluu-group`  and add `query_select`, `query_insert`, `query_update` and `query_delete` to gluu buckets `gluu`, `gluu_session`, `gluu_token`, `gluu_cache` and `gluu_site`.
    
                    1. Inside the Couchbase UI create a user by going to `Security` --> `ADD USER` and call that user `gluu` and choose a good password and remember that as you will be prompted for it later. Remember this is not the superuser password i.e admin. Assign the group `gluu-group`  which was create in the previous step to that user.
                                    
                === "Couchbase Operator v2"
                    
                    1.  Create a secret that will hold `gluu` password in the couchbase namespace:
                    
                    ```bash
                    kubectl create secret generic gluu-couchbase-user-password --from-literal=password=P@ssw0rd --namespace cbns
                    ```
                    
                    1.  Apply the following yaml in the couchbase namespace:
                    
                    ```yaml
                    cat <<EOF | kubectl apply -f -
                    apiVersion: couchbase.com/v2
                    kind: CouchbaseGroup
                    metadata:
                      name: gluu-group
                      labels:
                        cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                    spec:
                      roles:
                      - name: query_select
                        bucket: gluu
                      - name: query_select
                        bucket: gluu_site
                      - name: query_select
                        bucket: gluu_user
                      - name: query_select
                        bucket: gluu_cache
                      - name: query_select
                        bucket: gluu_token
                      - name: query_select
                        bucket: gluu_session
                    
                      - name: query_update
                        bucket: gluu
                      - name: query_update
                        bucket: gluu_site
                      - name: query_update
                        bucket: gluu_user
                      - name: query_update
                        bucket: gluu_cache
                      - name: query_update
                        bucket: gluu_token
                      - name: query_update
                        bucket: gluu_session
                    
                      - name: query_insert
                        bucket: gluu
                      - name: query_insert
                        bucket: gluu_site
                      - name: query_insert
                        bucket: gluu_user
                      - name: query_insert
                        bucket: gluu_cache
                      - name: query_insert
                        bucket: gluu_token
                      - name: query_insert
                        bucket: gluu_session
                    
                      - name: query_delete
                        bucket: gluu
                      - name: query_delete
                        bucket: gluu_site
                      - name: query_delete
                        bucket: gluu_user
                      - name: query_delete
                        bucket: gluu_cache
                      - name: query_delete
                        bucket: gluu_token
                      - name: query_delete
                        bucket: gluu_session
                    ---
                    apiVersion: couchbase.com/v2
                    kind: CouchbaseRoleBinding
                    metadata:
                      name: gluu-role-binding
                    spec:
                      subjects:
                      - kind: CouchbaseUser
                        name: gluu
                      roleRef:
                        kind: CouchbaseGroup
                        name: gluu-group
                    ---
                    apiVersion: couchbase.com/v2
                    kind: CouchbaseUser
                    metadata:
                      name: gluu
                      labels:
                        cluster: CLUSTERNAME # <--- change this to your cluster name i.e cbgluu
                    spec:
                      fullName: "Gluu Cloud Native"
                      authDomain: local
                      authSecret: gluu-couchbase-user-password
                    EOF
                    ```
                              
            1.  Run :
            
                 ```bash
                 ./pygluu-kubernetes.pyz upgrade
                 ```
                 
            !!! Note
                There is new health check which may result in kubernetes rejecting the update of statefulsets describing that there are mulitple healthchecks defined. This does not affect the upgrade process itself. This is often only seen in oxtrust and hence  after the confirmation that most  services are up you may have to `kubectl delete -f oxtrust.yaml` and re-apply `kubectl apply -f oxtrust.yaml` to re-initiate the statefulset.
     
             
    ### Exporting Data
    
    !!! Note
        This step is not needed.
    
    
    1.  Make sure to backup existing LDAP data
    
    1.  Set environment variable as a placeholder for LDAP server password (for later use):
    
        ```sh
        export LDAP_PASSWD=YOUR_PASSWORD_HERE
        ```
    
    1.  Assuming that existing LDAP container called `ldap` has data, export data from each backend:
    
        1.  Export `o=gluu`
    
            ```sh
            kubectl exec -ti ldap /opt/opendj/bin/ldapsearch \
                -Z \
                -X \
                -D "cn=directory manager" \
                -w $LDAP_PASSWD \
                -p 1636 \
                -b "o=gluu" \
                -s sub \
                'objectClass=*' > gluu.ldif
            ```
    
        1.  Export `o=site`
    
            ```sh
            kubectl exec -ti ldap /opt/opendj/bin/ldapsearch \
                -Z \
                -X \
                -D "cn=directory manager" \
                -w $LDAP_PASSWD \
                -p 1636 \
                -b "o=site" \
                -s sub \
                'objectClass=*' > site.ldif
            ```
    
        1.  Export `o=metric`
    
            ```sh
            kubectl exec -ti ldap /opt/opendj/bin/ldapsearch \
                -Z \
                -X \
                -D "cn=directory manager" \
                -w $LDAP_PASSWD \
                -p 1636 \
                -b "o=metric" \
                -s sub \
                'objectClass=*' > metric.ldif
            ```
    
    1.  Unset `LDAP_PASSWD` environment variable
