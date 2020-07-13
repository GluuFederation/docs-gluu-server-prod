# Setup Script

## Setup TUI
Setup script uses tui for collect information to install Gluu Server. If TUI is not available on your environment, it switches to command line. If you want to use command line, execute with `-c` argument:
```
/install/community-edition-setup/setup.py -c
```

## Setup Command Line

The setup script will bring up a prompt to provide information for certificate as well as the IP Address and the hostname for the Gluu Server.  Hit `Enter` to accept the default values. 

Refer to the following table for details about available setup options:    

| Setup Option                |  Explanation                               |
|-------------------------|--------------------------------------------|
| Enter IP Address | Used primarily by Apache httpd for the [Listen](https://httpd.apache.org/docs/2.4/bind.html) directive. **Use an IP address assigned to one of this server's network interfaces (usage of addresses assigned to loopback interfaces is not supported)**|
| Enter hostname | Internet-facing FQDN that is used to generate certificates and metadata. **Do not use an IP address or localhost.** |
| Enter your city or locality | Used to generate X.509 certificates. |
| Enter your state or province two letter code | Used to generate X.509 certificates. |
| Enter two letter Country Code | Used to generate X.509 certificates. |
| Enter Organization Name | Used to generate X.509 certificates. |
| Enter email address for support at your organization | Used to generate X.509 certificates. | 
| Optional: Enter oxTrust Admin Password | Used as the default admin user for oxTrust. |
| Optional: Enter Password for LDAP Admin | Used as the LDAP directory manager password, if you not provided it will be same as oxTrust admin password. |
| Install Local WrenDS Server? | Optional: Installs a local DB, used to store user info and configuration data. Can be omitted if using a remote LDAP or Couchbase. |
| Install oxAuth OAuth2 Authorization Server | Required. Includes Gluu's OpenID Connect provider (OP) and UMA authorization server (AS) implementations.|
| Install oxTrust Admin UI | Required. This is the Gluu server admin dashboard. |
| Install Apache 2 web server | Required |
| Install Shibboleth SAML IDP | Optional. Only install if a SAML identity provider (IDP) is needed. |
| Install oxAuth RP | Optional. OpenID Connect test client: useful for test environments, for more details see [here](../admin-guide/openid-connect/#oxauth-rp) |
| Install Passport |  Optional. Install if you want to support external IDP, for instance to offer users social login. |
| Install Casa | Optional. Install if you want to support self-service 2FA. More information is available [here](https://gluu.org/docs/casa). Selecting yes also prompts for [oxd installation](https://gluu.org/docs/oxd) |
| Install oxd | Optional. Install if you want to support simple, static APIs web application developers can use to implement user authentication and authorization against Gluu CE. More information is available [here](https://gluu.org/docs/oxd). |
| Install Gluu Radius | Optional. Installs Radius server. More information is available [here](../admin-guide/radius-server/gluu-radius.md)

When complete, the setup script will show the selections and prompt for confirmation. If everything looks OK, select Y to finish installation. 

After 5-10 minutes the following success message will appear: 

`Gluu Server installation successful! Point your browser to [hostname].`

!!! Login
    Log in using the username `admin` and the password from the setup script prompt e.g `hlE3vzf0hMdD` or the password entered

### Avoiding common issues

Avoid setup issues by acknowledging the following:         

- IP Address: Do **not** use `localhost` for either the IP address or hostname.     

- Hostname:     
     - Make sure to choose the hostname carefully. Changing the hostname after installation is not a simple task.   
     - Use a real hostname--this can always be managed via host file entries if adding a DNS entry is too much work for testing.   
     - For clustered deployments, use the hostname of the cluster that will be used by applications connecting to Gluu.   
     
!!! Warning
    Use a FQDN (fully qualified domain name) as hostname and refrain from using 127.0.0.1 as IP address or usage of private IP is not supported and not recommended.
    
- Only run the setup script **one time**. Running the command twice will break the instance.

If a resolvable DNS host is not used, then it must be added to the hostname of the Operating System hosts file on the server running the browser.

Errors can be found the the `setup_errors.log` file and a detailed step by step installation is found in the `setup.log` file under the `/install/community-edition-setup` folder.

## Script Command Line Options
The setup script can be used to configure your Gluu Server and to add initial data for oxAuth and oxTrust to start. If `setup.properties` or `setup.properties.last.enc` is found in this folder, these properties will automatically be used instead of the interactive setup.

The administrator can use the following command line options to include additional components:

* __-c__ Switches to command line
* __-r__ Install oxAuth RP
* __-p__ Install Passport
* __-d__ specify the directory where community-edition-setup is located. Defaults to '.'
* __-f__ specify `setup.properties` file
* __-h__ invoke this help
* __-n__ no interactive prompt before install starts. Run with `-f`
* __-N__ no Apache httpd server
* __-s__ install the Shibboleth IDP
* __-u__ update hosts file with IP address/hostname
* __-w__ get the development head war files
* __-t__ Load test data
* __-x__ Load test data and exit
* __-stm__ Enable Scim Test Mode
* __--import-ldif=custom-ldif-dir__ Render ldif templates from custom-ldif-dir and import them in LDAP
* __--listen_all_interfaces__ Allow the LDAP server to listen on all server interfaces. This is required for clustered installations to replicate between LDAP servers. If not enabled, the LDAP server listens only to localhost
* __---allow-pre-released-features__ Enable options to install experimental features, not yet officially supported.
* __--remote-ldap__ Allows use of a remote LDAP server. <!-- For further information see https://github.com/GluuFederation/support-docs/blob/master/howto/4.1/setup_remote_LDAP.md -->
* __--remote-couchbase__ Allows use of a remote Couchbase server. <!-- For further information see https://github.com/GluuFederation/support-docs/blob/master/howto/4.1/CE_with_remote_CB.md -->
* __-properties-password__ Encoded setup.properties file password (startinig from 4.1.0, setup.py saves encoded propertes files with name `setup.properties.last.enc`) 
Example Command: `# ./setup.py -ps` This command will install Gluu Server with Passport and Shibboleth IDP.
* __--install-casa__ Install Casa
* __--install-oxd__ Install Oxd Server

!!! Note
    `setup.py` will save an encrypted properties file named `setup.properties.last.enc`. The password is the same as the oxTrust admin password. Retain this password to use this file for future installations. To reuse the file, it needs to be decrypted with the following command:
    ```
    openssl enc -d -aes-256-cbc -in setup.properties.last.enc -out setup.properties.last
    ```
    When prompted, enter the oxTrust admin password.
