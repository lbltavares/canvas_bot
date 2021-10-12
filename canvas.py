import config
from canvasapi import Canvas

from logger import LoggerFactory

_log = LoggerFactory.get_default_logger(__name__, filename=config.get(
    'log_filename', 'app.log') if config.get('unique_log_file') else None)
_log.setLevel(config.get('canvas_log_level', 'INFO'))

canvas = Canvas(
    base_url=config.get('canvas_url'),
    access_token=config.get('canvas_token')
)
