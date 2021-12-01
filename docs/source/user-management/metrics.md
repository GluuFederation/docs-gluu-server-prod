# Active User Metrics

## Setup

### Configuration 

 - In oxTrust, navigate to `Configuration` > `JSON Configuration` > `oxAuth Configuration`
 - Make sure there is a valid value in the `statWebServiceIntervalLimitInSeconds` attribute. By default it's set to `60`. 

### Statistics Client

User metrics will be obtained using an OpenID Client. Create a new client using the following as an example: 

```
OPENID CONNECT CLIENTS DETAILS
------------------------------
- **Name:** StatCollector
- **Description:** User statistics collector
- **Client ID:** <auto_generated>
- **Subject Type:** pairwise
- **ClientSecret:** XXXXXXXXXXX
- **Application Type:** web
- **Persist Client Authorizations:** true
- **Pre-Authorization:** false
- **Authentication method for the Token Endpoint:** client_secret_basic
- **Logout Session Required:** false
- **Include Claims In Id Token:** false
- **Disabled:** false
- **Scopes:** [openid, jans_stat]
- **Grant types:** [client_credentials]
- **Response types:** [token]

```



## Testing

We are going to use `Bearer Token` to grab user's info from Gluu Server. You can either use `Postman` or `curl` to complete this task. 

  1. Request an access token. For example: `curl -k -u 'StatCollector_Client_ID:StatCollector_Client_Secret' -d "grant_type=client_credentials&scope=jans_stat" https://<Gluu_server>/oxauth/restv1/token`
  1. Use that access token to obtain metric information using Curl or Postman. For example, using Curl: `curl --location --request GET 'https://<Gluu_server>/oxauth/restv1/internal/stat?month=YEARMONTH&format=openmetrics' --header 'Authorization: Bearer <access_token>'`
  1. After running the command, the output should look like the following: 

```
# HELP refresh_token Refresh Token
# TYPE refresh_token counter
refresh_token{month="202111",grantType="authorization_code",
} 0.0
refresh_token{month="202111",grantType="client_credentials",
} 0.0
# HELP id_token Id Token
# TYPE id_token counter
id_token{month="202111",grantType="authorization_code",
} 144.0
id_token{month="202111",grantType="client_credentials",
} 0.0
# HELP monthly_active_users Monthly active users
# TYPE monthly_active_users counter
monthly_active_users{month="202111",
} 2.0
# HELP access_token Access Token
# TYPE access_token counter
access_token{month="202111",grantType="authorization_code",
} 144.0
access_token{month="202111",grantType="client_credentials",
} 10.0
# HELP uma_token UMA Token
# TYPE uma_token counter
uma_token{month="202111",grantType="authorization_code",
} 0.0
uma_token{month="202111",grantType="client_credentials",
} 0.0
```
