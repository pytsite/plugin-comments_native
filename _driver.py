"""PytSite Native Comments Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Iterable as _Iterable
from plugins import widget as _widget, auth as _auth, odm as _odm, comments as _comments, odm_auth as _odm_auth
from . import _model
from ._widget import Comments as _CommentsWidget


class Native(_comments.driver.Abstract):
    """Abstract Comments Driver.
    """

    def get_name(self) -> str:
        """Get driver's name.
        """
        return 'pytsite'

    def get_description(self) -> str:
        """Get driver's description.
        """
        return 'PytSite'

    def create_comment(self, thread_uid: str, body: str, author: _auth.model.AbstractUser, status: str = 'published',
                       parent_uid: str = None) -> _comments.model.AbstractComment:
        """Create new comment.
        """
        body = body.strip()

        comment = _odm.dispense('comment')  # type: _model.Comment
        comment.f_set('thread_uid', thread_uid)
        comment.f_set('body', body)
        comment.f_set('author', author.uid)
        comment.f_set('status', status)
        comment.save()

        if parent_uid:
            parent = _odm.get_by_ref('comment:' + parent_uid)
            if parent.depth == _comments.get_comment_max_depth():
                raise RuntimeError('Comment depth is too big')

            try:
                _auth.switch_user_to_system()
                parent.append_child(comment).save()
            finally:
                _auth.restore_user()

        return comment

    def get_widget(self, widget_uid: str, thread_uid: str) -> _widget.Abstract:
        """Get comments widget.
        """
        return _CommentsWidget(widget_uid, thread_id=thread_uid)

    def get_comments(self, thread_uid: str, limit: int = 0, skip: int = 0) -> _Iterable[_model.Comment]:
        """Get comments.
        """
        f = _odm.find('comment').eq('thread_uid', thread_uid).sort([('publish_time', _odm.I_ASC)]).skip(skip)

        return f.get(limit)

    def get_comment(self, uid: str) -> _comments.model.AbstractComment:
        """Get single comment by UID.
        """
        comment = _odm.find('comment').eq('_id', uid).first()

        if not comment:
            raise _comments.error.CommentNotExist("Comment '{}' not exist.".format(uid))

        return comment

    def get_comments_count(self, thread_uid: str) -> int:
        """Get comments count for particular thread.
        """
        return _odm.find('comment').eq('thread_uid', thread_uid).eq('status', 'published').count()

    def delete_comment(self, uid: str):
        """Mark comment as deleted.
        """
        comment = _odm.find('comment').eq('_id', uid).first()
        if not comment:
            raise _comments.error.CommentNotExist("Comment '{}' does not exist.".format(uid))

        comment.f_set('status', 'deleted').save()

    def delete_thread(self, thread_uid: str):
        """Physically remove comments for particular thread.
        """
        for comment in self.get_comments(thread_uid):
            try:
                comment.delete()
            except _odm.error.EntityDeleted:
                # Entity was deleted by another instance
                pass

    def get_permissions(self, user: _auth.model.AbstractUser = None) -> dict:
        """Get permissions definition for user.
        """
        return {
            'create': _odm_auth.check_permission('create', 'comment', user=user)
        }
