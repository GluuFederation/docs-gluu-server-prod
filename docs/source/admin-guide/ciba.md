# OpenID Connect Client Initiated Backchannel Authentication Flow (CIBA)

OpenID Connect Client Initiated Backchannel Authentication Flow is an authentication flow
like OpenID Connect. However, unlike OpenID Connect, there is direct Relying Party to OpenID
Provider communication without redirects through the user's browser.

[OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html) allows Relying Parties
(RP) to authenticate their users for clients of all types, including browser-based JavaScript
and native mobile apps, to launch sign-in flows and receive verifiable assertions about the
identity of signed-in users.

In all of these flows initiated by the RP, the end-user interaction from the consumption
device is required and, they are based on HTTP redirection mechanisms. However, some use cases
not covered by these flows have been raised, where the RP needs to be the initiator of the
user authentication flow and end-user interaction from the consumption device is not needed.

Client Initiated Backchannel Authentication (CIBA) is a new authentication flow in which RPs,
that can obtain a valid identifier for the user they want to authenticate, will be able to
initiate an interaction flow to authenticate their users without having end-user interaction
from the consumption device. The flow involves direct communication from the Client to the
OpenID Provider without redirect through the user's browser (consumption device).

This specification does not change the semantics of the OpenID Connect Authentication flow.
It introduces a new endpoint to which the authentication request is posted. It introduces a
new asynchronous method for authentication result notification or delivery. It does not
introduce new scope values nor does it change the semantics of standard OpenID Connect
parameters.

As the user does not provide authentication credentials directly to the consumption device,
supporting this flow requires the to OP have some mechanism of initiating user authentication
out-of-band from the interaction with the consumption device.

For more information, see [OpenID Connect Client Initiated Backchannel Authentication Flow](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0-ID1.html)

## Protocol Overview

Client Initiated Backchannel Authentication (CIBA) enables a Client to initiate the
authentication of an end-user by means of out-of-band mechanisms.

1. The Client makes an "HTTP POST" request to the Backchannel Authentication Endpoint to ask
for end-user authentication.

1. The OP will respond immediately with a unique identifier that identifies that
authentication while it tries to authenticate the user in the background.

1. The Client will receive the ID Token, Access Token and optionally Refresh Token by means
of either the Poll, Ping or Push modes, this choice must be established by the Client at
registration time.

    - *Poll Mode.* When configured in Poll mode, the Client will poll the token endpoint to
    get a response with the tokens.

    - *Ping Mode.* When configured in Ping mode, the OP will send a request to a callback URI
    previously registered by the Client with the unique identifier returned from the
    Backchannel Authentication Endpoint. Upon receipt of the notification, the Client makes a
    request to the token endpoint to obtain the tokens.

    - *Push Mode.* When configured in Push mode, the OP will send a request with the tokens
    to a callback URI previously registered by the Client.

It's handy to know some CIBA terminology:

- *Consumption Device (CD).* The Consumption Device is the device that helps the user consume
the service. In the CIBA use case, the user is not necessarily in control of the CD. For
example, the CD may be in the control of an RP agent (e.g. at a bank teller) or may be an RP
controlled device (e.g. a petrol pump).

- *Authentication Device (AD).* The device on which the user will authenticate and authorize
the request, often a smartphone.

## Discovery Metadata

