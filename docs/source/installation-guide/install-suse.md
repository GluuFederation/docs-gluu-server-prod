
!!! Attention
    All Linux assets, packages, and binaries require a support contract for access.
    Contact sales@gluu.org for more information. For free up-to-date binaries,
    check out the latest releases at [The Linux Foundation Janssen Project](https://docs.jans.io),
    the new upstream open source project.

# SUSE Installation 

## Overview
Single-node Gluu Server Linux package are available for SUSE Linux Enterprise Server 15. Follow the instructions below: 

1. [Install the Linux package](#install-the-package)
2. [Start the Server and log in to the container](#start-the-server-and-log-in)
3. [Run the setup script](#run-the-setup-script)
4. [Sign in via browser](#sign-in-via-browser)
5. [Disable Gluu repositories](#disable-gluu-repositories)

!!! Attention
    To upgrade an existing Gluu Server installation, follow the [upgrade guide](../upgrade/index.md).

## Prerequisites

- Make sure the target server or VM meets **all minimum requirements** specified in the [VM Preparation Guide](../installation-guide/index.md).   

- SELinux must be set to permissive in `/etc/selinux/config`
  
## Instructions

### Install the package

The Gluu Server will be installed under `/opt`. File size and [minimum requirements](../installation-guide/index.md) remain the same as the host.

For **SUSE Linux Enterprise Server 15**, run the following commands to install:

```
wget --user="your-username" --password="your-password" https://repo.gluu.org/suse/RPM-GPG-KEY-GLUU -O RPM-GPG-KEY-GLUU
```

```
rpm --import RPM-GPG-KEY-GLUU
```

```
zypper addrepo  https://repo.gluu.org/suse/15 Gluu-repo
```

```
zypper refresh
```

```
zypper install gluu-server-nochroot
```

After installation, the `gluu-server-nochroot` package needs to be excluded from automatic updates with the following command.

```
zypper addlock gluu-server-nochroot
```

### Start the server and log in

The Gluu Server must be started to proceed. 

Run the following commands: 

```
gluu-serverd start
```

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

```
zypper mr -d Gluu-repo
```

!!! Note
    The Gluu Server does **not** support package updates/upgrades via Linux package management (i.e. using commands like `# yum update` or `# apt-get update`). For upgrade instructions, see the [upgrade docs](../upgrade/index.md).

## Backups
Sometimes things go wrong! It can be difficult to troubleshoot issues if the steps to reproduce the issue are not clearly documented. This is why we **always** recommend creating [backups of your Gluu Server](../operation/backup.md). 

## Uninstallation

Run the following commands:

```
gluu-serverd stop
```

```
zypper remove gluu-server-nochroot
```

```
rm -rf /opt/dist /opt/gluu /install /ect/certs/casa.pub
```

## Support
Please review the [Gluu support portal](https://support.gluu.org). There are many existing tickets about troubleshooting installation issues. If there is no similar existing public issue, register for an account and open a new ticket. 

If your organization needs guaranteed responses, SLAs, and priority access to the Gluu support and development team, consider purchasing one of our [VIP support contracts](https://gluu.org/pricing).  
