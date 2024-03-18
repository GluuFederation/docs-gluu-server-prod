!!! Attention
    All Linux assets, packages, and binaries require a support contract for access.
    Contact sales@gluu.org for more information. For free up-to-date binaries,
    check out the latest releases at [The Linux Foundation Janssen Project](https://docs.jans.io),
    the new upstream open source project.

# Ubuntu Installation 
## Overview
Single-node Gluu Server Linux packages are available for Ubuntu 20.x, 22.x. Follow the instructions below: 

1. [Install the Linux package](#install-the-package)
2. [Start the Server and log in to the container](#start-the-server-and-log-in)
3. [Run the setup script](#run-the-setup-script)
4. [Sign in via browser](#sign-in-via-browser)
5. [Disable Gluu repositories](#disable-gluu-repositories)

!!! Attention
    To upgrade an existing Gluu Server installation, follow the [upgrade guide](../upgrade/index.md).

## Prerequisites
- Make sure the target server or VM meets **all minimum requirements** specified in the [VM Preparation Guide](../installation-guide/index.md). 
- **Ubuntu 20 or 22**: The Universe repository must be enabled.

## Instructions

### Install the package
The Gluu Server will create its file system under `/root/` and will be installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) remain the same as the host.

For **Ubuntu 22.x** run the following commands: 

```
echo "deb https://repo.gluu.org/ubuntu/ jammy main" > /etc/apt/sources.list.d/gluu-repo.list
```

```
curl --user "your-username:your-password" https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
```

```
Create a file named /etc/apt/auth.conf.d/99repo with content:

machine https://repo.gluu.org
login your-username
password your-password
```

```
apt update
```

```
apt install gluu-server
```

<!-- When the next version is released, this version should be changed to the most current 4.5.x package in repo.gluu.org, replacing the `_` between `gluu-server` and the version number with an `=` -->

For **Ubuntu 20.x** run the following commands: 

```
echo "deb https://repo.gluu.org/ubuntu/ focal main" > /etc/apt/sources.list.d/gluu-repo.list
```

```
curl --user "your-username:your-password" https://repo.gluu.org/ubuntu/gluu-apt.key | apt-key add -
```

```
Create a file named /etc/apt/auth.conf.d/99repo with content:

machine https://repo.gluu.org
login your-username
password your-password
```

```
apt update
```

```
apt install gluu-server
```
<!-- When the next version is released, this version should be changed to the most current 4.5.x package in repo.gluu.org, replacing the `_` between `gluu-server` and the version number with an `=` -->

After installation, the `gluu-server` package needs to be excluded from automatic updates with the following command.

```
apt-mark hold gluu-server
```

### Start the server and log in

The Gluu Server is a chroot container, which must be started to proceed. 

For **Ubuntu 20.x and 22.x** run the following commands: 

```
/sbin/gluu-serverd enable
```

```
/sbin/gluu-serverd start
```

```
/sbin/gluu-serverd login
```

### Run the setup script

Configuration is completed by running the setup script from inside the chroot container. This generates certificates, salt values, and renders configuration files. Run the script with the following commands:

```
cd /install/community-edition-setup
```   

```
./setup.py
```

See the [Setup Script Documentation](./setup_py.md#setup-prompt) for more detail on setup script options.

### Sign in via browser

Wait about 10 minutes in total for the server to restart and finalize its configuration. After that period, sign in via a web browser. The username will be `admin` and your password will be the `ldap_password` you provided during installation. 

!!! Note   
    If the Gluu Server login page does not appear, confirm that port 443 is open in the VM. If it is not open, open port 443 and try to reach the host in the browser again.   

### Disable Gluu Repositories

To prevent involuntary overwrites of the currently deployed instance (in case a newer version of the same package is found during regular OS updates), disable the previously added Gluu repositories after initial installation. 

Edit `/etc/apt/sources.list.d/gluu-repo.list` to comment out all Gluu-related repos.     

!!! Note
    The Gluu Server does **not** support package updates/upgrades via Linux package management (i.e. using commands like `# yum update` or `# apt-get update`). For upgrade instructions, see the [upgrade docs](../upgrade/index.md).

## Backups
Sometimes things go wrong! It can be difficult to troubleshoot issues if the steps to reproduce the issue are not clearly documented. This is why we **always** recommend creating [backups of your Gluu Server](../operation/backup.md). 

## Uninstallation

For **Ubuntu Server 20.x and Ubuntu Server 22.x**, run the following commands:

```
/sbin/gluu-serverd disable
```

```
/sbin/gluu-serverd stop
```

```
apt remove gluu-server
```

```
rm -fr /opt/gluu-server.save
```


!!! Note
    `apt-get purge gluu-server` or `apt-get remove --purge gluu-server` can also be used to uninstall and remove all the folders and services of the Gluu Server. Make sure to backup **ALL** directories of `/opt` into another directory (tmp or root directory itself) before running the purge command.

## Support
Please review the [Gluu support portal](https://support.gluu.org). There are many existing tickets about troubleshooting installation issues. If there is no similar existing public issue, register for an account and open a new ticket. 

If your organization needs guaranteed responses, SLAs, and priority access to the Gluu support and development team, consider purchasing one of our [VIP support contracts](https://gluu.org/pricing).  
