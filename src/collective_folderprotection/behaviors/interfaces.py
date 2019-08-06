from z3c.form.interfaces import IEditForm, IAddForm

from zope import schema
from zope.interface import alsoProvides

from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider

from plone.supermodel import model

from collective_folderprotection import _


class IPasswordProtected(model.Schema):
    """Behavior interface to enable password protection"""

    passw_hash = schema.Password(
        title=_(u"Password"),
        description=_(
            u"Choose a password to protect this object and, if it is a "
            u"folder, its children."
        ),
        required=False,
    )
    reset_password = schema.Bool(
        title=_(u"Reset password"),
        description=_(u"Check to remove password protection here."),
        required=False,
    )

    form.omitted("passw_hash")
    form.omitted("reset_password")
    form.no_omit(IEditForm, "passw_hash")
    form.no_omit(IEditForm, "reset_password")
    form.no_omit(IAddForm, "passw_hash")


alsoProvides(IPasswordProtected, IFormFieldProvider)


class IDeleteProtected(model.Schema):
    """Marker interface to enable delete protection behavior"""

    delete_protection = schema.Bool(
        title=_(u"Delete protection"),
        description=_(
            u"Mark this checkbox if you want to protect this object, and its "
            u"children (if this is a folder) from being deleted. NOTE: In "
            u"folders, the delete protection will only protect direct "
            u"children, it will not recurse into subfolders."
        ),
        required=False,
    )

    form.omitted("delete_protection")
    form.no_omit(IEditForm, "delete_protection")
    form.no_omit(IAddForm, "delete_protection")


alsoProvides(IDeleteProtected, IFormFieldProvider)


class IRenameProtected(model.Schema):
    """Marker interface to enable rename protection behavior"""

    rename_protection = schema.Bool(
        title=_(u"Rename protection"),
        description=_(
            u"Mark this checkbox if you want to protect this object, and its "
            u"children (if this is a folder) from being renamed. NOTE: In "
            u"folders, the rename protection will only protect direct "
            u"children, it will not recurse into subfolders."
        ),
        required=False,
    )

    form.omitted("rename_protection")
    form.no_omit(IEditForm, "rename_protection")
    form.no_omit(IAddForm, "rename_protection")


alsoProvides(IRenameProtected, IFormFieldProvider)
