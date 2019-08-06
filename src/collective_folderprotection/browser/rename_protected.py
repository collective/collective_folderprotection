# -*- coding: utf-8 -*-

from .. import _
from ..behaviors.interfaces import IRenameProtected
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.content.browser.actions import RenameForm as BaseRenameForm
from plone.app.content.browser.contents.rename import (
    RenameActionView as BaseRenameActionView,
)
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button


class RenameForm(BaseRenameForm):
    @button.buttonAndHandler(PloneMessageFactory(u"Rename"), name="Rename")
    def handle_rename(self, action):
        # First check if the object itself is protected
        adapter = IRenameProtected(self.context, None)
        if adapter:
            if adapter.rename_protection:
                IStatusMessage(self.request).add(
                    _(u"This item is protected against being renamed"),
                    type="error",
                )
                raise Unauthorized(
                    _(u"This item is protected against being renamed")
                )
        else:
            # Check with the parent
            parent = aq_parent(aq_inner(self.context))
            adapter = IRenameProtected(parent, None)
            if adapter:
                if adapter.rename_protection:
                    IStatusMessage(self.request).add(
                        _(
                            u"This folder is protected against renaming "
                            u"items inside of it."
                        ),
                        type="error",
                    )
                    raise Unauthorized(
                        _(
                            u"This folder is protected against renaming "
                            u"items inside of it."
                        )
                    )
        return super(RenameForm, self).handle_rename(self, action)

    @button.buttonAndHandler(
        PloneMessageFactory(u"label_cancel", default=u"Cancel"), name="Cancel"
    )
    def handle_cancel(self, action):
        self.request.response.redirect(self.view_url())


class RenameActionView(BaseRenameActionView):
    def __call__(self):
        self.errors = list()
        context = aq_inner(self.context)
        catalog = getToolByName(context, "portal_catalog")

        for key in self.request.form.keys():
            if not key.startswith("UID_"):
                continue
            uid = self.request.form[key]
            brains = catalog.searchResults(UID=uid, show_inactive=True)
            if len(brains) == 0:
                continue
            obj = brains[0].getObject()

            # First check if the object itself is protected
            adapter = IRenameProtected(obj, None)
            if adapter:
                if adapter.rename_protection:
                    msgid = _(
                        u"protected_item_rename",
                        default=(
                            u"Item ${title} is protected against "
                            u"being renamed"
                        ),
                        mapping={u"title": obj.Title()},
                    )
                    self.errors.append(msgid)
                    return self.message(list())
            else:
                # Check with the parent
                parent = aq_parent(aq_inner(obj))
                adapter = IRenameProtected(parent, None)
                if adapter:
                    if adapter.rename_protection:
                        self.errors.append(
                            _(
                                u"This folder is protected against renaming "
                                u"items inside of it."
                            )
                        )
                        return self.message(list())

        return super(RenameActionView, self).__call__()
