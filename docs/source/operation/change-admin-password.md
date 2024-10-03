## Overview

There are times when default Gluu admin password need to be changed, for example rotating password for security reason.

## Change admin password in oxTrust

1. Login to oxTrust UI as `admin` user (created during installation).
1. Go to `Users > Manage People` sidebar menu, search for `admin` user in the form field. A list of matched users will be presented in a table.
1. Click the `admin` UID in the results table.
1. Scroll down and click `Change Password` button; a popup will be presented. Click `Set password` after password has been changed. If password successfully updated, the user will be logged out.

## Update Kubernetes secrets

!!!info
    The following additional steps only applies in cloud-native installation.

Once admin password has been changed via oxTrust UI, the Kubernetes secrets need to be updated as well. See steps below on how to update the secrets:

1.  Change `config.adminPass` attribute in `values.yaml` for subsequential installs/upgrades using `helm`:

    ```yaml
    config:
      # use same password that was updated in oxTrust
      adminPass: "newAdminPassword"
    ```

1.  Create new file `update_admin_secrets.py` with the following contents:

    ```python
    from pygluu.containerlib import get_manager

    # get the value of `userPassword` attribute from `gluuPerson` table/objectClass/document in persistence
    encoded_oxtrust_admin_password = "<userPassword>"

    manager = get_manager()
    manager.secret.set("encoded_oxtrust_admin_password", encoded_oxtrust_admin_password)
    ```

    Note, the `<userPassword>` value is taken from `userPassword` attribute/column of `gluuPerson` table/document.
    Consult to persistence (MySQL/PostgreSQL/OpenDJ/Couchbase/Spanner) docs on how to get value of an attribute.

    !!!warning
        The following experimental `update_admin_secrets.py` script can be used to get `userPassword` attribute from persistence and save it into Kubernetes secrets.
        This may not work in older versions of Gluu cloud-native installation.

        ```python
        import os

        from pygluu.containerlib import get_manager
        from pygluu.containerlib.persistence.couchbase import CouchbaseClient
        from pygluu.containerlib.persistence.couchbase import id_from_dn
        from pygluu.containerlib.persistence.couchbase import get_couchbase_password
        from pygluu.containerlib.persistence.ldap import LdapClient
        from pygluu.containerlib.persistence.spanner import SpannerClient
        from pygluu.containerlib.persistence.sql import SQLClient
        from pygluu.containerlib.persistence.sql import doc_id_from_dn
        from pygluu.containerlib.utils import ldap_encode

        encoded_oxtrust_admin_password = ""  # nosec: B105

        manager = get_manager()

        # get encoded_oxtrust_admin_password from persistence
        admin_inum = manager.config.get("admin_inum")
        dn = f"inum={admin_inum},ou=people,o=gluu"

        persistence_type = os.environ.get("GLUU_PERSISTENCE_TYPE", "ldap")

        if persistence_type == "sql":
            client = SQLClient()
            entry = client.get("gluuPerson", doc_id_from_dn(dn), column_names=["userPassword"])
            encoded_oxtrust_admin_password = entry["userPassword"]

        elif persistence_type == "spanner":
            client = SpannerClient()
            entry = client.get("gluuPerson", doc_id_from_dn(dn), column_names=["userPassword"])
            encoded_oxtrust_admin_password = entry["userPassword"]

        elif persistence_type == "couchbase":
            client = CouchbaseClient(
                os.environ["GLUU_COUCHBASE_URL"],
                os.environ["GLUU_COUCHBASE_USER"],
                get_couchbase_password(manager),
            )
            bucket_prefix = os.environ["GLUU_COUCHBASE_BUCKET_PREFIX"]
            bucket = f"{bucket_prefix}_user"
            id_ = id_from_dn(dn)
            req = client.exec_query(
                f"SELECT {bucket}.userPassword FROM {bucket} USE KEYS '{id_}'"  # nosec: B608
            )
            entry = req.json()["results"][0]
            encoded_oxtrust_admin_password = entry["userPassword"]

        # fallback to ldap
        else:
            client = LdapClient(manager)
            entry = client.get(dn, attributes=["userPassword"])
            encoded_oxtrust_admin_password = entry["userPassword"].raw_values[0].decode()

        # push the new encoded_oxtrust_admin_password value to secrets
        manager.secret.set("encoded_oxtrust_admin_password", encoded_oxtrust_admin_password)
        ```

1.  Copy the `update_admin_secrets.py` to a running pod and execute:

    ```bash
    kubectl -n $NAMESPACE cp update_admin_secrets.py $POD:/tmp/update_admin_secrets.py
    ```

    Run the script to update the secrets:

    ```bash
    kubectl -n $NAMESPACE exec $POD -- python3 /tmp/update_admin_secrets.py
    ```

    !!!warning
        To avoid unwanted updates, it's best to delete the `update_admin_secrets.py` script after password has been changed. 

        ```bash
        kubectl -n $NAMESPACE exec $POD -- rm -f /tmp/update_admin_secrets.py
        ```
