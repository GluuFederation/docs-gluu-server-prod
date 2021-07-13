# Gluu Server Backup

The Gluu Server should be backed up frequently--**we recommend at least one daily and one weekly backup of Gluu's data and/or VM.** 

There are multiple methods for backing up the Gluu Server. A few recommended strategies are provided below.

=== "Community Edition Snapshot Backup"
    
    In the event of a production outage, a proper snapshot of the last working condition will help rapidly restore service. 
    
    Most platform virtualization software and cloud vendors have snapshot backup features. For instance, Digital Ocean has Live Snapshot and Droplet Snapshot; VMWare has Snapshot Manager, etc. 
    
    Snaphots should be taken for all Gluu environments (e.g. Prod, Dev, QA, etc.) and tested periodically to confirm consistency and integrity. 
    
    ## Tarball Method
    All Gluu Server files live in a single folder: `/opt`. The entire Gluu Server CE `chroot` folder can be archived using the `tar` command: 
    
    1. Stop the server: `service gluu-server stop` or `/sbin/gluu-serverd stop`
        
    1. Use `tar` to take a backup: `tar cvf gluu40-backup.tar /opt/gluu-server/`
        
    1. Start the server again: `service gluu-server start` or `/sbin/gluu-serverd start`
    
    ## LDIF Data Backup
    From time to time (daily or weekly), the LDAP database should be exported in a standard LDIF format. Having the data in plain text offers some options for recovery that are not possible with a binary backup. 
    
    Instructions are provided below for exporting OpenDJ data. The below instructions address situations where unused and expired cache and session related entries are piling and causing issues with functionality. Read more about this [issue](https://www.gluu.org/blog/managing-cache-in-the-gluu-server/).
    
    ### OpenDJ 
    
    Errors that this may help fix include but are not restricted to: 
    
    - Out of Memory
    
    If your Gluu Server is backed by OpenDJ, follow these steps to backup your data:
    
    1. First check your cache entries by running the following command:
    
        ```bash
        /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' 'oxAuthGrantId=*' dn | grep 'dn:' | wc -l
        ```
        
    1. Dump the data as LDIF
    
        - Log in to root:
            
        ```bash
        sudo su -
        ```
    
        - Log in to Gluu-Server:   
    
        ```bash
        service gluu-server login
        ```
        
        or
        
        ```bash
        /sbin/gluu-serverd login
        ```
    
        - [Stop](./services.md#stop) the `identity`, `oxauth` and `opendj` services
    
        - If you are moving to a new LDAP, copy over your schema files from the following directory. Otherwise simply copy it for backup:
    
        ```bash
        /opt/opendj/config/schema/
        ```
    
        - Now export the LDIF and save it somewhere safe. You will not be importing this if you choose to apply any filters as below:
    
        ```bash
        /opt/opendj/bin/export-ldif -n userRoot --offline -l exactdatabackup_date.ldif
        ```
    
        - Now exclude `oxAuthGrantId` so the command becomes:
    
        ```bash
        /opt/opendj/bin/export-ldif -n userRoot --offline -l yourdata_withoutoxAuthGrantId.ldif --includeFilter '(!(oxAuthGrantId=*))'
        ```
    
        - You may also wish to exclude `oxMetric` so the command becomes:
    
        ```bash
        /opt/opendj/bin/export-ldif -n userRoot --offline -l yourdata_withoutGrantIdMetic.ldif --includeFilter '(&(!(oxAuthGrantId=*))(!			(objectClass=oxMetric)))'
        ```
    
    1. Now, **only if needed**, rebuild indexes:
    
        - Check status of indexes: 
    
        ```bash
        /opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
        ```
    
        Take note of all indexes that need to be rebuilt. **If no indexing is needed, move on to step 4.**
    
        - [Start](./services.md#start) the `opendj` service
    
        - Build backend index for all indexes that need it accoring to previous status command, change passoword `-w` and index name accordingly. This command has to be run for every index separately: 
    
        ```bash
        /opt/opendj/bin/dsconfig create-backend-index --port 4444 --hostname localhost --bindDN "cn=directory manager" -w password --backend-name userRoot --index-name iname --set index-type:equality --set index-entry-limit:4000 --trustAll --no-prompt
        ```
    
        - [Stop](./services.md#stop) the `opendj` service
    
        - Rebuild the indexes as needed, here are examples : 
    
        ```bash
        /opt/opendj/bin/rebuild-index --baseDN o=gluu --index iname
        /opt/opendj/bin/rebuild-index --baseDN o=gluu --index uid
        /opt/opendj/bin/rebuild-index --baseDN o=gluu --index mail
        ```
    
        - Check status again :
    
        ```bash
        /opt/opendj/bin/backendstat show-index-status --backendID userRoot --baseDN o=gluu
        ```
    
        - Verify indexes: 
    
        ```bash
        /opt/opendj/bin/verify-index --baseDN o=gluu --countErrors
        ```
    
    1. Next import your previously exported LDIF. Here, we are importing without  `oxAuthGrantId` . 
        
    !!! Note
        You may import the exact export of your ldap `exactdatabackup_date.ldif`.Do not import your exact copy of your LDIF if you are following instructions to to clean your cache entries
        
        ```bash
        /opt/opendj/bin/import-ldif -n userRoot --offline -l yourdata_withoutoxAuthGrantId.ldif
        ```
        
      If you moved to a new LDAP, copy back your schema files to this directory:
    
    ```bash
    /opt/opendj/config/schema/
    ```
        
    1. [Start](./services.md#start) the `identity`, `oxauth` and `opendj` services
    
    1. Finally, verify the cache entries have been removed:
    
        /opt/opendj/bin/ldapsearch -h localhost -p 1636 -Z -X -D "cn=directory manager" -w <password> -b 'o=gluu' -T 		'oxAuthGrantId=*' dn | grep 'dn:' | wc –l
    
    You should be done and everything should be working perfectly. You may notice your Gluu Server responding slower than before. That is expected -- your LDAP is adjusting to the new data, and indexing might be in process. Give it some time and it should be back to normal.

=== "Cloud Native instructions"

    !!!warning
        This section is under construction. 
    
    ## Overview
    
    This guide introduces how to backup data and restore from a backup file.
    
    === "Couchbase"
        
        ### Install backup strategy
        
        A typical installation of Gluu using [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases)  will automatiically install a backup strategy that will backup Couchbase every 5 mins to a persistent volume. However, the Couchbase backup can be setup manually:
        
        1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).
        
        1.  Run :
        
             ```bash
             ./pygluu-kubernetes.pyz install-couchbase-backup
             ```
             
        !!! Note
            `./pygluu-kubernetes.pyz install-couchbase-backup` will not install couchbase.
        
        ### Uninstall backup strategy
        
        A file named `couchbase-backup.yaml` will have been generated during installation of backup strategy. Use that as follows to remove the backup strategy:
        
        ```bash
        kubectl delete -f ./couchbase-backup.yaml
        ```
        
        ### Restore from backup
        
        Please save a copy of the configurations to a file.
        
        ```bash
        kubectl get cm gluu -n <Gluu-namespace> -o yaml > configs-<date>.yaml
        kubectl get secret gluu -n <Gluu-namespace> -o yaml > secrets-<date>.yaml
        ```
        !!! Note
            An existing Gluu setup must exist for this to work. Please do not attempt to delete any resources and be very careful in handling Gluu configurations and secrets.
        
        #### Couchbase restore step
        
        1.  Install a new Couchbase if needed.
        
            ```bash
            ./pygluu-kubernetes.pyz install-couchbase
            ```
        
        1.  Create a pod definition file called `restore-cb-pod.yaml` and paste the below yaml changing the `volumes`, `volumeMounts` and `namespace` if they are different. 
        
            !!! Note
                `./pygluu-kubernetes.pyz install-couchbase-backup` uses the `volumes` and `volumeMounts` as seen in the yaml below
                
            ```yaml
            apiVersion: v1
            kind: Pod
            metadata:
              name: restore-node
              namespace: cbns
            spec:  # specification of the pod's contents
              containers:
                - name: restore-pod
                  image: couchbase/server:enterprise-6.5.0
                  # Just spin & wait forever
                  command: [ "/bin/bash", "-c", "--" ]
                  args: [ "while true; do sleep 30; done;" ]
                  volumeMounts:
                    - name: "couchbase-cluster-backup-volume"
                      mountPath: "/backups"
              volumes:
                - name: couchbase-cluster-backup-volume
                  persistentVolumeClaim:
                    claimName: backup-pvc
              restartPolicy: Never
            ```
        
        1.  Apply `restore-cb-pod.yaml`.
        
            ```bash
            kubectl apply -f  restore-cb-pod.yaml
            ```
            
        1.  Access the `restore-node` pod.
        
            ```bash
            kubectl exec -it restore-node -n cbns -- /bin/bash
            ```
         
        1.  Choose the backup of choice
        
            ```bash
            cbbackupmgr list --archive /backups --repo couchbase
            ```
            
            We will choose the oldest we received from the command above `2020-02-20T10_05_13.781131773Z`
            
        1.  Preform the restore using the `cbbackupmgr` command.
        
            ```bash
            cbbackupmgr restore --archive /backups --repo couchbase --cluster cbgluu.cbns.svc.cluster.local --username admin --password passsword --start 2020-02-20T10_05_13.781131773Z --end 2020-02-20T10_05_13.781131773Z
            ```
            
            Learn more about  [`cbbackupmgr`](https://docs.couchbase.com/server/current/backup-restore/cbbackupmgr-restore.html) command and its options.
            
        1. Once done delete the `restore-node` pod.
        
            ```bash
            kubectl delete -f restore-cb-pod.yaml -n cbns
            ```
            
        #### Gluu restore step
        
        === "Kustomize - Depreciated"
        
            1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).
            
            1.  Run :
            
                 ```bash
                 ./pygluu-kubernetes.pyz restore
                 ```

        === "Helm"
                    
            1. Save any custom files injected and used across `Gluu` services. These files might likely be save in [Jackrabbit](https://gluu.org/docs/gluu-server/latest/installation-guide/install-kubernetes/#working-with-jackrabbit).
            
            1. Save important gluu `ConfigMap`s:
            
                ```bash
                kubectl get cm gluu -n gluu -o yaml > gluu_main_cm.yaml && \
                kubectl get cm gluu-config-cm -n gluu -o yaml > gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-config-gen-json-file -n gluu -o yaml >> gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-config-tls-script -n gluu -o yaml >> gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-updatelbip -n gluu -o yaml >> gluu_cms.yaml
                ```
            
            1. Save important gluu `Secret`s:
            
                ```bash
                kubectl get secret gluu -n gluu -o yaml > gluu_main_secret.yaml && \
                kubectl get secret tls-certificate -n gluu -o yaml > gluu_secrets.yaml && \
                echo "---" >> gluu_secrets.yaml && \
                kubectl get secret gluu-jackrabbit-admin-pass -n gluu -o yaml >> gluu_secrets.yaml && \
                echo "---" >> gluu_secrets.yaml && \
                kubectl get secret gluu-jackrabbit-postgres-pass -n gluu -o yaml >> gluu_secrets.yaml
                ```        
        
            
            1. If this is a restore it likely means the helm deployment of Gluu is currupt. Delete the helm deployment of Gluu in preperation for a new fresh one:
            
                ```bash
                helm delete <release-name> -n <gluu-namespace>
                ```
            
            1. Create `gluu` `Secret` and `ConfigMap` from backup saved previosuly:
            
               ```bash
               kubectl create -f gluu_main_secret.yaml && kubectl create -f gluu_main_cm.yaml
               ```
            
            1. Run the install command for helm:
            
                ```bash
                helm install <release-name> -f ./values.yaml . -n <gluu-namespace>
                ```
                
            1. Preform a rolling update of each service, forexample :             
            
               ```bash
               kubectl rollout restart gluu-deployment -n gluu
               ```
               
    === "OpenDJ"    
    
        ### Install backup strategy
        
        A typical installation of Gluu using [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases)  will automatiically install a backup strategy that will backup opendj / wren:ds every 10 mins `/opt/opendj/ldif`. However, the couchbase backup can be setup manually:
        
        === "Kustomize - Depreciated"
        
            1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).
            
            1.  Run :
            
                 ```bash
                 ./pygluu-kubernetes.pyz install-ldap-backup
                 ```
                 
        === "Helm"
    
            1.  Run :
            
                 ```bash
                 git clone --single-branch --branch 4.3 https://github.com/GluuFederation/cloud-native-edition.git
                 cd pygluu/kubernetes/templates/helm/ldap-backup
                 ```
                 
            1. Edit the main values file to integrate with Gluu:
            
                ```bash
                vi values.yaml      
                ```
            
            1. Once done install the ldap-backup chart
            
                ```bash
                helm install <release-name> -f ./values.yaml . --namespace=<gluu-namespace>
                ```
                
        !!! Note
            Up to 6 backups will be stored at `/opt/opendj/ldif` on the running `opendj` pod. The backups will carry the name `backup-0.ldif` to `backup-5.ldif` and will be overwritten to save data.
        
        #### Uninstall backup strategy
        
        A file named `ldap-backup.yaml` will have been generated during installation of backup strategy. Use that as follows to remove the backup strategy:
        
        ```bash
        kubectl delete -f ./couchbase-backup.yaml
        ```
        
        ### Restore from backup
        
        !!! Note
            An existing Gluu setup must exist for this to work. Please do not attempt to delete any resources and be very careful in handling Gluu configurations and secrets.
        
        #### OpenDJ / Wren:DS restore step
        
        1.  Opendj volume attached should carry the backups at `/opt/opendj/ldif`
        
        1. If this is a fresh installation , attach the older volume to the new pod.
        
        1.  Access the opendj pod.
        
            ```bash
            kubectl exec -ti opendj-0 -n gluu /bin/sh
            ```
            
        1.  Choose the backup of choice and rename it to `backup-this-copy.ldif`. The `pygluu-kubernetes.pyz` will preform the import.
        
            ```bash
            ls /opt/opendj/ldif
            cd /opt/opendj/ldif
            cp backup-1.ldif backup-this-copy.ldif
            ```
            
        === "Kustomize - Depreciated"
                
            1.  Run :
            
                 ```bash
                 ./pygluu-kubernetes.pyz restore
                 ```
                 
        === "Helm"
        
            1. Save a copy of the ldif backups. The backups should already be on persistence disks but for ease of access please copy these ldifs to a secure location to be used in further steps. 
            
            1. Save any custom files injected and used across `Gluu` services. These files might likely be save in [Jackrabbit](https://gluu.org/docs/gluu-server/latest/installation-guide/install-kubernetes/#working-with-jackrabbit).
            
            1. Save important gluu `ConfigMap`s:
            
                ```bash
                kubectl get cm gluu -n gluu -o yaml > gluu_main_cm.yaml && \
                kubectl get cm gluu-config-cm -n gluu -o yaml > gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-config-gen-json-file -n gluu -o yaml >> gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-config-tls-script -n gluu -o yaml >> gluu_cms.yaml && \
                echo "---" >> gluu_cms.yaml && \
                kubectl get cm gluu-updatelbip -n gluu -o yaml >> gluu_cms.yaml
                ```
            
            1. Save important gluu `Secret`s:
            
                ```bash
                kubectl get secret gluu -n gluu -o yaml > gluu_main_secret.yaml && \
                kubectl get secret tls-certificate -n gluu -o yaml > gluu_secrets.yaml && \
                echo "---" >> gluu_secrets.yaml && \
                kubectl get secret gluu-jackrabbit-admin-pass -n gluu -o yaml >> gluu_secrets.yaml && \
                echo "---" >> gluu_secrets.yaml && \
                kubectl get secret gluu-jackrabbit-postgres-pass -n gluu -o yaml >> gluu_secrets.yaml
                ```        
        
            
            1. If this is a restore it likely means the helm deployment of Gluu is currupt. Delete the helm deployment of Gluu in preperation for a new fresh one:
            
                ```bash
                helm delete <release-name> -n <gluu-namespace>
                ```
            
            1. Create `gluu` `Secret` and `ConfigMap` from backup saved previosuly:
            
               ```bash
               kubectl create -f gluu_main_secret.yaml && kubectl create -f gluu_main_cm.yaml
               ```
            
            1. Run the install command for helm:
            
                ```bash
                helm install <release-name> -f ./values.yaml . -n <gluu-namespace>
                ```
                
            1. Move the backup ldifs to the new opendj pod at `/opt/opendj/ldif`
            
            1.  Choose the backup of choice and run the command below:
            
                ```bash
                /opt/opendj/bin/import-ldif --hostname localhost --port 4444 --bindDN "cn=Directory manager" --backendID userRoot --trustAll --ldifFile /opt/opendj/ldif/backup-4.ldif --bindPassword "<Password>"
                ```
            
            1. Preform a rolling update of each service, forexample :             
            
               ```bash
               kubectl rollout restart gluu-deployment -n gluu
               ```
            
