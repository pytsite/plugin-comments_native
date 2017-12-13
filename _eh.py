"""PytSite Native Comments Plugin Events Handlers
"""
from pytsite import mail as _mail, tpl as _tpl, lang as _lang
from plugins import auth as _auth, comments as _comments

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def comments_report_comment(uid: str):
    try:
        comment = _comments.get_comment(uid, 'pytsite')
    except _comments.error.CommentNotExist:
        return

    tpl_name = 'comments_native@mail/{}/report'.format(_lang.get_current())
    m_subject = _lang.t('comments_native@mail_subject_report_comment')

    for user in _auth.get_users({'status': 'active'}):
        if not user.has_permission('odm_auth.delete.comment'):
            continue

        m_body = _tpl.render(tpl_name, {'comment': comment, 'recipient': user})
        _mail.Message(user.email, m_subject, m_body).send()
