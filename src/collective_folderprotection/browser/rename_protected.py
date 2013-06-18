# -*- coding: utf-8 -*-

# Recreate what the object_rename python script does, so we can cancel if
# the folder is protected

from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import transaction_note
from Products.CMFCore.utils import getToolByName
from OFS.CopySupport import CopyError
from AccessControl import Unauthorized
from Products.PythonScripts.standard import url_quote_plus

from Products.Five.browser import BrowserView

from collective_folderprotection.behaviors.interfaces import IRenameProtected


class ObjectRenameView(BrowserView):

    def __call__(self):
        parent = self.context.aq_parent
        try:
            IRenameProtected(parent)
            raise Unauthorized()
        except TypeError:
            # This content type was not protected, so it can be renamed
            pass

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
