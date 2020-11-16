# Upgrade to Gluu Server 4.2

=== "Community Edition"
    
    ## Overview
    The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.2. 
    
    ### Pre-requisites
    
    - Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
    - Upgrades should always be thoroughly scoped and tested on a development environment *first*.
    - This upgrade process only upgrades versions 4.0.x and 4.1.x. To upgrade from a previous version, first [upgrade to 4.0](https://gluu.org/docs/gluu-server/4.0/upgrade/).
    
    #### Online Upgrade from 4.x to 4.2
    
    !!! Note
        Upgrade script runs on Python 3. You need to install Python 3 before running the script.
        * On CentoOS/RHEL: `yum install -y python3`
        * On Ubuntu/Debian: `apt-get update && apt-get install -y python3`
    
    The upgrade script downloads all needed software and applications from the internet. You can perform an online upgrade by following these steps:
    
    * Download the upgrade script
    
    ```
    wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.2.0/upg4xto420.py
    ```
    
    * Execute the script:
    
    ```
    python3 upg4xto420.py
    ```
    
    Your upgrade directory will be the current directory. The script will create these directories: `app`, and `ces_current`, and writes Gluu cacerts.
    
    <!--
    ### Upgrading from 3.1.x to 4.2
    
    At this time, only Gluu Server version 3.1.x can be upgraded to version 4.2. The upgrade script works on CentOS 7, Ubuntu 16, and RedHat 7. Upgrade script performs the following steps:
    
    - Upgrades Java to Amazon Corretto. Extracts certificates from the existing Java keystore to `hostname_service.crt` in the upgrade directory. After upgrading Java, imports to keystore
    - Upgrades all Gluu WAR files, NodeJS, and Passport components
    - Transfers all data from LDAP to `gluu.ldif` in the upgrade directory
    - Upgrades to [WrenDS](https://github.com/WrenSecurity/wrends) (a community maintained fork of OpenDJ). If you are currently running OpenLDAP, it will be backed up and migrated to WrenDS
    - Processes `gluu.ldif` to convert the existing data set to the new model. Removes all inums. Depending on the data
    size, this step will take some time. Writes resulting data to `gluu_noinum.ldif`. Your current passport configuration
    will be moved to `gluuPassportConfiguration.json` for future reference
    - Imports `gluu_noinum.ldif` to newly installed WrenDS. Rejected and Skipped entries will be written to 
    `opendj_rejects.txt` and `opendj_skips.txt` to the upgrade directory
    - Upgrade script uses setup.py to updated the configuration. All activities will be logged to `setup/update.log` and
    `update_error.log`
    - All files will be backed up with `file_name.gluu-version-#~` where # is a consecutive number, unless backup is specified in
    another way.
    - Sets the OpenID Connect `claimsParameterSupported` property to `false` by default to ensure clients are unable to gather unwanted claims. If a client in use depends on this property, it can be set back to `true` in the JSON configuration.
    
    !!! Note
        If you are using custom schema:  
        (a) OpenDJ Users: Back up the schema file  
        (b) OpenLDAP users: Convert the schema according to [this guide](https://backstage.forgerock.com/docs/opendj/3.5/admin-guide/#chap-schema)  
        
        When the upgrade script prompts:  
        
        ```
        If you have custom ldap schema, add them now and press c  
        If you don't have any custom schema you can continue with pressing c
        ```
        
        Put the schema file in `/opt/opendj/config/schema/`
    
    
    There are two options to perform the upgrade (both methods work inside the container):
    
    #### Online Upgrade
    !!! Note
        Upgrade script runs on Python 3. You need to install Python 3 before running the script.
        * On CentoOS/RHEL: `yum install -y python3`
        * On Ubuntu/Debian: `apt-get update && apt-get install -y python3`
    
    The upgrade script downloads all needed software and applications from the internet. You can perform an online upgrade by following these steps:
    
    * Download the upgrade script
    
    ```
    wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.2.0/upg4xto420.py
    ```
    
    * Execute the script:
    
    ```
    python3 upg4xto420.py
    ```
    
    Your upgrade directory will be the current directory. The script will create these directories: `app`, and `ces_current`, and writes Gluu cacerts.
    
    #### Static Upgrade
    The static, self-extracting upgrade package contains all components for the upgrade. You still need an internet connection to install the libraries that are needed by the upgrade script. To perform a static upgrade, follow these steps:
    
    * Download the self-extracting package
    
    ```
    wget http:// ...... /4.2-upg.sh
    ```
    
    * Execute the script
    
    ```
    sh 4.2-upg.sh
    ```
    
    The upgrade directory will be `/opt/upd/4.2-upg`
    -->

=== "Cloud Native Edition"

    !!!warning
        This section is under construction. 
    
    ## Overview
    
    This guide introduces how to upgrade cloud native edition from one version to another.

    ### Upgrade
    
    #### Kustomize
    
    - Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).
    
    - Move your  `settings.json` that was used in installing 4.1 next to `./pygluu-kubernetes.pyz`. 
    
    === "LDAP"

        -  Run :
        
            ```bash
            ./pygluu-kubernetes.pyz upgrade
            ```

        !!! Note
            Compated to 4.1 , 4.2 has a centrialized `configMap` holding the necessary environment variables for all Gluu services. Hence, you will come to realize that the associated `configMaps` for each service that were defined previosuly such as `oxauth-cm` are no longer used. The upgrade process does not delete these unused `configMaps` as a rollout back to 4.1 might be needed. You may choose to discard these unused `configMaps` after full confirmation that your deployment fully functions. 
                     
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
            There is a new health check in 4.2 which may result in kubernetes rejecting the update of statefulsets describing that there are mulitple healthchecks defined. This does not affect the upgrade process itself. This is often only seen in oxtrust and hence  after the confirmation that most  services are up you may have to `kubectl delete -f oxtrust.yaml` and re-apply `kubectl apply -f oxtrust.yaml` to re-initiate the statefulset.

        !!! Note
            Compated to 4.1 , 4.2 has a centrialized `configMap` holding the necessary environment variables for all Gluu services. Hence, you will come to realize that the associated `configMaps` for each service that were defined previosuly such as `oxauth-cm` are no longer used. The upgrade process does not delete these unused `configMaps` as a rollout back to 4.1 might be needed. You may choose to discard these unused `configMaps` after full confirmation that your deployment fully functions.  
                         
             
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
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.1"
                    - --target
                    - "4.2"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.2.1_04
                    name: gluu-upgrade-job
                    # Enable the command section below if using istio
                    #command:
                    #  - tini
                    #  - -g
                    #  - --
                    #  - /bin/sh
                    #  - -c
                    #  - |
                    #      /app/scripts/entrypoint.sh
                    #      curl -X POST http://localhost:15020/quitquitquit
                  restartPolicy: Never
            ```
            
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.2 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. Also make sure your current `values.yaml` other options are moved correctly to the new values.yaml.
            Move old `settings.json` that was used in 4.1 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
            
            Go over your `values.yaml` and make sure it reflects all current information.
            
        1.  Inside `values.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
        
        1.  Create configmap for `101-ox.ldif` file.
        
            ```bash
            kubectl -n <gluu-namespace> create -f https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/ldap/base/101-ox.yaml
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
                image: gluufederation/opendj:4.2.1_02
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
            
        !!! Note
            Compated to 4.1 , 4.2 has a centrialized `configMap` holding the necessary environment variables for all Gluu services. Hence, you will come to realize that the associated `configMaps` for each service that were defined previosuly such as `oxauth-cm` are no longer used. The upgrade process does not delete these unused `configMaps` as a rollout back to 4.1 might be needed. You may choose to discard these unused `configMaps` after full confirmation that your deployment fully functions.            
        
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
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.1"
                    - --target
                    - "4.2"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.2.1_04
                    name: gluu-upgrade-job
                    # Enable the command section below if using istio
                    #command:
                    #  - tini
                    #  - -g
                    #  - --
                    #  - /bin/sh
                    #  - -c
                    #  - |
                    #      /app/scripts/entrypoint.sh
                    #      curl -X POST http://localhost:15020/quitquitquit                    
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
            git clone --recursive --depth 1 --branch 4.2 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.1 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
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
            
        !!! Note
            Compated to 4.1 , 4.2 has a centrialized `configMap` holding the necessary environment variables for all Gluu services. Hence, you will come to realize that the associated `configMaps` for each service that were defined previosuly such as `oxauth-cm` are no longer used. The upgrade process does not delete these unused `configMaps` as a rollout back to 4.1 might be needed. You may choose to discard these unused `configMaps` after full confirmation that your deployment fully functions.             

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
                  labels:
                    app: gluu-upgrade
                spec:
                  containers:
                  - args:
                    - --source
                    - "4.1"
                    - --target
                    - "4.2"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.2.1_04
                    name: gluu-upgrade-job
                    # Enable the command section below if using istio
                    #command:
                    #  - tini
                    #  - -g
                    #  - --
                    #  - /bin/sh
                    #  - -c
                    #  - |
                    #      /app/scripts/entrypoint.sh
                    #      curl -X POST http://localhost:15020/quitquitquit                    
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
            git clone --recursive --depth 1 --branch 4.2 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.2/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.1 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
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
                image: gluufederation/opendj:4.2.1_02
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

        !!! Note
            Compated to 4.1 , 4.2 has a centrialized `configMap` holding the necessary environment variables for all Gluu services. Hence, you will come to realize that the associated `configMaps` for each service that were defined previosuly such as `oxauth-cm` are no longer used. The upgrade process does not delete these unused `configMaps` as a rollout back to 4.1 might be needed. You may choose to discard these unused `configMaps` after full confirmation that your deployment fully functions. 
    
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
        
