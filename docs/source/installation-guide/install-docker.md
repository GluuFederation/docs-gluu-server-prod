# Docker Installation

## Overview
This guide provides instructions for deploying the Gluu Server on a single node VM using Docker.

## Prerequisites

For Docker deployments, provision a VM with:

### Linux users

- The minimum system requirements, as described in the [VM Preparation Guide](../installation-guide/index.md#system-requirements).

- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script) is installed

### Mac users

- The minimum system requirements for [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)

- [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

## Instructions

### Obtain files for deployment

Download the `pygluu-compose.pyz` executable:

```sh
wget https://github.com/GluuFederation/community-edition-containers/releases/download/v1.0.2/pygluu-compose.pyz
chmod +x pygluu-compose.pyz
```

!!!Note
    `pygluu-compose.pyz` requires Python 3.6+ (and `python3-distutils` package if Ubuntu/Debian is used).

Run the following command to generate manifests for deployment:

```sh
./pygluu-compose.pyz config
```

The generated files are similar to example below:

```sh
tree
.
├── couchbase.crt
├── couchbase_password
├── docker-compose.yml
├── gcp_kms_creds.json
├── gcp_kms_stanza.hcl
├── pygluu-compose.pyz
├── svc.casa.yml
├── svc.cr_rotate.yml
├── svc.key_rotation.yml
├── svc.ldap.yml
├── svc.oxauth.yml
├── svc.oxd_server.yml
├── svc.oxpassport.yml
├── svc.oxshibboleth.yml
├── svc.oxtrust.yml
├── svc.radius.yml
├── svc.redis.yml
├── svc.vault_autounseal.yml
├── vault_gluu_policy.hcl
├── vault_role_id.txt
└── vault_secret_id.txt

0 directories, 21 files
```

Proceed to [deployment section](./#deploy-the-gluu-server) for basic setup of Gluu Server deployment or read the [customizing section](./#customizing-installation) for advance setup.

### Customizing installation

#### Choose services

The following services are available during deployment:

| Service             | Setting Name           | Mandatory | Enabled by default|
| ------------------- | ---------------------- | --------- | ------- |
| `consul`            | -                      | yes       | always  |
| `registrator`       | -                      | yes       | always  |
| `vault`             | -                      | yes       | always  |
| `nginx`             | -                      | yes       | always  |
| `oxauth`            | `SVC_OXAUTH`           | no        | yes     |
| `oxtrust`           | `SVC_OXTRUST`          | no        | yes     |
| `ldap`              | `SVC_LDAP`             | no        | yes     |
| `oxpassport`        | `SVC_OXPASSPORT`       | no        | no      |
| `oxshibboleth`      | `SVC_OXSHIBBOLETH`     | no        | no      |
| `redis`             | `SVC_REDIS`            | no        | no      |
| `radius`            | `SVC_RADIUS`           | no        | no      |
| `vault` auto-unseal | `SVC_VAULT_AUTOUNSEAL` | no        | no      |
| `oxd_server`        | `SVC_OXD_SERVER`       | no        | no      |
| `key_rotation`      | `SVC_KEY_ROTATION`     | no        | no      |
| `cr_rotate`         | `SVC_CR_ROTATE`        | no        | no      |

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

If `docker-compose.override.yml` exists, this file will be added as the last Compose file. For reference on multiple Compose file, please take a look at [https://docs.docker.com/compose/extends/#multiple-compose-files](https://docs.docker.com/compose/extends/#multiple-compose-files).

#### Choose persistence backends

Supported backends are LDAP, Couchbase, or mix of both (hybrid). The following config control which persistence backend is selected:

- `PERSISTENCE_TYPE`: choose one of `ldap`, `couchbase`, or `hybrid` (the default is `ldap`)
- `PERSISTENCE_LDAP_MAPPING`: choose one of `default`, `user`, `site`, `cache`, or `token` (default to `default`)

To choose a persistence backend, create a file called `settings.py` (if it wasn't created in the last step) and set the corresponding option as seen above. For example:

```python
PERSISTENCE_TYPE = "couchbase"      # Couchbase will be selected
PERSISTENCE_LDAP_MAPPING = "user"   # store user mapping in LDAP
COUCHBASE_USER = "admin"            # Couchbase user
COUCHBASE_URL = "192.168.100.4"     # Host/IP address of Couchbase server; omit the port
```

If `couchbase` or `hybrid` is selected, there are additional steps required to satisfy dependencies:

-   put Couchbase cluster certificate into the `couchbase.crt` file

-   put Couchbase password into the `couchbase_password` file

-   the Couchbase cluster must have `data`, `index`, and `query` services at minimum

-   if `COUCHBASE_URL` is set to hostname, make sure it can be reached by DNS query; alternatively add the extra host into `docker-compose.override.yml` file, for example:

    ```yaml
    services:
      oxauth:
        extra_hosts:
        - "${COUCHBASE_HOSTNAME}:${COUCHBASE_IP}"
    ```

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
    -b "o=gluu" \
    -s base \
    -T "objectClass=*"
```

### How to unseal Vault

There are several ways to unseal Vault:

1.  Use [auto-unseal](./#set-up-vault-auto-unseal)
1.  Re-run `pygluu-compose up` command.
1.  Quick manual unseal
    1. Get unseal key from `vault_key_token.txt` file.
    1. Log in to the Vault container: `docker exec -it vault sh`.
    1. Run `vault operator unseal` command (a prompt will appear). Enter the unseal key.
    1. Wait for few seconds for the containers to get back to work.
