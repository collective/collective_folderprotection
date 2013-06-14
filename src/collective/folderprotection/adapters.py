
from collective.folderprotection.behaviors.interfaces import IPasswordProtected

from ZPublisher.BaseRequest import DefaultPublishTraverse

from collective.folderprotection.exceptions import PasswordProtectedUnauthorized


class FolderprotectPublishTraverse(DefaultPublishTraverse):
    
    def publishTraverse(self, request, name):

        ob = super(FolderprotectPublishTraverse, self).publishTraverse(request, name)

        try:
            passwordprotected = IPasswordProtected(ob)
            # We are at a content type that is password protected, so
            # see if we are not actually at the passwordprompt view
            full_path = self.request.get('PATH_INFO')
            if "passwordprompt" not in full_path:
                # We are not at the passwordprotected prompt, so we now check
                # if the current user is not Manager or the Owner
                # XXX: Is there a better way of doing this?
                authorized = False
                auth=self.request._authUserPW()
                if auth:
                    pm = self.context.portal_membership
                    roles = pm.getMemberById(auth[0]).getRolesInContext(ob)
                    if ('Manager' in roles or 'Owner' in roles):
                        # This user is not the Owner nor a Manager, so we check
                        # if he's allowed to get further
                        authorized = True
                if not (authorized or passwordprotected.allowed_to_access()):
                    # User is not authorized to access this resource
                    raise PasswordProtectedUnauthorized(name=name)

        except TypeError:
            # Object does not provide behavior, so just continue
            pass

        return ob