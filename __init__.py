"""PytSite Comments ODM Driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, tpl, assetman, events, lang
    from plugins import comments
    from . import _model, _driver, _eh

    # Resources
    lang.register_package(__name__, alias='comments_native')
    tpl.register_package(__name__, alias='comments_native')

    assetman.register_package(__name__, alias='comments_native')
    assetman.t_less(__name__ + '@css/**', 'css')
    assetman.t_js(__name__ + '@js/**', 'js')
    assetman.js_module('comments-native-widget', __name__ + '@js/comments-native-widget')

    # Register ODM model
    odm.register_model('comment', _model.Comment)

    # Register comments driver
    comments.register_driver(_driver.Native())

    events.listen('pytsite.setup', _eh.setup)
    events.listen('comments.report_comment', _eh.comments_report_comment)


_init()
