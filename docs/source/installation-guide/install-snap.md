# Snap Installation

## Overview 

The Gluu Server now supports installation via [snap packages](https://snapcraft.io/). Using snaps, the installation process is simplified by bundling the Gluu Server and its dependencies into a single package that can be installed across Linux distributions. While the installation is different in Snap than chroot-based distributions, all other operations, file locations, and other configuration are identical to a chroot-based deployment.

## Prerequisites

Set up a server or VM with the following **minimum** requirements:

|CPU Unit  |    RAM     |   Disk Space      | Processor Type |
|----------|------------|-------------------|----------------|
|   2-4    |    8GB     |   60GB            |  64 Bit        |

## Installation

Installation instructions for all distributions can be found [on the Snap Website](https://snapcraft.io/gluu-server).

<iframe src="https://snapcraft.io/gluu-server/embedded?button=black" frameborder="0" width="100%" height="330px" style="border: 1px solid #CCC; border-radius: 2px;"></iframe>


### Uninstall process

```
$ snap remove gluu-server
```
