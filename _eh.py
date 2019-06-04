"""PytSite ODM Comments Plugin Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import mail, tpl, lang
from plugins import auth, comments, query


def comments_report_comment(uid: str):
    try:
        comment = comments.get_comment(uid, 'pytsite')
    except comments.error.CommentNotExist:
        return

    tpl_name = 'comments_odm@mail/{}/report'.format(lang.get_current())
    m_subject = lang.t('comments_odm@mail_subject_report_comment')

    for user in auth.find_users(query.Query(query.Eq('status', 'active'))):
        if not user.has_permission('odm_auth@delete.comment'):
            continue

        m_body = tpl.render(tpl_name, {'comment': comment, 'recipient': user})
        mail.Message(user.login, m_subject, m_body).send()
