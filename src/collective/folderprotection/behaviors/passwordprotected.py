from datetime import datetime

from zope.annotation import IAnnotations

from collective.folderprotection.config import HASHES_ANNOTATION_KEY
from collective.folderprotection.config import HASH_COOKIE_KEY


class PasswordProtected(object):

    def __init__(self, context):
        self.context = context

    def allowed_to_access(self):
        allowed = False
        request = self.context.REQUEST
        ann = IAnnotations(self.context)
        hashes = ann.get(HASHES_ANNOTATION_KEY, {})
        user_hash = request.cookies.get(HASH_COOKIE_KEY, None)
        
        if user_hash and user_hash in hashes:
            now = datetime.now()
            valid_until = hashes[user_hash]
            allowed = valid_until > now
            
        return allowed
