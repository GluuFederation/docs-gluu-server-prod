# PingID authentication

## Overview

This document describes how to integrate Ping Identity's PingID multifactor authentication with Gluu Server by means of an interception script. The script allows users to receive push notifications to their corresponding registered mobile devices in order to get access to applications protected by Gluu Server.

## Requisites

For a successful deployment the following is required:

- A PingOne Cloud Platform account. A trial account can be obtained [here](https://www.pingidentity.com/en/try-ping.html)

- Access to a Gluu Server installation

- [PingID mobile app](https://www.pingidentity.com/en/resources/downloads/pingid.html) (for testing users)

- Test users at Gluu and (optionally) at PingOne

### Mapping of local and remote identities

Configuring the correspondence between local (Gluu) users and remote (PingOne) users is key. Assuming that Gluu `uid` equals to PingOne `username` may not be practical. For this purpose it is required to setup an attribute in Gluu's local database to store the reference to the external identity, ie. PingOne username. If your underlying database is LDAP, this [page](https://www.gluu.org/docs/gluu-server/admin-guide/attribute#custom-attributes) explains how to add an attribute to openDJ schema.

The authentication flow the custom interception script implements may create users at ping side: if a user attempts to login (with Gluu) and the username referenced by the mapping attribute is not found as a pingID user, a new (remote) user is added. This applies as long as the [script](#add the-custom-script) is parameterized with the `addNonExistentPingUser` property. 

When the mapping attribute is not populated, authentication is performed by means of user+password combination only. The next section provides more information about the actual flow steps.

## Authentication flow overview

The script is implemented as a multi-step authentication flow. The number of steps varies according to the particular circumstances presented at login time:

- One step: the user attempting to login does not map to a PingOne identity

- Two steps: the user already has a registered device at PingID (will receive a push notification as 2nd step)

- Three steps: the user does not have a registered device at PingID (will make enrollment as 2nd step, and receive a push notification as 3rd)

Since enrollment of a mobile device is attempted in the three-stepped flow, this may trigger a change in the user status stored at PingID. Status values are explained [here](https://apidocs.pingidentity.com/pingid-api/guide/pingid-api/pid_c_PingIDapiUserManagement/#User-Status-Values). Note that for suspended accounts authentication will always fail.

The following sequence diagram depicts a successful sample journey in the context of a 3-stepped flow and illustrates the entities involved in the solution.

![flow](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/flow.png)

Note that PingID may detect the recipient device for a push is not reachable (eg. due to network problems). In this case, the user is prompted for the OTP code appearing in the screen of the mobile application. This may also happen when the user has explicitly disabled the swipe gesture in the app.

## Ping Identity setup

This section describes configurations to be carried out with your PingID platform account.

### Enable multifactor authentication

1.  In the PingOne admin portal, visit the "Your Environments" home

1.  Add an environment

1.  Choose "Build your own solution" and if using a trial account, ensure the "show trials" toggle is on.

1.  From "Cloud services" section select "PingOne SSO" and "Ping ID"

1.  Continue with the wizard steps and ensure sample users are generated

1.  When finished, go back to the environments home and click on the row of the recently created environment

1.  Both PingOne SSO and PingID should appear listed under "Services"

1.  On the left menu, click on "Experiences" (smiley icon), and then on "Authentication policies"

1.  A policy named "Multi_Factor" appears listed. Expand the row and click on the edit icon

1.  Click on "make default" under the policy name

### Gather Ping ID properties file 

1.  Back in the environments home, click on the ID widget appearing on the row of the environment created on the previous step. You will be taken to Ping ID's admin console

1.  Click on `Setup` > `Ping ID` > `Client integration settings` and download the properties file regarded in the section "INTEGRATE WITH PINGFEDERATE AND OTHER CLIENTS". Store this file in a safe please

## Gather test users

1.  In the PingID's admin console click on `Users` > `Users by service` and select the PingID checkbox

1.  Expand some 2-3 users. Those will show a disabled status with no devices listed. Grab their user names 

*Note*: A username appears right below the full user name (at the top)

## Gluu setup

This section describes configurations to be carried out in Gluu Server.


=== "Community Edition - VM"
    
    ### Transfer script assets

    Extract [this file](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/bundle.zip) to the root (ie. `/`) of your Gluu server. In a standard CE installation this means extraction should take place under `/opt/gluu-server`.
    
    The zip file contains UI pages (forms) and other miscellaneous files. When extracting use the `root` user.
    
    ### Deploy oxauth-pingid library
    
    1. Transfer this [file](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/oxauth-pingid-1.0.jar) to your Gluu instance inside folder `/opt/gluu/jetty/oxauth/custom/libs`. 
    
    1. Navigate to `/opt/gluu/jetty/oxauth/webapps` and edit the file `oxauth.xml` so that in the `extraClasspath` section the following path is added: `oxauth-pingid-1.0.jar`
    
    1. **Restart** oxAuth
    
    If you want to generate the jar file on your own (and possibly inspect the source code) follow the steps [below](#building-oxauth-pingid-library)
        

=== "Cloud Native Edition - Kubernetes"

    ### Transfer script assets and load oxauth-pingid library
    
    There are two methods of loading files into the deployment which can be used to load the files from the two steps below:
    
    -   Extract script assets from [this file](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/bundle.zip).
    
        ```bash
        wget https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/bundle.zip && unzip bundle.zip -d bundle
        ```
    
    - Get oxauth-pingid library from this [file](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/oxauth-pingid-1.0.jar). If you want to generate the jar file on your own (and possibly inspect the source code) follow the steps [below](#building-oxauth-pingid-library)
    
        ```bash
        wget https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/oxauth-pingid-1.0.jar
        ```
    
             
    === "ConfigMaps"
    
        1.  Create a ConfigMap that contains all the files extracted i.e `oxauth.properties`, `enroll.xhtml`, `login.xhtml`, `ppm.xhtml`, and `template.xhtml` and the jar file `oxauth-pingid-1.0.jar`
        
            ```sh
               kubectl create cm oxauth-pingid-integration --from-file=bundle/opt/gluu/jetty/oxauth/custom/i18n/oxauth.properties --from-file=bundle/opt/gluu/jetty/oxauth/custom/pages/auth/pingid/enroll.xhtml --from-file=bundle/opt/gluu/jetty/oxauth/custom/pages/auth/pingid/login.xhtml --from-file=bundle/opt/gluu/jetty/oxauth/custom/pages/auth/pingid/ppm.xhtml --from-file=bundle/opt/gluu/jetty/oxauth/custom/pages/auth/pingid/template.xhtml --from-file=oxauth-pingid-1.0.jar -n <gluu-namespace>                
            ```
        
        1.  Mount the created ConfigMap in your helm values.yaml inside oxauth
        
            ```yaml
            oxauth:
              volumes:
                - name: oxauth-pingid-integration-properties
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "oxauth.properties"
                      path: "oxauth.properties"
                - name: oxauth-pingid-integration-enroll
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "enroll.xhtml"
                      path: "enroll.xhtml"
                - name: oxauth-pingid-integration-login
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "login.xhtml"
                      path: "login.xhtml"
                - name: oxauth-pingid-integration-ppm
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "ppm.xhtml"
                      path: "ppm.xhtml"
                - name: oxauth-pingid-integration-template
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "template.xhtml"
                      path: "template.xhtml"
                - name: oxauth-pingid-integration-lib
                  configMap:
                    name: oxauth-pingid-integration
                    items:
                    - key: "oxauth-pingid-1.0.jar"
                      path: "oxauth-pingid-1.0.jar"
              volumeMounts:
                - name: oxauth-pingid-integration-properties
                  mountPath: /opt/gluu/jetty/oxauth/custom/i18n/oxauth.properties
                  subPath: oxauth.properties
                - name: oxauth-pingid-integration-enroll
                  mountPath: /opt/gluu/jetty/oxauth/custom/pages/auth/pingid/enroll.xhtml
                  subPath: enroll.xhtml
                - name: oxauth-pingid-integration-login
                  mountPath: /opt/gluu/jetty/oxauth/custom/pages/auth/pingid/login.xhtml
                  subPath: login.xhtml
                - name: oxauth-pingid-integration-ppm
                  mountPath: /opt/gluu/jetty/oxauth/custom/pages/auth/pingid/ppm.xhtml
                  subPath: ppm.xhtml
                - name: oxauth-pingid-integration-template
                  mountPath: /opt/gluu/jetty/oxauth/custom/pages/auth/pingid/template.xhtml
                  subPath: template.xhtml
                - name: oxauth-pingid-integration-lib
                  mountPath: /opt/gluu/jetty/oxauth/custom/libs/oxauth-pingid-1.0.jar
                  subPath: oxauth-pingid-1.0.jar                                                                            
            ```
            
        1.  Run helm upgrade 
        
            ```bash
            helm upgrade <release-name> gluu/gluu -f ./values.yaml -n <namespace> --set global.upgrade.enabled=true --set global.persistence.enabled=false
            ```       
        
    
    === "Jackrabbit"
    
        1. Connect to your [Jackrabbit](../installation-guide/install-kubernetes.md#working-with-jackrabbit)
        
        1. After connecting to  Jackrabbit move the extracted content from bundel.zip  and the oxauth-pingid library which should be mapped correctly as below inside jackrabbit
    
            ```bash
            +--- opt
            |   +--- gluu
            |   |   +--- jetty
            |   |   |   +--- oxauth
            |   |   |   |   +--- custom
            |   |   |   |   |   +--- libs
            |   |   |   |   |   |   +--- oxauth-pingid-1.0.jar        
            |   |   |   |   |   +--- i18n
            |   |   |   |   |   |   +--- oxauth.properties
            |   |   |   |   |   +--- pages
            |   |   |   |   |   |   +--- auth
            |   |   |   |   |   |   |   +--- pingid
            |   |   |   |   |   |   |   |   +--- enroll.xhtml
            |   |   |   |   |   |   |   |   +--- login.xhtml
            |   |   |   |   |   |   |   |   +--- ppm.xhtml
            |   |   |   |   |   |   |   |   +--- template.xhtml
            ```        
            
        1. After verifying the content has been moved to jackrabbit. Restart oxauth deployment.
                

### Add the custom script

1.  Log into oxTrust with admin credentials

1.  Visit `Configuration` > `Person Authentication Scripts`. At the bottom click on `Add custom script configuration` and fill values as follows:

    - For `name` use a meaningful identifier, like `pingid`
    
    - In the `script` field use the contents of this [file](https://github.com/GluuFederation/oxAuth/raw/version_4.5.0/Server/integrations/pingid/pingIDAuthenticator.py)
    
    - Tick the `enabled` checkbox
    
    - For the rest of fields, you can accept the defaults
    
1.  Click on `Add new property`. On the left enter `use_base64_key` on the right copy the corresponding value you will find in the properties file downloaded [earlier](#gather-ping-id-properties-file)

1.  Repeat the process for `token`, `org_alias`, and `authenticator_url`

1.  Add another property called `pingUserAttr` and set its value to the name of the attribute that will contain the reference to the remote pingID user, as explained [here](#mapping-of-local-and-remote-identities)

1. (Optional) Add a property `addNonExistentPingUser` if you require users to be created at ping when nonexisting.

1.  Scroll down and click on the `Update` button at the bottom of the page

### Building oxauth-pingid library

If you want to generate the jar file on your own (and possibly inspect the source code) follow the steps below:

1.  In a development machine, ensure Java 8+ and Maven build tool are installed. [Download](https://github.com/GluuFederation/oxAuth/archive/refs/heads/version_4.5.0.zip) oxAuth project  and extract it to a temporary location

1.  `cd` to `Server/integrations/pingid`

1.  Execute `mvn package`. Ensure the process finishes successfully

1.  `cd` to `target`. Resulting file is `oxauth-pingid-1.0.jar`
