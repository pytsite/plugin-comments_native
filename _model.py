"""PytSite ODM Comments Plugin Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Iterable
from datetime import datetime
from pytsite import router
from plugins import odm, auth, comments, auth_storage_odm, odm_ui
from plugins.odm_auth import PERM_MODIFY, PERM_DELETE


class ODMComment(odm_ui.UIEntity):
    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'comments'

    def _setup_fields(self):
        """Setup fields
        """
        valid_statuses = tuple(comments.get_comment_statuses().keys())
        min_body_len = comments.get_comment_min_body_length()
        max_body_len = comments.get_comment_max_body_length()

        self.define_field(odm.field.String('thread_uid', is_required=True))
        self.define_field(odm.field.Enum('status', is_required=True, default='published', values=valid_statuses))
        self.define_field(odm.field.String('body', is_required=True, min_length=min_body_len, max_length=max_body_len))
        self.define_field(odm.field.DateTime('publish_time', is_required=True, default=datetime.now()))
        self.define_field(auth_storage_odm.field.User('author', is_required=True))

    def _setup_indexes(self):
        """Setup indexes.
        """
        self.define_index([('thread_uid', odm.I_ASC), ('status', odm.I_ASC)])
        self.define_index([('publish_time', odm.I_ASC)])
        self.define_index([('author', odm.I_ASC)])


class Comment(comments.AbstractComment):
    @property
    def author(self) -> auth.AbstractUser:
        return self._entity.f_get('author')

    @property
    def body(self) -> str:
        return self._entity.f_get('body')

    @property
    def children(self) -> Iterable[comments.AbstractComment]:
        for c in self._entity.children:  # type: ODMComment
            yield Comment(c)

    @property
    def created(self) -> datetime:
        return self._entity.created

    @property
    def depth(self) -> int:
        return self._entity.depth

    @property
    def parent_uid(self) -> str:
        return str(self._entity.parent.id) if self._entity.parent else None

    @property
    def permissions(self) -> dict:
        return {
            PERM_MODIFY: self._entity.odm_auth_check_entity_permissions(PERM_MODIFY),
            PERM_DELETE: self._entity.odm_auth_check_entity_permissions(PERM_DELETE),
        }

    @property
    def publish_time(self) -> datetime:
        return self._entity.f_get('publish_time')

    @property
    def status(self) -> str:
        return self._entity.f_get('status')

    @property
    def thread_uid(self) -> str:
        return self._entity.f_get('thread_uid')

    @property
    def uid(self) -> str:
        return str(self._entity.id)

    @property
    def url(self) -> str:
        return router.url(self._entity.f_get('thread_uid'), fragment='comment-' + self.uid)

    def __init__(self, odm_entity: ODMComment):
        """Init
        """
        self._entity = odm_entity

    def delete(self):
        self._entity.f_set('status', comments.COMMENT_STATUS_DELETED)
