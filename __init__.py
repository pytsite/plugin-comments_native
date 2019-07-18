"""PytSite ODM Comments Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _widget as widget


def plugin_load():
    """Hook
    """
    from pytsite import events
    from plugins import comments, odm
    from . import _model, _driver, _eh

    # Register ODM model
    odm.register_model('comment', _model.ODMComment)

    # Register comments driver
    comments.register_driver(_driver.ODM())

    events.listen('comments@report_comment', _eh.comments_report_comment)
