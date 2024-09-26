# Admin REST APIs

## Overview

Gluu Server offers REST APIs for the [oxTrust Admin GUI](https://gluu.org/docs/gluu-server/4.4/admin-guide/oxtrust-ui/). With the REST API, server configurations can be automated, new GUIs can be built to expose specific admin functionality, and other integrations can be created for the Gluu admin portal.

## VM Installation instructions

Add the REST API extension to an existing Gluu 4.5.x deployment by following these steps:

1. Inside the Gluu chroot, navigate to `/opt/gluu/jetty/identity/custom/libs/`.

1. In this folder, download the .jar file corresponding to the Gluu Server 4.4 version currently installed: 

    - [4.5.5.Final](https://maven.gluu.org/maven/org/gluu/oxtrust-api-server/4.5.5.Final/oxtrust-api-server-4.5.5.Final.jar)

1. Change permission of this jar to `jetty:gluu`

1. Navigate to `/opt/gluu/jetty/identity/webapps/`.

1. Create a file called `identity.xml` if it does not already exist.

1. Add the following to `identity.xml`:

    ```
    <?xml version="1.0"  encoding="ISO-8859-1"?>
    <!DOCTYPE Configure PUBLIC "-//Jetty//Configure//EN" "http://www.eclipse.org/jetty/configure_9_0.dtd">

    <Configure class="org.eclipse.jetty.webapp.WebAppContext">
      <Set name="contextPath">/identity</Set>
      <Set name="war"><Property name="jetty.webapps" default="."/>/identity.war</Set>
      <Set name="extractWAR">true</Set>

      <Set name="extraClasspath">./custom/libs/[jarName].jar</Set>
    </Configure>
    ```

1. On the second to last line, replace `[jarName]` with the name of the `.jar` file downloaded in step 2.

1. [Restart](https://gluu.org/docs/gluu-server/4.4/operation/services/#restart) the `identity` service.

## Kubernetes and Docker instructions

## Overview

The following sections are guides on how to access oxTrust API using within Gluu Server container deployment.
See below [oxTrust API docs](#available-api-modes-for-vm) for reference.

## Prerequisites

1. `gluufederation/config-init:4.0.1_05` image (test mode client is introduced).
1. `gluufederation/persistence:4.0.1_05` image (enable oxTrust API upon deployment).
1. `gluufederation/oxauth:4.0.1_05` image.
1. `gluufederation/oxtrust:4.0.1_05` image.

## Available API Modes for CN

The oxTrust API has two modes that administrators can configure according to need for cloud native deployments.

### Test Mode for CN

!!! Note
    Test mode is not recommended for production. Choose UMA mode instead.

1.  Set environment variable `GLUU_OXTRUST_API_ENABLED=true` and `GLUU_OXTRUST_API_TEST_MODE=true` when running `gluufederation/persistence` container to enable oxTrust API:

    ```sh
    docker run \
        --rm \
        --name persistence \
        -e GLUU_CONFIG_CONSUL_HOST=consul \
        -e GLUU_SECRET_VAULT_HOST=vault \
        -e GLUU_PERSISTENCE_TYPE=ldap \
        -e GLUU_PERSISTENCE_LDAP_MAPPING=default \
        -e GLUU_LDAP_URL=ldap:1636 \
        -e GLUU_OXTRUST_API_ENABLED=true \
        -e GLUU_OXTRUST_API_TEST_MODE=true \
        -v $PWD/vault_role_id.txt:/etc/certs/vault_role_id \
        -v $PWD/vault_secret_id.txt:/etc/certs/vault_secret_id \
        gluufederation/persistence:4.4.0-1
    ```
    
    If using kubernetes `pygluu-kubernetes.pyz` answer yes to both the following prompts: 
    
    ```sh
    Enable oxTrust Api         [N]?[Y/N]                               y
    Enable oxTrust Test Mode [N]?[Y/N]                                 y
    ```
    
    Alternatively, enable the features using oxTrust UI.
    
    1. Navigate to `Configuration > Manage Custom Scripts`, Under `UMA RPT Policies`, select and enable the custom script named `oxtrust_api_access_policy`
    
    1. Navigate to `Configuration > JSON Configuration`, select `oxTrust Configuration` tab
Search for the field named `oxTrustApiTestMode`, set it to `True` and save the change.

1.  Obtain Test mode client credentials from config and secret backends.

    1.  Grab `api_test_client_id` from config backend; in this example, we're getting `0008-b52a8524.45b2-4.45-968e-481a366be8cd` as its value. This is the client ID.

    1.  Grab `api_test_client_secret` from secret backend; in this example, we're getting `TVtZwLZxp25XFDelMJNDQsa8` as its value. This is the client secret.

1.  Get token from Gluu Server; in this example we're using `https://demoexample.gluu.org`.

    ```sh
    curl -k -u '0008-b52a8524-35b2-4835-968e-481a366be8cd:TVtZwLZxp25XFDelMJNDQsa8' \
        https://demoexample.gluu.org/oxauth/restv1/token \
        -d grant_type=client_credentials
    ```

    The response example:

    ```json
    {
        "access_token": "0d14102c-70e5-485c-8b64-e56f1ecfcf3e",
        "token_type": "bearer",
        "expires_in": 299
    }
    ```

    Extract the `access_token` value (in this case, `0d14102c-70e5-485c-8b64-e56f1ecfcf3e` is the token).

1.  Make request to oxTrust API endpoints:

    ```sh
    curl -k -H 'Authorization: Bearer 0d14102c-70e5-485c-8b64-e56f1ecfcf3e' \
        https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    If succeed, the output is similar to the following:

    ```json
    [
        {
            "status": "ACTIVE",
            "displayName": "Gluu Manager Group",
            "description": "This group is for administrative purpose, with full acces to users",
            "members": [
                "inum=04f0d0e9-a609-4a0a-9580-ebd981a49a61,ou=people,o=gluu"
            ],
            "inum": "60B7",
            "owner": null,
            "organization": null,
            "iname": null
        }
    ]
    ```

### UMA Mode for CN

1.  Set environment variable `GLUU_OXTRUST_API_ENABLED=true` when running `gluufederation/persistence` container to enable oxTrust API:

    ```sh
    docker run \
        --rm \
        --name persistence \
        -e GLUU_CONFIG_CONSUL_HOST=consul \
        -e GLUU_SECRET_VAULT_HOST=vault \
        -e GLUU_PERSISTENCE_TYPE=ldap \
        -e GLUU_PERSISTENCE_LDAP_MAPPING=default \
        -e GLUU_LDAP_URL=ldap:1636 \
        -e GLUU_OXTRUST_API_ENABLED=true \
        -e GLUU_OXTRUST_API_TEST_MODE=false \
        -v $PWD/vault_role_id.txt:/etc/certs/vault_role_id \
        -v $PWD/vault_secret_id.txt:/etc/certs/vault_secret_id \
        gluufederation/persistence:4.4.0-1
    ```
    
    If using kubernetes `pygluu-kubernetes.pyz` answer `Y` to enabling `oxTrust API` and `N` to enabling `Test Mode`.
    
    ```sh
    Enable oxTrust Api         [N]?[Y/N]                               y
    Enable oxTrust Test Mode [N]?[Y/N]                                 N
    ```
    Alternatively, enable the features using oxTrust UI.
    
    1. Navigate to `Configuration > Manage Custom Scripts`, Under `UMA RPT Policies`, select and enable the custom script named `oxtrust_api_access_policy`    

1.  Make request to oxTrust API (in this example, we're going to use `https://demoexample.gluu.org` URL), for example:

    ```sh
    curl -k -I https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    The request is rejected due to unauthenticated client and the response headers will be similar as the following:

    ```
    HTTP/1.1 401 Unauthorized
    WWW-Authenticate: UMA realm="Authorization required", host_id=demoexample.gluu.org, as_uri=https://demoexample.gluu.org/.well-known/uma2-configuration, ticket=ed5d9fa7-7117-4fc0-85c2-17a064448dc8
    ```

    Extract the ticket from `WWW-Authenticate` header; in this example the ticket is `ed5d9fa7-7117-4fc0-85c2-17a064448dc8`.

1.  Copy `api-rp.jks` and `api-rp-keys.json` from oxAuth container into host:

    ```sh
    docker cp oxauth:/etc/certs/api-rp.jks api-rp.jks \
        && docker cp oxauth:/etc/certs/api-rp-keys.json api-rp-keys.json
    ```
    
    In kubernetes get the oxauth pod name and use the following commands:
  
      ```sh
    kubectl cp oxauth-acsacsd2123:etc/certs/api-rp.jks api-rp.jks \
        && kubectl cp oxauth-acsacsd2123:etc/certs/api-rp-keys.json api-rp-keys.json
    ```
    


1.  Determine algorithm for signing JWT string, i.e. `RS256`.

    Here's an example of `api-rp-keys.json` contents:

    ```json
    {
        "keys": [
            {
                "kty": "RSA",
                "e": "AQAB",
                "use": "sig",
                "crv": "",
                "kid": "777c0619-802c-480d-9432-a5e25f85867a_sig_rs256",
                "x5c": ["MIIDAzCCAeugAwIBAgIgIoDkhKXYZG5/LDPoUEUBxLpvsUDwL+OEzkAMuMpglzLH6g9dDUyGVEh8iRg=="],
                "exp": 1606219942910,
                "alg": "RS256",
                "n": "r3LItabzy3Lg0SXf_6EZ1oANjyYQ_HCEj-r5cynyD7dnAQdXvkRLVMAby0EAoCaeEo_QkU79BCOY6o2w"
            }
        ]
    }
    ```

    Make sure `alg` value is `RS256`.
    Grab the `kid` value (in this example `777c0619-802c-480d-9432-a5e25f85867a_sig_rs256`).

1.  Grab keystore password from secret backend where key is `api_rp_client_jks_pass`. In this example, we're getting `secret` as its value.

1.  Convert `api-rp.jks` to `api-rp.pkcs12` (delete existing `api-rp.pkcs12` file if any):

    ```sh
    keytool -importkeystore \
        -srckeystore api-rp.jks \
        -srcstorepass secret  \
        -srckeypass secret \
        -srcalias 777c0619-802c-480d-9432-a5e25f85867a_sig_rs256 \
        -destalias 777c0619-802c-480d-9432-a5e25f85867a_sig_rs256 \
        -destkeystore api-rp.pkcs12 \
        -deststoretype PKCS12 \
        -deststorepass secret \
        -destkeypass secret
    ```

1.  Extract public and private key pair from `api-rp.pkcs12`:

    ```sh
    openssl pkcs12 -in api-rp.pkcs12 -nodes -out api-rp.pem -passin pass:secret
    ```

    Here's an example of generated `api-rp.pem`:

    ```text
    Bag Attributes
        friendlyName: d405b162-fb5d-4e9f-81cd-4edcb0db486a_sig_rs256
        localKeyID: 54 69 6D 65 20 31 35 37 35 31 37 34 30 33 35 32 33 30
    Key Attributes: <No Attributes>
    -----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwvKNUOZxaOcRB
    wwFtCJIqoqnaPYA0kfJEnnnm
    -----END PRIVATE KEY-----
    Bag Attributes
        friendlyName: d405b162-fb5d-4e9f-81cd-4edcb0db486a_sig_rs256
        localKeyID: 54 69 6D 65 20 31 35 37 35 31 37 34 30 33 35 32 33 30
    subject=/CN=oxAuth CA Certificates
    issuer=/CN=oxAuth CA Certificates
    -----BEGIN CERTIFICATE-----
    MIIDAzCCAeugAwIBAgIgAPS1X/1F5GFLp8xNYLbw9zs34TOwSd2Kz++dZHRijIkw
    grfXl0CuwA==
    -----END CERTIFICATE-----
    ```

    Grab the string starts with `-----BEGIN PRIVATE KEY-----` and ends with `-----END PRIVATE KEY-----`.
    This is the private key.

1.  Prepare data for generating JWT string.

    1.  Header

        ```json
        {
            "typ": "JWT",
            "alg": "RS256",
            "kid": "777c0619-802c-480d-9432-a5e25f85867a_sig_rs256"
        }
        ```

    1.  Payload

        Grab client ID from config backend where key is `oxtrust_requesting_party_client_id`. In this example we're getting `0008-76f0b100-6d68-4f21-96ca-c6e49d30094b` as its value.

        ```json
        {
            "iss": "0008-76f0b100-6d68-4f21-96ca-c6e49d30094b",
            "sub": "0008-76f0b100-6d68-4f21-96ca-c6e49d30094b",
            "exp": 1575185573,
            "iat": 1575181565,
            "jti": "2f1c50c6-0359-4913-b3f9-c17ca93a1b82",
            "aud": "https://demoexample.gluu.org/oxauth/restv1/token"
        }
        ```

        Note:

        - `iat` value is time since epoch; we can use `date +%s` command to get a value
        - `exp` value is expiration since epoch; we can use `date --date="1 hours" +%s`
        - `jti` value must be unique; we can use `uuidgen` command to get a value
        - `aud` is the URL for getting the token
        - `iss` and `sub` are client ID

    1.  Private key (see previous section about extracting private key)

    After header, payload, and private key are ready, generate JWT string using [debugger](https://jwt.io/#debugger-io) or any of supported [libraries](https://jwt.io/#libraries-io). Save the JWT string, for example:

    ```text
    eyJhbGciOiJSUzI1NiIs.RiLZyW2yYdF4P0QD0oY9zjBfsFwFSpSCRUe.3WnaETMtAIPpXQhry6SYFR1tFv1t4XO14o1qVA
    ```

1.  Grab token from `https://demoexample.gluu.org/oxauth/restv1/token`:

    ```sh
    curl -k https://demoexample.gluu.org/oxauth/restv1/token \
        -d grant_type='urn:ietf:params:oauth:grant-type:uma-ticket' \
        -d ticket='ed5d9fa7-7117-4fc0-85c2-17a064448dc8'  \
        -d client_id='0008-76f0b100-6d68-4f21-96ca-c6e49d30094b' \
        -d client_assertion_type='urn:ietf:params:oauth:client-assertion-type:jwt-bearer' \
        -d client_assertion='eyJhbGciOiJSUzI1NiIs.RiLZyW2yYdF4P0QD0oY9zjBfsFwFSpSCRUe.3WnaETMtAIPpXQhry6SYFR1tFv1t4XO14o1qVA'
        -d scope=`oxtrust-api-read oxtrust-api-write`
    ```

    The response example:

    ```json
    {
        "access_token": "d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509",
        "token_type": "Bearer",
        "upgraded": false,
        "pct": "0b598193-11cb-4926-9e4c-cc7c95e6ce37_CB14.8C6B.E2B2.46CD.53B2.CBEF.C50E.9FE9"
    }
    ```

    Extract value of `access_token`; in this case `d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509`.

1.  Retry request to get groups (this time pass along the token in the request header):

    ```sh
    curl -k -H 'Authorization: Bearer d01cdc70-6519-4118-89bb-9ee1748acdd1_D8F4.E104.D094.6B62.79E0.6F8E.FB55.0509' \
        https://demoexample.gluu.org/identity/restv1/api/v1/groups
    ```

    If succeed, the output is similar to the following:

    ```json
    [
        {
            "status": "ACTIVE",
            "displayName": "Gluu Manager Group",
            "description": "This group is for administrative purpose, with full acces to users",
            "members": [
                "inum=04f0d0e9-a609-4a0a-9580-ebd981a49a61,ou=people,o=gluu"
            ],
            "inum": "60B7",
            "owner": null,
            "organization": null,
            "iname": null
        }
    ]
    ```

    Reuse the token (as long as it still valid) to make any request to oxTrust API endpoints.

## Available API modes for VM

The oxTrust API has two modes that administrators can configure according to need for VM-based deployments.

### Test Mode for VM
   
Follow these steps to configure the test mode:

1. Move the oxTrust API jar to `/opt/gluu/jetty/identity/custom/libs/`.
1. Edit `identity.xml` as mentioned [above](#vm-installation-instructions)
1. [Restart](../operation/services.md#commands) the `identity` service
1. Log into Gluu Admin UI
1. Navigate to `Configuration` > `JSON Configuration`, select `oxTrust Configuration` tab
1. Search for the field named `oxTrustApiTestMode`, set it to `True` and save the change.
1. Add an OpenId Connect client for testing:
    
    - Client Name: **whatever you want**
    - Client secret: **a memorable secret**
    - scopes: **openid**,**permission**, ** https://gluu.org/auth/oxtrust.authenticationmethod.read** [ you might need more scopes to be released depending on your target operation. See the oxtrust.log for further instructions if something doesn't work. Log is pretty straight forward and verbose ]
    - grand types: **client_credentials**
    - Response type: **token**
    - NB: After pressing the save button, take note of the client ID generated and the secret. We need them for next step.

1. Run the command below from a terminal to request an access token from Gluu Server

    ```
    curl -k -u 'testClientId:testClientSecert' -d grant_type=client_credentials https://yourhostname/oxauth/restv1/token
    ```
    
1. Use that accesss token as Bearer token when making api calls.
   
### UMA Mode for VM
  
The UMA mode is the mode in which the API is protected by UMA. This is the recommended mode for production server.

## Available Endpoints

| API | Description |
| --- | ----------- |
| addClientToUmaResource | Add client to an UMA resource |
| addGroupMember | Add a group member |
| addRadiusClient | Add a new RADIUS client |
| addScopeToClient | Add a scope to an OIDC client|
| addScopeToUmaResource | Add a scope to an UMA resource |
| create | Create a new configuration |
| createAttribute | Add a new attribute |
| createClient | Add a new OpenID Connect client |
| createCustomScript | Add a new custom script |
| createGroup | Add a new group |
| createPassportProvider | Add a new passport provider |
| createPerson | Add a new person |
| createScope | Add a new OpenID Connect scope |
| createSectorIdentifier | Add a new sector identifier |
| createUmaResource | Add a new UMA resource| 
| createUmaScope | Add a new UMA scope |
| delete | Delete an existing configuration |
| deleteAllProviders | Delete all providers |
| deleteAllUmaScopes | Delete all UMA scopes |
| deleteAttribute | Delete an attribute |
| deleteAttributes | Delete all attributes |
| deleteClient | Delete an OpenID Connect client |
| deleteClientScopes | Delete the scopes in an OpenID Connect Client |
| deleteClients | Delete all clients|
| deleteCustomScript | Delete a custom script |
| deleteGroup | Delete a group |
| deleteGroupMembers | Delete the members of a group |
| deleteGroups | Delete all groups |
| deletePeople | Delete all people |
| deletePerson | Delete a person |
| deleteProvider | Delete a passport provider|
| deleteRadiusClient | Delete a RADIUS client |
| deleteScope | Delete an OpenID Connect scope|
| deleteScopes | Delete all OpenID Connect scopes |
| deleteSectorIdentifier | Delete a Sector Identifier |
| deleteUmaResource | Delete an UMA resource |
| deleteUmaScope | Delete an UMA scope |
| getAllActiveAttributes | Get all active attributes |
| getAllAttributes | Get all attributes |
| getAllInactiveAttributes | Get all inactive attributes |
| getAllScopes | Get all scopes |
| getAllSectorIdentifiers | Get all sector identifiers |
| getAttributeByInum | Get a specific attribute |
| getCasConfig | Get the existing configuration |
| getClientByInum | Get a specific OpenID Connect client |
| getClientScope | Get scopes assigned to an OpenID client |
| getConfiguration | Get Gluu configuration |
| getCurrentAuthentication | Get current authentication methods |
| getCustomScriptsByInum | Get specific custom scripts |
| getGroupByInum | Get a specific group|
| getGroupMembers | Get members of a specific group |
| getOxAuthJsonSettings | Get oxAuth JSON configuration settings |
| getOxtrustJsonSettings | Get oxTrust JSON configuration settings |
| getOxtrustSettings | get oxTrust configuration settings |
| getPassportBasicConfig | Get Passport's basic configuration |
| getPersonByInum | Get a specific person |
| getProviderById | Get a specific Passport provider |
| getRadiusClient | Get a specific RADIUS client |
| getScopeByInum | Get a specific OpenID Connect scope |
| getScopeClaims | List all claims for a scope |
| getSectorIdentifierById | Get a specific Sector Identifier |
| getServerConfig | Get RADIUS server configuration |
| getServerStatus | Get current server status|
| getSmtpServerConfiguration | Get SMTP server configuration|
| getUmaResourceById | Get a specific UMA resource |
| getUmaResourceClients | Get the clients for a specific UMA resource |
| getUmaResourceScopes | Get the scopes for a specific UMA resource |
| getUmaScopeByInum | Get a specific UMA scope |
| listCertificates | List descriptions of the Gluu Server's certificates |
| listClients | List all OpenID Connect clients |
| listCustomScripts | List all custom scripts |
| listCustomScriptsByType | List all person authentication scripts |
| listGroups | List all groups |
| listPeople | List all people |
| listProviders | List all Passport providers |
| listRadiusClients | List all RADIUS clients |
| listUmaResources | List all UMA resources |
| listUmaScopes | List UMA scopes |
| read | Get the existing configuration |
| removeClientToUmaResource | Remove a client from an UMA resource |
| removeGroupMember | Remove a member from a group |
| removeScopeToClient | Remove an existing scope from a client |
| removeScopeToUmaResource | Remove a scope from an UMA resource |
| searchAttributes | Search attributes |
| searchGroups | Search OpenID Connect clients |
| searchGroups1 | Search groups |
| searchGroups2 | Search person |
| searchScope | Search OpenID Connect scopes |
| searchSectorIdentifier | Search sector identifiers |
| searchUmaResources | Search UMA resources |
| searchUmaScopes | Search UMA scopes |
| status | Check the status of a configuration |
| status1 | Check the status of an existing configuration |
| testSmtpConfiguration | Test the SMTP configuration |
| update | Update the configuration |
| update1 | Update an existing configuration |
| updateAttribute | Update a new attribute | 
| updateAuthenticationMethod | Update the authentication methods | 
| updateClient | Update an OpenID Connect client | 
| updateCustomScript | Update a custom script | 
| updateGroup | Update a group |
| updateGroup1 | Update a person |
| updateOxauthJsonSetting | Update an oxAuth JSON configuration setting | 
| updateOxtrustJsonSetting | Update an oxTrust JSON configuration setting |
| updateOxtrustSetting | Update oxTrust settings |
| updatePassportBasicConfig | Update Passport basic configuration |
| updatePassportProvider | Update a Passport provider |
| updateRadiusClient | Update RADIUS client |
| updateScope | Update an OpenID Connect scope|
| updateSectorIdentifier | Update a sector identifier | 
| updateServerConfiguration | Update the RADIUS server configuration |
| updateSmtpConfiguration | Update the SMTP configuration |
| updateUmaResource | Update an UMA Resource |
| updateUmaScope| Update an UMA scope |

## API Reference

Current Swagger documentation for oxTrust APIs can be found in the [oxTrust API doc](https://gluu.org/swagger-ui/?operationsSorter=alpha&url=https://raw.githubusercontent.com/GluuFederation/oxTrust/version_4.4.1/api-server/src/main/resources/META-INF/openapi.yaml).

## License

Gluu oxTrust APIs are made available under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
