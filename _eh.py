"""PytSite Native Comments Plugin Events Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import mail as _mail, tpl as _tpl, lang as _lang
from plugins import auth as _auth, comments as _comments, query as _query


def comments_report_comment(uid: str):
    try:
        comment = _comments.get_comment(uid, 'pytsite')
    except _comments.error.CommentNotExist:
        return

    tpl_name = 'comments_native@mail/{}/report'.format(_lang.get_current())
    m_subject = _lang.t('comments_native@mail_subject_report_comment')

    for user in _auth.find_users(_query.Query(_query.Eq('status', 'active'))):
        if not user.has_permission('odm_auth@delete.comment'):
            continue

        m_body = _tpl.render(tpl_name, {'comment': comment, 'recipient': user})
        _mail.Message(user.login, m_subject, m_body).send()
