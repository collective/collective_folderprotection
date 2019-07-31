# -*- coding: utf-8 -*-

from .. import _
from ..behaviors.interfaces import IRenameProtected
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.content.browser.actions import RenameForm as BaseRenameForm
from plone.app.content.browser.contents.rename import RenameActionView \
    as BaseRenameActionView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button


class RenameForm(BaseRenameForm):

    @button.buttonAndHandler(PloneMessageFactory(u'Rename'), name='Rename')
    def handle_rename(self, action):
        parent = aq_parent(aq_inner(self.context))
        try:
            IRenameProtected(parent)
            IStatusMessage(self.request).add(
                _(u'You are not allowed to rename items in this folder'),
                type='error'
            )
            raise Unauthorized(_(u'You are not allowed to rename items in this '
                                 u'folder'))
        except TypeError:
            pass
        return super(RenameForm, self).handle_rename(self, action)


class RenameActionView(BaseRenameActionView):

    def __call__(self):
        self.errors = list()
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        try:
            for key in self.request.form.keys():
                if not key.startswith('UID_'):
                    continue
                uid = self.request.form[key]
                brains = catalog.searchResults(UID=uid, show_inactive=True)
                if len(brains) == 0:
                    continue
                obj = brains[0].getObject()
                parent = aq_parent(aq_inner(obj))
                IRenameProtected(parent)
                self.errors.append(_(u'You are not allowed to rename items in '
                                     u'this folder.'))
                return self.message(list())
        except TypeError:
            pass

        return super(RenameActionView, self).__call__()
