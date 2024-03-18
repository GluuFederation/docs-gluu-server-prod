# Inbound identity using Apple Sign In

This tutorial offers a step-by-step guide to integrate Apple Sign In, an Apple feature that enables iOS and Mac users to sign in to apps and websites using their Apple ID.

While steps covered in the [Inbound identity using OIDC and OAuth](../authn-guide/inbound-oauth-passport.md) are enough to integrate any OIDC or OAuth compliant server, making Apple fit into the framework requires a lot more work due to the amount of configurations required by Apple and certain atypical behaviors of the authorization server itself. This guide was written to help you streamline the process.

## Pre-requisites

- No previous knowledge of [passport](../authn-guide/passport.md) (the key Gluu server component for inbound identity) is required to follow this document, however, it is assumed your Gluu server has Passport already [enabled](../authn-guide/inbound-oauth-passport.md#enable-passport).

- Ideally, your Gluu instance has to be publicly accessible to Internet. This is due to Apple URL verification processes. If this is a problem for your organization, it is possible to workaround it using proxy techniques. 

- An [Apple developer account](https://developer.apple.com/programs/enroll/) is required

!!! Note
    It's not necessary to have a valid production SSL cert in your Gluu instance
    
## Creating an Apple application

There are a number of configurations that must be performed using your Apple developer account before the actual integration takes place. [This tutorial](https://github.com/ananay/apple-auth/blob/master/SETUP.md) does a great job at explaining the steps required. As you go with it, ensure you collect the following elements:

- A service ID
- A team ID
- A key ID and a key file 

You will be prompted to enter a redirect URL. Please provide `https://<your-gluu-domain>/passport/auth/apple/callback`.

For domain verification purposes you will be given a file that it is supposed to be accessible at `https://<your-gluu-domain>/.well-known/apple-developer-domain-association.txt`. To do so follow the steps below:

=== "Community Edition - VM"
    1. SSH to your Gluu server
    1. Copy the file to `/opt/gluu/jetty/oxauth/custom/static` inside chroot
    1. In chroot, locate the Apache config file. In most cases it is `/etc/apache2/sites-available/https_gluu.conf`
    1. At the bottom, near to a directive like `ProxyPass /.well-known/openid-configuration` add a new one this way:
    
        ```
        ProxyPass /.well-known/apple-developer-domain-association.txt http://localhost:8081/oxauth/ext/resources/apple-developer-domain-association.txt
        ```
    
    1. Save the file and [restart](../operation/services.md#restart) Apache, eg. `# service apache2 restart`
    1. Ensure the file is correctly loaded. Open a browser, and hit `https://<your-gluu-domain>/.well-known/apple-developer-domain-association.txt`

=== "Cloud Native Edition - Kubernetes"

    1. Create file `apple-ing.yaml` with the following content.
    
        ```yaml
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          annotations:
            kubernetes.io/ingress.class: nginx
            nginx.ingress.kubernetes.io/configuration-snippet: rewrite /.well-known/apple-developer-domain-association.txt
              /oxauth/ext/resources/apple-developer-domain-association.txt$1 break;
            nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
            nginx.ingress.kubernetes.io/rewrite-target: /oxauth/ext/resources/apple-developer-domain-association.txt
            nginx.ingress.kubernetes.io/ssl-redirect: "false"
          generation: 3
          name: gluu-ingress-apple-configuration
          namespace: gluu
        spec:
          rules:
          - host: demoexample.gluu.org
            http:
              paths:
              - backend:
                  serviceName: oxauth
                  servicePort: 8080
                path: /.well-known/apple-developer-domain-association.txt
          tls:
          - hosts:
            - demoexample.gluu.org
            secretName: tls-certificate
        ```
    
    1. Apply the ing in the namespace where Gluu is installed in:
    
        ```bash
        kubectl apply -f apple-ing.yaml -n gluu
        ```
    
    1. Mount `apple-developer-domain-association.txt` in oxauth pods by first creating the configmap.
    
        ```bash
        kubectl create configmap apple-developer-domain-association-cm -n gluu --from-file=apple-developer-domain-association.txt
        ```
        
    1. Mount the `apple-developer-domain-association-cm` inside the oxauth pods.
    
        ```yaml
            volumeMounts:
            - mountPath: /opt/gluu/jetty/oxauth/custom/static/apple-developer-domain-association.txt
              name: apple-developer-domain-association
              subPath: apple-developer-domain-association.txt                
          volumes: 
          - name: apple-developer-domain-association
            configMap:
              name: apple-developer-domain-association-cm 
        ```

## Low level configurations

=== "Community Edition - VM"

    SSH to your Gluu server and copy the **key file** to `/etc/certs` inside chroot.     

=== "Cloud Native Edition - Kubernetes"

    Mount **key file** into `/etc/certs` inside oxpassport pod.
    
    1. Mount `AuthKey_88EXAMPLE.p8` in oxpassport pods by first creating the configmap.
    
        ```bash
        kubectl create configmap apple-auth-key-cm -n gluu --from-file=AuthKey_88EXAMPLE.p8
        ```
        
    1. Mount the `apple-auth-key-cm` inside the oxpassport pods.
    
        ```yaml
            volumeMounts:
            - mountPath: /etc/certs/AuthKey_88EXAMPLE.p8
              name: apple-auth-key
              subPath: AuthKey_88EXAMPLE.p8                
          volumes: 
          - name: apple-auth-key
            configMap:
              name: apple-auth-key-cm
        ```
        
## Add Apple Sign In to supported identity providers

In this section we'll onboard Apple to the list of known providers for inbound identity.

1. Login to oxtrust UI with an administrative user
1. Go to `Passport` > `Providers` and click on `Add new provider`
1. For provider ID, enter `apple`. If you want to use a different ID, you'll have to change the redirect URL in your Apple developer account to conform
1. Enter a Display Name (eg. Apple Sign In)
1. For type choose `oauth`
1. For strategy enter `@nicokaiser/passport-apple`
1. For mapping enter `apple`
1. Supply a logo location if desired. More info [here](../authn-guide/passport.md#about-logo-images)
1. Enter the **service ID** in `client ID` field
1. Remove `Client Secret`.
1. Add a new property `keyID` and fill its value with the **key id** you collected [earlier](#creating-an-apple-application)
1. Add a new property `teamID` and fill its value with the **team ID**
1. Add a new property `key` supplying the path to the key file, eg. `/etc/certs/AuthKey_blah_blah.p8`
1. Add a new property `scope` with value `["name", "email"]`
1. Click on `Add`

Here is an example of how the form might look:

![Sample form](../img/user-authn/passport/sample-apple-form.png)

## Test

Almost done...

Set passport's logging level to debug. You can revert to *info* or other when you are done with your tests. In oxTrust go to `Passport` > `Basic configuration` and change `Log level`.

You can use any OIDC app protected by Gluu in order to test. To do so, ensure to pass `passport_social` for `acr_values` in your authentication request. Actually you can leverage oxTrust to do this: go to `Configuration` > `Manage authentication` and set `oxTrust acr` to `passport_social`. Then logout.

Attempt to login to the application. You will see "Apple Sign In" listed on the right hand panel. Click on it to trigger the flow. You will be taken to the Apple web site to enter your credentials and then returned to the application with access to it.

Something went wrong?

- Double check all configurations were applied accurately
- Check `passport.log` (find it at `/opt/gluu/node/passport/logs`)
- Open a support ticket
