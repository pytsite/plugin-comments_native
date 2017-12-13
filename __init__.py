"""PytSite Native Comments Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import tpl, events, lang
    from plugins import assetman, comments, odm
    from . import _model, _driver, _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_less(__name__)
    assetman.t_js(__name__)
    assetman.js_module('comments-native-widget', __name__ + '@js/comments-native-widget')

    # Register ODM model
    odm.register_model('comment', _model.Comment)

    # Register comments driver
    comments.register_driver(_driver.Native())

    events.listen('comments@report_comment', _eh.comments_report_comment)
