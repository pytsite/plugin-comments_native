"""PytSite Native Comments Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _register_resources():
    from pytsite import lang
    from plugins import assetman

    if not lang.is_package_registered(__name__):
        lang.register_package(__name__)

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_less(__name__)
        assetman.t_js(__name__)
        assetman.js_module('comments-native-widget', __name__ + '@js/comments-native-widget')

    return assetman


def plugin_install():
    from plugins import auth, assetman

    # Allow ordinary users to create, modify and delete comments
    auth.switch_user_to_system()
    user_role = auth.get_role('user')
    user_role.permissions = list(user_role.permissions) + [
        'odm_auth.create.comment',
        'odm_auth.modify_own.comment',
        'odm_auth.delete_own.comment',
    ]
    user_role.save()
    auth.restore_user()

    _register_resources()
    assetman.build(__name__)
    assetman.build_translations()


def plugin_load():
    from pytsite import tpl

    tpl.register_package(__name__)
    _register_resources()


def plugin_load_uwsgi():
    from pytsite import events
    from plugins import comments, odm
    from . import _model, _driver, _eh

    _register_resources()

    # Register ODM model
    odm.register_model('comment', _model.Comment)

    # Register comments driver
    comments.register_driver(_driver.Native())

    events.listen('comments@report_comment', _eh.comments_report_comment)
