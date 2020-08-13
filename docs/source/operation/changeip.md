# Change IP Address of existing Gluu CE Server

If your IP changes after initial setup, you need to change your Gluu Server's configuration.

1. Start the Gluu Server
1. Log in to Gluu Server Chroot container
1. Change the IP address in `/etc/hosts` file
1. [Restart](./services.md#restart) the `opendj` service (or other service used for persistence)
1. [Restart](./services.md#restart) the `httpd` service
1. [Restart](./services.md#restart) the `idp` service
1. [Restart](./services.md#restart) the `identity` service
1. [Restart](./services.md#restart) the `oxauth` service
1. Test
