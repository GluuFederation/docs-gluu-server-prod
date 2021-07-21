## Overview

The following tables detail the appropriate data types for properties across different persistance mechanisms. 

## Data Type Charts

### cache
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| dat	| directoryString	| TEXT |	STRING(MAX)	|

### cibaRequest
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| clnId	| directoryString	| VARCHAR(64)	| STRING(64)	|

### gluuApplicationConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| gluuConfDynamic |	directoryString |	TEXT	| STRING(MAX)	|
| gluuConfStatic	| directoryString	| TEXT	| STRING(MAX)	|

### gluuAttribute
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| gluuAttributeName	| directoryString |	VARCHAR(64)	| STRING(64)	|
| gluuAttributeOrigin	| directoryString	| VARCHAR(64)	| STRING(64)	|
| gluuAttributeType	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthClaimName	| directoryString |	VARCHAR(64)	| STRING(64)	|
| gluuSAML1URI	| directoryString	| VARCHAR(64)	| STRING(64)	|
| gluuSAML2URI	| directoryString	| VARCHAR(64)	| STRING(64) |
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxValidation |	directoryString	| TINYTEXT	| STRING(MAX)	| 
| urn	| directoryString	| VARCHAR(128)	| STRING(128)	|

### gluuConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| o	| directoryString	| VARCHAR(64)	| STRING(64) |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthenticationMode	| directoryString |	VARCHAR(64) |	STRING(64) |
| oxCacheConfiguration	| directoryString	| TEXT	| STRING(MAX)	|
| oxDocumentStoreConfiguration	| directoryString	| TEXT	| STRING(MAX)	|
| oxIDPAuthentication	| directoryString	| JSON	| ARRAY<STRING(MAX)>	|
| oxLogViewerConfig	| directoryString	| TEXT	| STRING(MAX)	|
| oxSmtpConfiguration	| directoryString	| JSON	| ARRAY<STRING(MAX)>	|
| userPassword	| directoryString	| VARCHAR(100)	| STRING(100)	|

### gluuCustomPerson
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|

### gluuGroup
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| member	| directoryString	| JSON	| ARRAY<STRING(MAX)>	|
| o	| directoryString	| VARCHAR(64)	| STRING(64) | 
| oxTrustMetaLocation	| directoryString	| TINYTEXT	| STRING(MAX)	|

### gluuInumMap
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### gluuInvoice
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### gluuOrganization
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| gluuOrgShortName	| directoryString	| VARCHAR(64)	| STRING(64)	|
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| gluuThemeColor	| directoryString	| VARCHAR(64)	| STRING(64)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| memberOf	| distinguishedName	| JSON	| ARRAY<STRING(MAX)>	|
| o	| directoryString	| VARCHAR(64)	| STRING(64) | 
| uid	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| userPassword	| directoryString	| VARCHAR(100)	| STRING(100)	|

### gluuOxtrustStat
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### gluuPerson
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| givenName |	directoryString	| VARCHAR(64)	| STRING(64) |
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| memberOf	| distinguishedName	| JSON	| ARRAY<STRING(MAX)>	|
| middleName	| directoryString	| VARCHAR(64)	| STRING(64)	|
| nickname	| directoryString	| VARCHAR(64)	| STRING(64)	|
| o	| directoryString	| VARCHAR(64)	| STRING(64) | 
| oxTrustMetaLocation	| directoryString	| TINYTEXT	| STRING(MAX)	|
| picture	| directoryString	| VARCHAR(96)	| STRING(96)	|
| sn	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| uid	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| userPassword	| directoryString	| VARCHAR(100)	| STRING(100)	|

### gluuSAMLconfig
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| o	| directoryString	| VARCHAR(64)	| STRING(64) |

### oxApplicationConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxConfApplication	| directoryString	| TEXT	| STRING(MAX)	| 

### oxAuthClient
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAccessTokenSigningAlg	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAttributes |	directoryString	| TEXT	| STRING(MAX) |
| oxAuthClientIdIssuedAt	| GeneralizedTime	| DATETIME(3)	| TIMESTAMP	|
| oxAuthClientSecret	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthClientURI	| directoryString |	TINYTEXT	| STRING(MAX)	|
| oxAuthGrantType	| directoryString	| JSON	| ARRAY<STRING(MAX)>	|
| oxAuthIdTokenSignedResponseAlg	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthInitiateLoginURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxAuthJwks	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthJwksURI	| directoryString	| TINYTEXT	| STRING(MAX) |
| oxAuthLogoURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxAuthLogoutURI	| directoryString	| TINYTEXT	| STRING(MAX) |
| oxAuthPolicyURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxAuthResponseType	| directoryString	| JSON	 | ARRAY<STRING(MAX)>	|
| oxAuthRequestURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxAuthSectorIdentifierURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxAuthSubjectType	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthTokenEndpointAuthMethod	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthTosURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxClaimRedirectURI	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxSoftwareStatement	| directoryString	| TEXT	| STRING(MAX)	| 
| tknBndCnf	| directoryString	| TINYTEXT	| STRING(MAX) |

### oxAuthConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthConfDynamic	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthConfErrors	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthConfStatic	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthConfWebKeys	| directoryString	| TEXT	| STRING(MAX)	|

### oxAuthCustomScope
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| oxAttributes |	directoryString	| TEXT	| STRING(MAX) |
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|
| oxScopeType |	directoryString	| VARCHAR(64)	| STRING(64)	| 

