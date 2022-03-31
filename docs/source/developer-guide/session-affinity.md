# Authenticating via an External IDP a New User Created Using a Custom Authentication Script in a Cloud Native Setup with Kubernetes

## General Overview

This section explains how to authenticate via an external IDP a new user that has been created with a custom interception script in a cloud native setup of Gluu using LDAP as the backend persistence. For reference, you can read how a GLUU LDAP cloud native setup with Kubernetes is implemented [here](https://gluu.org/docs/gluu-server/4.3/installation-guide/install-kubernetes/). 

### Custom Authentication Script Overview

In the sample script being referred, we assume that the user is to be authenticated via an external IDP. If the user doesn't exist in OpenDJ, the script automatically creates the user in the database before attempting to query them.

- For example consider the sample snippet below extracted from the script:
 
    ```
    find_user_by_uid = userService.addUser(user, True)
    found_user_name = find_user_by_uid.getUserId()
    user_authenticated = authenticationService.authenticate(found_user_name)
    ```

### Cloud Native Setup Overview

LDAP as the backend persistence for GLUU can be setup in a cloud native approach. Refer to the link shared in the general overview on how to achieve this with Kubernetes. A complete setup enables having synchronized database instances for high availability.

For certain reasons E.g limited computing resources, OpenDJ replication might get so slow leading to unsynchronized databases at any given time intervals.

For instance a `find_user_by_uid.getUserId()` function in our script above can fail because Gluu ldap connections goes to a different opendj pod for every request made. The previously created user is not replicated quickly enough to all opendj pods thus causing authentication to fail.

### Solution

- To solve the issue above, a tested solution is to configure the services in a way that binds oxAuth for authentication to the same opendj it contacted when it created the user. This enables the clieent session to be reserved as long as the OpenDJ hasn't been restarted.

- In the OpenDJ service, set `service.spec.sessionAffinity` to `ClientIP`. By default the session held by the service is 3 hours and can be modified by setting `service.spec.sessionAffinityConfig.clientIP.timeoutSeconds`. For example to configure the sessionAffinity to the opendj service, refer to the snippet below.

    ```
    "sessionAffinity": "ClientIP",

    "sessionAffinityConfig": {
        "clientIP": {
            "timeoutSeconds": 28800
        }
    },
    ```

- Enhance the interception script with custom functionality that ease creation of a user E.g add detailed print statements and operation retries. For example the following custom addUser() method is added to the authentication script.

    ```
    def addUser(self, user, saml_user_uid):
        userService = CdiUtil.bean(UserService)
        count = 0
        while count < 5:
            count = count + 1
            try:
                find_user_by_uid = userService.getUserByAttribute("oxExternalUid", "custom_id_if_any:" + saml_user_uid)
                if not (find_user_by_uid is None):
                    return find_user_by_uid
                newUser = userService.addUser(user, True)
                return newUser
            except java.lang.Exception as err:
                print "Failed to add user."
                print str(err)
                time.sleep(count)
        print "ERROR: Failed to add user '%s' after 5 tries. " % user
        raise Exception("Failed to add user after 5 tries")
    ```

### Troubleshooting

- Ensure the setup is correct and the pods are running.

    ```
        kubectl get pods -n gluu
    ```

- Use the 'netstat' command to test if the opendj pods are connected

    ```
        kubectl exec -it -n gluu oxauth-xxxxxxxxxx-xxxx  -- sh 

        / # netstat -na |grep 1636
    ```