
from zope.interface import implements
from zope.interface.common.interfaces import IException

class IPasswordProtectedUnauthorized(IException):
    """
    """


class PasswordProtectedUnauthorized(Exception):
    implements(IPasswordProtectedUnauthorized)
    
    def _get_message(self):
        return self._message

    message = property(_get_message,)

    def __init__(self, message=None, name=None):
        """Possible signatures:

        PasswordProtectedUnauthorized()
        PasswordProtectedUnauthorized(message)
        PasswordProtectedUnauthorized(name)
        PasswordProtectedUnauthorized(message, name)

        """

        self.name=name
        self._message=message

    def __str__(self):
        if self.message is not None:
            return self.message
        if self.name is not None:
            return ("You need a password to access '%s'"
                    % self.name)
        return repr(self)

    def __unicode__(self):
        result = self.__str__()
        if isinstance(result, unicode):
            return result
        return unicode(result, 'ascii') # override sys.getdefaultencoding()
