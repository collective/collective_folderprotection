# -*- coding: utf-8 -*-
from AccessControl import Unauthorized

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from collective_folderprotection.at.interfaces import IATDeleteProtected
from collective_folderprotection import _

from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.interface import Interface

try:
    from Products.Archetypes.interfaces.base import IBaseFolder
    HAS_AT = True
except:
    HAS_AT = False


class IDeleteValidation(Interface):

    def can_disable_at_delete_protection():
        """ Return True if user can disable delete protection for this folder
        """

    def can_enable_at_delete_protection():
        """ Return True if user can enable delete protection for this folder
        """


class DeleteValidation(BrowserView):

    def can_disable_at_delete_protection(self):
        can_disable = False
        if IBaseFolder.providedBy(self.context) and\
           IATDeleteProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if ('Manager' in roles or 'Owner' in roles):
                can_disable = True

        return can_disable


    def can_enable_at_delete_protection(self):
        can_enable = False
        if IBaseFolder.providedBy(self.context) and not\
           IATDeleteProtected.providedBy(self.context):
                pm = self.context.portal_membership
                roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
                if ('Manager' in roles or 'Owner' in roles):
                    can_enable = True

        return can_enable



class EnableATDeleteProtection(BrowserView):

    def __call__(self):
        if IBaseFolder.providedBy(self.context) and not\
           IATDeleteProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if not ('Manager' in roles or 'Owner' in roles):
                raise Unauthorized("You are not authorized to enable delete protection for this folder")

            alsoProvides(self.context, IATDeleteProtected)
            messages = IStatusMessage(self.request)
            messages.add(_(u"Delete protection has been enabled"), type=u"info")

        self.request.response.redirect(self.context.absolute_url())


class DisableATDeleteProtection(BrowserView):

    def __call__(self):
        if IBaseFolder.providedBy(self.context) and\
           IATDeleteProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if not ('Manager' in roles or 'Owner' in roles):
                raise Unauthorized("You are not authorized to disable delete protection for this item")

            noLongerProvides(self.context, IATDeleteProtected)
            messages = IStatusMessage(self.request)
            messages.add(_(u"Delete protection has been disabled"), type=u"info")

        self.request.response.redirect(self.context.absolute_url())