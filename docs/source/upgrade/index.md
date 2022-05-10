# Upgrade to Gluu Server 4.4

=== "Community Edition"
    
    ## Overview
    The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.4. 
    
    ### Pre-requisites
    
    - Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
    - Upgrades should always be thoroughly scoped and tested on a development environment *first*.
    - This upgrade process only upgrades versions 4.0.x through 4.3.1. To upgrade from a previous version, first [upgrade to 4.0](https://gluu.org/docs/gluu-server/4.0/upgrade/).
        
    - Upgrade script runs on Python 3. You need to install Python 3 before running the script.
        * On CentoOS/RHEL: `yum install -y python3`
        * On Ubuntu/Debian: `apt-get update && apt-get install -y python3`
    
    
    #### Online Upgrade from 4.x to 4.4.0
  
    The upgrade script downloads all needed software and applications from the internet. You can perform an online upgrade by following these steps:
    
    * Download the upgrade script
    
    ```
    wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.4.0/upg4xto440.py
    ```
    
    * Execute the script:
    
    ```
    python3 upg4xto431.py
    ```
    
    Your upgrade directory will be the `/opt/upd/4.4.0/dist`. The script will create these sub directories: `app`, `gluu`, and `tmp`. It also downloads latest setup files to `/install/community_edition_setup_4.4.0`.

    #### Offline Upgrade from 4.x to 4.4.0
    
    If your machine is not open to public internet, you can download self extracting upgrade script form https://repo.gluu.org/upd/4.4-0.upg.run and you can run inside Gluu CE container as

    ```
    sh 4.4-0.upg.run
    ```
    
    The script extracts contents to `/opt/upd/4.4.0/dist`, and writes latest setup files to `/install/community_edition_setup_4.4.0`
    
=== "Cloud Native Edition"
 
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
                    - "4.3"
                    - --target
                    - "4.4"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.4.0-01
                    name: gluu-upgrade-job
                  restartPolicy: Never
            ```
            
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.4 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. Also make sure your current `values.yaml` other options are moved correctly to the new values.yaml.
            Move old `settings.json` that was used in 4.3 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
            
            Go over your `values.yaml` and make sure it reflects all current information.
            
        1.  Inside `values.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
        
        1.  Create configmap for `101-ox.ldif` file.
        
            ```bash
            kubectl -n <gluu-namespace> create -f https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/ldap/101-ox.yaml
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
                image: gluufederation/opendj:4.4.0-1
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
                    - "4.3"
                    - --target
                    - "4.4"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.4.0-1
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

                                
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.4 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.3 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
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
                    - "4.3"
                    - --target
                    - "4.4"
                    envFrom:
                    - configMapRef:
                        name: upgrade-cm
                    image: gluufederation/upgrade:4.4.0-1
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
                                    
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.4 https://github.com/GluuFederation/cloud-native-edition && cd pygluu/kubernetes/templates/helm/gluu
            ```
                        
        1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.4/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 
            Move old `settings.json` that was used in 4.3 installation into the same directory `pygluu-kubernetes` exists in and execute the following command :
            
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
                image: gluufederation/opendj:4.4.0-01
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
