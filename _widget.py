"""PytSite ODM Comments Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang
from plugins import widget2 as _widget2, comments as _comments, http_api as _http_api, auth as _auth, \
    auth_ui as _auth_ui


class Comments(_widget2.Base):
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        kwargs.setdefault('title', _lang.t('comments_odm@comments'))

        super().__init__(uid, **kwargs)

        thread_uid = kwargs.get('thread_uid')

        self._props.update({
            'authenticationURL': _auth_ui.sign_in_url(),
            'isUserAuthenticated': not _auth.get_current_user().is_anonymous,
            'settings': {
                'maxBodyLength': _comments.get_comment_max_body_length(),
                'minBodyLength': _comments.get_comment_min_body_length(),
                'maxDepth': _comments.get_comment_max_depth(),
                'statuses': _comments.get_comment_statuses(),
                'permissions': _comments.get_permissions(driver_name='odm')
            },
            'urls': {
                'get': _http_api.url('comments@get_comments', {'thread_uid': thread_uid}),
                'post': _http_api.url('comments@post_comment', {'thread_uid': thread_uid}),
            },
            'threadUID': kwargs.get('thread_uid'),
            'title': kwargs.get('title'),
        })
