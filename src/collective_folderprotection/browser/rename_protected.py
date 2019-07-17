# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective_folderprotection.behaviors.interfaces import IRenameProtected
from plone.app.content.browser.actions import RenameForm as BaseRenameForm


class RenameForm(BaseRenameForm):

    def handle_rename(self, action):
        try:
            IRenameProtected(self.context.aq_parent)
            raise Unauthorized()
        except TypeError:
            pass
        return super(RenameForm, self).handle_rename(action)
