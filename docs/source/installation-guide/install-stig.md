# DISA STIG Distribution Installation 

## Overview
A DISA STIG compliant single-node Gluu Server Linux package is available only or RHEL 8. This deployment does not use a chroot container. Follow the instructions below:

1. [Install the Linux package](#install-the-package)
2. [Start the Server and log in to the container](#start-the-server-and-log-in)
3. [Run the setup script](#run-the-setup-script)
4. [Sign in via browser](#sign-in-via-browser)
5. [Disable Gluu repositories](#disable-gluu-repositories)

!!! Attention
    To upgrade an existing Gluu Server installation, follow the [upgrade guide](../upgrade/index.md).

## Prerequisites

- Make sure the target server or VM meets **all minimum requirements** specified in the [VM Preparation Guide](../installation-guide/index.md).   

- SELinux must be set to permissive in /etc/selinux/config

## Instructions

### Install the package

The Gluu Server will create its file system under `/root/` and will be installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) remain the same as the host.

Run the following commands:

```
wget https://repo.gluu.org/rhel/Gluu-rhel8.repo -O /etc/yum.repos.d/Gluu.repo
```

```
wget https://repo.gluu.org/rhel/RPM-GPG-KEY-GLUU -O /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU
```

```
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-GLUU
```

```
yum clean all
```

```
yum install gluu-server
```

After installation, the `gluu-server` package needs to be excluded from automatic updates with the following command.

```
yum versionlock gluu-server
```

### Start the server and log in

This distribution of the Gluu Server does not use a chroot container and must be started using a different process from other distributions.

Run the following commands: 

TBD

### Run the setup script

Configuration is completed by running the setup script. This generates certificates, salt values, and renders configuration files. Run the script with the following commands:

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

Edit `/etc/yum.repos.d/Gluu.repo` so that the `enabled=1` clause is changed to `enabled=0`        

!!! Note
    The Gluu Server does **not** support package updates/upgrades via Linux package management (i.e. using commands like `# yum update` or `# apt-get update`). For upgrade instructions, see the [upgrade docs](../upgrade/index.md).

## Backups
Sometimes things go wrong! It can be difficult to troubleshoot issues if the steps to reproduce the issue are not clearly documented. This is why we **always** recommend creating [backups of your Gluu Server](../operation/backup.md). 

## Uninstallation

Run the following commands:

```
/sbin/gluu-serverd disable
```

```
/sbin/gluu-serverd stop
```

```
yum remove gluu-server 
```

```
rm -rf /opt/gluu-server.save
```

!!! Note
    `apt-get purge gluu-server` or `apt-get remove --purge gluu-server` can also be used to uninstall and remove all the folders and services of the Gluu Server. Make sure to back up ALL directories of `/opt` into other direction (tmp or root directory itself) before running the purge command.

## Support
Please review the [Gluu support portal](https://support.gluu.org). There are many existing tickets about troubleshooting installation issues. If there is no similar existing public issue, register for an account and open a new ticket. 

If your organization needs guaranteed responses, SLAs, and priority access to the Gluu support and development team, consider purchasing one of our [VIP support contracts](https://gluu.org/pricing).  
