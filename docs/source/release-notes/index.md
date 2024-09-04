# Release Notes

## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 4.5. The work is licensed under “[The Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) License” allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without limitation and liability. This document extends only to the aforementioned release version in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING OR USING THE RELEASE.

## Purpose

The document is released with the Version 4.5 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 4.5
- oxAuth, oxTrust, oxCore v4.5
- Gluu OpenDJ v4.4.11 (with Bouncy Castle FIPS 140-2 crypto package 1.0.2.1 and Bouncy Castle Java APIs for the TLS 1.0.9)
- Shibboleth v4.3.1
- Passport v4.1
- Java v1.8.0_112
- Node.js v9.9.0
- Jetty-distribution-9.4.12.v20180830
- Jython v2.7.2a
- Weld 3.0.0
- FluentD 3.5
- Redis

## 4.5.5 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [d4cbc4f](https://github.com/GluuFederation/oxAuth/commit/d4cbc4f9d5e4de385012a2d2657ebca8b5017b89) feat(oxAuth): check if UMA group already added
- [#1903](https://github.com/GluuFederation/oxAuth/issues/1903) feat(oxauth): uppercased typ=JWT
- [73e8a02](https://github.com/GluuFederation/oxAuth/commit/73e8a0248ab1de756d3aecc3e08d2c56808defb1) feat(jans-auth): remove dulicate import from SG script
- [#1916](https://github.com/GluuFederation/oxAuth/issues/1916) fix(oxauth): introspection endpoint returns error for valid basic client authentication and invalid token
- [39b98cc](https://github.com/GluuFederation/oxAuth/commit/39b98cc207811c462f68d192a2e89729baf95d01) fix(oxauth): update method to calculate user devices
- [#1907](https://github.com/GluuFederation/oxAuth/pull/1907) Removed whitespace from login.xhtml login button value attribute and empty login.login property from oxauth.properties

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#2431](https://github.com/GluuFederation/oxTrust/pull/2431) feat(oxtrust): added support for sp logout return url 
- [#2419](https://github.com/GluuFederation/oxTrust/issues/2419) Cache refresh first page and source backend server page merged
- [#2418](https://github.com/GluuFederation/oxTrust/issues/2418) getting password mismatch error on registration of a user on register.htm
- [#2423](https://github.com/GluuFederation/oxTrust/issues/2423) Unable to select different introspection script in OpenID Client

### [GluuFederation/oxd](https://github.com/GluuFederation/oxd/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [0f84bbe](https://github.com/GluuFederation/oxd/commit/0f84bbeddfb4cc46f022a035831d180285584d92) update bouncycastle libs

### [GluuFederation/casa](https://github.com/GluuFederation/casa/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#284](https://github.com/GluuFederation/casa/issues/284) fix: a variety of errors with the email_2fa_core plugin 
- [1cf35b4](https://github.com/GluuFederation/casa/commit/1cf35b49855208d9db020e84347c54eac0789eb9) chore: udpdate bc libs
- [#276](https://github.com/GluuFederation/casa/issues/276) fix: alternative options not working

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxshibboleth/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#182](https://github.com/GluuFederation/oxShibboleth/pull/182) feat(oxshib): slo redirect 
- [f859feb](https://github.com/GluuFederation/oxShibboleth/commit/f859feb749b88981c056f96f6f663202d0ab06eb) fix: exclude second library version

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [a0b73e7](https://github.com/GluuFederation/gluu-passport/commit/a0b73e78676e80275396620f595478f15af5018a) fix(package-lock): update package lock json

### [GluuFederation/fido2](https://github.com/GluuFederation/fido2/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [c301fbb](https://github.com/GluuFederation/fido2/commit/c301fbb258a12d5d07103a673f84e96501dc8860) fix(fido2): update attribute names in search filters
- [b41405f](https://github.com/GluuFederation/fido2/commit/b41405fdb692747b0f45c68b754515f4faabae3e) fix(fido2): remove weld dependencies
- [5f4529f](https://github.com/GluuFederation/fido2/commit/5f4529f310bda827ffee3aeb7c6ec172e64cae3f) feat: update maven repo URL

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#1041](https://github.com/GluuFederation/community-edition-setup/pull/1041) fix: casa default file
- [9220025](https://github.com/GluuFederation/community-edition-setup/commit/9220025abe7b65a0efabd46a4fe6b4c29a78eb76) feat(jans-auth): remove dulicate import from SG script
- [#1042](https://github.com/GluuFederation/community-edition-setup/issues/1042) Make creation of /etc/certs optional if it already existscreate
- [#1044](https://github.com/GluuFederation/community-edition-setup/issues/1044) fix: casa copy of super gluu script crashes upon load
- [#1048](https://github.com/GluuFederation/community-edition-setup/pull/1048) feat(fido2): add fido2 conf error

## 4.5.4 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#1763](https://github.com/GluuFederation/oxAuth/pull/1763) feat(oxauth): end 
  session - if id_token is expired but signature is correct, look up session by 
  sid claim
- [#6ae16bb](https://github.com/GluuFederation/oxAuth/commits/6ae16bb3441b9e55d09b028abd2ab2c1774213e5) fix: 
  catch org.eclipse.jetty.http.BadMessageException: in jans #3330
- [#1760](https://github.com/GluuFederation/oxAuth/issues/1760) feat(oxauth): 
  add ability to return error out of introspection and 
  update_token custom script
- [#1772](https://github.com/GluuFederation/oxAuth/issues/1772) feat: custom 
  script: skip step for authentication flow
- [#1767](https://github.com/GluuFederation/oxAuth/issues/1767) Custom script: 
  Captcha on oxAuth login
- [#1760](https://github.com/GluuFederation/oxAuth/issues/1760) feat(oxauth): add ability to return error out of introspection and update_token custom script
- [#1790](https://github.com/GluuFederation/oxAuth/pull/1790) Feature: Change response status 200 (Ok) by 201 (Created) for Client Registration
- [#1791](https://github.com/GluuFederation/oxAuth/pull/1791) Feature: Birthdate formatting added, respecting backward compatibility
- [#1793](https://github.com/GluuFederation/oxAuth/issues/1793) When trying to get a claims name, oxAuth does not return it
- [#80f850d](https://github.com/GluuFederation/oxAuth/commit/80f850df7643f4200c76ba4e1507363edd336bc6) feat: add HttpService2 based on new API and connection pool
- [#1818](https://github.com/GluuFederation/oxAuth/issues/1818) feat(oxauth): we should strive to let RP handle error instead of showing Ooops page 
- [#1728](https://github.com/GluuFederation/oxAuth/issues/1728) feat: introduce new UpdateToken methods
- [#1774](https://github.com/GluuFederation/oxAuth/issues/1774) feat(oxauth): make not found exception logging level configurable
- [#fed0d02](https://github.com/GluuFederation/oxAuth/commit/fed0d020674b253f07e1937a7759ea4ecbce819e) feat: add method to allow modify headers
- [#83a663d](https://github.com/GluuFederation/oxAuth/commit/83a663d599aeee70da9fe3d29433834e3af43456)  feat: add authorization headers needed to access scan API from SG script
- [#1839](https://github.com/GluuFederation/oxAuth/issues/1839) feat: add proxy support to HttpService2 (apache http client) 
- [#1f5a737](https://github.com/GluuFederation/oxAuth/commit/1f5a737c8d58694b4e5f3d0971886adc344f6eaa) feat: add option to HttpService2 to allow configure connection timeouts
- [#1850](https://github.com/GluuFederation/oxAuth/issues/1850) feat(oxauth): create MAU exporter
- []() 
- [#1850](https://github.com/GluuFederation/oxAuth/issues/1850) feat(oxauth): stat exporter - added dynamic client registration
- [#1849](https://github.com/GluuFederation/oxAuth/issues/1849) fix(oxauth): explicit user consent is required when up-scope within client authorized scopes 
- [#1853](https://github.com/GluuFederation/oxAuth/issues/1853) fix(oxauth): if scopes are missed in grant_type=refresh_token AS must take scopes from previous grant
- [#1860](https://github.com/GluuFederation/oxAuth/issues/1860) Support passing custom parameters in the body of POST authorization request
- [#1865](https://github.com/GluuFederation/oxAuth/issues/1865) feat: add configuration property to AS which will allow to bypass basic client authentication restriction to query only own tokens
- [#1891](https://github.com/GluuFederation/oxAuth/issues/1891) fix(oxauth): the `requestUriParameterSupported` and `requestParameterSupported` should be involved in request processing
- [#9dc5697](https://github.com/GluuFederation/oxAuth/commit/9dc5697d94b3318eccb28714884e67d0aa3a4a1b) feat(fido2): allow to update device data in SG authentication response

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#2287](https://github.com/GluuFederation/oxTrust/issues/2287) fix : Remove Locale dropdown from to top menu
- [#2282](https://github.com/GluuFederation/oxTrust/issues/2282) Not possible to add a deep link as redirect_uri
- [#2261](https://github.com/GluuFederation/oxTrust/issues/2261) fix(api-server): Deleting trust relationship has no response from server
- [#2266](https://github.com/GluuFederation/oxTrust/issues/2266) Audit Log for All Config Changes
- [#c2445d2](https://github.com/GluuFederation/oxTrust/commit/c2445d23ef187b0c25ccd1e76e77bfa0e81a7d64) feat: added search box to filter scopes
- [#2333](https://github.com/GluuFederation/oxTrust/issues/2333) feat CR should support person loads from AD servers with different primary key attribute names
- [#2346](https://github.com/GluuFederation/oxTrust/issues/2346) feat: Add MAU Report to oxTrust

### [GluuFederation/oxd](https://github.com/GluuFederation/oxd/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#3ad3f89](https://github.com/GluuFederation/oxd/commit/3ad3f8957463cd2bb9461cf492eef715709bb0f1) feat(jans-orm): update dropwizard-core

### [GluuFederation/casa](https://github.com/GluuFederation/casa/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#254](https://github.com/GluuFederation/casa/issues/254) feat: support custom location of .administrable file
- [#278](https://github.com/GluuFederation/casa/issues/278) feat: allow usage of 2fa when user has no password
- [#276](https://github.com/GluuFederation/casa/issues/276) fix: alternative options not working

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxshibboleth/issues?utf8=%3F&q=is:issue+milestone:4.5+) 

- [#56f4ac3](https://github.com/GluuFederation/oxShibboleth/commit/56f4ac3eda95163cc56de24e9eb6f1e76101ae33) feat(idp): update java-support

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#976](https://github.com/GluuFederation/community-edition-setup/pull/976) Change response status 200 (Ok) by 201 (Created) for Client Registration
- [#977](https://github.com/GluuFederation/community-edition-setup/pull/977) feat: Added new settings for date formatting
- [#988](https://github.com/GluuFederation/community-edition-setup/issues/988) fix(community-edition-setup): Post-install possiblity to add certificates needed for Passwurd API
- [#9e12c20](https://github.com/GluuFederation/community-edition-setup/commit/9e12c20b443066fb6188fc05e82d8d6c9172954b) feat: add options to validation connections
- [#1001](https://github.com/GluuFederation/community-edition-setup/pull/1001) feat: support for EL 9
- [#f4feac2](https://github.com/GluuFederation/community-edition-setup/commit/f4feac2192ec9b7bcf3d0783bf07a138bdf03407) feat: RHEL 9 support
- [#1030](https://github.com/GluuFederation/community-edition-setup/pull/1030) feat: cache cleaning script
- [#4d16b43](https://github.com/GluuFederation/community-edition-setup/commit/4d16b4325a592d4154c2d58d94bdaac02f7802ae) fix casa startup

## 4.5.3 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=%3F&q=is:issue+milestone:4.5+)

- [#1859](https://github.com/GluuFederation/oxAuth/issues/1859) fix(stat-exporter): if run stat exporter against jans-auth-server it is trying to connect to wrong endpoint and fail
- [#1878](https://github.com/GluuFederation/oxAuth/issues/1878) fix(stat-exporter): stat exporter can't run against jans-auth-server
- [#1879 ](https://github.com/GluuFederation/oxAuth/issues/1879) fix(oxauth): re-authentication doesn't happen for OIDC authz request with the higher "level" acr requested anymore 
- [#1880](https://github.com/GluuFederation/oxAuth/pull/1880) fix(oxauth): client secret printed on logs
- [#1883](https://github.com/GluuFederation/oxAuth/issues/1883) feat: implement Saml router script
- [#1861](https://github.com/GluuFederation/oxAuth/issues/1861) fix(oxauth) : add exclusion to authentication filter for "/token" and "public client" when PKCE is used
- [#1867](https://github.com/GluuFederation/oxAuth/issues/1867) Unable to add multiple case sensitive redirect URI
- [#1869](https://github.com/GluuFederation/oxAuth/issues/1868) fix(oxauth): cnf introspection response is null even when valid cert is send during MTLS #6343 #1868
  

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxtrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

 - [#2371](https://github.com/GluuFederation/oxTrust/issues/2371) feat: Add Search Field for Scopes Selection in OpenID Client


### [GluuFederation/casa](https://github.com/GluuFederation/casa/issues?q=is%3Aissue+is%3Aclosed)

  - [#265](https://github.com/GluuFederation/casa/issues/265) fix: error while enrolling OTP

  

## 4.5.2 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=%3F&q=is:issue+milestone:4.5+)

- [#1849 ](https://github.com/GluuFederation/oxAuth/issues/1849) Explicit user consent is required when up-scope within client authorized scopes 
- [#1850](https://github.com/GluuFederation/oxAuth/issues/1850) create MAU exporter
- [#1853](https://github.com/GluuFederation/oxAuth/issues/1853) scopes are missed in grant_type=refresh_token AS must take scopes from previous grant
- [#1857](https://github.com/GluuFederation/oxAuth/issues/1857) state is not always returned on redirect from /end_session endpoint
- [#1862](https://github.com/GluuFederation/oxAuth/issues/1862) added client_id parameter support to /end_session
  

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxtrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#2346](https://github.com/GluuFederation/oxTrust/issues/2346) Added MAU Report to oxTrust

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#996](https://github.com/GluuFederation/community-edition-setup/issues/996) Make jans_stat a default oauth scope

## 4.5.1 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=%3F&q=is:issue+milestone:4.5+)

- [#1849 ](https://github.com/GluuFederation/oxAuth/issues/1849) Explicit user consent is required when up-scope within client authorized scopes 
- [#1365](https://github.com/GluuFederation/oxAuth/issues/1365) Login Page blank value error message is not user friendly
- [#1838](https://github.com/GluuFederation/oxAuth/issues/1838) Failed to initialize resteasy proxy from script at server startup
- [#1774](https://github.com/GluuFederation/oxAuth/issues/1774) Make not found exception logging level configurable
- [#1830](https://github.com/GluuFederation/oxAuth/issues/1830) Upgrade nimbus
- [#1828](https://github.com/GluuFederation/oxAuth/issues/1828) Unnecessary "session not found" error messages during refresh token flow 
- [#1826](https://github.com/GluuFederation/oxAuth/issues/1826) Upgrade dependencies
- [#1827](https://github.com/GluuFederation/oxAuth/issues/1827) Jettison 1.5.2 -> 1.5.4 
- [#1728](https://github.com/GluuFederation/oxAuth/issues/1728) Introduce new UpdateToken methods in oxauth which exist in jans
- [#1825](https://github.com/GluuFederation/oxAuth/issues/1825) Introduce new UpdateToken methods
- [#1818](https://github.com/GluuFederation/oxAuth/issues/1818) We should strive to let RP handle error instead of showing Ooops page
- [#1820](https://github.com/GluuFederation/oxAuth/issues/1820) Apply  client WhiteList  when session is valid (allowPostLogoutRedirectWithoutValidation=true )
- [#1821](https://github.com/GluuFederation/oxAuth/issues/1821) Corrected post_logout_redirect_uri validation 
- [#1812](https://github.com/GluuFederation/oxAuth/issues/1812) oxAuth still searches custom script using it's acr_value while it should be its inum
- [#1805](https://github.com/GluuFederation/oxAuth/issues/1805) oxAuth seems to drop parts of url query string when comparing redirect_uri during request authorization
- [#1660](https://github.com/GluuFederation/oxAuth/issues/1660) Login page doesn't display the correct localized characters
- [#1747](https://github.com/GluuFederation/oxAuth/issues/1747) Do not log WebApplicationException as error since it's expected behavior

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxtrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#2343](https://github.com/GluuFederation/oxTrust/issues/2343) Password reset page showing success even when passwords mismatching
- [#2311](https://github.com/GluuFederation/oxTrust/issues/2311) User self-registration page doesn't seem to enforce custom validation rules for attributes
- [#2307](https://github.com/GluuFederation/oxTrust/issues/2307) Reset password page error handling / Strong password policy
- [#2310](https://github.com/GluuFederation/oxTrust/issues/2310) Regex pattern validation on Password attributes causes error when creating user
- [#2321](https://github.com/GluuFederation/oxTrust/issues/2321) oxTrust won't allow to set several postlogout redirect uris for OIDC client
- [#2295](https://github.com/GluuFederation/oxTrust/issues/2295) It's hard to browse list of OIDC scopes when configuring client's properties, it's cluttered too much and not organized enough
- [#2320](https://github.com/GluuFederation/oxTrust/issues/2320) oxTrust won't allow for multiple acrs set as "Default ACR value" for OIDC client

## 4.5 Fixes / Enhancements

### [GluuFederation/oxOrm](https://github.com/GluuFederation/oxOrm/issues?utf8=?&q=is%3Aissue+milestone%3A4.5+)

- [#25](https://github.com/GluuFederation/oxOrm/issues/25) Add PostgreSQL support
- [#24](https://github.com/GluuFederation/oxOrm/issues/24) update to conform Couchbase SDK 3.x

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.5+)

- [#1748](https://github.com/GluuFederation/oxAuth/issues/1748) Duplicate iss and aud on introspection as jwt
- [#1760](https://github.com/GluuFederation/oxAuth/issues/1760) add ability to return error out of introspection and update_token custom script 
- [#1763](https://github.com/GluuFederation/oxAuth/issues/1763) end session - if id_token is expired but signature is correct, look up session by sid claim
- [#1758](https://github.com/GluuFederation/oxAuth/issues/1758) log WebApplicationException in debug log level
- [#1735](https://github.com/GluuFederation/oxAuth/issues/1735) add convenient idTokenLifetime client property
- [#1733](https://github.com/GluuFederation/oxAuth/issues/1733) PKCE parameters from first SSO request retains in futher calls
- [#1730](https://github.com/GluuFederation/oxAuth/issues/1730) do not unauthenticate session on prompt=login if there was no at least 1 successful redirect to rp
- [#1727](https://github.com/GluuFederation/oxAuth/issues/1727) fixed request file method failure
- [#1725](https://github.com/GluuFederation/oxAuth/issues/1725) SpontaneousScopeHttpTest fails during build 
- [#1723](https://github.com/GluuFederation/oxAuth/issues/1723) fix NPE in JwtAuthorizationRequest
- [#1721](https://github.com/GluuFederation/oxAuth/issues/1721) allow end session with expired id_token_hint (by checking signature and aud/sid)
- [#1714](https://github.com/GluuFederation/oxAuth/issues/1714) allow authentication for max_age=0
- [#1705](https://github.com/GluuFederation/oxAuth/issues/1705) Auth Server JSON config for allowSpontaneousScopes 
- [#1701](https://github.com/GluuFederation/oxAuth/issues/1701) CIBA has hardcoded false for includeIdTokenClaims
- [#1537](https://github.com/GluuFederation/oxAuth/issues/1537) add custom script method to get device registration token. 

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxtrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#2282](https://github.com/GluuFederation/oxtrust/issues/2282) Not possible to add a deep link as redirect_uri
- [#2262](https://github.com/GluuFederation/oxtrust/issues/2262) oxTrust with 100+ SAML trust relationships
- [#2209](https://github.com/GluuFederation/oxtrust/issues/2209) Cache refresh should remove persons sub entries on removal
- [#2225](https://github.com/GluuFederation/oxtrust/issues/2225) Remove files in /var/gluu/identity/removed 
- [#1704](https://github.com/GluuFederation/oxtrust/issues/1704) Support SAML MDQ as alternative to downloading federation metadata
- [#2226](https://github.com/GluuFederation/oxtrust/issues/2226) make languages configurable in properties
- [#2176](https://github.com/GluuFederation/oxtrust/issues/2176) remove deprecated caCertsLocation, caCertsPassphrase properties

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#961](https://github.com/GluuFederation/community-edition-setup/issues/961) Gluu radius post installation failed when the backend is spanner.
- [#950](https://github.com/GluuFederation/community-edition-setup/issues/950) Apply persistence update to all CE projects to conform jetty 10
- [#946](https://github.com/GluuFederation/community-edition-setup/issues/946) Incorrect JDBC driver class in SAML IDP [postgresql]
- [#937](https://github.com/GluuFederation/community-edition-setup/issues/937) Install CB/Spanner DB libraries from separated archive

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#155](https://github.com/GluuFederation/oxShibboleth/issues/155) No attributes released in saml sso.

### [GluuFederation/scim](https://github.com/GluuFederation/scim/issues?utf8=?&q=is%3Aissue+milestone%3A4.5.0+)

- [#47](https://github.com/GluuFederation/scim/issues/47) include the name of problematic attribute part of extension in the error response

## 4.4.1 Fixes / Enhancements

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.1+)

- fix: setup removal notice
- fix: remove cache refresh files on uninstall
- feat: generating of keystore for signing emails has been refactored
- feat: support of sending signed emails has been added
- feat: definition of signing algorithm has been added
- fix: unnecessary .encode('utf-8') has been removed
- fix: fix repository URL
- fix: oxd for cluster
- fix: gcs path
- feat: added localhost to requestUriBlackList
- feat: set auth mode and enable scripts by setup.properties
- feat: options -ox-trust-authentication-mode -ox-authentication-mode -enable-script
- [#874](https://github.com/GluuFederation/community-edition-setup/issues/874) fix: cacert path in oxtrust config
- [#872](https://github.com/GluuFederation/community-edition-setup/issues/872) Skip not required SQL tables creation
- fix: fido external files
- [#870](https://github.com/GluuFederation/community-edition-setup/issues/870) fix: multivalued attributes of eduPerson
  
### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.1+)

- feat: support of sending signed emails has been added;
- chore(oxauth): renamed requestUriBlackList -> requestUriBlockList
- feat(oxauth): added restriction for request_uri parameter (blacklist/allowed list)
- [#1682](https://github.com/GluuFederation/oxAuth/issues/1682) chore: Upgrade crypto-js to 4.1.1 version
- feat: add sample script for multi auth conf which uses Gluu LDAP auth confs
- feat: add methods to simplify getting auth manager configurations
- chore: force to use latest OWASP html-sanitizer

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.1+)

- feat: oxcore issue 223 display DB option on ui
- feat: sending of emails has been added (for bcprov and bc-fips);
- fix: remove blue strip for the message.
- fix: disabled multivalued check box for mysql db
- fix: added onelogin saml lib and removed those classes
- fix: removed unused attributes
- feat: added organization details in saml metadata format
- feat: added functionality to create metadata by filling form
- fix: add dynamic script in openid scopes.
- fix: import attribute in mysql db
- feat: usage smtpconnectprotectiontype has been updated;
- feat: entering of keystore parameters has been added in interface;
- feat: added saml apis
- fix : removed sesssionDEnabled attributes

### [GluuFederation/oxCore](https://github.com/GluuFederation/oxCore/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.1+)

- fix: fix for display name
- feat: sending of emails has been updated (for bcprov and bc-fips);
- feat: add DB documentstore provider
- feat: sending signed emails has been added;
- feat: updating smtp configuring has been added;
- feat: add method for saml api

## 4.4.0 Fixes / Enhancements

- Numerous bug fixes to fully support MySQL in VM-based deployments

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.0+)

- [#1518](https://github.com/GluuFederation/oxAuth/issues/1518) Switching to DUO Universal Prompt (newer UI version) from the older authentication prompt

- [#1587](https://github.com/GluuFederation/oxAuth/issues/1587) feat: add ability to specify key length for KeyGenerator 

- [#1631](https://github.com/GluuFederation/oxAuth/issues/1631) Enable Casa Script to Support External LDAP Authentication Source

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.4.0+)

- [#129](https://github.com/GluuFederation/oxShibboleth/issues/129) Update resteasy libraries to latest 4.5.x version

- [#130](https://github.com/GluuFederation/oxShibboleth/issues/130) Update log4j-over-slf4j to 1.7.36

## 4.3.1 Fixes / Enhancements

    - Updated log4j to version 2.17 in all services

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.3.1+)

- [#1584](https://github.com/GluuFederation/oxAuth/issues/1584) Update to RestEasy 4

- [#1570](https://github.com/GluuFederation/oxAuth/issues/1570) Enhance casa login page and its derivations when the browser saves credentials 

- [#1448](https://github.com/GluuFederation/oxAuth/issues/1448) passport_saml and passport_social produces script error after reloading script

- [#900](https://github.com/GluuFederation/oxAuth/issues/900) Remove sessionIdEnabled Property

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.3.1+)

- [#2082](https://github.com/GluuFederation/oxTrust/issues/2082) Password reset success completion redirection

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?q=is%3Aopen+is%3Aissue+milestone%3A4.3.1+)

- [#288](https://github.com/GluuFederation/gluu-passport/issues/288) saml-passport upgraded to version 3.1.2

## 4.3.0 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.3.0+)

- [#1545](https://github.com/GluuFederation/oxAuth/issues/1545) Oxauth-rp service unable to start after fresh installation of 4.3.0

- [#1544](https://github.com/GluuFederation/oxAuth/issues/1544) Openmetric request fail with label as digits only

- [#1538](https://github.com/GluuFederation/oxAuth/issues/1538) MAU: discrepancy of hll cardinality before and after serialization
 
- [#1536](https://github.com/GluuFederation/oxAuth/issues/1536) feat(new-acr-link): create script to replace acr_values in authz url 

- [#1534](https://github.com/GluuFederation/oxAuth/issues/1534) forgot_password script not updated according other oxauth changes
 
- [#1533](https://github.com/GluuFederation/oxAuth/issues/1533) Add JSON Property to release id_token for password grant
 
- [#1528](https://github.com/GluuFederation/oxAuth/issues/1528) There is no automatic expiration of UMA permissions/pct/rpt/etc with Couchbase
 
- [#1526](https://github.com/GluuFederation/oxAuth/issues/1526) Retain claim in access token after refreshing

- [#1525](https://github.com/GluuFederation/oxAuth/issues/1525) Whitelist encryption and signing algorithms in JWKS 
 
- [#1523](https://github.com/GluuFederation/oxAuth/issues/1523) New interceptions script to modify id_token
 
- [#1517](https://github.com/GluuFederation/oxAuth/issues/1517) Avoid NPE in User Info Endpoint (caused by scope removing)

- [#1321](https://github.com/GluuFederation/oxAuth/issues/1321) Add live metric endpoints to oxAuth

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.3.0+)

- [#2085](https://github.com/GluuFederation/oxTrust/issues/2085) Enhance usability of scopes picker in client edition form

- [#2084](https://github.com/GluuFederation/oxTrust/issues/2084) Updating client id in passport IDP-initiated flow config throws Oops error.

- [#2081](https://github.com/GluuFederation/oxTrust/issues/2081) Oops error on clicking Other custom Scripts

- [#2078](https://github.com/GluuFederation/oxTrust/issues/2078) Update morris.js library to latest

- [#2075](https://github.com/GluuFederation/oxTrust/issues/2075) "Organization Configuration" throwing error 

- [#2074](https://github.com/GluuFederation/oxTrust/issues/2074) Fill correct provider options as per type in Passport Provider Configuration

- [#2073](https://github.com/GluuFederation/oxTrust/issues/2073) SAML NameID configuration is not working in Cloud Edition

- [#2072](https://github.com/GluuFederation/oxTrust/issues/2072) Cache Refresh not working on 4.3.0 version. 

- [#2070](https://github.com/GluuFederation/oxTrust/issues/2070) Attribute Form: Enable custom validation checked by default (incorrectly)

- [#2069](https://github.com/GluuFederation/oxTrust/issues/2069) Add Person Form Crashes with New Objectclass 

- [#2066](https://github.com/GluuFederation/oxTrust/issues/2066) Update cleaner job to use more effective RDBS methods

- [#2065](https://github.com/GluuFederation/oxTrust/issues/2065) Don't update GluuConfiguration bean attributes in get method

- [#2061](https://github.com/GluuFederation/oxTrust/issues/2061) oxTrust is crashed when a search with a broad criteria is executed using User search feature against a big enough user database

- [#2055](https://github.com/GluuFederation/oxTrust/issues/2055) Cache Refresh: Don't print ldap password in log

- [#2054](https://github.com/GluuFederation/oxTrust/issues/2054) Email Attribute Validation Not working on View Profile Section
 
- [#2052](https://github.com/GluuFederation/oxTrust/issues/2052) Design configuration for openid-client new passport provider strategy

- [#2051](https://github.com/GluuFederation/oxTrust/issues/2051) Setting custom acr-value for IDP-Initiated Flow
 
- [#2043](https://github.com/GluuFederation/oxTrust/issues/2043) Remove 'Generate SP metadata' feature 

- [#1985](https://github.com/GluuFederation/oxTrust/issues/1985) Missing popup when clicking SP Metadata File link

### [GluuFederation/gluu-passport](https://github.com/GluuFederation/gluu-passport/issues?q=is%3Aopen+is%3Aissue+milestone%3A4.3.0+)

- [#313](https://github.com/GluuFederation/gluu-passport/issues/313) Bug: getRPT. Failed to get RPT token in Gluu 4.3.0

- [#291](https://github.com/GluuFederation/gluu-passport/issues/291) Passport social not recognizing any external identity provider (google, facebook etc ).

- [#242](https://github.com/GluuFederation/gluu-passport/issues/242) Sign In with Apple fails after multiple successive logins

- [#241](https://github.com/GluuFederation/gluu-passport/issues/241) R&D on openid-client provider configuration without requesting to discovery endpoint

- [#239](https://github.com/GluuFederation/gluu-passport/issues/239) ci(husky): update husky

- [#213](https://github.com/GluuFederation/gluu-passport/issues/213) Upgrade node allowed versions to allow latest LTS

- [#210](https://github.com/GluuFederation/gluu-passport/issues/210) build(deps-dev): bump husky from 4.3.8 to 5.0.9

- [#206](https://github.com/GluuFederation/gluu-passport/issues/206) Replace `passport-openidconnect` with `openid-client` 

- [#205](https://github.com/GluuFederation/gluu-passport/issues/205) Update uma.js to use got lib and remove request 

- [#187](https://github.com/GluuFederation/gluu-passport/issues/187) Passing non-user attributes from idp provider to OP (custom_data)

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.3.0+)

- [#93](https://github.com/GluuFederation/oxShibboleth/issues/93) Code migration to Shibboleth IDP 4.1.4

## 4.2.2 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.2+)

- [#1503](https://github.com/GluuFederation/oxAuth/issues/1503) `sector_identifier` has to be based on host only. Also optimize redirect_uri's validation based on `sector_identifier_uri`

- [#1514](https://github.com/GluuFederation/oxAuth/issues/1514) Persistence extension script still running after disabled

- [#1502](https://github.com/GluuFederation/oxAuth/issues/1502) Introduce revoke interception script

- [#1506](https://github.com/GluuFederation/oxAuth/issues/1506) Modify the `claims-gathering` script so that it first tries to read claims from PCT before directing to the page to enter claims

- [#1508](https://github.com/GluuFederation/oxAuth/issues/1508) Fix PasswordValidator faces validator dependend beans injection after JSF update to 2.3.x

- [#1505](https://github.com/GluuFederation/oxAuth/issues/1505) BUG : NPE during backchannel logout if grant object was not identified

- [#1493](https://github.com/GluuFederation/oxAuth/issues/1493) id_token is missed during 2 concurrent calls for ROPC 

- [#1472](https://github.com/GluuFederation/oxAuth/issues/1472) Error "oxTrust wasn't allowed to access user data" shown

- [#1504](https://github.com/GluuFederation/oxAuth/issues/1504) BUG : PostAuthentication script calls re-authentication instead of re-authorization. 

- [#1478](https://github.com/GluuFederation/oxAuth/issues/1478) Avoid race condition during saving grant object in cache

- [#1496](https://github.com/GluuFederation/oxAuth/issues/1496) Add configuration property to allow switch off forcing prompt consent for offline access

- [#1497](https://github.com/GluuFederation/oxAuth/issues/1497) Add a new claim to the id_token: `"grant": "password"`

- [#1499](https://github.com/GluuFederation/oxAuth/issues/1499) Introspection endpoint not returning scopes as json string

- [#1491](https://github.com/GluuFederation/oxAuth/issues/1491) Return sub value for ROPC based on `openidSubAttribute`.

- [#949](https://github.com/GluuFederation/oxAuth/issues/949) Add support for nested JWE tokens 

- [#1488](https://github.com/GluuFederation/oxAuth/issues/1488) Return custom attributes specified in dynamicRegistrationCustomAttributes in client registration response

- [#1486](https://github.com/GluuFederation/oxAuth/issues/1486) invalidateSessionCookiesAfterAuthorizationFlow is broken in 4.2.1

- [#1494](https://github.com/GluuFederation/oxAuth/issues/1494) If there are more then one key for same `alg` and `use` then take key by `èxp` with configurable strategy

- [#1492](https://github.com/GluuFederation/oxAuth/issues/1492) Bug : ROPC - refresh token is not returned with forceOfflineAccessScopeToEnableRefreshToken=true and offline_access scope

- [#1460](https://github.com/GluuFederation/oxAuth/issues/1460) oxAuth reloads custom scripts (file method)

- [#1487](https://github.com/GluuFederation/oxAuth/issues/1487) `.well-known/openid-configuration` has to be cached (no DB) on configurable amount of time (5min by default)

- [#1485](https://github.com/GluuFederation/oxAuth/issues/1485) session_id should not be included into response if it's not explicitly allowed.

- [#1483](https://github.com/GluuFederation/oxAuth/issues/1483) fix: update jwt date check function in passport scripts

- [#1480](https://github.com/GluuFederation/oxAuth/issues/1480) Refresh token removing doesn't look up in persistence (4.x).

- [#1476](https://github.com/GluuFederation/oxAuth/issues/1476) DuplicateEntryException: Entry already exists when using Consent Gathering script

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.2+)

- [#2046](https://github.com/GluuFederation/oxTrust/issues/2046) "The request is missing a required parameter" error obtained in flow 3

- [#2027](https://github.com/GluuFederation/oxTrust/issues/2027) Passport Config: field mapping dropdown

- [#2028](https://github.com/GluuFederation/oxTrust/issues/2028) Add Local Authentication for oxTrust 

- [#2045](https://github.com/GluuFederation/oxTrust/issues/2045) Use oxAuth configuration to check if application should render login graph on home page

- [#2044](https://github.com/GluuFederation/oxTrust/issues/2044) Remove `sector_identifier_uri` menu with dialogs and provide ability to enter it as text with automatic population of `redirect_uris`

- [#2041](https://github.com/GluuFederation/oxTrust/issues/2041) On oxtrust passport provider, the automatically generated callback url is invalid when using containers

- [#2040](https://github.com/GluuFederation/oxTrust/issues/2040) Prevent registration of the attribute with the same name

- [#2033](https://github.com/GluuFederation/oxTrust/issues/2033) oxTrust should use acr level to check acr instead of acr_name

### [GluuFederation/oxCore](https://github.com/GluuFederation/oxCore/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.2+)

-[#204](https://github.com/GluuFederation/oxCore/issues/204) Fix method to update log level

-[#206](https://github.com/GluuFederation/oxCore/issues/206) Metric Service clean all entries when DB is Couchbase

-[#207](https://github.com/GluuFederation/oxCore/issues/207) Destroy CouchbaseEnvironment object on container restart

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.2+)

-[#723](https://github.com/GluuFederation/community-edition-setup/issues/723) The jar file `bcpkix-jdk15on-1.54.jar` missing at `/opt/oxd-server/lib/` (inside Gluu Chroot) 

-[#720](https://github.com/GluuFederation/community-edition-setup/issues/720) Improve setup.py messages during oxd installation

-[#719](https://github.com/GluuFederation/community-edition-setup/issues/719) Write post setup strings to setup.log

### [GluuFederation/oxShibboleth](https://github.com/GluuFederation/oxShibboleth/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.2+)

-[#78](https://github.com/GluuFederation/oxShibboleth/issues/78) Add new endpoint /idp/health-check to allow cluster check IDP it status

## 4.2.1 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.1+)

- [#1468](https://github.com/GluuFederation/oxAuth/issues/1468) Avoid redundant session load on `removeOutdatedCurrentSessions` if session id was changed (due to changeSessionIdOnAuthentication=true)

- [#1467](https://github.com/GluuFederation/oxAuth/issues/1467) Not able to complete idp-initiated flow due session id / cookies issue

- [#1466](https://github.com/GluuFederation/oxAuth/issues/1466) oxAuth tries to find session entry which led to exception

- [#1459](https://github.com/GluuFederation/oxAuth/issues/1459) Remove log noise from passport-saml

- [#1461](https://github.com/GluuFederation/oxAuth/issues/1461) JWKS published invalid key for "crv" : "P-521"

- [#1456](https://github.com/GluuFederation/oxAuth/issues/1456) redirect_uri must be re-validated at authorize auction and on error redirect

- [#1443](https://github.com/GluuFederation/oxAuth/issues/1443) Update passport scripts to store oxExternalUid as multivalued

- [#1458](https://github.com/GluuFederation/oxAuth/issues/1458) Add clear sid support

- [#1455](https://github.com/GluuFederation/oxAuth/issues/1455) Misleading WARNING message on non-expired key

- [#1447](https://github.com/GluuFederation/oxAuth/issues/1447) If software_statement is present in dynamic registration request, plain claims are lost 

- [#1449](https://github.com/GluuFederation/oxAuth/issues/1449) Do not extend refresh token lifetime on refresh token rotation 

- [#1446](https://github.com/GluuFederation/oxAuth/issues/1446) `acr` and `amr` (auth_level) claims are missed in id_token if does not specify `acr_values` parameter explicitly in authorization request

- [#1444](https://github.com/GluuFederation/oxAuth/issues/1444) Dynamic Registration: fix software_statement validation behavior

- [#1445](https://github.com/GluuFederation/oxAuth/issues/1445) Use CustomObjectAttribute instead of CustomAttribute in user services to use JSON data types

- [#1442](https://github.com/GluuFederation/oxAuth/issues/1442) Update methods to store oxExternalUid as multivalued by default

- [#1130](https://github.com/GluuFederation/oxAuth/issues/1130) Restrict scopes in dynamic registration request for clients with password grant

- [#1438](https://github.com/GluuFederation/oxAuth/issues/1438) Add unique identifier for each metric entry to allow to find which node added that record

- [#1437](https://github.com/GluuFederation/oxAuth/issues/1437) Add option to not return new refresh token on refreshing token at Token Endpoint

- [#1435](https://github.com/GluuFederation/oxAuth/issues/1435) Authentication counter metrics is doubled with default authentication method

- [#1436](https://github.com/GluuFederation/oxAuth/issues/1436) Store issued tokens count metrics

- [#1422](https://github.com/GluuFederation/oxAuth/issues/1422) oxAuth generates backchannel logout tokens for wrong client

- [#1432](https://github.com/GluuFederation/oxAuth/issues/1432) Add configuration option to put session in cache (performance)

- [#1430](https://github.com/GluuFederation/oxAuth/issues/1430) Support hash fragment validation for `request_uri` (required by some new conformance tests)

- [#1428](https://github.com/GluuFederation/oxAuth/issues/1428) Reduce number of session queries to DB (Performance)

- [#1424](https://github.com/GluuFederation/oxAuth/issues/1424) Performance: switch Client Authorization from querying to getting by key

- [#1418](https://github.com/GluuFederation/oxAuth/issues/1418) Keys are not reloaded automatically from keystore file. Full oxauth restart is required.

- [#1420](https://github.com/GluuFederation/oxAuth/issues/1420) Performance: we have a lot of requests to ClientTokens cache key which doesn't make sense for NATIVE cache

- [#1419](https://github.com/GluuFederation/oxAuth/issues/1419) Bug: select account functionality is broken

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.1+)

- [#2029](https://github.com/GluuFederation/oxTrust/issues/2029) Error Viewing InCommon Metadata

- [#2025](https://github.com/GluuFederation/oxTrust/issues/2025) CR copy binary attributes to local LDAP as base64 string

- [#2016](https://github.com/GluuFederation/oxTrust/issues/2016) oxTrust should not rely on configuration endpoint for scopes

- [#2020](https://github.com/GluuFederation/oxTrust/issues/2020) Bug: GUI allows to persist redirect_uri with fragment

- [#2017](https://github.com/GluuFederation/oxTrust/issues/2017) U2F enrollments not shown in User's Authentication Methods panel

- [#2018](https://github.com/GluuFederation/oxTrust/issues/2018) Visual issues on OIDC client advanced settings page

- [#2015](https://github.com/GluuFederation/oxTrust/issues/2015) Change label / values for Scope visibility

- [#2012](https://github.com/GluuFederation/oxTrust/issues/2012) Injection: Cross-site scripting

- [#2010](https://github.com/GluuFederation/oxTrust/issues/2010) Using Components with Known Vulnerabilities: Outdated jQuery Library Version

- [#2009](https://github.com/GluuFederation/oxTrust/issues/2009) Bump Jython version

- [#2003](https://github.com/GluuFederation/oxTrust/issues/2003) There are two save buttons in json configuration

- [#2002](https://github.com/GluuFederation/oxTrust/issues/2002) Not able to delete `claims redirect uri` for any client

### [GluuFederation/community-edition-setup](https://github.com/GluuFederation/community-edition-setup/issues?utf8=?&q=is%3Aissue+milestone%3A4.2.1+)

- [#713](https://github.com/GluuFederation/community-edition-setup/issues/713) offline_access scope should be created during setup

- [#709](https://github.com/GluuFederation/community-edition-setup/issues/709) Update Casa scripts to store and retrieve oxExternalUid as multivalued

- [#708](https://github.com/GluuFederation/community-edition-setup/issues/708) Add index for multivalued oxExternalUid

- [#707](https://github.com/GluuFederation/community-edition-setup/issues/707) CB: Store sessions in new bucket `gluu_session`

- [#703](https://github.com/GluuFederation/community-edition-setup/issues/703) Don't specify MaxMetaspaceSize java option

## 4.2.0 Fixes / Enhancements

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A4.2+)

- [#1410](https://github.com/GluuFederation/oxAuth/issues/1410) Failed to start redisProvider

- [#1408](https://github.com/GluuFederation/oxAuth/issues/1408) BUG : Introspection script is not identified by client which was used during obtaining access_token

- [#1406](https://github.com/GluuFederation/oxAuth/issues/1406) oxauth slows down in 4 times when CIBA is turned on.

- [#1397](https://github.com/GluuFederation/oxAuth/issues/1397) Add 'RPT Claims' script to add/modify RPT claims.

- [#1396](https://github.com/GluuFederation/oxAuth/issues/1396) Add support to use any client authentication for revoke token endpoint (currently it works only with basic client authentication)

- [#1391](https://github.com/GluuFederation/oxAuth/issues/1391) oxAuth fail to prepare JMS

- [#1385](https://github.com/GluuFederation/oxAuth/issues/1385) Check and possibly remove oxInvolvedClients attribute from session

- [#1379](https://github.com/GluuFederation/oxAuth/issues/1379) Correct security alert in test depedency

- [#1373](https://github.com/GluuFederation/oxAuth/issues/1373) Fido to Fido2 enrollment migration

- [#1371](https://github.com/GluuFederation/oxAuth/issues/1371) Add property to allow keep authenticator parameters on ACR change

- [#1370](https://github.com/GluuFederation/oxAuth/issues/1370) Control visibility of OAuth Scopes in configuration endpoint

- [#1362](https://github.com/GluuFederation/oxAuth/issues/1362) NotImplementedError in oxauth_script.log for person authentication scripts

- [#1361](https://github.com/GluuFederation/oxAuth/issues/1361) CIBA: Return an expired_token error when the auth_req_id has expired

- [#1358](https://github.com/GluuFederation/oxAuth/issues/1358) Security: Block "none" and not signed tokens

- [#1356](https://github.com/GluuFederation/oxAuth/issues/1356) Instead of redirect from authorize.htm to login.htm render login.htm page

- [#1354](https://github.com/GluuFederation/oxAuth/issues/1354) Associate consent script with client.

- [#1353](https://github.com/GluuFederation/oxAuth/issues/1353) Session : interception script should be informed about state change and when session ended by expiration

- [#1350](https://github.com/GluuFederation/oxAuth/issues/1350) OPENID Connect :  Request for Permission page only shown on second login attempt after 40s  interval.

- [#1344](https://github.com/GluuFederation/oxAuth/issues/1344) We should not return `reason` field in error response because it expose too much information outside

- [#1342](https://github.com/GluuFederation/oxAuth/issues/1342) CIBA: QA doc

- [#1341](https://github.com/GluuFederation/oxAuth/issues/1341) Front channel logout fails to logout all session participants after a re-authentication

- [#1335](https://github.com/GluuFederation/oxAuth/issues/1335) AuthenticationService.authenticate(String, String) throws exception if password is wrong

- [#1327](https://github.com/GluuFederation/oxAuth/issues/1327) CIBA: Securely store configuration keys.

- [#1326](https://github.com/GluuFederation/oxAuth/issues/1326) Add support to store session in htmlLocalStorage as an alternative to cookies

- [#1325](https://github.com/GluuFederation/oxAuth/issues/1325) Remove sub from Userinfo response for password grant clients

- [#1319](https://github.com/GluuFederation/oxAuth/issues/1319) CIBA: Load FCM config values from database configuration

- [#1316](https://github.com/GluuFederation/oxAuth/issues/1316) CIBA: Conformance Testing for FAPI-CIBA

- [#1315](https://github.com/GluuFederation/oxAuth/issues/1315) CIBA: Interception script for User Notification

- [#1311](https://github.com/GluuFederation/oxAuth/issues/1311) end_session : return error in post_logout_redirect_uri (configurable)

- [#1309](https://github.com/GluuFederation/oxAuth/issues/1309) Authorization header: "Bearer" should not be case sensitive

- [#1308](https://github.com/GluuFederation/oxAuth/issues/1308) Add oxAuth JSON properties to set logging format

- [#1306](https://github.com/GluuFederation/oxAuth/issues/1306) Mitigate replay of modified JWT from Passport-JS

- [#1302](https://github.com/GluuFederation/oxAuth/issues/1302) Blocker for RP conformance test : `response_types` during registration must be array of space separated string

- [#1300](https://github.com/GluuFederation/oxAuth/issues/1300) Use `exp` instead of `oxAuthExpiration` all over the code

- [#1299](https://github.com/GluuFederation/oxAuth/issues/1299) keyRegenerationInterval does not work if value is more then 595 (due to type overflow?)

- [#1298](https://github.com/GluuFederation/oxAuth/issues/1298) Fido2: Add option to not fail on device attestation which not have registerd metadata

- [#1297](https://github.com/GluuFederation/oxAuth/issues/1297) Password-less authentication with Fido2

- [#1296](https://github.com/GluuFederation/oxAuth/issues/1296) Client tests stops to work due to bootfaces remove

- [#1292](https://github.com/GluuFederation/oxAuth/issues/1292) Add JSON Configuration properties  to control JWKS endpoint algorithms

- [#1291](https://github.com/GluuFederation/oxAuth/issues/1291) Logout : conformance suite fail because it can't find sid claim in id_token.

- [#1290](https://github.com/GluuFederation/oxAuth/issues/1290) Support OpenID Connect prompt=select_account Authn request

- [#1289](https://github.com/GluuFederation/oxAuth/issues/1289) Introduce swagger spec file to oxauth

- [#1288](https://github.com/GluuFederation/oxAuth/issues/1288) Remove i18n oxauth_en.properties

- [#1286](https://github.com/GluuFederation/oxAuth/issues/1286) Logout : conformance tests expect successful page if session was ended but post_logout_redirect_uri not provided

- [#1280](https://github.com/GluuFederation/oxAuth/issues/1280) Client authentication : handle `Bearer` prefix when authenticate by access_token

- [#1279](https://github.com/GluuFederation/oxAuth/issues/1279) Logout Test - RP Initiated should validate id_token_hint is present

- [#1278](https://github.com/GluuFederation/oxAuth/issues/1278) Use browser locale if there is no AuthZ ui_locales parameter

- [#1277](https://github.com/GluuFederation/oxAuth/issues/1277) UMA : resource registration endpoint doesn't use passed resources iat, exp

- [#1275](https://github.com/GluuFederation/oxAuth/issues/1275) Use ui_locales_supported from confguration instead of JSF locales list

- [#1274](https://github.com/GluuFederation/oxAuth/issues/1274) Logout test - RP-Initiated - Unexcepted error

- [#1272](https://github.com/GluuFederation/oxAuth/issues/1272) Logout test observed because we don't show success logout message to the user

- [#1271](https://github.com/GluuFederation/oxAuth/issues/1271) Write SCIM Changelog for social login and password update

- [#1270](https://github.com/GluuFederation/oxAuth/issues/1270) FIDO2 : Support username-less authentication workflow

- [#1269](https://github.com/GluuFederation/oxAuth/issues/1269) We got redundant keys references in persistence oxAuthConfWebKeys

- [#1268](https://github.com/GluuFederation/oxAuth/issues/1268) CIBA: Super Gluu Integration

- [#1265](https://github.com/GluuFederation/oxAuth/issues/1265) Error 404 when calling to the FCM: unsubscribe endpoint

- [#1261](https://github.com/GluuFederation/oxAuth/issues/1261) OpenID Connect Client: Add client claim to specify introspection scripts to execute

- [#1260](https://github.com/GluuFederation/oxAuth/issues/1260) FAPI test (private key jwt) is failing because of not considering client_assertion and client_assertion_type parameters

- [#1256](https://github.com/GluuFederation/oxAuth/issues/1256) FAPI test fail because conformance suite is sending a list of auds

- [#1255](https://github.com/GluuFederation/oxAuth/issues/1255) FAPI test fail because of not checking aud field correctly

- [#1253](https://github.com/GluuFederation/oxAuth/issues/1253) Change behavior of `default` scope

- [#1252](https://github.com/GluuFederation/oxAuth/issues/1252) Dynamic registration: do not add fallback response_type or grant_type.

- [#1250](https://github.com/GluuFederation/oxAuth/issues/1250) FAPI test fail because of using state query parameter

- [#1249](https://github.com/GluuFederation/oxAuth/issues/1249) FAPI test is not passing because refresh token issued to a client can be used with another client

- [#1248](https://github.com/GluuFederation/oxAuth/issues/1248) FAPI : swap clients - test fail because of sending an unexpected kind of error

- [#1247](https://github.com/GluuFederation/oxAuth/issues/1247) Gather geolocation data from client instead of server side

- [#1244](https://github.com/GluuFederation/oxAuth/issues/1244) FAPI tests fail because of not validating that exp and scope must be present in the request.

- [#1242](https://github.com/GluuFederation/oxAuth/issues/1242) Change session_id after user authentication

- [#1241](https://github.com/GluuFederation/oxAuth/issues/1241) FAPI  complains that oxauth does not return error in fragment only and that state in error response does not match

- [#1240](https://github.com/GluuFederation/oxAuth/issues/1240) samesite cookie handling in upcoming Chrome 80

- [#1239](https://github.com/GluuFederation/oxAuth/issues/1239) FAPI : during test we noticed that `c_hash` and `s_hash` is not always present in id_token

- [#1238](https://github.com/GluuFederation/oxAuth/issues/1238) FAPI test fail because of including headers that shouldn't be sent

- [#1230](https://github.com/GluuFederation/oxAuth/issues/1230) FAPI : acr requested claim is not returned in id_token

- [#1228](https://github.com/GluuFederation/oxAuth/issues/1228) FAPI test fail because oxAuth should reject when response_type is only code

- [#1227](https://github.com/GluuFederation/oxAuth/issues/1227) FAPI : one of FAPI tests fail because oxauth does not handle request as JWT correctly

- [#1226](https://github.com/GluuFederation/oxAuth/issues/1226) Test automation

- [#1224](https://github.com/GluuFederation/oxAuth/issues/1224) FIDO2 authentication not working in  chrome

- [#1220](https://github.com/GluuFederation/oxAuth/issues/1220) Write script to facilitate multiple test email address against one valid address

- [#1219](https://github.com/GluuFederation/oxAuth/issues/1219) Introduce separate server-side session lifetime configuration property

- [#1213](https://github.com/GluuFederation/oxAuth/issues/1213) Pass Logout Conformance Tests

- [#1212](https://github.com/GluuFederation/oxAuth/issues/1212) Persist sessions in persistence layer

- [#1211](https://github.com/GluuFederation/oxAuth/issues/1211) Key expiration messages should be logged only if auto re-new is not enabled or re-generation interval is too big for key lifetime

- [#1202](https://github.com/GluuFederation/oxAuth/issues/1202) oxAuth should auto configure tokens clean size based on server load

- [#1198](https://github.com/GluuFederation/oxAuth/issues/1198) Add JSON configuration property to control removal of offline access refresh tokens

- [#1197](https://github.com/GluuFederation/oxAuth/issues/1197) Support "prompt=consent" parameter

- [#1196](https://github.com/GluuFederation/oxAuth/issues/1196) Session cookies should support domain parameter

- [#1195](https://github.com/GluuFederation/oxAuth/issues/1195) Authorization endpoint should not use session_id unless admin allowed to use it

- [#1191](https://github.com/GluuFederation/oxAuth/issues/1191) Super Gluu should support communtiction with web application on desktop

- [#1187](https://github.com/GluuFederation/oxAuth/issues/1187) Don't allow to issue openid scope in password grant without the admin permission

- [#1186](https://github.com/GluuFederation/oxAuth/issues/1186) Make password grant type configurable for dynamic clients

- [#1182](https://github.com/GluuFederation/oxAuth/issues/1182) Don't issue openid scope without authorization

- [#1181](https://github.com/GluuFederation/oxAuth/issues/1181) Set session state to unathenticated if application session script prohibit it creation

- [#1178](https://github.com/GluuFederation/oxAuth/issues/1178) Invalidate access tokens after refresh token revocation

- [#1175](https://github.com/GluuFederation/oxAuth/issues/1175) Parameterize OCs that passport scripts can use for user profile manipulation

- [#1174](https://github.com/GluuFederation/oxAuth/issues/1174) Add method to Person Authn Script to send context to proposed Post-Authn Interception Script

- [#1172](https://github.com/GluuFederation/oxAuth/issues/1172) Implement OpenID Connect offline access

- [#1171](https://github.com/GluuFederation/oxAuth/issues/1171) Support custom parameters in request object

- [#1166](https://github.com/GluuFederation/oxAuth/issues/1166) `refresh_ token` is automatically added to registered client in CE using oxd

- [#1157](https://github.com/GluuFederation/oxAuth/issues/1157) Make active scripts more visible on "Manage custom scripts" page

- [#1150](https://github.com/GluuFederation/oxAuth/issues/1150) oxauth code should use new `cacheService.getWithPut()` method

- [#1149](https://github.com/GluuFederation/oxAuth/issues/1149) Review FIDO2 implementation to confrom latest specification and conformance tools

- [#1136](https://github.com/GluuFederation/oxAuth/issues/1136) Make front-channel logout page customizable

- [#1134](https://github.com/GluuFederation/oxAuth/issues/1134) Make it easy to support new locale without unpacking oxauth war

- [#1133](https://github.com/GluuFederation/oxAuth/issues/1133) Support Spontaneous Scopes for UMA 2

- [#1130](https://github.com/GluuFederation/oxAuth/issues/1130) Restrict scopes in dynamic registration request for clients with password grant

- [#1129](https://github.com/GluuFederation/oxAuth/issues/1129) Add Interception Script:  Post-Authn Authorize

- [#1125](https://github.com/GluuFederation/oxAuth/issues/1125) CIBA: End-User Device Registration and Authentication

- [#1113](https://github.com/GluuFederation/oxAuth/issues/1113) Add OpenID Connect front channel logout custom interception script

- [#1104](https://github.com/GluuFederation/oxAuth/issues/1104) Allow 'passcode' along with QR code in OTP script

- [#1102](https://github.com/GluuFederation/oxAuth/issues/1102) Introspection interception script: add to ExternalIntrospectionContext user and grant object

- [#1079](https://github.com/GluuFederation/oxAuth/issues/1079) Discovery - Use jackson on both server and client side (and oxd) for consistency during json construction instead of manual parsing (`OpenIdConfigurationResponse`)

- [#1073](https://github.com/GluuFederation/oxAuth/issues/1073) Move tokens, RPT, (authorization grants) to ou=client_token (outside client entry)

- [#1062](https://github.com/GluuFederation/oxAuth/issues/1062) Configure Supported algorithms

- [#1060](https://github.com/GluuFederation/oxAuth/issues/1060) Prevent OTP replay attack

- [#1053](https://github.com/GluuFederation/oxAuth/issues/1053) Do not return client_secret on client read

- [#1038](https://github.com/GluuFederation/oxAuth/issues/1038) Userinfo response is not as expected as describe in specification

- [#1036](https://github.com/GluuFederation/oxAuth/issues/1036) Introduce `oxauth-persistence-model` maven module to be re-used by oxTrust API

- [#1032](https://github.com/GluuFederation/oxAuth/issues/1032) Add new property for BasicLockAccount authentication script

- [#1024](https://github.com/GluuFederation/oxAuth/issues/1024) On session expiration show "Login" button on OP page directly which should re-initiate login process (instead of "Go back" button)

- [#1019](https://github.com/GluuFederation/oxAuth/issues/1019) CIBA: Polling protection by interval

- [#1018](https://github.com/GluuFederation/oxAuth/issues/1018) CIBA: Signed Authentication Request

- [#1017](https://github.com/GluuFederation/oxAuth/issues/1017) CIBA: Push Mode with Pairwise Identifiers

- [#1016](https://github.com/GluuFederation/oxAuth/issues/1016) CIBA: Poll and Ping Modes with Pairwise Identifiers

- [#1015](https://github.com/GluuFederation/oxAuth/issues/1015) CIBA: Authentication result for Push Mode

- [#1014](https://github.com/GluuFederation/oxAuth/issues/1014) CIBA: Update Token Endpoint for request with Poll Mode

- [#1013](https://github.com/GluuFederation/oxAuth/issues/1013) CIBA: Update Token Endpoint for request with Ping Mode

- [#1012](https://github.com/GluuFederation/oxAuth/issues/1012) CIBA: Obtain End-User Consent/Authorization

- [#1011](https://github.com/GluuFederation/oxAuth/issues/1011) CIBA: Authentication Request with user code

- [#1010](https://github.com/GluuFederation/oxAuth/issues/1010) CIBA: Authentication Request with binding message

- [#1009](https://github.com/GluuFederation/oxAuth/issues/1009) CIBA: Implement Backchannel Authentication Endpoint

- [#1008](https://github.com/GluuFederation/oxAuth/issues/1008) CIBA: Update Dynamic Client Registration

- [#1007](https://github.com/GluuFederation/oxAuth/issues/1007) CIBA: Update Discovery Metadata

- [#1003](https://github.com/GluuFederation/oxAuth/issues/1003) Allow to refresh `ID Token` with grant_type refresh_token

- [#961](https://github.com/GluuFederation/oxAuth/issues/961) FAPI Conformance Suite

- [#958](https://github.com/GluuFederation/oxAuth/issues/958) More flexibilty to set audience on a per client basis

- [#936](https://github.com/GluuFederation/oxAuth/issues/936) FIDO 2: Add support for multi facet application IDs for impl

- [#935](https://github.com/GluuFederation/oxAuth/issues/935) Improve error page for Super Gluu denied authentication

- [#931](https://github.com/GluuFederation/oxAuth/issues/931) Return client_name in response of dynamic client registration

- [#928](https://github.com/GluuFederation/oxAuth/issues/928) Allow users to edit list of released scopes on the fly on the authorization page

- [#922](https://github.com/GluuFederation/oxAuth/issues/922) Encrypt oxAuth login information which are showing in HAR file

- [#921](https://github.com/GluuFederation/oxAuth/issues/921) Session Revocation

- [#895](https://github.com/GluuFederation/oxAuth/issues/895) Values for javax.faces.converter.XXX strings in messages.properties not overriding default messages

- [#861](https://github.com/GluuFederation/oxAuth/issues/861) Request objects should have iat and expiration

- [#853](https://github.com/GluuFederation/oxAuth/issues/853) CAS logout with oxAuth-session script ( application_session )

- [#839](https://github.com/GluuFederation/oxAuth/issues/839) Support for spontaneous scopes

- [#823](https://github.com/GluuFederation/oxAuth/issues/823) Authenitcator should not use "@!" to distingusih use/client credentials.

- [#800](https://github.com/GluuFederation/oxAuth/issues/800) Userinfo can't be contacted with access_token issued during resource owner creds grant flow if redirect_uri is not specified for the client

- [#795](https://github.com/GluuFederation/oxAuth/issues/795) Allow to set the pairwiseIdType (algorithmic/persistent) on a client basis

- [#789](https://github.com/GluuFederation/oxAuth/issues/789) Add support for id token upon token refresh

- [#782](https://github.com/GluuFederation/oxAuth/issues/782) Import clients with existing client_ids

- [#759](https://github.com/GluuFederation/oxAuth/issues/759) Scopes from request object get compared to reduced list of scopes during authorization

- [#751](https://github.com/GluuFederation/oxAuth/issues/751) Update Saml script to allow sign request

- [#750](https://github.com/GluuFederation/oxAuth/issues/750) Add CIBA support to oxAuth

- [#719](https://github.com/GluuFederation/oxAuth/issues/719) Allow to update oxDisabled attribute using Dynamic Client Registration endpoint

- [#697](https://github.com/GluuFederation/oxAuth/issues/697) Performance : ˜40% of time is blocked by weld synchronization during high load (>800 threads).

- [#694](https://github.com/GluuFederation/oxAuth/issues/694) Support redis failover in standalone

- [#667](https://github.com/GluuFederation/oxAuth/issues/667) Custom interception authorization script for Connect.

- [#657](https://github.com/GluuFederation/oxAuth/issues/657) Synchronize CAS logout with OpenID Connect logout

- [#637](https://github.com/GluuFederation/oxAuth/issues/637) Create reusable login template

- [#586](https://github.com/GluuFederation/oxAuth/issues/586) UMA 2 : Add Selenium user emulation for Claims-Gathering test pages (country.xhtml and city.xhml)

- [#535](https://github.com/GluuFederation/oxAuth/issues/535) Provide customization of front-channel generated html from /end_session

- [#498](https://github.com/GluuFederation/oxAuth/issues/498) Strip querystring from logout redirect URI comparison

- [#469](https://github.com/GluuFederation/oxAuth/issues/469) Extend Session Endpoint

- [#460](https://github.com/GluuFederation/oxAuth/issues/460) Performance : go over oxauth threads blocks that appears after 140req/s

- [#447](https://github.com/GluuFederation/oxAuth/issues/447) Federation: Publish metadata_statement_uris

- [#446](https://github.com/GluuFederation/oxAuth/issues/446) Federation: add signed_jwks_uri

- [#445](https://github.com/GluuFederation/oxAuth/issues/445) Federation: add signing_keys_uri

- [#437](https://github.com/GluuFederation/oxAuth/issues/437) Implement better HTTP Header Security

- [#393](https://github.com/GluuFederation/oxAuth/issues/393) Collect performance stats in oxAuth

- [#302](https://github.com/GluuFederation/oxAuth/issues/302) Client Registration: Validation user facing values

- [#233](https://github.com/GluuFederation/oxAuth/issues/233) New iFrame implicit flow

- [#223](https://github.com/GluuFederation/oxAuth/issues/223) Add postLogin method for authentication script

- [#218](https://github.com/GluuFederation/oxAuth/issues/218) Implement U2F attestation certificate validation

- [#208](https://github.com/GluuFederation/oxAuth/issues/208) New .well-known endpoint to publish acr configuration

- [#160](https://github.com/GluuFederation/oxAuth/issues/160) U2F: Add TLS Channel ID Binding

- [#89](https://github.com/GluuFederation/oxAuth/issues/89) Support for Software Statement Protected Client Registration

- [#70](https://github.com/GluuFederation/oxAuth/issues/70) Back-Channel Logout

- [#68](https://github.com/GluuFederation/oxAuth/issues/68) Add metric to store CPU/memory usage

- [#9](https://github.com/GluuFederation/oxAuth/issues/9) oxAuth client should support HTTP proxy

### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A4.2+)

- [#1991](https://github.com/GluuFederation/oxTrust/issues/1991) Add ability to add RPT Claims script to client

- [#1987](https://github.com/GluuFederation/oxTrust/issues/1987) Gluu 4.1.1 and 4.2: getting same Pairwise ID ( first generated one ) for rest of the users

- [#1973](https://github.com/GluuFederation/oxTrust/issues/1973) U2F and FIDO2 dates are using the same format

- [#1967](https://github.com/GluuFederation/oxTrust/issues/1967) Use JSON Property to allow extra attributes for person status

- [#1959](https://github.com/GluuFederation/oxTrust/issues/1959) Fix an issue when securely store CIBA configuration keys

- [#1958](https://github.com/GluuFederation/oxTrust/issues/1958) CIBA configuration UI

- [#1946](https://github.com/GluuFederation/oxTrust/issues/1946) Cust script not reloading when properties change and script location is file

- [#1930](https://github.com/GluuFederation/oxTrust/issues/1930) Break out SCIM into a separate service

- [#1927](https://github.com/GluuFederation/oxTrust/issues/1927) SAML TR / "Attributes Published" column buggy

- [#1924](https://github.com/GluuFederation/oxTrust/issues/1924) FAPI compatibility

- [#1923](https://github.com/GluuFederation/oxTrust/issues/1923) Fix error form too large for custom scripts page

- [#1922](https://github.com/GluuFederation/oxTrust/issues/1922) Use ui_locales_supported from confguration instead of JSF locales list

- [#1907](https://github.com/GluuFederation/oxTrust/issues/1907) Ehanced management for redirect_uri lists

- [#1891](https://github.com/GluuFederation/oxTrust/issues/1891) Re-visit differences between single-SP and federation types of SAML TR

- [#1890](https://github.com/GluuFederation/oxTrust/issues/1890) Add spontaneous scope script to UI

- [#1889](https://github.com/GluuFederation/oxTrust/issues/1889) Add `oxAttributes` JSON value support to Scopes (UI and API)

- [#1886](https://github.com/GluuFederation/oxTrust/issues/1886) Always show "Edit Type" and "View Type" in attribute form

- [#1873](https://github.com/GluuFederation/oxTrust/issues/1873) Deactivate "default acr" field in oxTrust OIDC client

- [#1868](https://github.com/GluuFederation/oxTrust/issues/1868) Add note on top of `Cache Provider Configuration` that oxauth restart is required if cache connection settings are changed.

- [#1867](https://github.com/GluuFederation/oxTrust/issues/1867) Log viewing from the UI allows to display of any sensitive file

- [#1865](https://github.com/GluuFederation/oxTrust/issues/1865) Configuration / Add Script: Pre-populate class and method according to interface

- [#1862](https://github.com/GluuFederation/oxTrust/issues/1862) Enhance web UI representation of nameids

- [#1861](https://github.com/GluuFederation/oxTrust/issues/1861) Optimize Cache Refresh to better handle really huge userbases

- [#1808](https://github.com/GluuFederation/oxTrust/issues/1808) Allow administrator to add libraries and plugins to oxAuth via GUI

- [#1750](https://github.com/GluuFederation/oxTrust/issues/1750) Detect OS security updates and allow to run upgrade

- [#1749](https://github.com/GluuFederation/oxTrust/issues/1749) Show notification about released upgrades

- [#1682](https://github.com/GluuFederation/oxTrust/issues/1682) Improve Error Reporting In oxTrust API

- [#1663](https://github.com/GluuFederation/oxTrust/issues/1663) Allow special character "underscore" in attribute name

- [#1641](https://github.com/GluuFederation/oxTrust/issues/1641) Contact Email field validation in Configuration > Organization configuration

- [#1636](https://github.com/GluuFederation/oxTrust/issues/1636) Performance degrade for /person/view, person/viewProfile.htm (potentially other pages)

- [#1626](https://github.com/GluuFederation/oxTrust/issues/1626) Configure supported algorithms

- [#1602](https://github.com/GluuFederation/oxTrust/issues/1602) Remove the finishlogout page

- [#1583](https://github.com/GluuFederation/oxTrust/issues/1583) Fix an invalid Birthdate Format

- [#1551](https://github.com/GluuFederation/oxTrust/issues/1551) Disallow the match between the username and the password
