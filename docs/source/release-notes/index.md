## Notice

This document, also known as the Gluu Release Note, 
relates to the Gluu Server Release versioned 3.1.8. The work is licensed under “The MIT License” 
allowing the use, copy, modify, merge, publish, distribute, sub-license and sale without 
limitation and liability. This document extends only to the aforementioned release version 
in the heading.

UNLESS IT HAS BEEN EXPRESSLY AGREED UPON BY ANY WRITTEN AGREEMENT BEFOREHAND, 
THE WORK/RELEASE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OR GUARANTEE OF ANY KIND 
EXPRESS OR IMPLIED. UNDER NO CIRCUMSTANCE, THE AUTHOR, OR GLUU SHALL BE LIABLE FOR ANY 
CLAIMS OR DAMAGES CAUSED DIRECTLY OR INDIRECTLY TO ANY PROPERTY OR LIFE WHILE INSTALLING 
OR USING THE RELEASE.

## Lifecycle

Status: Active Release

| Released | Community EOL | Enterprise EOL |
| --- | --- | --- |
| April 2020 | October 2020 | October 2021 |

## Purpose

The document is released with the Version 3.1.8 of the Gluu Software. The purpose of this document is to provide the changes made/new features included in this release of the Gluu Software. The list is not exhaustive and there might be some omission of negligible issues, but the noteworthy features, enhancements and fixes are covered. 

## Background

The Gluu Server is a free open source identity and access management (IAM) platform. The Gluu Server is a container distribution composed of software written by Gluu and incorporated from other open source projects. 

The most common use cases for the Gluu Server include single sign-on (SSO), mobile authentication, API access management, two-factor authentication, customer identity and access management (CIAM) and identity federation.

## Documentation

Please visit the [Gluu Documentation Page](http://www.gluu.org/docs/ce) for the complete 
documentation and administrative guide. 

## Available components in Gluu Server 3.1.8
- oxAuth, oxTrust, oxCore v3.1.8
- Gluu OpenLDAP v2.4.44-5
- Gluu OpenDJ v3.0
- Shibboleth v3.2.1
- Asimba forked from v1.3.0 + v1.3.1 snapshot changes (v1.3.1 was never released)
- Passport v0.3.2
- Java v1.8.0_112
- Node.js v6.9.1
- Jetty-distribution-9.3.15.v20161220
- Jython v2.7.0
- Weld 3.0.0
- FluentD 3.5
- Redis

## 3.1.8 Changes

### [GluuFederation/oxAuth](https://github.com/GluuFederation/oxAuth/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.8+)

- [#1193](https://github.com/GluuFederation/oxAuth/pull/1193) Fix oidc session change detection

- [#1217](https://github.com/GluuFederation/oxAuth/issues/1217) Forced session object push to cache on modification inside Authorization Endpoint.


### [GluuFederation/oxTrust](https://github.com/GluuFederation/oxTrust/issues?utf8=?&q=is%3Aissue+milestone%3A3.1.8+)

- Fix password reset

- Fix relax constraints on redirect_uri when subject type is public

- Fix redirect issue in registration

- [#1928](https://github.com/GluuFederation/oxTrust/pull/1928) SAML metadata validation issue in all 4.x instances #1928
