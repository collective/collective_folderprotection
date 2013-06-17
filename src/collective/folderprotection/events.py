# -*- coding: utf-8 -*-

from collective.folderprotection.behaviors.interfaces import IPasswordProtected
from collective.folderprotection.exceptions import PasswordProtectedUnauthorized


def checkPassword(portal, request):
    portal_path = '/'.join(portal.getPhysicalPath())
    # We get the full path
    full_path = request.get('PATH_INFO')
    if full_path.startswith(portal_path):
        # just strip the portal_path from the full_path and the '/'
        full_path = full_path[len(portal_path)+1:]
    ob = portal
    # Now iterate over each one
    for name in full_path.split('/'):
        try:
            ob = ob.restrictedTraverse(name)
        except AttributeError:
            # This path is not traversable, just ignore
            break
        try:
            authorized = False
            passwordprotected = IPasswordProtected(ob)
            # We are at a content type that is password protected, so
            # see if we are not actually at the passwordprompt view
            if "passwordprompt" not in full_path:
                # We are not at the passwordprotected prompt, so we now check
                # if the current user is not Manager or the Owner
                pm = portal.portal_membership
                roles = pm.getAuthenticatedMember().getRolesInContext(ob)
                if ('Manager' in roles or 'Owner' in roles):
                    # This user is the Owner or a Manager, so we just authorize
                    # it
                    authorized = True

                if not (authorized or passwordprotected.allowed_to_access()):
                    # User is not authorized to access this resource
                    #import pdb;pdb.set_trace()
                    raise PasswordProtectedUnauthorized(name=name)
        except TypeError:
            # Object does not provide behavior, so just continue
            pass

    return None

def insertCheckPasswordHook(portal, event):
    """ Add this hook to the post_traversal so we can check if some object
    during the traversal needs a password
    """
    event.request.post_traverse(checkPassword, (portal, event.request))