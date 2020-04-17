# Upgrade to Gluu Server 4.1

## Overview
The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.1. 

## Prerequisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

## Upgrade with Scripts

Community Edition version 4.1 must be upgraded from version 4.0.x. Explanations of what actions the upgrade script performs are included [below](#40-upgrade-script-details).

### Upgrade 3.1.x to 4.0

The upgrade script can download all needed software and applications from the internet. [Skip this step](#upgrade-40-to-41) if already using 4.0. You can perform an online upgrade by following these steps:

* Create directory
```
# mkdir /root/upg40
```

* Download the upgrade script
```
# wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.0/update.py -O /root/upg40/update.py
```

* Execute the script with `-o` argument
```
# cd /root/upg40
# python update.py -o
```

Your upgrade directory will be the current directory. The script will create these directories: `app`, `war`, `temp`, `setup`

When the upgrade script prompts:  
    
    ```
    If you have custom ldap schema, add them now and press c  
    If you don't have any custom schema you can continue with pressing c
    ```
    
Put the schema file in `/opt/opendj/config/schema/`


!!! Note
 * This upgrade replaces all the default Gluu Server scripts WITH SCRIPTS FROM 4.0 and removes other custom scripts. (This will replace any customization you may have made to these default script entries) 
 * Default authentication mode will be set to auth_ldap_server
 * Cache provider configuration will be set to 4.0 default
 * Reconfigure your logo and favicon


### Upgrade 4.0 to 4.1

* Create directory
```
# mkdir /root/upg410
```

* Download the upgrade script
```
# wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.1.0/upg40to410.py -O /root/upg410/upg40to410.py
```

* Execute the script:

```
# cd /root/upg410/
# python upg40to410.py
```
### 4.0 upgrade script details

The 4.0 upgrade script performs the following tasks:

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

## Kubernetes upgrading instructions 

### Overview

This guide introduces how to upgrade from one version to another.

### Upgrade

#### Kustomize

1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.1/README.md#build-pygluu-kubernetespyz-manually).

1.  **If using LDAP**: Create configmap for `101-ox.ldif` file.

    ```bash
    kubectl create cm oxldif -n gluu --from-file=101-ox.ldif
    ```
    
1.  **If using LDAP**: Mount [101-ox.ldif](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.1/pygluu/kubernetes/templates/ldap/base/101-ox.ldif) in opendj-pods. Open opendj yaml or edit the statefulset directly `kubectl edit statefulset opendj -n gluu`

    ```yaml
      volumes:
      - name: ox-ldif-cm
        configMap:
          name: oxldif
      containers:
      - envFrom:
        - configMapRef:
            name: opendj-cm-b9g25hk457
        image: gluufederation/wrends:4.1.0_01
        ...
        ...
        volumeMounts:
        - name: ox-ldif-cm
          mountPath: /opt/opendj/config/schema/101-ox.ldif
          subPath: 101-ox.ldif

    ```
    
1.  Run :

     ```bash
     ./pygluu-kubernetes.pyz upgrade
     ```

#### Helm
  
1.  Copy the following yaml into `upgrade.yaml` and adjust all entries marked below:
 
    ```yaml
    apiVersion: v1
    data:
      DOMAIN: FQDN #<-- Change this to your FQDN
      GLUU_CACHE_TYPE: NATIVE_PERSISTENCE #<-- Change this if necessary
      GLUU_CONFIG_ADAPTER: kubernetes
      GLUU_CONFIG_KUBERNETES_NAMESPACE: gluu  #<-- Change this to Gluus namespace
      GLUU_COUCHBASE_CERT_FILE: /etc/certs/couchbase.crt
      GLUU_COUCHBASE_PASSWORD_FILE: /etc/gluu/conf/couchbase_password
      GLUU_COUCHBASE_URL: cbgluu.cbns.svc.cluster.local #<-- Change this if necessary
      GLUU_COUCHBASE_USER: admin #<-- Change this if necessary
      GLUU_LDAP_URL: opendj:1636
      GLUU_PERSISTENCE_LDAP_MAPPING: "" #<-- Change this if using hybrid with ldap as persistence
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
            - "4.0" #<-- Change this if necessary
            - --target
            - "4.1" #<-- Change this if necessary
            envFrom:
            - configMapRef:
                name: upgrade-cm
            image: gluufederation/upgrade:4.1.1_02
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

1.  Modify all images  inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.1/pygluu/kubernetes/templates/helm/gluu/values.yaml) to latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.1/pygluu/kubernetes/templates/gluu_versions.json) according to upgrade target version. 

1.  **If using LDAP**: Create configmap for `101-ox.ldif` file.

    ```bash
    kubectl create cm oxldif -n gluu --from-file=101-ox.ldif
    ```
    
1.  **If using LDAP**: Mount [101-ox.ldif](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.1/pygluu/kubernetes/templates/ldap/base/101-ox.ldif) in opendj-pods. Open opendj yaml or edit the statefulset directly `kubectl edit statefulset opendj -n gluu`

    ```yaml
      volumes:
      - name: ox-ldif-cm
        configMap:
          name: oxldif
      containers:
      - envFrom:
        - configMapRef:
            name: opendj-cm-b9g25hk457
        image: gluufederation/wrends:4.1.0_01
        ...
        ...
        volumeMounts:
        - name: ox-ldif-cm
          mountPath: /opt/opendj/config/schema/101-ox.ldif
          subPath: 101-ox.ldif

    ```
    
1. Apply `upgrade.yaml`

    ```bash
    kubectl create -f upgrade.yaml -n <namespace>
    ```
   
   Wait until upgrade job is finished and tail the logs of the upgrade pod.
   
1.  Run upgrade `Helm`

    ```bash
    helm upgrade -f values.yaml .
    ```

### Exporting Data

!!! Note
 * This step is not needed.


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
