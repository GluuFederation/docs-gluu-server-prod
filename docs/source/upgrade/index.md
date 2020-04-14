# Upgrade to the latest Gluu Server

## Overview
Find your existing version below for instructions to upgrade to the latest version of Gluu. 

!!! Note
    The Gluu Server **cannot** be upgraded with a simple `apt-get upgrade`. In lieu of using our upgrade scripts documented below, you can perform a fresh install of the latest version and export/import your existing data. 

### Prerequisites

- Before upgrading, make sure to [back up](../operation/backup.md) the Gluu container or LDAP LDIF. 
- Upgrades should always be thoroughly scoped and tested on a development environment *first*.

### Additional notes

- Scripts and directories outside the Chroot will still reflect the version from which you upgraded. For example, if you started with version 3.1.3, the directory will still be gluu-server-3.1.3, even after upgrading to 3.1.8.

## Upgrade from 3.1.x to 3.1.8

!!! Note 
    The upgrade script requires the `/install/community-edition-setup/setup.properties.last` to be available. Information in this file is used in the upgrade process.

To perform an in-place upgrade to Gluu Server 3.1.8, download and run our in-place upgrade script, following these instructions:

1. Log in to your server with `service gluu-server-3.1.x login`

1. Download the upgrade script with `https://repo.gluu.org/upd/3-1-8-upg.sh`

1. Run the script with `sh 3-1-8-upg.sh`

1. When the script has finished, restart your server:

```
logout
service gluu-server-3.1.x restart
```

## Upgrade from 3.0.x to 3.1.8


Upgrading generally involves the following steps:

- Install the new version

- Export the data from your current version

- Stop the current Gluu Server

- Start the new version of Gluu Server

- Import data into the new server

Gluu provides the necessary [scripts](https://github.com/GluuFederation/community-edition-setup/tree/master/static/scripts) to import and export data in and out of the servers.

### Export the Data from the Current Installation

```
# service gluu-server-3.0.x login

# cd

# wget https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/export3031.py

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/version_3.1.8/ldif.py
```

Install the `python-pip` package.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge

# python export3031.py
```

!!! Note
    Choose OpenLDAP if your current LDAP Server is OpenLDAP when you are asked to choose a target LDAP Server.

The export script will generate a directory called `backup_3031` which will have all the data from the current installation. Check the log file generated in the directory for any errors.

### Install the Latest Version of the Gluu Server

Stop the current version of the Gluu Server.

```
# service gluu-server-3.0.x stop
```

Review the [installation docs](../installation-guide/install.md) to install the Gluu Server using the package manager. Once the package manager has installed version `3.1.8`, execute the following commands:

```
# cp -r /opt/gluu-server-3.0.x/root/backup_3031/ /opt/gluu-server-3.1.8/root/

# service gluu-server-3.1.8 start

# service gluu-server-3.1.8 login

# cd

# cp backup_3031/setup.properties /install/community-edition-setup/

# cd /install/community-edition-setup/

# ./setup.py
```

Enter the required information to complete the installation.

### Import your Old Data

Navigate to where you have the `backup_3031` folder (if the above commands were followed, it is in `/root/`) and execute the following commands to get the necessary scripts:

```
# cd

# wget -c https://raw.githubusercontent.com/GluuFederation/community-edition-setup/master/static/scripts/import3031.py

# wget https://raw.githubusercontent.com/GluuFederation/cluster-mgr/master/testing/ldifschema_utils.py
```

Install the `python-pip` package using your package manager.

```
# curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"

# python get-pip.py
```

Install the `json-merge` Python package and run the import script.

```
# pip install jsonmerge
```

Install the python-ldap package. 
For Debian and Ubuntu:

```
# apt-get update

# apt-get install python-ldap
```

For CentOS and RHEL:

```
# yum install python-ldap
```

Now run the import script:

```
# python import3031.py backup_3031
```

!!! Note
    The import script will enable the default admin user and will disable all custom authentication scripts. You should manually enable them if any were configured.
    
    After completion of import, stop/start gluu-server container one final time.

Any errors or warnings will be displayed in the terminal and can be reviewed in the import log. Now you should be able to log into the oxTrust web UI using the old admin credentials and you should see all previous data in place. 

