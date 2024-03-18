# MAU Exporter

Works against AS "4.3.1" and later.

## Prepare Authorization Server

1. Make sure `jans_stat` scope is present on server and is set as default (`defaultScope=true`)
2. AS restricts by time how often `/stat` endpoint can be called. Default limit is `60` seconds. Server replies with `403 Forbidden` error if exceeds it.
   Limit can be changed via `statWebServiceIntervalLimitInSeconds` global configuration property. 
3. If dynamic registration is disabled on AS, enable it (`dynamicRegistrationEnabled=true`)

## Run

Run jar with following command:
```cmd
#java -jar stat-exporter-4.5.2-SNAPSHOT-jar-with-dependencies.jar <well known endpoint of AS>
```

Successful execution sample:
```cmd
root@yuriyz-charmed-skylark:/opt# java -jar stat-exporter-4.5.2-SNAPSHOT-jar-with-dependencies.jar https://yuriyz-charmed-skylark.gluu.info/.well-known/openid-configuration
Downloading discovery https://yuriyz-charmed-skylark.gluu.info/.well-known/openid-configuration
Downloaded
Issuer: https://yuriyz-charmed-skylark.gluu.info
Registering client at https://yuriyz-charmed-skylark.gluu.info/oxauth/restv1/register
Registered client_id 55724b5a-1611-46fb-80bd-c2f4536ede38
Requesting token at https://yuriyz-charmed-skylark.gluu.info/oxauth/restv1/token with client_id: 55724b5a-1611-46fb-80bd-c2f4536ede38
Obtained token successfully with scopes 'jans_stat openid'
Downloading stat info ...
Downloaded stat info successfully.
Stat Result:
{
  "data" : {
    "202306" : 1
  },
  "mau-signature" : "44cb730c420480a0477b505ae68af508fb90f96cf0ec54c6ad16949dd427f13a"
}
root@yuriyz-charmed-skylark:/opt#
```

[Download stat-exporter JAR](https://jenkins.gluu.org/maven/org/gluu/stat-exporter/4.5.2-SNAPSHOT/stat-exporter-4.5.2-SNAPSHOT-jar-with-dependencies.jar)
