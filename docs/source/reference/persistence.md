# Persistence Mechanisms

## Overview

In previous versions the Gluu Server was tightly bundled with LDAP for persistence. In 4.x, the persistence layer has been re-architected, and there is no longer a tight bundling with a specific DB (i.e. LDAP). Now, new persistence plugins can be added and data can be split between multiple persistence modules.

Gluu 4.3 CE supports these persistence modules out-of-the-box:

1. [LDAP](https://github.com/GluuFederation/oxCore/tree/master/persistence-ldap), which is still the default persistence method.

1. [Couchbase Enterprise Edition](https://github.com/GluuFederation/oxCore/tree/master/persistence-couchbase), supporting both local (on the same server as Gluu) and remote Couchbase clusters. 
 
1. [Hybrid](https://github.com/GluuFederation/oxCore/tree/master/persistence-hybrid), a meta module allowing data to be mapped to different persistence modules. For example, user and group entries can be stored in LDAP, while all other entries are stored in Couchbase.  

The internal data model is the same for all persistence modules. This consistency is based on generic annotations, the filters API, the persistence API, entry type (objectClass) and persistence key (Domain Name). 

Here is a sample persistence bean:

![Entry definitions](../img/admin-guide/installation-guide/entry_definition.png)
    
The persistence entry manager API supports CRUD operations, which work with the persistence beans. The base API is defined in the oxcore-persistence-core library, in the [PersistenceEntryManager](https://github.com/GluuFederation/oxCore/blob/master/persistence-core/src/main/java/org/gluu/persist/PersistenceEntryManager.java).

## Persistence Layer Dependencies

This diagram shows the EntryManager dependencies and type resolutions based on the `persistence.type` specified in `gluu.properties`:

![Dependency Chart](../img/admin-guide/installation-guide/persistence_dependencies.png)

## Persistence Layer Modules

### LDAP

This module uses an LDAP server to store data. The module code is in the [oxcore-persistence-ldap](https://github.com/GluuFederation/oxCore/tree/master/persistence-ldap) project.

There are few major data structure changes in the data model:

- Dropped `o=<inumOrg>` sub level
- Dropped `ou=appliances` sub level
- Moved configuration to `ou=configuration,o=gluu`
- Moved `ou=tokens` and `ou=authoriztions` from client sub-entries to `o=gluu`

In Gluu 4.2, there is a migrator to convert an existing data set to the new model.

<!-- More detail on the migrator to come -->

The following is an example of a typical LDAP tree after installation:

![LDAP Data tree structure](../img/admin-guide/installation-guide/ldap_data_tree.png)

This module uses the configuration specified in `/etc/gluu/conf/gluu-ldap.properties`:

```
bindDN: <ldap_binddn>
bindPassword: <encoded_ ldap_pw>
servers: <ldap_hostname>:<ldaps_port>

useSSL: true
ssl.trustStoreFile: <ldapTrustStoreFn>
ssl.trustStorePin: <encoded_ldapTrustStorePass>
ssl.trustStoreFormat: pkcs12

maxconnections: 10

# Max wait 20 seconds
connection.max-wait-time-millis=20000

# Force to recreate polled connections after 30 minutes
connection.max-age-time-millis=1800000

# Invoke connection health check after checkout it from pool
connection-pool.health-check.on-checkout.enabled=false

# Interval to check connections in pool. Value is 3 minutes. Not used when onnection-pool.health-check.on-checkout.enabled=true
connection-pool.health-check.interval-millis=180000

# How long to wait during connection health check. Max wait 20 seconds
connection-pool.health-check.max-response-time-millis=20000

binaryAttributes=objectGUID
certificateAttributes=userCertificate
```

The default settings are suitable for most environments.

### Couchbase

[Couchbase](https://www.couchbase.com/) is a persistence layer option very similar to LDAP, so an existing DB can be converted from LDIF to Couchbase. 

Here is sample data entry with key `scopes_10B2`:

```
{
  "dn": "inum=10B2,ou=scopes,o=gluu",
  "objectClass": "oxAuthCustomScope",
  "defaultScope": false,
  "description": "View your local username in the Gluu Server.",
  "inum": "10B2",
  "oxAuthClaim": [
    "inum=42E0,ou=attributes,o=gluu"
  ],
  "oxId": "user_name",
  "oxScopeType": "openid"
}
```

![Couchbase Buckets list](../img/admin-guide/installation-guide/couchbase_buckets.png)
    
The list of buckets is not hardcoded and can be changed via the `gluu-couchbase.properties` configuration file.

The following is an example of the default mapping configuration:

```
buckets: gluu, gluu_client, gluu_cache, gluu_site, gluu_token, gluu_authorization, gluu_user, gluu_statistic

bucket.default: gluu
bucket.gluu_user.mapping: people, groups
bucket.gluu_cache.mapping: cache
bucket.gluu_statistic.mapping: statistic
bucket.gluu_site.mapping: cache-refresh
bucket.gluu_authorization.mapping: authorizations
bucket.gluu_token.mapping: tokens
bucket.gluu_client.mapping: clients
```

There are two mandatory keys in this configuration, `buckets` and `bucket.default`. `buckets` provides information about all available buckets. `bucket.default` is the main bucket that applications should use if other mapping rules were not applied.

The optional third type of line, `bucket.<>.mapping: <comma_separated_second_level_names>` gives instructions for which bucket should store specified entries. The value here is the RDN value of the second level in the LDAP tree.

The table below specifies the list of entry types that applications store in buckets:

| Bucket | Entry Type |
| --- | --- |
|gluu | <ul> <li> gluuOrganization </li> <li> gluuConfiguration </li> <li> oxAuthConfiguration </li> <li> oxTrustConfiguration </li> <li> oxPassportConfiguration </li> <li> oxApplicationConfiguration </li> <li> gluuAttribute </li> <li> oxCustomScript </li> <li> oxAuthCustomScope </li> <li> oxSectorIdentifier </li> <li> oxUmaResource </li> <li> oxUmaResourcePermission </li> <li> oxAuthUmaRPT </li> <li> oxAuthUmaPCT </li> <li> oxDeviceRegistration </li> <li> oxU2fRequest </li> </ul> |
| gluu_client | oxAuthClient |
| gluu_cache | oxCacheEntity |
| gluu_site | gluuInumMap |
| gluu_authorization | oxClientAuthorization |
| gluu_token | oxAuthToken |
| gluu_user | <ul> <li> gluuPerson </li> <li> gluuGroup </li> <li> pairwiseIdentifier </li> <li> oxDeviceRegistration </li> <li> oxFido2AuthenticationEntry </li> <li> oxFido2RegistrationEntry </li> </ul> |
| gluu_statistic | oxMetric |

Both LDAP and Couchbase persistence layers use the [Gluu Filter API](https://github.com/GluuFederation/oxCore/blob/master/persistence-filter/src/main/java/org/gluu/search/filter/Filter.java) to minimize the Gluu Server's dependency on a specific DB. At runtime, the Couchbase persistence layer converts them to the N1QL query language.

This module uses the configuration specified in `/etc/gluu/conf/gluu-couchbase.properties`:

```
servers: <hostname>

connection.connect-timeout:10000
connection.connection-max-wait-time: 20000
connection.operation-tracing-enabled: false

# If mutation tokens are enabled, they can be used for advanced durability requirements,
# as well as optimized RYOW consistency.
connection.mutation-tokens-enabled: false

# Sets the pool size (number of threads to use) for all non blocking operations in the core and clients
# (default value is the number of CPUs).
# connection.computation-pool-size: 5

# Default scan consistency. Possible values are: not_bounded, request_plus, statement_plus
connection.scan-consistency: not_bounded

auth.userName: <couchbase_server_user>
auth.userPassword: <encoded_couchbase_server_pw>

buckets: gluu, gluu_client, gluu_cache, gluu_site, gluu_token, gluu_authorization, gluu_user, gluu_statistic

bucket.default: gluu
bucket.gluu_user.mapping: people, groups
bucket.gluu_cache.mapping: cache
bucket.gluu_statistic.mapping: statistic
bucket.gluu_site.mapping: cache-refresh
bucket.gluu_authorization.mapping: authorizations
bucket.gluu_token.mapping: tokens
bucket.gluu_client.mapping: clients

password.encryption.method: <encryption_method>

ssl.trustStore.enable: <ssl_enabled>
ssl.trustStore.file: <couchbaseTrustStoreFn>
ssl.trustStore.pin: <encoded_couchbaseTrustStorePass>
ssl.trustStore.format: pkcs12

binaryAttributes=objectGUID
certificateAttributes=userCertificate
```

### Hybrid

The hybrid persistence mechanism is a meta-DB persistence layer. Its main role is to add an abstraction layer to help split data between DBs. For example, it could be used to resolve these and other issues:

1. Store expired entries separately to reduce the main DB's size. For example, an id_token needed for the end_session endpoint
1. Store modification history
1. Use LDAP to store users data

This module combines other persistence layers, so all layers used should be correctly configured. This module uses the configuration specified in `/etc/gluu/conf/gluu-hybrid.properties`. The following is a sample file:

```
storages: couchbase, ldap
storage.default: couchbase
storage.ldap.mapping: people, groups
storage.couchbase.mapping: clients, cache, site, tokens, statistic, authorization
```

In this example, CE applications will use LDAP for `ou=people` and `ou=groups`. All other data will be stored in the Couchbase DB.

## Generic configuration properties

Base configuration details are stored in the `/etc/gluu/conf/gluu.properties` file.

The following is a self-explanatory sample configuration:

```
persistence.type=couchbase

oxauth_ConfigurationEntryDN=ou=oxauth,ou=configuration,o=gluu
oxtrust_ConfigurationEntryDN=ou=oxtrust,ou=configuration,o=gluu
oxidp_ConfigurationEntryDN=ou=oxidp,ou=configuration,o=gluu
oxcas_ConfigurationEntryDN=ou=oxcas,ou=configuration,o=gluu
oxpassport_ConfigurationEntryDN=ou=oxpassport,ou=configuration,o=gluu
oxradius_ConfigurationEntryDN=ou=oxradius,ou=configuration,o=gluu

certsDir=/etc/certs
confDir=
pythonModulesDir=/opt/gluu/python/libs
```

## Data Type Chart

| Name	| LDAP	| SQL	| Spanner	| objectClass/Table |
| ---- | --- | --- | --- | --- |
| oxDeviceData	| directoryString	| TINYTEXT	| STRING(MAX)	| oxDeviceRegistration | 
| oxPublicKeyId	| directoryString	| VARCHAR(96)	| STRING(96)	| oxFido2RegistrationEntry |
| oxAuthRequestURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient| 
| oxAuthConfWebKeys	| directoryString	| TEXT	| STRING(MAX)	| oxAuthConfiguration |
| gluuSAML1URI	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuAttribute |
| oxData	| directoryString	| TEXT	| STRING(MAX)	| oxMetric |
| oxCacheConfiguration	| directoryString	| TEXT	| STRING(MAX)	| gluuConfiguration |
| memberOf	| distinguishedName	| JSON	| ARRAY<STRING(MAX)>	| gluuPerson, gluuOrganization |
| oxAuthTokenEndpointAuthMethod	| directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthClient |
| oxInvolvedClients	| directoryString	| TEXT	| STRING(MAX)	| oxAuthSessionId |
| oxScriptError	| directoryString	| TEXT	| STRING(MAX)	| oxCustomScript |
| gluuThemeColor	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuOrganization |
| oxIDPAuthentication	| directoryString	| JSON	| ARRAY<STRING(MAX)>	| gluuConfiguration |
| oxAuthTosURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| scimCustomSecond	|	| JSON	| ARRAY<STRING(MAX)> | |	
| oxSmtpConfiguration	| directoryString	| JSON	| ARRAY<STRING(MAX)>	| gluuConfiguration |
| oxAuthLogoURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| oxRegistrationData	| directoryString	| TEXT	| STRING(MAX)	| oxFido2RegistrationEntry |
| nickname	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuPerson |
| doc_id		| | VARCHAR(64)	|STRING(64) | |	
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuSAMLconfig, gluuConfiguration, gluuAttribute, gluuPerson, gluuInumMap, oxPassportConfiguration, gluuOrganization, gluuGroup |
| oxResource	| directoryString |	TINYTEXT	| STRING(MAX) |	oxUmaResource |
| gluuConfDynamic |	directoryString |	TEXT	| STRING(MAX)	| gluuApplicationConfiguration |
| oxAuthConfStatic	| directoryString	| TEXT	| STRING(MAX)	| oxAuthConfiguration |
| tknTyp	| directoryString	| VARCHAR(32)	| STRING(32)	| token |
| member	| directoryString	| JSON	| ARRAY<STRING(MAX)>	| gluuGroup |
| middleName	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuPerson |
| oxAuthenticationMode	| directoryString |	VARCHAR(64) |	STRING(64) |	gluuConfiguration |
| scp |	directoryString	| TEXT	| STRING(MAX)	| token |
| oxScopeType |	directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthCustomScope |
| oxSoftwareStatement	| directoryString	| TEXT	| STRING(MAX)	| oxAuthClient |
| oxAuthJwks	| directoryString	| TEXT	| STRING(MAX)	| oxAuthClient |
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	| oxProxOp, oxAuthCustomScope, oxClientAuthorization, oxExpiredObject, oxUmaResource, oxDeviceRegistration, oxAuthSessionId, oxPushDevice, oxFido2AuthenticationEntry, oxSectorIdentifier, oxRp, oxFido2RegistrationEntry, oxU2fRequest, pairwiseIdentifier, oxPushApplication
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	| gluuSAMLconfig, gluuConfiguration, oxAuthCustomScope, oxUmaResource, oxCustomScript, oxDeviceRegistration, gluuAttribute, gluuCustomPerson, oxLink, oxSectorIdentifier, oxAuthClient, gluuOrganization, gluuGroup |
| oxAuthClientSecret	| directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthClient |
| picture	| directoryString	| VARCHAR(96)	| STRING(96)	| gluuPerson |
| gluuAttributeType	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuAttribute |
| oxAuthUserDN	| distinguishedName	| VARCHAR(128)	| STRING(128)	| oxAuthSessionId |
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	| oxShibbolethCASProtocolConfiguration, gluuSAMLconfig, gluuConfiguration, oxProxOp, oxAuthCustomScope, samlAcr, oxProxClient, oxUmaResource, oxCustomScript, gluuInvoice, oxScript, gluuAttribute, oxAuthClient, gluuPerson, gluuInumMap, gluuOrganization, gluuGroup, oxEntry, gluuOxtrustStat
| oxAuthUmaScope	| directoryString	| VARCHAR(128)	| STRING(128)	| oxUmaResource, oxUmaResourcePermission
| gluuAttributeName	| directoryString |	VARCHAR(64)	| STRING(64)	| gluuAttribute |
| oxValidation |	directoryString	| TINYTEXT	| STRING(MAX)	| gluuAttribute |
| oxTrustConfCacheRefresh	| directoryString	| TEXT |	STRING(MAX) |	oxTrustConfiguration |
| dat	| directoryString	| TEXT |	STRING(MAX)	| cache, oxExpiredObject, oxRp, jansStatEntry |
| oxAuthResponseType	| directoryString	| JSON	 | ARRAY<STRING(MAX)>	| oxAuthClient |
| clnId	| directoryString	| VARCHAR(64)	| STRING(64)	| cibaRequest, token, oxAuthUmaPCT, oxAuthUmaRPT|
| oxClaimRedirectURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| oxAuthPolicyURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| programmingLanguage	| directoryString	| VARCHAR(64)	| STRING(64)	| oxCustomScript |
| oxSessionState	| directoryString	| TEXT	| STRING(MAX)	| oxAuthSessionId |
| uid	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuPerson, gluuOrganization |
| gluuAttributeOrigin	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuAttribute |
| gluuConfStatic	| directoryString	| TEXT	| STRING(MAX)	| gluuApplicationConfiguration |
| oxAuthSessionAttribute	| directoryString	| TEXT	| STRING(MAX)	| oxAuthSessionId |
| gluuOrgShortName	| directoryString	| VARCHAR(64)	| STRING(64)	| gluuOrganization |
| oxAccessTokenSigningAlg	| directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthClient |
| oxAuthClientURI	| directoryString |	TINYTEXT	| STRING(MAX)	| oxAuthClient |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	| gluuSAMLconfig, gluuConfiguration, oxProxOp, oxAuthCustomScope, oxProxClient, oxUmaResource, oxCustomScript, oxDeviceRegistration, gluuAttribute, oxAuthClient, gluuPerson, gluuOrganization, gluuGroup, oxFido2RegistrationEntry, oxEntry, oxPushApplication |
| oxLogViewerConfig	| directoryString	| TEXT	| STRING(MAX)	| gluuConfiguration |
| gluuSAML2URI	| directoryString	| VARCHAR(64)	| STRING(64) |	gluuAttribute |
| oxApplicationType	| directoryString	| VARCHAR(64)	| STRING(64)	| oxMetric |
| oxScript	| directoryString	| TEXT	| STRING(MAX)	| oxCustomScript, oxScript |
| oxAuthConfErrors	| directoryString	| TEXT	| STRING(MAX)	| oxAuthConfiguration |
| oxAuthSubjectType	| directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthClient |
| oxAuthGrantType	| directoryString	| JSON	| ARRAY<STRING(MAX)>	| oxAuthClient |
| oxAuthLogoutURI	| directoryString	| TINYTEXT	| STRING(MAX) |	oxAuthClient |
| oxAttributes |	directoryString	| TEXT	| STRING(MAX) |	oxAuthCustomScope, oxUmaResourcePermission, oxAuthClient |
| oxAuthPermissionGrantedMap	| directoryString	| TEXT	| STRING(MAX)	| oxAuthSessionId |
| classRef	| directoryString	| TEXT	| STRING(MAX)	| samlAcr |
| oxAuthSectorIdentifierURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| nnc	| directoryString	| TEXT	| STRING(MAX)	| token |
| oxAuthClientId	| directoryString	| VARCHAR(64)	| STRING(64)	| oxClientAuthorization, oxSectorIdentifier, pairwiseIdentifier |
| oxTrustConfImportPerson	| directoryString	| TEXT	| STRING(MAX)	| oxTrustConfiguration |
| oxAuthInitiateLoginURI	| directoryString	| TINYTEXT	| STRING(MAX)	| oxAuthClient |
| oxAuthIdTokenSignedResponseAlg	| directoryString	| VARCHAR(64)	| STRING(64)	| oxAuthClient |
| oxDocumentStoreConfiguration	| directoryString	| TEXT	| STRING(MAX)	| gluuConfiguration |
| oxAuthJwksURI	| directoryString	| TINYTEXT	| STRING(MAX) |	oxAuthClient |
| attr	| directoryString	| TEXT	| STRING(MAX)	| token, jansStatEntry |
| oxScriptType	| directoryString	| VARCHAR(64)	| STRING(64)	| oxCustomScript, oxScript |
| tknCde	| directoryString	| VARCHAR(80)	| STRING(80)	| token, oxAuthUmaPCT, oxAuthUmaRPT |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	| oxShibbolethCASProtocolConfiguration, gluuConfiguration, oxApplicationConfiguration, oxAuthConfiguration, gluuApplicationConfiguration, oxTrustConfiguration, oxPassportConfiguration, vdapcontainer, oxProxConfiguration |
| urn	| directoryString	| VARCHAR(128)	| STRING(128)	| gluuAttribute |
| oxTrustMetaLocation	| directoryString	| TINYTEXT	| STRING(MAX)	| oxDeviceRegistration, gluuPerson, gluuGroup |
| userPassword	| directoryString	| VARCHAR(100)	| STRING(100)	| gluuConfiguration, gluuPerson, gluuOrganization |
| oxAuthClientIdIssuedAt	| GeneralizedTime	| DATETIME(3)	| TIMESTAMP	| oxAuthClient |
| oxJwt	| directoryString	| TEXT	| STRING(MAX)	| oxAuthSessionId |
| oxTrustConfApplication	| directoryString	| TEXT	| STRING(MAX)	| oxTrustConfiguration |
| oxAuthConfDynamic	| directoryString	| TEXT	| STRING(MAX)	| oxAuthConfiguration | 
| oxDeviceRegistrationConf	| directoryString	| TEXT	| STRING(MAX)	| oxDeviceRegistration |
| jwtReq	| directoryString	| TEXT	| STRING(MAX)	| token |
| oxScopeExpression	| directoryString	| TEXT	| STRING(MAX)	| oxUmaResource |
| oxDeviceKeyHandle	| directoryString	| VARCHAR(96)	| STRING(96)	| oxDeviceRegistration | 
| oxConfApplication	| directoryString	| TEXT	| STRING(MAX)	| oxShibbolethCASProtocolConfiguration, oxApplicationConfiguration | 
| o	| directoryString	| VARCHAR(64)	| STRING(64) | gluuSAMLconfig, gluuConfiguration, vdlabel, vdDirectoryView, gluuPerson, gluuOrganization, gluuGroup
sn	directoryString	VARCHAR(64)	STRING(64)	gluuPerson |
| givenName |	directoryString	| VARCHAR(64)	| STRING(64) |	gluuPerson |
| tknBndCnf	| directoryString	| TINYTEXT	| STRING(MAX) |	token, oxAuthClient |
| acr	| directoryString	| VARCHAR(48)	| STRING(48)	| token |
| oxAuthClaimName	| directoryString |	VARCHAR(64)	| STRING(64)	| gluuAttribute |
| oxUmaPermission	| directoryString |	JSON	| ARRAY<STRING(MAX)>	| oxAuthUmaRPT |
