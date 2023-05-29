!!! Attention
    All Linux assets, packages, and binaries require a support contract for access.
    Contact sales@gluu.org for more information. For free up-to-date binaries,
    check out the latest releases at [The Linux Foundation Janssen Project](https://docs.jans.io),
    the new upstream open source project.


# Docker Installation

## Overview
This guide provides instructions for deploying the Gluu Server on a single node VM using Docker.

## Prerequisites

For Docker deployments, provision a VM with:

### Linux users

- If using Ubuntu use `20.04` and higher.

- The minimum system requirements, as described in the [VM Preparation Guide](../installation-guide/index.md#system-requirements).

- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script) is installed

### Mac users

- The minimum system requirements for [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)

- [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

## Instructions

### Setup credentials for accessing docker images and assets

1.  Contact sales@gluu.org for credentials to access and pull our docker images. Existing customers should have received the credentials already. 

1.  Run the following command to use the credentials mentioned in previous step:

    ```
    docker login 
    ```

    You will be prompted for username and password/token.

### Obtain files for deployment

Download the latest `pygluu-compose-linux-amd64.pyz` (or `pygluu-compose-macos-amd64.pyz` for Mac users) file from [Releases](https://github.com/GluuFederation/community-edition-containers/releases) page and save it as `pygluu-compose.pyz`.

!!!Note
    `pygluu-compose.pyz` requires Python 3.6+ (and `python3-distutils` package if Ubuntu/Debian is used).

Make sure to set the downloaded `pygluu-compose.pyz` file as executable:

```
chmod +x pygluu-compose.pyz
```

Run the following command to generate manifests for deployment:

```sh
./pygluu-compose.pyz init
```

The generated files are similar to example below:

```sh
.
├── couchbase.crt
├── couchbase_password
├── couchbase_superuser_password
├── docker-compose.yml
├── gcp_kms_creds.json
├── gcp_kms_stanza.hcl
├── generate.json
├── google-credentials.json
├── jackrabbit_admin_password
├── job.configuration.yml
├── job.persistence.yml
├── settings.py
├── sql_password
├── svc.casa.yml
├── svc.cr_rotate.yml
├── svc.fido2.yml
├── svc.jackrabbit.yml
├── svc.ldap.yml
├── svc.oxauth.yml
├── svc.oxd_server.yml
├── svc.oxpassport.yml
├── svc.oxshibboleth.yml
├── svc.oxtrust.yml
├── svc.redis.yml
├── svc.scim.yml
├── svc.vault_autounseal.yml
├── svc.mysql.yml
├── svc.nginx_ports.yml
├── vault_gluu_policy.hcl
├── vault_key_token.txt
├── vault_role_id.txt
├── vault_secret_id.txt
```

Proceed to [deployment section](./#deploy-the-gluu-server) for basic setup of Gluu Server deployment or read the [customizing section](./#customizing-installation) for advance setup.

### Customizing installation

#### Available settings

The following settings are default settings.

```python
# ========
# Services
# ========

# enable LDAP service (set to `True` if `PERSISTENCE_TYPE` is set to `ldap`)
SVC_LDAP = True

# enable oxAuth service
SVC_OXAUTH = True

# enable oxTrust service
SVC_OXTRUST = True

# enable Passport service
SVC_OXPASSPORT = False

# enable Shibboleth service
SVC_OXSHIBBOLETH = False

# enable CacheRefresh rotation service
SVC_CR_ROTATE = False

# enable oxd service
SVC_OXD_SERVER = False

# enable Vault service with auto-unseal
SVC_VAULT_AUTOUNSEAL = False

# enable Casa service
SVC_CASA = False

# enable Jackrabbit service (set to `True` if `DOCUMENT_STORE_TYPE` is set to `JCA`)
SVC_JACKRABBIT = False

# enable SCIM service
SVC_SCIM = False

# enable Fido2 service
SVC_FIDO2 = False

# enable persistence loader service
JOB_PERSISTENCE = True

# enable config-init service
JOB_CONFIGURATION = True

# enable Redis service (set to `True` if `CACHE_TYPE` is set to `REDIS`)
SVC_REDIS = False

# =====
# Cache
# =====

# supported cache type (choose `NATIVE_PERSISTENCE` or `REDIS`)
CACHE_TYPE = "NATIVE_PERSISTENCE"

# ===========
# Persistence
# ===========

# supported persistence type (choose one of `ldap`, `couchbase`, `hybrid`, `sql`, or `spanner`)
PERSISTENCE_TYPE = "ldap"

# dataset saved into LDAP (choose one of `default`, `user`, `site`, `token`, `cache`, or `session`)
# this setting only affects hybrid `PERSISTENCE_TYPE`
PERSISTENCE_LDAP_MAPPING = "default"

# Couchbase username
COUCHBASE_USER = "admin"

# Couchbase superuser
COUCHBASE_SUPERUSER = ""

# hostname/IP address of Couchbase server (scheme and port are omitted)
COUCHBASE_URL = "localhost"

# Prefix of Couchbase bucket
COUCHBASE_BUCKET_PREFIX = "gluu"

# SQL dialect (currently only support mysql; postgresql support is experimental)
SQL_DB_DIALECT= "mysql"

# SQL database name
SQL_DB_NAME = "gluu"

# hostname/IP address of SQL server
SQL_DB_HOST = "localhost"

# port of SQL server
SQL_DB_PORT = 3306

# username to access SQL database
SQL_DB_USER = "gluu"

# Google project ID
GOOGLE_PROJECT_ID = ""

# Instance ID of Google Spanner
GOOGLE_SPANNER_INSTANCE_ID = ""

# Database ID of Google Spanner
GOOGLE_SPANNER_DATABASE_ID = ""

# Host of Spanner emulator, i.e. 10.10.1.2:9010
SPANNER_EMULATOR_HOST = ""

# ==============
# Document store
# ==============

# supported store type (choose one of `LOCAL` or `JCA`)
DOCUMENT_STORE_TYPE = "LOCAL"

# admin username for Jackrabbit service
JACKRABBIT_USER = "admin"

# ====
# Misc
# ====

# load customization from docker-compose.override.yml (if exists)
ENABLE_OVERRIDE = False

# enable oxTrust API
OXTRUST_API_ENABLED = False

# enable test-mode for oxTrust API
OXTRUST_API_TEST_MODE = False

# enable Passport support
PASSPORT_ENABLED = False

# enable Casa support
CASA_ENABLED = False

# enable SAML Shibboleth support
SAML_ENABLED = False

# enable SCIM API
SCIM_ENABLED = False

# enable test-mode for SCIM API (default to `OAUTH`)
GLUU_SCIM_PROTECTION_MODE = "TEST"
```

To override any of these settings, create `settings.py` and adjust the value, for example:

```python
# settings.py
COUCHBASE_URL = "10.2.1.1"
COUCHBASE_BUCKET_PREFIX = "my_org"
```

#### Choose services

The following services are available during deployment:

| Service             | Setting Name           | Mandatory | Enabled by default|
| ------------------- | ---------------------- | --------- | ----------------- |
| `consul`            | -                      | yes       | always            |
| `registrator`       | -                      | yes       | always            |
| `vault`             | -                      | yes       | always            |
| `nginx`             | -                      | yes       | always            |
| `persistence`       | `JOB_PERSISTENCE`      | no        | yes               |
| `configuration`     | `JOB_CONFIGURATION`    | no        | yes               |
| `oxauth`            | `SVC_OXAUTH`           | no        | yes               |
| `oxtrust`           | `SVC_OXTRUST`          | no        | yes               |
| `ldap`              | `SVC_LDAP`             | no        | yes               |
| `oxpassport`        | `SVC_OXPASSPORT`       | no        | no                |
| `oxshibboleth`      | `SVC_OXSHIBBOLETH`     | no        | no                |
| `redis`             | `SVC_REDIS`            | no        | no                |
| `vault` auto-unseal | `SVC_VAULT_AUTOUNSEAL` | no        | no                |
| `oxd_server`        | `SVC_OXD_SERVER`       | no        | no                |
| `cr_rotate`         | `SVC_CR_ROTATE`        | no        | no                |
| `casa`              | `SVC_CASA`             | no        | no                |
| `scim`              | `SVC_SCIM`             | no        | no                |
| `fido2`             | `SVC_FIDO2`            | no        | no                |
| `jackrabbit`        | `SVC_JACKRABBIT`       | no        | no                |
| `mysql`             | `SVC_MYSQL`            | no        | no                |
| `nginx_ports`       | `SVC_NGINX_PORTS`      | no        | yes               |

To enable/disable non-mandatory services listed above, create a file called `settings.py` and set the value to `True` to enable or set to `False` to disable the service. For example:

```python
SVC_LDAP = True                 # will be enabled
SVC_OXPASSPORT = False          # will be disabled
```

Any services not specified in `settings.py` will follow the default settings.

To override manifests (i.e. changing oxAuth service definition), add `ENABLE_OVERRIDE = True` in `settings.py`, for example:

```python
ENABLE_OVERRIDE = True
```

Then define overrides in `docker-compose.override.yml` (create the file if not exist):

```yaml
version: "2.4"

services:
  oxauth:
    container_name: my-oxauth
```

If `docker-compose.override.yml` exists, this file will be added as the last Compose file. For reference on multiple Compose file, please take a look at [Multiple Compose Files](https://docs.docker.com/compose/extends/#multiple-compose-files).

#### Choose persistence backends

Supported backends are LDAP, Couchbase, hybrid (LDAP + Couchbase), SQL, and Google Spanner. The following config control which persistence backend is selected:

- `PERSISTENCE_TYPE`: choose one of `ldap`, `couchbase`, `hybrid` (`ldap` + `couchbase`), `sql`, or `spanner` (default to `ldap`)
- `PERSISTENCE_LDAP_MAPPING`: choose one of `default`, `user`, `site`, `cache`, `token`, or `session` (default to `default`)

Modify `settings.py` (create the file if doesn't exist) and configure based on selected persistence. For example:

1.  LDAP

    No additional configuration needed.

1.  Couchbase


    ```python
    PERSISTENCE_TYPE = "couchbase"
    COUCHBASE_USER = "admin"
    COUCHBASE_SUPERUSER = ""
    COUCHBASE_BUCKET_PREFIX = "gluu"
    COUCHBASE_URL = "192.168.100.4"
    # disable LDAP service
    SVC_LDAP = False
    ```

    Additional steps required to satisfy dependencies:

    -   put Couchbase cluster certificate into the `couchbase.crt` file (the root certificate is visible on the Root Certificate panel of the Security screen of Couchbase Web Console)

    -   put Couchbase password into the `couchbase_password` file

    -   the Couchbase cluster must have `data`, `index`, and `query` services at minimum

    -   if `COUCHBASE_URL` is set to hostname, make sure it can be reached by DNS query; alternatively add the extra host into `docker-compose.override.yml` file, for example:

        ```yaml
        services:
        oxauth:
            extra_hosts:
            - "${COUCHBASE_HOSTNAME}:${COUCHBASE_IP}"
        ```

1.  Hybrid

    ```python
    PERSISTENCE_TYPE = "hybrid"
    # store user mapping in LDAP
    PERSISTENCE_LDAP_MAPPING = "user"
    # ensure LDAP service is enabled
    SVC_LDAP = True
    ```

    Additional steps required to satisfy dependencies:

    -   put Couchbase cluster certificate into the `couchbase.crt` file (the root certificate is visible on the Root Certificate panel of the Security screen of Couchbase Web Console)

    -   put Couchbase password into the `couchbase_password` file

    -   the Couchbase cluster must have `data`, `index`, and `query` services at minimum

1.  SQL

    ```python
    PERSISTENCE_TYPE = "sql"
    SQL_DB_DIALECT= "mysql"
    SQL_DB_NAME = "gluu"
    SQL_DB_HOST = "localhost"
    SQL_DB_PORT = 3306
    SQL_DB_USER = "gluu"
    # ensure MySQL service is enabled
    SVC_MYSQL = True
    # ensure LDAP service is disabled
    SVC_LDAP = False
    ```

    Additional steps required to satisfy dependencies:

    -   put MySQL password into the `sql_password` file.
    -   put MySQL root password into the `sql_root_password` file (required to bootstrap the database).
    -   minimum MySQL version is `v5.7`.

1.  Spanner

    ```python
    PERSISTENCE_TYPE = "spanner"
    GOOGLE_PROJEC_ID = "my-project-id"
    GOOGLE_SPANNER_INSTANCE_ID = "my-instance-id"
    GOOGLE_SPANNER_DATABASE_ID = "my-db-id"

    # optionally use Spanner emulator instead of Spanner cloud
    # SPANNER_EMULATOR_HOST = "10.10.1.2:9010"
    # disable LDAP service
    SVC_LDAP = False
    ```

    Additional steps required to satisfy dependencies:

    -   put Google credentials into `google-credentials.json` file.
    -   alternative is to use Spanner emulator

#### Set up Vault auto-unseal

Enable Vault auto-unseal with GCP KMS API by specifying it in `settings.py`:

```python
# settings.py
SVC_VAULT_AUTOUNSEAL = True     # enable Vault auto-unseal with GCP KMS API
```

The following is an example of how to obtain [GCP KMS credentials](https://shadow-soft.com/vault-auto-unseal/) JSON file, and save it as `gcp_kms_creds.json` in the same directory where `pygluu-compose.pyz` is located, for example:

```json
{
    "type": "service_account",
    "project_id": "project",
    "private_key_id": "1234abcd",
    "private_key": "-----BEGIN PRIVATE KEY-----\nabcdEFGH==\n-----END PRIVATE KEY-----\n",
    "client_email": "sa@project.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sa%40project.iam.gserviceaccount.com"
}
```

Afterwards, create `gcp_kms_stanza.hcl` in the same directory where `pygluu-compose.pyz` is located; for example:

```hcl
seal "gcpckms" {
    credentials = "/vault/config/creds.json"
    project     = "vault-project-1234"
    region      = "us-east1"
    key_ring    = "vault-keyring"
    crypto_key  = "vault-key"
}
```

!!!Note
    Adjust the contents of `gcp_kms_stanza.hcl` except the `credentials` value as it is mapped in `svc.vault_autounseal.yml` file.

#### Choose Document Storage

There are 2 types of supported document storage:

1.  `LOCAL`

    This is the default document store (using container's filesystem).

2.  `JCA`

    This document store uses `jackrabbit` service. To enable `JCA` document store, modify `settings.py` as seen below:

    ```python
    SVC_JACKRABBIT = True
    DOCUMENT_STORE_TYPE = "JCA"
    ```

### Deploy the Gluu Server

Run the following command to install the Gluu Server:

```sh
./pygluu-compose.pyz up
```

Running the command above will show the deployment process:

```text
[I] Attempting to gather external IP address
[I] Using 192.168.100.4 as external IP address
```

!!!Note
    `pygluu-compose.pyz up` command will try to detect external IP address of the host.
    In the example above, `192.168.100.4` is detected automatically.
    If somehow the IP is incorrect, stop current process and set the IP address explicitly in `settings.py` (create the file if not exist).

    ```python
    # settings.py
    HOST_IP = "192.168.100.10"  # set the external IP address explicitly
    ```

    Re-run the `pygluu-compose.pyz up` command to load new settings.

```text
Creating consul ... done
Creating vault  ... done
```

The `consul` and `vault` services are required to provide config and secret layers used by the rest of Gluu Server services.

```text
[I] Checking Vault status
[W] Unable to get seal status in Vault; retrying ...
[I] Initializing Vault with 1 recovery key and token
[I] Vault recovery key and root token saved to vault_key_token.txt
[I] Unsealing Vault manually
[I] Creating Vault policy for Gluu
[I] Enabling Vault AppRole auth
```

On initial deployment, since Vault has not been configured yet, the `pygluu-compose.pyz` will generate a root token and key to interact with Vault API, saved as `vault_key_token.txt` (secure this file, as it contains the recovery key and root token).
`pygluu-compose.pyz` will also setup Vault AppRole for interaction between other services to Vault. Note that by enabling AppRole, there will be `vault_role_id.txt` and `vault_secret_id.txt` files under working directory.

```text
[I] Attempting to gather FQDN from Consul
[W] Unable to get FQDN from Consul; retrying ...
[W] Unable to get FQDN from Consul; retrying ...
[W] Unable to get FQDN from Consul; retrying ...
Enter hostname [demoexample.gluu.org]:
Enter country code [US]:
Enter state [TX]:
Enter city [Austin]:
Enter oxTrust admin password: ***********
Repeat password: ***********
Enter LDAP admin password: ***********
Repeat password: ***********
Enter email [support@demoexample.gluu.org]:
Enter organization [Gluu]:
```

After `consul` and `vault` have been deployed, the next things is getting config from `consul`. If there's no existing config, a series of config will be prompted to user as seen above.

!!!Note
    When prompted for hostname (which will be used as `https://<hostname>` address), using a public FQDN is highly recommended.
    If somehow there's no way to use public FQDN, map the VM IP address and the FQDN in `/etc/hosts` file.

    ```text
    # /etc/hosts
    192.168.100.4 demoexample.gluu.org
    ```

Wait for few seconds and the deployment will continue the rest of the processes.

```
[I] Launching Gluu Server .........................................
[I] Gluu Server installed successfully; please visit https://demoexample.gluu.org
```

See [checkings logs](./#checking-the-deployment-logs) section on how to track the progress.

### Checking the deployment logs

The deployment process may take some time. You can keep track of the deployment by using the following command:

```sh
./pygluu-compose.pyz logs -f
```

### Uninstall the Gluu Server

Run the following command to delete all objects during the deployment:

```sh
./pygluu-compose.pyz down
```

## FAQ

### How to use ldapsearch

```sh
docker exec -ti ldap /opt/opendj/bin/ldapsearch \
    -h localhost \
    -p 1636 \
    -Z \
    -X \
    -D "cn=directory manager" \
    -w $LDAP_PASSWORD \
    -b "o=gluu" \
    -s base \
    "objectClass=*"
```

where `$LDAP_PASSWORD` is the password for LDAP given in installation process.

### How to unseal Vault

There are several ways to unseal Vault:

1.  Use [auto-unseal](./#set-up-vault-auto-unseal)
1.  Re-run `pygluu-compose up` command.
1.  Quick manual unseal
    1. Get unseal key from `vault_key_token.txt` file.
    1. Log in to the Vault container: `docker exec -it vault sh`.
    1. Run `vault operator unseal` command (a prompt will appear). Enter the unseal key.
    1. Wait for few seconds for the containers to get back to work.
