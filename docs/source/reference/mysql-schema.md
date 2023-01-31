# MySQL Database Schema

## Cache

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|uuid|varchar(64)|DEFAULT|NULL|||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|dat||||||

## cibaRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|authReqId|varchar(64)|DEFAULT|NULL|||
|clnId|json|DEFAULT|NULL|||
|usrId|varchar(64)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|oxStatus|varchar(64)|DEFAULT|NULL|||

## GluuApplicationConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|gluuConfDynamic|text|||||
|gluuConfStatic|text|||||
|oxRevision|int|DEFAULT|NULL|||

## gluuAttribute

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|gluuAttributeEditType|json|DEFAULT|NULL|||
|gluuAttributeName|varchar(64)|DEFAULT|NULL|||
|gluuAttributeOrigin|varchar(64)|DEFAULT|NULL|||
|gluuAttributeSystemEditType|varchar(64)|DEFAULT|NULL|||
|gluuAttributeType|varchar(64)|DEFAULT|NULL|||
|oxAuthClaimName|varchar(64)|DEFAULT|NULL|||
|gluuAttributeUsageType|varchar(64)|DEFAULT|NULL|||
|gluuAttributeViewType|json|DEFAULT|NULL|||
|gluuCategory|varchar(64)|DEFAULT|NULL|||
|gluuSAML1URI|varchar(64)|DEFAULT|NULL|||
|gluuSAML2URI|varchar(64)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxMultivaluedAttribute|smallint|DEFAULT|NULL|||
|oxNameIdType|varchar(64)|DEFAULT|NULL|||
|oxSCIMCustomAttribute|smallint|DEFAULT|NULL|||
|oxSourceAttribute|varchar(64)|DEFAULT|NULL|||
|seeAlso|varchar(64)|DEFAULT|NULL|||
|urn|varchar(128)|DEFAULT|NULL|||
|gluuRegExp|varchar(64)|DEFAULT|NULL|||
|gluuTooltip|varchar(64)|DEFAULT|NULL|||
|oxValidation|tinytext|||||

## gluuConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|blowfishPassword|varchar(64)|DEFAULT|NULL|||
|c|varchar(2)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|gluuAdditionalBandwidth|varchar(64)|DEFAULT|NULL|||
|gluuAdditionalMemory|varchar(64)|DEFAULT|NULL|||
|gluuApplianceDnsServer|varchar(64)|DEFAULT|NULL|||
|gluuAppliancePollingInterval|varchar(64)|DEFAULT|NULL|||
|gluuBandwidthRX|varchar(64)|DEFAULT|NULL|||
|gluuBandwidthTX|varchar(64)|DEFAULT|NULL|||
|gluuDSstatus|varchar(64)|DEFAULT|NULL|||
|gluuFederationHostingEnabled|varchar(64)|DEFAULT|NULL|||
|gluuHTTPstatus|varchar(64)|DEFAULT|NULL|||
|gluuHostname|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceNo|varchar(64)|DEFAULT|NULL|||
|gluuLastUpdate|datetime(3)|DEFAULT|NULL|||
|gluuLifeRay|varchar(64)|DEFAULT|NULL|||
|gluuManageIdentityPermission|smallint|DEFAULT|NULL|||
|gluuManager|varchar(64)|DEFAULT|NULL|||
|gluuMaxLogSize|int|DEFAULT|NULL|||
|gluuOrgProfileMgt|smallint|DEFAULT|NULL|||
|gluuPaidUntil|varchar(64)|DEFAULT|NULL|||
|gluuPaymentProcessorTimestamp|varchar(64)|DEFAULT|NULL|||
|gluuPrivate|varchar(64)|DEFAULT|NULL|||
|gluuPublishIdpMetadata|varchar(64)|DEFAULT|NULL|||
|gluuResizeInitiated|varchar(64)|DEFAULT|NULL|||
|gluuSPTR|varchar(64)|DEFAULT|NULL|||
|gluuScimEnabled|smallint|DEFAULT|NULL|||
|gluuShibAssertionsIssued|varchar(64)|DEFAULT|NULL|||
|gluuShibFailedAuth|varchar(64)|DEFAULT|NULL|||
|gluuShibSecurityEvents|varchar(64)|DEFAULT|NULL|||
|gluuShibSuccessfulAuths|varchar(64)|DEFAULT|NULL|||
|oxTrustEmail|json|DEFAULT|NULL|||
|gluuSmtpFromEmailAddress|varchar(64)|DEFAULT|NULL|||
|gluuSmtpFromName|varchar(64)|DEFAULT|NULL|||
|gluuSmtpHost|varchar(64)|DEFAULT|NULL|||
|gluuSmtpPassword|varchar(64)|DEFAULT|NULL|||
|gluuSmtpPort|varchar(64)|DEFAULT|NULL|||
|gluuSmtpRequiresAuthentication|varchar(64)|DEFAULT|NULL|||
|gluuSmtpRequiresSsl|varchar(64)|DEFAULT|NULL|||
|gluuSmtpUserName|varchar(64)|DEFAULT|NULL|||
|gluuSslExpiry|varchar(64)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|gluuTargetRAM|varchar(64)|DEFAULT|NULL|||
|gluuUrl|varchar(64)|DEFAULT|NULL|||
|gluuVDSenabled|varchar(64)|DEFAULT|NULL|||
|gluuVDSstatus|varchar(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshEnabled|smallint|DEFAULT|NULL|||
|gluuVdsCacheRefreshLastUpdate|datetime(3)|DEFAULT|NULL|||
|gluuVdsCacheRefreshLastUpdateCount|varchar(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshPollingInterval|varchar(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshProblemCount|varchar(64)|DEFAULT|NULL|||
|gluuWhitePagesEnabled|varchar(64)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|inumFN|varchar(64)|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|oxAuthenticationMode|varchar(64)|DEFAULT|NULL|||
|oxTrustAuthenticationMode|varchar(64)|DEFAULT|NULL|||
|oxIDPAuthentication|json|DEFAULT|NULL|||
|oxLogViewerConfig|text|||||
|oxLogConfigLocation|varchar(64)|DEFAULT|NULL|||
|oxSmtpConfiguration|json|DEFAULT|NULL|||
|oxCacheConfiguration|text|||||
|oxDocumentStoreConfiguration|text|||||
|oxTrustStoreCert|varchar(64)|DEFAULT|NULL|||
|oxTrustStoreConf|varchar(64)|DEFAULT|NULL|||
|passwordResetAllowed|smallint|DEFAULT|NULL|||
|softwareVersion|varchar(64)|DEFAULT|NULL|||
|userPassword|varchar(256)|DEFAULT|NULL|||
|oxTrustCacheRefreshServerIpAddress|varchar(64)|DEFAULT|NULL|||
|gluuPassportEnabled|smallint|DEFAULT|NULL|||
|gluuRadiusEnabled|smallint|DEFAULT|NULL|||
|gluuSamlEnabled|smallint|DEFAULT|NULL|||
|gluuSmtpServerTrust|varchar(64)|DEFAULT|NULL|||
|gluuConfigurationPollingInterval|varchar(64)|DEFAULT|NULL|||
|gluuConfigurationDnsServer|varchar(64)|DEFAULT|NULL|||

## gluuGroup

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|c|varchar(2)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|gluuGroupType|varchar(64)|DEFAULT|NULL|||
|gluuGroupVisibility|varchar(64)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|member|json|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|owner|varchar(64)|DEFAULT|NULL|||
|seeAlso|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaCreated|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaLastModified|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|tinytext|||||
|oxTrustMetaVersion|varchar(64)|DEFAULT|NULL|||

## **gluuInumMap

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|primaryKeyAttrName|varchar(64)|DEFAULT|NULL|||
|primaryKeyValue|json|DEFAULT|NULL|||
|secondaryKeyAttrName|varchar(64)|DEFAULT|NULL|||
|secondaryKeyValue|json|DEFAULT|NULL|||
|tertiaryKeyAttrName|varchar(64)|DEFAULT|NULL|||
|tertiaryKeyValue|json|DEFAULT|NULL|||

## gluuInvoice

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|gluuInvoiceAmount|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceDate|datetime(3)|DEFAULT|NULL|||
|gluuInvoiceLineItemName|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceNumber|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceProductNumber|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceQuantity|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceStatus|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||

## gluuOrganization

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|c|varchar(2)|DEFAULT|NULL|||
|county|varchar(64)|DEFAULT|NULL|||
|deployedAppliances|varchar(64)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|gluuAddPersonCapability|varchar(64)|DEFAULT|NULL|||
|gluuAdditionalUsers|varchar(64)|DEFAULT|NULL|||
|gluuApplianceUpdateRequestList|varchar(64)|DEFAULT|NULL|||
|gluuCustomMessage|varchar(64)|DEFAULT|NULL|||
|gluuFaviconImage|varchar(64)|DEFAULT|NULL|||
|gluuFederationHostingEnabled|varchar(64)|DEFAULT|NULL|||
|gluuInvoiceNo|varchar(64)|DEFAULT|NULL|||
|gluuLogoImage|varchar(64)|DEFAULT|NULL|||
|gluuManageIdentityPermission|smallint|DEFAULT|NULL|||
|gluuManager|varchar(64)|DEFAULT|NULL|||
|gluuManagerGroup|tinytext|||||
|gluuOrgShortName|varchar(64)|DEFAULT|NULL|||
|gluuPaidUntil|varchar(64)|DEFAULT|NULL|||
|gluuPaymentProcessorTimestamp|varchar(64)|DEFAULT|NULL|||
|gluuProStoresUser|varchar(64)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|gluuTempFaviconImage|varchar(64)|DEFAULT|NULL|||
|gluuThemeColor|varchar(64)|DEFAULT|NULL|||
|gluuWhitePagesEnabled|varchar(64)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|l|varchar(64)|DEFAULT|NULL|||
|mail|varchar(96)|DEFAULT|NULL|||
|memberOf|json|DEFAULT|NULL|||
|nonProfit|smallint|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|oxCreationTimestamp|datetime(3)|DEFAULT|NULL|||
|oxLinkLinktrack|varchar(64)|DEFAULT|NULL|||
|oxLinktrackEnabled|varchar(64)|DEFAULT|NULL|||
|oxLinktrackLogin|varchar(64)|DEFAULT|NULL|||
|oxLinktrackPassword|varchar(64)|DEFAULT|NULL|||
|oxRegistrationConfiguration|text|||||
|postalCode|varchar(16)|DEFAULT|NULL|||
|proStoresToken|varchar(64)|DEFAULT|NULL|||
|prostoresTimestamp|varchar(64)|DEFAULT|NULL|||
|scimAuthMode|varchar(64)|DEFAULT|NULL|||
|scimGroup|tinytext|||||
|scimStatus|varchar(64)|DEFAULT|NULL|||
|st|varchar(64)|DEFAULT|NULL|||
|street|tinytext|||||
|telephoneNumber|varchar(20)|DEFAULT|NULL|||
|title|varchar(64)|DEFAULT|NULL|||
|uid|varchar(64)|DEFAULT|NULL|||
|userPassword|varchar(256)|DEFAULT|NULL|||
|oxTrustLogoPath|varchar(64)|DEFAULT|NULL|||
|oxTrustFaviconPath|varchar(64)|DEFAULT|NULL|||
|oxAuthLogoPath|varchar(64)|DEFAULT|NULL|||
|oxAuthFaviconPath|varchar(64)|DEFAULT|NULL|||
|idpLogoPath|varchar(64)|DEFAULT|NULL|||
|idpFaviconPath|varchar(64)|DEFAULT|NULL|||

## GluuOxtrustStat

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|gluuFreeDiskSpace|varchar(64)|DEFAULT|NULL|||
|gluuFreeMemory|varchar(64)|DEFAULT|NULL|||
|gluuFreeSwap|varchar(64)|DEFAULT|NULL|||
|gluuGroupCount|varchar(64)|DEFAULT|NULL|||
|gluuIpAddress|varchar(64)|DEFAULT|NULL|||
|gluuLoadAvg|varchar(64)|DEFAULT|NULL|||
|gluuPersonCount|varchar(64)|DEFAULT|NULL|||
|gluuSystemUptime|varchar(64)|DEFAULT|NULL|||
|uniqueIdentifier|varchar(64)|DEFAULT|NULL|||

## gluuPasswordResetRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|oxGuid|varchar(64)|DEFAULT|NULL|||
|personInum|varchar(64)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||

## gluuPerson

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|associatedClient|json|DEFAULT|NULL|||
|c|varchar(2)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|givenName|varchar(128)|DEFAULT|NULL|||
|gluuManagedOrganizations|varchar(64)|DEFAULT|NULL|||
|gluuOptOuts|json|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|gluuWhitePagesListed|varchar(64)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|NOT|NULL|||
|mail|varchar(96)|DEFAULT|NULL|||
|gluuSLAManager|smallint|DEFAULT|NULL|||
|memberOf|json|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|oxAuthPersistentJWT|varchar(64)|DEFAULT|NULL|||
|oxCreationTimestamp|datetime(3)|DEFAULT|NULL|||
|oxExternalUid|json|DEFAULT|NULL|||
|oxOTPCache|json|DEFAULT|NULL|||
|oxLastLogonTime|datetime(3)|DEFAULT|NULL|||
|oxTrustActive|smallint|DEFAULT|NULL|||
|oxTrustAddresses|json|DEFAULT|NULL|||
|oxTrustEmail|json|DEFAULT|NULL|||
|oxTrustEntitlements|json|DEFAULT|NULL|||
|oxTrustExternalId|varchar(128)|DEFAULT|NULL|||
|oxTrustImsValue|json|DEFAULT|NULL|||
|oxTrustMetaCreated|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaLastModified|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|tinytext|||||
|oxTrustMetaVersion|varchar(64)|DEFAULT|NULL|||
|oxTrustNameFormatted|tinytext|||||
|oxTrustPhoneValue|json|DEFAULT|NULL|||
|oxTrustPhotos|json|DEFAULT|NULL|||
|oxTrustProfileURL|varchar(256)|DEFAULT|NULL|||
|oxTrustRole|json|DEFAULT|NULL|||
|oxTrustTitle|varchar(64)|DEFAULT|NULL|||
|oxTrustUserType|varchar(64)|DEFAULT|NULL|||
|oxTrusthonorificPrefix|varchar(64)|DEFAULT|NULL|||
|oxTrusthonorificSuffix|varchar(64)|DEFAULT|NULL|||
|oxTrustx509Certificate|json|DEFAULT|NULL|||
|oxPasswordExpirationDate|datetime(3)|DEFAULT|NULL|||
|persistentId|varchar(64)|DEFAULT|NULL|||
|middleName|varchar(64)|DEFAULT|NULL|||
|nickname|varchar(64)|DEFAULT|NULL|||
|preferredUsername|varchar(64)|DEFAULT|NULL|||
|profile|varchar(64)|DEFAULT|NULL|||
|picture|tinytext|||||
|website|varchar(64)|DEFAULT|NULL|||
|emailVerified|smallint|DEFAULT|NULL|||
|gender|varchar(32)|DEFAULT|NULL|||
|birthdate|datetime(3)|DEFAULT|NULL|||
|zoneinfo|varchar(64)|DEFAULT|NULL|||
|locale|varchar(64)|DEFAULT|NULL|||
|phoneNumberVerified|smallint|DEFAULT|NULL|||
|address|tinytext|||||
|updatedAt|datetime(3)|DEFAULT|NULL|||
|preferredLanguage|varchar(64)|DEFAULT|NULL|||
|role|json|DEFAULT|NULL|||
|secretAnswer|tinytext|||||
|secretQuestion|tinytext|||||
|seeAlso|varchar(64)|DEFAULT|NULL|||
|sn|varchar(128)|DEFAULT|NULL|||
|cn|varchar(128)|DEFAULT|NULL|||
|transientId|varchar(64)|DEFAULT|NULL|||
|uid|varchar(64)|DEFAULT|NULL|||
|userPassword|varchar(256)|DEFAULT|NULL|||
|st|varchar(64)|DEFAULT|NULL|||
|street|tinytext|||||
|l|varchar(64)|DEFAULT|NULL|||
|oxCountInvalidLogin|varchar(64)|DEFAULT|NULL|||
|oxEnrollmentCode|varchar(64)|DEFAULT|NULL|||
|gluuIMAPData|varchar(64)|DEFAULT|NULL|||
|oxPPID|json|DEFAULT|NULL|||
|oxGuid|varchar(64)|DEFAULT|NULL|||
|userRandomKey|varchar(64)|DEFAULT|NULL|||
|oxPreferredMethod|varchar(64)|DEFAULT|NULL|||
|userCertificate|blob|||||
|oxOTPDevices|varchar(512)|DEFAULT|NULL|||
|oxMobileDevices|varchar(512)|DEFAULT|NULL|||
|oxStrongAuthPolicy|varchar(64)|DEFAULT|NULL|||
|oxTrustedDevicesInfo|text|||||
|oxUnlinkedExternalUids|varchar(64)|DEFAULT|NULL|||
|oxAuthBackchannelDeviceRegistrationToken|varchar(64)|DEFAULT|NULL|||
|oxAuthBackchannelUserCode|varchar(64)|DEFAULT|NULL|||
|oxEmailAlternate|varchar(64)|DEFAULT|NULL|||
|telephoneNumber|varchar(20)|DEFAULT|NULL|||
|mobile|json|DEFAULT|NULL|||
|carLicense|varchar(64)|DEFAULT|NULL|||
|facsimileTelephoneNumber|varchar(20)|DEFAULT|NULL|||
|departmentNumber|varchar(64)|DEFAULT|NULL|||
|employeeType|varchar(64)|DEFAULT|NULL|||
|manager|tinytext|||||
|postOfficeBox|varchar(64)|DEFAULT|NULL|||
|employeeNumber|varchar(64)|DEFAULT|NULL|||
|preferredDeliveryMethod|varchar(50)|DEFAULT|NULL|||
|roomNumber|varchar(64)|DEFAULT|NULL|||
|secretary|tinytext|||||
|homePostalAddress|tinytext|||||
|postalCode|varchar(16)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|title|varchar(64)|DEFAULT|NULL|||
|oxBiometricDevices|json|DEFAULT|NULL|||
|oxDuoDevices|json|DEFAULT|NULL|||
|eduPersonAffiliation|json|DEFAULT|NULL|||
|eduPersonNickName|varchar(64)|DEFAULT|NULL|||
|eduPersonOrgDN|varchar(64)|DEFAULT|NULL|||
|eduPersonOrgUnitDN|json|DEFAULT|NULL|||
|eduPersonPrimaryAffiliation|json|DEFAULT|NULL|||
|eduPersonPrincipalName|varchar(64)|DEFAULT|NULL|||
|eduPersonEntitlement|json|DEFAULT|NULL|||
|eduPersonPrimaryOrgUnitDN|json|DEFAULT|NULL|||
|eduPersonScopedAffiliation|json|DEFAULT|NULL|||
|eduPersonTargetedID|varchar(64)|DEFAULT|NULL|||
|eduPersonAssurance|varchar(64)|DEFAULT|NULL|||
|eduPersonPrincipalNamePrior|varchar(64)|DEFAULT|NULL|||
|eduPersonUniqueId|varchar(64)|DEFAULT|NULL|||
|eduPersonOrcid|json|DEFAULT|NULL|||

## gluuSAMLconfig

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|federationRules|varchar(64)|DEFAULT|NULL|||
|gluuContainerFederation|tinytext|||||
|gluuEntityId|json|DEFAULT|NULL|||
|gluuIsFederation|varchar(64)|DEFAULT|NULL|||
|gluuProfileConfiguration|json|DEFAULT|NULL|||
|gluuReleasedAttribute|json|DEFAULT|NULL|||
|gluuRulesAccepted|varchar(64)|DEFAULT|NULL|||
|gluuSAMLMetaDataFilter|json|DEFAULT|NULL|||
|gluuSAMLTrustEngine|varchar(64)|DEFAULT|NULL|||
|gluuSAMLmaxRefreshDelay|varchar(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataFN|varchar(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataSourceType|varchar(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataURL|varchar(64)|DEFAULT|NULL|||
|gluuSpecificRelyingPartyConfig|varchar(64)|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||
|gluuTrustContact|json|DEFAULT|NULL|||
|gluuTrustDeconstruction|json|DEFAULT|NULL|||
|gluuValidationLog|json|DEFAULT|NULL|||
|gluuValidationStatus|varchar(64)|DEFAULT|NULL|||
|iname|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|oxAuthPostLogoutRedirectURI|json|DEFAULT|NULL|||
|url|varchar(64)|DEFAULT|NULL|||
|researchAndScholarshipEnabled|varchar(64)|DEFAULT|NULL|||
|gluuEntityType|varchar(64)|DEFAULT|NULL|||

## jansStatEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|jansId|varchar(64)|DEFAULT|NULL|||
|dat|text|||||
|attr|text|||||

## oxApplicationConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|oxConfApplication|text|||||
|oxRevision|int|DEFAULT|NULL|||

## oxAuthClient

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|o|varchar(64)|DEFAULT|NULL|||
|associatedPerson|json|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxAuthAppType|varchar(64)|DEFAULT|NULL|||
|oxAuthClientIdIssuedAt|datetime(3)|DEFAULT|NULL|||
|oxAuthClientSecret|varchar(64)|DEFAULT|NULL|||
|oxAuthClientSecretExpiresAt|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|oxAuthClientURI|tinytext|||||
|oxAuthContact|json|DEFAULT|NULL|||
|oxAuthDefaultAcrValues|json|DEFAULT|NULL|||
|oxAuthDefaultMaxAge|int|DEFAULT|NULL|||
|oxAuthGrantType|json|DEFAULT|NULL|||
|oxAuthIdTokenEncryptedResponseAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthIdTokenEncryptedResponseEnc|varchar(64)|DEFAULT|NULL|||
|oxAuthIdTokenSignedResponseAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthInitiateLoginURI|tinytext|||||
|oxAuthJwksURI|tinytext|||||
|oxAuthJwks|text|||||
|oxAuthLogoURI|tinytext|||||
|oxAuthPolicyURI|tinytext|||||
|oxAuthPostLogoutRedirectURI|json|DEFAULT|NULL|||
|oxAuthRedirectURI|json|DEFAULT|NULL|||
|oxAuthRegistrationAccessToken|varchar(64)|DEFAULT|NULL|||
|oxAuthRequestObjectSigningAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthRequestObjectEncryptionAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthRequestObjectEncryptionEnc|varchar(64)|DEFAULT|NULL|||
|oxAuthRequestURI|json|DEFAULT|NULL|||
|oxAuthRequireAuthTime|smallint|DEFAULT|NULL|||
|oxAuthResponseType|json|DEFAULT|NULL|||
|oxAuthScope|json|DEFAULT|NULL|||
|oxAuthClaim|json|DEFAULT|NULL|||
|oxAuthSectorIdentifierURI|tinytext|||||
|oxAuthSignedResponseAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthSubjectType|varchar(64)|DEFAULT|NULL|||
|oxAuthTokenEndpointAuthMethod|varchar(64)|DEFAULT|NULL|||
|oxAuthTokenEndpointAuthSigningAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthTosURI|tinytext|||||
|oxAuthTrustedClient|smallint|DEFAULT|NULL|||
|oxAuthUserInfoEncryptedResponseAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthUserInfoEncryptedResponseEnc|varchar(64)|DEFAULT|NULL|||
|oxAuthExtraConf|varchar(64)|DEFAULT|NULL|||
|oxClaimRedirectURI|tinytext|||||
|oxLastAccessTime|datetime(3)|DEFAULT|NULL|||
|oxLastLogonTime|datetime(3)|DEFAULT|NULL|||
|oxPersistClientAuthorizations|smallint|DEFAULT|NULL|||
|oxIncludeClaimsInIdToken|smallint|DEFAULT|NULL|||
|oxRefreshTokenLifetime|int|DEFAULT|NULL|||
|oxDisabled|smallint|DEFAULT|NULL|||
|oxAuthLogoutURI|json|DEFAULT|NULL|||
|oxAuthLogoutSessionRequired|smallint|DEFAULT|NULL|||
|oxdId|varchar(64)|DEFAULT|NULL|||
|oxAuthAuthorizedOrigins|varchar(64)|DEFAULT|NULL|||
|tknBndCnf|tinytext|||||
|oxAccessTokenAsJwt|smallint|DEFAULT|NULL|||
|oxAccessTokenSigningAlg|varchar(64)|DEFAULT|NULL|||
|oxAccessTokenLifetime|int|DEFAULT|NULL|||
|oxSoftwareId|varchar(64)|DEFAULT|NULL|||
|oxSoftwareVersion|varchar(64)|DEFAULT|NULL|||
|oxSoftwareStatement|text|||||
|oxRptAsJwt|smallint|DEFAULT|NULL|||
|oxAttributes|text|||||
|oxAuthBackchannelTokenDeliveryMode|varchar(64)|DEFAULT|NULL|||
|oxAuthBackchannelClientNotificationEndpoint|varchar(64)|DEFAULT|NULL|||
|oxAuthBackchannelAuthenticationRequestSigningAlg|varchar(64)|DEFAULT|NULL|||
|oxAuthBackchannelUserCodeParameter|smallint|DEFAULT|NULL|||

## oxAuthConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|oxAuthConfDynamic|text|||||
|oxAuthConfErrors|text|||||
|oxAuthConfStatic|text|||||
|oxAuthConfWebKeys|text|||||
|oxRevision|int|DEFAULT|NULL|||
|oxWebKeysSettings|varchar(64)|DEFAULT|NULL|||

## oxAuthCustomScope

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|defaultScope|smallint|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxScopeType|varchar(64)|DEFAULT|NULL|||
|oxAuthClaim|json|DEFAULT|NULL|||
|oxScriptDn|json|DEFAULT|NULL|||
|oxAuthGroupClaims|smallint|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxIconUrl|varchar(64)|DEFAULT|NULL|||
|oxUmaPolicyScriptDn|tinytext|||||
|oxAttributes|text|||||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||

## oxAuthGrant

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|grtId|varchar(64)|DEFAULT|NULL|||
|iat|datetime(3)|DEFAULT|NULL|||

## oxAuthSessionId

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|sid|varchar(64)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|oxLastAccessTime|datetime(3)|DEFAULT|NULL|||
|oxAuthUserDN|varchar(128)|DEFAULT|NULL|||
|authnTime|datetime(3)|DEFAULT|NULL|||
|oxState|varchar(64)|DEFAULT|NULL|||
|oxSessionState|text|||||
|oxAuthPermissionGranted|smallint|DEFAULT|NULL|||
|oxAsJwt|smallint|DEFAULT|NULL|||
|oxJwt|text|||||
|oxAuthPermissionGrantedMap|text|||||
|oxInvolvedClients|text|||||
|oxAuthSessionAttribute|text|||||

## oxAuthUmaPCT

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|clnId|json|DEFAULT|NULL|||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|tknCde|varchar(80)|DEFAULT|NULL|||
|ssnId|varchar(64)|DEFAULT|NULL|||
|oxClaimValues|varchar(64)|DEFAULT|NULL|||

## oxAuthUmaRPT

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|authnTime|datetime(3)|DEFAULT|NULL|||
|clnId|json|DEFAULT|NULL|||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|tknCde|varchar(80)|DEFAULT|NULL|||
|usrId|varchar(64)|DEFAULT|NULL|||
|ssnId|varchar(64)|DEFAULT|NULL|||
|oxUmaPermission|json|DEFAULT|NULL|||
|uuid|varchar(64)|DEFAULT|NULL|||
|authzCode|varchar(64)|DEFAULT|NULL|||
|grtId|varchar(64)|DEFAULT|NULL|||
|grtTyp|varchar(64)|DEFAULT|NULL|||
|jwtReq|text|||||
|nnc|text|||||
|scp|text|||||
|tknTyp|varchar(32)|DEFAULT|NULL|||
|acr|varchar(48)|DEFAULT|NULL|||
|chlng|varchar(64)|DEFAULT|NULL|||
|chlngMth|varchar(64)|DEFAULT|NULL|||
|clms|varchar(64)|DEFAULT|NULL|||
|attr|text|||||
|tknBndCnf|tinytext|||||

## oxClientAuthorization

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(100)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxAuthClientId|json|DEFAULT|NULL|||
|oxAuthUserId|varchar(64)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|oxAuthScope|json|DEFAULT|NULL|||

## oxCustomScript

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|oxScript|text|||||
|oxScriptType|varchar(64)|DEFAULT|NULL|||
|programmingLanguage|varchar(64)|DEFAULT|NULL|||
|oxModuleProperty|json|DEFAULT|NULL|||
|oxConfigurationProperty|json|DEFAULT|NULL|||
|oxLevel|int|DEFAULT|NULL|||
|oxRevision|int|DEFAULT|NULL|||
|oxEnabled|smallint|DEFAULT|NULL|||
|oxScriptError|text|||||
|oxAlias|json|DEFAULT|NULL|||

## oxDeviceRegistration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|oxDeviceKeyHandle|varchar(128)|DEFAULT|NULL|||
|oxDeviceHashCode|int|DEFAULT|NULL|||
|oxApplication|varchar(64)|DEFAULT|NULL|||
|oxDeviceRegistrationConf|text|||||
|oxDeviceNotificationConf|varchar(64)|DEFAULT|NULL|||
|oxNickName|varchar(64)|DEFAULT|NULL|||
|oxDeviceData|text|||||
|oxCounter|int|DEFAULT|NULL|||
|oxStatus|varchar(64)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|personInum|varchar(64)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|oxLastAccessTime|datetime(3)|DEFAULT|NULL|||
|oxTrustMetaLastModified|varchar(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|tinytext|||||
|oxTrustMetaVersion|varchar(64)|DEFAULT|NULL|||

## oxDocument

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|document|text|||||
|creationDate|datetime(3)|DEFAULT|NULL|||
|oxModuleProperty|json|DEFAULT|NULL|||
|oxLevel|int|DEFAULT|NULL|||
|oxRevision|int|DEFAULT|NULL|||
|oxEnabled|smallint|DEFAULT|NULL|||
|oxAlias|json|DEFAULT|NULL|||

## oxExpiredObject

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|dat|text|||||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|oxType|varchar(64)|DEFAULT|NULL|||

## oxFido2AuthenticationEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|oxSessionStateId|varchar(64)|DEFAULT|NULL|||
|oxCodeChallenge|varchar(64)|DEFAULT|NULL|||
|personInum|varchar(64)|DEFAULT|NULL|||
|oxAuthenticationData|text|||||
|oxStatus|varchar(64)|DEFAULT|NULL|||

## oxFido2RegistrationEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|oxSessionStateId|varchar(64)|DEFAULT|NULL|||
|oxCodeChallenge|varchar(64)|DEFAULT|NULL|||
|oxCodeChallengeHash|varchar(64)|DEFAULT|NULL|||
|oxPublicKeyId|varchar(96)|DEFAULT|NULL|||
|personInum|varchar(64)|DEFAULT|NULL|||
|oxRegistrationData|text|||||
|oxDeviceNotificationConf|varchar(64)|DEFAULT|NULL|||
|oxCounter|int|DEFAULT|NULL|||
|oxStatus|varchar(64)|DEFAULT|NULL|||

## oxMetric

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|uniqueIdentifier|varchar(64)|DEFAULT|NULL|||
|oxStartDate|datetime(3)|DEFAULT|NULL|||
|oxEndDate|datetime(3)|DEFAULT|NULL|||
|oxApplicationType|varchar(64)|DEFAULT|NULL|||
|oxMetricType|varchar(64)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|oxData|text|||||
|oxHost|varchar(64)|DEFAULT|NULL|||

## oxNode

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|organizationalOwner|tinytext|||||
|owner|varchar(64)|DEFAULT|NULL|||
|sourceRelationalXdiStatement|varchar(64)|DEFAULT|NULL|||
|targetRelationalXdiStatement|varchar(64)|DEFAULT|NULL|||
|x|varchar(64)|DEFAULT|NULL|||
|xdiStatement|varchar(64)|DEFAULT|NULL|||
|xri|varchar(64)|DEFAULT|NULL|||

## oxPassportConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|gluuPassportConfiguration|json|DEFAULT|NULL|||
|gluuStatus|varchar(16)|DEFAULT|NULL|||

## oxPushDevice

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxAuthUserId|varchar(64)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxPushApplication|tinytext|||||
|oxPushDeviceConf|varchar(64)|DEFAULT|NULL|||
|oxType|varchar(64)|DEFAULT|NULL|||

## OxRadiusClient

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxRadiusClientName|varchar(64)|DEFAULT|NULL|||
|oxRadiusClientIpAddress|varchar(64)|DEFAULT|NULL|||
|oxRadiusClientSecret|varchar(64)|DEFAULT|NULL|||
|oxRadiusClientSortPriority|int|DEFAULT|NULL|||

## oxRadiusServerConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|oxRadiusListenInterface|varchar(64)|DEFAULT|NULL|||
|oxRadiusAuthenticationPort|int|DEFAULT|NULL|||
|oxRadiusAccountingPort|int|DEFAULT|NULL|||
|oxRadiusOpenIdBaseUrl|varchar(64)|DEFAULT|NULL|||
|oxRadiusOpenIdUsername|varchar(64)|DEFAULT|NULL|||
|oxRadiusOpenIdPassword|varchar(64)|DEFAULT|NULL|||
|oxRadiusAcrValue|varchar(64)|DEFAULT|NULL|||
|oxRadiusAuthScope|varchar(64)|DEFAULT|NULL|||
|oxRadiusAuthenticationTimeout|int|DEFAULT|NULL|||

## oxRp

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|dat|text|||||

## oxScript

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxScript|text|||||
|oxScriptType|varchar(64)|DEFAULT|NULL|||

## oxSectorIdentifier

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||
|oxAuthRedirectURI|json|DEFAULT|NULL|||
|oxAuthClientId|json|DEFAULT|NULL|||

## oxShibbolethCASProtocolConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|uniqueIdentifier|varchar(64)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|oxConfApplication|text|||||
|oxRevision|int|DEFAULT|NULL|||

## oxTrustConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|ou|varchar(64)|DEFAULT|NULL|||
|oxTrustConfApplication|text|||||
|oxTrustConfCacheRefresh|text|||||
|oxRevision|int|DEFAULT|NULL|||
|oxTrustConfImportPerson|text|||||
|oxTrustConfAttributeResolver|text|||||

## oxTrustedIdp

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|remoteIdpName|varchar(64)|DEFAULT|NULL|||
|remoteIdpHost|varchar(64)|DEFAULT|NULL|||
|supportedSingleSignOnServices|varchar(64)|DEFAULT|NULL|||
|selectedSingleSignOnService|varchar(64)|DEFAULT|NULL|||
|signingCertificates|varchar(64)|DEFAULT|NULL|||

## oxU2fRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxRequestId|varchar(64)|DEFAULT|NULL|||
|oxRequest|text|||||
|oxSessionStateId|varchar(64)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|personInum|varchar(64)|DEFAULT|NULL|||
|creationDate|datetime(3)|DEFAULT|NULL|||

## oxUmaResource

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|displayName|varchar(128)|DEFAULT|NULL|||
|inum|varchar(64)|DEFAULT|NULL|||
|owner|varchar(64)|DEFAULT|NULL|||
|oxAssociatedClient|json|DEFAULT|NULL|||
|oxAuthUmaScope|json|DEFAULT|NULL|||
|oxFaviconImage|varchar(64)|DEFAULT|NULL|||
|oxGroup|varchar(64)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxResource|tinytext|||||
|oxRevision|int|DEFAULT|NULL|||
|oxType|varchar(64)|DEFAULT|NULL|||
|oxScopeExpression|text|||||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|description|varchar(768)|DEFAULT|NULL|||

## oxUmaResourcePermission

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|oxAuthUmaScope|json|DEFAULT|NULL|||
|oxConfigurationCode|varchar(64)|DEFAULT|NULL|||
|oxResourceSetId|varchar(64)|DEFAULT|NULL|||
|oxAttributes|text|||||
|oxTicket|varchar(64)|DEFAULT|NULL|||
|oxStatus|varchar(64)|DEFAULT|NULL|||

## PairwiseIdentifier

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|oxId|varchar(128)|DEFAULT|NULL|||
|oxSectorIdentifier|varchar(64)|DEFAULT|NULL|||
|oxAuthClientId|json|DEFAULT|NULL|||
|oxAuthUserId|varchar(64)|DEFAULT|NULL|||

## SamlAcr

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|parent|varchar(64)|DEFAULT|NULL|||
|classRef|text|||||
|inum|varchar(64)|DEFAULT|NULL|||

## token

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|varchar(64)|NOT|NULL||PRI|
|objectClass|varchar(48)|DEFAULT|NULL|||
|dn|varchar(128)|DEFAULT|NULL|||
|authnTime|datetime(3)|DEFAULT|NULL|||
|authzCode|varchar(64)|DEFAULT|NULL|||
|iat|datetime(3)|DEFAULT|NULL|||
|exp|datetime(3)|DEFAULT|NULL|||
|del|smallint|DEFAULT|NULL|||
|grtId|varchar(64)|DEFAULT|NULL|||
|grtTyp|varchar(64)|DEFAULT|NULL|||
|jwtReq|text|||||
|nnc|text|||||
|scp|text|||||
|tknCde|varchar(80)|DEFAULT|NULL|||
|tknTyp|varchar(32)|DEFAULT|NULL|||
|usrId|varchar(64)|DEFAULT|NULL|||
|clnId|json|DEFAULT|NULL|||
|acr|varchar(48)|DEFAULT|NULL|||
|uuid|varchar(64)|DEFAULT|NULL|||
|chlng|varchar(64)|DEFAULT|NULL|||
|chlngMth|varchar(64)|DEFAULT|NULL|||
|clms|varchar(64)|DEFAULT|NULL|||
|ssnId|varchar(64)|DEFAULT|NULL|||
|attr|text|||||
|tknBndCnf|tinytext|||||
