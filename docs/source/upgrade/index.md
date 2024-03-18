# Upgrade to Gluu Server 4.5

=== "Community Edition"
    
    ## Overview
    The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. You will need to either use our in-place upgrade script or explicitly install the new version and export/import your data. Find the existing version below for upgrade instructions to Gluu Server 4.5. 
    
    ## Pre-requisites
    
    - Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
    - Upgrades should always be thoroughly scoped and tested on a development environment *first*.
    - This upgrade process only upgrades versions 4.0.x through 4.5.0. To upgrade from a previous version, first [upgrade to 4.0](https://gluu.org/docs/gluu-server/4.0/upgrade/).
        
    - Upgrade script runs on Python 3. You need to install Python 3 before running the script.
        * On CentoOS/RHEL: `yum install -y python3`
        * On Ubuntu/Debian: `apt-get update && apt-get install -y python3`
    
    
    ## Online Upgrade from 4.x to 4.5.0
    
    The upgrade script downloads all needed software and applications from the internet. You can perform an online upgrade by following these steps:
    
    * Download the upgrade script
    
    ```
    wget https://raw.githubusercontent.com/GluuFederation/community-edition-package/master/update/4.5.0/upg4xto450.py
    ```
    
    * Execute the script:
    
    ```
    python3 upg4xto450.py
    ```
    
    Your upgrade directory will be the `/opt/upd/4.5.0/dist`. The script will create these sub directories: `app`, `gluu`, and `tmp`. It also downloads latest setup files to `/install/community_edition_setup_4.5.0`.

    ## Offline Upgrade from 4.x to 4.5.0
    
    If your machine is not open to public internet, you can download self extracting upgrade script form https://repo.gluu.org/upd/4.5-0.upg.run and you can run inside Gluu CE container as

    ```
    sh 4.5-0.upg.run
    ```
    
    The script extracts contents to `/opt/upd/4.5.0/dist`, and writes latest setup files to `/install/community_edition_setup_4.5.0`
    
=== "Cloud Native Edition"
 
    ## Overview
    
    This guide introduces how to upgrade cloud native edition from one version to another. 
    We support both upgrading from different versions, for example 4.4 to 4.5, or doing a patch upgrade of the same version. 
    You can upgrade using either `pygluu` or `helm`.


    === "LDAP"
        ### pygluu upgrade
        In order to upgrade your deployment using `pygluu`, you have to first [install](https://github.com/GluuFederation/cloud-native-edition/releases) and [build](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-kubernetes/#build-pygluu-kubernetespyz-manually) the `pygluu` tool.
        
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.5 https://github.com/GluuFederation/cloud-native-edition && cd cloud-native-edition/pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml) to the latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/gluu_versions.json) according to the upgrade target version. Also make sure your `override.yaml` other options are moved correctly to the new `values.yaml`.
        1.  Move the old `settings.json` that was used in the 4.4 installation into the same directory `pygluu-kubernetes.pyz` exists in.  The `json` file can be generated  using `./pygluu-kubernetes.pyz generate-settings`.

        1.  Execute the following command:
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
        ### helm upgrade

        Another way to upgrade your deployment is by simply going over your `override.yaml` used in 4.4 and adjust it according to the 4.5 [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml).
                    
        1.  Inside your new `override.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
            ``` yaml
            global:
                upgrade:
                    enabled: true
                    sourceVersion: "4.4"
                    targetVersion: "4.5"  
                persistence:
                    enabled: false
            ```
            To perform a patch upgrade, where the source and target version are the same, your `override.yaml` will be:

            ``` yaml
                global:
                    upgrade:
                        enabled: true
                        sourceVersion: "4.5"
                        targetVersion: "4.5"  
                    persistence:
                        enabled: true
            ```
        1.  Delete `oxAuthExpiration` index
        
            ```bash
            kubectl exec -ti gluu-opendj-0 -n <namespace> -- /opt/opendj/bin/dsconfig delete-backend-index --backend-name userRoot --index-name oxAuthExpiration --hostName 0.0.0.0 --port 4444 --bindDN 'cn=Directory Manager' --trustAll -f
            ```

            You will be prompted to enter the `LDAP password` and confirm the deletion.

        1.  Run `helm upgrade`
        
            ```bash
            helm upgrade <helm-release-name> gluu/gluu -f override.yaml -n <namespace>   
            ```

        1.  Once done revert `global.upgrade.enabled` to `false` and `global.persistence.enabled` to `true`.             
        
    === "Couchbase"
       
        ### pygluu upgrade
        In order to upgrade your deployment using `pygluu`, you have to first [install](https://github.com/GluuFederation/cloud-native-edition/releases) and [build](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-kubernetes/#build-pygluu-kubernetespyz-manually) the `pygluu` tool.
        
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.5 https://github.com/GluuFederation/cloud-native-edition && cd cloud-native-edition/pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml) to the latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/gluu_versions.json) according to the upgrade target version. Also make sure your `override.yaml` other options are moved correctly to the new `values.yaml`. For example, make sure your couchbase url, crt and other configurations are filled and correctly.

        1.  Move the old `settings.json` that was used in the 4.4 installation into the same directory `pygluu-kubernetes.pyz` exists in.  The `json` file can be generated  using `./pygluu-kubernetes.pyz generate-settings`.

        1.  Execute the following command:
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
        ### helm upgrade

        Another way to upgrade your deployment is by simply going over your `override.yaml` used in 4.4 and adjust it according to the 4.5 [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml).
                    
        1.  Inside your new `override.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
            ``` yaml
            global:
                upgrade:
                    enabled: true
                    sourceVersion: "4.4"
                    targetVersion: "4.5"  
                persistence:
                    enabled: false
            ```
            To perform a patch upgrade, where the source and target version are the same, your `override.yaml` will be:

            ``` yaml
                global:
                    upgrade:
                        enabled: true
                        sourceVersion: "4.5"
                        targetVersion: "4.5"  
                    persistence:
                        enabled: true
            ```

        1.  Run `helm upgrade`
        
            ```bash
            helm upgrade <helm-release-name> gluu/gluu -f override.yaml -n <namespace>   
            ```

        1.  Once done revert `global.upgrade.enabled` to `false` and `global.persistence.enabled` to `true`.             

    === "Hybrid"
       
        ### pygluu upgrade
        In order to upgrade your deployment using `pygluu`, you have to first [install](https://github.com/GluuFederation/cloud-native-edition/releases) and [build](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-kubernetes/#build-pygluu-kubernetespyz-manually) the `pygluu` tool.
        
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.5 https://github.com/GluuFederation/cloud-native-edition && cd cloud-native-edition/pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml) to the latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/gluu_versions.json) according to the upgrade target version. Also make sure your `override.yaml` other options are moved correctly to the new `values.yaml`. Also make sure your `override.yaml` other options are moved correctly to the new `values.yaml`. For example, make sure your couchbase url, crt and other configurations are filled and correctly.

        1.  Move the old `settings.json` that was used in the 4.4 installation into the same directory `pygluu-kubernetes.pyz` exists in.  The `json` file can be generated  using `./pygluu-kubernetes.pyz generate-settings`.

        1.  Execute the following command:
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
        ### helm upgrade

        Another way to upgrade your deployment is by simply going over your `override.yaml` used in 4.4 and adjust it according to the 4.5 [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml).
                    
        1.  Inside your new `override.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
            ``` yaml
            global:
                upgrade:
                    enabled: true
                    sourceVersion: "4.4"
                    targetVersion: "4.5"  
                persistence:
                    enabled: false
            ```
            To perform a patch upgrade, where the source and target version are the same, your `override.yaml` will be:

            ``` yaml
                global:
                    upgrade:
                        enabled: true
                        sourceVersion: "4.5"
                        targetVersion: "4.5"  
                    persistence:
                        enabled: true
            ```

        1.  Run `helm upgrade`
        
            ```bash
            helm upgrade <helm-release-name> gluu/gluu -f override.yaml -n <namespace>   
            ```

        1.  Once done revert `global.upgrade.enabled` to `false` and `global.persistence.enabled` to `true`.    

    === "SQL"

        ### pygluu upgrade
        In order to upgrade your deployment using `pygluu`, you have to first [install](https://github.com/GluuFederation/cloud-native-edition/releases) and [build](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-kubernetes/#build-pygluu-kubernetespyz-manually) the `pygluu` tool.
        
        1.  Clone latest stable manifests.
        
            ```bash
            git clone --recursive --depth 1 --branch 4.5 https://github.com/GluuFederation/cloud-native-edition && cd cloud-native-edition/pygluu/kubernetes/templates/helm/gluu
            ```
            
        1.  Modify all images inside main [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml) to the latest [images](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/gluu_versions.json) according to the upgrade target version. Also make sure your `override.yaml` other options are moved correctly to the new `values.yaml`.
        1.  Move the old `settings.json` that was used in the 4.4 installation into the same directory `pygluu-kubernetes.pyz` exists in.  The `json` file can be generated  using `./pygluu-kubernetes.pyz generate-settings`.

        1.  Execute the following command:
            ```bash
            ./pygluu-kubernetes.pyz upgrade-values-yaml
            ```
        ### helm upgrade

        Another way to upgrade your deployment is by simply going over your `override.yaml` used in 4.4 and adjust it according to the 4.5 [`values.yaml`](https://raw.githubusercontent.com/GluuFederation/cloud-native-edition/4.5/pygluu/kubernetes/templates/helm/gluu/values.yaml).
                    
        1.  Inside your new `override.yaml` set `global.upgrade.enabled` to `true` and `global.persistence.enabled` to `false`.
            ``` yaml
            global:
                upgrade:
                    enabled: true
                    sourceVersion: "4.4"
                    targetVersion: "4.5"  
                persistence:
                    enabled: false
            ```
            To perform a patch upgrade, where the source and target version are the same, your `override.yaml` will be:

            ``` yaml
                global:
                    upgrade:
                        enabled: true
                        sourceVersion: "4.5"
                        targetVersion: "4.5"  
                    persistence:
                        enabled: true
            ```

        1.  Run `helm upgrade`
        
            ```bash
            helm upgrade <helm-release-name> gluu/gluu -f override.yaml -n <namespace>   
            ```

        1.  Once done revert `global.upgrade.enabled` to `false` and `global.persistence.enabled` to `true`.


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
