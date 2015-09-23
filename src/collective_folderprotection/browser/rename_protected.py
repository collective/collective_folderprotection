# -*- coding: utf-8 -*-

# Recreate what the object_rename python script does, so we can cancel if
# the folder is protected

from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.utils import getToolByName
from OFS.CopySupport import CopyError
from AccessControl import Unauthorized
from Products.PythonScripts.standard import url_quote_plus

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective_folderprotection.at.interfaces import IATRenameProtected
from collective_folderprotection.behaviors.interfaces import IRenameProtected
from collective_folderprotection import _

from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.interface import Interface

try:
    from Products.Archetypes.interfaces.base import IBaseFolder
    HAS_AT = True
except:
    HAS_AT = False


class ObjectRenameView(BrowserView):

    def __call__(self):
        parent = self.context.aq_parent

        try:
            IRenameProtected(parent)
            raise Unauthorized()
        except TypeError:
            if HAS_AT:
                # This will be true if AT and pw-protected enabled
                if IBaseFolder.providedBy(parent) and\
                   IATRenameProtected.providedBy(parent):
                    raise Unauthorized()

        title = safe_unicode(self.context.title_or_id())

        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.checkPermission('Copy or Move', self.context):
            raise Unauthorized, _(u'Permission denied to rename ${title}.',
                                  mapping={u'title': title})

        pathName = url_quote_plus('paths:list')
        safePath = '/'.join(self.context.getPhysicalPath())
        orig_template = self.request['HTTP_REFERER'].split('?')[0]
        url = '%s/folder_rename_form?orig_template=%s&%s=%s' % (self.context.absolute_url(),
                                                                orig_template,
                                                                pathName,
                                                                safePath)

        self.request.response.redirect(url)


class IRenameValidation(Interface):

    def can_disable_at_rename_protection():
        """ Return True if user can disable rename protection for this folder
        """

    def can_enable_at_rename_protection():
        """ Return True if user can enable rename protection for this folder
        """


class RenameValidation(BrowserView):

    def can_disable_at_rename_protection(self):
        can_disable = False
        if IBaseFolder.providedBy(self.context) and\
           IATRenameProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if ('Manager' in roles or 'Owner' in roles):
                can_disable = True

        return can_disable


    def can_enable_at_rename_protection(self):
        can_enable = False
        if IBaseFolder.providedBy(self.context) and not\
           IATRenameProtected.providedBy(self.context):
                pm = self.context.portal_membership
                roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
                if ('Manager' in roles or 'Owner' in roles):
                    can_enable = True

        return can_enable



class EnableATRenameProtection(BrowserView):

    def __call__(self):
        if IBaseFolder.providedBy(self.context) and not\
           IATRenameProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if not ('Manager' in roles or 'Owner' in roles):
                raise Unauthorized("You are not authorized to enable rename protection for this folder")

            alsoProvides(self.context, IATRenameProtected)
            messages = IStatusMessage(self.request)
            messages.add(_(u"Rename protection has been enabled"), type=u"info")

        self.request.response.redirect(self.context.absolute_url())


class DisableATRenameProtection(BrowserView):

    def __call__(self):
        if IBaseFolder.providedBy(self.context) and\
           IATRenameProtected.providedBy(self.context):
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if not ('Manager' in roles or 'Owner' in roles):
                raise Unauthorized("You are not authorized to disable rename protection for this item")

            noLongerProvides(self.context, IATRenameProtected)
            messages = IStatusMessage(self.request)
            messages.add(_(u"Rename protection has been disabled"), type=u"info")

        self.request.response.redirect(self.context.absolute_url())