### oxAuthSessionId 
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxAuthPermissionGrantedMap	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthSessionAttribute	| directoryString	| TEXT	| STRING(MAX)	|
| oxAuthUserDN	| distinguishedName	| VARCHAR(128)	| STRING(128)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|
| oxInvolvedClients	| directoryString	| TEXT	| STRING(MAX)	|
| oxJwt	| directoryString	| TEXT	| STRING(MAX)	|
| oxSessionState	| directoryString	| TEXT	| STRING(MAX)	|

### oxAuthUmaPCT
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| clnId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| tknCde	| directoryString	| VARCHAR(80)	| STRING(80)	| 

### oxAuthUmaRPT
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| clnId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxUmaPermission	| directoryString |	JSON	| ARRAY<STRING(MAX)>	|
| tknCde	| directoryString	| VARCHAR(80)	| STRING(80)	| 

### oxClientAuthorization
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxAuthClientId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxCustomScript
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxScript	| directoryString	| TEXT	| STRING(MAX)	|
| oxScriptError	| directoryString	| TEXT	| STRING(MAX)	|
| oxScriptType	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| programmingLanguage	| directoryString	| VARCHAR(64)	| STRING(64)	|

### oxDeviceRegistration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| oxDeviceData	| directoryString	| TINYTEXT	| STRING(MAX)	|
| oxDeviceKeyHandle	| directoryString	| VARCHAR(96)	| STRING(96)	|
| oxDeviceRegistrationConf	| directoryString	| TEXT	| STRING(MAX)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|
| oxTrustMetaLocation	| directoryString	| TINYTEXT	| STRING(MAX)	|

### oxEntry
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### oxExpiredObject
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| dat	| directoryString	| TEXT |	STRING(MAX)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxFido2AuthenticationEntry
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxFido2RegistrationEntry
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|
| oxPublicKeyId	| directoryString	| VARCHAR(96)	| STRING(96)	|
| oxRegistrationData	| directoryString	| TEXT	| STRING(MAX)	|

### oxLink
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|

### oxMetric 
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxApplicationType	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxData	| directoryString	| TEXT	| STRING(MAX)	|

### oxPassportConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| gluuStatus	| directoryString	| VARCHAR(64)	| STRING(64)	|
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|

### oxProxClient
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### oxProxConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|

### oxProxOp
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	| 
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxPushApplication
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxPushDevice
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxRp
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| dat	| directoryString	| TEXT |	STRING(MAX)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxScript
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxScript	| directoryString	| TEXT	| STRING(MAX)	|
| oxScriptType	| directoryString	| VARCHAR(64)	| STRING(64)	| 

### oxSectorIdentifier
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| oxAuthClientId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxShibbolethCASProtocolConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxConfApplication	| directoryString	| TEXT	| STRING(MAX)	| 

### oxStatEntry
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| attr	| directoryString	| TEXT	| STRING(MAX)	|
| dat	| directoryString	| TEXT |	STRING(MAX)	| 

### oxTrustConfiguration
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxTrustConfApplication	| directoryString	| TEXT	| STRING(MAX)	|
| oxTrustConfCacheRefresh	| directoryString	| TEXT |	STRING(MAX) |
| oxTrustConfImportPerson	| directoryString	| TEXT	| STRING(MAX)	|

### oxU2fRequest
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### oxUmaResource
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| description	| directoryString	| VARCHAR(768)	| STRING(MAX)	|
| displayName	| directoryString	| VARCHAR(128) |	STRING(128)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxAuthUmaScope	| directoryString	| VARCHAR(128)	| STRING(128)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	| 
| oxResource	| directoryString |	TINYTEXT	| STRING(MAX) |
| oxScopeExpression	| directoryString	| TEXT	| STRING(MAX)	|

### oxUmaResourcePermission 
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxAttributes |	directoryString	| TEXT	| STRING(MAX) |
| oxAuthUmaScope	| directoryString	| VARCHAR(128)	| STRING(128)	|

### pairwiseIdentifier
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| oxAuthClientId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| oxId	| directoryString	| VARCHAR(128)	| STRING(128)	|

### samlAcr
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| classRef	| directoryString	| TEXT	| STRING(MAX)	|
| inum	| directoryString	| VARCHAR(64)	| STRING(64)	|

### token
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| acr	| directoryString	| VARCHAR(48)	| STRING(48)	|
| attr	| directoryString	| TEXT	| STRING(MAX)	|
| clnId	| directoryString	| VARCHAR(64)	| STRING(64)	|
| jwtReq	| directoryString	| TEXT	| STRING(MAX)	|
| nnc	| directoryString	| TEXT	| STRING(MAX)	|
| scp |	directoryString	| TEXT	| STRING(MAX)	|
| tknBndCnf	| directoryString	| TINYTEXT	| STRING(MAX) |
| tknCde	| directoryString	| VARCHAR(80)	| STRING(80)	| 
| tknTyp	| directoryString	| VARCHAR(32)	| STRING(32)	|

### vdapcontainer
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| ou	| directoryString	| VARCHAR(64)	| STRING(64)	|

### vdDirectoryView
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| o	| directoryString	| VARCHAR(64)	| STRING(64) |

### vdlabel
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| o	| directoryString	| VARCHAR(64)	| STRING(64) |

### No Table
| Name	| LDAP	| SQL	| Spanner	| 
| ---- | --- | --- | --- |
| doc_id		| | VARCHAR(64)	|STRING(64) |
| scimCustomSecond	|	| JSON	| ARRAY<STRING(MAX)> |
