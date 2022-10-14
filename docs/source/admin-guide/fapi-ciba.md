# Financial-grade API - Client Initiated Backchannel Authentication Profile (FAPI-CIBA)

**Financial-grade API** is a REST API that provides JSON data representing higher risk data. These APIs are protected by the OAuth 2.0 Authorization Framework.

Gluu Server supports and it's also certified as a FAPI implementation by OpenID, more info about the certification [here](https://openid.net/certification/#FAPI_OPs) and it supports a higher level of security about endpoints responsible to process authentication and authorization.

All specs about FAPI profile you can find here:
[OpenID Financial API Part 2 ID2](https://openid.net/specs/openid-financial-api-part-2-ID2.html)

**Client Initiated Backchannel Authentication** is an authentication flow in which RPs, that can obtain a valid identifier for the user they want to authenticate, will be able to initiate an interaction flow to authenticate their users without having end-user interaction from the consumption device. The flow involves direct communication from the Client to Gluu Server without redirect through the user's browser (consumption device).

Gluu Server is also certified as a CIBA implementation, more info about the certification you could see [here](https://openid.net/certification/#FAPI-CIBA_OPs).

About CIBA implementation is highly recommended to see this another page, since it contains some fundamentals features that are very important to understand this document: [CIBA](ciba.md)

All specs about CIBA profile you could find here:
[OpenID Connect Client-Initiated Backchannel Authentication Flow](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html)

More information about **FAPI-CIBA** profile here:
[Financial-grade API: Client Initiated Backchannel Authentication Profile](https://openid.net/specs/openid-financial-api-ciba-ID1.html)

## CIBA Token Delivery Modes
The push mode is not permitted by this specification as it delivers tokens to the client by calling an endpoint owned by the client. This substantially differs from the established pattern of retrieving tokens by presenting client authentication to the token endpoint, and it may have security concerns that are currently unknown.

The poll and ping modes both follow the established convention of retrieving tokens from the token endpoint and hence do not have this concern.

The ping mode delivers a notification to an endpoint owned by the client. The information contained in this notification is limited to the `auth_req_id` for the request. The bearer token used by the authorization server to access this resource is not sender constrained.

## Security Considerations

#### TLS
All connections to the server should use the following TLS configuration:

- TLS version allowed MUST be 1.2 or higher.
- TLS server certificate should be configured also.
- TLS cipher suites are:
    + TLS_DHE_RSA_WITH_AES_128_GCM_SHA256
    + TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    + TLS_DHE_RSA_WITH_AES_256_GCM_SHA384
    + TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384

#### Algorithms
In order to sign correctly JWT, it only can use `PS256` and `ES256` algorithms. It's not allowed to use any other algorithm and also it's not allowed to use `none`.

## Client Authentication
FAPI-CIBA implementation supports two types of client authentication, Mutual TLS and Private Key JWT and ciba authorization endpoint can use any of them, of course this should be configured in the client registration also.

#### Mutual TLS
In this kind of authentication, client should send a certificate to the server that is only issued for that specific client and it also includes `client_id` in the CIBA request. Gluu Server with MTLS is configured using `Apache` which is deeply explained in the next link:

[Mutual TLS Client Authentication and Certificate Bound Access Tokens](https://www.gluu.org/docs/gluu-server/4.0/fe/mtls/)

Using client certificate server should authenticate that client and after that Gluu Server check the JWT sent by the client to get all information about the CIBA request.

Example:
![CIBA MTLS Authentication Request](../img/admin-guide/ciba/CIBAMtlsAuthRequest.png)

#### Private Key JWT
This kind of authentication also uses a client certificate in order to validate every request and authenticate the client, however it also uses two new parameters in the request, which are:
- *client_assertion_type* for this profile, it always has the value `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`
- *client_assertion* This is also a JWT containing some information about the client.

Example:

*Encoded:*
```
eyJraWQiOiJmYXBpLWNpYmEtMyIsImFsZyI6IlBTMjU2In0.eyJzdWIiOiJmYXBpLWNpYmEtMyIsImF1ZCI6Imh0dHBzOlwvXC9jZS1vYi5nbHV1Lm9yZyIsImlzcyI6ImZhcGktY2liYS0zIiwiZXhwIjoxNTkyMzM3MDU5LCJpYXQiOjE1OTIzMzY5OTksImp0aSI6IllOaVg4UkJIYWlyUHhQclJuZzZYIn0.eH9-jCdGHkT2rCX7lMki68kKwPtDvRRkAA7mqC33sHk16xt3vuVDEqAr3nAXL7bG3y2l9mtTZWXM9kNF07GQgBezqCr-J43TUIpX2XVCQWx2_xdD5ioxm2RVVf_Qc5xx5PU-RsdSMTuGCiKm1orrBQziMxJRHoaMWZSFkr8rXtNPUqhX_jMY5Qj3qFtL81Sod2JEayd1oV4jsM_uxT7sljTWQD3fa7q0q6EogEkuCCG5iGj6Jj8-dLNBJNNnAY2NatlXUGoGGmciwKQkwSKG8eOHjYs9llghJ-blKGbT-ePp_Vcs1BfFsfBMfkUd-7RJ1DsKekNOF4b5BzwxzcpnWQ
```

*Decoded:*
```
HEADER
{
  "kid": "fapi-ciba-3",
  "alg": "PS256"
}

PAYLOAD
{
  "sub": "fapi-ciba-3",
  "aud": "https://ce-ob.gluu.org",
  "iss": "fapi-ciba-3",
  "exp": 1592337059,
  "iat": 1592336999,
  "jti": "YNiX8RBHairPxPrRng6X"
}
```

![Private Key JWT Authentication Request](../img/admin-guide/ciba/CIBAPrivateKeyJWTAuthRequest.png)

## Authentication Request
After client authentication using any of those client authentication modes commented above, every request MUST contain the `request` parameter containing the JWT with all information about the CIBA request, these claims are:

- *aud* The Audience claim MUST contain the value of the Issuer Identifier for the OP, which identifies the Authorization Server as an intended audience.
- *iss* The Issuer claim MUST be the client_id of the OAuth Client.
- *exp* An expiration time that limits the validity lifetime of the signed authentication request.
- *iat* The time at which the signed authentication request was created.
- *nbf* The time before which the signed authentication request is unacceptable.
- *jti* A unique identifier for the signed authentication request.

The signed authentication request JWT is passed as an application/x-www-form-urlencoded HTTP request parameter. Authentication request parameters MUST NOT be present outside of the JWT, in particular they MUST NOT appear as HTTP request parameters. Additional HTTP request parameters as required by the given client authentication method, however, MUST be included as application/x-www-form-urlencoded parameters (e.g. Mutual TLS client authentication uses client_id while JWT assertion based client authentication uses client_assertion and client_assertion_type).

Example:

*Encoded:*
```
eyJraWQiOiJmYXBpLWNpYmEtMyIsImFsZyI6IlBTMjU2In0.eyJhdWQiOiJodHRwczpcL1wvY2Utb2IuZ2x1dS5vcmciLCJsb2dpbl9oaW50IjoidGVzdF91c2VyIiwibmJmIjoxNTkyMzM2OTk5LCJzY29wZSI6Im9wZW5pZCIsImlzcyI6ImZhcGktY2liYS0zIiwiYmluZGluZ19tZXNzYWdlIjoiMTIzNCIsImV4cCI6MTU5MjMzNzI5OSwiaWF0IjoxNTkyMzM2OTk5LCJqdGkiOiI2NTl2N2pwT3BlWkVLUE1oSlU4RiJ9.BK8VzIlhtm_apeQBH9yiigZfsaBlWrS_N78uy4cBJo5NAibFbvKMd7jIgepWK2SskD5w0RxuXvf7QZ8ndsR4HQPjZx3rvtm_ZtfqC0YLeZjwNYqpyD0YExhf0PV2wEgZCcoExbIUrFdHJV79C6R1yzA1kwfFF5JAqknPpqE3jqOufLrBAbPR7XPsA1b_9FUFRkIuvnGOjIG7sA2qT0-ADWC9KFUUEqDOPUj-MjjHjhS_Ik-e1lH1YouNYgTXiSefnIT_Uw9gYBNRqDFKUDvoz-uIViiAFzokbUpbigGHJ-UCPo1l6SFJ3hlabSfDnARn--hwRsj7G8FJ1it11cmk4g
```

*Decoded*
```
HEADER
{
  "kid": "fapi-ciba-3",
  "alg": "PS256"
}

PAYLOAD
{
  "aud": "https://ce-ob.gluu.org",
  "login_hint": "test_user",
  "nbf": 1592336999,
  "scope": "openid",
  "iss": "fapi-ciba-3",
  "binding_message": "1234",
  "exp": 1592337299,
  "iat": 1592336999,
  "jti": "659v7jpOpeZEKPMhJU8F"
}
```

## Authentication Response
Response will be send in the same way that it's defined in CIBA documented linked [here](ciba.md).

Successful Example:
```
HTTP/1.1 200
Cache-Control: no-store
Content-Length: 116
Content-Type: application/json
Server: Jetty(9.4.19.v20190610)

{ "auth_req_id": "e0645ddcbd7c663f943157bf60ea04ae2622abb180be1ac2", "interval": 2, "expires_in": 300 }
```

Failed Example:
```
HTTP/1.1 400
Content-Length: 245
Content-Type: application/json
Server: Jetty(9.4.19.v20190610)

{
    "error_description": "The request is missing a required parameter, includes an invalid parameter value, includes a parameter more than once, contains more than one of the hints, or is otherwise malformed.",
    "error": "invalid_request"
}
```

## Token Request
Token request MUST use the client authentication mode configured for the client and the response will be the same as defined in CIBA document.

MTLS Request:
```
POST /oxauth/restv1/token
content-type: application/x-www-form-urlencoded
accept: application/json

grant_type=urn%3Aopenid%3Aparams%3Agrant-type%3Aciba&auth_req_id=5cb8f7941a3910138716ecb84ab31e88a0c325b58b5ac3d5&client_id=fapi-ciba-1
```

![MTLS CIBA Token Request](../img/admin-guide/ciba/CIBAMtlsTokenRequest.png)

Private Key JWT Request:
```
POST /restv1/token
content-type: application/x-www-form-urlencoded
accept: application/json

grant_type=urn%3Aopenid%3Aparams%3Agrant-type%3Aciba&auth_req_id=e0645ddcbd7c663f943157bf60ea04ae2622abb180be1ac2&client_assertion=eyJraWQiOiJmYXBpLWNpYmEtMyIsImFsZyI6IlBTMjU2In0.eyJzdWIiOiJmYXBpLWNpYmEtMyIsImF1ZCI6Imh0dHBzOlwvXC9jZS1vYi5nbHV1Lm9yZ1wvb3hhdXRoXC9yZXN0djFcL3Rva2VuIiwiaXNzIjoiZmFwaS1jaWJhLTMiLCJleHAiOjE1OTIzMzcwNTksImlhdCI6MTU5MjMzNjk5OSwianRpIjoiRGRpdldhZ01BQXhXS3NpSUlTeloifQ.zBSaIu1So__cQIGl4ugjV_QVJexHKSyka7lp5QAKTmRijvEh1kzkV9BBrS5Rnf30_cWZVwU4I2F5lcOYB7QXAOrq7AN9NVrh0alivpBKSBbGLCKkAtzQJnA8jacNjaZsdLNbWWC3aL7B_yBAiWa9knpCNzZ3ONDAouCWMike6aDVg1IDeddoZof7ogfRAtPlDYuy21GT3KgiZ9wGBBbg_mF13J0S8R848tHXG5kRxxz2vg4OrU-Hy9tab5-bzDfg9DOsdwuRTNAuEfwIhsWEqLmXf8qeY78K7bFV0LdOlFd-hlnhWg83oVx9bViv0e9_TWIdsSglpZNlMQuKzGf8pw&client_assertion_type=urn%3Aietf%3Aparams%3Aoauth%3Aclient-assertion-type%3Ajwt-bearer
```

![Private Key JWT CIBA Token Request](../img/admin-guide/ciba/CIBAPrivateKeyJWTTokenRequest.png)

## Token Response
Response will be send in the same way that it's defined in CIBA documented linked [here](ciba.md).

Successful Example:
```
HTTP/1.1 200
Cache-Control: no-store
Content-Length: 1122
Content-Type: application/json
Pragma: no-cache
Server: Jetty(9.4.19.v20190610)

{"access_token":"8cc0cb03-efdb-4545-a1dd-a5568bff6aa9","id_token":"eyJraWQiOiJlYTc4NDgxYy05OTJkLTRmN2UtYTkzMS03NjM2NTYyMzgwZjVfc2lnX3JzMjU2IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiNllLcGVKUlhHNldDZWcxTnY5QUVJZyIsImF1ZCI6IjEyMy0xMjMtMTIzIiwiYWNyIjoic2ltcGxlX3Bhc3N3b3JkX2F1dGgiLCJzdWIiOiJpRDUyZlN4TVh5YjNFRnNjR1d4TlUxZnB5UU9qQWlMY3RkSldFQk55M1BVIiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOmF1dGhfcmVxX2lkIjoiNGJhMzVkNTM1YzhlOTllYTVkOWFhMTRiZDEzZDVkNDI2MDdlMzYyZmFlMWRmNTNhIiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOnJ0X2hhc2giOiJianFrYS1tOS1xZnpacE1rUXB5cURBIiwiYW1yIjpbIi0xIl0sImlzcyI6Imh0dHBzOi8vdGVzdC5nbHV1Lm9yZzo4NDQzIiwiZXhwIjoxNTkyODc0MDUyLCJpYXQiOjE1OTI4NzA0NTIsIm94T3BlbklEQ29ubmVjdFZlcnNpb24iOiJvcGVuaWRjb25uZWN0LTEuMCJ9.AtVs_PAsk8-O1jhPwsSIOqaCcDmc1lfE8gY2zgngyJf-ryC7HbhWuOQ_FcwVSHu9Og0Q9DqhTiOLAgeF6C2yHu88o72Bb6AFYJnn8Fyb-hEya3oggQU7j3jdNQB15S-p15ERvNwdT9nSWyxfezeruhBRtaC676iUOMLk61N8HyM4jnadWeGiDUC-7L4ZfLSkMnI0gy3I0dLQ6wKwyuRXPWbZcmqimCKTrVSmBuRRjQ-JLFyaWn2quyki7tSlDpVZ_o_9zwIYLkiFW4Mc1gOAbg-Gz7jqyVb-drarWLNQJWXsqfF0JERk19lTjA1CGW9nbcwhcEnmbFCtYavOW_X8YQ","token_type":"bearer","expires_in":299}
```

Failed Example:
```
HTTP/1.1 400
Cache-Control: no-store
Content-Length: 90
Content-Type: application/json
Pragma: no-cache
Server: Jetty(9.4.19.v20190610)

{
    "error_description": "authorization_pending",
    "error": "authorization_pending"
}
```

## Ping Callback
Gluu Server will send the callback to the client notification endpoint depending on the status of the request already defined in CIBA document. It's important to keep in mind that the security considerations should be done also here, it means TLS version 1.2 and list of ciphers supported.

Request body will be done in the same way that is already defined in CIBA.

Example:
```
Content-Type: application/json
Authorization: Bearer ebq/mzAm_2H2sqcnogfc=
Server: Jetty(9.4.19.v20190610)

{"auth_req_id": "2dc59a83b2318d2486c61a1c8015472f11711a5bba3ec40d"}
```

Response of this request is not processed by Gluu Server based on specs.
