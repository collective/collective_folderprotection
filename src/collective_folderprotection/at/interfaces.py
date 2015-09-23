
from z3c.form.interfaces import IEditForm, IAddForm

from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.interface import implements

from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider

from plone.supermodel import model

from collective_folderprotection import _


class IATPasswordProtected(Interface):
    """Interface for protecting a folder with a password"""

    passw_hash = schema.Password(
            title=_(u"Password"),
            description=_(u"Choose a password to protect this object and, if it is a folder, its children."),
            required=False,
        )
    reset_password = schema.Bool(
            title=_(u"Reset password"),
            description=_(u"Check to remove password protection here."),
            required=False,
        )


class IATDeleteProtected(Interface):
    """Marker interface to enable delete protection"""


class IATRenameProtected(Interface):
    """Marker interface to enable rename protection"""
