# oxShibboleth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2022, Gluu
#
# Author: Djeumen Rolain <rolain@gluu.org>
# This IDP interception script remaps attributes 
#

from org.gluu.model.custom.script.type.idp import IdpType
from org.gluu.util import StringHelper
from org.gluu.idp.externalauth import AuthenticatedNameTranslator
from org.gluu.idp.externalauth import ShibOxAuthAuthServlet
from net.shibboleth.idp.authn.principal import UsernamePrincipal, IdPAttributePrincipal
from net.shibboleth.idp.authn import ExternalAuthentication
from net.shibboleth.idp.attribute import IdPAttribute, StringAttributeValue
from net.shibboleth.idp.authn.context import AuthenticationContext, ExternalAuthenticationContext
from net.shibboleth.idp.attribute.context import AttributeContext
from javax.security.auth import Subject
from java.util import Collections, HashMap, HashSet, ArrayList, Arrays
from java.lang import String


import java
import sys
import json

class IdpExtension(IdpType):

    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, customScript, configurationAttributes):
        print "Idp Remap Script. Initialization"
        
        self.defaultNameTranslator = AuthenticatedNameTranslator()

        self.allowedAcrsList = ArrayList()
        if configurationAttributes.containsKey("allowed_acrs"):
            allowed_acrs = configurationAttributes.get("allowed_acrs").getValue2()
            allowed_acrs_list_array = StringHelper.split(allowed_acrs,",")
            self.allowedAcrsList = Arrays.asList(allowed_acrs_list_array)
        
        self.remapConfiguration = {}
        if configurationAttributes.containsKey("remap_configuration"):
            remap_configuration = configurationAttributes.get("remap_configuration").getValue2()
            try:
                self.remapConfiguration = json.loads(remap_configuration)
                print "Idp Remap Script. %s " % (self.remapConfiguration)
            except:
                print "Idp Remap Script. Could not load remap configuration"
                self.remapConfiguration = {}
        

        return True

    def destroy(self, configurationAttributes):
        print "Idp Remap Script. Destroy"
        return True

    def getApiVersion(self):
        return 13

    # Translate attributes from user profile
    #   context is org.gluu.idp.externalauth.TranslateAttributesContext (https://github.com/GluuFederation/shib-oxauth-authn3/blob/master/src/main/java/org/gluu/idp/externalauth/TranslateAttributesContext.java)
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def translateAttributes(self, context, configurationAttributes):
        print "Idp Remap Script. Method: translateAttributes"
        
        #Return True to specify that default method is not needed
        #In this case we return false so if there is another script 
        #it's translateAttributes method should be invoked instead , or if there 
        # isn't , the default attribute translation should kick in 
        return False

    # Update attributes before releasing them
    #   context is org.gluu.idp.consent.processor.PostProcessAttributesContext (https://github.com/GluuFederation/shib-oxauth-authn3/blob/master/src/main/java/org/gluu/idp/consent/processor/PostProcessAttributesContext.java)
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def updateAttributes(self, context, configurationAttributes):
        print "Idp Remap Script. Method: updateAttributes"
        #
        #
        #
        print "Idp Remap Script. Method: updateAttributes"
        if self.remapConfiguration is None:
            print "Idp Remap Script. No remap configuration loaded. Nothing to do."
            return True
        if type(self.remapConfiguration) is not dict:
            print "Idp Remap Script. Invalid remap configuration loaded. Nothing to do."
            return True
        
        # Get all of the source attributes and iterate through them 
        for sourceAttribute in self.remapConfiguration.keys():
            targetAttribute = self.remapConfiguration[sourceAttribute]
            self.remapAttribute(context,sourceAttribute,targetAttribute)
        return True

    # Check before allowing user to log in
    #   context is org.gluu.idp.externalauth.PostAuthenticationContext (https://github.com/GluuFederation/shib-oxauth-authn3/blob/master/src/main/java/org/gluu/idp/externalauth/PostAuthenticationContext.java)
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def postAuthentication(self, context, configurationAttributes):
        print "Idp Remap Script. Method: postAuthentication"
        userProfile = context.getUserProfile()
        authenticationContext = context.getAuthenticationContext
        
        requestedAcr = None
        if authenticationContext != None:
            requestedAcr = authenticationContext.getAuthenticationStateMap().get(org.gluu.idp.externalauth.OXAUTH_ACR_REQUESTED)

        usedAcr = userProfile.getUsedAcr()

        print "Idp Remap Script. Method: postAuthentication. requestedAcr = %s, usedAcr = %s" % (requestedAcr, usedAcr)

        if requestedAcr == None:
            print "Idp Remap Script. Method: postAuthentication. requestedAcr is not specified"
            return True

        if not self.allowedAcrsList.contains(usedAcr):
            print "Idp Remap Script. Method: postAuthentication. usedAcr '%s' is not allowed" % usedAcr
            return False

        return True

    # Check before allowing user to log in
    #   context is org.gluu.idp.externalauth.PostAuthenticationContext (https://github.com/GluuFederation/shib-oxauth-authn3/blob/master/src/main/java/org/gluu/idp/externalauth/PostAuthenticationContext.java)
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def postAuthentication(self, context, configurationAttributes):
        print "Idp Remap Script. Method: postAuthentication"
        userProfile = context.getUserProfile()
        authenticationContext = context.getAuthenticationContext()
        
        requestedAcr = None
        if authenticationContext != None:
            requestedAcr = authenticationContext.getAuthenticationStateMap().get(ShibOxAuthAuthServlet.OXAUTH_ACR_REQUESTED)

        usedAcr = userProfile.getUsedAcr()

        print "Idp Remap Script. Method: postAuthentication. requestedAcr = %s, usedAcr = %s" % (requestedAcr, usedAcr)

        if requestedAcr == None:
            print "Idp Remap Script. Method: postAuthentication. requestedAcr is not specified"
            return True

        if not self.allowedAcrsList.contains(usedAcr):
            print "Idp Remap Script. Method: postAuthentication. usedAcr '%s' is not allowed" % usedAcr
            return False

        return TrueRich
    
    def remapAttribute(self, context , sourceAttribute , targetAttribute):
        print "Idp Remap Script. Method: remapAttribute (%s, %s)" % (sourceAttribute , targetAttribute)
        if not sourceAttribute or not targetAttribute:
            print "Idp Remap Script. Source and/or target attributes are null"
            return False
        sourceIdpAttribute = context.getIdpAttributeMap().get(sourceAttribute)
        if sourceIdpAttribute is not None:
            context.getIdpAttributeMap().remove(sourceAttribute)
            targetIdpAttr = IdPAttribute(targetAttribute)
            targetIdpAttr.setValues(sourceIdpAttribute.getValues())
            context.getIdpAttributeMap().put(targetAttribute , targetIdpAttr)
            print "Idp Remap Script. Source attribute found and remapped to target attribute"
            return True
        
        print "Idp Remap Script. Source attribute not found. Nothing to do"
        return False
