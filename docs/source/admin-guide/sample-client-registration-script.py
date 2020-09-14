from org.gluu.model.custom.script.type.client import ClientRegistrationType
from org.gluu.util import StringHelper, ArrayHelper
from org.gluu.oxauth.service import ScopeService
from java.util import Arrays, ArrayList

import java

class ClientRegistration(ClientRegistrationType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, configurationAttributes):
        print "Client registration. Initialization"

        self.scopeService = ScopeService.instance()

        print "Client registration. Initialized successfully"

        return True   

    def destroy(self, configurationAttributes):
        print "Client registration. Destroy"
        print "Client registration. Destroyed successfully"
        return True   

    # Update client entry before persistent it
    #   registerRequest is org.gluu.oxauth.client.RegisterRequest
    #   client is org.gluu.oxauth.model.registration.Client
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def updateClient(self, registerRequest, client, configurationAttributes):
        print "Client registration. UpdateClient method"

        redirectUris = client.getRedirectUris()
        print "Client registration. Redirect Uris:", redirectUris

        addAddressScope = False
        for redirectUri in redirectUris:
            if (StringHelper.equalsIgnoreCase(redirectUri, "https://client.example.com/example1")):
                addAddressScope = True
                break
        
        print "Client registration. Is add address scope:", addAddressScope

        if (addAddressScope):
            currentScopes = client.getScopes()
            print "Client registration. Current scopes:", currentScopes
            
            addressScope = self.scopeService.getScopeByDisplayName("address")
            newScopes = ArrayHelper.addItemToStringArray(currentScopes, addressScope.getDn())
    
            print "Client registration. Result scopes:", newScopes
            client.setScopes(newScopes)

        return True

    def getApiVersion(self):
        return 1

    # Returns secret key which will be used to validate Software Statement if HMAC algorithm is used (e.g. HS256, HS512). Invoked if oxauth conf property softwareStatementValidationType=SCRIPT which is default/fallback value.
    # context is reference of org.gluu.oxauth.service.external.context.DynamicClientRegistrationContext (in https://github.com/GluuFederation/oxauth project )
    def getSoftwareStatementHmacSecret(self, context):
        return ""

    # Returns JWKS which will be used to validate Software Statement if keys are used (e.g. RS256). Invoked if oxauth conf property softwareStatementValidationType=SCRIPT which is default/fallback value.
    # context is reference of org.gluu.oxauth.service.external.context.DynamicClientRegistrationContext (in https://github.com/GluuFederation/oxauth project )
    def getSoftwareStatementJwks(self, context):
        return ""