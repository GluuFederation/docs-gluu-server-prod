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

    
    ## Overview
    
    This guide introduces how to backup and restore `gluu` deployment on Kubernetes.
    
    ## Persistence Backup and Restore

    === "Couchbase"   
         You can follow the Couchbase [docs](https://docs.couchbase.com/operator/current/howto-backup.html) to [backup](https://docs.couchbase.com/operator/current/howto-backup.html#overview) and [restore](https://docs.couchbase.com/operator/current/howto-backup.html#restoring-from-a-backup) your persistence.

    === "OpenDJ"    
        !!! Note
            Up to 6 backups will be stored at `/opt/opendj/ldif` on the running `opendj` pod. The backups will carry the name `backup-0.ldif` to `backup-5.ldif` and will be overwritten to save te data.

        ### Automatic backup 
        A typical installation of Gluu using `pygluu` or `helm` will automatically backup opendj at `/opt/opendj/ldif`.

        
        ### Manual backup
        Opendj backup can also be configured manually:
                
                 
        1. Edit your [override.yaml](https://github.com/GluuFederation/cloud-native-edition/blob/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml) file and set `opendj.backup.enabled` to true and `opendj.backup.enabled.cronJobSchedule` to the [schedule](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#schedule-syntax) of your choice. 
        
        1. Run `helm install` or `helm upgrade` if `Gluu` is already installed
        
            ```bash
            helm upgrade <helm-release-name> gluu/gluu -f override.yaml -n <namespace>
            ```
        1. Save any custom files injected and used across `Gluu` services. These files might likely be saved in [Jackrabbit](https://gluu.org/docs/gluu-server/latest/installation-guide/install-kubernetes/#working-with-jackrabbit).    

        
        
        ### Opendj restore
        
        
        1.  Access the opendj pod:
        
            ```bash
            kubectl exec -it gluu-opendj-0 -n <namespace> -- /bin/sh
            ```
            
        1.  Let's assume the file you want to restore from is `/opt/opendj/ldif/backup-1.ldif`. Run this to perform the restore:
            ```bash
            /opt/opendj/bin/import-ldif --hostname localhost --port 4444 --bindDN "cn=Directory manager" --backendID userRoot --trustAll --ldifFile /opt/opendj/ldif/backup-1.ldif --bindPassword "<Password>"
            ```                     
            
    === "SQL"

        SQL databases backup and restore are a common feature whether in a User-managed or Cloud-Managed deployment.


        One way to *backup* your postgresql database for example:
        ```bash
        pg_dump dbname > dumpfile
        ```
        
        Restore the database using the generated `dumpfile`:
        ```bash
        psql dbname < dumpfile
        ```

    ## Configmaps and Secrets - Backup and Restore    

    ### Backup of Configmaps and Secrets    

    1.  Configmaps backup:
    ```bash
    kubectl get configmap gluu -n <namespace> -o yaml > configmap-backup.yaml
    ```

    2.  Secrets backup:
    ```bash
    kubectl get secret gluu -n <namespace> -o yaml > secret-backup.yaml
    ```

    3.  Get the user supplied values:

        Save the values.yaml that was used in the initial `gluu` installation using helm.

        In the event that the user supplied or override values yaml was lost, you can obtain it by executing the following command:
        ```bash
        helm get values <release name> -n <namespace>
        ```

    4.  Keep note of installed chart version:
    ```bash
    helm list -n <namespace>
    ```

    Keep note of the chart version. For example: `backup-chart-version`

    ### Restore of Configmaps and Secrets 
    !!! Note
        You have to restore your [Persistence](#persistence-backup-and-restore) before doing this step.

    1.  Create namespace
    ```bash
    kubectl create namespace <namespace>
    ```

    2.  Configmap restore:
    ```bash
    kubectl create -f configmap-backup.yaml
    ```

    3.  Secret restore:
    ```bash
    kubectl create -f secret-backup.yaml
    ```

    4.  Insall `gluu` using the override or user supplied values with the same chart version:

    ```bash
    helm install <release-name> gluu/gluu -f values.yaml --version=<backup-chart-version> -n <namespace>
    ```