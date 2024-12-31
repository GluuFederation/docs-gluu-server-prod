# Test Gluu Server with SPTEST.IAMSHOWCASE.COM

## Configuration in Gluu Server

* From https://sptest.iamshowcase.com/instructions#start, grab the sptest.iamshowcase.com SP metadata, link: https://sptest.iamshowcase.com/testsp_metadata.xml

* Move to create Trust Relationship in Gluu Server. Here is how you can create SAML Trust Relationship in Gluu Server. 


![Screenshot from 2024-09-18 00-51-38](https://github.com/user-attachments/assets/f2983b9e-dd61-48ff-98a9-dcc44279e7bb)


## Configuration in SPTEST.IAMSHOWCASE.COM website

* Navigate to the SAMLTest website: https://sptest.iamshowcase.com/instructions#spinit
* Upload your Gluu Server Shibboleth metadata. Collect your IDP metadata with the following link: https://<server_name>/idp/shibboleth

  
![Screenshot from 2024-09-20 02-16-59](https://github.com/user-attachments/assets/860d98eb-d319-4fb0-82a5-34b1a45dc544)

* After successful upload, you will see the following confirmation URL

  
![Screenshot from 2024-09-20 02-20-17](https://github.com/user-attachments/assets/a2064296-6518-437d-a898-7da966251e09)


## Test 

- Copy the confirmation URL.
- Open a new tab and paste it.
- After successful authentication, you will be redirected to the protected page of the SPTEST.IAMSHOWCASE.COM website.

![Screenshot from 2024-09-20 23-57-10](https://github.com/user-attachments/assets/ee18badf-b28b-4f26-929b-45ab0dd5a987)


// ![Screenshot from 2024-09-20 02-44-24](https://github.com/user-attachments/assets/bd84a976-0aa1-48c9-bf5d-32f065d5083d)

