"""PytSite ODM Comments Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang
from plugins import widget2, comments, http_api, auth, auth_ui


class Comments(widget2.Container):
    def __init__(self, uid: str = None, **kwargs):
        """Init.
        """
        kwargs.setdefault('title', lang.t('comments_odm@comments'))

        super().__init__(uid, **kwargs)

        thread_uid = kwargs.get('thread_uid')

        self._props.update({
            'authenticationURL': auth_ui.sign_in_url(),
            'isUserAuthenticated': not auth.get_current_user().is_anonymous,
            'settings': {
                'maxBodyLength': comments.get_comment_max_body_length(),
                'minBodyLength': comments.get_comment_min_body_length(),
                'maxDepth': comments.get_comment_max_depth(),
                'statuses': comments.get_comment_statuses(),
                'permissions': comments.get_permissions(driver_name='odm')
            },
            'urls': {
                'get': http_api.url('comments@get_comments', {'thread_uid': thread_uid}),
                'post': http_api.url('comments@post_comment', {'thread_uid': thread_uid}),
            },
            'threadUID': kwargs.get('thread_uid'),
            'title': kwargs.get('title'),
        })
