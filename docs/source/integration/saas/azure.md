# Connect Azure AD as an External IDP with Gluu Server through Passport

## Requirements
- Azure AD administration portal
- Gluu Server with Passport installed

## Register Application at Azure Portal

1. Login into [Azure Portal](https://portal.azure.com/)
2. Go to **Microsoft Entra ID**( Previously known as Azure AD)
3. Go to Enterprise applications (left sidebar)
4. New Application > Create your Own application
5. Set your application name and choose 2nd one from the application type (Register an application to integrate with Microsoft Entra ID (App you're developing)) then create 

<img width="571" alt="Screenshot 2023-12-26 at 17 50 19" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/76fdf8f3-8698-4aa1-9bca-8a3f92f89f1e">

6. On the next page, choose account types (single tenant)
7. **register**

<img width="890" alt="Screenshot 2023-12-26 at 17 52 25" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/c7993bb8-9a77-455b-9cac-8814e496c8e5">

## Configure Application
Go to **Enterprise application** again, you will see a list of applications there.

1. select the application you just created in the above steps
2. go to **user and groups** and add some users
3. go to **Single sign-on** > Application Settings. You will see details of the application
4. from **Endpoints** You will get an OpenID configuration Endpoint which may look like this: `https://login.microsoftonline.com/[Directory (tenant) ID]/v2.0/.well-known/openid-configuration`

<img width="1483" alt="Screenshot 2023-12-26 at 18 11 04" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/7661f1ad-652c-4d4d-8523-819478ab0711">

Grab:
- from the OpenID Config URL grab the issuer
- Application / Client ID 
- Client credential (go to client credential > create a client secret and copy value) 

## Create Provider at Gluu Server

Create a passport provider from the gluu server like the below image.

<img width="1500" alt="Screenshot 2023-12-27 at 09 56 14" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/f4bb7e25-d33e-4a4f-a0be-f42f5fc3a9f6">

- client_id: azure application/client id
- client secret: application client credential
- issuer: application issuer URL
- scope: openid, email, profile
- token_endpoint_auth_method: client_secret_post

After creating the provider, grab the **Callback URL** which we are going to add on the application.

## Add Redirect URI in the application

- Go to the application 
- Select **Authentication**
- Add Platform > Web > add redirect URI

<img width="755" alt="Screenshot 2023-12-27 at 10 16 58" src="https://github.com/GluuFederation/docs-gluu-server-prod/assets/20867846/f02b0a73-a0f2-47b6-b5bb-165ac9f28d13">

We are done. You can test from the gluu server using the `passport social` authentication method. See the video [here](https://www.youtube.com/watch?v=aqlrSwBqLf8)