- *Grant Type.* This specification introduces the CIBA grant type (an extension grant type
as defined by [Section 4.5 of OAuth 2.0](https://tools.ietf.org/html/rfc6749#section-4.5))
with the value: ```urn:openid:params:grant-type:ciba```

- *OpenID Provider Metadata.* The following authorization server metadata parameters are
introduced for OPs publishing their support of the CIBA flow:

    - *backchannel_authentication_endpoint*. URL of the OP's Backchannel Authentication
    Endpoint.

    - *backchannel_token_delivery_modes_supported.* JSON array containing one or more of the
    following values: poll, ping and push.

    - *backchannel_authentication_request_signing_alg_values_supported.* JSON array
    containing a list of the JWS signing algorithms (alg values) supported by the OP for
    signed authentication requests.

    - *backchannel_user_code_parameter_supported.* Boolean value specifying whether the OP
    supports use of the user_code parameter.

Example configuration request using oxauth-client:

```
OpenIdConfigurationClient client = new OpenIdConfigurationClient(configurationEndpoint);
OpenIdConfigurationResponse response = client.execOpenIdConfiguration();
```

Configuration Request:

```
GET /.well-known/openid-configuration HTTP/1.1
Host: idp.example.com
```

Configuration Response:

```
HTTP/1.1 200
Content-Length: 6758
Content-Type: application/json
Server: Jetty(9.4.11.v20180605)

{
  .....
  "backchannel_authentication_endpoint" : "https://idp.example.com:8443/restv1/bc-authorize",
  "backchannel_token_delivery_modes_supported" : [ "poll", "ping", "push" ],
  "backchannel_authentication_request_signing_alg_values_supported" : [
    "RS512",
    "ES256",
    "ES384",
    "ES512",
    "ES512",
    "PS256",
    "PS384",
    "PS512"
  ],
  "backchannel_user_code_parameter_supported" : true,
  "grant_types_supported" : [
    .....
    "urn:openid:params:grant-type:ciba"
  ],
  .....
}
```

## Dynamic Client Registration

Clients registering to use CIBA must indicate a token delivery mode. When using the *ping*
or *poll* mode, the Client must include the CIBA grant type in the *grant_types* field. When
using the *ping* or *push* mode, the Client must register a client notification endpoint.
Clients intending to send signed authentication requests must register the signature
algorithm that will be used.

The following parameters are introduced by this specification:

- *backchannel_token_delivery_mode.* One of the following values are required: poll, ping
or push.

- *backchannel_client_notification_endpoint.* Required if the token delivery mode is set to
ping or push. This is the endpoint to which the OP will post a notification after a
successful or failed end-user authentication. It must be an HTTPS URL.

- *backchannel_authentication_request_signing_alg.* The JWS algorithm alg value that the
Client will use for signing authentication request. When omitted, the Client will not send
signed authentication requests.

- *backchannel_user_code_parameter.* Boolean value specifying whether the Client supports
the user_code parameter. If omitted, the default value is false.

Example registration request using oxauth-client:

```
RegisterRequest registerRequest = new RegisterRequest(ApplicationType.WEB, "oxAuth test app", null);
registerRequest.setGrantTypes(Arrays.asList(GrantType.CIBA));

registerRequest.setBackchannelTokenDeliveryMode(BackchannelTokenDeliveryMode.PUSH);
registerRequest.setBackchannelClientNotificationEndpoint(backchannelClientNotificationEndpoint);
registerRequest.setBackchannelAuthenticationRequestSigningAlg(AsymmetricSignatureAlgorithm.RS256);
registerRequest.setBackchannelUserCodeParameter(true);

RegisterClient registerClient = new RegisterClient(registrationEndpoint);
registerClient.setRequest(registerRequest);
RegisterResponse registerResponse = registerClient.exec();
```

Registration Request:

```
POST /restv1/register HTTP/1.1
Content-Type: application/json
Accept: application/json
Host: idp.example.com

{
  "grant_types" : [ "urn:openid:params:grant-type:ciba" ],
  "application_type" : "web",
  "backchannel_client_notification_endpoint" : "https://idp.example.com:8443/oxauth-ciba-client-test/client-notification-endpoint",
  "jwks_uri" : "https://idp.example.com:8443/oxauth/restv1/jwks",
  "backchannel_user_code_parameter" : true,
  "backchannel_authentication_request_signing_alg" : "RS256",
  "client_name" : "oxAuth test app",
  "backchannel_token_delivery_mode" : "push"
}
```

Registration Response:

```
HTTP/1.1 200
Cache-Control: no-store
Content-Length: 1561
Content-Type: application/json
Pragma: no-cache
Server: Jetty(9.4.11.v20180605)

{
    "application_type": "web",
    "registration_client_uri": "https://idp.example.com:8443/restv1/register?client_id=4251a8c4-69e3-4d3e-a807-758ecbc51118",
    "registration_access_token": "e9ecb1a1-001c-4d04-b2f2-b42e35664975",
    "client_id": "4251a8c4-69e3-4d3e-a807-758ecbc51118",
    "token_endpoint_auth_method": "client_secret_basic",
    "scope": "profile openid permission super_gluu_ro_session work_phone phone address org_name clientinfo email user_name test oxd uma_protection",
    "backchannel_user_code_parameter": true,
    "client_secret": "f101f27b-0f18-4bff-9470-c33361f28ff9",
    "client_id_issued_at": 1574831171,
    "backchannel_authentication_request_signing_alg": "RS256",
    "client_name": "oxAuth test app",
    "backchannel_token_delivery_mode": "push",
    "id_token_signed_response_alg": "RS256",
    "grant_types": ["urn:openid:params:grant-type:ciba"],
    "subject_type": "pairwise",
    "client_secret_expires_at": 1574917571,
    "jwks_uri" : "https://idp.example.com:8443/oxauth/restv1/jwks",
    "backchannel_client_notification_endpoint": "https://idp.example.com:8443/oxauth-ciba-client-test/client-notification-endpoint",
    "access_token_signing_alg": "RS256",
}
```

## Poll, Ping and Push Modes

This specification allows the Client to get the authentication result in three ways: poll,
ping or push.

In the *Push* mode, the OP will post the full authentication result to the Client.

![CIBA Push Mode](../img/admin-guide/ciba/CIBAPushMode.png)

In the *Ping* mode, the OP will post the unique identifier of the authentication session to
the Client, the Client will then retrieve the authentication result from the token endpoint
using the new grant type.

![CIBA Ping Mode](../img/admin-guide/ciba/CIBAPingMode.png)

In the *Poll* mode, the authentication result is retrieved by the Client by polling the OP's
token endpoint using the new grant type.

![CIBA Poll Mode](../img/admin-guide/ciba/CIBAPollMode.png)

## Authentication Request
CIBA authentication request contains a list of parameters that should be sent depending on the mode(ping, poll, push), however here is the main list of parameters:

- *scope (required)* The scope of the access request as described by Section 3.3 of [RFC6749](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html#RFC6749). OpenID Connect implements authentication as an extension to OAuth 2.0 by including the openid scope value in the authorization requests.
- *client_notification_token (required)* if the Client is registered to use Ping or Push modes. It is a bearer token provided by the Client that will be used by Gluu Server to authenticate the callback request to the Client.
- *acr_values (optional)* Requested Authentication Context Class Reference values. Space-separated string that specifies the acr values that Gluu Server is being requested to use for processing this Authentication Request, with the values appearing in order of preference.
- *login_hint_token (optional)* A token containing information identifying the end-user for whom authentication is being requested.
- *id_token_hint (optional)* An ID Token previously issued to the Client by Gluu Server being passed back as a hint to identify the end-user for whom authentication is being requested.
- *login_hint (optional)* The value may contain an email address, phone number, account number, subject identifier, username, etc., which identifies the end-user to the OP.
- *binding_message (optional)* A human readable identifier or message intended to be displayed on both the consumption device and the authentication device to interlock them together for the transaction by way of a visual cue for the end-user.
- *user_code (optional)* A secret code, such as password or pin, known only to the user but verifiable by Gluu Server. The code is used to authorize sending an authentication request to user's authentication device.
- *requested_expiry (optional)* A positive integer allowing the client to request the `expires_in` value for the `auth_req_id` the server will return.

Example:
```
POST /restv1/bc-authorize HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: test.gluu.org
Authorization: Basic MTIzLTEyMy0xMjM6WkE1aWxpTFFDYUR4

scope=openid&client_notification_token=12-12&acr_values=simple_password_auth&login_hint=test_user
```

#### Successful Authentication Response
Gluu Server is going to return an HTTP 200 OK response to the Client to indicate that the authentication request has been accepted and it is going to be processed. The body of this response will contain:

- *auth_req_id (required)* This is a unique identifier to identify the authentication request made by the Client.
- *expires_in (required)* A positive integer value indicating the expiration time of the `auth_req_id` in seconds since the authentication request was received.
- *interval (optional)* A positive integer value indicating the minimum amount of time in seconds that the Client MUST  wait between polling requests to the token endpoint.

Example:
```
HTTP/1.1 200
Cache-Control: no-store
Content-Length: 116
Content-Type: application/json
Server: Jetty(9.4.19.v20190610)

{
    "auth_req_id": "01754518964fba15ca786e0d82e1030c320733a10fddfd6d",
    "interval": 2,
    "expires_in": 3600
}
```

#### Authentication Error Response
Error response is sent using a HTTP code different than 200 and a json body containing some information about the error which could containg these fields:

- *error (required)* A single error code that could contain following values listed below.
- *error_description (optional)* Human-readable text providing additional information.

List of authentication error codes associated to HTTP Errors:

HTTP 400 Bad Request:
  - *invalid_request*
  - *invalid_scope*
  - *expired_login_hint_token*
  - *unknown_user_id*
  - *unauthorized_client*
  - *missing_user_code*
  - *invalid_user_code*
  - *invalid_binding_message*

HTTP 401 Unauthorized
  - *invalid_client*

HTTP 403 Forbidden
  - *access_denied*

Example:
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

## Ping Callback
In case that the client is registered to use Ping mode, then Gluu Server will send an HTTP POST Request to the client notification endpoint after a successful or failed end-user authentication.

In this mode the OP sends the `client_notification_token` as a bearer token in the Authorization header field and sends only the `auth_req_id` in the body of the request. The request uses the `application/json` media type.

In case the request is expired, OP will send same ping callback and the expiration message will be received once client calls token endpoint.

Example:
```
Content-Type: application/json
Authorization: Bearer ebq/mzAm_2H2sqcnogfc=
Server: Jetty(9.4.19.v20190610)

{"auth_req_id": "2dc59a83b2318d2486c61a1c8015472f11711a5bba3ec40d"}
```
Response of this request is not processed by Gluu Server based on specs.

## Push Callback

#### Authorized Push Callback
If the client is registered in push mode and the end-user is authenticated correctly, then OP will deliver a payload that includes an ID Token, an Access Token and optionally, a Refresh Token to the client notification endpoint.

Example:
```
Content-Type: application/json
Authorization: Bearer ebq/mzAm_2H2sqcnogfc=
Server: Jetty(9.4.19.v20190610)

{
    "access_token": "1532284a-b357-462c-8749-517d3d5483e1",
    "refresh_token": "4219ebac-3e18-446b-bd17-f2dfdbfab405",
    "auth_req_id": "55da56321ca83b6d1dbc5fbab83adb50b941e5021521f135",
    "id_token": "eyJraWQiOiJlYTc4NDgxYy05OTJkLTRmN2UtYTkzMS03NjM2NTYyMzgwZjVfc2lnX3JzMjU2IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiVzdHVnlqTzVmLXh4dS1vQnRJRnRBUSIsImF1ZCI6IjEyMy0xMjMtMTIzIiwiYWNyIjoic2ltcGxlX3Bhc3N3b3JkX2F1dGgiLCJzdWIiOiJ0VmRiMUpFZnpLeHhkUE45RkU1TE0xQndaTjRaTHF0SF81Y0RIdkstaWxJIiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOmF1dGhfcmVxX2lkIjoiNTVkYTU2MzIxY2E4M2I2ZDFkYmM1ZmJhYjgzYWRiNTBiOTQxZTUwMjE1MjFmMTM1IiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOnJ0X2hhc2giOiJYYjg2V2t1TDdtb2FrUWc2ejg1aDFRIiwiYW1yIjpbIi0xIl0sImlzcyI6Imh0dHBzOi8vdGVzdC5nbHV1Lm9yZzo4NDQzIiwiZXhwIjoxNTkyOTI0MTIxLCJpYXQiOjE1OTI5MjA1MjEsIm94T3BlbklEQ29ubmVjdFZlcnNpb24iOiJvcGVuaWRjb25uZWN0LTEuMCJ9.0KBg06A43ujDAL2bw3855V1zWtrxcg7RML2CQRCU8rWGn-IB-mhTZgxvRMjlMnb8fq8VQE3F2Snpl1Te0bjQRrz71_-nUnt0VdCnxOCiIv5kr46kp6kiM2lQnCeRrPKIY2D05EYxtArPsQvsnA7-BetXpGD6K79b-Y05WCF4KzFinBSUyOWScE7jy0X0cgF2ns4lChotjFOD8tUnAleGGKa59W3t3KJJchoD6XFE9qOW6c5IqYHpTBhcQmYDtPsjW9DjJ-x3IuHBRC5PSkC7d0FEJBfrzFnNnsYC7D93rca9QQSfJFy6BF0INwpys6L5jg_QfoyEuKI1_Iq2uZU8UA",
    "token_type": "bearer",
    "expires_in": 299
}
```

#### Push Error Callback
In case the authentication fails for any reason, it means client doesn't response, he denies the authorization or any reason, OP will send an error payload to the client notification endpoint.

Body of the callback could contain these following parameteres:
- *error_description (optional)* Human-readable text providing additional information, used to assist the client developer in understanding the error.
- *error (required)* A single error code, values are listed below.
- *auth_req_id (required)* The authentication request identifier.

Error codes applicable to the push error payload:
- *access_denied*
- *expired_token*
- *transaction_failed*

Example:
```
Content-Type: application/json
Authorization: Bearer ebq/mzAm_2H2sqcnogfc=
Server: Jetty(9.4.19.v20190610)

{
    "auth_req_id": "05b64509ef9dbf9125783d0a23413e9917a5a006df2fc6d5",
    "error_description": "The end-user denied the authorization request.",
    "error": "access_denied"
}
```

## Token Request
Token request should be done using CIBA grant and is only used in `poll` and `ping` flows, so this endpoint should be used in this way:

- *poll mode* In this case, client should call every N seconds to this endpoint.
- *ping mode* client should call once he receives the callback from the OP, however it's also possible to call to the endpoint before, in that case, the behavior would be very similar than `poll` mode.

Custom parameters for CIBA grant type are:
- *grant_type (required)* Value MUST be `urn:openid:params:grant-type:ciba`
- *auth_req_id (required)* It's the unique identifier to identify the authentication request made by the Client.

Example:
```
POST /restv1/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: test.gluu.org
Authorization: Basic MTIzLTEyMy0xMjM6WkE1aWxpTFFDYUR4

grant_type=urn%3Aopenid%3Aparams%3Agrant-type%3Aciba&authReqId=4ba35d535c8e99ea5d9aa14bd13d5d42607e362fae1df53a
```

#### Successful Token Response
If the authorization goes fine, then authorization server will return all tokens according to the configuration and a HTTP 200 status.

Example:
```
HTTP/1.1 200
Cache-Control: no-store
Content-Length: 1122
Content-Type: application/json
Pragma: no-cache
Server: Jetty(9.4.19.v20190610)

{"access_token":"8cc0cb03-efdb-4545-a1dd-a5568bff6aa9","id_token":"eyJraWQiOiJlYTc4NDgxYy05OTJkLTRmN2UtYTkzMS03NjM2NTYyMzgwZjVfc2lnX3JzMjU2IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiNllLcGVKUlhHNldDZWcxTnY5QUVJZyIsImF1ZCI6IjEyMy0xMjMtMTIzIiwiYWNyIjoic2ltcGxlX3Bhc3N3b3JkX2F1dGgiLCJzdWIiOiJpRDUyZlN4TVh5YjNFRnNjR1d4TlUxZnB5UU9qQWlMY3RkSldFQk55M1BVIiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOmF1dGhfcmVxX2lkIjoiNGJhMzVkNTM1YzhlOTllYTVkOWFhMTRiZDEzZDVkNDI2MDdlMzYyZmFlMWRmNTNhIiwidXJuOm9wZW5pZDpwYXJhbXM6and0OmNsYWltOnJ0X2hhc2giOiJianFrYS1tOS1xZnpacE1rUXB5cURBIiwiYW1yIjpbIi0xIl0sImlzcyI6Imh0dHBzOi8vdGVzdC5nbHV1Lm9yZzo4NDQzIiwiZXhwIjoxNTkyODc0MDUyLCJpYXQiOjE1OTI4NzA0NTIsIm94T3BlbklEQ29ubmVjdFZlcnNpb24iOiJvcGVuaWRjb25uZWN0LTEuMCJ9.AtVs_PAsk8-O1jhPwsSIOqaCcDmc1lfE8gY2zgngyJf-ryC7HbhWuOQ_FcwVSHu9Og0Q9DqhTiOLAgeF6C2yHu88o72Bb6AFYJnn8Fyb-hEya3oggQU7j3jdNQB15S-p15ERvNwdT9nSWyxfezeruhBRtaC676iUOMLk61N8HyM4jnadWeGiDUC-7L4ZfLSkMnI0gy3I0dLQ6wKwyuRXPWbZcmqimCKTrVSmBuRRjQ-JLFyaWn2quyki7tSlDpVZ_o_9zwIYLkiFW4Mc1gOAbg-Gz7jqyVb-drarWLNQJWXsqfF0JERk19lTjA1CGW9nbcwhcEnmbFCtYavOW_X8YQ","token_type":"bearer","expires_in":299}
```

#### Token Error Response
If the authorization is not completed, then authorization server could return one of these error response:

- *authorization_pending* The authorization request is still pending as the end-user hasn't yet been authenticated.
- *slow_down* A variant of "authorization_pending", the authorization request is still pending and polling should continue, but the interval MUST be increased by at least 5 seconds for this and all subsequent requests.
- *expired_token* The auth_req_id has expired. The Client will need to make a new Authentication Request.
- *access_denied* The end-user denied the authorization request.
- *invalid_grant*
- *invalid_request*
- *unauthorized_client*

Example:

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

## Firebase integration

CIBA internally generates an authorization url that should be sent to the end-user and it should be shown in the end-user device, it could be in the navigator, mobile app or other kind of supported agents. Gluu AS has already integrated Firebase in order to send these authorization urls to the end-user and also it can be used using interception scripts which is detailed in the next section.

To use Firebase integration, Gluu AS should know which Firebase token of the device should be used to send those push notification containing the authorization url. In order to associate every user with an end-user device, Gluu AS has `backchannelDeviceRegistrationEndpoint` endpoint to register end-user Firebase token.

Device registration parameters:
- *device_registration_token (required)* This should be gotten from Firebase after device is registered to receive push notifications.
- *id_token_hint (required)* This should be gotten after user authentication and authorization in Gluu AS, it's used to identify the end-user that will be associated with the Firebase device.

Example:
```
POST /restv1/bc-deviceRegistration HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: test.gluu.org

device_registration_token=dgpjEZK6nnE:APA91bFqFQUIi9vG3-XxDr-Luqo9bIg1c8XnMuFKCRMrCdoyCz-UY-LFmaubp505tznTjRo_omQ0_mTZMU2aCy2shYahKaKyZEWij-VgnfVaE7JBb-Eg2JsE9puX-raVaE6Xy0vEkQ50&id_token_hint=eyJraWQiOiJkNTVjZTRmYy00ODZkLTQ2YjItYWExNy1jOWRkZjEzY2IzOTlfc2lnX3JzMjU2IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiTTdKVmNpR2YyY2p0ckE0QVZFc2Q2ZyIsInN1YiI6InFIUHUweEZ5NTJSSkR1cThUdVpQNklGNEVUZnI3N3FZeTdyOEVQSE82RnMiLCJhbXIiOlsiLTEiXSwiaXNzIjoiaHR0cHM6Ly9jZS1kZXY1LmdsdXUub3JnIiwibm9uY2UiOiIzOGFiMzZjZi0wOTQ2LTRkMTEtYWU1Yy05MDkwYjUyNWU0ZDUiLCJzaWQiOiI0NTE0OTQyZC1hOTVmLTRlYzItOWM5OC0xY2Y5OTIzYmI3ODYiLCJveE9wZW5JRENvbm5lY3RWZXJzaW9uIjoib3BlbmlkY29ubmVjdC0xLjAiLCJhdWQiOiIyNzE4YTg2ZC02YzlhLTQ1MjEtYjdjMi1lNWJkZGM2NzZkOWEiLCJhY3IiOiJhdXRoX2xkYXBfc2VydmVyIiwic19oYXNoIjoiUTRBNmFkUkNMTGozX2lZcjNUaTRQUSIsImF1dGhfdGltZSI6MTYwNDY5Mjk2NSwiZXhwIjoxNjA0Njk2NTY1LCJpYXQiOjE2MDQ2OTI5NjV9.iVqfhUnpqPs0TpAo4jKok2Oh11SyPr4iyYU0DLBlHnJL7AZL66ohGKy7rj--ohqiKllIldwYrspau9vqJwBpMsqTcfxKmKgfqhJrFAfdCmpDFgGrQea-9bpC39cE2z5nt4LYzKI-fE1D9jn3Cr7SN4litG16E87BO0Wwr64y4Ns_D3y-TeNE6xZXEvicKjDB9rRMbnlzZec3v7orS85uCCLbN27QNJ4TfyCBGrqVR3_7oYRRVtxQ9I-5j7q9exQg2hjncluNpg_Bev-fvyjwXRlHjZgnE5KYlX8ZdpFBEO-zFL9WQbb8igEkeOHtUxfqbvzJccBOXOtJwIDvmmCJnQ
```

Gluu AS should be also allowed to send push notification and it will be done using some Firebase configuration that can be found in oxTrust, section to configuration json properties of oxAuth, all properties are found in the section `cibaEndUserNotificationConfig`.

![CIBA Firebase Configuration](../img/admin-guide/ciba/CIBA-FirebaseConfig.png)

In order to associate and test these whole flow, Gluu AS has a page to associate devices and also to test CIBA flow (this shouldn't be used in production). Once whole Firebase configuration is done according to the previous documentation and with Firebase activated, you can use it to test your environment. To test it, you can navigate to `/ciba`, for instance, *https://test.gluu.org/oxauth/ciba*, here there is a screenshot that you should see.

![CIBA Firebase Configuration](../img/admin-guide/ciba/CIBA-Test1.png)

Also this page will ask you for the permission to receive push notifications, you should allow it. After that, press `Authenticate User` button, it will start common authentication flow in order to identify which user you want to associate to this navigator/device.

Once you finish the authentication flow, you will be back again to the same page, but you should have your `Id Token` in the screen. After some seconds, below of that section you will see a section called `Instance ID Token`, this is your Firebase identificator that will be used by CIBA to send you push notifications. Here you can press `Delete Token` button just to update that token and create a new one. At this point, this page uses `/bc-deviceRegistration` endpoint to associate user and this navigator.

![CIBA Firebase Configuration](../img/admin-guide/ciba/CIBA-Test2.png)

## Interception Script

It is also possible to use interception script to send that authorization url to the end-user using any custom channel defined in the deployment.

Those interception script could be configured using oxTrust in the section `Other Custom Scripts -> CIBA End User Notification`.

![CIBA Interception Script](../img/admin-guide/ciba/CIBAInterceptionScript.png)

Gluu Server could use default Firebase notifications or it could use the interception script configured in database if there is any.

## Configuration

All this configuration could be managed using oxTrust.

#### JSON Configuration

This is the list of new properties or some others that have to be considered whenever CIBA should be deployed.

| Property | Values | Description |
|----------|--------|-------------|
| cibaEnabled | | Boolean value specifying whether turn on CIBA. If true AS will process CIBA requests. |
| backchannelClientId | | Client identificator that will be used to associate end-user with a device. |
| backchannelRedirectUri | | Url used to process the callback once the authentication/authorization is done |
| backchannelAuthenticationEndpoint | | CIBA Endpoint used to initiate the authentication/authorization flow using CIBA flow. |
| backchannelDeviceRegistrationEndpoint | | CIBA Endpoint used to associate a device with a people entry. This device would be used to process all authentications/authorizations steps |
| backchannelTokenDeliveryModesSupported | poll ping push | Token delivery modes that could be supported in the authentication server. It could depend on the CIBA flow. |
| backchannelAuthenticationRequestSigningAlgValuesSupported | RS512 ES256 ES384 ES512 ES512 PS256 PS384 PS512 | Signing algorithms supported to process authentication requests. |
| backchannelUserCodeParameterSupported | true false | It defines whether authorization server will accept or not User Code parameter in the CIBA authentication/authorization flow |
| backchannelBindingMessagePattern | *regex* | This is a regex used to validate the content in the binding_message parameter sent by the client. |
| backchannelAuthenticationResponseExpiresIn | | Default limit time used to process the authentication response. |
| backchannelAuthenticationResponseInterval | | Default interval recommended to the client to call to the /token endpoint to verify whether client has answered or not. |
| backchannelRequestsProcessorJobIntervalSec | | Time interval used for the job responsible to process all requests. |
| backchannelRequestsProcessorJobChunkSize | | Max limit of requests that every cycle in the job can process. |
| cibaGrantLifeExtraTimeSec | | Extra time added for a CIBA request in cache in order to have extra time which client could use to do the `/token` endpoint call. |
| cibaMaxExpirationTimeAllowedSec | | Limit of time that client could send in the CIBA authorization request, it's only used as a validation. |
| backchannelLoginHintClaims | inum uid mail | Determines which value is going to be shared by the client to identify his client. |
| cibaEndUserNotificationConfig | | This property contains a set of other properties related to Firebase configuration. It could be gotten from the Firebase console. One of the fields *notificationKey* must be put encrypted, therefore it is highly recommended to use oxTrust to put this value. |
| grantTypesSupported | | There is a new grant type for this implementation and according to the specifications, this must be *urn:openid:params:grant-type:ciba* |
| dynamicGrantTypeDefault | | There is a new grant type for this implementation and according to the specifications, this must be *urn:openid:params:grant-type:ciba* |

#### CIBA Client attributes

These attributes were added to process all CIBA requests per client.

| Attribute | Description |
|--|--|
| oxAuthBackchannelAuthenticationRequestSigningAlg | Signing algorithm used to process requests received in /bc-authorize endpoint as JWT |
| oxAuthBackchannelClientNotificationEndpoint | Client endpoint that is used by ping and push modes to deliver messages depending the case. |
| oxAuthBackchannelTokenDeliveryMode | Defines the flow that will be used by the client, this value is one of the supported modes configured in the oxAuth json property *backchannelTokenDeliveryModesSupported* |
| oxAuthBackchannelUserCodeParameter | Defines whether this client will be able to sent a User Code or not. |
