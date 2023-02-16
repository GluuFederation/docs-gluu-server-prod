# Ports

## Ports used by Gluu Server components

The following ports are used by internal Gluu Server applications (i.e. oxAuth, oxTrust, LDAP, Passport, etc.). These are backend ports, not open to the world, that listen at loopback iface (127.0.0.x).

|Port| Application|
-----|-------------
|8081| oxAuth Server|
|8082| oxTrust Server|
|8085| oxAuth-RP|
|8086| Shibboleth IDP|
|8087| SCIM|
|8090| Passport |
|8091| Casa |

!!! Note
    If Gluu is being clustered, more ports must be accessible from the clustered nodes. Follow the [cluster documentation](../installation-guide/cluster.md). 

## Ports open to the Internet

The following ports are open to the Internet by default.

|       Port Number     |       Protocol        |   Notes          |
|-----------------------|-----------------------|------------------|
|       80              |       tcp             | Forwards to 443  |
|       443             |       tcp             | apache2/httpd    |
|       22              |       tcp             | ssh              |
