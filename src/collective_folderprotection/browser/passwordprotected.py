# -*- coding: utf-8 -*-
from hashlib import md5
from datetime import datetime
from random import random

from z3c.form import button
from z3c.form import field
from z3c.form import form

from zope.annotation import IAnnotations

from zope.component import getMultiAdapter

from zope.interface import Interface

from plone.app.z3cform.layout import wrap_form

from Products.Five.browser import BrowserView

from collective_folderprotection.behaviors.interfaces import IPasswordProtected
from collective_folderprotection.config import ANNOTATION_PASSWORD_HASH
from collective_folderprotection.config import HASHES_ANNOTATION_KEY
from collective_folderprotection.config import HASH_COOKIE_KEY
from collective_folderprotection.config import TIME_TO_LIVE
from collective_folderprotection import _


class RenderPasswordView(BrowserView):

    def __call__(self):
        self.came_from = self.request.get('PATH_INFO')
        self.request.set('came_from', self.came_from)
        # Get the object for which we need to get access to
        ob = getattr(self.__parent__, self.context.name)
        prompt = getMultiAdapter((ob, self.request), name="passwordprompt")
        return prompt()
      
      
class AskForPasswordView(BrowserView):
    """
    """
    
    def __call__(self):
        if self.request.get('submit', False):
            # The password was submitted
            passw = self.request.get('password', '')
            passw_hash = md5(passw).hexdigest()
            ann = IAnnotations(self.context)
            if ANNOTATION_PASSWORD_HASH in ann:
                # If this is not true, means the Manager has not set a password
                # for this resource yet, then do not authenticate...
                
                # If there's no came_from, then just go to the object itself
                came_from = self.request.get('came_from', '/'.join(self.context.getPhysicalPath()))
                if passw_hash == ann[ANNOTATION_PASSWORD_HASH]:
                    # The user has entered a valid password, then we store a
                    # random hash with a TTL so we know he already authenticated
                    hashes = ann.get(HASHES_ANNOTATION_KEY, {})
                    random_hash = md5(str(random())).hexdigest()
                    while random_hash in hashes:
                        # This would be *REALLY* hard to happen, but just in case...
                        random_hash = md5(str(random())).hexdigest()

                    hashes[random_hash] = datetime.now() + TIME_TO_LIVE
                    # Store the hash in the annotation
                    ann[HASHES_ANNOTATION_KEY] = hashes
                    # Save the hash in a cookie
                    self.request.response.setCookie(HASH_COOKIE_KEY, random_hash)
                    # Now that we have our cookie set, we can traverse to the object
                    ob = self.context.restrictedTraverse(came_from)
                    self.request.response.redirect(ob.absolute_url())
                    return
                else:
                    # Invalid password, stay here, but mantain the "came_from"
                    self.request.set('came_from', came_from)
            
        return self.index()


class AssignPasswordForm(form.Form):

    fields = field.Fields(IPasswordProtected)

    ignoreContext = False

    @button.buttonAndHandler(_('Save'), name='save')
    def save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _(u"Please correct errors")
            return
        passw = data.get('password', '')
        passw_hash = md5(passw).hexdigest()
        ann = IAnnotations(self.context)
        if HASHES_ANNOTATION_KEY in ann:
            # Remove old storde hashes
            del ann[HASHES_ANNOTATION_KEY]

        ann[ANNOTATION_PASSWORD_HASH] = passw_hash
        self.status = _(u"Password assigned.")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def cancel(self, action):
        self.status = _(u"Cancelled.")

AssignPasswordFormView = wrap_form(AssignPasswordForm)


class IAssignPasswordValidation(Interface):
    
    def allowed():
        """ Decide when to show the Assign password tab"""


class AssignPasswordValidation(BrowserView):
    
    def allowed(self):
        authorized = False
        try:
            IPasswordProtected(self.context)
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if ('Manager' in roles or 'Owner' in roles):
                authorized = True
        except TypeError:
            pass

        return authorized
