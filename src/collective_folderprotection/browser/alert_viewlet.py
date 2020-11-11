# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from collective_folderprotection.behaviors.interfaces import IPasswordProtected
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.contenttypes.interfaces import IFolder
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot


class AlertViewlet(ViewletBase):
    """ Displays alert messages when content is pw protected"""

    context_pw_protected = False
    folder_pw_protected = False
    parent_pw_protected = None

    def update(self):
        super(AlertViewlet, self).update()
        if self.request.response.getStatus() == 401:
            return
        context = aq_inner(self.context)
        if not IPloneSiteRoot.providedBy(context):
            if not IFolder.providedBy(context):
                context = aq_parent(context)
                if self.context.id != context.getDefaultPage():
                    self.folder_pw_protected = True

        passw_behavior = IPasswordProtected(context, None)
        if passw_behavior:
            self.context_pw_protected = passw_behavior.is_password_protected()

        while not IPloneSiteRoot.providedBy(context):
            context = aq_parent(context)
            passw_behavior = IPasswordProtected(context, None)
            if passw_behavior and passw_behavior.is_password_protected():
                self.parent_pw_protected = context
                break
