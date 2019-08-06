# -*- coding: utf-8 -*-
import six
from hashlib import md5
from datetime import datetime
from random import random

from z3c.form import button
from z3c.form import field
from z3c.form import form

from zope.annotation import IAnnotations

from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

from DateTime.DateTime import DateTime

from plone.app.layout.icons.icons import CatalogBrainContentIcon
from plone.app.layout.icons.interfaces import IContentIcon

from plone.app.z3cform.layout import wrap_form

from Products.Five.browser import BrowserView

from collective_folderprotection.behaviors.interfaces import IPasswordProtected
from collective_folderprotection.config import HASHES_ANNOTATION_KEY
from collective_folderprotection.config import HASH_COOKIE_KEY
from collective_folderprotection.config import TIME_TO_LIVE
from collective_folderprotection import _


class RenderPasswordView(BrowserView):
    def __call__(self):
        self.came_from = self.request.get("URL")

        self.request.set("came_from", self.came_from)
        # Get the object for which we need to get access to
        ob = getattr(self.__parent__, self.context.name)
        prompt = getMultiAdapter((ob, self.request), name="passwordprompt")
        return prompt()


class AskForPasswordView(BrowserView):
    """
    """

    def __call__(self):
        if self.request.get("submit", False):
            # The password was submitted
            passw = self.request.get("password", "")
            if six.PY3:
                passw_hash = md5(passw.encode()).hexdigest()
            else:
                passw_hash = md5(passw).hexdigest()

            password_protected = None

            context = self.context

            # This will be true if DX and pw-protected enabled
            password_protected = IPasswordProtected(context, None)
            if not password_protected:
                # It could be that this is the default view for the
                # protected parent, so let's try that
                parent_dp = context.aq_parent.getDefaultPage()
                if parent_dp == context.id:
                    context = context.aq_parent
                    # This will be true if DX and pw-protected enabled
                    password_protected = IPasswordProtected(context, None)

            if password_protected:
                if password_protected.is_password_protected():
                    # If this is not true, means the Manager has not
                    # set a password for this resource yet, then do
                    # not authenticate...
                    # If there's no came_from, then just go to the
                    # object itself
                    came_from = self.request.get(
                        "came_from", context.absolute_url()
                    )
                    if passw_hash == password_protected.passw_hash:
                        # The user has entered a valid password, then
                        # we store a random hash with a TTL so we know
                        # he already authenticated
                        ann = IAnnotations(context)
                        hashes = ann.get(HASHES_ANNOTATION_KEY, {})
                        if six.PY3:
                            random_hash = md5(
                                str(random()).encode()
                            ).hexdigest()
                        else:
                            random_hash = md5(str(random())).hexdigest()
                        while random_hash in hashes:
                            # This would be *REALLY* hard to happen,
                            # but just in case...
                            if six.PY3:
                                random_hash = md5(
                                    str(random()).encode()
                                ).hexdigest()
                            else:
                                random_hash = md5(str(random())).hexdigest()

                        hashes[random_hash] = datetime.now() + TIME_TO_LIVE
                        # Store the hash in the annotation
                        ann[HASHES_ANNOTATION_KEY] = hashes
                        if context is not self.context:
                            # Also store the hash in the default view
                            # object, if that's the case
                            ann = IAnnotations(self.context)
                            ann[HASHES_ANNOTATION_KEY] = hashes

                        # Save the hash in a cookie
                        path = context.getPhysicalPath()
                        virtual_path = self.request.physicalPathToVirtualPath(
                            path
                        )
                        options = {
                            "path": "/".join(("",) + virtual_path),
                            "expires": (DateTime("GMT") + 5).rfc822(),
                        }
                        self.request.response.setCookie(
                            HASH_COOKIE_KEY, random_hash, **options
                        )
                        # Now that we have our cookie set, go to
                        # the original url
                        self.request.response.redirect(came_from)
                        return
                    else:
                        # Invalid password, stay here, but mantain
                        # the "came_from"
                        self.request.set("came_from", came_from)

        self.request.response.setStatus(401, lock=True)
        return self.index()


class AssignPasswordForm(form.Form):

    fields = field.Fields(IPasswordProtected)

    ignoreContext = False

    @button.buttonAndHandler(_("Save"), name="save")
    def save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _(u"Please correct errors")
            return
        passw = data.get("passw_hash", "")
        reset_passw = data.get("reset_password", "")
        passw_behavior = IPasswordProtected(self.context)

        if passw and passw != "":
            passw_behavior.assign_password(passw)
            self.status = _(u"Password assigned.")

        if reset_passw:
            passw_behavior.remove_password()
            self.status = _(
                u"This content is not going to be password protected."
            )

    @button.buttonAndHandler(_("Cancel"), name="cancel")
    def cancel(self, action):
        self.status = _(u"Cancelled.")


AssignPasswordFormView = wrap_form(AssignPasswordForm)


class IAssignPasswordValidation(Interface):
    def allowed():
        """ Decide when to show the Assign password tab"""


class AssignPasswordValidation(BrowserView):
    def allowed(self):
        obj_is_protected = False
        authorized = False

        # First we check if the current context has the password
        # protection enabled
        try:
            # This will be true if DX and pw-protected enabled
            IPasswordProtected(self.context)
            obj_is_protected = True
        except TypeError:
            pass

        if obj_is_protected:
            # Only allow to set password to Manager or Owner
            pm = self.context.portal_membership
            roles = pm.getAuthenticatedMember().getRolesInContext(self.context)
            if "Manager" in roles or "Owner" in roles:
                authorized = True

        return authorized


@implementer(IContentIcon)
class PasswordProtectedIcon(CatalogBrainContentIcon):
    def __init__(self, context, request, brain):
        self.context = context
        self.request = request
        self.brain = brain
        self.has_protection_enabled = False
        self.is_protected = False

        portal_types = self.context.portal_types
        portal_type = self.brain.portal_type
        behaviors = getattr(portal_types[portal_type], "behaviors", None)

        if (
            behaviors
            and "collective_folderprotection.behaviors.interfaces.IPasswordProtected"  # noqa: E501
            in behaviors
        ):
            self.has_protection_enabled = True
            ob = self.brain.getObject()
            passwordprotected = IPasswordProtected(ob)

            if passwordprotected.is_password_protected():
                self.is_protected = True

    @property
    def url(self):
        if not self.has_protection_enabled:
            return super(PasswordProtectedIcon, self).url

        if self.is_protected:
            path = "++resource++resources/lock_locked_16.png"
        else:
            path = "++resource++resources/lock_unlocked_16.png"

        portal_state_view = getMultiAdapter(
            (self.context, self.request), name=u"plone_portal_state"
        )
        portal_url = portal_state_view.portal_url()
        return "%s/%s" % (portal_url, path)

    @property
    def description(self):
        if not self.has_protection_enabled:
            return super(PasswordProtectedIcon, self).description

        if self.is_protected:
            return "%s protected by password." % self.brain["portal_type"]
        else:
            return "%s not protected by password." % self.brain["portal_type"]
