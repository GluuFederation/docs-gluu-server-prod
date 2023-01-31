# PostgreSQL Database Schema

## Cache

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|uuid|character varying(64)|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|dat|boolean|DEFAULT|NULL|||

## cibaRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|authReqId|character varying(64)|DEFAULT|NULL|||
|clnId|jsonb|DEFAULT|NULL|||
|usrId|character varying(64)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|oxStatus|character varying(64)|DEFAULT|NULL|||

## GluuApplicationConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|gluuConfDynamic|text|||||
|gluuConfStatic|text|||||
|oxRevision|integer|DEFAULT|NULL|||

## gluuAttribute

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|gluuAttributeEditType|jsonb|DEFAULT|NULL|||
|gluuAttributeName|character varying(64)|DEFAULT|NULL|||
|gluuAttributeOrigin|character varying(64)|DEFAULT|NULL|||
|gluuAttributeSystemEditType|character varying(64)|DEFAULT|NULL|||
|gluuAttributeType|character varying(64)|DEFAULT|NULL|||
|oxAuthClaimName|character varying(64)|DEFAULT|NULL|||
|gluuAttributeUsageType|character varying(64)|DEFAULT|NULL|||
|gluuAttributeViewType|jsonb|DEFAULT|NULL|||
|gluuCategory|character varying(64)|DEFAULT|NULL|||
|gluuSAML1URI|character varying(64)|DEFAULT|NULL|||
|gluuSAML2URI|character varying(64)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxMultivaluedAttribute|boolean|DEFAULT|NULL|||
|oxNameIdType|character varying(64)|DEFAULT|NULL|||
|oxSCIMCustomAttribute|boolean|DEFAULT|NULL|||
|oxSourceAttribute|character varying(64)|DEFAULT|NULL|||
|seeAlso|character varying(64)|DEFAULT|NULL|||
|urn|character varying(128)|DEFAULT|NULL|||
|gluuRegExp|character varying(64)|DEFAULT|NULL|||
|gluuTooltip|character varying(64)|DEFAULT|NULL|||
|oxValidation|text|DEFAULT|NULL|||

## gluuConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|blowfishPassword|character varying(64)|DEFAULT|NULL|||
|c|character varying(2)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|gluuAdditionalBandwidth|character varying(64)|DEFAULT|NULL|||
|gluuAdditionalMemory|character varying(64)|DEFAULT|NULL|||
|gluuApplianceDnsServer|character varying(64)|DEFAULT|NULL|||
|gluuAppliancePollingintegererval|character varying(64)|DEFAULT|NULL|||
|gluuBandwidthRX|character varying(64)|DEFAULT|NULL|||
|gluuBandwidthTX|character varying(64)|DEFAULT|NULL|||
|gluuDSstatus|character varying(64)|DEFAULT|NULL|||
|gluuFederationHostingEnabled|character varying(64)|DEFAULT|NULL|||
|gluuHTTPstatus|character varying(64)|DEFAULT|NULL|||
|gluuHostname|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceNo|character varying(64)|DEFAULT|NULL|||
|gluuLastUpdate|timestamp without time zone(3)|DEFAULT|NULL|||
|gluuLifeRay|character varying(64)|DEFAULT|NULL|||
|gluuManageIdentityPermission|boolean|DEFAULT|NULL|||
|gluuManager|character varying(64)|DEFAULT|NULL|||
|gluuMaxLogSize|integer|DEFAULT|NULL|||
|gluuOrgProfileMgt|boolean|DEFAULT|NULL|||
|gluuPaidUntil|character varying(64)|DEFAULT|NULL|||
|gluuPaymentProcessorTimestamp|character varying(64)|DEFAULT|NULL|||
|gluuPrivate|character varying(64)|DEFAULT|NULL|||
|gluuPublishIdpMetadata|character varying(64)|DEFAULT|NULL|||
|gluuResizeInitiated|character varying(64)|DEFAULT|NULL|||
|gluuSPTR|character varying(64)|DEFAULT|NULL|||
|gluuScimEnabled|boolean|DEFAULT|NULL|||
|gluuShibAssertionsIssued|character varying(64)|DEFAULT|NULL|||
|gluuShibFailedAuth|character varying(64)|DEFAULT|NULL|||
|gluuShibSecurityEvents|character varying(64)|DEFAULT|NULL|||
|gluuShibSuccessfulAuths|character varying(64)|DEFAULT|NULL|||
|oxTrustEmail|jsonb|DEFAULT|NULL|||
|gluuSmtpFromEmailAddress|character varying(64)|DEFAULT|NULL|||
|gluuSmtpFromName|character varying(64)|DEFAULT|NULL|||
|gluuSmtpHost|character varying(64)|DEFAULT|NULL|||
|gluuSmtpPassword|character varying(64)|DEFAULT|NULL|||
|gluuSmtpPort|character varying(64)|DEFAULT|NULL|||
|gluuSmtpRequiresAuthentication|character varying(64)|DEFAULT|NULL|||
|gluuSmtpRequiresSsl|character varying(64)|DEFAULT|NULL|||
|gluuSmtpUserName|character varying(64)|DEFAULT|NULL|||
|gluuSslExpiry|character varying(64)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|gluuTargetRAM|character varying(64)|DEFAULT|NULL|||
|gluuUrl|character varying(64)|DEFAULT|NULL|||
|gluuVDSenabled|character varying(64)|DEFAULT|NULL|||
|gluuVDSstatus|character varying(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshEnabled|boolean|DEFAULT|NULL|||
|gluuVdsCacheRefreshLastUpdate|timestamp without time zone(3)|DEFAULT|NULL|||
|gluuVdsCacheRefreshLastUpdateCount|character varying(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshPollingintegererval|character varying(64)|DEFAULT|NULL|||
|gluuVdsCacheRefreshProblemCount|character varying(64)|DEFAULT|NULL|||
|gluuWhitePagesEnabled|character varying(64)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|inumFN|character varying(64)|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|oxAuthenticationMode|character varying(64)|DEFAULT|NULL|||
|oxTrustAuthenticationMode|character varying(64)|DEFAULT|NULL|||
|oxIDPAuthentication|jsonb|DEFAULT|NULL|||
|oxLogViewerConfig|text|||||
|oxLogConfigLocation|character varying(64)|DEFAULT|NULL|||
|oxSmtpConfiguration|jsonb|DEFAULT|NULL|||
|oxCacheConfiguration|text|||||
|oxDocumentStoreConfiguration|text|||||
|oxTrustStoreCert|character varying(64)|DEFAULT|NULL|||
|oxTrustStoreConf|character varying(64)|DEFAULT|NULL|||
|passwordResetAllowed|boolean|DEFAULT|NULL|||
|softwareVersion|character varying(64)|DEFAULT|NULL|||
|userPassword|character varying(256)|DEFAULT|NULL|||
|oxTrustCacheRefreshServerIpAddress|character varying(64)|DEFAULT|NULL|||
|gluuPassportEnabled|boolean|DEFAULT|NULL|||
|gluuRadiusEnabled|boolean|DEFAULT|NULL|||
|gluuSamlEnabled|boolean|DEFAULT|NULL|||
|gluuSmtpServerTrust|character varying(64)|DEFAULT|NULL|||
|gluuConfigurationPollingintegererval|character varying(64)|DEFAULT|NULL|||
|gluuConfigurationDnsServer|character varying(64)|DEFAULT|NULL|||

## gluuGroup

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|c|character varying(2)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|gluuGroupType|character varying(64)|DEFAULT|NULL|||
|gluuGroupVisibility|character varying(64)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|member|jsonb|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|owner|character varying(64)|DEFAULT|NULL|||
|seeAlso|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaCreated|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaLastModified|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|text|||||
|oxTrustMetaVersion|character varying(64)|DEFAULT|NULL|||

## gluuInumMap

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|primaryKeyAttrName|character varying(64)|DEFAULT|NULL|||
|primaryKeyValue|jsonb|DEFAULT|NULL|||
|secondaryKeyAttrName|character varying(64)|DEFAULT|NULL|||
|secondaryKeyValue|jsonb|DEFAULT|NULL|||
|tertiaryKeyAttrName|character varying(64)|DEFAULT|NULL|||
|tertiaryKeyValue|jsonb|DEFAULT|NULL|||

## gluuInvoice

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|gluuInvoiceAmount|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceDate|timestamp without time zone(3)|DEFAULT|NULL|||
|gluuInvoiceLineItemName|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceNumber|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceProductNumber|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceQuantity|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceStatus|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||

## gluuOrganization

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|c|character varying(2)|DEFAULT|NULL|||
|county|character varying(64)|DEFAULT|NULL|||
|deployedAppliances|character varying(64)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|gluuAddPersonCapability|character varying(64)|DEFAULT|NULL|||
|gluuAdditionalUsers|character varying(64)|DEFAULT|NULL|||
|gluuApplianceUpdateRequestList|character varying(64)|DEFAULT|NULL|||
|gluuCustomMessage|character varying(64)|DEFAULT|NULL|||
|gluuFaviconImage|character varying(64)|DEFAULT|NULL|||
|gluuFederationHostingEnabled|character varying(64)|DEFAULT|NULL|||
|gluuInvoiceNo|character varying(64)|DEFAULT|NULL|||
|gluuLogoImage|character varying(64)|DEFAULT|NULL|||
|gluuManageIdentityPermission|boolean|DEFAULT|NULL|||
|gluuManager|character varying(64)|DEFAULT|NULL|||
|gluuManagerGroup|text|||||
|gluuOrgShortName|character varying(64)|DEFAULT|NULL|||
|gluuPaidUntil|character varying(64)|DEFAULT|NULL|||
|gluuPaymentProcessorTimestamp|character varying(64)|DEFAULT|NULL|||
|gluuProStoresUser|character varying(64)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|gluuTempFaviconImage|character varying(64)|DEFAULT|NULL|||
|gluuThemeColor|character varying(64)|DEFAULT|NULL|||
|gluuWhitePagesEnabled|character varying(64)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|l|character varying(64)|DEFAULT|NULL|||
|mail|character varying(96)|DEFAULT|NULL|||
|memberOf|jsonb|DEFAULT|NULL|||
|nonProfit|boolean|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|oxCreationTimestamp|timestamp without time zone(3)|DEFAULT|NULL|||
|oxLinkLinktrack|character varying(64)|DEFAULT|NULL|||
|oxLinktrackEnabled|character varying(64)|DEFAULT|NULL|||
|oxLinktrackLogin|character varying(64)|DEFAULT|NULL|||
|oxLinktrackPassword|character varying(64)|DEFAULT|NULL|||
|oxRegistrationConfiguration|text|||||
|postalCode|character varying(16)|DEFAULT|NULL|||
|proStoresToken|character varying(64)|DEFAULT|NULL|||
|prostoresTimestamp|character varying(64)|DEFAULT|NULL|||
|scimAuthMode|character varying(64)|DEFAULT|NULL|||
|scimGroup|text|||||
|scimStatus|character varying(64)|DEFAULT|NULL|||
|st|character varying(64)|DEFAULT|NULL|||
|street|text|||||
|telephoneNumber|character varying(20)|DEFAULT|NULL|||
|title|character varying(64)|DEFAULT|NULL|||
|uid|character varying(64)|DEFAULT|NULL|||
|userPassword|character varying(256)|DEFAULT|NULL|||
|oxTrustLogoPath|character varying(64)|DEFAULT|NULL|||
|oxTrustFaviconPath|character varying(64)|DEFAULT|NULL|||
|oxAuthLogoPath|character varying(64)|DEFAULT|NULL|||
|oxAuthFaviconPath|character varying(64)|DEFAULT|NULL|||
|idpLogoPath|character varying(64)|DEFAULT|NULL|||
|idpFaviconPath|character varying(64)|DEFAULT|NULL|||

## GluuOxtrustStat

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|gluuFreeDiskSpace|character varying(64)|DEFAULT|NULL|||
|gluuFreeMemory|character varying(64)|DEFAULT|NULL|||
|gluuFreeSwap|character varying(64)|DEFAULT|NULL|||
|gluuGroupCount|character varying(64)|DEFAULT|NULL|||
|gluuIpAddress|character varying(64)|DEFAULT|NULL|||
|gluuLoadAvg|character varying(64)|DEFAULT|NULL|||
|gluuPersonCount|character varying(64)|DEFAULT|NULL|||
|gluuSystemUptime|character varying(64)|DEFAULT|NULL|||
|uniqueIdentifier|character varying(64)|DEFAULT|NULL|||

## gluuPasswordResetRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxGuid|character varying(64)|DEFAULT|NULL|||
|personInum|character varying(64)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||

## gluuPerson

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|associatedClient|jsonb|DEFAULT|NULL|||
|c|character varying(2)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|givenName|character varying(128)|DEFAULT|NULL|||
|gluuManagedOrganizations|character varying(64)|DEFAULT|NULL|||
|gluuOptOuts|jsonb|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|gluuWhitePagesListed|character varying(64)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|NOT|NULL|||
|mail|character varying(96)|DEFAULT|NULL|||
|gluuSLAManager|boolean|DEFAULT|NULL|||
|memberOf|jsonb|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|oxAuthPersistentJWT|character varying(64)|DEFAULT|NULL|||
|oxCreationTimestamp|timestamp without time zone(3)|DEFAULT|NULL|||
|oxExternalUid|jsonb|DEFAULT|NULL|||
|oxOTPCache|jsonb|DEFAULT|NULL|||
|oxLastLogonTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxTrustActive|boolean|DEFAULT|NULL|||
|oxTrustAddresses|jsonb|DEFAULT|NULL|||
|oxTrustEmail|jsonb|DEFAULT|NULL|||
|oxTrustEntitlements|jsonb|DEFAULT|NULL|||
|oxTrustExternalId|character varying(128)|DEFAULT|NULL|||
|oxTrustImsValue|jsonb|DEFAULT|NULL|||
|oxTrustMetaCreated|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaLastModified|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|text|||||
|oxTrustMetaVersion|character varying(64)|DEFAULT|NULL|||
|oxTrustNameFormatted|text|||||
|oxTrustPhoneValue|jsonb|DEFAULT|NULL|||
|oxTrustPhotos|jsonb|DEFAULT|NULL|||
|oxTrustProfileURL|character varying(256)|DEFAULT|NULL|||
|oxTrustRole|jsonb|DEFAULT|NULL|||
|oxTrustTitle|character varying(64)|DEFAULT|NULL|||
|oxTrustUserType|character varying(64)|DEFAULT|NULL|||
|oxTrusthonorificPrefix|character varying(64)|DEFAULT|NULL|||
|oxTrusthonorificSuffix|character varying(64)|DEFAULT|NULL|||
|oxTrustx509Certificate|jsonb|DEFAULT|NULL|||
|oxPasswordExpirationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|persistentId|character varying(64)|DEFAULT|NULL|||
|middleName|character varying(64)|DEFAULT|NULL|||
|nickname|character varying(64)|DEFAULT|NULL|||
|preferredUsername|character varying(64)|DEFAULT|NULL|||
|profile|character varying(64)|DEFAULT|NULL|||
|picture|text|||||
|website|character varying(64)|DEFAULT|NULL|||
|emailVerified|boolean|DEFAULT|NULL|||
|gender|character varying(32)|DEFAULT|NULL|||
|birthdate|timestamp without time zone(3)|DEFAULT|NULL|||
|zoneinfo|character varying(64)|DEFAULT|NULL|||
|locale|character varying(64)|DEFAULT|NULL|||
|phoneNumberVerified|boolean|DEFAULT|NULL|||
|address|text|||||
|updatedAt|timestamp without time zone(3)|DEFAULT|NULL|||
|preferredLanguage|character varying(64)|DEFAULT|NULL|||
|role|jsonb|DEFAULT|NULL|||
|secretAnswer|text|DEFAULT|NULL|||
|secretQuestion|text|DEFAULT|NULL|||
|seeAlso|character varying(64)|DEFAULT|NULL|||
|sn|character varying(128)|DEFAULT|NULL|||
|cn|character varying(128)|DEFAULT|NULL|||
|transientId|character varying(64)|DEFAULT|NULL|||
|uid|character varying(64)|DEFAULT|NULL|||
|userPassword|character varying(256)|DEFAULT|NULL|||
|st|character varying(64)|DEFAULT|NULL|||
|street|text|||||
|l|character varying(64)|DEFAULT|NULL|||
|oxCountInvalidLogin|character varying(64)|DEFAULT|NULL|||
|oxEnrollmentCode|character varying(64)|DEFAULT|NULL|||
|gluuIMAPData|character varying(64)|DEFAULT|NULL|||
|oxPPID|jsonb|DEFAULT|NULL|||
|oxGuid|character varying(64)|DEFAULT|NULL|||
|userRandomKey|character varying(64)|DEFAULT|NULL|||
|oxPreferredMethod|character varying(64)|DEFAULT|NULL|||
|userCertificate|text|DEFAULT|NULL|||
|oxOTPDevices|character varying(512)|DEFAULT|NULL|||
|oxMobileDevices|character varying(512)|DEFAULT|NULL|||
|oxStrongAuthPolicy|character varying(64)|DEFAULT|NULL|||
|oxTrustedDevicesInfo|text|||||
|oxUnlinkedExternalUids|character varying(64)|DEFAULT|NULL|||
|oxAuthBackchannelDeviceRegistrationToken|character varying(64)|DEFAULT|NULL|||
|oxAuthBackchannelUserCode|character varying(64)|DEFAULT|NULL|||
|oxEmailAlternate|character varying(64)|DEFAULT|NULL|||
|telephoneNumber|character varying(20)|DEFAULT|NULL|||
|mobile|jsonb|DEFAULT|NULL|||
|carLicense|character varying(64)|DEFAULT|NULL|||
|facsimileTelephoneNumber|character varying(20)|DEFAULT|NULL|||
|departmentNumber|character varying(64)|DEFAULT|NULL|||
|employeeType|character varying(64)|DEFAULT|NULL|||
|manager|text|||||
|postOfficeBox|character varying(64)|DEFAULT|NULL|||
|employeeNumber|character varying(64)|DEFAULT|NULL|||
|preferredDeliveryMethod|character varying(50)|DEFAULT|NULL|||
|roomNumber|character varying(64)|DEFAULT|NULL|||
|secretary|text|DEFAULT|NULL|||
|homePostalAddress|text|DEFAULT|NULL|||
|postalCode|character varying(16)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|title|character varying(64)|DEFAULT|NULL|||
|oxBiometricDevices|jsonb|DEFAULT|NULL|||
|oxDuoDevices|jsonb|DEFAULT|NULL|||
|eduPersonAffiliation|jsonb|DEFAULT|NULL|||
|eduPersonNickName|character varying(64)|DEFAULT|NULL|||
|eduPersonOrgDN|character varying(64)|DEFAULT|NULL|||
|eduPersonOrgUnitDN|jsonb|DEFAULT|NULL|||
|eduPersonPrimaryAffiliation|jsonb|DEFAULT|NULL|||
|eduPersonPrincipalName|character varying(64)|DEFAULT|NULL|||
|eduPersonEntitlement|jsonb|DEFAULT|NULL|||
|eduPersonPrimaryOrgUnitDN|jsonb|DEFAULT|NULL|||
|eduPersonScopedAffiliation|jsonb|DEFAULT|NULL|||
|eduPersonTargetedID|character varying(64)|DEFAULT|NULL|||
|eduPersonAssurance|character varying(64)|DEFAULT|NULL|||
|eduPersonPrincipalNamePrior|character varying(64)|DEFAULT|NULL|||
|eduPersonUniqueId|character varying(64)|DEFAULT|NULL|||
|eduPersonOrcid|jsonb|DEFAULT|NULL|||

## gluuSAMLconfig

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|federationRules|character varying(64)|DEFAULT|NULL|||
|gluuContainerFederation|text|||||
|gluuEntityId|jsonb|DEFAULT|NULL|||
|gluuIsFederation|character varying(64)|DEFAULT|NULL|||
|gluuProfileConfiguration|jsonb|DEFAULT|NULL|||
|gluuReleasedAttribute|jsonb|DEFAULT|NULL|||
|gluuRulesAccepted|character varying(64)|DEFAULT|NULL|||
|gluuSAMLMetaDataFilter|jsonb|DEFAULT|NULL|||
|gluuSAMLTrustEngine|character varying(64)|DEFAULT|NULL|||
|gluuSAMLmaxRefreshDelay|character varying(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataFN|character varying(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataSourceType|character varying(64)|DEFAULT|NULL|||
|gluuSAMLspMetaDataURL|character varying(64)|DEFAULT|NULL|||
|gluuSpecificRelyingPartyConfig|character varying(64)|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||
|gluuTrustContact|jsonb|DEFAULT|NULL|||
|gluuTrustDeconstruction|jsonb|DEFAULT|NULL|||
|gluuValidationLog|jsonb|DEFAULT|NULL|||
|gluuValidationStatus|character varying(64)|DEFAULT|NULL|||
|iname|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|oxAuthPostLogoutRedirectURI|jsonb|DEFAULT|NULL|||
|url|character varying(64)|DEFAULT|NULL|||
|researchAndScholarshipEnabled|character varying(64)|DEFAULT|NULL|||
|gluuEntityType|character varying(64)|DEFAULT|NULL|||

## jansStatEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|jansId|character varying(64)|DEFAULT|NULL|||
|dat|text|||||
|attr|text|||||

## oxApplicationConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|oxConfApplication|text|||||
|oxRevision|integer|DEFAULT|NULL|||

## oxAuthClient

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|o|character varying(64)|DEFAULT|NULL|||
|associatedPerson|jsonb|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxAuthAppType|character varying(64)|DEFAULT|NULL|||
|oxAuthClientIdIssuedAt|timestamp without time zone(3)|DEFAULT|NULL|||
|oxAuthClientSecret|character varying(64)|DEFAULT|NULL|||
|oxAuthClientSecretExpiresAt|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|oxAuthClientURI|text|||||
|oxAuthContact|jsonb|DEFAULT|NULL|||
|oxAuthDefaultAcrValues|jsonb|DEFAULT|NULL|||
|oxAuthDefaultMaxAge|integer|DEFAULT|NULL|||
|oxAuthGrantType|jsonb|DEFAULT|NULL|||
|oxAuthIdTokenEncryptedResponseAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthIdTokenEncryptedResponseEnc|character varying(64)|DEFAULT|NULL|||
|oxAuthIdTokenSignedResponseAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthInitiateLoginURI|text|||||
|oxAuthJwksURI|text|||||
|oxAuthJwks|text|||||
|oxAuthLogoURI|text|||||
|oxAuthPolicyURI|text|||||
|oxAuthPostLogoutRedirectURI|jsonb|DEFAULT|NULL|||
|oxAuthRedirectURI|jsonb|DEFAULT|NULL|||
|oxAuthRegistrationAccessToken|character varying(64)|DEFAULT|NULL|||
|oxAuthRequestObjectSigningAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthRequestObjectEncryptionAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthRequestObjectEncryptionEnc|character varying(64)|DEFAULT|NULL|||
|oxAuthRequestURI|jsonb|DEFAULT|NULL|||
|oxAuthRequireAuthTime|boolean|DEFAULT|NULL|||
|oxAuthResponseType|jsonb|DEFAULT|NULL|||
|oxAuthScope|jsonb|DEFAULT|NULL|||
|oxAuthClaim|jsonb|DEFAULT|NULL|||
|oxAuthSectorIdentifierURI|text|||||
|oxAuthSignedResponseAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthSubjectType|character varying(64)|DEFAULT|NULL|||
|oxAuthTokenEndpointegerAuthMethod|character varying(64)|DEFAULT|NULL|||
|oxAuthTokenEndpointegerAuthSigningAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthTosURI|text|||||
|oxAuthTrustedClient|boolean|DEFAULT|NULL|||
|oxAuthUserInfoEncryptedResponseAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthUserInfoEncryptedResponseEnc|character varying(64)|DEFAULT|NULL|||
|oxAuthExtraConf|character varying(64)|DEFAULT|NULL|||
|oxClaimRedirectURI|text|||||
|oxLastAccessTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxLastLogonTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxPersistClientAuthorizations|boolean|DEFAULT|NULL|||
|oxIncludeClaimsInIdToken|boolean|DEFAULT|NULL|||
|oxRefreshTokenLifetime|integer|DEFAULT|NULL|||
|oxDisabled|boolean|DEFAULT|NULL|||
|oxAuthLogoutURI|jsonb|DEFAULT|NULL|||
|oxAuthLogoutSessionRequired|boolean|DEFAULT|NULL|||
|oxdId|character varying(64)|DEFAULT|NULL|||
|oxAuthAuthorizedOrigins|character varying(64)|DEFAULT|NULL|||
|tknBndCnf|text|||||
|oxAccessTokenAsJwt|boolean|DEFAULT|NULL|||
|oxAccessTokenSigningAlg|character varying(64)|DEFAULT|NULL|||
|oxAccessTokenLifetime|integer|DEFAULT|NULL|||
|oxSoftwareId|character varying(64)|DEFAULT|NULL|||
|oxSoftwareVersion|character varying(64)|DEFAULT|NULL|||
|oxSoftwareStatement|text|||||
|oxRptAsJwt|boolean|DEFAULT|NULL|||
|oxAttributes|text|||||
|oxAuthBackchannelTokenDeliveryMode|character varying(64)|DEFAULT|NULL|||
|oxAuthBackchannelClientNotificationEndpointeger|character varying(64)|DEFAULT|NULL|||
|oxAuthBackchannelAuthenticationRequestSigningAlg|character varying(64)|DEFAULT|NULL|||
|oxAuthBackchannelUserCodeParameter|boolean|DEFAULT|NULL|||

## oxAuthConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|oxAuthConfDynamic|text|||||
|oxAuthConfErrors|text|||||
|oxAuthConfStatic|text|||||
|oxAuthConfWebKeys|text|||||
|oxRevision|integer|DEFAULT|NULL|||
|oxWebKeysSettings|character varying(64)|DEFAULT|NULL|||

## oxAuthCustomScope

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|defaultScope|boolean|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxScopeType|character varying(64)|DEFAULT|NULL|||
|oxAuthClaim|jsonb|DEFAULT|NULL|||
|oxScriptDn|jsonb|DEFAULT|NULL|||
|oxAuthGroupClaims|boolean|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxIconUrl|character varying(64)|DEFAULT|NULL|||
|oxUmaPolicyScriptDn|text|||||
|oxAttributes|text|||||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||

## oxAuthGrant

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|grtId|character varying(64)|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||

## oxAuthSessionId

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|sid|character varying(64)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|oxLastAccessTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxAuthUserDN|character varying(128)|DEFAULT|NULL|||
|authnTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxState|character varying(64)|DEFAULT|NULL|||
|oxSessionState|text|||||
|oxAuthPermissionGranted|boolean|DEFAULT|NULL|||
|oxAsJwt|boolean|DEFAULT|NULL|||
|oxJwt|text|DEFAULT|NULL|||
|oxAuthPermissionGrantedMap|text|DEFAULT|NULL|||
|oxInvolvedClients|text|DEFAULT|NULL|||
|oxAuthSessionAttribute|text|DEFAULT|NULL|||

## oxAuthUmaPCT

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|clnId|jsonb|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|tknCde|character varying(80)|DEFAULT|NULL|||
|ssnId|character varying(64)|DEFAULT|NULL|||
|oxClaimValues|character varying(64)|DEFAULT|NULL|||

## oxAuthUmaRPT

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|authnTime|timestamp without time zone(3)|DEFAULT|NULL|||
|clnId|jsonb|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|tknCde|character varying(80)|DEFAULT|NULL|||
|usrId|character varying(64)|DEFAULT|NULL|||
|ssnId|character varying(64)|DEFAULT|NULL|||
|oxUmaPermission|jsonb|DEFAULT|NULL|||
|uuid|character varying(64)|DEFAULT|NULL|||
|authzCode|character varying(64)|DEFAULT|NULL|||
|grtId|character varying(64)|DEFAULT|NULL|||
|grtTyp|character varying(64)|DEFAULT|NULL|||
|jwtReq|text|DEFAULT|NULL|||
|nnc|text|DEFAULT|NULL|||
|scp|text|||||
|tknTyp|character varying(32)|DEFAULT|NULL|||
|acr|character varying(48)|DEFAULT|NULL|||
|chlng|character varying(64)|DEFAULT|NULL|||
|chlngMth|character varying(64)|DEFAULT|NULL|||
|clms|character varying(64)|DEFAULT|NULL|||
|attr|text|DEFAULT|NULL|||
|tknBndCnf|text|DEFAULT|NULL|||

## oxClientAuthorization

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(100)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxAuthClientId|jsonb|DEFAULT|NULL|||
|oxAuthUserId|character varying(64)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|oxAuthScope|jsonb|DEFAULT|NULL|||

## oxCustomScript

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|oxScript|text|||||
|oxScriptType|character varying(64)|DEFAULT|NULL|||
|programmingLanguage|character varying(64)|DEFAULT|NULL|||
|oxModuleProperty|jsonb|DEFAULT|NULL|||
|oxConfigurationProperty|jsonb|DEFAULT|NULL|||
|oxLevel|integer|DEFAULT|NULL|||
|oxRevision|integer|DEFAULT|NULL|||
|oxEnabled|boolean|DEFAULT|NULL|||
|oxScriptError|text|||||
|oxAlias|jsonb|DEFAULT|NULL|||

## oxDeviceRegistration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|oxDeviceKeyHandle|character varying(128)|DEFAULT|NULL|||
|oxDeviceHashCode|integer|DEFAULT|NULL|||
|oxApplication|character varying(64)|DEFAULT|NULL|||
|oxDeviceRegistrationConf|text|DEFAULT|NULL|||
|oxDeviceNotificationConf|character varying(64)|DEFAULT|NULL|||
|oxNickName|character varying(64)|DEFAULT|NULL|||
|oxDeviceData|text|||||
|oxCounter|integer|DEFAULT|NULL|||
|oxStatus|character varying(64)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|personInum|character varying(64)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxLastAccessTime|timestamp without time zone(3)|DEFAULT|NULL|||
|oxTrustMetaLastModified|character varying(64)|DEFAULT|NULL|||
|oxTrustMetaLocation|text|DEFAULT|NULL|||
|oxTrustMetaVersion|character varying(64)|DEFAULT|NULL|||

## oxDocument

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|document|text|||||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxModuleProperty|jsonb|DEFAULT|NULL|||
|oxLevel|integer|DEFAULT|NULL|||
|oxRevision|integer|DEFAULT|NULL|||
|oxEnabled|boolean|DEFAULT|NULL|||
|oxAlias|jsonb|DEFAULT|NULL|||

## oxExpiredObject

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|dat|text|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|oxType|character varying(64)|DEFAULT|NULL|||

## oxFido2AuthenticationEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxSessionStateId|character varying(64)|DEFAULT|NULL|||
|oxCodeChallenge|character varying(64)|DEFAULT|NULL|||
|personInum|character varying(64)|DEFAULT|NULL|||
|oxAuthenticationData|text|||||
|oxStatus|character varying(64)|DEFAULT|NULL|||

## oxFido2RegistrationEntry

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|oxSessionStateId|character varying(64)|DEFAULT|NULL|||
|oxCodeChallenge|character varying(64)|DEFAULT|NULL|||
|oxCodeChallengeHash|character varying(64)|DEFAULT|NULL|||
|oxPublicKeyId|character varying(96)|DEFAULT|NULL|||
|personInum|character varying(64)|DEFAULT|NULL|||
|oxRegistrationData|text|||||
|oxDeviceNotificationConf|character varying(64)|DEFAULT|NULL|||
|oxCounter|integer|DEFAULT|NULL|||
|oxStatus|character varying(64)|DEFAULT|NULL|||

## oxMetric

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|uniqueIdentifier|character varying(64)|DEFAULT|NULL|||
|oxStartDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxEndDate|timestamp without time zone(3)|DEFAULT|NULL|||
|oxApplicationType|character varying(64)|DEFAULT|NULL|||
|oxMetricType|character varying(64)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|oxData|text|||||
|oxHost|character varying(64)|DEFAULT|NULL|||

## oxNode

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|organizationalOwner|text|||||
|owner|character varying(64)|DEFAULT|NULL|||
|sourceRelationalXdiStatement|character varying(64)|DEFAULT|NULL|||
|targetRelationalXdiStatement|character varying(64)|DEFAULT|NULL|||
|x|character varying(64)|DEFAULT|NULL|||
|xdiStatement|character varying(64)|DEFAULT|NULL|||
|xri|character varying(64)|DEFAULT|NULL|||

## oxPassportConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|gluuPassportConfiguration|jsonb|DEFAULT|NULL|||
|gluuStatus|character varying(16)|DEFAULT|NULL|||

## oxPushDevice

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxAuthUserId|character varying(64)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxPushApplication|text|||||
|oxPushDeviceConf|character varying(64)|DEFAULT|NULL|||
|oxType|character varying(64)|DEFAULT|NULL|||

## OxRadiusClient

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxRadiusClientName|character varying(64)|DEFAULT|NULL|||
|oxRadiusClientIpAddress|character varying(64)|DEFAULT|NULL|||
|oxRadiusClientSecret|character varying(64)|DEFAULT|NULL|||
|oxRadiusClientSortPriority|integer|DEFAULT|NULL|||

## oxRadiusServerConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|oxRadiusListenintegererface|character varying(64)|DEFAULT|NULL|||
|oxRadiusAuthenticationPort|integer|DEFAULT|NULL|||
|oxRadiusAccountingPort|integer|DEFAULT|NULL|||
|oxRadiusOpenIdBaseUrl|character varying(64)|DEFAULT|NULL|||
|oxRadiusOpenIdUsername|character varying(64)|DEFAULT|NULL|||
|oxRadiusOpenIdPassword|character varying(64)|DEFAULT|NULL|||
|oxRadiusAcrValue|character varying(64)|DEFAULT|NULL|||
|oxRadiusAuthScope|character varying(64)|DEFAULT|NULL|||
|oxRadiusAuthenticationTimeout|integer|DEFAULT|NULL|||

## oxRp

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|dat|text|||||

## oxScript

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxScript|text|||||
|oxScriptType|character varying(64)|DEFAULT|NULL|||

## oxSectorIdentifier

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||
|oxAuthRedirectURI|jsonb|DEFAULT|NULL|||
|oxAuthClientId|jsonb|DEFAULT|NULL|||

## oxShibbolethCASProtocolConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|uniqueIdentifier|character varying(64)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|oxConfApplication|text|||||
|oxRevision|integer|DEFAULT|NULL|||

## oxTrustConfiguration

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|ou|character varying(64)|DEFAULT|NULL|||
|oxTrustConfApplication|text|||||
|oxTrustConfCacheRefresh|text|||||
|oxRevision|integer|DEFAULT|NULL|||
|oxTrustConfImportPerson|text|||||
|oxTrustConfAttributeResolver|text|||||

## oxTrustedIdp

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|remoteIdpName|character varying(64)|DEFAULT|NULL|||
|remoteIdpHost|character varying(64)|DEFAULT|NULL|||
|supportedSingleSignOnServices|character varying(64)|DEFAULT|NULL|||
|selectedSingleSignOnService|character varying(64)|DEFAULT|NULL|||
|signingCertificates|character varying(64)|DEFAULT|NULL|||

## oxU2fRequest

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxRequestId|character varying(64)|DEFAULT|NULL|||
|oxRequest|text|||||
|oxSessionStateId|character varying(64)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|personInum|character varying(64)|DEFAULT|NULL|||
|creationDate|timestamp without time zone(3)|DEFAULT|NULL|||

## oxUmaResource

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|displayName|character varying(128)|DEFAULT|NULL|||
|inum|character varying(64)|DEFAULT|NULL|||
|owner|character varying(64)|DEFAULT|NULL|||
|oxAssociatedClient|jsonb|DEFAULT|NULL|||
|oxAuthUmaScope|jsonb|DEFAULT|NULL|||
|oxFaviconImage|character varying(64)|DEFAULT|NULL|||
|oxGroup|character varying(64)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxResource|text|||||
|oxRevision|integer|DEFAULT|NULL|||
|oxType|character varying(64)|DEFAULT|NULL|||
|oxScopeExpression|text|||||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|description|character varying(768)|DEFAULT|NULL|||

## oxUmaResourcePermission

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|oxAuthUmaScope|jsonb|DEFAULT|NULL|||
|oxConfigurationCode|character varying(64)|DEFAULT|NULL|||
|oxResourceSetId|character varying(64)|DEFAULT|NULL|||
|oxAttributes|text|||||
|oxTicket|character varying(64)|DEFAULT|NULL|||
|oxStatus|character varying(64)|DEFAULT|NULL|||

## PairwiseIdentifier

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|oxId|character varying(128)|DEFAULT|NULL|||
|oxSectorIdentifier|character varying(64)|DEFAULT|NULL|||
|oxAuthClientId|jsonb|DEFAULT|NULL|||
|oxAuthUserId|character varying(64)|DEFAULT|NULL|||

## SamlAcr

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|parent|character varying(64)|DEFAULT|NULL|||
|classRef|text|||||
|inum|character varying(64)|DEFAULT|NULL|||

## token

|**Field**|**Type**|**Null**|**Default**|**Extra**|**Key**|
| :- | :- | :- | :- | :- | :- |
|doc_id|character varying(64)|NOT|NULL||PRI|
|objectClass|character varying(48)|DEFAULT|NULL|||
|dn|character varying(128)|DEFAULT|NULL|||
|authnTime|timestamp without time zone(3)|DEFAULT|NULL|||
|authzCode|character varying(64)|DEFAULT|NULL|||
|iat|timestamp without time zone(3)|DEFAULT|NULL|||
|exp|timestamp without time zone(3)|DEFAULT|NULL|||
|del|boolean|DEFAULT|NULL|||
|grtId|character varying(64)|DEFAULT|NULL|||
|grtTyp|character varying(64)|DEFAULT|NULL|||
|jwtReq|text|||||
|nnc|text|||||
|scp|text|||||
|tknCde|character varying(80)|DEFAULT|NULL|||
|tknTyp|character varying(32)|DEFAULT|NULL|||
|usrId|character varying(64)|DEFAULT|NULL|||
|clnId|jsonb|DEFAULT|NULL|||
|acr|character varying(48)|DEFAULT|NULL|||
|uuid|character varying(64)|DEFAULT|NULL|||
|chlng|character varying(64)|DEFAULT|NULL|||
|chlngMth|character varying(64)|DEFAULT|NULL|||
|clms|character varying(64)|DEFAULT|NULL|||
|ssnId|character varying(64)|DEFAULT|NULL|||
|attr|text|||||
|tknBndCnf|text|||||
