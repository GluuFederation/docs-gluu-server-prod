# Gluu Server Patches

## oxTrust Unauthorized Access Patch
### May 13, 2019

### Affected versions
All versions of the Gluu Server

### Issue Description

The following page in oxTrust is not properly protected:

```
../identity/authentication/finishlogin/
```

Navigating to this URL directly obtains an unauthorized session for a random user.

Normally, oxAuth sends a request with an authorization code to oxTrust at `../identity/authentication/getauthcode`. oxTrust then uses that code to obtain the user's `id_token` and personal claims, then redirects to `../finishlogin`.

Navigating directly to `../finishlogin` without meaningful session context caused `entryManager` to build an `objectClass=gluuPerson` filter without `uid=user_name`. This returned all users and created an unauthorized session for the first user on that list.

### Fix Description

The patch below adds two lines to the `finishlogin` xhtml file to catch null `user-id` parameters. Once applied, unauthenticated attempts to access this URL will be blocked.

!!! Note
    As the administrative portal for your authentication service, we always recommend **blocking public access to oxTrust**. Learn how [in the docs](https://gluu.org/docs/ce/operation/security/#securing-oxtrust).
    
### Steps to apply fix

The steps below apply to **all** affected Gluu Server versions.

!!! Note
    A 5-minute maintenance window is needed to apply the fix. Make sure to test and confirm in a non-production environment first. If Gluu helps manage your server(s), please [open a ticket](https://support.gluu.org) to schedule a maintenance window.

- [Back up your Gluu Server](https://gluu.org/docs/ce/operation/backup/)  -- either a VM snapshot or a tarball of the Gluu Server container.
 
- Log into your Gluu Server container:

    - For Centos 6.x, Red Hat 6.x, Ubuntu 14/16, and Debian 8:
    
    ```
    # service gluu-server-3.1.3 login
    ```
    
    - For Centos 7.x, Red Hat 7.x and Debian 9:
    
    ```
    # /sbin/gluu-serverd-3.1.3 login
    ```

- Download the patch script:

    ```
    wget https://repo.gluu.org/upd/security_patch_identity-2.py
    ```
    
- Run the command:

    ```
    chmod +x security_patch_identity-2.py
    ```
    
- Run the command:

    ```
    python security_patch_identity-2.py
    ```
    
- Open an incognito window in your browser and attempt to access the affected page: https://{hostname}/identity/authentication/finishlogin . If it results in a blank page, the patch was successful.

## OPENDJ-2969 
### February 15, 2019

### Affected versions
- All Gluu versions (2.x - 3.x), any installation using Gluu OpenDJ

### Description

OpenDJ 3.0 is affected by bug preventing replication server component from successfully starting if its DB's certain changelog (binary) files are of size of multiply of 256. More info on the [OpenDJ jira](https://bugster.forgerock.org/jira/browse/OPENDJ-2969).

Upgrading to a fixed 3.5 package version isn't yet possible at the time of writting due to licensing. The only possible workaround is to rename/remove the `changeDBlog/` dir before starting OpenDJ's JVM. Thus a workaround was developed by the Gluu Team in attempt to mitigate its impact, which automates the process and does it transparenlty to an user.

### Steps to Fix

#### Patching steps

Follow next steps to apply the patch:

1. All work should be done inside Gluu-Server container. 

1. Put patching script at `/usr/local/sbin/check_changelog.sh` (see source code of it below)   

1. Edit `/opt/opendj/bin/start-ds` script by adding section calling the patch script to the beginning of it (see diff below for clues)    
1. Set proper permissions for the patch script: `# chmod +x /usr/local/sbin/check_changelog.sh; chown ldap:ldap /usr/local/sbin/check_changelog.sh`

When service is started/restarted, if unsafe condition is detected, script will rename the current `changeDBlog/` dir to `changeDBlog.TIMESTAMP/` and then will allow `start-ds` script to proceed with starting OpenDJ, expecting it to re-create the directory.

#### Patch script's source

```
#!/bin/bash

base=`basename $PWD`
TODAY=`date +%Y%m%d_%H%M`
changeDBlog="/opt/opendj/changelogDb"

date=`date "+%y%m%d-%H%M%S"`

files=`find $changeDBlog -name "head.log" -print` 
for file in $files; do
	size=`ls -l $file | awk '{print $5}'`
	check1=`expr ${size} / 256`
	check2=`expr 256 \* ${check1}`
	if [ "${size}" = "${check2}" -a "${check1}" != "0" ]; then
		echo "ALERT! $file has size as multiple of 256..."
		echo "Renaming $changeDBlog as ${changeDBlog}.$TODAY"
		mv $changeDBlog ${changeDBlog}.$TODAY
		break
	fi
done
echo "Moving towards normal opendj start now..."
```

#### Diff between the modified and original `start-ds` files

```
# diff -c /opt/opendj/bin/start-ds-new /opt/opendj/bin/start-ds
*** /opt/opendj/bin/start-ds-new	2018-02-12 12:17:38.534685038 -0500
--- /opt/opendj/bin/start-ds	2016-04-20 07:16:29.000000000 -0400
***************
*** 19,33 ****
  # Capture the current working directory so that we can change to it later.
  # Then capture the location of this script and the Directory Server instance
  # root so that we can use them to create appropriate paths.
- 
- ### This is custom procedure implemented by Ganesh/Zico/Alex
- test_changelog () {
-   /usr/local/sbin/check_changelog.sh
- }
- 
- test_changelog
- ####################################
- 
  WORKING_DIR=`pwd`
  
  cd "`dirname "${0}"`"
--- 19,24 ----

```
#### Double checking

To confirm, compare the amount of entries between all replicated trees of nodes after completing the above steps. Even if there is no error in replication, there might still be a difference between node A and node B. In the event this happens, disable/re-enable the whole replication operation. 

## Publicly viewable oxTrust pages

### January 30, 2019

### Affected Versions 

Gluu Server 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4 

### Description

We discovered the following two pages in oxTrust are not properly protected: 

 - `../identity/status/appliance`
 - `../identity/configuration/registration`

The steps to fix below apply to **all** affected Gluu Server versions. 

### Steps to fix

!!! Note 
    You will need a 5 minute maintenance window for your /identity endpoint to apply the fix.
    
!!! Warning
    We always recommend testing on a non-production environment first.
    

1. Backup your Gluu Server -- either a VM snapshot or a tarball of the gluu-server container. [Read the docs](https://gluu.org/docs/ce/3.1.4/operation/backup/)        

1. Log into your Gluu Server container.              
     For Centos 6.x, Red Hat 6.x, Ubuntu 14/16, and Debian 8:
         `# service gluu-server-3.1.x login`

     For Centos 7.x, Red Hat 7.x and Debian 9:
         `# /sbin/gluu-serverd-3.1.x login` 

1. Download the patch script:             
         `wget https://repo.gluu.org/upd/security_patch_identity.py`

1. Run the command:               
         `chmod +x security_patch_identity.py`

1. Run the command:             
         `python security_patch_identity.py` 

1. Open an incognito window in your browser and attempt to access the two affected pages. They should now require authentication.    

## Code White Patch
### August 21, 2018

### Affected versions
- All currently supported Gluu versions (2.4.4, 3.x)

### Description
We have discovered a critical vulnerability in the Jboss Richfaces library. All versions of the component Richfaces (including the latest v4.5.17.Final) are affected by the vulnerability, which is an EL injection leading to Remote Code Execution. The CVE assignment to MITRE for it is CVE-2018-12532. The CVE can be seen on the [MITRE](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-12532) site as well as [NIST](https://nvd.nist.gov/vuln/detail/CVE-2018-12532). 

This vulnerability is basically a bypass of CVE-2015-0279. CVE-2015-0279 hardens the `org.richfaces.resource.MediaOutputResource` class by blocking expressions containing [parantheses](https://github.com/richfaces/richfaces/blob/4.5.17.Final/components/a4j/src/main/java/org/richfaces/resource/MediaOutputResource.java#L67-L69). The new vulnerability lies in the fact that EL additionally made use of custom variable mappers internally to resolve the variable name in case it's not found in the main expression, but variable mappers themselves can contain EL code just the same. Variable mappers are implemented through the `varMapper` field of `org.apache.el.MethodExpressionImpl` in Tomcat EL API, which Jetty is also using.

The general flow looks like this: the application deserializes the "do" parameter (the 'source') at `org.richfaces.resource.ResourceUtils#decodeBytesData`, passes the object through some other calls, and eventually calls a `MethodExpression.invoke` on a field in the object (the 'sink') at `org.richfaces.resource.MediaOutputResource#encode`. There is however a protection in place restricting deserialization to [certain classes](https://github.com/richfaces/richfaces/blob/4.5.17.Final/core/src/main/java/org/richfaces/util/LookAheadObjectInputStream.java#L133), but as the `VariableMapperImpl` class is also whitelisted there, we then have full control over the `varMapper` field in the `MethodExpressionImpl` instance, which essentially means arbitrary EL injection.

As oxTrust/Identity utilizes Jboss Richfaces, this allows an unauthorized user to perform unauthorized Remote Code Execution. Knowing this, we have created a richfaces updater script that removes the affected class from the `identity.war` file, negating the impact of this vulnerability. That being said, we strongly recommend that **oxTrust should not be internet facing.**

### Steps to fix using a script for 2.4.4 and newer

!!! Note
    We **strongly** recommend [backing up your environment](../operation/backup.md) before proceeding. 

!!! Note
    The script will suggest you to restart container after the patching is done. This step can be omitted if steps below were followed to the letter, as stopping and starting particular service ("tomcat" for 2.x and "identity" for 3.x) is enough to apply the changes.
    
1. Login to the Gluu Server chroot
1. Download the security patch `richfaces_updater.sh` from [https://repo.gluu.org/upd/](https://repo.gluu.org/upd/)
1. You can verify the integrity of the file by running `sha256sum richfaces_updater.sh` and verifying it against the sha256 checksum `richfaces_updater.sh.sha256` in [https://repo.gluu.org/upd/](https://repo.gluu.org/upd/)
1. Grant `richfaces_updater.sh` executable privileges
1. Stop "tomcat"/"identity" services:

        Gluu Server 3.x: [root@localhost ~]# service identity stop
        Gluu Server 2.x: [root@localhost ~]# service tomcat stop

1. Run `richfaces_updater.sh`

        [root@example ~]# service gluu-server-x.x.x Login
        Welcome to the Gluu Server!
        [root@localhost ~]# chmod +x richfaces_updater.sh 
        [root@localhost ~]# ./richfaces_updater.sh 
        Creating directory /opt/upd
        Verifying archive integrity...  100%   MD5 checksums are OK. All good.
        Uncompressing Gluu Richfaces Updater  100%  

        Backing up /opt/gluu/jetty/identity/webapps/identity.war to /opt/upd/Thu_Aug_16_20:21:50_2018
        Updating /opt/gluu/jetty/identity/webapps/identity.war
        Deleting old richfaces from identity.war
        deleting: WEB-INF/lib/richfaces-4.5.17.Final.jar
        deleting: WEB-INF/lib/richfaces-core-4.5.17.Final.jar
        deleting: WEB-INF/lib/richfaces-a4j-4.5.17.Final.jar
        Adding latest richfaces to identity.war
        adding: WEB-INF/lib/richfaces-4.5.17-gluu.Final.jar (deflated 20%)
        adding: WEB-INF/lib/richfaces-a4j-4.5.17-gluu.Final.jar (deflated 10%)
        adding: WEB-INF/lib/richfaces-core-4.5.17-gluu.Final.jar (deflated 9%)

1. Start "tomcat"/"identity" services:

        Gluu Server 3.x: [root@localhost ~]# service identity start
        Gluu Server 2.x: [root@localhost ~]# service tomcat start
        
### Patching 2.4.3 and below:

- Download jar files

```
wget https://ox.gluu.org/maven/com/sun/faces/jsf-api/2.1.28/jsf-api-2.1.28.jar
wget https://ox.gluu.org/maven/com/sun/faces/jsf-impl/2.1.28-jbossorg-1/jsf-impl-2.1.28-jbossorg-1.jar
wget https://ox.gluu.org/maven/org/jboss/spec/javax/faces/jboss-jsf-api_2.1_spec/2.1.28.Final/jboss-jsf-api_2.1_spec-2.1.28.Final.jar
wget https://ox.gluu.org/maven/org/richfaces/richfaces/4.5.17-gluu.Final/richfaces-4.5.17-gluu.Final.jar
wget https://ox.gluu.org/maven/org/richfaces/richfaces-a4j/4.5.17-gluu.Final/richfaces-a4j-4.5.17-gluu.Final.jar
wget https://ox.gluu.org/maven/org/richfaces/richfaces-core/4.5.17-gluu.Final/richfaces-core-4.5.17-gluu.Final.jar
```

- Make backup

```
mkdir -p /opt/upd/backup
cp -r /opt/tomcat/webapps/identity/ /opt/upd/backup
cp -r /opt/tomcat/webapps/identity.war /opt/upd/backup
```

- Stop tomcat

```
/opt/tomcat/bin/shutdown.sh
```

- Delete current files

```
rm /opt/tomcat/webapps/identity.war
rm /opt/tomcat/webapps/identity/WEB-INF/lib/jsf-api-2.1.0.jar
rm /opt/tomcat/webapps/identity/WEB-INF/lib/jsf-impl-2.1.7.jar
rm /opt/tomcat/webapps/identity/WEB-INF/lib/jboss-jsf-api_2.1_spec-2.0.9.Final.jar
rm /opt/tomcat/webapps/identity/WEB-INF/lib/richfaces*
 
```

- Copy jar files

```
cp jsf-api-2.1.28.jar /opt/tomcat/webapps/identity/WEB-INF/lib/
cp jsf-impl-2.1.28-jbossorg-1.jar /opt/tomcat/webapps/identity/WEB-INF/lib/
cp jboss-jsf-api_2.1_spec-2.1.28.Final.jar /opt/tomcat/webapps/identity/WEB-INF/lib/
cp richfaces-core-4.5.17-gluu.Final.jar /opt/tomcat/webapps/identity/WEB-INF/lib/
cp richfaces-a4j-4.5.17-gluu.Final.jar  /opt/tomcat/webapps/identity/WEB-INF/lib/
cp richfaces-4.5.17-gluu.Final.jar  /opt/tomcat/webapps/identity/WEB-INF/lib/
```
- Fix customScriptListForm.xhtml and trustRelationshipForm.xhtml

Edit this file `/opt/tomcat/webapps/identity/WEB-INF/incl/script/customScriptListForm.xhtml` and add followings after
`.removeConfig` directive:

```
    .rf-tab-hdr-tabline-vis.rf-tab-hdr-tabline-top {
            height: 9% !important;
            background: none !important;
            background-color: transparent !important;
            border: none !important;
            overflow-x: auto  !important;            
   }
```

Edit this file `/opt/tomcat/webapps/identity/WEB-INF/incl/trustmanager/trustRelationshipForm.xhtml` and add followings between </:outputStylesheet>...</h:outputStylesheet> tag:

```
    .rf-tab-hdr-tabline-vis.rf-tab-hdr-tabline-top {
            height: 9% !important;
            background: none !important;
            background-color: transparent !important;
            border: none !important;
            overflow-x: auto  !important;            
   }
```

- create war file

```
cd /opt/tomcat/webapps/identity/
jar -cf ../identity.war *
```

- exit container, stop and start gluu server

### Explanation of fix

By following the above instructions, you will replace the old richfaces library in `identity.war` with a custom fixed version for the Gluu Server. The fix is accomplished by removing the affected (and unused) classes from the vulnerable library, negating the impact of the vulnerabiity. In 2.4.3 and below, the patched library needs to update jsf for functionality.

A backup of your `identity.war`, before changes, is in the `/opt/upd/backup_$TIME_STAMP` directory in case you need it.\

## Patching image/files uploading for Gluu 3.1.3
 
 There is a [known issue](https://github.com/GluuFederation/oxTrust/issues/1007) in Gluu 3.1.3 that affects file upload feature like **Person Import**, **Organization logo upload**.
 
 Below are steps to fix that issue by patching the oxtrust war file.
 
 1. Login into Gluu container
 1. Save a copy of you actual `/opt/gluu/jetty/identity/webapps/identity.war`
 1. Move to home directory: `#cd` 
 1. Copy identity.war in the current directory: `#cp /opt/gluu/jetty/identity/webapps/identity.war .`
 1. Run : ``` #zip -d identity.war WEB-INF/lib/jsf-api-2.2.17.jar```
 1. Run : ``` #zip -d identity.war WEB-INF/lib/jsf-impl-2.2.17.jar```
 1. Make directory: `#mkdir -p WEB-INF/lib`
 1. Change directory: `#cd WEB-INF/lib`
 1. Run: `#wget http://repository.jboss.org/nexus/content/groups/public-jboss/com/sun/faces/jsf-api/2.2.16/jsf-api-2.2.16.jar`
 1. Run: `#wget http://repository.jboss.org/nexus/content/groups/public-jboss/com/sun/faces/jsf-impl/2.2.16/jsf-impl-2.2.16.jar`
 1. Run: `#jar -uf identity.war WEB-INF/lib/jsf-api-2.2.16.jar`
 1. Run: `#jar -uf identity.war WEB-INF/lib/jsf-impl-2.2.16.jar`
 1. Move back the war file: `#cp identity.war /opt/gluu/jetty/identity/webapps/identity.war`
 1. Restart identity service: `#service identity restart`