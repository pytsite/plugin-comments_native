"""Native Comments Event Handlers.
"""
from pytsite import mail as _mail, tpl as _tpl, lang as _lang, auth as _auth
from plugins import comments as _comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """`pytsite.setup` event handler.
    """
    # Allow ordinary users to create, modify and delete comments
    user_role = _auth.get_role('user')
    user_role.permissions = list(user_role.permissions) + [
        'pytsite.odm_auth.create.comment',
        'pytsite.odm_auth.modify_own.comment',
        'pytsite.odm_auth.delete_own.comment',
    ]

    _auth.switch_user_to_system()
    user_role.save()
    _auth.restore_user()


def comments_report_comment(uid: str):
    try:
        comment = _comments.get_comment(uid, 'pytsite')
    except _comments.error.CommentNotExist:
        return

    tpl_name = 'comments_native@mail/{}/report'.format(_lang.get_current())
    m_subject = _lang.t('comments_native@mail_subject_report_comment')

    for user in _auth.get_users({'status': 'active'}):
        if not user.has_permission('pytsite.odm_auth.delete.comment'):
            continue

        m_body = _tpl.render(tpl_name, {'comment': comment, 'recipient': user})
        _mail.Message(user.email, m_subject, m_body).send()
