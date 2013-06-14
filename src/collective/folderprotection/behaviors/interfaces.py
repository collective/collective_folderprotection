
from zope import schema
from zope.interface import Interface
from zope.interface import implements

from collective.folderprotection import _


class IPasswordProtected(Interface):
    """Marker interface to enable password protected behavior"""

    password = schema.Password(
            title=_(u"Password"),
            description=_(u"Choose a password to protect this object and, if it is a folder, its children."),
            required=False,
        )
