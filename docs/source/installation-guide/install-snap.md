# Snap Installation

## Overview 

The Gluu Server now supports installation via [snap packages](https://snapcraft.io/). Using snaps, the installation process is simplified by bundling the Gluu Server and its dependencies into a single package that can be installed across Linux distributions.

## Prerequisites

Set up a server or VM with the following **minimum** requirements:

|CPU Unit  |    RAM     |   Disk Space      | Processor Type |
|----------|------------|-------------------|----------------|
|   2-4    |    8GB     |   60GB            |  64 Bit        |

## Installation

### Ubuntu and Debian

=== "Snapcraft Repo"

    ```
    apt install -y snapd python3 python3-pip
    ```
    
    ```
    export PATH="/snap/bin:$PATH"
    ```
    
    ```
    snap install core
    ```
    
    ```
    snap install gluu-server
    ```
    
    ```
    gluu-server.setup
    ```

=== "Gluu Repo"

    ```
    apt install -y snapd python3 python3-pip
    ```
    
    ```
    export PATH="/snap/bin:$PATH"
    ```
    
    ```
    wget https://repo.gluu.org/snaps/gluu-server_4.2.1_amd64.snap
    ```
    
    ```
    snap install core
    ```
    
    ```
    snap install --dangerous gluu-server_4.2.1_amd64.snap
    ```
    
    ```
    gluu-server.setup
    ```

### Centos and RHEL

=== "Snapcraft Repo"

    ```
    sudo yum install -y epel-release
    ```
    
    ```
    sudo yum install -y snapd python3 python3-pip
    ```
    
    ```
    sudo ln -s /var/lib/snapd/snap /snap
    ```
    
    ```
    sudo systemctl enable --now snapd.socket
    ```
    
    ```
    export PATH="/var/lib/snapd/snap/bin:/snap/bin:$PATH"
    ```
    
    ```
    snap install core
    ```
    
    ```
    snap install gluu-server
    ```
    
    ```
    gluu-server.setup
    ```

=== "Gluu Repo"

    ```
    sudo yum install -y epel-release
    ```
    
    ```
    sudo yum install -y snapd wget python3 python3-pip
    ```
    
    ```
    sudo ln -s /var/lib/snapd/snap /snap
    ```
    
    ```
    sudo systemctl enable --now snapd.socket
    ```
    
    ```
    export PATH="/var/lib/snapd/snap/bin:/snap/bin:$PATH"
    ```
    
    ```
    snap install core
    ```
    
    ```
    wget https://repo.gluu.org/snaps/gluu-server_4.2.1_amd64.snap
    ```
    
    ```
    snap install --dangerous gluu-server_4.2.1_amd64.snap
    ```
    
    ```
    gluu-server.setup
    ```

### Uninstall process

```
$ snap remove gluu-server
```
