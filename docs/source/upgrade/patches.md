# Gluu Server Patches

## Patching the Log4j vulnerability in Gluu Server

!!! Important
    This patch is already applied in versions 4.3.1 and above.
    
#### Gluu Server versions covered: Gluu v4, v3 ( from 3.1.5 to 3.1.8 ), Enterprise Edition, Cloud Native and Snapcraft.
#### Security Vulnerabilities: CVE-2021-44832, CVE-2021-45105, CVE-2021-45046 and CVE-2021-44228 
#### Log4j library versions affected: 2.1.6 and earlier 
&nbsp;


### Overview:
On December 17th, Apache announced critical vulnerabilities that would allow a malicious user access to a remote server to execute code. (Details can be found [here](https://logging.apache.org/log4j/2.x/index.html)) Apache has released an update to their Log4j (version 2.17.0) to eliminate this vulnerability, which requires updating the Log4j library in all installations.


There are three methods to patch log4j in Gluu Server: 
 - Using automated script 
 - Using manual method 
 - Update using latest war/image. 

The third option is best suited for Cloud Native Gluu Servers, like K8s and/or Docker. Snap update follows a manual process, and is detailed in a separate section below.
&nbsp;

&nbsp;

### Before patching server....

**Make sure to backup your Gluu Server!** Snapshot backup is the recommended method. 

Also, here is the direct link to Gluu Support, in case of issues: [Gluu Support - New Support Ticket Form](https://support.gluu.org/tickets/add/)
&nbsp;

&nbsp;

### Method #1: Using automated script

We developed and published a script to automate the entire update process. Here are the steps to run this script to update your Gluu Server: 

 - Download script: `wget -c https://repo.gluu.org/upd/update_log4j.run`
 - Copy script inside Gluu Server container. 
 - Make it executable: `chmod +x update_log4j.run`
 - Run script from root console: `./update_log4j.run`
 - Follow the rest of the post-op procedure according to the on-screen instructions. 
&nbsp;

&nbsp;

### Method #2: Using manual method
 
Below are the steps detailing how to manually patch each component (oxAuth, oxTrust/identity, IDP, Casa and Shibboleth, in this case ) within Gluu Server. 

##### oxAuth

 - Backup 'oxauth.war' from `/opt/gluu/jetty/oxauth/webapps/`
 - Create a temporary directory inside: `mkdir war`
 - Un-war `oxauth.war` in that directory called `war`: `unzip oxauth.war -d war`
 - Make a directory named `old`: `mkdir old`
 - Move all `log4j-*` into `old` directory: `mv -f ./war/WEB-INF/lib/log4j-*-2*.jar ./old` [ **Important!** Check the number of lib4j libraries it copied. **You need to  download and upgrade ONLY these artifacts.** DO NOT DOWNLOAD those files which are not required for your installation! ]
 - Go to library directory now: `cd ./war/WEB-INF/lib`
 - Download these jars in current `lib` directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar` 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-jul/2.17.1/log4j-jul-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar`
 - It's time to re-pack war: 
   - `cd  ../../../`
   - `cd ./war`
     - For 3.1.5 or 3.1.6 system: `/opt/jdk1.8.0_181/bin/jar -cvf oxauth.war *`
     - For 4.x or > 3.1.7 system: `/opt/amazon-corretto-11.0.8.10.1-linux-x64/bin/jar -cvf oxauth.war *` or `/opt/amazon-corretto-8.222.10.1-linux-x64/bin/jar -cvf oxauth.war *`
 - Stop `oxauth` service
 - Check if there are any directories like these inside: `/opt/jetty-x.x/temp/jetty-localhost-808x-oxauth_war-_oxauth-any-.....` . If present, remove them all. 
 - Copy new war into `/opt/gluu/jetty/oxauth/webapps/` directory
 - Start oxauth service


##### oxTrust/ identity

 - Backup 'identity.war' from `/opt/gluu/jetty/identity/webapps/`
 - Create a temporary directory inside: `mkdir war`
 - Un-war `identity.war` in that directory called `war`: `unzip identity.war -d war`
 - Make a directory named `old`: `mkdir old`
 - Move all `log4j-*` into `old` directory: `mv -f ./war/WEB-INF/lib/log4j-*-2*.jar ./old` [ **Important!** Check the number of lib4j libraries it copied. **You need to  download and upgrade ONLY these artifacts.** DO NOT DOWNLOAD those files which are not required for your installation! ]
 - Go to library directory now: `cd ./war/WEB-INF/lib`
 - Download these jars in current `lib` directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar` 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-jul/2.17.1/log4j-jul-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar`
 - It's time to re-pack war: 
   - `cd  ../../../`
   - `cd ./war`
     - For 3.1.5 or 3.1.6 system: `/opt/jdk1.8.0_181/bin/jar -cvf identity.war *`
     - For 4.x or > 3.1.7 system: `/opt/amazon-corretto-11.0.8.10.1-linux-x64/bin/jar -cvf identity.war *` or `/opt/amazon-corretto-8.222.10.1-linux-x64/bin/jar -cvf identity.war *`
 - Stop `identity` service
 - Check if there are any directories like these inside: `/opt/jetty-x.x/temp/jetty-localhost-808x-identity_war-_.....`. If present, remove them all.
 - Copy new war into `/opt/gluu/jetty/identity/webapps/` directory
 - Start identity service


##### idp

 - Backup 'idp.war' from `/opt/gluu/jetty/idp/webapps/`
 - Create a temporary directory inside: `mkdir war`
 - Un-war `oxauth.war` in that directory called `war`: `unzip idp.war -d war`
 - Make a directory named `old`: `mkdir old`
 - Move all `log4j-*` into `old` directory: `mv -f ./war/WEB-INF/lib/log4j-*-2*.jar ./old`[ **Important!** Check the number of lib4j libraries it copied. **You need to  download and upgrade ONLY these artifacts.** DO NOT DOWNLOAD those files which are not required for your installation! ]
 - Go to library directory now: `cd ./war/WEB-INF/lib`
 - Download these jars in current `lib` directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
 - It's time to re-pack war: 
   - `cd  ../../../`
   - `cd ./war`
     - For 3.1.5 or 3.1.6 system: `/opt/jdkx.x.x.x/bin/jar -cvf idp.war *`
     - For 4.x or > 3.1.7 system: `/opt/amazon-corretto-11.0.8.10.1-linux-x64/bin/jar -cvf idp.war *` or `/opt/amazon-corretto-8.222.10.1-linux-x64/bin/jar -cvf idp.war *`
 - Stop `idp` service
 - Check if there are any directories like these inside: `/opt/jetty-x.x/temp/jetty-localhost-808x-oxauth_war-_.....`. If present, remove them all. 
 - Copy new war into `/opt/gluu/jetty/idp/webapps/` directory
 - Start `idp` service

##### Casa

 - Login to chroot (eg. `service gluu-server-3.1.5 login`, `gluu-serverd login`, etc.)
 - Create a temporary directory: `cd /root && mkdir casa`
 - Extract casa war contents: `jar -xf /opt/gluu/jetty/casa/webapps/casa.war`
 - Enter the libs directory: `cd WEB-INF/lib` - Remove old log4j jars: `rm log4*`
 - Download new log4j files
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar` 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar`
 - Run `cd ../..`
 - Repack war: `jar -cf casa.war *` (for 4.x systems the `jar` executable might not be in the PATH, you can locate it under `/opt/amazon-corretto.../bin` directory)
 - Backup your current war: `cp /opt/gluu/jetty/casa/webapps/casa.war casa.war.bak`
 - Stop casa service
 - Copy patched war: `cp casa.war /opt/gluu/jetty/casa/webapps`
 - Start casa

##### Shibboleth ( optional ) 

 - Go to `/opt/shibboleth-idp/webapp/WEB-INF/lib/` location
 - Backup `log4j-1.2-api-2.x.x.jar`, `log4j-api-2.x.x.jar` and `log4j-core-2.x.x.jar`
 - Move these jar into separate directory
 - Download these jars in currnet ( /opt/shibboleth-idp/webapp/WEB-INF/lib/ ) directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
   - Change permission of these jars to `jetty:jetty`
 - Restart `identity` and `idp` services. 


&nbsp;

&nbsp;

### Method #3: Image Files for Cloud Native ( K8s ) patches with log4j 2.17

|Version   |    oxAuth |   oxTrust| oxShibboleth  | 	oxd server | casa      | scim      | fido2      |
|---------|----------|---------|---------------|--------------|---------|---------|---------|
|3.1.6       |  3.1.6_05 | 3.1.6_07 | 3.1.6_05          | N/A                 | N/A        |N/A          |N/A         |     
|4.0         |    4.0.1_11 | 4.0.1_10 | 4.0.1_08   	  | 4.0.0_04	  | N/A        |N/A          |N/A         | 
|4.1          |   4.1.3_11  |4.1.3_02 |4.1.3_02           | 4.1.3_02        | N/A         |N/A          |N/A         | 
|4.2         |   4.2.3_14 |4.2.3_09 | 4.2.3_14         | 4.2.3_04        | 4.2.3_08| 4.2.3_08| 4.2.3_06|
|4.3         |   4.3.1_01 | 4.3.1_01 |4.3.1_01           | 4.3.1_01         | 4.3.1_01 | 4.3.1_01 | 4.3.1_01 |

&nbsp;

&nbsp;

## Gluu Snap installation patching:

Gluu Snap installations need to follow the manual method of patching:

##### oxAuth

 - Backup 'oxauth.war' from `/var/snap/gluu-server/common/gluu/jetty/oxauth/webapps/`
 - Create a temporary directory inside: `mkdir war`
 - Un-war `oxauth.war` in that directory called `war`: `unzip oxauth.war -d war`
 - Make a directory named `old`: `mkdir old`
 - Move all `log4j-*` into `old` directory: `mv -f ./war/WEB-INF/lib/log4j-*-2*.jar ./old` [ **Important!** Check the number of lib4j libraries it copied. **You need to  download and upgrade ONLY these artifacts.** DO NOT DOWNLOAD those files which are not required for your installation! ]
 - Go to library directory now: `cd ./war/WEB-INF/lib`
 - Download these jars in current `lib` directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar` 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-jul/2.17.1/log4j-jul-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar`
 - It's time to re-pack war: 
   - `cd  ../../../`
   - `cd ./war`
   - `/snap/gluu-server/8/gluu-opt/jre/bin/jar -cvf oxauth.war *`
 - Stop `oxauth` service: `snap stop gluu-server.oxauth`
 - Copy new war into `/var/snap/gluu-server/common/gluu/jetty/oxauth/webapps/` directory
 - Start `oxauth` service: `snap start gluu-server.oxauth`

##### oxTrust/ identity

 - Backup 'identity.war' from `/var/snap/gluu-server/common/gluu/jetty/identity/webapps/`
 - Create a temporary directory inside: `mkdir war`
 - Un-war `identity.war` in that directory called `war`: `unzip identity.war -d war`
 - Make a directory named `old`: `mkdir old`
 - Move all `log4j-*` into `old` directory: `mv -f ./war/WEB-INF/lib/log4j-*-2*.jar ./old` [ **Important!** Check the number of lib4j libraries it copied. **You need to  download and upgrade ONLY these artifacts.** DO NOT DOWNLOAD those files which are not required for your installation! ]
 - Go to library directory now: `cd ./war/WEB-INF/lib`
 - Download these jars in current `lib` directory: 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-api/2.17.1/log4j-api-2.17.1.jar` 
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-1.2-api/2.17.1/log4j-1.2-api-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-core/2.17.1/log4j-core-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-jul/2.17.1/log4j-jul-2.17.1.jar`
      - `wget -c https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-slf4j-impl/2.17.1/log4j-slf4j-impl-2.17.1.jar`
 - It's time to re-pack war: 
   - `cd  ../../../`
   - `cd ./war`
   - `/snap/gluu-server/8/gluu-opt/jre/bin/jar -cvf identity.war *`
   - Stop `identity` service: `snap stop gluu-server.identity`
   - Copy new war into `/var/snap/gluu-server/common/gluu/jetty/identity/webapps/` directory
   - Start identity service: `snap start gluu-server.identity`
