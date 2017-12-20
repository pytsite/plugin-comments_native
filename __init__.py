"""PytSite Native Comments Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import tpl, lang
    from plugins import assetman

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__)
    assetman.t_js(__name__)
    assetman.js_module('comments-native-widget', __name__ + '@js/comments-native-widget')


def plugin_load_uwsgi():
    from pytsite import events
    from plugins import comments, odm
    from . import _model, _driver, _eh

    # Register ODM model
    odm.register_model('comment', _model.Comment)

    # Register comments driver
    comments.register_driver(_driver.Native())

    events.listen('comments@report_comment', _eh.comments_report_comment)


def plugin_install():
    from plugins import auth, assetman

    plugin_load()

    # Allow ordinary users to create, modify and delete comments
    user_role = auth.get_role('user')
    user_role.permissions = list(user_role.permissions) + [
        'odm_auth.create.comment',
        'odm_auth.modify_own.comment',
        'odm_auth.delete_own.comment',
    ]

    auth.switch_user_to_system()
    user_role.save()
    auth.restore_user()

    assetman.build(__name__)
    assetman.build_translations()
