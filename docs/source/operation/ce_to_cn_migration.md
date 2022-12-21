# Migrating from the Community Edition (VM base) to the Cloud Native edition

## Overview
This operational guide walks through migration from the community edition, which uses a VM approach, to the cloud native edition, which is primarily a Kubernetes cluster.

## Requirements

-   Access to the CE VM
-   Gluu CE version >= 4.5    
-   A Kubernetes cluster, and access to kubectl. You may take a look at the following [section](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-kubernetes/#system-requirements-for-cloud-deployments) to get a better sense on sizing requirements for the Kubernetes cluster.

## Migration Steps

1.  Log in to the server where CE is installed:

    ```bash
    ssh $USER@$CE_SERVER
    ```
    
1.  Back up the data in persistence and save them elsewhere.
    
1.  Set an environment variable to mark where the root directory of CE installation is.

    If using chrooted installation:

    ```bash
    export CE_HOME=/opt/gluu-server
    ```

    otherwise:

    ```bash
    export CE_HOME=
    ```
    
1.  Prepare manifests files:

    1.  Create new directory:

        ```bash
        mkdir -p $HOME/ce-migration
        cd $HOME/ce-migration
        ```

        Take a note about the full path of this directory (for example `/root/ce-migration`).
    
    1.  If `setup.properties.last` exists create `setup.properties`. Otherwise generate setup.properties.:
        
        ```bash
        cp $CE_HOME/install/community-edition-setup/setup.properties.last setup.properties
        ```

        If `setup.properties.last` does not exist:
        
        ```bash
        openssl enc -d -aes-256-cbc -in $CE_HOME/install/community-edition-setup/setup.properties.last.enc -out setup.properties
        ```

    1.  Get all certificates, keys, and keystores:
    
        ```bash  
        cp $CE_HOME/etc/certs/*.crt .
        cp $CE_HOME/etc/certs/*.key .
        cp $CE_HOME/etc/certs/*.pem .
        cp $CE_HOME/etc/certs/*.jks .
        cp $CE_HOME/etc/certs/*.pkcs12 .
        cp $CE_HOME/opt/shibboleth-idp/credentials/*.jks .
        cp $CE_HOME/opt/shibboleth-idp/credentials/*.kver .
        cp $CE_HOME/opt/shibboleth-idp/conf/datasource.properties .
        ```
    
    1.  Get the `salt` file:
        
        ```bash
        cp $CE_HOME/etc/gluu/conf/salt .
        ```
    
1.  Get configuration/secret from the persistence that is used with your current CE installation.

    === "LDAP"
         Run the following LDAP search queries:
    
        ```bash
        $CE_HOME/opt/opendj/bin/ldapsearch \
            --useSSL \
            --trustAll \
            -D "cn=directory manager" \
            -p 1636 \
            -w $LDAP_PASSWD \
            -b "o=gluu" \
            -s sub '(objectClass=gluuConfiguration)' > gluu-configuration.ldif
        ```
            
        ```bash
        $CE_HOME/opt/opendj/bin/ldapsearch \
            --useSSL \
            --trustAll \
            -D "cn=directory manager" \
            -p 1636 \
            -w $LDAP_PASSWD \
            -b "o=gluu" \
            -s sub '(objectClass=oxAuthConfiguration)' > oxauth-configuration.ldif
        ```
            
        ```bash
        $CE_HOME/opt/opendj/bin/ldapsearch \
            --useSSL \
            --trustAll \
            -D "cn=directory manager" \
            -p 1636 \
            -w $LDAP_PASSWD \
            -b "o=gluu" \
            -s sub '(objectClass=oxAuthClient)' > oxauth-client.ldif
        ```
        
        Here's an example of expected `.ldif` file:

        ```bash
        dn: ou=configuration,o=gluu
        gluuHostname: 1b4211097aa4
        gluuOrgProfileMgt: false
        gluuPassportEnabled: false
        gluuRadiusEnabled: false
        gluuSamlEnabled: false
        gluuScimEnabled: false
        gluuVdsCacheRefreshEnabled: true
        ```
    
    === "Couchbase"
        Run the following N1QL queries (in Couchbase UI):
    
        ```sql
        # save the result as gluu-configuration.json manually
        SELECT META().id, gluu.*
        FROM gluu
        WHERE objectClass = 'gluuConfiguration'
        ```

        ```sql
        # save the result as oxauth-configuration.json manually
        SELECT META().id, gluu.*
        FROM gluu
        WHERE objectClass = 'oxAuthConfiguration'
        ```

        ```sql
        # save the result as oxauth-client.json manually
        SELECT META().id, gluu.*
        FROM gluu
        WHERE objectClass = 'oxAuthClient'
        ```

        Here's an example of the expected `.json` file:
    
        ```json
        [
            {
                "dn": "ou=configuration,o=gluu",
                "gluuPassportEnabled": false,
                "gluuRadiusEnabled": false,
                "gluuSamlEnabled": false,
                "gluuScimEnabled": false,
                "gluuVdsCacheRefreshEnabled": false,
                "id": "configuration",
                "objectClass": "gluuConfiguration"
            }
        ]
        ```
    
    === "Spanner"
    
        Follow the official docs at https://cloud.google.com/spanner/docs/export (currently the supported format is Avro only).

        Here's an example of exported Avro filenames:
    
        ```bash
        gluuConfiguration.avro-00000-of-00001
        oxAuthConfiguration.avro-00000-of-00001
        oxAuthClient.avro-00000-of-00001
        ```

        The expected filenames used by config-init container are:
    
        ```bash
        gluu-configuration.avro
        oxauth-configuration.avro
        oxauth-client.avro
        ```
        hence you may need to copy them manually from the original Avro files.

    === "SQL"
        === "MySQL"
    
            Install [mysqlsh](https://dev.mysql.com/doc/mysql-shell/8.0/en/mysql-shell-install.html), then run the following commands:
    
            ```bash
            echo 'select * from gluuConfiguration' | mysqlsh --json=pretty --sql --show-warnings=false --uri=$DBUSER@$DBHOST:$DBPORT/$DBNAME -p > gluu-configuration.json
            echo 'select * from oxAuthConfiguration' | mysqlsh --json=pretty --sql --show-warnings=false --uri=$DBUSER@$DBHOST:$DBPORT/$DBNAME -p > oxauth-configuration.json
            echo 'select * from oxAuthClient' | mysqlsh --json=pretty --sql --show-warnings=false --uri=$DBUSER@$DBHOST:$DBPORT/$DBNAME -p > oxauth-client.json
            ```
    
            Here's an example of the expected `.json` file:
    
            ```json
            {
                "hasData": true,
                "rows": [
                    {
                        "doc_id": "configuration",
                        "objectClass": "gluuConfiguration",
                        "dn": "ou=configuration,o=gluu",
                        "description": null,
                        "oxSmtpConfiguration": {
                            "v": []
                        },
                        "gluuVDSenabled": null,
                        "ou": "configuration",
                        "gluuStatus": null,
                        "displayName": null
                    }
                ]
            }
            ```
    
        === "PostgreSQL"
    
            ```bash
            psql -h $DBHOST -p $DBPORT -U $DBUSER -d $DBNAME -W -t -A -o gluu-configuration.json -c 'select json_agg(t) from (select * from "gluuConfiguration") t;'
            psql -h $DBHOST -p $DBPORT -U $DBUSER -d $DBNAME -W -t -A -o oxauth-configuration.json -c 'select json_agg(t) from (select * from "oxAuthConfiguration") t;'
            psql -h $DBHOST -p $DBPORT -U $DBUSER -d $DBNAME -W -t -A -o oxauth-client.json -c 'select json_agg(t) from (select * from "oxAuthClient") t;'
            ```
    
        Here's an example of the expected `.json` file:

        ```json
        [
            {
                "doc_id": "configuration",
                "objectClass": "gluuConfiguration",
                "dn": "ou=configuration,o=gluu",
                "oxTrustStoreConf": "{\"useJreCertificates\":true}",
                "gluuAdditionalMemory": null,
                "gluuSmtpRequiresAuthentication": null,
                "gluuPassportEnabled": 0,
                "gluuShibFailedAuth": null,
                "gluuAppliancePollingInterval": null,
                "gluuAdditionalBandwidth": null,
                "gluuRadiusEnabled": 0,
                "description": null
            }
        ]
        ```

1.  Log out from the server where CE is installed.

1.  Download manifests files:

    ```bash
    scp -r $USER@$CE_SERVER:/root/ce-migration .
    ```
    
1.  Download [`pygluu-kubernetes.pyz`](https://github.com/GluuFederation/cloud-native-edition/releases). This package can be built [manually](https://github.com/GluuFederation/cloud-native-edition/blob/4.2/README.md#build-pygluu-kubernetespyz-manually).

1.  Run :

    ```bash
    ./pygluu-kubernetes.pyz install
    ```
    
    You will be prompted to migrate from CE.
    
    !!!note
        The services will not run until the persistence backup data is imported.
  
1.  Import backup data into the persistence manually.

1.  Restart main services: 

    ```bash
    kubectl rollout restart deployment <gluu-release-name>-auth-server -n <gluu-namespace>
    kubectl rollout restart statefulset <gluu-release-name>-oxtrust -n <gluu-namespace>
    #kubectl rollout restart deployment gluu-auth-server -n gluu
    ```

1.  If new additional services were deployed that originally were not on the source CE VM (i.e. SCIM, Fido2, etc), the persistence job must be enabled  to fill the missing entries (existing entries will not be modified). Note that some configuration may need to be modified manually via oxTrust UI. 
    
    1.  Open  `helm/gluu/values.yaml` using your favourite editor, and set `global.persistence.enabled` to `true` and `global.upgrade.enabled` to `true`. 
    
    1.  Run helm upgrade:
    
        ```bash
        helm upgrade <release-name> . -f ./helm/gluu/values.yaml -n <namespace>   
        ```
    
