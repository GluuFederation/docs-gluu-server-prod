# SNAP Installation

Ubuntu and Debian:

snapcraft repo:
```
$ apt install snapd
$ export PATH="/snap/bin:$PATH"
$ snap install core
$ snap install gluu-server
$ gluu-server.setup
```

Gluu repo:
```
$ apt install snapd
$ export PATH="/snap/bin:$PATH"
$ wget https://repo.gluu.org/snaps/gluu-server_4.1.1_amd64.snap
$ snap install core
$ snap install --dangerous gluu-server_4.1.1_amd64.snap
$ gluu-server.setup
```


Centos and RHEL:

snapcraft repo:
```
$ sudo yum install epel-release
$ sudo yum -y install snapd
$ sudo ln -s /var/lib/snapd/snap /snap
$ sudo systemctl enable --now snapd.socket
$ export PATH="/var/lib/snapd/snap/bin:/snap/bin:$PATH"
$ snap install core
$ snap install gluu-server
$ gluu-server.setup
```

GLuu repo:
```
$ sudo yum install epel-release
$ sudo yum -y install snapd wget
$ sudo ln -s /var/lib/snapd/snap /snap
$ sudo systemctl enable --now snapd.socket
$ export PATH="/var/lib/snapd/snap/bin:/snap/bin:$PATH"
$ snap install core
$ wget https://repo.gluu.org/snaps/gluu-server_4.1.1_amd64.snap
$ snap install --dangerous gluu-server_4.1.1_amd64.snap
$ gluu-server.setup
```
