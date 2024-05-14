# Mod oauth OpenID Connect + WSO2 API Manager / Identity Server + Gluu Server

# Tested on Setup
- GLuu Server 4.5
- WSO2 API Manager 4.3.0, 3.2.0
- WSO2 Identity Server 7.0.0
- Apache RP (mod Auth OpenID client)
- All are running in ubuntu 20

# Pre-requirements
- Running [Gluu server (v4.x)](https://gluu.org/docs/gluu-server/4.5/installation-guide/install-ubuntu/)
- Running WSO2 [API manager (v4.3.0/3.2.0)](https://apim.docs.wso2.com/en/latest/install-and-setup/install/installing-the-product/installing-api-m-runtime/) / [Identity Server (v7.0.0)](https://is.docs.wso2.com/en/next/get-started/quick-set-up/)
- Running Apache server with [mod_ouath_openidc](https://github.com/OpenIDC/mod_auth_openidc) enabled


In this tutorial, I have used below ***`hostname`***:
- `idp.gluu.mydomain` for Gluu server
- `idp.wso2.mydomain` for WSO2 APIM and IS
- `sso.sp.mydomain` for service provider

# Create OpenID Client at Gluu Server

Please create an OpenID client in your gluu server using the below configurations:

OPENID CONNECT CLIENTS DETAILS
------------------------------
- **Name:** wso2am
- **Subject Type:** pairwise
- **ClientSecret:** XXXXXXXXXXX
- **Application Type:** web
- **Persist Client Authorizations:** true
- **Pre-Authorization:** false
- **Authentication method for the Token Endpoint:** client_secret_post
- **Logout Session Required:** false
- **Include Claims In Id Token:** false
- **Disabled:** false
- **Login Redirect URIs:** [https://idp.wso2.mydomain:9444/commonauth]
- **Scopes:** [openid, user_name, profile, email]
- **Grant types:** [authorization_code]
- **Response types:** [code]

# Configure WSO2 API Manager

I assume you already have a running WSO2 API Manager server. If you don't have a running server, please check [this](#install-wso2) or [official documentation](https://apim.docs.wso2.com/en/latest/install-and-setup/install/installing-the-product/installing-api-m-runtime/#installing-the-api-manager-runtime) for wso2 API manager installtion. 

## Add Gluu Server as External IDP
Let's add gluu server as an external IDP in WSO2 API Manager. You can add External Identity Providers from ***`Identity Provider`*** Section. Click on `Add` button under `Identity Provider` section and add following informations:

### Basic Information
- **Identity Provider Name**: GluuIDP
- **Display Name**: Gluu IDP
- **Choose IDP Certificate Type**: Upload IDP Certificate
- **IDP Public Certificate**: Upload your Gluu Server public SSL in .pem format
- **IDP Issuer**: Gluu Server issuer name

### Claim Configuration
- **Basic claim**: select `http://wso2.org/claims/role` in basic local claim dialect

### Role Configuration
- **IDP Role**: We can skip this for now

### Federated Authenticators
In this setup, we are using Inbound OpenID authentication. Please apply following configuration in **`OAuth2/OpenID Connect Configuration`** section:

- `Enable` OAuth2/OpenID Connect
- **Clien Id**: client id from the client created in gluu server
- **Client Secret**: client secret from the client created in gluu server
- **Authrorization Endpoint**: `https://idp.gluu.mydomain/oxauth/restv1/authorize`
- **Token Endpoint**: `https://idp.gluu.mydomain/oxauth/restv1/token`
- **Callback Url**: `https://idp.wso2.mydomain:9444/commonauth`
- **Userinfo Endpoint**: `https://idp.gluu.mydomain/oxauth/restv1/userinfo`
- **Logout Endpoint**: `https://idp.gluu.mydomain/oxauth/restv1/end_session`
- **OpenID Connect User ID Location**: Select `User ID found in 'sub' attribute`
- **Scopes**: `openid profile email user_name`

> ***NB:*** Please change endpoint urls according to your server hostname

### Just-in-time Provisioning
- Always provision to User Store Domain: `PRIMARY`
- Provision Silently

After filling in the following information correctly, click on the `Register` button at the end It will register Gluu Server as an External IDP. We are done here, now let's move into ***[Service Provider](#add-service-provider)*** section.

<img width="743" alt="Screenshot 2024-05-14 at 11 11 11" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/394fe202-40dc-42d9-88d2-2e9efc32962f">

## Add Service Provider

From the `Service Provider` section, click on the `Add` button to register a service provider.
You can register a SP if you have a .xml file with all details or you can go manually. Let's proceed with the manual steps:

### Basic Information
- **Service Provider Name**: Give a unique sp name, ex: `mod_oauth_oidc`
- Click on the `Register` button

After registration, Let's configure with the below information:

### Cliam Configuration
- Mark on `Use local claim dialect`

### Inbound Authentication Configuration

Click on `configure` to set inbound authentication for this sp:

- **Callback Url**: Add the redirect URI of your SP

Click on `Add`, Once it is complete it will generate a client ID and secret key. We will need these for the SP server.

### Local and Outbound Authentication 

- **Authentication Type**: select `gluuIDP` from Federated Authentication 
- Mark `Assert identity using mapped local subject identifier` and `Use user store domain in roles`

Configurations are done, click on the `update button` to update the changes.

<img width="1221" alt="Screenshot 2024-05-14 at 11 09 47" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/885f7a9a-a203-49b7-9a86-81d02bbbe96f">

# Setup SP Server

I assume you already have a running Apache server with [mod_oauth_openidc](https://github.com/OpenIDC/mod_auth_openidc) module enabled. If you don't setup yet, please consider this [docs](https://gluu.org/docs/gluu-server/4.5/integration/sswebapps/openidc-rp/) to setup. 

Let's configure VirtualHost in the SP server to allow authentication with the WSO2 API Manager/Identity Server.

```
vi /etc/apache2/sites-available/default-ssl.conf
```
Add the following right under `<VirtualHost _default_:443>`:

```
OIDCProviderMetadataURL https://idp.wso2.mydomain:9444/oauth2/token/.well-known/openid-configuration
OIDCClientID client-id-that-you-got-when-added-sp-in-wso2
OIDCClientSecret (your-client-secret)
OIDCRedirectURI https://sso.sp.mydomain/callback
OIDCResponseType code
OIDCScope "openid profile email"
OIDCSSLValidateServer Off
OIDCCryptoPassphrase (a-random-seed-value)
OIDCPassClaimsAs environment
OIDCClaimPrefix USERINFO_
OIDCPassIDTokenAs payload
<Location "/">
    Require valid-user
    AuthType openid-connect
</Location>
```

Let's restart the Apache service and try to access your sp server secure page. It should redirect the user to the WSO2 login page first, and then WSO2 will redirect to Gluu Server login page for authentication. Once user logged in gluu server, it sends it back to wso2 for authorization and then finally redirects to your SP server page upon  successful authentication and authorization.

# Configure WSO2 Identity Server

Apart from the WSO2 API Manager, the Gluu server also supports OpenID Connect-based authentication with the WSO2 Identity Server. In this part, We will configure WSO2 Identity Server for authenticating with External IDP(Gluu). I assume you already have a running WSO2 IS. If you don't have yet, please consider this [section](#install-wso2) or [official documentation](https://is.docs.wso2.com/en/next/get-started/quick-set-up/). In my case, it's running on `idp.wso2.mydomain:9443`. 

## Add Connection for External IDP

Let's go to `Connection > New Connection` and create a ***Standard-Based IDP***:
- set `IDP` name and choose protocol `OpenID Connect`, then proceeed next
- put `client id`, `client secret`, `authorization endpoint` and `token endpoint` from gluu server. If you don't create client yet for WSO2 Identity server, create it in the similar way like [this](#create-openid-client-at-gluu-server)
- In the next part, upload your gluu server ssl certificate in `.pem` format
- `finish`

So it will look this:

<img width="1108" alt="Screenshot 2024-05-14 at 09 54 43" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/91bcc570-6d82-4cf9-a248-7350284af6e4">

### General

- ***issuer:*** update with your gluu server issuer name correctly

### Settings
Additionally, complete the following things:
- ***User info endpoint URL***
- ***Logout URL***
- ***Scopes:*** Add some required scopes, `email`, `profile`, `user_name` etc.

### JIT User Provisioning

- ***User store:*** PRIMARY
- ***Provision scheme:*** Provision Silently

Everything is updated successfully, let's move into [***`apppliction`***](#add-application) section.

## Add Application
Let's go to `Application > New Application > Standard-Based Application`: 
- ***name:*** app name
- ***protocol:*** OAuth2.0 OpenID Connect

Once you create the application, it will generate `client id` and `secret` in ***Protocol*** section. This is what it looks like:

<img width="1139" alt="Screenshot 2024-05-14 at 10 27 18" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/e75d24b8-96b8-4a64-9058-cb3f9a82e626">

### Protocol
- ***Allow grant types:*** `Code`
- ***Authorized redirect URL:*** `https://sso.sp.mydomain/secure/callback`
- ***Allowed origins*** `https://sso.sp.mydomain`
- ***Client Authentication method***: `client secret post`
- `update` the app


### Login Flow

From the login flow tab, click on the `add sign in option` and select `Gluu IDP` from the Sso flow list. and finally, update.

Configuring the `SP` server is the similar steps explained [here](#setup-sp-server).


# How it Works

![WSO2 with Gluu Server](https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/29e51138-7e34-4aa0-82fb-abe2c131cc78)


# How to Install WSO2 Products
<details>
<summary> Installation of WSO2 API Manager/Identity Server</summary>

1. Let's download the latest version of the wso2 product from their GitHub page:

- [WSO2 Identity Server](https://github.com/wso2/product-is/releases/)
- [WSO2 API Manager](https://github.com/wso2/product-apim/releases/)

Direct Download command:
```
wget https://github.com/wso2/product-is/releases/download/v7.0.0/wso2is-7.0.0.zip
```
```
wget https://github.com/wso2/product-apim/releases/download/v4.3.0/wso2am-4.3.0.zip
```

2. Extract into directory:

```
unzip wso2am-4.3.0.zip
```
```
unzip wso2is-7.0.0.zip
```

3. We need jdk for wso2. Let install JDK if it's not installed and add it to the PATH:

```
sudo apt update
sudo apt install openjdk-11-jdk
java -version
```

Add these two lines in the `.bashrc` file

```
export JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64
export PATH=${JAVA_HOME}/jre/bin:${PATH}
```

Please update `JAVA_HOME` depending on your Java version and path.

4. Let's configure the wso2 API manager before running it. 

```
vi wso2am-4.3.0/repository/conf/deployment.toml
```

Update with these values:

```
[server]
hostname = "hostname"
offset=1
```
5. To run:
```
wso2am-4.3.0/bin/api-manager.sh start
```
```
wso2is-7.0.0/bin/wso2server.sh start
```

By default, WSO2 runs in 9443. Since we have set the `offset` value to `1`, it will be running on port 9444. You can access your wso2 server console page using `[hostname]:[port]/carbon` and default credentials are `admin/admin`.
</details>
