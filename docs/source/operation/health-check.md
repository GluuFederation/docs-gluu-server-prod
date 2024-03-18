# Health Checks For Service Endpoints

Health checks are used to determine if a container is working as it should be or not.
By default some primary endpoints are enabled ouf of the box to check status of various components. 

## oxAuth

Endpoint: 
```
https://[hostname]/oxauth/restv1/health-check
```

Output should be something like this: 
```json
{"status": "running", "db_status":"online"}
```
Which means service is running and it's backend data store ( DB / LDAP ) is operating properly. 

## oxTrust

Endpoint: 
```
https://[hostname]/identity/restv1/health-check
```

Output will be same as [oxAuth health check endpoint](#oxauth). 

## Shibboleth

Endpoint: 
```
https://[hostname]/idp/health-check
```

Output will be same as [oxAuth health check endpoint](#oxauth).
   
## Passport

Endpoint: 
```
https://[hostname]/passport/health-check
```

Output should be little different from other services: 

```json
{"message":"Cool!!!","sessionCookie":{"originalMaxAge":86400000,"expires":"2023-09-11T17:13:24.401Z","secure":true,"httpOnly":true,"path":"/","sameSite":"none"}}
```
